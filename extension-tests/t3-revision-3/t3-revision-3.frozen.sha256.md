# T3 Revision-3 Frozen Record

**Revision 3 frozen 30 September 2026. Not run.** Freeze approved after the
source review of revision 3. **Reviewed revision: paper commit `0ee4edb`.** The
revision-3 run requires a separate approval.

This record **supersedes `t3-post-repair.frozen.sha256.md` for the revision-3
run only.** Earlier records and runs are unchanged and remain final:

- the original freeze, with initial attempts 1 (aborted before measurement) and
  2 (Redis not selectable; B1–B7 NOT ASSESSED);
- the post-repair freeze and run (`cd81624`): within-instance PASSes, B5a and B5b
  FAIL, B4 INCOMPLETE.

## Verified at freeze

1. The six reviewed digests match: protocol `c0b468be…`, harness `494081e8…`, the
   two regression tests `0078fab9…` and `7bb30828…`, the repaired key factory
   `d37ad727…` and the repaired `runtime-cache/pom.xml` `851afaa1…`.
2. The regression tests in the runtime are byte-identical to the reviewed copies.
3. Every other post-repair frozen file verifies unchanged.
4. A fresh inventory is identical to the reviewed revision-3 footprint: permitted
   changes (the two repairs), two added test files, **no protected surface
   changed**. The runtime contains exactly those four changes.
5. No T3 containers are present.

## Runtime state at freeze

Prototypes monorepo `7e44342b2fe82414f297f4fcf517c858c6428257`, plus these four
uncommitted changes in `Enterprise_AI_Runtime_Service`:

```
851afaa12c838ee24778e5f9f5dd8c332aaf4c8f89132b3517f2b3820b2cec7c  Enterprise_AI_Runtime_Service/runtime-cache/pom.xml
d37ad72788aa333fdca19042c1eafab1590723ffc41ff3523b0463a2d139880e  Enterprise_AI_Runtime_Service/runtime-cache/src/main/java/com/enterprise/ai/runtime/cache/response/ResponseCacheKeyFactory.java
0078fab97fe2df7d31eb5497c5b3c282f7a00ff10d9408cca0686f288002ed40  Enterprise_AI_Runtime_Service/runtime-cache/src/test/java/com/enterprise/ai/runtime/cache/response/CrossProcessKeyComputer.java
7bb308282c7a4024d17030b793b9b70cd3f5e451b1f98a587e2c0240e780c1cf  Enterprise_AI_Runtime_Service/runtime-cache/src/test/java/com/enterprise/ai/runtime/cache/response/ResponseCacheKeyCrossProcessTest.java
```

Containment for the revision-3 run is compared against the frozen **pre-repair**
before-inventory, `t3.before.sha256`. Redis image unchanged:
`redis:7.4-alpine@sha256:858f009f9709ce576febc734aa78b8f6d624b82571f9ddb6bda4377c833b3499`.

## Documented limitation carried forward

F3 recorded 596 AI Runtime tests; the full runtime suite during revision-3
preparation totalled 300 (surefire reports). The difference is **unreconciled**,
and the current suite must not be described as equivalent in coverage to F3
until it is.

## Frozen digest set (revision 3)

```
c0b468bea76d168ec5ee0591ef49bb65f7fbf49eadc62456193fdbbcb75f872a  t3-response-cache-protocol.md
cac377a2be8c2f22012eb34e96c06e6690c18669bb92d1e64cddbd33b66b42ca  freeze_interface_inventory_t3.py
8d584dad2c481ef0fa31061cb11cea9e5f97b3174e278e8e8df088e9e8c9a6fd  t3-histories.json
494081e841988f04e8d7f9b981565efff9aede61851bd0457ff9bec9e409fba7  t3-harness/run_t3.py
7193b4bc9647b6b76601f9fc07dff1666c8945c0637e2f4f7a471448666b746e  t3-harness/recorder/src/t3harness/T3RecorderAutoConfiguration.java
ebb7452feba844e00e2f09cf8a420689d8503d8a4ab52e7f70f6882a8facc7fa  t3-harness/recorder/src/META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports
eb3e9b5ec39f56a0abe11ca1370329780a1a7474d6859d2ec764ef41e45e89b2  t3-harness/recorder/build-recorder.sh
0508a737d883193677d7ab13a930858983e24612057e204672172667708c9dbf  t3-harness/KeyProbe.java
d0e5cf68ad5733826a3f187e5bfea052ed17bfa4380a55c3922c4d9f7dc79f13  t3-harness/run-key-probe.sh
5261a2425d45fb89b988c3685d404637b853f859c401a540e5d0af7e32a83b57  t3.before.sha256
455e82b3672fc1bdc2110bdc877eaf20406e8dd120bf44113bdb5d33d0669d0d  t3-revision-3/key-repair.diff
c9886125168219394949daba647f0da2c7b58978053ba1fd5b2765f4cccf38ca  t3-revision-3/ResponseCacheKeyFactory.before-key-repair.java
d37ad72788aa333fdca19042c1eafab1590723ffc41ff3523b0463a2d139880e  t3-revision-3/ResponseCacheKeyFactory.after-key-repair.java
0078fab97fe2df7d31eb5497c5b3c282f7a00ff10d9408cca0686f288002ed40  t3-revision-3/CrossProcessKeyComputer.java
7bb308282c7a4024d17030b793b9b70cd3f5e451b1f98a587e2c0240e780c1cf  t3-revision-3/ResponseCacheKeyCrossProcessTest.java
6197e15faaa743760ee25f228d3ac2b024ffc2dd043f57435f5c8769ce6c4e81  t3-revision-3/t3.after-revision-3.sha256
d899b20c37d6f0600f51de7b6574ef472fae05d68a50e1c4186d46de39350d71  t3-revision-3/harness-and-protocol.diff
```

Verify with `shasum -a 256 -c` on the block above, run from `extension-tests/`.
The runtime block verifies from the prototypes root (`~/Desktop/AI Projects`).
