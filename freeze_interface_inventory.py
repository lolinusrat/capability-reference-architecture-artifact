#!/usr/bin/env python3
"""Capture the interface inventory for the F3 technology-substitution test.

F3 asks whether substituting a materially different realization of one
capability domain forces an interface change *outside* that domain. Answering it
requires a definition of "the interface" that was fixed before the substitution
was performed, so that the answer cannot be arranged afterwards by choosing a
convenient surface.

This script is that definition, executed. It walks five surfaces — four
neighbouring capability domains plus the outward-facing contract of the domain
being substituted — and records a SHA-256 for every file, plus one aggregate
digest per surface. Run it once before the substitution and once after; the
comparison is the measurement.

  python3 freeze_interface_inventory.py before  > technology-substitution.before.sha256
  python3 freeze_interface_inventory.py after   > technology-substitution.after.sha256
  diff technology-substitution.before.sha256 technology-substitution.after.sha256

Any difference under a neighbouring-domain surface meets F3. Differences under
the Model Services surface are read against §3 of the protocol: the outward
contract must not change, but the realization behind it is expected to.

The prototype repositories are not part of this artifact. PROTOTYPES points at
the tree that holds them; override it with the PROTOTYPES environment variable
if they live elsewhere. The recorded digests let a reader confirm that the two
runs saw the same files, even without the repositories themselves.
"""
import hashlib
import os
import sys
from pathlib import Path

PROTOTYPES = Path(os.environ.get(
    "PROTOTYPES", Path.home() / "Desktop" / "AI Projects"))

#: The five surfaces, fixed before the substitution. Each entry is a capability
#: domain and the paths that constitute its interface — the types a consumer in
#: another domain can name. Implementation packages are deliberately excluded:
#: the question is whether the *contract* moved, not whether code did.
SURFACES = {
    "Developer Experience": [
        "Enterprise_AI_SDK/sdk-core/src/main/java/com/enterprise/ai/api",
    ],
    "AI Runtime": [
        "Enterprise_AI_Runtime_Service/runtime-api/src/main/java",
        "Enterprise_AI_Runtime_Service/runtime-inference/src/main/java/"
        "com/enterprise/ai/runtime/inference/gateway",
    ],
    "Governance and Security": [
        "Enterprise_AI_Guardrail_Service/guardrail-common/src/main/java",
    ],
    "Evaluation": [
        "Enterprise_AI_Runtime_Service/runtime-evaluation/src/main/java",
    ],
    # The domain under substitution. Its outward contract is inventoried for the
    # opposite reason to the others: it is the surface that must hold while the
    # realization behind it is replaced.
    "Model Services (outward contract)": [
        "Model_Gateway/gateway-api/src/main/java",
        "Model_Gateway/gateway-common/src/main/java/com/enterprise/gateway/common/model",
        "Model_Gateway/gateway-capabilities/src/main/java",
    ],
}


def digest(path):
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def walk(root):
    """Java sources under root, excluding build output, in a stable order."""
    return sorted(p for p in root.rglob("*.java")
                  if "target" not in p.parts and "/test/" not in str(p))


def main():
    label = sys.argv[1] if len(sys.argv) > 1 else "unlabelled"
    print(f"# Interface inventory — {label}")
    print(f"# Prototypes root: {PROTOTYPES}")
    missing = []
    for surface, paths in SURFACES.items():
        files = []
        for rel in paths:
            root = PROTOTYPES / rel
            if not root.is_dir():
                missing.append(rel)
                continue
            files.extend(walk(root))
        print(f"\n## {surface}  ({len(files)} files)")
        roll = hashlib.sha256()
        for f in files:
            d = digest(f)
            roll.update(d.encode())
            print(f"{d}  {f.relative_to(PROTOTYPES)}")
        print(f"{roll.hexdigest()}  AGGREGATE [{surface}]")
    if missing:
        # Loud, because a silently absent surface would read as "no change".
        print("\n# MISSING SURFACES — inventory is incomplete:", file=sys.stderr)
        for m in missing:
            print(f"#   {m}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
