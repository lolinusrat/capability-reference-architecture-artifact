# T3 Initial Run — Attempt 2 Report

**30 September 2026, 08:46–08:49Z.** Frozen commit `bdbed44`, frozen code
unchanged, launched with an absolute output path (approved after attempt 1
aborted on the relative-path defect). Runtime jar SHA-256 `fa8ee5cb…`, recorder
jar `e5d5bf7c…`, Redis image `sha256:858f009f…` (pinned).

This is the **initial run** under protocol §10. Its outcomes are final; any
repair belongs to a separately approved post-repair run.

## Result: the substitution could not start

**With `RUNTIME_CACHE_PROVIDER=redis`, the runtime failed to start.** No
`ResponseCache` bean existed:

> No qualifying bean of type 'com.enterprise.ai.runtime.common.spi.ResponseCache'
> available … APPLICATION FAILED TO START

**Cause, confirmed from the built application.** The runtime jar contains
`runtime-cache` (including `RedisResponseCache`) but **no Redis client libraries**:
no `spring-data-redis`, no Lettuce. `runtime-cache/pom.xml` declares
`spring-boot-starter-data-redis-reactive` as `<optional>true</optional>`, and
`runtime-api/pom.xml` does not add it. The Redis wiring is guarded by
`@ConditionalOnClass(ReactiveStringRedisTemplate.class)`, so it was skipped, no
cache bean was created, and startup failed.

So **the Redis realization, as built, cannot be selected by configuration.**
Selecting it needs a build-level dependency change. This had never been
observed, because no test had ever started the runtime with Redis. It is the kind
of previously unexercised path T3 was designed to run. The failure was loud (the
application refused to start), not silent.

## Assertion outcomes

| Assertion | Outcome |
|:---|:---|
| B1–B7 (Redis) | **Not assessed.** The Redis-backed runtime never started, so no assertion executed. None is a pass. |
| Caffeine reference (B2b input) | Ran: silent miss, then an observed hit, with the recorder capturing the key. |
| B5-keys-probe (observation) | Ran: see below. |
| B5-keys-live, B5b | Not run. |

`results.json` records `status: incomplete`, phase reached, and the exception.

## Containment

After-inventory captured and compared (`t3.after.sha256`,
`containment-comparison.txt`): **no protected surface changed**, and no
permitted surface changed either. This is expected: no repair was attempted. The
runtime repository was clean after the run, and the recorder installed cleanly
with no errors.

## Observation: B5-keys-probe

Two independent same-build JVMs (not the runtime instances) computed keys for
all 20 histories, using the unchanged key factory (class SHA-256 `bfb6053d…`,
matching the frozen record) and the frozen histories file (SHA-256 `8d584dad…`).
**All 20 keys were identical across the two JVMs.**

**This does not bear out the expectation disclosed in protocol §8**, which
predicted differing keys because `Role` is an enum with an identity-based
`hashCode`. A plausible explanation, **not verified**: HotSpot's identity-hash
generation can repeat across fresh JVMs that execute identical code in the same
order, as these two probe processes did. Runtime instances serving different
request sequences might still diverge. The observation that would settle that,
B5-keys-live, compares the keys two running instances actually used, and it did
not run. The §8 expectation is therefore **neither confirmed nor refuted for
live runtime instances.**

## What a repair would involve (for decision; nothing has been changed)

Selecting Redis requires the Redis client libraries in the deployable. Under the
frozen manifest (§4 and §5), the containment classification depends on **where**
the dependency is added:

- **`runtime-cache/pom.xml`** (permitted): make the Redis starter non-optional.
  This would be a within-domain change.
- **`runtime-api/pom.xml`** (protected): add the starter in the application
  assembly. This would be a **containment failure** under protocol §4.

Which location is architecturally correct is a real design question: whether the
component that owns the realizations, or the application that assembles them,
decides which realizations ship. It is recorded here for the repair decision and
is not pre-judged.
