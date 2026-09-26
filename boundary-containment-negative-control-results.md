# Negative-Control Results — Boundary-Containment Measurement

Executed 22 September 2026 against the protocol frozen in
`boundary-containment-negative-control-protocol.md` (SHA-256
`6c6e6483816352135b47b2cf3af40ab4ace538c4e020087e99a9140596342c42`, recorded in
`boundary-containment-negative-control.frozen.sha256`). The protocol was not
modified after execution began. F3 was not re-run and its result is unchanged.

## 1 Outcome

> **The success criterion was met.** With one realization-specific field planted
> in a neighbouring domain's wire contract, the unchanged interface-inventory
> procedure reported a **non-zero cross-boundary footprint**: one changed file
> and one changed surface aggregate, both under AI Runtime.

| | F3 substitution | Negative control |
|:---|---:|---:|
| Cross-boundary footprint | **0 files** | **1 file** |
| Surface affected | none outside Model Services | AI Runtime |
| Instrument | `freeze_interface_inventory.py` | identical, unedited |

## 2 Instrument reproducibility

Before the control, `freeze_interface_inventory.py` was run against the
unmodified tree and compared with `technology-substitution.after.sha256`,
recorded on 5 September 2026. All 116 digest lines were identical (111 per-file digests plus
the five surface aggregates) — the
instrument reproduced the frozen post-substitution state seventeen days later,
on a tree nobody had touched in between. The baseline for this control is
therefore the same tree state F3 finished on.

## 3 Manipulation

One field was added to `GatewayProtocol.InferenceRequest` in

    Enterprise_AI_Runtime_Service/runtime-inference/src/main/java/
      com/enterprise/ai/runtime/inference/gateway/GatewayProtocol.java

The file sits in the **AI Runtime** surface, a neighbouring domain, and its own
documentation states the invariant violated: the request "names a model profile,
and there is no field for a provider, a model, an endpoint or a credential. That
absence is the whole architecture." The planted field named the Ollama
realization in the consuming domain's contract.

Exactly one file was touched. No other file was modified.

## 4 Measurement

    35c35
    < a7b58110d910d0c7…  …/inference/gateway/GatewayProtocol.java
    > 2315b2f7ce61ca6e…  …/inference/gateway/GatewayProtocol.java
    37c37
    < 1a32b91abbeb6808…  AGGREGATE [AI Runtime]
    > e5e0b325e92759bf…  AGGREGATE [AI Runtime]

Two entries changed: the planted file and the AI Runtime aggregate that covers
it. The four other surfaces, Model Services' outward contract included, were
byte-identical. The detection is localised to the surface that was violated.

## 5 Revert

The manipulation was reverted and the inventory re-captured. All 116 digest
lines matched the baseline, and the file contains no residue of the planted
field. The prototype tree is in the state F3 left it.

## 6 What this establishes, and what it does not

**Establishes.** The procedure that reported zero cross-boundary change for the
F3 substitution is not a procedure that reports zero unconditionally. Presented
with a known violation of the same boundary, it reported the violation, on the
correct surface. F3's zero is therefore a measurement rather than an artifact of
an insensitive instrument.

**Does not establish.** Nothing about whether the capability decomposition is
correct, and nothing further about the substitution itself. The limitation
recorded for F3 stands unchanged: the reference implementations were written by
the same researcher who defined the boundaries, so a favourable containment
result partly reflects how the instantiation was written. This control narrows
that objection to the instrument; it does not answer it for the architecture.

The control is also trivially easy to pass. A planted change inside a hashed
file will be detected by any hashing procedure. Its value is not that detection
was in doubt, but that the claim "the measurement discriminates" is now recorded
as an executed test under a pre-fixed criterion rather than assumed.
