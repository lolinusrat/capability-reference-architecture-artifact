# T3 Post-Repair Run — Report

**30 September 2026, 08:57–08:58Z.** Re-frozen tooling (commit `03ec627`), frozen
assertions unchanged, fresh directory, label `post-repair`. The repair is the one
line removed from `runtime-cache/pom.xml` (the Redis starter's `<optional>`). This
report is **separate from the initial run**, whose findings are unchanged: the
Redis realization was not selectable as built, and B1–B7 were NOT ASSESSED.

Run status: `complete`. Both runtime instances started with
`RedisResponseCache`, and the recorder installed cleanly on both.

## Assertion outcomes

| Assertion | Outcome | Evidence |
|:---|:---|:---|
| B1 hit is real | **PASS** | Silent miss, then an observed hit. The recorder key equals the Redis key and the key `MONITOR` shows being `SET`. |
| B2a round-trip through the runtime's serializer | **PASS** | Every record component equal between the outcome stored and the outcome returned; same entry (store key = returned key = Redis key); no scale differences. |
| B2b Redis hit equals Caffeine hit | **PASS** | Public responses equal. |
| B3 key isolation (exercised dimensions) | **PASS** | Each accepted variant missed and had a different key. Tenant, response schema, temperature, maximum output tokens and model profile were verified at the gateway; variables are key-only (see `results.json`). |
| B3: prompt version | NOT_EXERCISABLE | One approved version of `policy-qa`. |
| B3: retrieval fingerprint | NOT_EXERCISABLE | No `Retriever` realization. |
| B5a cross-instance | **FAIL** | A populated the entry (silent miss), and B missed. The recorder's keys for A and B differ, and `MONITOR` confirms each instance's key. |
| B5b cross-instance, 20 histories | **FAIL** | All 20 exercised and populated by A; **all 20 missed on B**. The recorder agrees with `MONITOR` in every case. |
| B6 policy honoured | **PASS** | Opt-out never stored; streamed request reached the stream endpoint once, the chat endpoint zero times, and stored nothing. |
| B4 expiry | **INCOMPLETE** | See finding 2. Redis reported a TTL of 300 s, but expiry was not observed. |
| B7 degradation | **PASS** | With Redis stopped, the request was served as a silent miss in 0.23 s. |

**Observations.**
- **B5-keys-live:** for all 20 histories, the key runtime A used differed from the
  key runtime B used; the recorder agreed with `MONITOR` in every case.
- **B5-keys-probe:** two independent same-build JVMs produced identical keys for
  all 20 histories, as in the initial run.

## Containment

After-inventory against the frozen pre-repair before-inventory: **one permitted
change** (`runtime-cache/pom.xml`, the approved repair) and **no protected surface
changed**. The harness field `runtime_repository_unchanged_by_harness` is `false`
only because that approved repair is present in the runtime's working tree.

## Findings

**1. Cross-instance cache sharing does not work: the history-key defect (protocol
§8) is observed in live instances.** In B5a and in all 20 B5b cases, two runtime
instances computed different keys for identical requests, so an entry written by
one was never found by the other. Within one instance the keys are stable (B1,
B2a). This is consistent with the defect disclosed before freezing:
`ResponseCacheKeyFactory` hashes conversation history with `hashCode()` over
`Message(Role, String)`, and `Role` is an enum whose identity-based hash differs
between processes. The independent probe's identical keys (two fresh JVMs
running identical code) are consistent with the explanation recorded after the
initial run. The history hash is the only process-dependent input to the key
that the code shows; the other inputs are constant or value-based for these
requests (tenant, prompt id and version, profile name, empty variables, a
retrieval fingerprint of `"none"`, null schema, temperature and token limit).
**The cause is therefore strongly indicated, but it was not isolated
experimentally.** No repair has been attempted.

**2. B4 is INCOMPLETE because of a harness design flaw, not recorder loss.** B6's
streamed request is sent outside the harness's request path, so its two recorder
events (sequence 70 and 71, present in `recorder-A-redis.jsonl`) were never
consumed. The integrity check then reported a gap on the next request, which was
B4's. There were no recorder errors on either instance. Under the frozen rules,
missing or unreliable recorder evidence makes B4 INCOMPLETE, so it returned
before waiting for expiry.

**3. B5a did not test "without history".** The runtime maps every request message
into the conversation history that enters the key. B5a's single user message
therefore is a one-message history, and its failure is consistent with finding
1. The protocol's distinction between B5a and B5b does not hold for this API.

## What this establishes

- The Redis realization, once packaged, is **behaviourally compatible within an
  instance**: exact round-trip (B2a), public-response equivalence with Caffeine
  (B2b), key isolation (B3), policy (B6) and degradation (B7).
- **Its defining purpose, sharing entries across instances, fails** (B5a, B5b).
- **Containment held**: no protected surface changed. The failing behaviour is a
  defect inside the key construction, not an interface change crossing the
  boundary.
- The substitution surfaced **two latent defects that Caffeine could never
  expose**: the deployable did not package Redis (initial run), and the key is not
  stable across processes (this run).

## Not done, and why

Per the approval, anything requiring another repair or an assertion change stops
here for review:

- **Repairing the key** (for example hashing each role's name and content inside
  `ResponseCacheKeyFactory`, a permitted surface, rather than changing `Message`
  or `Role`, which are protected) would be a second repair.
- **Fixing the harness flaw behind finding 2**, and re-labelling or redesigning
  B5a (finding 3), would be harness or assertion changes.
