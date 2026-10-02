#!/usr/bin/env python3
"""T4-P2 harness: behavioural assertions K1-K7 for pgvector and Qdrant.

Usage:  run_t4.py <output-dir>     (a fresh directory)

Evidence kinds, kept apart:
  retrieval observed  the documents' content appears in the system prompt the
                      stub gateway received (journal), AND the recorder shows the
                      engine returned them. A successful response alone is never
                      retrieval: failures degrade silently by default.
  recorder evidence   what each engine returned (ids, sources, metadata), from the
                      harness-owned, non-interfering T4 recorder. Recorder errors or
                      sequence gaps make dependent assertions INCOMPLETE.
  behaviour vs containment
                      every K assertion has its own outcome; containment (the
                      interface inventory) is reported separately.

Outcomes: PASS, FAIL, INCOMPLETE, OBSERVATION. Pass rules are fixed here, before
execution. Results are written after every assertion and on any exception.
"""
import hashlib
import json
import os
import secrets
import signal
import subprocess
import sys
import time
import traceback
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXT = HERE.parent
CORPUS, QUERIES = EXT / "t4-corpus.json", EXT / "t4-queries.json"
FROZEN = EXT / "t4.frozen.sha256.md"
PROTOTYPES = Path(os.environ.get("PROTOTYPES", Path.home() / "Desktop" / "AI Projects"))
RUNTIME = PROTOTYPES / "Enterprise_AI_Runtime_Service"

PG_IMAGE = "pgvector/pgvector:0.8.6-pg16@sha256:ccc6e83d6e35e931dc7c5def2022729d5a6c370318d099181995567ff1fb4d6b"
QD_IMAGE = "qdrant/qdrant:v1.19.1@sha256:12364fe851b9f17356fc88189fc06d1b521262e04659ec7345975b00c9246a10"
PG_NAME, QD_NAME = "t4-pgvector", "t4-qdrant"
STUB_PORT, PG_PORT, QD_PORT, RT_PORT = 18180, 15432, 16333, 18181

# K5: text that would show a raw engine or transport error reaching the API.
RAW_ERROR_MARKERS = ["PSQLException", "org.postgresql", "SQLException", "Connection refused",
                     "ConnectException", "WebClientRequestException", "WebClientResponseException",
                     "io.netty", "java.net.", "Exception:"]
# Not a marker: the strategy name ("pgvector", "qdrant"), which the declared
# degraded mark legitimately carries (retrieval.degraded=<strategy>).
DECLARED_RETRIEVAL_ERROR = "retrieval_error"
CONCEALMENT_KEYS = ["purpose", "input_type", "inputtype", "task", "embedding_type"]


class Harness:
    def __init__(self, out):
        self.out = out
        self.results = {"_run": {"status": "started", "phase": None, "recorder_errors": [],
                                 "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}}
        self.proc = self.stub = None
        self.rec_file = self.rt_log = None
        self.last_seq, self.log_offset = 0, 0
        self.corpus = {d["id"]: d for d in json.loads(CORPUS.read_text())["documents"]}
        self.queries = json.loads(QUERIES.read_text())
        self.java = Path(os.environ.get("JAVA_HOME") or self.maven_java_home()) / "bin" / "java"
        self.pg_password = secrets.token_hex(12)          # test-only, never recorded

    # ------------------------------------------------------------ plumbing
    @staticmethod
    def maven_java_home():
        out = subprocess.run(["mvn", "-v"], capture_output=True, text=True).stdout
        return next(l.split("runtime: ", 1)[1].strip() for l in out.splitlines() if "runtime: " in l)

    def log(self, msg):
        line = f"[{time.strftime('%H:%M:%S', time.gmtime())}Z] {msg}"
        print(line, flush=True)
        with open(self.out / "harness.log", "a") as f:
            f.write(line + "\n")

    def write(self):
        (self.out / "results.json").write_text(json.dumps(self.results, indent=2, default=str))

    def phase(self, name):
        self.results["_run"]["phase"] = name
        self.write()
        self.log(f"--- phase: {name}")

    def record(self, key, outcome, evidence):
        assert outcome in ("PASS", "FAIL", "INCOMPLETE", "OBSERVATION", "NOT_EXERCISABLE")
        self.results[key] = {"outcome": outcome, "evidence": evidence}
        self.write()
        self.log(f"== {key}: {outcome}")

    def sh(self, *args, check=True):
        return subprocess.run(args, capture_output=True, text=True, check=check).stdout.strip()

    def http(self, method, url, body=None, headers=None, timeout=30):
        data = None if body is None else json.dumps(body).encode()
        req = urllib.request.Request(url, data=data, method=method, headers=headers or {})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.status, r.read().decode()
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode()
        except Exception as e:
            return 0, str(e)

    def wait(self, probe, seconds, what):
        deadline = time.time() + seconds
        while time.time() < deadline:
            try:
                if probe():
                    return
            except Exception:
                pass
            time.sleep(1)
        raise TimeoutError(f"{what} did not become ready")

    # ------------------------------------------------------------ setup
    def verify_inputs(self):
        frozen = FROZEN.read_text()
        for f in (CORPUS, QUERIES):
            digest = hashlib.sha256(f.read_bytes()).hexdigest()
            if f"{digest}  {f.name}" not in frozen:
                raise RuntimeError(f"{f.name} digest {digest} is not the frozen one")
        if self.queries.get("topK") != 3:
            raise RuntimeError("topK must be 3 (frozen)")

    def build(self):
        subprocess.run(["mvn", "-q", "-o", "-pl", "runtime-api", "-am", "package", "-DskipTests"],
                       cwd=RUNTIME, check=True)
        self.jar = RUNTIME / "runtime-api" / "target" / "runtime-api-1.0.0-SNAPSHOT-app.jar"
        self.recorder_jar = Path(self.sh(str(HERE / "recorder" / "build-recorder.sh"),
                                         str(self.out / "recorder-build")).splitlines()[-1])
        run = self.results["_run"]
        run["runtime_revision"] = self.sh("git", "-C", str(RUNTIME), "rev-parse", "HEAD")
        run["runtime_jar_sha256"] = self.sh("shasum", "-a", "256", str(self.jar)).split()[0]
        run["recorder_jar_sha256"] = self.sh("shasum", "-a", "256", str(self.recorder_jar)).split()[0]

    def start_stub(self):
        self.stub = subprocess.Popen([sys.executable, str(HERE / "stub_gateway.py"), str(STUB_PORT)])
        self.wait(lambda: self.http("GET", f"http://127.0.0.1:{STUB_PORT}/v1/health")[0] == 200, 20, "stub gateway")

    def start_engines(self):
        for name in (PG_NAME, QD_NAME):
            subprocess.run(["docker", "rm", "-f", name], capture_output=True)
        self.sh("docker", "run", "-d", "--name", PG_NAME, "-p", f"{PG_PORT}:5432",
                "-e", "POSTGRES_USER=knowledge", "-e", f"POSTGRES_PASSWORD={self.pg_password}",
                "-e", "POSTGRES_DB=knowledge", PG_IMAGE)
        self.sh("docker", "run", "-d", "--name", QD_NAME, "-p", f"{QD_PORT}:6333", QD_IMAGE)
        self.wait(lambda: subprocess.run(["docker", "exec", PG_NAME, "pg_isready", "-U", "knowledge",
                                          "-d", "knowledge"], capture_output=True).returncode == 0, 90, "pgvector")
        self.wait(lambda: self.http("GET", f"http://127.0.0.1:{QD_PORT}/readyz")[0] == 200, 90, "qdrant")
        time.sleep(2)
        self.log(self.sh(sys.executable, str(HERE / "load_corpus.py"), PG_NAME, f"http://127.0.0.1:{QD_PORT}"))
        run = self.results["_run"]
        run["pgvector_image_id"] = self.sh("docker", "inspect", "--format", "{{.Image}}", PG_NAME)
        run["qdrant_image_id"] = self.sh("docker", "inspect", "--format", "{{.Image}}", QD_NAME)

    def start_runtime(self, label, engine, fail_on_error):
        env = dict(os.environ, SERVER_PORT=str(RT_PORT), RUNTIME_ENVIRONMENT="integration",
                   RUNTIME_SECURITY_MODE="NONE", RUNTIME_CACHE_PROVIDER="caffeine",
                   MODEL_GATEWAY_URL=f"http://127.0.0.1:{STUB_PORT}",
                   RUNTIME_RETRIEVAL_ENGINE=engine,
                   RUNTIME_RETRIEVAL_FAIL_ON_ERROR=str(fail_on_error).lower(),
                   RUNTIME_RETRIEVAL_ENGINES_PGVECTOR_URL=f"jdbc:postgresql://127.0.0.1:{PG_PORT}/knowledge",
                   RUNTIME_RETRIEVAL_ENGINES_PGVECTOR_USERNAME="knowledge",
                   RUNTIME_RETRIEVAL_ENGINES_PGVECTOR_PASSWORD=self.pg_password,
                   RUNTIME_RETRIEVAL_ENGINES_QDRANT_URL=f"http://127.0.0.1:{QD_PORT}")
        self.rec_file = self.out / f"recorder-{label}.jsonl"
        self.rt_log = self.out / f"runtime-{label}.log"
        self.last_seq, self.log_offset = 0, 0
        logf = open(self.rt_log, "w")
        self.proc = subprocess.Popen(
            [str(self.java), "-cp", str(self.jar), f"-Dloader.path={self.recorder_jar}",
             f"-Dt4.instance={label}", f"-Dt4.recorder.out={self.rec_file}",
             "org.springframework.boot.loader.launch.PropertiesLauncher"],
            env=env, stdout=logf, stderr=subprocess.STDOUT)
        self.wait(lambda: self.http("GET", f"http://127.0.0.1:{RT_PORT}/v1/ready")[0] == 200, 120, "runtime")
        events = self.events(0)
        installed = [e for e in events if e["event"] == "recorder-installed"]
        self.startup_ok = self.integrity(events)[0] and any(e.get("strategy") == engine for e in installed)
        self.results["_run"].setdefault("recorder_startup", {})[label] = {
            "clean": self.startup_ok, "installed": [e.get("strategy") for e in installed]}
        self.log(f"runtime {label} ready: engine={engine} fail_on_error={fail_on_error} "
                 f"installed={[e.get('strategy') for e in installed]}")

    def stop_runtime(self):
        if self.proc:
            self.proc.send_signal(signal.SIGTERM)
            try:
                self.proc.wait(timeout=60)
            except subprocess.TimeoutExpired:
                self.proc.kill()
            self.proc = None

    def cleanup(self):
        self.stop_runtime()
        if self.stub:
            self.stub.terminate()
        for name in (PG_NAME, QD_NAME):
            subprocess.run(["docker", "rm", "-f", name], capture_output=True)

    # ------------------------------------------------------------ evidence
    def events(self, offset):
        if not self.rec_file or not self.rec_file.exists():
            return []
        with open(self.rec_file) as f:
            f.seek(offset)
            return [json.loads(l) for l in f.read().splitlines() if l.strip()]

    def integrity(self, events):
        problems = []
        if self.rt_log and self.rt_log.exists():
            with open(self.rt_log, errors="replace") as f:
                f.seek(self.log_offset)
                problems += [l.strip() for l in f.read().splitlines() if "T4-RECORDER-ERROR" in l]
                self.log_offset = f.tell()
        for e in events:
            if e.get("seq") != self.last_seq + 1:
                problems.append(f"sequence gap: expected {self.last_seq + 1}, got {e.get('seq')}")
            self.last_seq = e.get("seq", self.last_seq + 1)
        self.results["_run"]["recorder_errors"] += problems
        return not problems, problems

    def journal(self):
        return json.loads(self.http("GET", f"http://127.0.0.1:{STUB_PORT}/__journal")[1])

    def ask(self, query, name):
        """One governed retrieval request; returns the evidence of every kind."""
        offset = self.rec_file.stat().st_size if self.rec_file.exists() else 0
        before = len(self.journal())
        payload = {"promptId": "policy-qa", "cacheable": False,
                   "messages": [{"role": "user", "content": query["query"]}],
                   "rag": {"enabled": True, "query": query["query"], "topK": self.queries["topK"]}}
        headers = {"Content-Type": "application/json", "X-Enterprise-AI-Application": "retail-dashboard",
                   "X-Enterprise-AI-Use-Case": "policy-qa", "X-Enterprise-AI-Environment": "integration",
                   "X-Enterprise-AI-Region": "australia", "X-Enterprise-AI-Tenant": query["tenant"]}
        status, body = self.http("POST", f"http://127.0.0.1:{RT_PORT}/v1/chat", payload, headers)
        time.sleep(0.3)
        new = self.journal()[before:]
        chats = [j["body"] for j in new if j["path"] == "/v1/inference/chat"]
        embeds = [j["body"] for j in new if j["path"] == "/v1/inference/embeddings"]
        events = self.events(offset)
        ok, problems = self.integrity(events)
        if not self.startup_ok:
            ok, problems = False, problems + ["recorder startup was not clean"]
        returned = [e for e in events if e["event"] == "retrieve-returned"]
        errors = [e for e in events if e["event"] == "retrieve-error"]
        system = chats[-1].get("system", "") if chats else ""
        in_prompt = sorted(i for i, d in self.corpus.items() if d["content"] in system)
        (self.out / "responses" / f"{name}.json").write_text(body)
        parsed = json.loads(body) if body.startswith("{") else {}
        rec_ids = [d["id"] for e in returned for d in e["documents"]]
        self.log(f"{name}: HTTP {status} recorder={rec_ids} prompt={in_prompt} errors={len(errors)}")
        return {"status": status, "body": parsed, "raw": body, "recorder_ok": ok, "recorder_problems": problems,
                "recorder_docs": [d for e in returned for d in e["documents"]], "recorder_ids": rec_ids,
                "recorder_errors": [e["error"] for e in errors], "prompt_ids": in_prompt, "embeds": embeds}

    # ------------------------------------------------------------ assertions
    def engine_assertions(self, engine):
        per, failed_k1, failed_k2, failed_k4, unmeasured = {}, [], [], [], []
        for q in self.queries["queries"]:
            r = self.ask(q, f"{engine}-{q['id']}")
            per[q["id"]] = r
            if not r["recorder_ok"]:
                unmeasured.append(q["id"])
            other = [i for i in set(r["recorder_ids"]) | set(r["prompt_ids"])
                     if self.corpus.get(i, {}).get("tenant") != q["tenant"]]
            if other:
                failed_k2.append({q["id"]: other})
            for req in q["required"]:
                if r["status"] != 200 or req not in r["recorder_ids"] or req not in r["prompt_ids"]:
                    failed_k1.append({q["id"]: req})
            for d in r["recorder_docs"]:
                c = self.corpus.get(d["id"])
                if not c or d.get("source") != c["source"] or d["metadata"].get("title") != c["metadata"]["title"]:
                    failed_k4.append({q["id"]: d["id"]})
        self.per_engine[engine] = per
        k1 = "FAIL" if failed_k1 else ("INCOMPLETE" if unmeasured else "PASS")
        self.record(f"K1 retrieval ({engine})", k1, {"failures": failed_k1, "unmeasured": unmeasured,
                    "rule": "every required document returned by the engine (recorder) and present in the prompt the gateway received"})
        k2 = "FAIL" if failed_k2 else ("INCOMPLETE" if unmeasured else "PASS")
        self.record(f"K2 tenant isolation ({engine})", k2, {"cross_tenant_documents": failed_k2, "unmeasured": unmeasured})
        probe = next(q for q in self.queries["queries"] if q.get("restricted_probe"))
        r = per[probe["id"]]
        returned = probe["restricted_probe"] in r["recorder_ids"]
        self.record(f"K3 access beyond tenant ({engine})", "OBSERVATION" if r["recorder_ok"] else "INCOMPLETE",
                    {"restricted_document": probe["restricted_probe"], "returned_to_unentitled_caller": returned,
                     "prediction_P_acl": "the contract cannot express entitlement, so the document is returned",
                     "prediction_held": returned,
                     "information_missing": "a Security decision or caller entitlements reachable from ExecutionContext"})
        k4 = "FAIL" if failed_k4 else ("INCOMPLETE" if unmeasured else "PASS")
        self.record(f"K4 citation metadata ({engine})", k4, {"mismatches": failed_k4, "unmeasured": unmeasured})

    def k5(self, engine, container):
        q = self.queries["queries"][0]
        self.sh("docker", "stop", container)
        degraded = self.ask(q, f"{engine}-K5-degraded")
        self.stop_runtime()
        self.start_runtime(f"{engine}-failonerror", engine, True)
        failing = self.ask(q, f"{engine}-K5-fail-on-error")
        self.stop_runtime()
        self.sh("docker", "start", container)
        if container == PG_NAME:
            self.wait(lambda: subprocess.run(["docker", "exec", PG_NAME, "pg_isready", "-U", "knowledge"],
                                             capture_output=True).returncode == 0, 60, "pgvector restart")
        else:
            self.wait(lambda: self.http("GET", f"http://127.0.0.1:{QD_PORT}/readyz")[0] == 200, 60, "qdrant restart")
        leaks_degraded = [m for m in RAW_ERROR_MARKERS if m.lower() in degraded["raw"].lower()]
        error = failing["body"].get("error", {}) if isinstance(failing["body"], dict) else {}
        leaks_failing = [m for m in RAW_ERROR_MARKERS if m.lower() in failing["raw"].lower()]
        meta = degraded["body"].get("metadata") or {} if isinstance(degraded["body"], dict) else {}
        marked = meta.get("retrieval.degraded") == engine
        a = (degraded["status"] == 200 and marked and not degraded["prompt_ids"]
             and bool(degraded["recorder_errors"]) and not leaks_degraded)
        b = failing["status"] not in (0, 200) and error.get("type") == DECLARED_RETRIEVAL_ERROR and not leaks_failing
        measured = degraded["recorder_ok"] and failing["recorder_ok"]
        outcome = "FAIL" if not (a and b) else ("PASS" if measured else "INCOMPLETE")
        self.record(f"K5 failure behaviour ({engine})", outcome, {
            "fail_on_error_false": {"http": degraded["status"], "marked_degraded": marked,
                                    "retrieved_into_prompt": degraded["prompt_ids"],
                                    "engine_error_recorded": bool(degraded["recorder_errors"]),
                                    "raw_error_text_in_response": leaks_degraded,
                                    "response_metadata": degraded["body"].get("metadata")},
            "fail_on_error_true": {"http": failing["status"], "error_type": error.get("type"),
                                   "error_message": error.get("message"),
                                   "raw_error_text_in_response": leaks_failing},
            "raw_error_markers": RAW_ERROR_MARKERS})

    def cross_engine(self):
        def shape(v):
            if isinstance(v, dict):
                return {k: shape(x) for k, x in sorted(v.items())}
            if isinstance(v, list):
                return [shape(v[0])] if v else []
            return type(v).__name__
        a = self.per_engine["pgvector"]["Q1"]["body"]
        b = self.per_engine["qdrant"]["Q1"]["body"]
        same = shape(a) == shape(b)
        both_complete = all(self.results.get(f"K{n} {t} (" + e + ")", {}).get("outcome") == "PASS"
                            for e in ("pgvector", "qdrant")
                            for n, t in ((1, "retrieval"), (2, "tenant isolation"), (4, "citation metadata"), (5, "failure behaviour")))
        self.record("K6 substitution by configuration", "PASS" if same and both_complete else "FAIL",
                    {"switch": "RUNTIME_RETRIEVAL_ENGINE only", "response_structure_identical": same,
                     "K1_K2_K4_K5_pass_for_both": both_complete})
        missing = {}
        for q in self.queries["queries"]:
            for req in q["required"]:
                lacking = [e for e in ("pgvector", "qdrant") if req not in self.per_engine[e][q["id"]]["recorder_ids"]]
                if lacking:
                    missing[f"{q['id']}:{req}"] = lacking
        self.record("K7 cross-engine consistency", "FAIL" if missing else "PASS",
                    {"required_missing": missing,
                     "returned_ids": {e: {q: r["recorder_ids"] for q, r in self.per_engine[e].items()}
                                      for e in ("pgvector", "qdrant")},
                     "note": "identical rankings are not required"})

    def concealment(self):
        found = []
        for e, per in self.per_engine.items():
            for qid, r in per.items():
                for emb in r["embeds"]:
                    keys = list((emb.get("attributes") or {}).keys()) + list(emb.keys())
                    hit = [k for k in keys if any(c in k.lower() for c in CONCEALMENT_KEYS)]
                    if hit:
                        found.append({f"{e}:{qid}": hit})
        self.record("Concealment check (embedding requests)", "FAIL" if found else "PASS",
                    {"suspicious_keys": found, "checked_for": CONCEALMENT_KEYS})

    def containment(self):
        after = self.out / "t4.after-p2.sha256"
        after.write_text(self.sh(sys.executable, str(EXT / "freeze_interface_inventory_t4.py"), "after-p2"))
        cmp = subprocess.run([sys.executable, str(EXT / "freeze_interface_inventory_t4.py"), "compare",
                              str(EXT / "t4.baseline.sha256"), str(after)], capture_output=True, text=True)
        (self.out / "containment-comparison.txt").write_text(cmp.stdout)
        self.record("Containment (interface inventory)", {0: "PASS", 1: "FAIL"}.get(cmp.returncode, "INCOMPLETE"),
                    {"summary": cmp.stdout.strip().splitlines()[-1] if cmp.stdout.strip() else cmp.stderr})

    # ------------------------------------------------------------ run
    def run(self):
        (self.out / "responses").mkdir(parents=True, exist_ok=True)
        self.per_engine = {}
        try:
            self.phase("verify frozen inputs"); self.verify_inputs()
            self.phase("build"); self.build()
            self.phase("start stub, engines, load corpus"); self.start_stub(); self.start_engines()
            for engine, container in (("pgvector", PG_NAME), ("qdrant", QD_NAME)):
                self.phase(f"{engine}: K1-K4")
                self.start_runtime(engine, engine, False)
                self.engine_assertions(engine)
                self.phase(f"{engine}: K5")
                self.k5(engine, container)
            self.phase("K6, K7, concealment"); self.cross_engine(); self.concealment()
            self.results["_run"]["status"] = "assertions complete"
        except Exception:
            self.results["_run"]["status"] = "incomplete"
            self.results["_run"]["exception"] = traceback.format_exc()
            self.log("RUN INCOMPLETE: " + traceback.format_exc().strip().splitlines()[-1])
        finally:
            self.cleanup()
            self.write()
        try:
            self.phase("containment"); self.containment()
        except Exception:
            self.results["_run"]["status"] = "incomplete"
            self.results["_run"]["containment_exception"] = traceback.format_exc()
        if self.results["_run"]["status"] == "assertions complete":
            self.results["_run"]["status"] = "complete"
        self.results["_run"]["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        self.write()
        self.log(f"run status: {self.results['_run']['status']}")


if __name__ == "__main__":
    out = Path(sys.argv[1]).resolve()
    if out.exists() and any(out.iterdir()):
        sys.exit(f"{out} is not empty; each run writes to a fresh directory")
    out.mkdir(parents=True, exist_ok=True)
    Harness(out).run()
