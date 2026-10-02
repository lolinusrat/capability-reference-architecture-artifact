# T3 Freeze Package

**STATUS: FROZEN 30 September 2026 — NOT RUN.** Reviewed revision: commit `455c166`. The frozen digests are in `t3.frozen.sha256.md`. The Redis run requires a separate approval.

Assembled and frozen 30 September 2026. Nothing in this package has been executed
against Redis, and the key probe has been compiled but not run. This file is not
itself in the digest set, so its status line does not alter any frozen digest.

## 1 Source revisions

| Repository | Revision | Working-tree state |
|:---|:---|:---|
| Prototypes monorepo (`~/Desktop/AI Projects`), branch `paper3-cain2027-freeze` | `7e44342b2fe82414f297f4fcf517c858c6428257` | Runtime, SDK and Guardrail: clean. `Model_Gateway`: F3's uncommitted `application.yml` (SHA-256 `4a91a21c…`; see results §4 correction); outside T3's scope |
| Paper repository | recorded in the freezing commit | |

## 2 Redis image

`redis:7.4-alpine`, the tag the runtime's `docker-compose.yml` already uses.

| | Digest |
|:---|:---|
| Index (multi-platform) | `sha256:858f009f9709ce576febc734aa78b8f6d624b82571f9ddb6bda4377c833b3499` |
| `linux/arm64/v8` (this machine) | `sha256:1f09a89a207d794a8c61d9edfc26e7c58427de10ccef7c5d18d638df79a63b85` |
| `linux/amd64` | `sha256:ca0acbb137c1dc3339c8b147a58fd6f42775d4599327b50e7b116c23de501af2` |

The run references the image by digest, not by tag.

## 3 Digest set (frozen)

Identical to `t3.frozen.sha256.md`.

| File | SHA-256 |
|:---|:---|
| `t3-response-cache-protocol.md` | `278cba3bb066471db5e8b3a66ae85840e5931b8e93ccf430f2e89fb754104f47` |
| `freeze_interface_inventory_t3.py` | `cac377a2be8c2f22012eb34e96c06e6690c18669bb92d1e64cddbd33b66b42ca` |
| `t3-histories.json` | `8d584dad2c481ef0fa31061cb11cea9e5f97b3174e278e8e8df088e9e8c9a6fd` |
| `t3-harness/run_t3.py` (B1–B7 harness) | `bbec920fdfcf056d467f4e29361f89fccda3e5624e0bdb4f240cf2f51b5e41b4` |
| `t3-harness/recorder/src/t3harness/T3RecorderAutoConfiguration.java` | `7193b4bc9647b6b76601f9fc07dff1666c8945c0637e2f4f7a471448666b746e` |
| `t3-harness/recorder/src/META-INF/spring/…AutoConfiguration.imports` | `ebb7452feba844e00e2f09cf8a420689d8503d8a4ab52e7f70f6882a8facc7fa` |
| `t3-harness/recorder/build-recorder.sh` | `89fc5bf022ab3f521dddfa72a8e85c5112a983982f08fcc4f82073ee8376ac2c` |
| `t3-harness/KeyProbe.java` | `0508a737d883193677d7ab13a930858983e24612057e204672172667708c9dbf` |
| `t3-harness/run-key-probe.sh` | `0dab3ea00f4d2812c6377b99124cda19dc8ddf09fa74064f9170b94990e5dda5` |
| `t3.before.sha256` (before-inventory, 13 surfaces) | `5261a2425d45fb89b988c3685d404637b853f859c401a540e5d0af7e32a83b57` |

The protocol's reviewed digest (as `t3-response-cache-protocol.DRAFT.md`) was `63f2b2f57dddd4d0a9a2d9a000b6a1759d01957fc57a46045e0ac5f3a95bb168`. It differs only by the removed title marker.

Supporting, recorded but not part of the frozen set: `t3-harness/smoke-caffeine.sh`
(`04aa571ee05db5bdc5fc1eb8a5815f94e8df945126c28a693fcdc38eac361ecc`) and the
smoke-run record `t3-smoke-run.md` (attempts 1–5).

The recorder jar itself is rebuilt from the frozen source at run time; each run
records the jar's digest in `results.json`.

For reference, the key factory under test, unchanged:

| File | SHA-256 |
|:---|:---|
| `ResponseCacheKeyFactory.java` (source) | `c9886125168219394949daba647f0da2c7b58978053ba1fd5b2765f4cccf38ca` |
| `ResponseCacheKeyFactory.class` (current build) | `bfb6053dc495289241aa5667c3299788189d4eb5ece7721551f6339697af4cd5` |

## 4 Manifest

**Protected: any change is a T3 failure.**
- `ResponseCache` SPI
- `runtime-common/.../model`: `ChatOutcome`, `Cost`, `TokenUsage`, `FinishReason`,
  `Message`, `Role` and the rest of the package (10 files)
- `runtime-api/src/main/java`: outward contract and serialization configuration
- `runtime-api/src/main/resources/application.yml`
- AI Runtime gateway client (`runtime-inference/.../gateway`)
- Shared dependency declarations: root, `runtime-common` and `runtime-api` build files (`pom.xml`)
- Neighbours, as F3: Developer Experience; Governance and Security; Evaluation;
  Model Services outward contract

**Protected, existing files only: modifying or removing an existing file is a failure; new files are permitted.**
- `runtime-cache/src/test/java` (4 existing test files)

**Permitted: changes are allowed and reported as the footprint.**
- `runtime-cache/src/main/java`: realizations, `ResponseCacheKeyFactory`, cache wiring
- `runtime-cache/pom.xml`
- `docker-compose.yml`

**Recorded for reporting, outside the inventory.**
- The harness (`t3-harness/`), including the T3 recorder loaded into each runtime
  process from outside its source tree, and all outputs
- Environment variables used: `RUNTIME_CACHE_PROVIDER`, `SPRING_DATA_REDIS_HOST`,
  `SPRING_DATA_REDIS_PORT`
- The effort log, `t3-effort-log.md`

## 5 Checks performed before presenting this package

| Check | Result |
|:---|:---|
| Both JVM probes use the unchanged key factory | **Yes.** There is one probe class, run as two separate processes by `run-key-probe.sh`. It instantiates `ResponseCacheKeyFactory` from the runtime's own build output, never a copy, and each output file records the factory's code source and class digest. The launcher rebuilds `runtime-common` and `runtime-cache` from source first, so the probe cannot run against a stale jar in `~/.m2`. |
| All 20 histories come from the fixed file | **Yes.** The probe reads `t3-histories.json` and refuses to run unless it contains exactly 20 histories. Each output records the file's SHA-256. No history is constructed in code. |
| The suspected defect is unfixed | **Yes.** `ResponseCacheKeyFactory.java` line 76 still reads `append(material, "history", Integer.toHexString(invocation.history().hashCode()));`. Its source digest is recorded above and in the before-inventory. |
| The probe compiles against the current build | **Yes**, compiled only, **not run**. No key has been computed. |
| The inventory comparison classifies correctly | **Yes**, tested on a doctored copy of the inventory, with no file edited. A changed `ChatOutcome` produced `FAIL`; an added test produced `changed` (permitted); a changed key factory produced `changed` (permitted). |
| The runtime repository was not modified | **Yes.** `git status` is clean after all of the above. |

## 6 Historical: harness revision 2, after the first harness review

*Superseded review context, retained for the record. The approved harness is revision 4 (§6b).*

Protocol §7 is the authoritative statement of every rule; this is a summary.

| Review point | Revision |
|:---|:---|
| B5-keys did not run in the runtime JVMs | **B5-keys-live**: the T3 recorder records, inside runtime A and runtime B, the key each actually used; `MONITOR` corroborates. **B5-keys-probe** is renamed and described accurately as independent same-build JVMs, compared by history id. |
| B2a compared selected public fields | **B2a** compares, every record component recursively, the outcome handed to `store` against the outcome `lookup` returned, both captured by the recorder inside the runtime. The runtime's own serializer does the round trip; rendering is by reflection, not Jackson. |
| B5b controls | The histories file's **digest is verified** against the frozen value, and 20 distinct ids and message lists are required. **All 20 must be exercised** for a complete claim; a partial result is **INCOMPLETE**, never a pass. |
| An exception could lose the results | Results are written **after every assertion**, and on any exception, with `status: incomplete`, the phase reached and the traceback. Cleanup and the probe are guarded separately. |
| B3 effective input | Each accepted variant needs a silent miss, a **different recorder key**, and (where the input reaches the gateway) the **changed field in the gateway request**. Tenant is checked at `attributes.ai.tenant_id`, because the full map differs on every request. Variables are labelled key-only. |
| B4 timing | Records the store time (from the recorder), the TTL read immediately afterwards (295–300 s window), and the expiry detection time. |
| B6 stream | Requires exactly one call to the gateway's **stream** endpoint and none to chat. |
| B5-keys compared with `zip` | Compared **by id**; ids missing on one side are reported. |

**Checked without running Redis:** the harness compiles. On real recorder output
from smoke attempt 3, the store/lookup comparison reports no differences; on a
doctored copy, it flags a content mismatch and reports a scale-only difference
separately. The histories digest and distinctness checks pass. The recorder was
verified under Caffeine only (smoke attempts 2 and 3; attempt 2 failed, and the
cause is recorded).

## 6a Revision 3, after the recorder review

| Review point | Revision |
|:---|:---|
| Recorder failures could change cache behaviour | Every recording step (key computation, rendering, writing) is guarded and **never throws into a cache operation**. Failures go to a separate diagnostic channel: standard error, captured in the runtime log as `T3-RECORDER-ERROR` lines. Events carry sequence numbers. **Shown under Caffeine with recording deliberately broken** (smoke attempt 5): all five writes failed, all five were reported, and the cache hit was still observed with one gateway call. |
| Missing events must never pass | After every request, the harness checks for diagnostic lines and sequence gaps. Recorder-dependent assertions (B1, B2a, B3, B4, B5a, B5-keys-live) report **INCOMPLETE** when recorder evidence is missing or unreliable. Checked on the real attempt-5 log (5 errors detected), clean attempt-4 events (none) and a synthetic gap (detected). |
| The recorded key is a separate computation | Documented as a **separately computed observation** by the same key factory on the same context: both realizations compute their key internally with `keyFactory.key(context)`, and `key(context)` returns the same factory's result. It is cross-checked against the key `MONITOR` shows actually issued (`SET` by A, `GET` by B) in B1, B5a and B5b. |
| B4 could pass without the store event | The store-called event is **mandatory**; without it, B4 is INCOMPLETE. |
| B2a and B5a key checks | B2a requires store key = returned key = Redis key (same entry). B5a requires recorder keys for A and B, equal to each other and to `MONITOR`'s. |

## 6b Revision 4, after the final source review

| Review point | Revision |
|:---|:---|
| B5b could PASS with unreliable recorder evidence | B5b's outcome now incorporates measurement integrity. **Any observed miss on B is a FAIL.** A PASS needs all 20 cases exercised, populated by A, hit on B, measured by the recorder and corroborated by `MONITOR`. Otherwise the result is INCOMPLETE, listing rejected, unpopulated, unmeasured and disagreeing cases separately. Checked offline with scripted responses in seven scenarios: clean (PASS); one miss (FAIL); one unmeasured, one unpopulated, `MONITOR` disagreement, A/B key disagreement and one rejected (each INCOMPLETE, with the right list). |
| Recorder startup errors not enforced | Startup integrity is **retained per JVM** and forces every later request on that JVM to be marked unreliable. Checked through the real request path: a JVM with unclean startup marks its requests unreliable, with the reason. |
| A must populate the entry | B5a and B5b require the request on A to be a **silent miss**. |
| Disagreement handling | Key or `MONITOR` disagreement is INCOMPLETE, recorded explicitly, in B1, B2a, B5a and B5b, never treated as corroborated. Behaviour still decides FAIL. |
| Digest discrepancy | The digests the review computed for the recorder (`7193b4bc…`) and harness (`f7ac6871…`) are exactly those pinned in revision 3 (commit `8897ff5`); the earlier values (`562de3d7…`, `bf3ddf7d…`) belong to revision 2 (`6b54fd9`). Revision 4 changes the harness, so section 3 now pins the revision-4 digests. The recorder is unchanged since revision 3. |

## 7 Blocking items: resolved

1. **Runtime provisioning: resolved.** The Caffeine-only smoke run succeeded on
   its first attempt, with provisioning from environment variables and headers
   only (`t3-smoke-run.md`). A hit was observed through `cached` plus the gateway
   count.
2. **B1–B7 harness: written**, and included in the digest set above.
3. **Inventory tooling: corrected.** `compare` now rejects a missing, extra or
   reclassified surface as an invalid comparison (exit 2, "NOT ASSESSED"). This
   was tested on three doctored inventories.
4. **Baseline unaffected by preparation.** After all five smoke attempts and
   builds, a fresh capture is byte-identical to `t3.before.sha256`, and the
   runtime repository is clean.

**Frozen** after the revision-4 review. The Redis run starts only on a separate approval.
