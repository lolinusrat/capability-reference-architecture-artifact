# T3 — In-Process Cache to Networked Cache

## 1 The question

> Can the AI Runtime's response cache be moved from an in-process realization to a
> networked one without changing shared types or any neighbouring interface, while
> the cache still behaves as a cache?

## 2 Scope

| | |
|:---|:---|
| **Domain** | AI Runtime (response caching) |
| **Contract** | `ResponseCache` SPI, `runtime-common/.../common/spi/ResponseCache.java`, first committed `a68e2b06`, 5 August 2026 |
| **Realization A** | `CaffeineResponseCache`: process-local |
| **Realization B** | `RedisResponseCache`: networked, entries serialized to JSON text |
| **Selection** | `runtime.cache.provider` (`caffeine` → `redis`) |

**Domain placement is a retrospective judgement.** The paper does not assign
response caching to a domain. It is placed in AI Runtime because AI Runtime owns
execution coordination, context and execution state on the request path, whereas
Operations owns telemetry, provenance, cost and capacity monitoring. The
placement is recorded here before freezing; it is not claimed as something the
original architecture specified.

## 3 Why this is not the excluded guardrail case

Results §11.1 excluded the guardrail candidate partly because its realizations
were selected by one configuration property, and "no consuming code names either
realization, so no neighbouring interface *could* change, whatever the
substitution did." `ResponseCache` has the same selection structure. Flipping the
property and comparing file digests would therefore measure nothing, by the same
reasoning.

T3 differs in what it runs, not in how the realization is selected.
`RedisResponseCache` has **never been executed**: it has no unit test, and no
integration test reaches it. A live run introduces a serialization path
(`ChatOutcome` to JSON text and back) and a network path that no test has
exercised. Either can expose a real incompatibility whose repair would reach
shared types. That is the outcome T3 can observe and a property flip could not.
**A configuration flip without the live behavioural assertions in §7 does not
constitute T3.**

## 4 What counts as failure (containment)

**T3 fails if making Redis work requires any change to:**

1. the `ResponseCache` SPI;
2. `ChatOutcome` or any type it contains (`TokenUsage`, `Cost`, `FinishReason`,
   metadata), or any other type in `runtime-common/.../model`;
3. `Message` or `Role`, which enter the cache key;
4. the AI Runtime outward contract (`runtime-api` controllers, `wire` and error
   types);
5. shared serialization configuration (`runtime-api` configuration);
6. any neighbouring surface: Developer Experience, the Model Services outward
   contract, Governance and Security, or Evaluation.

A repair that works only because a shared type was changed **counts as failure,
not as a fix.**

## 5 What does not count as failure

- changes inside `runtime-cache`: `RedisResponseCache`, `ResponseCacheKeyFactory`,
  `RuntimeCacheConfiguration`;
- the `runtime.cache.provider` property, Redis connection settings and the Redis
  service in `docker-compose.yml`;
- new tests.

A change to `ResponseCacheKeyFactory` alters behaviour for Caffeine too, so it is
permitted only if all existing Caffeine tests still pass unchanged.

## 6 Contract inventory, frozen before Redis is run

A new script, `freeze_interface_inventory_t3.py`, captures SHA-256 digests of
every surface below. Each surface's class is fixed in the script, and the
script's `compare` mode applies it mechanically.

| Surface | Class |
|:---|:---|
| `ResponseCache` SPI | protected |
| `runtime-common/.../model` (`ChatOutcome`, `Cost`, `TokenUsage`, `FinishReason`, `Message`, `Role` and the rest of the package) | protected |
| `runtime-api/src/main/java` (controllers, `wire`, `error`, `RuntimeApiConfiguration`) | protected |
| `runtime-api/src/main/resources/application.yml` | protected |
| AI Runtime gateway client (`runtime-inference/.../gateway`, as F3) | protected |
| Shared dependency declarations: the root, `runtime-common` and `runtime-api` build files (`pom.xml`) | protected |
| Existing cache tests (`runtime-cache/src/test/java`) | protected-existing: new files permitted, existing files unchanged |
| The four neighbouring surfaces, as F3 | protected |
| `runtime-cache/src/main/java`, `runtime-cache/pom.xml` | permitted; reported |
| `docker-compose.yml` | permitted; reported |

**Selection and connection are made through environment variables**
(`RUNTIME_CACHE_PROVIDER=redis`, `SPRING_DATA_REDIS_HOST`, `SPRING_DATA_REDIS_PORT`),
so no protected file is edited to switch realizations.

## 7 Behavioural assertions (live Redis, pinned image version)

`RedisResponseCache` treats every Redis or deserialization failure as a cache
miss and continues. A broken cache therefore produces correct answers, just
never cached ones. **Every hit must be positively observed.** A run in which no
hit is observed is a failure, not a pass.

**How evidence is observed, without touching a protected surface.**

- **Hits.** The runtime's existing public response carries a `cached` flag
  (`runtime-api/.../wire/RuntimeProtocol`), which the cache-hit path
  (`ChatOutcome.asCacheHit()`) sets to true. Every response is classified the
  moment it arrives. An **observed hit** is HTTP 200 with `cached` true **and**
  zero stubbed-gateway calls for that request. A **silent miss** is HTTP 200 with
  `cached` false and a gateway call. Anything else is **anomalous** or an
  **error**. Only an observed hit counts as a hit.
- **The T3 recorder (test-only instrumentation).** A harness-owned jar
  (`t3-harness/recorder/`), loaded into each runtime process from outside the
  runtime's source tree through Spring Boot's `PropertiesLauncher` and
  `loader.path`. It wraps the `ResponseCache` bean the runtime selected,
  delegates every call unchanged, and records the key of every lookup, the
  outcome handed to `store` (before serialization) and the outcome `lookup`
  returns (after the runtime's own deserialization). Outcomes are rendered by
  reflection over record components, **never through Jackson**, so the rendering
  is independent of the serializer under test. No file in §4 or §5 is changed.
  - **Non-interference.** Recording never affects a cache operation. Key
    computation, rendering and writing are all guarded; a failure is reported on
    a separate diagnostic channel (standard error, captured in the runtime log,
    as lines beginning `T3-RECORDER-ERROR`), and `store` and `lookup` proceed
    exactly as without the recorder. Every event carries a sequence number, so a
    lost event shows up as a gap.
  - **Recorder failure means incomplete measurement, never a pass.** At startup,
    the harness records whether each JVM's recorder installed cleanly, and that
    status is **retained and applied to every later request on that JVM**. After
    every request, it also checks for new diagnostic lines and sequence gaps. Any
    assertion that depends on recorder evidence reports INCOMPLETE when that
    evidence is missing or unreliable. Hits and misses themselves are observed
    without the recorder (`cached` flag and gateway count), so a miss remains a
    FAIL whatever the recorder shows.
  - **The recorded key is a separately computed observation.** Both realizations
    compute the key they use internally with `keyFactory.key(context)`, and their
    `key(context)` returns the same factory's result for the same context. The
    recorder calls `key(context)` separately, so its key is an observation by the
    same factory on the same context, not a value captured from inside the cache
    call. Where Redis is involved, it is **cross-checked against the key `MONITOR`
    shows the instance actually issued** (B1, B5a, B5b).
  - Caffeine-only checks of the recorder, including a run with recording
    deliberately broken, are recorded in `t3-smoke-run.md` (attempts 2–5).
- **Redis `MONITOR`** records every key each instance actually issues, including
  on misses, and corroborates the recorder.

**Outcomes.** PASS; FAIL; NOT_EXERCISABLE (the configuration cannot vary the
input, with the reason given); INCOMPLETE (no failure observed, but not every
required case was exercised); and OBSERVATION. **NOT_EXERCISABLE and INCOMPLETE
are never counted as passes.** Results are written after every assertion and
again on any exception, so an interrupted run leaves a structured record marked
incomplete rather than raw logs alone.

- **B1 Hit is real.** A silent miss, exactly one new Redis key (polled for up to
  5 seconds), then an observed hit. The recorder's key must be the same for both
  requests and must equal both the Redis key and the key `MONITOR` shows being
  `SET`. Behaviour decides FAIL. Missing or unreliable recorder evidence, or keys
  that disagree, make B1 INCOMPLETE, recorded explicitly.
- **B2 Round-trip equivalence**, in two parts, because a hit legitimately differs
  from the stored outcome: `asCacheHit()` sets `cached`, zeroes `cost` and marks
  `finishReason` as `CACHED`.
  - **B2a: round-trip through the runtime's own serializer.** The outcome handed to
    `store` and the outcome `lookup` returned, both captured by the recorder,
    must be equal in **every** record component, recursively, and must belong to
    the same entry: the store event's key, the returned event's key and the Redis
    key must all be identical. The runtime's own serializer does the serializing
    and deserializing; the harness does neither. A field mismatch on the same
    entry is a FAIL. Missing or unreliable recorder events, or outcomes that
    cannot be shown to belong to the same entry, make B2a INCOMPLETE. The raw Redis entry is kept as supporting
    evidence.
  - **B2b: public response.** The API response on a Redis hit equals the API
    response on a Caffeine hit for the same request.
  - **Equality rule:** decimals are compared numerically, without rounding. A
    difference of scale alone is **reported separately and is not a mismatch**,
    unless the contract gives scale meaning. JSON numbers are parsed as exact
    decimals, never binary floats.
- **B3 Key isolation.** Requests differing in tenant, model profile, variables,
  response schema, temperature or maximum output tokens must never share an
  entry. For each accepted variant, the harness requires a silent miss **and** a
  recorder key that differs from the base request's key. Where the input reaches
  the gateway, it also requires the corresponding field of the gateway request to
  have changed: tenant at `attributes.ai.tenant_id`, then `modelProfile`,
  `responseSchema`, `temperature` and `maxOutputTokens`. Variables have no
  observable effect on the gateway request for `policy-qa`, whose template uses
  none. Their result is labelled **key-only** rather than verified. An accepted
  variant whose gateway input did not change is a FAIL, not a pass. A rejected
  variant is NOT_EXERCISABLE, with its HTTP status. Prompt version (`policy-qa`
  has one approved version) and retrieval fingerprint (no `Retriever` realization
  exists) are **separate NOT_EXERCISABLE results**. The B3 outcome covers only
  the dimensions actually exercised.
- **B4 Expiry.** The `policy-qa` TTL is 5 minutes. It is set in the protected
  `application.yml`, and it is **observed, never shortened or bypassed**. B4
  records the time the recorder saw `store` called (a **mandatory** event:
  without it, or with unreliable recorder evidence, B4 is INCOMPLETE), reads the
  entry's TTL from Redis immediately afterwards, and requires 295 to 300 seconds. That window
  allows for whole-second reporting and the delay between insertion and reading.
  B4 then records the time the entry's expiry was detected (checked every
  second, limit 360 seconds) and requires the repeated request to be a silent
  miss.
- **B5 Cross-instance stability.** Two runtime instances, run as **separate JVM
  processes**, share one real Redis. A request served by one is an observed hit
  when repeated on the other.
  - **B5a: one-message history.** *(Relabelled in revision 3. It was previously
    described as "without conversation history", but the runtime maps every
    request message into the history that enters the key, so B5a's single user
    message is a one-message history.)* The request on A must be a **silent
    miss**, so that A demonstrably populated the entry. PASS requires that, an
    observed hit on B, and recorder keys for A and B that are present, equal to
    each other, and equal to the keys `MONITOR` shows A `SET` and B `GET`. A miss
    on B is a FAIL. Anything else short of PASS is INCOMPLETE, recorded
    explicitly.
  - **B5b:** with conversation history. The harness first verifies that
    `t3-histories.json` matches its frozen SHA-256 and holds 20 cases with
    distinct ids and distinct message lists; otherwise the run stops, incomplete.
    **Any observed miss on B is a FAIL.** A PASS requires every one of the 20
    cases to be exercised, populated by A (a silent miss on A), an observed hit
    on B, measured by the recorder on both instances, and corroborated by
    `MONITOR` (A's `SET` key and B's `GET` key equal the recorder's keys, and on a
    hit A and B used one key). Without a miss, anything short of that is
    **INCOMPLETE**, never a pass, and the result lists each shortfall
    separately: rejected cases, cases A did not populate, unmeasured cases, and
    key or `MONITOR` disagreements.
  - **B5-keys-live (observation).** The key each runtime instance actually used,
    recorded inside runtime A and runtime B by the recorder, compared history by
    history. `MONITOR` corroborates the keys instance B issues.
  - **B5-keys-probe (observation).** Two **independent same-build JVMs** (not the
    runtime instances) run `KeyProbe` against the unchanged `ResponseCacheKeyFactory`
    for all 20 histories. Their outputs are compared **by history id**, and a
    case present on one side only is reported.
  - Both key observations are reported beside B5a and B5b, never merged with them.
- **B6 Policy.** Opting out through `cacheable: false` must produce two silent
  misses and no new Redis key. A streamed request must reach the gateway's
  **stream** endpoint exactly once and the chat endpoint not at all, return a
  final event, and add no Redis key. Any of these failing is a FAIL. *(Revision 3,
  evidence-integrity correction:)* the streamed request's recorder events are
  consumed and checked, and if the behaviour passes but that recorder evidence is
  unreliable, B6 is INCOMPLETE, never PASS. With clean recorder evidence the
  outcome is exactly the pre-revision rule.
- **B7 Degradation.** With Redis stopped, a request is still served, as a silent
  miss.

## 8 Prior knowledge, disclosed

While drafting this protocol, the key construction was read. For conversation
history, `ResponseCacheKeyFactory` uses `invocation.history().hashCode()`.
`history` is a list of `Message(Role role, String content)`, and `Role` is an
enum. An enum's `hashCode` is identity-based and differs between JVM processes.
**B5 with history is therefore expected to fail:** two instances will compute
different keys for the same conversation. Caffeine, being process-local, could
never expose this.

It is disclosed before freezing, and it is **not fixed before execution**; fixing
it first would be tuning the test. If B5 fails as expected:

- a repair confined to `ResponseCacheKeyFactory` (for example, hashing the role's
  name and the content) is a within-domain change. The test is reported as having
  **surfaced a latent defect that was contained**;
- a repair that requires changing `Message`, `Role` or another shared type is a
  **containment failure** under §4.

## 9 Negative control

After the run, plant one Redis-specific annotation or field on `ChatOutcome`, and
confirm that the unchanged T3 inventory detects it. Revert the plant. This control
is reported separately.

## 10 Reporting

**Two results, never merged.**

- **Initial run:** the substitution as first executed, before any repair. Its
  containment outcome and its B1–B7 outcomes are final. A behavioural assertion
  that fails here stays failed in the report, whatever happens afterwards.
- **Post-repair run, if any:** the same assertions after a repair, with the
  repair's complete footprint, classified under §4 and §5.

A successful within-domain repair can show that a discovered defect was
**contained**. It does not turn the initial run into a clean pass.

In both runs, containment (§4) is reported separately from behaviour (B1–B7).
Interface stability is not quality. Report the full `runtime-cache` footprint and
the logged effort.

## 11 Decisions

Resolved on review (30 September 2026):

- **Harness:** two separate JVM processes sharing one real Redis instance, with a
  stubbed gateway (WireMock, as in `RuntimeServiceIT`).
- **Equality:** numerical, without rounding (§7, B2).
- **History:** B5a and B5b are reported separately; B5b compares keys directly
  across at least 20 histories.
- **Initial and post-repair results** are reported separately (§10).
- **Observation:** through the existing `cached` flag, the gateway call count and
  Redis keys (§7).

Settled during preparation (30 September 2026):

- **Use case: `policy-qa`.** It is the only use case whose policy enables the
  cache, so every T3 request uses it.
- **Provisioning is supplied by environment variables and headers only**
  (`RUNTIME_ENVIRONMENT=integration`, matching platform headers), as
  `RuntimeServiceIT` does. A Caffeine-only smoke run confirmed on 30 September
  2026 that the runtime serves requests this way and that a hit is observable
  through `cached` plus the gateway count. The run is recorded in
  `t3-smoke-run.md`; it is preparation, not part of T3.
- **The `cache=hit` context annotation does not appear in the response metadata.**
  Hits are observed through the `cached` flag and the gateway count, as §7
  already specifies.
- **The harness is `t3-harness/run_t3.py`**, with every pass rule fixed in code.

Revised on harness review (30 September 2026):

- **Test-only instrumentation:** the T3 recorder (§7) replaces reading keys from
  Redis alone. It gives B2a the true stored and returned outcomes, and gives
  B5-keys and B3 the keys the live instances used.
- **B5-keys** is split into live keys (recorder) and probe keys (independent
  same-build JVMs), both reported as observations.
- **B5b** verifies the histories file's digest and distinctness and requires all
  20 cases; a partial result is INCOMPLETE.
- **B3** verifies the effective input at the gateway; **B4** records insertion,
  TTL-read and expiry times; **B6** verifies the stream endpoint was called.
- **Results survive failure:** written after every assertion and on any exception.

Revised on the recorder review (30 September 2026):

- **The recorder is non-interfering.** Recording failures go to a separate
  diagnostic channel and never alter a cache operation. This was shown under
  Caffeine with recording deliberately broken (`t3-smoke-run.md`, attempt 5).
- **Recorder failures, and sequence gaps, make recorder-dependent assertions
  INCOMPLETE**, never PASS.
- **The recorded key is documented as a separately computed observation** and
  cross-checked against `MONITOR` in B1, B5a and B5b.
- **B4 requires the store-called event.** B2a requires the same-entry key check,
  and B5a requires the key agreement check.

Revised on the final source review (30 September 2026):

- **B5b's outcome incorporates measurement integrity.** A miss is a FAIL. A PASS
  needs all 20 cases populated by A, hit on B, measured and corroborated.
  Anything else is INCOMPLETE, with each shortfall listed separately.
- **Recorder startup integrity is retained per JVM** and enforced on every
  recorder-dependent assertion.
- **B5a and B5b require A's request to be a silent miss.**
- **Key disagreement is INCOMPLETE, not FAIL**, in B1, B2a, B5a and B5b: it means
  the measurement is inconsistent, not that the behaviour failed. It is always
  recorded explicitly, never treated as corroborated.

Revision 3, after the post-repair run (30 September 2026; prepared, not frozen):

- **B5a is relabelled "one-message history"**, which is what it has always
  tested. Its assertion and pass rule are unchanged. B5b's 20 histories are
  unchanged.
- **B6 now consumes its streamed request's recorder events**, so the continuity
  check no longer reports a false gap on the next request (which made B4
  INCOMPLETE in the post-repair run). B4's TTL assertion and expiry window are
  unchanged.
- **B6 evidence-integrity correction:** unreliable recorder evidence for the
  streamed request makes B6 INCOMPLETE instead of PASS. The behavioural rule,
  which decides FAIL, is unchanged.
- **A second repair is under test**: `ResponseCacheKeyFactory` digests each
  history turn's role name and content in order, instead of calling
  `history().hashCode()`. It is a permitted surface; `Message` and `Role` are not
  changed.

Factual inputs, fixed 30 September 2026:

- **Redis image: `redis:7.4-alpine`, pinned to index digest
  `sha256:858f009f9709ce576febc734aa78b8f6d624b82571f9ddb6bda4377c833b3499`**,
  the same tag the runtime's `docker-compose.yml` already uses. The run references
  the image by digest, not by tag.
- **Histories: `t3-histories.json`**, 20 cases. Cases H07/H08 differ only by
  role and H09/H10 only by order, so a key that ignored role or order would be
  caught. The file is included in the frozen digest set.

Nothing further is open for T3.
