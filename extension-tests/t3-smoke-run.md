# T3 Preparation — Caffeine-Only Smoke Run

**Preparation, not part of T3.** Approved 30 September 2026 as a prerequisite for
freezing T3. No Redis was started, and no T3 assertion was evaluated.

## Purpose

In F3 the runtime refused every request ("model profile … not published to this
environment", then "prompt not found"; results §8, deviation 2). T3's
behavioural assertions need requests to pass through the full pipeline. This run
checked whether that can be achieved **without editing a protected file**, and
whether a cache hit is observable through the existing API.

## Configuration

- **Runtime revision:** monorepo `7e44342b2fe82414f297f4fcf517c858c6428257`,
  `Enterprise_AI_Runtime_Service` clean before and after the run.
- **Runtime build:** `runtime-api-1.0.0-SNAPSHOT-app.jar`, rebuilt from current
  source by the script, SHA-256
  `4c7eadc6e2c74e35008e7f3f2d5637b69f1b14f86377c1ab6002e6f33450716f`.
- **Stub gateway:** `wiremock/wiremock:3.9.1`, the image `RuntimeServiceIT` uses,
  with `/v1/inference/chat` and `/v1/health` stubs.
- **Provisioning, environment variables only:** `RUNTIME_ENVIRONMENT=integration`,
  `RUNTIME_SECURITY_MODE=NONE`, `RUNTIME_CACHE_PROVIDER=caffeine`,
  `MODEL_GATEWAY_URL=http://localhost:18080`, `SERVER_PORT=18081`.
- **Headers:** application `retail-dashboard`, use case `policy-qa`, environment
  `integration`, region `australia`, tenant `acme`.
- **Request:** `{"promptId":"policy-qa","messages":[{"role":"user","content":"What is the refund window?"}]}`, sent twice.
- **Why `policy-qa`:** it is the only use case whose policy enables the cache.

`application.yml`, shared types and the cache implementation were not modified.

## Command

```
extension-tests/t3-harness/smoke-caffeine.sh extension-tests/t3-smoke/attempt-1
```

## Outcome

**Attempt 1 of 1: succeeded.** No attempt failed, so none is omitted.

| | HTTP | `cached` | `finishReason` | Cost | Gateway calls (cumulative) |
|:---|:---|:---|:---|:---|:---|
| Request 1 | 200 | false | STOP | 0.00012000 / 0.00002800 USD | 1 |
| Request 2 | 200 | **true** | CACHED | 0 / 0 USD | **1** |

- Readiness: `{"status":"UP","checks":{"configuration":"UP","configurationVersion":"local-configuration","modelGateway":"UP"}}`.
- The second request was answered from the cache without a gateway call. That is
  the "observed hit" T3's B1 requires, seen through the existing `cached` flag and
  the gateway's request count.
- **Observation for the harness:** the `cache=hit` annotation the cache writes to
  the execution context does not appear in the response metadata. The harness
  relies on `cached` plus the gateway count, as the protocol specifies.

Full logs and both responses are in `t3-smoke/attempt-1/`.

## Attempts 2 and 3: the T3 recorder (30 September 2026)

After the harness review, observation moved to a harness-owned **T3 recorder**
(`t3-harness/recorder/`), loaded into the runtime process from outside its source
tree through Spring Boot's `PropertiesLauncher` and `loader.path`. These two
attempts checked, under Caffeine only, that the recorder loads and records
correctly. Same configuration as attempt 1, plus
`RECORDER_JAR=<built jar>`.

**Attempt 2: failed.** The runtime did not start: `Unsupported class file major
version 70`. The recorder had been compiled with JDK 26's default target, which
Spring 6.2's bytecode reader cannot parse. The runtime itself targets Java 21
(`<java.version>21</java.version>`). **Fix:** `build-recorder.sh` now compiles with
`--release` read from the runtime's own `pom.xml`. Logs are in
`t3-smoke/attempt-2/`.

**Attempt 3: succeeded.** Recorder jar SHA-256
`0705d97cdf9c76de44851ee064945bda18746d49136a777bb33e3123bc4e8a15`.

| | HTTP | `cached` | Gateway calls (cumulative) |
|:---|:---|:---|:---|
| Request 1 | 200 | false | 1 |
| Request 2 | 200 | **true** | **1** |

The recorder installed itself on the realization the runtime selected
(`CaffeineResponseCache`) and recorded, in order: `lookup-called` (key
`eair:v1:00c05eb0…`), `store-called` (the outcome before storage),
`lookup-called` and `lookup-returned` (the outcome the cache returned), all under
one key. Behaviour was unchanged: the hit was still observed, and the gateway was
still called once. The runtime repository was clean before and after. Logs and
the recorder output are in `t3-smoke/attempt-3/`.

## Attempts 4 and 5: the non-interfering recorder (30 September 2026)

After the recorder review, the recorder was changed so that a recording failure
can never alter a cache operation: every recording step is guarded, failures go
to standard error as `T3-RECORDER-ERROR` lines, and events carry sequence
numbers. Both attempts are Caffeine only.

**Attempt 4, normal recording: succeeded.** Recorder jar SHA-256
`61f6079fed3d9c8539cb2d1040e45351ced9e24499189ffb3610011992990f0d`. Request 1
was a miss (gateway calls 1), request 2 a hit (gateway calls still 1). Events
were recorded with sequence numbers 1–5, all under one key: `recorder-installed`,
`lookup-called`, `store-called`, `lookup-called`, `lookup-returned`.

**Attempt 5, recording deliberately broken: succeeded as a non-interference
check.** The recorder's output path was set to a directory
(`RECORDER_OUT=t3-smoke/attempt-5/unwritable-dir`), so every write failed. All
five events produced a `T3-RECORDER-ERROR` line in the runtime log, and **cache
behaviour was unchanged**: request 1 `cached: false` (gateway calls 1), request 2
`cached: true` (gateway calls still 1). The harness's integrity check, applied to
this log, reported all five errors, so a real run would have marked every
recorder-dependent assertion INCOMPLETE.
