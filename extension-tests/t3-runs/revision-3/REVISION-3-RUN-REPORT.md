# T3 Revision-3 Run — Report

**30 September 2026, 09:14–09:20Z.** Frozen commit `57761c0` (reviewed revision
`0ee4edb`). Before execution, the working tree and both digest blocks of
`t3-revision-3.frozen.sha256.md` verified, and the runtime held exactly its four
frozen changes. Fresh directory `t3-runs/revision-3`. The frozen harness accepts
only the labels `initial` and `post-repair`, so `results.json` records
`label: post-repair`; this run is identified by its directory and frozen record.
Runtime jar `65284eee…`, recorder jar `53e9cb03…`, Redis image `sha256:858f009f…`.

This report is **separate** from the initial attempts and the post-repair run
(`cd81624`). All of their evidence is unchanged.

Run status: `complete`. Both instances started with `RedisResponseCache`.

## Assertion outcomes

| Assertion | Outcome | Evidence |
|:---|:---|:---|
| B1 hit is real | **PASS** | Silent miss, then an observed hit; recorder key = Redis key = `MONITOR` `SET` key |
| B2a round-trip through the runtime's serializer | **PASS** | Every record component equal; same entry; no scale differences |
| B2b Redis hit equals Caffeine hit | **PASS** | Public responses equal |
| B3 key isolation (exercised dimensions) | **PASS** | Tenant, response schema, temperature, maximum output tokens and model profile verified at the gateway; variables key-only; base request still an observed hit afterwards |
| B3: prompt version | NOT_EXERCISABLE | One approved version of `policy-qa` |
| B3: retrieval fingerprint | NOT_EXERCISABLE | No `Retriever` realization |
| B5a cross-instance, one-message history | **PASS** | A populated the entry (silent miss); B observed a hit; keys agree with each other and with `MONITOR` |
| B5b cross-instance, 20 histories | **PASS** | All 20 exercised, populated by A and observed as hits on B; recorder measured every case and agreed with `MONITOR` in every case; no rejections, misses or disagreements |
| B6 policy honoured | **PASS** | Opt-out never stored; streamed request reached the stream endpoint once, the chat endpoint zero times, and stored nothing; its 2 recorder events were consumed and clean |
| B4 expiry | **PASS** | Store at 09:15:01.48Z (recorder); Redis TTL 300 s, read at 09:15:01Z; expiry detected at 09:20:01Z, 300 s after the TTL read (1 s polling); the next request was a silent miss |
| B7 degradation | **PASS** | With Redis stopped, the request was served as a silent miss in 0.12 s |

**Observations.**
- **B5-keys-live:** all 20 histories used identical keys on runtimes A and B, and
  the recorder agreed with `MONITOR` for every one.
- **B5-keys-probe:** two independent same-build JVMs produced identical keys for
  all 20.

## Recorder integrity

Clean throughout. There were no recorder errors or sequence gaps, both
instances' recorders started cleanly, and there were zero `T3-RECORDER-ERROR`
lines in any runtime log. The B6 fix worked as intended: the two streamed-request
events were consumed, and B4's first request showed no false gap.

## Containment

After-inventory against the frozen **pre-repair** before-inventory
(`containment-comparison.txt`): **no protected surface changed.**

- **Permitted:** `runtime-cache/pom.xml` (repair 1: package Redis) and
  `ResponseCacheKeyFactory.java` (repair 2: process-independent history key).
- **Protected-existing, additions permitted:** the two new regression-test files;
  no existing test modified.

The harness field `runtime_repository_unchanged_by_harness` is `false` only
because those four frozen changes are in the runtime's working tree. The run
itself changed nothing.

## What the three T3 runs establish together

| Run | Finding |
|:---|:---|
| Initial (attempt 2) | The Redis realization was **not selectable as built**: the deployable lacked the Redis client libraries. B1–B7 NOT ASSESSED. |
| Post-repair (`cd81624`) | After a contained packaging repair, Redis was **compatible within an instance** but **failed to share entries across instances** (B5a, B5b). B4 INCOMPLETE because of a harness flaw. |
| Revision 3 (this run) | After a second contained repair to the key's history encoding, **all B1–B7 assertions pass**, including cross-instance sharing across all 20 histories and the real 300-second expiry. |

Across all three runs, **no protected surface changed**. Both defects were
fixed inside the permitted cache component.

**The cause of the cross-instance failure is now supported by two independent
pieces of evidence.** It was isolated at unit level before this run: the
regression test shows the pre-repair key diverging across JVMs with different
execution histories and the repaired key not diverging. In this run, the live
instances share entries after the repair. That is strong support, not proof of
a single cause. Only the history encoding changed between the post-repair run
and this one, apart from the B6 harness fix, which does not affect B5.

## Limits

- **One author-built instantiation**, one pair of instances, one run.
- **Two B3 dimensions are NOT_EXERCISABLE**, and variables are isolated at key
  level only.
- **Test-count discrepancy:** F3 recorded 596 AI Runtime tests; the runtime suite
  during revision-3 preparation totalled 300. This is unreconciled, and the
  current suite is not claimed to match F3's coverage.
- **The repairs remain uncommitted** in the prototypes monorepo. They are recorded
  by diff and digest in the paper repository.
- **This report awaits review.** Run approval did not approve the results, and no
  further repair has been made.
