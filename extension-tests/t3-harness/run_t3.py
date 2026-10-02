#!/usr/bin/env python3
"""T3 behavioural harness: assertions B1-B7 against live Redis.

NOT TO BE RUN before the T3 protocol is frozen and the Redis run is approved.

Usage:  run_t3.py <label> <output-dir>      label: initial | post-repair

Evidence is kept in separate kinds, because RedisResponseCache treats every
Redis or deserialization failure as a miss and carries on:

  observed hit     HTTP 200, cached=true AND zero gateway calls for the request.
                   Only this counts as a hit.
  silent miss      HTTP 200, cached=false, one or more gateway calls. A correct
                   answer is not a cache hit.
  live keys        the key each runtime instance used, recorded inside that
                   instance by the T3 recorder (recorder/), corroborated by the
                   keys Redis MONITOR shows. Observation, reported beside hits.
  probe keys       keys computed by two independent same-build JVMs (KeyProbe),
                   not the runtime instances. Observation only.

The T3 recorder is a harness-owned jar loaded into each runtime process through
Spring Boot's PropertiesLauncher (loader.path). It wraps the selected
ResponseCache bean, delegates every call unchanged, and records keys and
outcomes by reflection, never through Jackson.

Every pass rule is fixed here, before execution. Outcomes: PASS, FAIL,
NOT_EXERCISABLE (the configuration cannot vary the input; reason given) and
INCOMPLETE (no failure observed, but not every required case was exercised).
NOT_EXERCISABLE and INCOMPLETE are never counted as passes. Results are written
after every assertion and again on any exception, so an interrupted run still
leaves a structured record marked incomplete.
"""
import hashlib
import json
import os
import re
import signal
import subprocess
import sys
import time
import traceback
import urllib.error
import urllib.request
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
HISTORIES = HERE.parent / "t3-histories.json"
EXPECTED_HISTORIES_SHA256 = "8d584dad2c481ef0fa31061cb11cea9e5f97b3174e278e8e8df088e9e8c9a6fd"
PROTOTYPES = Path(os.environ.get("PROTOTYPES", Path.home() / "Desktop" / "AI Projects"))
RUNTIME = PROTOTYPES / "Enterprise_AI_Runtime_Service"

REDIS_IMAGE = ("redis:7.4-alpine@sha256:"
               "858f009f9709ce576febc734aa78b8f6d624b82571f9ddb6bda4377c833b3499")
WIREMOCK_IMAGE = "wiremock/wiremock:3.9.1"
REDIS_PORT, GW_PORT, PORT_A, PORT_B = 16379, 18080, 18081, 18082
REDIS_NAME, GW_NAME = "t3-redis", "t3-gateway"
POLICY_TTL_SECONDS = 300          # policy-qa cache ttl in the protected application.yml
EXPIRY_WAIT_LIMIT = 360
KEY_APPEAR_LIMIT = 5              # seconds to wait for a stored key to become visible

HEADERS = {
    "Content-Type": "application/json",
    "X-Enterprise-AI-Application": "retail-dashboard",
    "X-Enterprise-AI-Use-Case": "policy-qa",       # the only use case with caching enabled
    "X-Enterprise-AI-Environment": "integration",
    "X-Enterprise-AI-Region": "australia",
    "X-Enterprise-AI-Tenant": "acme",
}

CHAT_STUB = {"request": {"method": "POST", "url": "/v1/inference/chat"},
             "response": {"status": 200, "headers": {"Content-Type": "application/json"},
                          "jsonBody": {"content": "Refunds are accepted within 30 days [source: refunds-policy].",
                                       "provider": "stub", "model": "stub-model", "finishReason": "STOP",
                                       "usage": {"inputTokens": 120, "outputTokens": 14, "cachedInputTokens": 0},
                                       "cost": {"inputCost": "0.00012000", "outputCost": "0.00002800",
                                                "currency": "USD"}}}}
STREAM_STUB = {"request": {"method": "POST", "url": "/v1/inference/stream"},
               "response": {"status": 200, "headers": {"Content-Type": "text/event-stream"},
                            "body": 'data: {"type":"delta","text":"Refunds are accepted "}\n\n'
                                    'data: {"type":"delta","text":"within 30 days."}\n\n'
                                    'data: {"type":"final","finishReason":"STOP","provider":"stub",'
                                    '"model":"stub-model","usage":{"inputTokens":120,"outputTokens":14,'
                                    '"cachedInputTokens":0},"cost":{"inputCost":"0.00012000",'
                                    '"outputCost":"0.00002800","currency":"USD"}}\n\n'}}
HEALTH_STUB = {"request": {"method": "GET", "url": "/v1/health"},
               "response": {"status": 200, "headers": {"Content-Type": "application/json"},
                            "jsonBody": {"status": "UP", "providers": {"stub": "UP"}}}}

OUTCOMES = ("PASS", "FAIL", "NOT_EXERCISABLE", "INCOMPLETE", "OBSERVATION")
DECIMAL_TEXT = re.compile(r"^-?\d+(\.\d+)?([eE][-+]?\d+)?$")


def number_equal(a, b):
    """Numerical equality without rounding (protocol §7, B2)."""
    return Decimal(str(a)).normalize() == Decimal(str(b)).normalize()


def normalise(value):
    """For public-response comparison: numbers by value, never as binary floats."""
    if isinstance(value, dict):
        return {k: normalise(v) for k, v in value.items()}
    if isinstance(value, list):
        return [normalise(v) for v in value]
    if isinstance(value, bool) or value is None:
        return value
    if isinstance(value, (int, Decimal)):
        return ("number", Decimal(value).normalize())
    if isinstance(value, str) and DECIMAL_TEXT.match(value):
        return ("number", Decimal(value).normalize())
    return value


def compare_rendered(expected, actual, path="outcome"):
    """Compare two recorder renderings field by field.

    BigDecimals ({"decimal", "scale"}) compare by value; a scale difference is
    reported separately, as the protocol requires, and is not a mismatch.
    Returns (mismatches, scale_differences).
    """
    mismatches, scales = [], []
    if isinstance(expected, dict) and "decimal" in expected and "scale" in expected:
        if not (isinstance(actual, dict) and "decimal" in actual):
            return [f"{path}: expected decimal, got {actual!r}"], []
        if not number_equal(expected["decimal"], actual["decimal"]):
            mismatches.append(f"{path}: {expected['decimal']} != {actual['decimal']}")
        elif expected["scale"] != actual["scale"]:
            scales.append(f"{path}: scale {expected['scale']} -> {actual['scale']}")
        return mismatches, scales
    if isinstance(expected, dict) and isinstance(actual, dict):
        for k in sorted(set(expected) | set(actual)):
            if k not in expected or k not in actual:
                mismatches.append(f"{path}.{k}: present on one side only")
                continue
            m, s = compare_rendered(expected[k], actual[k], f"{path}.{k}")
            mismatches += m
            scales += s
        return mismatches, scales
    if isinstance(expected, list) and isinstance(actual, list):
        if len(expected) != len(actual):
            return [f"{path}: length {len(expected)} != {len(actual)}"], []
        for i, (e, a) in enumerate(zip(expected, actual)):
            m, s = compare_rendered(e, a, f"{path}[{i}]")
            mismatches += m
            scales += s
        return mismatches, scales
    return ([] if expected == actual else [f"{path}: {expected!r} != {actual!r}"]), []


class Harness:
    def __init__(self, label, out):
        self.label, self.out = label, out
        self.results = {"_run": {"label": label, "status": "started", "phase": None,
                                 "started_utc": self.now()}}
        self.procs, self.recorder_files, self.runtime_logs = {}, {}, {}
        self.last_seq, self.log_offsets, self.startup_ok = {}, {}, {}
        self.results["_run"]["recorder_errors"] = []
        self.monitor = self.monitor_file = None
        self.java = Path(os.environ.get("JAVA_HOME") or self._maven_java_home()) / "bin" / "java"

    # ------------------------------------------------------------ plumbing
    @staticmethod
    def now():
        return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    @staticmethod
    def _maven_java_home():
        out = subprocess.run(["mvn", "-v"], capture_output=True, text=True).stdout
        return next(l.split("runtime: ", 1)[1].strip() for l in out.splitlines() if "runtime: " in l)

    def log(self, msg):
        line = f"[{time.strftime('%H:%M:%S', time.gmtime())}Z] {msg}"
        print(line, flush=True)
        with open(self.out / "harness.log", "a", encoding="utf-8") as f:
            f.write(line + "\n")

    def phase(self, name):
        self.results["_run"]["phase"] = name
        self.write_results()
        self.log(f"--- phase: {name}")

    def write_results(self):
        (self.out / "results.json").write_text(json.dumps(self.results, indent=2, default=str),
                                               encoding="utf-8")

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

    def redis(self, *args):
        return self.sh("docker", "exec", REDIS_NAME, "redis-cli", *args)

    def keys(self):
        out = self.redis("--scan", "--pattern", "eair:v1:*")
        return set(out.split()) if out else set()

    def wait_new_keys(self, before):
        deadline = time.time() + KEY_APPEAR_LIMIT
        while time.time() < deadline:
            new = self.keys() - before
            if new:
                return sorted(new)
            time.sleep(0.2)
        return []

    def gateway_count(self, url):
        _, body = self.http("POST", f"http://localhost:{GW_PORT}/__admin/requests/count",
                            {"method": "POST", "url": url}, {"Content-Type": "application/json"})
        return json.loads(body)["count"]

    def last_gateway_body(self, url):
        _, body = self.http("GET", f"http://localhost:{GW_PORT}/__admin/requests")
        for entry in json.loads(body)["requests"]:          # newest first
            if entry["request"]["url"] == url:
                return json.loads(entry["request"]["body"], parse_float=Decimal)
        return None

    def recorder_events(self, instance, offset):
        path = self.recorder_files.get(instance)
        if not path or not path.exists():
            return [], offset
        with open(path, encoding="utf-8") as f:
            f.seek(offset)
            data = f.read()
            end = f.tell()
        return [json.loads(l) for l in data.splitlines() if l.strip()], end

    def recorder_offset(self, instance):
        path = self.recorder_files.get(instance)
        return path.stat().st_size if path and path.exists() else 0

    def chat(self, port, payload, name, tenant=None, instance=None):
        headers = dict(HEADERS)
        if tenant:
            headers["X-Enterprise-AI-Tenant"] = tenant
        instance = instance or {PORT_A: "A", PORT_B: "B"}[port]
        offset = self.recorder_offset(instance)
        before = self.gateway_count("/v1/inference/chat")
        status, body = self.http("POST", f"http://localhost:{port}/v1/chat", payload, headers)
        calls = self.gateway_count("/v1/inference/chat") - before
        time.sleep(0.1)
        events, _ = self.recorder_events(instance, offset)
        recorder_ok, recorder_problems = self.recorder_integrity(instance, events)
        if not self.startup_ok.get(instance, False):
            recorder_ok = False
            recorder_problems = recorder_problems + [f"recorder startup on {instance} was not clean"]
        (self.out / "responses" / f"{name}.json").write_text(body, encoding="utf-8")
        parsed = json.loads(body, parse_float=Decimal) if body.startswith("{") else {}
        kind = ("observed-hit" if status == 200 and parsed.get("cached") is True and calls == 0
                else "silent-miss" if status == 200 and parsed.get("cached") is False and calls >= 1
                else "anomalous" if status == 200 else "error")
        lookup_keys = [e["key"] for e in events if e["event"] == "lookup-called"]
        self.log(f"{name}: HTTP {status} cached={parsed.get('cached')} gateway+{calls} -> {kind}"
                 f"; live key {lookup_keys[0][:20] + '…' if lookup_keys else 'none'}")
        return {"status": status, "body": parsed, "gateway_calls": calls, "kind": kind,
                "events": events, "live_key": lookup_keys[0] if lookup_keys else None,
                "recorder_ok": recorder_ok, "recorder_problems": recorder_problems}

    def recorder_integrity(self, instance, events):
        """Measurement integrity for one request: no recorder errors, no sequence gaps.

        A recorder failure never changes cache behaviour, but it does mean the
        measurement is incomplete. Any assertion that depends on recorder events
        reports INCOMPLETE, never PASS, when this is not clean.
        """
        problems = []
        log = self.runtime_logs.get(instance)
        if log and log.exists():
            with open(log, encoding="utf-8", errors="replace") as f:
                f.seek(self.log_offsets.get(instance, 0))
                errors = [l.strip() for l in f.read().splitlines() if "T3-RECORDER-ERROR" in l]
                self.log_offsets[instance] = f.tell()
            problems += errors
        for e in events:
            expected = self.last_seq.get(instance, 0) + 1
            if e.get("seq") != expected:
                problems.append(f"sequence gap on {instance}: expected {expected}, got {e.get('seq')}")
            self.last_seq[instance] = e.get("seq", expected)
        if problems:
            self.results["_run"]["recorder_errors"] += problems
        return not problems, problems

    def record(self, key, outcome, evidence):
        assert outcome in OUTCOMES, outcome
        self.results[key] = {"outcome": outcome, "evidence": evidence}
        self.write_results()
        self.log(f"== {key}: {outcome}")

    # ------------------------------------------------------------ lifecycle
    def build(self):
        subprocess.run(["mvn", "-q", "-o", "-pl", "runtime-api", "-am", "package", "-DskipTests"],
                       cwd=RUNTIME, check=True)
        self.jar = RUNTIME / "runtime-api" / "target" / "runtime-api-1.0.0-SNAPSHOT-app.jar"
        self.recorder_jar = Path(self.sh(str(HERE / "recorder" / "build-recorder.sh"),
                                         str(self.out / "recorder-build")).splitlines()[-1])
        self.results["_run"]["runtime_revision"] = self.sh("git", "-C", str(RUNTIME), "rev-parse", "HEAD")
        self.results["_run"]["runtime_jar_sha256"] = self.sh("shasum", "-a", "256", str(self.jar)).split()[0]
        self.results["_run"]["recorder_jar_sha256"] = self.sh("shasum", "-a", "256",
                                                              str(self.recorder_jar)).split()[0]

    def start_gateway(self):
        subprocess.run(["docker", "rm", "-f", GW_NAME], capture_output=True)
        self.sh("docker", "run", "-d", "--name", GW_NAME, "-p", f"{GW_PORT}:8080", WIREMOCK_IMAGE)
        self._wait(lambda: self.http("GET", f"http://localhost:{GW_PORT}/__admin/mappings")[0] == 200, 60)
        for stub in (CHAT_STUB, STREAM_STUB, HEALTH_STUB):
            self.http("POST", f"http://localhost:{GW_PORT}/__admin/mappings", stub,
                      {"Content-Type": "application/json"})

    def start_redis(self):
        subprocess.run(["docker", "rm", "-f", REDIS_NAME], capture_output=True)
        self.sh("docker", "run", "-d", "--name", REDIS_NAME, "-p", f"{REDIS_PORT}:6379", REDIS_IMAGE,
                "redis-server", "--save", "", "--appendonly", "no")
        self._wait(lambda: self.redis("PING") == "PONG", 30)
        self.results["_run"]["redis_image_id"] = self.sh("docker", "inspect", "--format", "{{.Image}}", REDIS_NAME)
        # MONITOR corroborates the recorder's live keys: it shows every key each
        # instance issues, including on a miss. Observation only.
        self.monitor_file = open(self.out / "redis-monitor.log", "w", encoding="utf-8")
        self.monitor = subprocess.Popen(["docker", "exec", REDIS_NAME, "redis-cli", "MONITOR"],
                                        stdout=self.monitor_file, stderr=subprocess.STDOUT)

    def start_runtime(self, name, port, provider):
        env = dict(os.environ, SERVER_PORT=str(port), RUNTIME_ENVIRONMENT="integration",
                   RUNTIME_SECURITY_MODE="NONE", RUNTIME_CACHE_PROVIDER=provider,
                   MODEL_GATEWAY_URL=f"http://localhost:{GW_PORT}",
                   SPRING_DATA_REDIS_HOST="localhost", SPRING_DATA_REDIS_PORT=str(REDIS_PORT))
        rec = self.out / f"recorder-{name}-{provider}.jsonl"
        self.recorder_files[name] = rec
        self.runtime_logs[name] = self.out / f"runtime-{name}-{provider}.log"
        self.last_seq[name], self.log_offsets[name] = 0, 0
        logf = open(self.runtime_logs[name], "w", encoding="utf-8")
        self.procs[name] = subprocess.Popen(
            [str(self.java), "-cp", str(self.jar), f"-Dloader.path={self.recorder_jar}",
             f"-Dt3.instance={name}", f"-Dt3.recorder.out={rec}",
             "org.springframework.boot.loader.launch.PropertiesLauncher"],
            env=env, stdout=logf, stderr=subprocess.STDOUT)
        self._wait(lambda: self.http("GET", f"http://localhost:{port}/v1/ready")[0] == 200, 120)
        installed, _ = self.recorder_events(name, 0)
        # Startup integrity is retained per JVM and applied to every later request
        # on that JVM: a recorder that reported errors while installing makes all
        # of that instance's recorder evidence unreliable.
        startup_ok, startup_problems = self.recorder_integrity(name, installed)
        self.startup_ok[name] = startup_ok and any(e["event"] == "recorder-installed" for e in installed)
        self.results["_run"].setdefault("recorder_startup", {})[name] = {
            "clean": self.startup_ok[name], "problems": startup_problems}
        realization = next((e["realization"] for e in installed if e["event"] == "recorder-installed"), None)
        expected = {"redis": "RedisResponseCache", "caffeine": "CaffeineResponseCache"}[provider]
        if not realization or not realization.endswith(expected):
            raise RuntimeError(f"runtime {name}: recorder reports {realization!r}, expected {expected}")
        self.log(f"runtime {name} ready on {port} with {realization.split('.')[-1]}, pid {self.procs[name].pid}")

    def stop_runtime(self, name):
        p = self.procs.pop(name, None)
        if p:
            p.send_signal(signal.SIGTERM)
            try:
                p.wait(timeout=60)
            except subprocess.TimeoutExpired:
                p.kill()

    def _wait(self, probe, seconds):
        deadline = time.time() + seconds
        while time.time() < deadline:
            try:
                if probe():
                    return
            except Exception:
                pass
            time.sleep(1)
        raise TimeoutError("service did not become ready")

    def cleanup(self):
        errors = []
        for name in list(self.procs):
            try:
                self.stop_runtime(name)
            except Exception as e:
                errors.append(f"stop {name}: {e}")
        if self.monitor:
            self.monitor.terminate()
            self.monitor_file.close()
        for c in (REDIS_NAME, GW_NAME):
            subprocess.run(["docker", "rm", "-f", c], capture_output=True)
        return errors

    @staticmethod
    def msg(text):
        return {"promptId": "policy-qa", "messages": [{"role": "user", "content": text}]}

    # ------------------------------------------------------------ assertions
    def b2b_caffeine_reference(self):
        """The Caffeine hit response that B2b compares against."""
        self.start_runtime("A", PORT_A, "caffeine")
        self.chat(PORT_A, self.msg("T3 B2b reference question"), "b2b-caffeine-miss")
        self.caffeine_hit = self.chat(PORT_A, self.msg("T3 B2b reference question"), "b2b-caffeine-hit")
        self.stop_runtime("A")

    def monitor_mark(self):
        path = self.out / "redis-monitor.log"
        return path.stat().st_size if path.exists() else 0

    def monitor_commands(self, mark, command):
        """Keys for one Redis command (e.g. GET, SET) issued since mark, per MONITOR."""
        time.sleep(0.2)
        with open(self.out / "redis-monitor.log", encoding="utf-8", errors="replace") as f:
            f.seek(mark)
            return [l.split('"')[3] for l in f.read().splitlines() if f'"{command}"' in l.upper()
                    and len(l.split('"')) > 3]

    def b1_b2(self):
        before = self.keys()
        mark = self.monitor_mark()
        miss = self.chat(PORT_A, self.msg("T3 B1 question"), "b1-first")
        new = self.wait_new_keys(before)
        set_keys = self.monitor_commands(mark, "SET")
        hit = self.chat(PORT_A, self.msg("T3 B1 question"), "b1-second")
        measured = miss["recorder_ok"] and hit["recorder_ok"] and miss["live_key"] and hit["live_key"]
        behaviour_ok = miss["kind"] == "silent-miss" and len(new) == 1 and hit["kind"] == "observed-hit"
        # The recorder's key is a separately computed observation; it must match
        # the key Redis actually holds and the key MONITOR shows being SET.
        keys_agree = measured and len(new) == 1 and miss["live_key"] == new[0] == hit["live_key"] \
            and set_keys == [new[0]]
        # Behaviour (cached flag, gateway count, one new key) decides FAIL. Missing
        # recorder evidence, or keys that disagree with Redis and MONITOR, leave the
        # measurement inconsistent: INCOMPLETE, recorded explicitly, never PASS.
        outcome = ("FAIL" if not behaviour_ok else "INCOMPLETE" if not (measured and keys_agree)
                   else "PASS")
        self.record("B1 hit is real", outcome,
                    {"first": miss["kind"], "second": hit["kind"], "new_redis_keys": new,
                     "keys_SET_(MONITOR)": set_keys, "recorder_key_first": miss["live_key"],
                     "recorder_key_second": hit["live_key"], "recorder_keys_match_redis": keys_agree,
                     "recorder_clean": bool(miss["recorder_ok"] and hit["recorder_ok"])})

        # B2a: the outcome handed to store (recorded before serialization) against
        # the outcome lookup returned (after the runtime's own deserialization),
        # every field, rendered by reflection rather than Jackson.
        stored = [e for e in miss["events"] if e["event"] == "store-called"]
        returned = [e for e in hit["events"] if e["event"] == "lookup-returned"]
        if not (miss["recorder_ok"] and hit["recorder_ok"]) or len(stored) != 1 or len(returned) != 1:
            self.record("B2a round-trip through the runtime's serializer", "INCOMPLETE",
                        {"reason": "recorder evidence missing or unreliable",
                         "store_events": len(stored), "lookup_returned_events": len(returned),
                         "recorder_problems": miss["recorder_problems"] + hit["recorder_problems"]})
        else:
            # The two outcomes must belong to the same entry: the same key on both
            # events, and that key must be the one Redis holds.
            same_entry = len(new) == 1 and stored[0]["key"] == returned[0]["key"] == new[0]
            mismatches, scales = compare_rendered(stored[0]["outcome"], returned[0]["outcome"])
            if len(new) == 1:
                (self.out / "b2a-raw-redis-entry.json").write_text(self.redis("GET", new[0]), encoding="utf-8")
            # Field mismatches on the same entry are a FAIL. If the two outcomes cannot
            # be shown to belong to the same entry, the comparison proves nothing:
            # INCOMPLETE, recorded explicitly.
            self.record("B2a round-trip through the runtime's serializer",
                        "INCOMPLETE" if not same_entry else "FAIL" if mismatches else "PASS",
                        {"fields_compared": "every record component, recursively",
                         "same_entry_(store key = returned key = Redis key)": same_entry,
                         "mismatches": mismatches,
                         "scale_differences_(reported,_not_mismatches)": scales})

        # B2b: public response on a Redis hit against a Caffeine hit.
        self.chat(PORT_A, self.msg("T3 B2b reference question"), "b2b-redis-miss")
        redis_hit = self.chat(PORT_A, self.msg("T3 B2b reference question"), "b2b-redis-hit")
        same = (redis_hit["kind"] == "observed-hit" and self.caffeine_hit["kind"] == "observed-hit"
                and normalise(redis_hit["body"]) == normalise(self.caffeine_hit["body"]))
        self.record("B2b Redis hit equals Caffeine hit (public response)", "PASS" if same else "FAIL",
                    {"redis": redis_hit["kind"], "caffeine": self.caffeine_hit["kind"]})

    def b3(self):
        base = self.msg("T3 B3 base question")
        first = self.chat(PORT_A, base, "b3-base-first")
        base_body = self.last_gateway_body("/v1/inference/chat")
        # (payload, tenant header, path of the gateway-request field expected to
        # change, or None if the input has no observable effect on the gateway
        # request for policy-qa). The tenant is checked at attributes.ai.tenant_id,
        # not the whole attributes map, which also carries per-request trace and
        # request ids and so differs on every request regardless of tenant.
        variants = {
            "tenant": (dict(base), "globex", ("attributes", "ai.tenant_id")),
            "variables": (dict(base, variables={"region": "north"}), None, None),
            "response schema": (dict(base, responseSchema={"type": "object"}), None, ("responseSchema",)),
            "temperature": (dict(base, temperature=0.5), None, ("temperature",)),
            "max output tokens": (dict(base, maxOutputTokens=512), None, ("maxOutputTokens",)),
            "model profile": (dict(base, modelProfile="cheap-batch"), None, ("modelProfile",)),
        }
        per, failed, verified, unmeasured = {}, False, 0, 0
        for label, (payload, tenant, field) in variants.items():
            r = self.chat(PORT_A, payload, f"b3-{label.replace(' ', '-')}", tenant=tenant)
            if r["status"] != 200:
                per[label] = {"result": "REJECTED", "http": r["status"],
                              "outcome": "NOT_EXERCISABLE"}
                continue
            if not (r["recorder_ok"] and first["recorder_ok"] and r["live_key"] and first["live_key"]):
                per[label] = {"result": "UNMEASURED (recorder evidence missing or unreliable)",
                              "kind": r["kind"]}
                unmeasured += 1
                if r["kind"] == "observed-hit":
                    failed = True       # a shared entry is observed without the recorder
                continue
            key_differs = r["live_key"] != first["live_key"]
            body = self.last_gateway_body("/v1/inference/chat") if r["gateway_calls"] else None
            def at(doc, path):
                for part in path:
                    doc = doc.get(part) if isinstance(doc, dict) else None
                return doc
            effect = (None if field is None or body is None or base_body is None
                      else normalise(at(body, field)) != normalise(at(base_body, field)))
            if r["kind"] != "silent-miss" or not key_differs:
                result, failed = "SHARED_OR_UNSEPARATED", True
            elif field is None:
                result = "ISOLATED_KEY_ONLY (no observable effect on the gateway request for policy-qa)"
                verified += 1
            elif effect:
                result = "ISOLATED_VERIFIED (key differs; input reached the gateway changed)"
                verified += 1
            else:
                result, failed = "ACCEPTED_BUT_INPUT_NOT_CHANGED_AT_GATEWAY", True
            per[label] = {"result": result, "kind": r["kind"], "key_differs_from_base": key_differs,
                          "gateway_field": ".".join(field) if field else None,
                          "gateway_field_changed": effect}
        still = self.chat(PORT_A, base, "b3-base-again")
        if still["kind"] != "observed-hit":
            failed = True
        per["base after variants"] = still["kind"]
        outcome = ("FAIL" if failed else "INCOMPLETE" if unmeasured
                   else "PASS" if verified else "NOT_EXERCISABLE")
        # The outcome covers only the dimensions actually exercised.
        self.record("B3 key isolation (exercised dimensions only)", outcome, per)
        self.record("B3 key isolation: prompt version", "NOT_EXERCISABLE",
                    {"reason": "policy-qa has a single approved version (v1.4) in this configuration"})
        self.record("B3 key isolation: retrieval fingerprint", "NOT_EXERCISABLE",
                    {"reason": "no Retriever realization exists (results §11), so the fingerprint cannot vary"})

    def b5a(self):
        mark_a = self.monitor_mark()
        # One user message, which the runtime treats as a one-message history.
        on_a = self.chat(PORT_A, self.msg("T3 B5a question"), "b5a-on-A")
        set_a = self.monitor_commands(mark_a, "SET")
        mark_b = self.monitor_mark()
        on_b = self.chat(PORT_B, self.msg("T3 B5a question"), "b5a-on-B")
        get_b = self.monitor_commands(mark_b, "GET")
        measured = on_a["recorder_ok"] and on_b["recorder_ok"] and on_a["live_key"] and on_b["live_key"]
        keys_agree = measured and on_a["live_key"] == on_b["live_key"] and set_a == [on_a["live_key"]] \
            and get_b == [on_b["live_key"]]
        # A must populate the entry in this case (a silent miss); otherwise a hit on
        # B would not show that A's write is what B read.
        a_populated = on_a["kind"] == "silent-miss"
        outcome = ("FAIL" if on_b["kind"] != "observed-hit"
                   else "INCOMPLETE" if not (a_populated and measured)
                   else "PASS" if keys_agree else "INCOMPLETE")
        # Relabelled (T3 revision 3): the runtime maps every request message into the
        # history that enters the key, so this request carries a one-message history.
        self.record("B5a cross-instance, one-message history", outcome,
                    {"on_A": on_a["kind"], "A_populated_the_entry": a_populated, "on_B": on_b["kind"], "recorder_key_A": on_a["live_key"], "recorder_key_B": on_b["live_key"],
                     "keys_SET_by_A_(MONITOR)": set_a, "keys_GET_by_B_(MONITOR)": get_b,
                     "recorder_keys_agree_with_each_other_and_MONITOR": keys_agree})

    def load_histories(self):
        raw = HISTORIES.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        if digest != EXPECTED_HISTORIES_SHA256:
            raise RuntimeError(f"t3-histories.json digest {digest} does not match the frozen "
                               f"{EXPECTED_HISTORIES_SHA256}")
        histories = json.loads(raw)["histories"]
        ids = [h["id"] for h in histories]
        rendered = [json.dumps(h["messages"], sort_keys=True) for h in histories]
        if len(histories) != 20 or len(set(ids)) != 20 or len(set(rendered)) != 20:
            raise RuntimeError("t3-histories.json must hold 20 cases with distinct ids and distinct messages")
        return histories

    def b5b(self):
        histories = self.load_histories()
        per, live_keys = {}, {}
        rejected, misses, not_populated, unmeasured, disagreements = [], [], [], [], []
        for h in histories:
            payload = {"promptId": "policy-qa", "messages": h["messages"]}
            mark_a = self.monitor_mark()
            on_a = self.chat(PORT_A, payload, f"b5b-{h['id']}-A")
            if on_a["status"] != 200:
                rejected.append(h["id"])
                per[h["id"]] = {"result": "REJECTED", "http_on_A": on_a["status"]}
                continue
            set_a = self.monitor_commands(mark_a, "SET")
            mark_b = self.monitor_mark()
            on_b = self.chat(PORT_B, payload, f"b5b-{h['id']}-B")
            get_b = self.monitor_commands(mark_b, "GET")
            # A must populate the entry in this case, or a hit on B proves nothing.
            a_populated = on_a["kind"] == "silent-miss"
            if not a_populated:
                not_populated.append(h["id"])
            hit = on_b["kind"] == "observed-hit"
            if not hit:
                misses.append(h["id"])
            measured = bool(on_a["recorder_ok"] and on_b["recorder_ok"] and on_a["live_key"] and on_b["live_key"])
            monitor_agrees = measured and set_a == [on_a["live_key"]] and get_b == [on_b["live_key"]]
            if not measured:
                unmeasured.append(h["id"])
            else:
                live_keys[h["id"]] = {"A": on_a["live_key"], "B": on_b["live_key"]}
                # On an observed hit, A and B must have used one key, and MONITOR must
                # show that key. Anything else is recorded, never assumed corroborated.
                if not monitor_agrees or (hit and on_a["live_key"] != on_b["live_key"]):
                    disagreements.append(h["id"])
            per[h["id"]] = {"on_A": on_a["kind"], "A_populated_the_entry": a_populated,
                            "result_on_B": "hit" if hit else on_b["kind"],
                            "recorder_measured": measured,
                            "recorder_key_A": on_a["live_key"], "recorder_key_B": on_b["live_key"],
                            "keys_SET_by_A_(MONITOR)": set_a, "keys_GET_by_B_(MONITOR)": get_b,
                            "recorder_agrees_with_MONITOR": monitor_agrees,
                            "recorder_problems": on_a["recorder_problems"] + on_b["recorder_problems"]}
        exercised = 20 - len(rejected)
        # An observed miss on B is a FAIL whatever else is true: hits and misses are
        # observed without the recorder. A PASS needs every one of the 20 cases
        # exercised, populated by A, hit on B, measured by the recorder and
        # corroborated by MONITOR. Anything short of that, without a miss, is
        # INCOMPLETE, with the reasons listed.
        if misses:
            outcome = "FAIL"
        elif exercised == 0:
            outcome = "NOT_EXERCISABLE"
        elif exercised < 20 or not_populated or unmeasured or disagreements:
            outcome = "INCOMPLETE"
        else:
            outcome = "PASS"
        self.record("B5b cross-instance, with history (20 histories)", outcome,
                    {"exercised": exercised, "rejected": rejected, "missed_on_B": misses,
                     "A_did_not_populate": not_populated, "recorder_unmeasured": unmeasured,
                     "key_or_MONITOR_disagreement": disagreements,
                     "pass_requires": "all 20 exercised, populated by A, observed hits on B, "
                                      "measured by the recorder and corroborated by MONITOR",
                     "per_history": per})
        differing = sorted(i for i, k in live_keys.items() if k["A"] != k["B"])
        self.record("B5-keys-live (observation: keys the runtime instances used)",
                    "OBSERVATION" if not unmeasured else "INCOMPLETE",
                    {"source": "recorder in runtime A and B (a separately computed observation by the "
                               "same key factory on the same context), cross-checked against MONITOR",
                     "histories_compared": len(live_keys), "histories_unmeasured": unmeasured,
                     "histories_with_differing_keys": differing,
                     "histories_where_recorder_disagrees_with_MONITOR": [
                         i for i in live_keys if not per[i]["recorder_agrees_with_MONITOR"]]})

    def b6(self):
        before_keys = self.keys()
        optout = dict(self.msg("T3 B6 opt-out question"), cacheable=False)
        first = self.chat(PORT_A, optout, "b6-optout-1")
        second = self.chat(PORT_A, optout, "b6-optout-2")
        optout_ok = (first["kind"] == "silent-miss" and second["kind"] == "silent-miss"
                     and self.keys() == before_keys)
        keys_before_stream = self.keys()
        stream_offset = self.recorder_offset("A")
        stream_before = self.gateway_count("/v1/inference/stream")
        chat_before = self.gateway_count("/v1/inference/chat")
        status, body = self.http("POST", f"http://localhost:{PORT_A}/v1/chat/stream",
                                 self.msg("T3 B6 streamed question"),
                                 dict(HEADERS, Accept="text/event-stream"))
        (self.out / "responses" / "b6-stream.txt").write_text(body, encoding="utf-8")
        stream_calls = self.gateway_count("/v1/inference/stream") - stream_before
        chat_calls = self.gateway_count("/v1/inference/chat") - chat_before
        time.sleep(0.5)
        # The streamed request bypasses chat(), so its recorder events must be
        # consumed here. Otherwise the continuity check reports a false gap on the
        # next request (T3 post-repair run, B4).
        stream_events, _ = self.recorder_events("A", stream_offset)
        stream_recorder_ok, stream_recorder_problems = self.recorder_integrity("A", stream_events)
        stream_ok = (status == 200 and '"final"' in body and stream_calls == 1 and chat_calls == 0
                     and self.keys() == keys_before_stream)
        # Behaviour decides FAIL, exactly as before. Revision 3 evidence-integrity
        # correction: when behaviour passes but the streamed request's recorder
        # evidence is unreliable, B6 is INCOMPLETE, never PASS.
        behaviour_ok = optout_ok and stream_ok
        b6_outcome = ("FAIL" if not behaviour_ok
                      else "PASS" if stream_recorder_ok else "INCOMPLETE")
        self.record("B6 policy honoured", b6_outcome,
                    {"opt_out_never_stored": optout_ok, "stream_http": status,
                     "stream_gateway_calls": stream_calls, "chat_gateway_calls_during_stream": chat_calls,
                     "streamed_response_not_stored": self.keys() == keys_before_stream,
                     "stream_recorder_events_consumed": len(stream_events),
                     "stream_recorder_clean": stream_recorder_ok,
                     "stream_recorder_problems": stream_recorder_problems})

    def b4(self):
        before = self.keys()
        first = self.chat(PORT_A, self.msg("T3 B4 expiry question"), "b4-first")
        new = self.wait_new_keys(before)
        if len(new) != 1:
            self.record("B4 expiry", "FAIL", {"error": "no single new key", "first": first["kind"]})
            return
        ttl = int(self.redis("TTL", new[0]))
        ttl_read_at = time.time()
        store = next((e for e in first["events"] if e["event"] == "store-called"), None)
        if store is None or not first["recorder_ok"]:
            # The store time anchors the TTL measurement; without it B4 is unmeasured.
            self.record("B4 expiry", "INCOMPLETE",
                        {"reason": "store-called event missing or recorder evidence unreliable",
                         "redis_reported_ttl_seconds": ttl,
                         "recorder_problems": first["recorder_problems"]})
            return
        store_at = store["at"]
        # The policy TTL is observed, never shortened or bypassed: it comes from the
        # protected application.yml and is read back from Redis here.
        self.log(f"B4: Redis reports TTL {ttl}s; waiting for expiry (limit {EXPIRY_WAIT_LIMIT}s)")
        while new[0] in self.keys() and time.time() - ttl_read_at < EXPIRY_WAIT_LIMIT:
            time.sleep(1)
        detected_at = time.time()
        gone = new[0] not in self.keys()
        after = self.chat(PORT_A, self.msg("T3 B4 expiry question"), "b4-after-expiry")
        # Redis reports whole seconds, and time passes between insertion and the
        # TTL read, so the reading may be slightly below 300 but never above it.
        ttl_ok = POLICY_TTL_SECONDS - 5 <= ttl <= POLICY_TTL_SECONDS
        ok = ttl_ok and gone and after["kind"] == "silent-miss"
        self.record("B4 expiry", "PASS" if ok else "FAIL",
                    {"redis_reported_ttl_seconds": ttl,
                     "ttl_acceptance": f"{POLICY_TTL_SECONDS - 5}..{POLICY_TTL_SECONDS}",
                     "store_called_at_utc_(recorder)": store_at,
                     "ttl_read_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(ttl_read_at)),
                     "expiry_detected_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(detected_at)),
                     "seconds_from_ttl_read_to_expiry": round(detected_at - ttl_read_at),
                     "poll_interval_seconds": 1, "expired": gone, "after_expiry": after["kind"]})

    def b7(self):
        self.sh("docker", "stop", REDIS_NAME)
        started = time.time()
        r = self.chat(PORT_A, self.msg("T3 B7 degradation question"), "b7-redis-down")
        elapsed = round(time.time() - started, 2)
        ok = r["status"] == 200 and r["kind"] == "silent-miss"
        self.record("B7 degradation", "PASS" if ok else "FAIL",
                    {"http": r["status"], "kind": r["kind"], "seconds": elapsed})

    def b5_keys_probe(self):
        """Observation: independent same-build JVMs, NOT the runtime instances."""
        probe_out = self.out / "b5-keys-probe"
        r = subprocess.run([str(HERE / "run-key-probe.sh"), str(probe_out)], capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(f"key probe failed: {r.stderr.strip()[-500:]}")

        def rows(name):
            lines = (probe_out / name).read_text(encoding="utf-8").splitlines()
            return dict(l.split("\t", 1) for l in lines if l and not l.startswith("#"))
        a, b = rows("keys-jvm-a.tsv"), rows("keys-jvm-b.tsv")
        missing = sorted(set(a) ^ set(b))
        differing = sorted(i for i in set(a) & set(b) if a[i] != b[i])
        self.record("B5-keys-probe (observation: independent same-build JVMs, not the runtime instances)",
                    "OBSERVATION", {"ids_in_A": len(a), "ids_in_B": len(b), "ids_missing_on_one_side": missing,
                                    "histories_with_differing_keys": differing})

    # ------------------------------------------------------------ run
    def run(self):
        (self.out / "responses").mkdir(parents=True, exist_ok=True)
        try:
            self.phase("verify histories"); self.load_histories()
            self.phase("build"); self.build()
            self.phase("start gateway"); self.start_gateway()
            self.phase("caffeine reference"); self.b2b_caffeine_reference()
            self.phase("start redis and runtimes")
            self.start_redis()
            self.start_runtime("A", PORT_A, "redis")
            self.start_runtime("B", PORT_B, "redis")
            for name, step in (("B1-B2", self.b1_b2), ("B3", self.b3), ("B5a", self.b5a),
                               ("B5b", self.b5b), ("B6", self.b6), ("B4", self.b4), ("B7", self.b7)):
                self.phase(name)
                step()
            self.results["_run"]["status"] = "assertions complete"
        except Exception:
            self.results["_run"]["status"] = "incomplete"
            self.results["_run"]["exception"] = traceback.format_exc()
            self.log("RUN INCOMPLETE: " + traceback.format_exc().strip().splitlines()[-1])
        finally:
            self.results["_run"]["cleanup_errors"] = self.cleanup()
            self.write_results()
        try:
            self.phase("B5-keys-probe"); self.b5_keys_probe()
        except Exception:
            self.results["_run"]["probe_exception"] = traceback.format_exc()
            self.results["_run"]["status"] = "incomplete"
        status = self.sh("git", "-C", str(RUNTIME), "status", "--short", ".", check=False)
        self.results["_run"]["runtime_repository_unchanged_by_harness"] = status == ""
        self.results["_run"]["finished_utc"] = self.now()
        if self.results["_run"]["status"] == "assertions complete":
            self.results["_run"]["status"] = "complete"
        self.write_results()
        self.log(f"run status: {self.results['_run']['status']}; results in results.json")


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("initial", "post-repair"):
        sys.exit("usage: run_t3.py initial|post-repair <output-dir>")
    # Absolute, because helper scripts run Maven inside the runtime repository and
    # would resolve a relative path there (T3 initial run, attempt 1).
    out = Path(sys.argv[2]).resolve()
    if out.exists() and any(out.iterdir()):
        sys.exit(f"{out} is not empty; each run writes to a fresh directory")
    out.mkdir(parents=True, exist_ok=True)
    Harness(sys.argv[1], out).run()
