# T3 Post-Repair Package

**STATUS: FROZEN 30 September 2026 — NOT RUN.** Frozen digests: `t3-post-repair.frozen.sha256.md`. The post-repair behavioural run requires a separate approval.

Prepared 30 September 2026, after the T3 initial run (attempt 2, commit
`e55a0b9`) found that the Redis realization could not be selected as built. The
initial run's findings are final and unchanged: the runtime failed to start with
Redis selected, and **B1–B7 are NOT ASSESSED**. Nothing here alters them. The
post-repair run will be a separately labelled experiment (`run_t3.py post-repair`,
fresh directory) and is reported separately, never merged with the initial run.

## 1 The repair (in the prototypes monorepo, uncommitted there)

One line removed from `Enterprise_AI_Runtime_Service/runtime-cache/pom.xml`: the
`<optional>true</optional>` on `spring-boot-starter-data-redis-reactive`
(`repair.diff`). The file's pre-repair content is kept as
`runtime-cache.pom.before-repair.xml`.

- **Surface class:** permitted (`runtime-cache/pom.xml`, frozen manifest §4).
  **`runtime-api/pom.xml` was not touched.**
- **This is an experimental repair choice**, not a conclusion that a cache
  component should own deployment dependencies. Whether the owning component or
  the assembling application should decide what ships is recorded as an open
  architectural question.

| | SHA-256 |
|:---|:---|
| `runtime-cache/pom.xml` before repair | `fa07f39caf17fa04ad2ed08699dc64362d6b19daf20724b75bf4d6af3945145f` |
| `runtime-cache/pom.xml` after repair | `851afaa12c838ee24778e5f9f5dd8c332aaf4c8f89132b3517f2b3820b2cec7c` |
| `repair.diff` | `f3fc6a876179c069a27a5fc72fc0ada9df894eca69bbf5b6987bca1c68e6dcc8` |

## 2 Verification before any behavioural test

These checks confirm only that the repair makes Redis selectable. They are not
T3 assertions, and no request was sent.

| Check | Result |
|:---|:---|
| Deployable rebuilt from source | Runtime jar SHA-256 `8faf7615e55f6997…` (was `fa8ee5cb…` in the initial run) |
| Redis client libraries packaged | **Yes:** `spring-data-redis-3.5.0.jar` and `lettuce-core-6.5.5.RELEASE.jar` are now in `BOOT-INF/lib` (library count 126 → 135) |
| Redis `ResponseCache` bean created | **Yes:** with `RUNTIME_CACHE_PROVIDER=redis`, the runtime started (1.5 s) and the T3 recorder reported `RedisResponseCache` as the installed realization, with no recorder errors. No Redis container was running and no request was made (`bean-check/`). |
| Repair footprint against the frozen before-inventory | **One permitted change** (`runtime-cache/pom.xml`); **no protected surface changed** (`repair-footprint-comparison.txt`, `t3.after-repair.sha256`) |
| Runtime repository | The only change is the repair |

## 3 Tooling change: relative-path fix

The fix for the defect behind initial-run attempt 1. It makes the output path
absolute in the three places that pass it to Maven (`tooling-path-fix.diff`,
against frozen commit `bdbed44`):

- `recorder/build-recorder.sh`: `OUT="$(cd "$OUT" && pwd)"`
- `run-key-probe.sh`: `OUT="$(cd "$OUT" && pwd)"`
- `run_t3.py`: `out = Path(sys.argv[2]).resolve()`

Each also gains a comment explaining why. **No assertion, pass rule or
measurement changes.** Checked: a relative path now resolves correctly, and
nothing is written into the runtime repository.

| File | Frozen SHA-256 (`bdbed44`) | Revised SHA-256 |
|:---|:---|:---|
| `t3-harness/run_t3.py` | `bbec920fdfcf…` | `a3b19b31629318254cd46b75eb2a5d62116a8ea5d103a3558215a0e8a2c44edc` |
| `t3-harness/recorder/build-recorder.sh` | `89fc5bf022ab…` | `eb3e9b5ec39f56a0abe11ca1370329780a1a7474d6859d2ec764ef41e45e89b2` |
| `t3-harness/run-key-probe.sh` | `0dab3ea00f4d…` | `d0e5cf68ad5733826a3f187e5bfea052ed17bfa4380a55c3922c4d9f7dc79f13` |

All other frozen files (protocol, inventory script, histories, recorder source,
key probe source, before-inventory) are unchanged.

## 4 How the post-repair run is compared

- **Containment** is compared against the **frozen pre-repair before-inventory**
  (`t3.before.sha256`), so the repair itself appears in the footprint (one
  permitted change), together with anything else the run needs.
- **B1–B7** use the frozen assertions and pass rules unchanged.
- **The history-key expectation (protocol §8) is not assumed.** B5-keys-live and
  B5b report what the live instances actually do. The initial run's probe
  observation (identical keys across two fresh JVMs) is reported alongside, as a
  separate observation.

## 5 Status

Re-frozen after review and the four verification checks recorded in
`t3-post-repair.frozen.sha256.md`. **Awaiting a separate approval to execute the
post-repair run.**
