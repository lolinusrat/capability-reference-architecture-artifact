# T3 Revision 3 Package

**STATUS: FROZEN 30 September 2026 — NOT RUN.** Reviewed revision: commit `0ee4edb`. Frozen digests: `t3-revision-3.frozen.sha256.md`. The revision-3 run requires a separate approval.

Prepared 30 September 2026, after the post-repair run (commit `cd81624`). That
run's results are unchanged and remain a valid record of the failure: within one
instance the Redis realization behaved correctly, but B5a and all 20 B5b cases
failed across instances, and B4 was INCOMPLETE. Any run under this revision gets
its own freeze, evidence directory, results and containment comparison.

## 1 Second repair: a process-independent history key

`ResponseCacheKeyFactory` (in `runtime-cache/src/main`, a **permitted** surface)
no longer calls `history().hashCode()`. It appends a SHA-256 digest of each turn's
**role name**, content length and content, **in order**. `Message` and `Role`
(protected) are unchanged.

- Order and role stay significant: `[USER a, USER b]` differs from
  `[USER b, USER a]`, and `USER a` from `ASSISTANT a`. The length prefix keeps the
  rendering unambiguous even if content contains the separators.
- **Content is never null, by contract.** `Message`'s canonical constructor
  rejects a null role or null content (`Objects.requireNonNull`, `Message.java`
  lines 19–20), and the API mapper additionally drops null-content messages
  (`InvocationMapper.java` line 73). The digest's use of `content.length()`
  therefore cannot meet a null.
- An empty history now contributes an empty string rather than `1` (the hash of
  an empty list). Keys for every request change once on deployment. The
  `eair:v1` namespace was **not** bumped; old entries simply stop matching and
  expire.
- Diff: `key-repair.diff` (both runtime repairs, `pom.xml` and key factory).
  Pre-repair file: `ResponseCacheKeyFactory.before-key-repair.java`, SHA-256
  `c9886125…`, identical to the file frozen as the key factory under test.
  Post-repair file SHA-256:
  `d37ad72788aa333fdca19042c1eafab1590723ffc41ff3523b0463a2d139880e`.

## 2 Regression test: identical keys across JVMs with different histories

Two new test files in `runtime-cache/src/test` (additions are permitted on the
protected-existing surface; copies are kept here):

- `CrossProcessKeyComputer.java`: a child-process entry point. With `perturb`, it
  first draws 400,000 identity hash codes across the main thread and four other
  threads, so the `Role` constants receive different identity hashes than in a
  plain process. It writes each case's key, plus the pre-repair component
  (`history().hashCode()`) for a sensitivity check.
- `ResponseCacheKeyCrossProcessTest.java`: runs one **plain** and one
  **perturbed** JVM. It requires the pre-repair component to differ between them
  (otherwise the check is reported **inconclusive**, not passed), then asserts
  identical keys for every case. A second test asserts that role-only and
  order-only differences still give different keys.

**Results, run as preparation (unit tests, no T3 run):**

| Check | Result |
|:---|:---|
| New test against the **repaired** factory | **Passed**, and ran rather than being skipped (the perturbation did change the pre-repair hash) |
| New test against the **pre-repair** factory, restored temporarily | **Failed**: the two JVMs produced different keys at history case 1, a one-message history (`sensitivity-old-factory.log`). The repaired file was then restored exactly (digest `d37ad727…` verified). |
| `runtime-cache` suite on the repair | 37 tests, 0 failures, 0 errors, 0 skipped; the 10 existing `ResponseCacheKeyFactoryTest` tests pass unchanged |
| Full runtime suite on the repair | 300 tests, 0 failures, 0 errors, 0 skipped (surefire reports) |

**What this establishes about the cause.** In a controlled setting, holding
every other key input fixed and changing only a JVM's execution history changed
the pre-repair keys and not the repaired ones. That isolates the enum-based
history hash as the cause **at unit level**. Whether the repair makes live
instances share entries is what the revision-3 run would test (B5a, B5b and
B5-keys-live).

**A discrepancy to flag.** F3 recorded 596 AI Runtime tests; this run's surefire
reports total 300. The reason has not been investigated. It may be counting
(for example, integration tests or duplicates in F3's figure). No test failed
either way.

## 3 Harness and protocol changes

Diff against the post-repair freeze: `harness-and-protocol.diff`.

- **B6 consumes its streamed request's recorder events.** The streamed request
  bypasses the harness's normal request path, so its events went unconsumed and
  the continuity check reported a false gap on the next request, making B4
  INCOMPLETE. B6's pass rule is unchanged; the events are now reported in its
  evidence. **B4's TTL assertion and expiry window are unchanged.** Checked by
  replaying the real post-repair recorder sequence: the old logic reproduces the
  false gap (`expected 70, got 72`), and the new logic reports none.
- **B6 evidence-integrity correction (after source review).** Consuming the
  stream's recorder events also means checking them: if B6's behaviour passes
  but that recorder evidence is unreliable, B6 is **INCOMPLETE**, never PASS. The
  behavioural rule is unchanged, and it alone decides FAIL. All four
  combinations were checked:

  | Behaviour | Recorder | Before | After |
  |:---|:---|:---|:---|
  | passes | clean | PASS | PASS |
  | passes | unreliable | PASS | **INCOMPLETE** |
  | fails | clean | FAIL | FAIL |
  | fails | unreliable | FAIL | FAIL |
- **B5a is relabelled "cross-instance, one-message history"**, which is what it
  has always tested. Its assertion and pass rule are unchanged. **B5b's 20
  histories are unchanged.**
- The protocol records all three changes under "Revision 3".

## 4 Footprint against the frozen pre-repair before-inventory

`revision-3-footprint-comparison.txt`:

- **Permitted:** `runtime-cache/pom.xml` (repair 1) and `ResponseCacheKeyFactory.java`
  (repair 2).
- **Protected-existing (additions permitted):** the two new test files; no
  existing test modified.
- **No protected surface changed.**

## 5 Digests (review copies; to be recomputed at freeze)

| File | SHA-256 |
|:---|:---|
| `t3-response-cache-protocol.md` | `c0b468bea76d168ec5ee0591ef49bb65f7fbf49eadc62456193fdbbcb75f872a` |
| `t3-harness/run_t3.py` | `494081e841988f04e8d7f9b981565efff9aede61851bd0457ff9bec9e409fba7` |
| runtime `ResponseCacheKeyFactory.java` (repaired) | `d37ad72788aa333fdca19042c1eafab1590723ffc41ff3523b0463a2d139880e` |
| `CrossProcessKeyComputer.java` | `0078fab97fe2df7d31eb5497c5b3c282f7a00ff10d9408cca0686f288002ed40` |
| `ResponseCacheKeyCrossProcessTest.java` | `7bb308282c7a4024d17030b793b9b70cd3f5e451b1f98a587e2c0240e780c1cf` |
| `key-repair.diff` | `455e82b3672fc1bdc2110bdc877eaf20406e8dd120bf44113bdb5d33d0669d0d` |

All other files in the post-repair frozen set are unchanged.

## 6 Status

Frozen after source review. The 596-versus-300 test-count difference remains an
unreconciled, documented limitation. **Awaiting a separate approval before any
revision-3 run.**
