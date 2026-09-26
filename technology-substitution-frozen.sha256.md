# Technology substitution — frozen digests

Recorded 2026-09-05 09:41 UTC. The protocol, the interface inventory it measures
against, and the script that produced that inventory were fixed before
realization B was stood up and before any file was substituted.

```
eaf260db41121e9666ca6d749d43002b888d1a4ec32c2f2a309b4bc55a372c11  technology-substitution-protocol.md
3d13c250421186f297abe882fb1694f7ac5e83616b3b2c529b4cbf463207b11d  technology-substitution.before.sha256
5755805c40d126fbc756aeff78e99eac6759a2134e7c485d7ec6c04665e07e4b  freeze_interface_inventory.py
```

`technology-substitution-results.md` did not exist at this timestamp; it was
written only after step 6 of the protocol's procedure.

**What these digests establish, and what they do not.** A SHA-256 digest
establishes *integrity*: it identifies exactly which bytes were used and lets you
confirm the files shipped here are those bytes. It does **not** establish
*chronology* — no digest can prove when it was computed. The ordering claim rests
on the recorded timestamp above and on the absence of the results file at that
point. A reader who declines to take the timestamp on trust should read F3 as a
result reported against a criterion fixed in advance by the author, not as
externally pre-registered work; Section X-C of the paper states this limitation.

## What you can verify in this copy

The inventory script and the before-inventory are shipped unmodified and
reproduce their recorded digests exactly:

```
shasum -a 256 freeze_interface_inventory.py technology-substitution.before.sha256
```

Excluding their two header lines, the before- and after-inventories digest to
the same value, `8d6915e8f18a95c38f397ba796312b6dace5df292c1c947b3cee5d8225435e7e`:

```
tail -n +3 technology-substitution.before.sha256 | shasum -a 256
tail -n +3 technology-substitution.after.sha256  | shasum -a 256
```

**That equality is the F3 result**: not one of the 111 inventoried interface
files changed across the substitution. It can be confirmed from this package
alone, without the prototype repositories.

## Amendment after freezing — one paragraph, no methodological content

On 2026-09-12, after the substitution, the protocol's closing paragraph was
amended to remove a forward-looking sentence that had become false: it said that
whether the prototype repositories would be published was still open. They are
not included, and the paragraph now says so plainly. This is recorded rather
than done quietly, because amending a frozen document is exactly the kind of
change a digest exists to expose.

The amendment breaks the whole-file protocol digest above, which refers to the
protocol as frozen on 2026-09-05:

```
eaf260db41121e9666ca6d749d43002b888d1a4ec32c2f2a309b4bc55a372c11  as frozen 2026-09-05
5f25c908087cd8492fcd9fbd9a1373a2219f48e9a615a727ceb6f3cdd591326a  as amended (the copy shipped here)
```

The amended paragraph is the last in the file. Everything that defines the
experiment — the realizations, the interface surfaces held fixed, the failure
criterion, the permitted within-domain change, the discrimination case, the
reporting rules and the threats stated in advance — is lines 1-233, which the
amendment did not touch:

```
head -233 technology-substitution-protocol.md | shasum -a 256
fd14b9a02543f7d70383f1dcdabec4623c76b180b0344053934d74ddd1c1be7c
```
