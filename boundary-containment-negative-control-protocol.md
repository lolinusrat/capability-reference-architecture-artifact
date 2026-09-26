# Negative-Control Protocol — Boundary-Containment Measurement

Frozen before execution. Separate from `technology-substitution-protocol.md`,
which was frozen before the 5 September 2026 F3 experiment and is **not**
modified or extended by this document. F3's result stands as recorded.

## 1 Why

F3 measured a contained substitution and observed a zero cross-boundary
footprint. That establishes the measurement can *confirm* containment. It does
not establish the measurement can *detect* its absence. A procedure that
reported zero unconditionally would have produced the same F3 result.

This control tests one narrow question:

> Does the interface-inventory procedure used in F3 distinguish a contained
> substitution from a known boundary violation?

It provides no additional evidence that the capability decomposition is
correct, and none about F3's substitution, which is not re-run.

## 2 Instrument — unchanged

`freeze_interface_inventory.py`, exactly as used for F3: five surfaces, Java
sources, build output excluded, SHA-256 per file plus one aggregate per surface.
The script is not edited for this control. Verified on 22 September 2026 to
reproduce `technology-substitution.after.sha256` byte-for-byte.

## 3 Manipulation

One realization-specific dependency is introduced deliberately across the
Model Services → AI Runtime boundary, in:

    Enterprise_AI_Runtime_Service/runtime-inference/src/main/java/
      com/enterprise/ai/runtime/inference/gateway/GatewayProtocol.java

This file is inside the **AI Runtime** surface — a neighbouring domain, not the
domain under substitution. Its own documentation states the invariant being
violated: the request "names a model profile, and there is no field for a
provider, a model, an endpoint or a credential. That absence is the whole
architecture."

The manipulation adds a provider-specific field to `InferenceRequest`, naming
the Ollama realization in the consuming domain's wire contract. This is the
leak the architecture exists to prevent.

Exactly one file is touched. No other file is modified. The change is reverted
after measurement and the tree re-verified against the baseline.

## 4 Expected outcome

At least one change detected in a surface outside Model Services —
specifically, one changed file and one changed aggregate under AI Runtime.

## 5 Criteria, fixed before execution

**Success.** The unchanged interface-inventory procedure reports a non-zero
cross-boundary footprint under AI Runtime.

**Failure.** The planted cross-boundary change exists in the tree, and the
procedure continues to report a zero cross-boundary footprint. Failure would
mean F3's zero result is uninformative, and would be reported as such.

## 6 Procedure

1. Capture the baseline inventory.
2. Apply the manipulation of §3.
3. Capture the post-manipulation inventory by the same command.
4. Diff. Record every differing line.
5. Revert the manipulation; re-capture; confirm the tree matches the baseline.

## 7 What a pass does not establish

A pass shows the instrument discriminates. It does not address the limitation
recorded in the F3 results and in the manuscript: the reference implementations
were written by the same researcher who defined the boundaries, so a favourable
containment result partly reflects how the instantiation was written. The
control narrows the objection; it does not remove it.
