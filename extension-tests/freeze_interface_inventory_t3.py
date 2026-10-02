#!/usr/bin/env python3
"""Capture the interface inventory for T3 (response cache, Caffeine -> Redis).

A new script, written for T3. freeze_interface_inventory.py is not edited: its
digest is part of the F3 record.

Each surface carries a class, fixed before T3 is run:

  protected           any added, removed or modified file is a T3 failure
  protected-existing  modifying or removing an existing file is a failure;
                      added files (new tests) are permitted and recorded
  permitted           changes are allowed and reported as the footprint

Run once before and once after the first Redis run:

  python3 freeze_interface_inventory_t3.py before > t3.before.sha256
  python3 freeze_interface_inventory_t3.py after  > t3.after.sha256
  python3 freeze_interface_inventory_t3.py compare t3.before.sha256 t3.after.sha256

PROTOTYPES points at the tree holding the prototype repositories; override it
with the PROTOTYPES environment variable if they live elsewhere.
"""
import hashlib
import os
import re
import sys
from pathlib import Path

PROTOTYPES = Path(os.environ.get("PROTOTYPES", Path.home() / "Desktop" / "AI Projects"))
RT = "Enterprise_AI_Runtime_Service"

#: (surface, class, paths). A path is a file or a directory; directories
#: contribute their .java sources, excluding build output.
SURFACES = [
    ("AI Runtime: ResponseCache SPI", "protected", [
        f"{RT}/runtime-common/src/main/java/com/enterprise/ai/runtime/common/spi/ResponseCache.java",
    ]),
    ("AI Runtime: shared model types (ChatOutcome and contents, Message, Role)", "protected", [
        f"{RT}/runtime-common/src/main/java/com/enterprise/ai/runtime/common/model",
    ]),
    ("AI Runtime: outward contract and serialization configuration", "protected", [
        f"{RT}/runtime-api/src/main/java",
    ]),
    ("AI Runtime: runtime configuration", "protected", [
        f"{RT}/runtime-api/src/main/resources/application.yml",
    ]),
    ("AI Runtime: gateway client (as F3)", "protected", [
        f"{RT}/runtime-inference/src/main/java/com/enterprise/ai/runtime/inference/gateway",
    ]),
    ("Build: shared dependency declarations", "protected", [
        f"{RT}/pom.xml",
        f"{RT}/runtime-common/pom.xml",
        f"{RT}/runtime-api/pom.xml",
    ]),
    ("AI Runtime: existing cache tests", "protected-existing", [
        f"{RT}/runtime-cache/src/test/java",
    ]),
    # The four neighbouring surfaces, exactly as F3 defined them.
    ("Neighbour: Developer Experience", "protected", [
        "Enterprise_AI_SDK/sdk-core/src/main/java/com/enterprise/ai/api",
    ]),
    ("Neighbour: Governance and Security", "protected", [
        "Enterprise_AI_Guardrail_Service/guardrail-common/src/main/java",
    ]),
    ("Neighbour: Evaluation", "protected", [
        f"{RT}/runtime-evaluation/src/main/java",
    ]),
    ("Neighbour: Model Services outward contract", "protected", [
        "Model_Gateway/gateway-api/src/main/java",
        "Model_Gateway/gateway-common/src/main/java/com/enterprise/gateway/common/model",
        "Model_Gateway/gateway-capabilities/src/main/java",
    ]),
    # Inside the cache component: changes are expected, and reported.
    ("Permitted: cache realizations, key factory, cache wiring", "permitted", [
        f"{RT}/runtime-cache/src/main/java",
        f"{RT}/runtime-cache/pom.xml",
    ]),
    ("Permitted: local Redis service definition", "permitted", [
        f"{RT}/docker-compose.yml",
    ]),
]

LINE = re.compile(r"^([0-9a-f]{64})  (.+)$")
HEAD = re.compile(r"^## (.+?)  \[(protected|protected-existing|permitted)\]")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def files_under(rel):
    root = PROTOTYPES / rel
    if root.is_file():
        return [root]
    if not root.is_dir():
        return None
    return sorted(p for p in root.rglob("*.java")
                  if "target" not in p.parts)


def capture(label):
    print(f"# T3 interface inventory — {label}")
    print(f"# Prototypes root: {PROTOTYPES}")
    missing = []
    for surface, cls, paths in SURFACES:
        entries = []
        for rel in paths:
            found = files_under(rel)
            if found is None:
                missing.append(rel)
                continue
            entries += [(digest(f), f.relative_to(PROTOTYPES)) for f in found]
        agg = hashlib.sha256("".join(f"{d}  {p}\n" for d, p in entries).encode()).hexdigest()
        print(f"\n## {surface}  [{cls}]  ({len(entries)} files)")
        print(f"# aggregate {agg}")
        for d, p in entries:
            print(f"{d}  {p}")
    if missing:
        print("\n# MISSING — inventory is incomplete:", file=sys.stderr)
        for rel in missing:
            print(f"#   {rel}", file=sys.stderr)
        sys.exit(1)


def parse(path):
    surfaces, current = {}, None
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        h = HEAD.match(line)
        if h:
            current = h.group(1)
            surfaces[current] = {"class": h.group(2), "files": {}}
            continue
        m = LINE.match(line)
        if m and current:
            surfaces[current]["files"][m.group(2)] = m.group(1)
    return surfaces


def compare(before_path, after_path):
    before, after = parse(before_path), parse(after_path)
    # The comparison is only valid if both inventories cover exactly the surfaces
    # this script defines, each with its defined class. A missing, extra or
    # reclassified surface invalidates the comparison rather than passing it.
    expected = {surface: cls for surface, cls, _ in SURFACES}
    problems = []
    for label, inv in (("before", before), ("after", after)):
        for surface in sorted(set(expected) - set(inv)):
            problems.append(f"{label}: missing surface {surface!r}")
        for surface in sorted(set(inv) - set(expected)):
            problems.append(f"{label}: unexpected surface {surface!r}")
        for surface in sorted(set(expected) & set(inv)):
            if inv[surface]["class"] != expected[surface]:
                problems.append(f"{label}: surface {surface!r} classed "
                                f"{inv[surface]['class']!r}, expected {expected[surface]!r}")
    if problems:
        print("INVALID COMPARISON — inventories do not match the defined surfaces:")
        for p in problems:
            print(f"  {p}")
        print("\nT3 containment: NOT ASSESSED (invalid inventory)")
        sys.exit(2)
    failed = False
    for surface, b in before.items():
        a = after[surface]
        bf, af = b["files"], a["files"]
        added = sorted(set(af) - set(bf))
        removed = sorted(set(bf) - set(af))
        changed = sorted(p for p in set(bf) & set(af) if bf[p] != af[p])
        cls = b["class"]
        if cls == "protected":
            violation = added or removed or changed
        elif cls == "protected-existing":
            violation = removed or changed
        else:
            violation = []
        status = "FAIL" if violation else ("changed" if (added or removed or changed) else "unchanged")
        failed = failed or bool(violation)
        print(f"{status:9}  [{cls}]  {surface}")
        for tag, items in (("added", added), ("removed", removed), ("modified", changed)):
            for p in items:
                print(f"           {tag}: {p}")
    print("\nT3 containment:", "FAILED" if failed else "no protected surface changed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "compare" and len(sys.argv) == 4:
        compare(sys.argv[2], sys.argv[3])
    else:
        capture(sys.argv[1] if len(sys.argv) > 1 else "unlabelled")
