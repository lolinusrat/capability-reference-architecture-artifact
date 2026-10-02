# T4 Report — Knowledge Services: pgvector and Qdrant Against the Frozen `Retriever` Contract

**Status: P2 complete (attempt 1); P3 report. Submitted for review. No manuscript
claim until the reviewer accepts these results.**

| Record | Commit |
|:---|:---|
| P0 frozen (protocol, corpus, queries, inventory, baseline) | 87392da (author's authorization; reviewer's line-by-line review not completed, disclosed) |
| P1 complete (both engines; finding P1-1, deviation P1-D1) | 9b4a2ac |
| P2 harness frozen, before any run | 2fb49a3 (`../../t4-p2.frozen.sha256.md`) |
| P2 attempt 1 evidence | `attempt-1/` (this commit) |

P2 authorization: the author's instruction to complete T4 (2 October 2026). The
protocol (§7) asks for P2 to be separately authorized; that instruction is the
authorization relied on.

## 1 Results

Behaviour and containment are reported separately (protocol §6, §9).

| Assertion | pgvector | Qdrant |
|:---|:---|:---|
| K1 Retrieval (recorder **and** prompt) | PASS | PASS |
| K2 Tenant isolation | PASS | PASS |
| K3 Access beyond tenant | OBSERVATION: restricted document returned (P-acl held) | OBSERVATION: same |
| K4 Citation metadata | PASS | PASS |
| K5 Failure behaviour | **FAIL** (raw engine error reaches the API with `fail-on-error=true`) | **FAIL** (same) |
| K6 Substitution by configuration | **FAIL** by its frozen rule (K5 fails); the switch itself held: see §3 | |
| K7 Cross-engine consistency | PASS | |
| Concealment check (embedding requests) | PASS | |
| **Containment** (interface inventory, baseline → after P2) | **PASS: no protected surface changed** | |

Recorder integrity: there were no recorder errors and no sequence gaps, and all four
runtime starts were clean (`results.json` → `_run`). Both engines ran from
their pinned digests (image ids recorded). Both runs used one runtime jar
(sha256 `32d4f0f72668bd80e5c1d20dfdac645bb1cbcbf7570d75c04e128c034dd1c102`).

## 2 Findings

### Finding P2-1 (K5): the existing consumer passes raw engine error text to the API

With the engine stopped:

- **`fail-on-error=false`: as specified.** HTTP 200, `retrieval.degraded` set to the
  strategy, no documents in the prompt, the engine error recorded by the recorder,
  and no raw error text in the response.
- **`fail-on-error=true`: declared type, raw message.** HTTP 502 with
  `error.type = retrieval_error`, as declared. The message, however, carries the
  engine's raw exception:
  - pgvector: `retrieval failed via pgvector: org.postgresql.util.PSQLException: Connection to 127.0.0.1:15432 refused. Check that the hostname and port are correct and that the postmaster is accepting TCP/IP connections.`
  - Qdrant: `retrieval failed via qdrant: org.springframework.web.reactive.function.client.WebClientRequestException: Connection refused: /127.0.0.1:16333`

  The protocol states "in neither case may a raw engine error reach the API", so
  K5 is FAIL for both engines.

**Where the text comes from.** Neither adapter produces this message. The
pre-existing, protected consumer `DefaultContextBuilder` (line 94) builds
`new RetrievalException(strategy, failure.toString(), …)`. The `runtime-common`
`RetrievalException` prefixes it, and `runtime-api`'s `ErrorStatusMapper`
(line 64) returns `failure.getMessage()` in the error body. Any `Retriever`
realization's exception text, including an engine's host, port and driver class,
therefore reaches the caller. The defect was latent from before T4. T4 is the first
experiment to exercise it, because before T4 no realization existed to fail.

**Disclosure.** I read this code path while writing the harness (before the
freeze) and noted that the message "may leak raw engine text". It was not
recorded as a P0 prediction (protocol §8). The pass rule follows the protocol's
P0 wording and was not adjusted after the run.

**Not repaired.** The options are reviewer decisions, as in T3:

- **(a) Adapter-side sanitisation.** Each adapter wraps engine failures in an
  exception with fixed text. This stays inside the permitted engine package, but it
  hides diagnostics, and every future realization would have to repeat it.
- **(b) Consumer-side.** `DefaultContextBuilder`/`ErrorStatusMapper` stop
  returning `failure.toString()`. This changes a protected surface, so it would be
  a post-test repair with its own containment count, as with T3's post-repair
  runs.
- **(c) Report as is.** The boundary's failure path, as originally implemented,
  does not conceal realization errors.

### Observation P2-2 (K3): prediction P-acl held, for both engines

`acme-salary-bands` (classification `restricted`) was returned to an acme caller
with no expressed entitlement. It was ranked first for Q6, and it also appeared in
Q2's top 3 for both engines. The contract cannot express entitlement beyond the
tenant: `CallerIdentity` has no roles, and `ExecutionContext` carries no Security
decision. Neither engine invented a channel. The concealment check found no
semantic keys in the embedding requests, and no adapter reads `tags`. **This is a
contract limitation, reported as a finding (protocol §4) and not repaired.**
Missing information: a Security decision or the caller's entitlements, reachable
from `ExecutionContext`.

### Observation P2-3: zero-similarity documents fill top-K

Both engines return `topK=3` documents even when the third has similarity 0.0. In
Q1 and Q3, rank 3 is a zero-score document (pgvector `acme-expenses`, Qdrant
`acme-parental`), and it goes into the prompt. The contract has no relevance
threshold. This is noted, not assessed: no K assertion covers it. The engines
differ at rank 3 only among tied zero scores, and ranks 1–2 are identical, scores
included. K7 does not require ranking equality.

## 3 Substitution (K6) and footprints (protocol §9)

- **Introduction footprint** (P1, from `../../t4-p1/`):
  - Each engine added files only in the permitted engine package and changed
    `runtime-retrieval/pom.xml`. Six engine files in total; no protected change.
  - Finding P1-1: adding an R2DBC driver activated Spring Boot auto-configuration
    application-wide, breaking startup for every deployment, invisibly to the
    inventory.
  - Deviation P1-D1: pgvector moved to JDBC on `boundedElastic`.
- **Substitution footprint** (what switching changed): **zero files.** Both engines
  ran from one jar, and the only differing setting was `RUNTIME_RETRIEVAL_ENGINE`
  (`../../t4-engine-config.md`). The Q1 response structure was identical across
  engines.
- **K6 outcome: FAIL.** The frozen rule requires K1, K2, K4 and K5 to hold for both
  engines, and K5 failed for both. The switch-by-configuration part of K6 held. The
  FAIL is inherited entirely from Finding P2-1.

## 4 Containment

`attempt-1/containment-comparison.txt`, baseline (P0) → after P2:

- All 12 protected and protected-existing surfaces are unchanged.
- Changes appear only in the permitted surfaces: six engine files added and
  `runtime-retrieval/pom.xml` modified.
- No protected surface changed.

## 5 Limits of this evidence

- One run per engine, synthetic 12-document corpus, deterministic symmetric stub
  embeddings. T4 does not test embedding semantics (T2's question) or retrieval
  quality.
- Only the query path is tested; indexing is outside the contract (harness
  tooling).
- Local containers; K5 exercises one failure mode (engine unreachable), not
  timeouts or partial failures.
- The runtime test-count discrepancy (F3 recorded 596; the suite now reports 300)
  remains unreconciled and documented.

## 6 Evidence (`attempt-1/`)

- `results.json`: every outcome with its evidence and run metadata.
- `harness.log`: the run log.
- `responses/`: every API response.
- `recorder-*.jsonl`: the engine returns and errors, per runtime start.
- `runtime-*.log`: runtime logs.
- `t4.after-p2.sha256` and `containment-comparison.txt`: the inventory and its
  comparison.
- `recorder-build/t4-recorder.jar`: the recorder as run (sha256 recorded in
  `results.json`). Build intermediates were removed.

No credential appears in the evidence: the pgvector password was random per run
and was never written.
