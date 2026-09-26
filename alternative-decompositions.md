# Alternative Decompositions

The paper states that the three boundary criteria — independent
substitutability, ownership and assessment — constrain the decomposition rather
than uniquely determining it. This file tests that claim by constructing four
plausible alternatives from the same twelve requirements and applying the same
criteria to each.

The exercise is only worth anything if the alternatives are allowed to win. One
of the four is rejected outright, two are rejected with separation supported
but not compelled, and one is **defensible on
the criteria and rejected on a ground the criteria do not capture**. That last
result is reported here in full because it is the honest answer to "why ten and
not eleven?".

## 1 Method

For each alternative:

1. State the alternative and the domain count it produces.
2. Apply each criterion, using the same evidence available elsewhere in this
   artifact — the 40-cell vendor register, the 36-cell documentary register and
   the boundary findings B1–B4 in `requirements-traceability.md`.
3. Record the verdict per criterion, including where a criterion **does not
   discriminate**, which is as informative as a pass or a fail.
4. State what the result means for the ten-domain model.

No requirement was added, removed or reworded to make an alternative fail. The
requirements in Section 4 of the paper are held fixed throughout.

## 2 Alternative A — merge Governance, Security and Evaluation into one Assurance domain

**Ten domains become eight.** This is the decomposition an architect reaches by
grouping on *when* a capability acts — everything that constrains or checks
execution — rather than on what it is responsible for.

| Criterion | Verdict | Reasoning |
|:---|:---|:---|
| Substitutability | **Fails** | The three are sourced and replaced independently in practice. Identity, secrets and data protection are typically inherited from an existing enterprise security stack; policy, approval and risk classification are realized in a governance or policy-engine product; evaluation is realized in an evaluation framework on its own release cycle. A merged domain imposes one substitution boundary across three independently substitutable capabilities. |
| Ownership | **Fails** | These have different accountable owners in most enterprises the architecture targets: security engineering, risk and compliance, and the platform or ML engineering function respectively. A merged domain would have no single owner, which is the condition the criterion exists to prevent. |
| Assessment | **Fails** | Merging destroys real signal. In the 40-cell register, Security and Evaluation are rated ● for all four platforms while Governance is ◐ for two of them. A single Assurance rating would conceal that the weakness is specific to governance. |

**Verdict: rejected on all three criteria.**

**The honest counterweight.** EAIOF groups exactly these capabilities together,
as cross-cutting "trust, security and governance capabilities" (recorded at S5
in `documentary-triangulation.md`). An independent source therefore makes this
merge. The disagreement is not about the capabilities but about what the
grouping is *for*: EAIOF groups them by a placement property — they apply across
every layer — whereas the criteria used here group by substitution, ownership
and assessment. Both groupings can be right for their own purpose, and the
architecture adopts D3 (assurance spans rather than sits beneath execution) to
capture the cross-cutting property that EAIOF's grouping expresses. A reviewer
who prefers the placement property as the organizing basis would reach eight
domains, and the criteria alone would not stop them.

## 3 Alternative B — merge AI Runtime with Agent Services

**Ten domains become nine.** The runtime executes; agents are a kind of
execution. This is the most frequently proposed merge, and finding B1 in
`requirements-traceability.md` records that this boundary was the most contested
in development.

| Criterion | Verdict | Reasoning |
|:---|:---|:---|
| Substitutability | **Favors separation** | The separation rests first on Table 1: coordination, context, execution state and runtime control enforcement are AI Runtime responsibilities; planning, tool invocation, memory, reflection and multi-agent collaboration are Agent Services responsibilities. The vendor evidence shows several realization patterns over a runtime, not one. Amazon supplies a first-party managed agent loop — AgentCore Harness, which "handles orchestration, tool execution, memory management, and response generation" (GA June 2026) — while its AgentCore services "work together or independently with any open-source framework such as CrewAI, LangGraph, LlamaIndex, and Strands Agents", so one runtime hosts first-party and third-party agent realizations. Google supplies agent reasoning first-party through ADK. An earlier version of this cell said Amazon delegates planning and reflection to third-party frameworks; the 24 September 2026 re-check found Harness and episodic-memory reflection documented before the snapshot, and that claim is withdrawn. |
| Ownership | **Does not discriminate** | In most enterprises at the scale this architecture targets, one AI platform team owns both. The criterion gives no reason to separate them, and none to merge them. This is a genuine null result. |
| Assessment | **Favors separation** | The two are assessed on different evidence. Runtime health is latency, error rate, retry and fallback behaviour; agent quality is trajectory quality, tool-use correctness and the rate at which human approvers override proposals. An organization can be strong at one and weak at the other. |

**Verdict: ambiguous, resolved two-to-nothing with one abstention.** Separation
is supported, but not by all three criteria, and a reader who weights ownership
most heavily would merge them. The architecture separates them, and B1 records
that the boundary was revised — the runtime now owns the execution lifecycle and
invokes agent behaviour rather than implementing it — precisely because the
first attempt at this boundary did not survive the criteria.

## 4 Alternative C — split Platform Management

**Ten domains become eleven:** a technical *Platform Operations* domain
(tenancy, environments, configuration, feature flags, versioning and release)
and a *Platform Product Management* domain (roadmap, catalog curation,
documentation, adoption).

| Criterion | Verdict | Reasoning |
|:---|:---|:---|
| Substitutability | **Favors the split** | Finding B2 records the problem directly: a service catalog product can be swapped; a roadmap cannot. The technical half substitutes cleanly and the product half is not technology at all, so the merged domain substitutes only partially — the defect the manuscript concedes in Section 11.2. |
| Ownership | **Does not discriminate, or mildly favours merging** | Both halves are owned by the same AI platform team in the operating model of Section 8. Splitting creates two domains with one owner, which the criterion neither requires nor forbids. |
| Assessment | **Favors the split** | The halves are assessed against different evidence: documented technical capability for one, adoption and consumer experience for the other. The 40-cell register shows the consequence — Platform Management is the domain where ratings moved most between the unverified baseline and the verified assessment, because the two halves are documented very differently by vendors. |

**Verdict: the alternative is defensible on the criteria, and on two of the three
it is preferable.** The ten-domain model does not adopt it.

**Why not, stated plainly.** The reason is not one the three criteria supply. A
*Platform Product Management* domain would not be a technical capability, and
the capability model is defined throughout as a decomposition of technical
platform responsibilities; introducing a domain that provides no technology
would break the frame the other nine sit in. The architecture instead keeps the
domain whole and accepts the partial substitution defect, which Section 11.2
now states. **This is the clearest evidence in this artifact that the criteria
constrain rather than determine the decomposition:** where they and the frame
disagree, the frame decided, and the paper says so rather than pretending the
criteria settled it.

## 5 Alternative D — absorb Platform Management into Operations

**Ten domains become nine.** Platform Management is the domain most often
questioned — the manuscript notes it is the one most often omitted in practice —
and folding it into Operations is the obvious way to remove it without losing
its responsibilities. This is the opposite move to Alternative C: rather than
splitting the domain, it disappears.

| Criterion | Verdict | Reasoning |
|:---|:---|:---|
| Substitutability | **Favors separation** | The two rest on different, independently replaced toolchains. Observability — tracing, metrics, alerting — is realized in a telemetry stack; tenancy, environments, configuration, feature flags and release management are realized in delivery and platform-engineering tooling. Substituting one imposes no change on the other. |
| Ownership | **Weakly favors separation** | Running the platform and evolving it are different accountabilities — availability and incident response against roadmap, versioning and consumer adoption — but in a small platform team one person may hold both. The criterion discriminates, though not decisively. |
| Assessment | **Does not discriminate on the vendor evidence** | The two are assessed on different measures in principle — availability, latency and incident response for Operations; versioning, release and consumer compatibility for Platform Management. But the 40-cell register no longer separates them: after the 24 September 2026 re-rating (see `commercial-platform-evidence-matrix.md`), all four platforms are ● on both. An earlier version of this file cited the two domains dissociating in opposite directions across three platforms; that dissociation came from Platform Management cells scored against an earlier domain definition and from watsonx Operations evidence drawn from a product page, and it did not survive re-scoring against Table 1. |

**Verdict: rejected, on substitutability.** Separation is supported but not
compelled: one criterion favours it, one weakly favours it, and assessment does
not discriminate on the available evidence. This alternative was previously
presented as the strongest empirical evidence in this file that a boundary earns
its place. After the re-rating it is not — it now stands on the same footing as
Alternative B, and it is reported that way rather than kept on evidence that no
longer holds.

Note the tension with Alternative C, which is deliberate. The evidence says
Platform Management should not be absorbed into Operations *and* that its own
internal boundary is impure. Both findings stand; the domain is correctly
separate from Operations and is still the least clean domain in the model.

## 6 Result

| Candidate | Substitutability | Ownership | Assessment | Outcome |
|:---|:---|:---|:---|:---|
| **Proposed model** (10 domains) | Holds | Holds | Holds, qualified at Platform Management | Retained |
| **A** Merge Governance + Security + Evaluation (8) | Fails | Fails | Fails | Rejected on the criteria; an independent source nonetheless makes this grouping for a different purpose |
| **B** Merge AI Runtime + Agent Services (9) | Favours separation | No discrimination | Favours separation | Separation supported but not compelled |
| **C** Split Platform Management (11) | Favours split | No discrimination | Favours split | **Alternative preferred on the criteria; rejected on frame consistency** |
| **D** Absorb Platform Management into Operations (9) | Favours separation | Weakly favours separation | No discrimination | Separation supported but not compelled |

Three conclusions follow, and only the first is comfortable.

1. **The criteria do real work.** They reject Alternative A decisively, on all
   three criteria and on independent grounds — vendor evidence and enterprise
   ownership structure — rather than by assertion.
2. **They do not settle every boundary.** Ownership fails to discriminate cleanly
   in two of the four alternatives, and assessment fails to discriminate for
   Alternative D, so separation is supported but not compelled for both the
   runtime and agent boundary and the Operations and Platform Management
   boundary.
3. **They are not sufficient on their own.** Alternative C is preferred on the
   criteria and is not adopted. The ten-domain model is therefore the product of
   the criteria *and* a frame decision about what a capability domain is — and
   any claim that the criteria alone produce ten domains would be false.

## 7 Reproducing this analysis

1. Take the three criteria from Section 5 of the paper and the twelve
   requirements from Section 4.
2. Construct the four alternatives in §2–§5 above, or others of your own.
3. Apply each criterion using the evidence in
   `commercial-platform-evidence-matrix.md`,
   `documentary-triangulation.md` and the B1–B4 findings in
   `requirements-traceability.md`.
4. Compare with the result table in §6.

Disagreement is most likely on Alternative A, where an architect who organizes
by cross-cutting placement rather than by substitution will reach eight domains
and be able to cite EAIOF in support. That disagreement is a difference in
organizing principle, not an error in applying the criteria, and the paper does
not claim otherwise.
