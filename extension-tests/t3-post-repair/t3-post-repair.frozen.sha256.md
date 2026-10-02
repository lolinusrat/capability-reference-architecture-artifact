# T3 Post-Repair Frozen Record

**Post-repair run frozen 30 September 2026. Not run.** Re-freeze approved after
review of `POST-REPAIR-PACKAGE.md` (commit `cc15c12`). The post-repair behavioural
run requires a separate approval.

This record **supersedes `t3.frozen.sha256.md` for the post-repair run only.**
The original frozen record, and the initial run made under it (attempt 1:
aborted before measurement; attempt 2: Redis not selectable, B1–B7 NOT ASSESSED),
are unchanged and remain final.

## Verified before re-freezing

1. **Revised scripts against frozen `bdbed44`:** the only changes are the
   absolute-path lines and their comments: `out = Path(sys.argv[2]).resolve()` in
   `run_t3.py`, and `OUT="$(cd "$OUT" && pwd)"` in `build-recorder.sh` and
   `run-key-probe.sh` (`tooling-path-fix.diff`). No assertion or pass rule changed.
2. **Full SHA-256 digests** of the three revised scripts and the repaired
   `runtime-cache/pom.xml` match `POST-REPAIR-PACKAGE.md`.
3. **The runtime's one-line repair is the only inventory change.** A fresh
   inventory, compared with the frozen before-inventory, shows one permitted
   change (`runtime-cache/pom.xml`) and no protected change. `git diff` of the
   runtime shows exactly the removed `<optional>true</optional>` line, and nothing
   else is modified or untracked in the runtime.
4. **Every other originally frozen file** verifies against `t3.frozen.sha256.md`.

## Runtime state at re-freeze

- Prototypes monorepo `7e44342b2fe82414f297f4fcf517c858c6428257`, plus the
  uncommitted one-line repair.
- `Enterprise_AI_Runtime_Service/runtime-cache/pom.xml`, post-repair SHA-256:
  `851afaa12c838ee24778e5f9f5dd8c332aaf4c8f89132b3517f2b3820b2cec7c`.
- Containment for the post-repair run is compared against the frozen
  **pre-repair** before-inventory, `t3.before.sha256`.
- Redis image unchanged: `redis:7.4-alpine` at
  `sha256:858f009f9709ce576febc734aa78b8f6d624b82571f9ddb6bda4377c833b3499`.
- The history-key expectation (protocol §8) is not assumed. The live
  instances' behaviour will be reported as observed.

## Frozen digest set (post-repair)

```
278cba3bb066471db5e8b3a66ae85840e5931b8e93ccf430f2e89fb754104f47  t3-response-cache-protocol.md
cac377a2be8c2f22012eb34e96c06e6690c18669bb92d1e64cddbd33b66b42ca  freeze_interface_inventory_t3.py
8d584dad2c481ef0fa31061cb11cea9e5f97b3174e278e8e8df088e9e8c9a6fd  t3-histories.json
a3b19b31629318254cd46b75eb2a5d62116a8ea5d103a3558215a0e8a2c44edc  t3-harness/run_t3.py
7193b4bc9647b6b76601f9fc07dff1666c8945c0637e2f4f7a471448666b746e  t3-harness/recorder/src/t3harness/T3RecorderAutoConfiguration.java
ebb7452feba844e00e2f09cf8a420689d8503d8a4ab52e7f70f6882a8facc7fa  t3-harness/recorder/src/META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports
eb3e9b5ec39f56a0abe11ca1370329780a1a7474d6859d2ec764ef41e45e89b2  t3-harness/recorder/build-recorder.sh
0508a737d883193677d7ab13a930858983e24612057e204672172667708c9dbf  t3-harness/KeyProbe.java
d0e5cf68ad5733826a3f187e5bfea052ed17bfa4380a55c3922c4d9f7dc79f13  t3-harness/run-key-probe.sh
5261a2425d45fb89b988c3685d404637b853f859c401a540e5d0af7e32a83b57  t3.before.sha256
f3fc6a876179c069a27a5fc72fc0ada9df894eca69bbf5b6987bca1c68e6dcc8  t3-post-repair/repair.diff
fa07f39caf17fa04ad2ed08699dc64362d6b19daf20724b75bf4d6af3945145f  t3-post-repair/runtime-cache.pom.before-repair.xml
21c9bc9fdc72f43e35495a94f9e76454d851d866c2eddd2d9ee8870f429c9bcb  t3-post-repair/t3.after-repair.sha256
```

Verify with `shasum -a 256 -c` on the block above, run from `extension-tests/`.
