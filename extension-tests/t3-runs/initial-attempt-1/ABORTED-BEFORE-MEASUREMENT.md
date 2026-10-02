# T3 initial run, attempt 1 — aborted before measurement

**30 September 2026, 08:33Z. Frozen commit `bdbed44`, frozen code unchanged.**

The run stopped in the build phase. **No Redis container was started, no B1–B7
assertion ran, and the key probe computed no keys.** No T3 result exists from
this attempt. `results.json` records `status: incomplete`, with the exception.

## Cause

The run was launched with a relative output directory (`t3-runs/initial`).
`build-recorder.sh` and `run-key-probe.sh` both run Maven from inside the runtime
repository with `-Dmdep.outputFile="$OUT/classpath.txt"`. Maven resolved that
relative path against its module directory, so each script wrote `classpath.txt`
into the runtime repository and then failed to find it at the relative path it
expected. All earlier smoke runs had used absolute paths. This is a defect in
the frozen tooling's handling of relative paths, not in the code under test.

## Side effect, and how it was undone

Two untracked files (classpath lists only) were written into the runtime
repository:

- `Enterprise_AI_Runtime_Service/runtime-api/t3-runs/initial/recorder-build/classpath.txt`
- `Enterprise_AI_Runtime_Service/runtime-cache/t3-runs/initial/b5-keys-probe/classpath.txt`

The harness flagged this (`runtime_repository_unchanged_by_harness: false`).
Neither file is in the T3 inventory, which covers `.java` sources and specific
named files. Both were **moved, not deleted**, into
`stray-files-moved-from-runtime-repo/` in this directory. Afterwards, the runtime
repository was clean, and a fresh inventory capture was byte-identical to
`t3.before.sha256`.

The directory was first committed as `t3-runs/initial` (commit `ea3a372`) and
then renamed to `initial-attempt-1`, so that a later attempt can use a fresh
directory.
