# Falsification Assessment

This register records how the three falsification conditions stated in Section
10 of the paper were assessed, what evidence each assessment rests on, and where
that evidence lives. The paper states the outcomes; this file states the working
so that a reader can disagree with it.

## 1 The conditions

| ID | Condition | Would be shown by |
|:---|:---|:---|
| **F1 — Completeness failure** | Independently developed platforms repeatedly require a responsibility that cannot be placed in any of the ten domains without redefining that domain. | A documented first-party capability with no architectural home, recurring across platforms. |
| **F2 — Boundary failure** | Independent architectures repeatedly divide responsibilities in ways that contradict the proposed boundaries for architectural reasons rather than commercial packaging. | Repeated placement of the same responsibility on the other side of a proposed boundary, for stated architectural reasons. |
| **F3 — Technology-independence failure** | Substituting a materially different realization of one capability requires changes outside its own domain. | A substitution that propagates an interface change into another domain. |

**These conditions were formulated after the evaluation was carried out, not
pre-registered.** They discipline how the results are reported; they did not
constrain how the study was designed. This is stated in §11.2 of the paper and
is repeated here because it bounds what the assessment below can claim.

## 2 F1 — Completeness

**Assessed against:** the 40-cell commercial-platform comparison
(`commercial-platform-evidence-matrix.md`).

**Method.** Each documented first-party capability encountered while rating the
four platforms was placed against the ten domain definitions in Table 1. A
completeness failure would be recorded where a capability had to be assigned by
widening a domain definition, or where it had no home at all.

**Result: no failure.** All forty cells were rated without redefining a domain,
and no platform documented a responsibility that could not be placed. Every
platform reached at least partial coverage in all ten domains; thirty-six of
the forty ratings are substantial and four partial, after the 24 September 2026
re-rating recorded in `commercial-platform-evidence-matrix.md` (originally
thirty-one and nine).

**How to challenge this.** The result is weak in one direction that a reader
should know about: the assessment ran *from* vendor documentation *to* the
domains, so it tests whether the domains can absorb what vendors document. It
does not test the converse — whether the domains demand responsibilities that no
platform provides. Platform Management is the domain where that converse
question bites hardest, and the matrix records it as the weakest-covered domain
in the earlier baseline. After re-rating all four platforms reach ● on it, so
the converse question now has to be asked of the responsibilities the vendors
document least — tenancy above all — rather than of the rating. A reader who believes a domain is an invention rather
than a requirement should attack it there.

## 3 F2 — Boundaries

Assessed twice, against independent bodies of evidence.

### 3.1 Against the four commercial platforms

**Result: no repeated contradiction, with one recorded exception.**

The packaging differences observed in §X-A — agent orchestration offered by one
vendor both as a first-party managed loop and through third-party frameworks on
the same runtime, and by another through its own development kit; platform
management appearing as a fleet control plane in two platforms and as registry,
versioning and quota APIs in the others — follow each vendor's commercial
surface. They place the same responsibilities differently without arguing that
the proposed boundary is wrong.

An earlier version of this example said one vendor delegated agent reasoning to
third-party frameworks. The 24 September 2026 re-check found AWS's AgentCore
Harness (a first-party managed agent loop, GA June 2026) and episodic-memory
reflection (December 2025) documented before the snapshot, so that example was
withdrawn. The F2 result does not change. Harness does bundle orchestration with
tool execution and memory, but AWS also offers the runtime on its own, hosting
any framework — the vendor itself keeps the runtime separable from the agent
loop. That is a packaging choice on one side of the proposed boundary, not a
placement that contradicts it.

**The exception: cost placement.** This architecture assigns cost monitoring to
Operations and cost-aware routing to Model Services, with cost flowing back to
routing as one of the three feedback relationships in Section 7 (R10). Vendor
packaging does not agree on this: one platform treats cost as an input to
routing decisions, another as an observability concern reported after the fact.

Two things must be said about this finding, both of which weaken it:

1. **It is not isolated to one rated cell.** No single cell in the 40-cell
   register turns on cost placement, so this observation is a reading across the
   platform documentation rather than a rating that can be checked line by line.
   A reader who rejects the reading loses the finding.
2. **It is corroborated internally rather than externally.** The independent
   support for it is not another vendor — it is finding **B3** in
   `requirements-traceability.md`, which records that Model Services carries
   "cost optimization" while Operations carries "cost monitoring" and that R10
   maps to both domains. That is a boundary the architecture itself does not
   draw cleanly. The vendor observation and the internal finding agree, and the
   paper flags the dual ownership rather than concealing it.

The honest characterization is therefore: a single architectural disagreement,
observed rather than measured, and matching a boundary weakness the architecture
already admits. It is not a repeated contradiction, which is what F2 requires,
but it is the closest the evidence comes to one.

### 3.2 Against the six documentary sources

**Result: no repeated contradiction, with one substantive divergence.**

Where the two capability sources address the proposed domains they align with
them; the per-proposition evidence is in `documentary-triangulation.md` §5.1.

**The divergence: IBM's organizing basis.** The IBM Generative AI Capability
Model groups assurance by the *asset being protected* — AI Application Security
Management, AI Model Security Management, AI Data Security Management — where
this architecture groups it by *concern*: Governance, Security, Evaluation. IBM
also has no separate evaluation domain; evaluation sits inside GenAI Governance
as Model Monitoring.

This is a genuine alternative decomposition of the same responsibilities, not a
packaging difference, and it is the strongest single piece of evidence against
the proposed grouping. It does not satisfy F2 because it is one source rather
than a repeated pattern: EAIOF groups cross-cutting capabilities by concern in a
way that matches this architecture closely, and the governance sources do not
decompose a platform at all. A reader who weighted IBM more heavily than EAIOF
would reach a different conclusion here, and the ratings in
`documentary-triangulation.md` §5 make that re-weighting possible.

## 4 F3 — Technology independence

**Assessed against:** one substitution in a self-built instantiation, under a
criterion frozen beforehand (`technology-substitution-protocol.md`, results in
`technology-substitution-results.md`).

**Method.** The Model Services realization was replaced — `provider-openai`,
hosted commercial, `openai-chat-completions` wire, API-key auth →
`provider-ollama`, self-hosted, `ollama-chat` wire, no credential. Before the
substitution, the interface of each of the four neighbouring capability domains,
and Model Services' own outward contract, was inventoried by SHA-256 across 111
files. What would count as a failure, and what would not, was fixed in the same
frozen document.

**Result: no failure.** Zero interface changes outside Model Services: all five
surface aggregates were byte-identical afterwards, no file in the four
neighbouring repositories was modified, and their suites still passed (94 and
596 tests; the guardrail repository has none). The within-domain footprint was
one configuration file. One capability difference was exposed — embeddings from
a realization declaring none — and was rejected at admission through the
existing `ProviderCapabilities` mechanism and an existing error type, with no
new error crossing a boundary.

**How to challenge this.** Three ways, in order of force. First, this is a
*self-instantiation* test: the prototypes and the architecture share an author,
so the result is partly a statement about how the prototypes were written, and F3
is less independent than F1 and F2, which draw on third-party evidence. However,
F3 is the only condition tested prospectively, against a failure criterion and
interface inventory fixed before the substitution. Second, one
substitution in one domain does not establish a property E2 asserts of ten.
Third, the end-to-end path was verified at the Model Services contract rather
than through the Developer Experience surface as the protocol required; that
deviation, and one other, are recorded in the results.

## 5 Summary

| Condition | Evidence | Outcome |
|:---|:---|:---|
| **F1** Completeness | 40 commercial-platform ratings | Not met — no capability lacked a home |
| **F2** Boundaries, commercial | 40 commercial-platform ratings | Not met — one exception recorded (cost placement) |
| **F2** Boundaries, documentary | 36 documentary ratings | Not met — one divergence recorded (IBM organizing basis) |
| **F3** Technology independence | one frozen-criterion substitution, `provider-openai` → `provider-ollama` | Not met — 0 cross-boundary interface changes, 1 within-domain configuration change |

All three conditions were assessed and none was met. F1 and F2 organize evidence observed retrospectively; F3 was tested prospectively, against a failure criterion and interface inventory fixed before the substitution. The two near-misses on F2 are
recorded above with the evidence that would let a reader turn them into failures
if they weigh that evidence differently. F3's evidence is the least independent
and least generalizable of the three, for the reasons given under it, but it is
the only prospectively specified behavioral test; it should be read as bounded
corroboration from a self-built instantiation rather than as independent validation.

## 6 Reproducing this assessment

1. Take the three conditions in §1 as given.
2. For F1, re-rate the forty cells from
   `commercial-platform-evidence-matrix.md` and record any capability that
   required a domain definition to be widened.
3. For F2, work through the packaging differences in §10.1 of the paper and the
   per-source evidence in `documentary-triangulation.md` §5.1, and judge for
   each whether the difference is commercial or architectural. The cost and IBM
   cases above are where reasonable readers will most likely disagree.
4. For F3, `technology-substitution-protocol.md` fixes the criterion and
   `technology-substitution-results.md` reports what was observed. The frozen
   digests in `technology-substitution-frozen.sha256.md` show the criterion
   preceded the result. Re-running the substitution itself requires the
   prototype repositories, which are not part of this artifact.

Disagreement on the two recorded exceptions is expected and is the point of
recording them. What would change the paper's conclusion is not a single
disagreement but a *repeated* one — the same responsibility placed on the other
side of the same boundary, by several independent architectures, for stated
architectural reasons.
