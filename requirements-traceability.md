# Requirements Traceability

Supplementary artifact for *A Capability-Based Reference Architecture for Enterprise AI Platforms*.

This document records the derivation chain behind contribution **C1**:

> source evidence → recurring concern → requirement (R1–R12) → capability domain → evaluation criterion

The paper carries a condensed form; this is the full version.

## Status of each column

Not every column is established to the same standard. This is stated explicitly
so the matrix is not read as claiming more than it supports.

| Column | Status |
|:---|:---|
| Requirement | **Established** — Section IV of the manuscript, unchanged |
| Architectural concern | **Established** — restatement of the requirement's own wording |
| Literature evidence | **Established where cited**, and gaps are marked; see [Gap register](#gap-register) |
| Practitioner grounding | **CONFIRMED.** The requirements were informed by the author's prior professional experience designing and implementing enterprise AI platform architecture in an industry setting. |
| Practitioner corpus (this repository) | **CANDIDATE — chronology not established.** See [Provenance](#provenance-of-the-practitioner-corpus) |
| Capability domain | **Established** — Table 1 of the manuscript |
| Evaluation criterion | **Established where the manuscript states the link**, otherwise marked *(inferred)* |

**Practitioner grounding is confirmed; the corpus chronology is not.** The
requirements were informed by the author's prior professional experience
designing and implementing enterprise AI platform architecture in an industry
setting. That professional experience is **distinct from** the reference
implementations and repository artifacts used in this study, and the repository
corpus should not be read as establishing its chronology or provenance.

The practitioner column below therefore remains **candidate**. It lists corpus
material that exists and is on point, but it does not assert that this
particular material drove the requirements; the confirmed grounding is the
professional experience, not these files. The manuscript cites no requirement to
the corpus.

## Matrix

Reference numbers are those of the paper's bibliography. Corpus documents are cited
as `Dnn §s` (see [Corpus inventory](#corpus-inventory)); implementations by
module.

| Req. | Architectural concern | Literature evidence | Practitioner evidence (candidate) | Capability domain | Criterion |
|:---|:---|:---|:---|:---|:---|
| **R1** Multi-model support | Provider coupling; model and provider selection and substitution behind a stable provider-neutral interface, managed, self-hosted or combined | [36] Lu et al. | D02 §5; ADR-002 *Technology-Neutral Architecture*; ADR-003 *Enterprise Model Gateway*; `Model_Gateway` | Model Services | E2 **stated** |
| **R2** Enterprise knowledge access | Governed access, ingestion, indexing, refresh and retrieval over heterogeneous enterprise knowledge | [14] Edge et al.; [24] Hogan et al.; [33] Lewis et al. | D03 §3, §13, §15; ADR-004 *Retrieval as a Shared Platform Capability*; `Project_Synapse` (vector RAG vs GraphRAG, orig. "Nexus") | Knowledge Services | E1, E5 *(inferred)* |
| **R3** Agent execution | Agentic execution within enforced limits; autonomous, semi-autonomous or combined modes | [34] Liu et al.; [57] Wooldridge; [58] Yao et al. | D04 §5–14 (patterns 1–10); D02 §7; `Adaptive_Multi-Agent_Code_Review_System` | AI Runtime; Agent Services | E1, E6 *(inferred)* |
| **R4** Human accountability | Human oversight and decision authority | [16] EU AI Act; [46] NIST AI RMF | D01 P8 *Human Accountability*; D04 §10 *Human-in-the-Loop*; ADR-008 *Human Approval for High-Risk Actions*; `control-approval` | AI Runtime *(principal)*; Governance *(contributing)* | E5 *(inferred)* |
| **R5** Policy enforcement on the execution path | Runtime enforcement rather than periodic assessment | [46] NIST AI RMF; [47] NIST GenAI Profile — establish the governance need; **request-path enforcement is this paper's architectural response, not a NIST prescription** | D06 §10 *Policy Enforcement*; D09 *PDP*/*PEP*; D01 P2 *Governance by Design*; ADR-007; `guardrail-policy`, `guardrail-orchestrator/DecisionAggregator` | Governance | E5 **stated** |
| **R6** Security across AI-specific attack surfaces | Direct and indirect prompt injection, sensitive-data exposure and leakage, model abuse, tool misuse | [47] NIST GenAI Profile; [56] Vassilev et al. | D06 (security domains); D01 P5 *Security by Default*; `guardrail-input`, `guardrail-security`, `control-security` | Security | E6 *(inferred)* |
| **R7** Continuous evaluation | AI quality as a lifecycle concern, not a release gate | [2] Amershi et al.; [47] NIST GenAI Profile | D05 (whole); D01 P7 *Evaluation as a Platform Capability*; ADR-005; `Tethera_Eval` | Evaluation | E1 **stated** |
| **R8** AI-specific observability | Telemetry that conventional infrastructure metrics cannot supply | [47] NIST GenAI Profile; [48] OpenTelemetry GenAI — five of seven listed fields map to documented attributes; *policy decisions* has no OpenTelemetry equivalent | D01 P6 *Observability by Default*; D04 §17 *Agent Observability*; ADR-006; `control-observability`, `guardrail-observability` | Operations | E7 **stated** |
| **R9** Developer experience and platform consumption | Reusable self-service consumption of shared capabilities | [18] Forsgren et al.; [55] Skelton & Pais | D02 §3; D01 P9 *Developer Experience*; `Enterprise_AI_SDK` | Developer Experience | E8 *(inferred — name match only)* |
| **R10** Cost transparency and control | Consumption economics as an architectural input | [13] Dekoninck et al. — carries the cost–performance premise only; **request/tenant/application accounting and quotas are the paper's synthesis** | D05 §13 *Cost Evaluation*; D09 *Cost Attribution*, *Step Budget*; `gateway-rate-limit`; `self-hosted-llm-benchmark`; `Project_Synapse` (quantization) | Model Services; Operations | E2, E7 *(inferred)* |
| **R11** Platform lifecycle | Repeatable deployment, configuration and versioning; independent evolution of platform and consumers | [10] CNCF; [53] Sculley et al. — CNCF carries the platform-lifecycle claim; Sculley supports the coupling concern | D08 (maturity model); D01 P10 *Continuous Evolution*; D02 §12 | Platform Management | E3 **stated** |
| **R12** Auditability and traceability | Provenance sufficient to reconstruct AI-assisted execution | [16] EU AI Act; [46] NIST AI RMF; [47] NIST GenAI Profile | D06 (audit); D01 P2; `control-audit`, `guardrail-evidence` | Governance *(principal)*; Operations *(contributing)* | E5 **stated** |

**stated** = the manuscript explicitly says the domain discharges that
requirement, or the criterion names it. *(inferred)* = consistent with the text
but not asserted in it. E1 (requirements coverage and internal consistency) applies to every
requirement by construction, so it is listed only where it is the primary
criterion.

## Gap register

All six gaps recorded in the first version of this document are now closed, and
every requirement carries literature evidence that supports the claim attached
to it. No reference in the bibliography is uncited.

Closed by the targeted source review:

| Req. | Was | Now |
|:---|:---|:---|
| **R5** | no citation | [46] NIST AI RMF and [47] NIST GenAI Profile establish the governance need; request-path enforcement is stated in the paper as its own architectural response, not attributed to NIST |
| **R6** | zero trust only, not AI-specific | [47] NIST GenAI Profile and [56] Vassilev et al. cover prompt injection, data leakage and model abuse directly |
| **R7** | Amershi alone, thin | [2] Amershi et al. and [47] NIST GenAI Profile — the GenAI Profile calls for regular safety evaluation and post-deployment monitoring |
| **R8** | no citation | [47] NIST GenAI Profile and [48] OpenTelemetry GenAI — five of the seven listed telemetry fields map to documented OpenTelemetry attributes; *policy decisions* has no equivalent and rests on NIST |
| **R10** | no citation | [13] Dekoninck et al. carries the cost–performance premise; the enterprise accounting and quota obligations are separated out in the manuscript as the paper's synthesis |
| **R11** | Sculley alone, not about platform versioning | [10] CNCF added alongside [53] Sculley et al.; CNCF carries the platform-lifecycle claim |

Two further defects found during the claim-to-citation audit and fixed:

- **Sculley misattributed in §2.3.** Compression had merged two citations so that
  Sculley appeared to supply MLOps practices rather than the technical-debt
  motivation. Re-separated.
- **[52] NIST SP 800-207 orphaned.** Zero Trust lost its only citation when §5
  was compressed. Restored to the Security domain paragraph, supporting
  per-request access decisions rather than perimeter inheritance — a closer fit
  than its previous placement.

Also revised: **R1** no longer calls direct provider integration "the most
consequential enterprise AI anti-pattern" — a superlative [36] Lu et al. does not
establish. It now claims provider coupling and reduced substitutability, which
it does.

### Sources added

All four were verified independently — DOI resolution against Crossref/DataCite,
or retrieval of the publisher's own record — rather than taken from a search
result.

| # | Source | Verified | Supports |
|:---|:---|:---|:---|
| [13] | Dekoninck, J., Baader, M., Vechev, M.: A unified approach to routing and cascading for LLMs. ICML 2025, PMLR 267:12987–13010 | PMLR record; abstract confirms cost–performance framing. No DOI — PMLR mints none | R10 |
| [47] | NIST: AI RMF: Generative Artificial Intelligence Profile. NIST AI 600-1 (2024) | doi:10.6028/NIST.AI.600-1 | R5, R6, R7, R8 |
| [48] | OpenTelemetry: GenAI semantic conventions | Canonical repository. **Note:** these conventions moved out of the main semconv docs; the older `opentelemetry.io/docs/specs/semconv/gen-ai/` URL now serves only a "Moved" notice, so the repository URL is cited instead | R8 |
| [56] | Vassilev, A., et al.: Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations. NIST AI 100-2 E2025 (2025) | doi:10.6028/NIST.AI.100-2e2025. Note this is the 2025 edition; a 2023 edition exists under a different DOI | R6 |

## Derivation decisions: normalization, consolidation and separation

**Status: reconstructed rationale.** This section was written for the artifact
after R1–R12 were fixed. It records the decisions the derivation embodies and the
test applied to them. It is **not** a contemporaneous log, and no claim is made
that these tables were consulted while the requirements were being written. Their
purpose is to make the derivation auditable and contestable: a reader can apply
the stated test to the same concerns and see where they would have decided
differently.

**The test.** Two concerns become **one** requirement where they impose the same
architectural responsibility on the same boundary. They remain **separate** where
a single statement would force one domain to own responsibilities that are
substituted, owned or assessed separately — the same three criteria the
manuscript applies to capability boundaries in Section V, applied one level
earlier.

### 1 Normalization — product-specific mechanism to implementation-independent statement

| Mechanism as it appears in practice and vendor material | Implementation-independent statement | R |
|:---|:---|:---|
| Provider SDK called directly from application code | Access to multiple models through a stable provider-neutral interface | R1 |
| Model gateway or router product | Provider-neutral access with routing and fallback behind one interface | R1 |
| Vector database | Retrieval over unstructured enterprise knowledge | R2 |
| Graph store or knowledge-graph product | Retrieval over relationships between enterprise records | R2 |
| Retrieval-augmented generation pipeline | Ingestion, indexing, refresh and retrieval as a shared capability | R2 |
| Agent framework | Agentic execution within enforced limits | R3 |
| Tool or function-calling API | Tool invocation within declared permissions | R3 |
| Approval step built into an application's own interface | Human approval as a participant in the workflow | R4 |
| Guardrail product | Input and output controls enforced during execution | R5 |
| Policy engine | Policy decisions taken on the execution path | R5 |
| Prompt-injection filter | Coverage of AI-specific attack surfaces | R6 |
| Per-application evaluation script | Evaluation as a reusable service | R7 |
| Tracing SDK | Capture of AI-specific execution context | R8 |
| Internal developer portal | Consistent interfaces and programming models for consumers | R9 |
| Token counter or usage dashboard | Consumption accounting at request, tenant and application scope | R10 |
| Prompt registry | Versioned platform configuration under a platform lifecycle | R11 |

### 2 Consolidation — several recurring concerns into one requirement

| R | Concerns consolidated | Why one requirement |
|:---|:---|:---|
| R2 | Unstructured retrieval; structured-record retrieval; relationship retrieval; ingestion; indexing; refresh; metadata filtering; source attribution | All impose one responsibility — governed retrieval behind a single consumption boundary — and they are substituted together when the retrieval realization changes |
| R3 | Planning; tool invocation; memory; reflection; multi-agent collaboration | All are capabilities of bounded autonomous execution, exercised through one execution boundary and limited by one permission model |
| R5 | Authentication; workload and user identity; authorization; tenant isolation; model and tool approval; usage policy; input and output controls | All state the same architectural property: enforceability **during** execution rather than assessment after it. The controls differ; the responsibility does not |
| R7 | Offline evaluation; online evaluation; correctness; groundedness; safety; cost; business outcomes | One reusable assessment capability. The measures vary by workload; the responsibility to provide assessment as a service does not |
| R8 | Model selection; consumption metrics; tool execution; policy decisions; evaluation signals; prompts and retrieved evidence | One capture responsibility over AI-specific execution context, discharged by one domain and consumed by several |
| R11 | Deployment; configuration; versioning; release; capability evolution | One lifecycle responsibility over platform capabilities, all of which change together when the platform is released |

### 3 Separation — concerns kept apart, and why not merged

This table answers the reviewer's question directly: each row is a merge that was
available and not taken.

| Pair | Why a single requirement would conflate them |
|:---|:---|
| R1 / R10 | Multi-model access is a **substitution** property; cost is an **accounting and decision** property, discharged jointly by Model Services and Operations. A merged statement would bind cost accounting to the provider interface and lose the platform-level scope |
| R3 / R4 | Human approval applies to non-agentic workloads as well. Folding it into agent execution would place approval inside Agent Services rather than on the request path, which is where Section VII puts it |
| R5 / R6 | R5 states **where** controls act; R6 states **which surfaces** must be covered. They are discharged by different domains with different accountable owners, and the commercial evidence rates them differently |
| R7 / R8 | Observability **captures**; evaluation **assesses**. Operations supplies the signals Evaluation consumes. A merged requirement would make assessment a property of telemetry |
| R8 / R12 | Observability serves operators; auditability serves reconstruction, subject to security, privacy and retention constraints that R12 states and R8 does not |
| R9 / R11 | R9 is how applications **reach** capabilities; R11 is how capabilities **change** without forcing coordinated consumer change. Consumption and sustainment are separate concerns in the arrangement of Section VI |

### 4 Why twelve

Twelve is the number of statements that survive both operations. Consolidation
removes concerns imposing the same responsibility on the same boundary;
separation retains those a single statement would conflate. The count is a
**consequence** of applying the test, not a target set in advance, and a
different corpus of concerns could yield a different count. What the analysis
fixes is not the number but the test, so that a reader who disagrees can point to
the row where the decision went the other way.

## Capability-boundary validation

Section III states the principle governing domain boundaries: a capability domain
should be **independently substitutable, independently ownable and
independently assessable**. Section XI-B concedes that some boundaries are
judgment calls. This section applies the three tests to all ten domains, so
that the concession rests on analysis rather than assertion.

The tests are read as follows. *Substitutable*: the realizing technology can be
replaced without changing another domain's interface. *Ownable*: one team can
be held accountable for the domain as a whole. *Assessable*: the domain's
health can be judged on evidence attributable to it, whether or not it produces
that evidence itself.

| Domain | Substitutable | Ownable | Assessable |
|:---|:---:|:---:|:---:|
| Developer Experience | ✓ | ✓ | ✓ |
| AI Runtime | ~ | ✓ | ~ |
| Model Services | ✓ | ✓ | ✓ |
| Knowledge Services | ✓ | ✓ | ✓ |
| Agent Services | ✓ | ✗ | ~ |
| Governance | ✓ | ✓ | ✓ |
| Security | ~ | ✓ | ✓ |
| Evaluation | ✓ | ✓ | ✓ |
| Operations | ✓ | ✓ | ✓ |
| Platform Management | ✗ | ✓ | ~ |

Six domains pass all three tests without qualification. Four are strained, and
the strain is not evenly distributed.

### B1 — AI Runtime ⟷ Agent Services (most serious)

This single boundary carries three distinct problems:

1. **Duplicated responsibility.** The AI Runtime entry in Section V listed
   "agent execution" among its responsibilities, while the Agent Services entry
   had it "expose agent execution to the runtime". Both domains claimed the same
   responsibility.
2. **Shared requirement discharge.** Table 1 maps **R3 to both domains**,
   because the requirement spans execution coordination and agent-specific
   autonomy. This is not dual ownership of one responsibility: AI Runtime owns
   execution state and invocation, while Agent Services owns planning, agent
   memory, reflection, collaboration and bounded tool use. The boundary was
   revised to remove the earlier overlap.
3. **Split memory.** "Memory management" sits in the Runtime, "agent memory" in
   Agent Services, so memory state has two homes.

Of these, (1) and (3) were genuine defects and were fixed by the boundary
revision; (2) is not a defect, since Table 1 records what each domain
principally discharges rather than sole ownership. Most of the capability
model's boundary strain was concentrated here.

### B2 — Platform Management fails substitution

This is a category problem rather than a placement problem. The domain mixes
substitutable technical capabilities (tenancy, environment management,
configuration, feature flags, version and release management) with product
functions that are not substitutable technology (roadmap, platform
documentation, catalog curation). A service catalog product can be swapped; a
roadmap cannot.

Notably, the manuscript observes that this is the domain "most often omitted"
in practice. The analysis suggests a reason: it is not wholly a capability.

### B3 — Cost is dual-owned

Model Services carries "cost optimization", Operations carries "cost
monitoring", and Table 1 maps **R10 to both**. This is a deliberate split
rather than an unresolved defect: Model Services owns request-level accounting
and cost-aware routing, Operations aggregates platform-level cost, utilization
and capacity telemetry. The manuscript flags it as a judgment call.

### B4 — Security is a cross-cutting concern rendered as a domain

Identity federation and secret management substitute cleanly. Prompt-injection
protection does not: it is inseparable from the request path, as
permission-aware retrieval is from Knowledge Services and tool permissions are
from Agent Services. Security passes the ownership test decisively — enterprise
security functions exist and are accountable — but substitution only in part.

The Security/Governance line is defensible but thin: Security supplies
authentication and authorization primitives, Governance renders policy
decisions, yet both produce allow/deny verdicts on the request path.

### Resolution

The ten-domain decomposition was reviewed against these findings and retained
in full: no domain was added, removed or merged. The findings were resolved as
follows.

| Finding | Resolution |
|:---|:---|
| **B1** Runtime ⟷ Agent Services | **Resolved by revising the boundary rather than the model.** The AI Runtime now owns the execution lifecycle and orchestration; Agent Services owns agent-specific reasoning and autonomy. The AI Runtime entry's responsibilities changed from "agent execution; memory management; tool invocation" to "execution state; agent and tool invocation", so the Runtime invokes agent behavior rather than implementing it, and memory belongs unambiguously to Agent Services. Table 1's summary row was updated to match. |
| **B2** Platform Management | **Assessed and kept.** The domain passes ownership and assessment, and its technical responsibilities (tenancy, configuration, feature flags, release management) are substitutable. The product-management responsibilities are accepted as part of treating the platform as a product, which is the domain's stated purpose. |
| **B3** Cost dual-owned | **Accepted with an explicit rationale.** The division is act versus observe: Model Services acts on cost (routing, token accounting, optimization); Operations observes and aggregates it (monitoring, capacity planning, usage analytics). Section VII already expresses the direction of flow — Operations supplies observed cost and capacity, Model Services routes on it — so the dual assignment reflects a real feedback loop rather than an unowned requirement. |
| **B4** Security ⟷ Governance | **Separation preserved.** The operative distinction is that Governance decides what is permitted, while Security establishes and enforces who and what may access or execute. The interaction model already expresses this. |

Section V now states the boundary rationale directly, so the decomposition
reads as principled rather than selected: *"These criteria also define the
domain boundaries: responsibilities remain together where they share
substitution, ownership and assessment concerns, and separate where those
concerns diverge."*

Both items flagged after this pass are now closed:

- **Resolved.** R3's mapping to both AI Runtime and Agent Services is
  intentional. Table 1 records the requirements each domain *principally
  discharges*, not sole ownership, and R3 spans execution coordination and
  agent-specific autonomy. The B1 revision separated those responsibilities, so
  no dual assignment remains to close.
- **Resolved.** Section XI-B no longer offers "the placement of
  memory between the runtime and agent services" as a genuine judgment call.
  That boundary has been settled, so the example no longer holds; cost remains
  a valid example.

This analysis also supplies concrete evidence for **E3 (extensibility)**, which
at present asserts that the four-concern grouping provides the criterion for
placing a new domain without demonstrating that the criterion discriminates.

## Provenance of the practitioner corpus

**Resolved for the grounding; still open for this corpus.** The practitioner
grounding is confirmed — prior professional experience designing and implementing
enterprise AI platform architecture in an industry setting. What this section
cannot settle is whether *these repository files* preceded the requirements, and
the practitioner column stays candidate for that reason.

The manuscript (Section III) names the practice source as

> the author's prior professional experience designing and implementing
> enterprise AI platform architecture

and the topic list that follows it maps one-to-one, in order, onto documents
D01–D08 below. That correspondence is what made this corpus look like the
source. It is not evidence that these files are the source: the confirmed
grounding is the professional experience, and the corpus is context whose
chronology this section cannot establish. The corpus is therefore identifiable. Two things about it are
not yet settled, and both affect how C1 may be worded:

1. **Whether the material informed the requirements, or was written alongside
   them.** If the documents and implementations preceded the requirements, this
   is derivation evidence and belongs in C1. If they followed, it is
   instantiation evidence and belongs in C3 — a *stronger* claim, since a
   capability model realized in eight systems is better evidence than one
   consolidated from documents.
2. **The period.** The artifacts carry a ten-week window, and the recorded
   sequence is:

   | When | What |
   |:---|:---|
   | 2026-06-10 → 07-21 | `Project_Synapse` (vector RAG vs GraphRAG; later quantization) |
   | 2026-06-17 → 06-27 | `Adaptive_Multi-Agent_Code_Review_System` |
   | 2026-07-23 → 07-30 | `self-hosted-llm-benchmark` |
   | 2026-08-04 05:42 → 08-05 17:18 | five platform services |
   | 2026-08-05 19:09 → 19:23 | reference documentation committed (5-doc generation, `image/`) |
   | 2026-08-06 02:26 | full 12-document set (`sample/`), single identical mtime |
   | 2026-08-06 04:12 | paper source |

   Each stage precedes the next, which is consistent with derivation. But the
   last three stages are separated by hours, not months, and the corpus carries
   one identical mtime, so it was written or copied in a single operation. The
   artifacts therefore establish a **sequence**, not a derivation: they cannot
   distinguish requirements consolidated from a corpus from a corpus and
   requirements both expressing the same prior thinking. They also do not
   support "an extended period".

   The exception is the first three systems, which show weeks of iterated
   commits ending well before the manuscript. That subset — bearing on R1, R2,
   R3 and R10 — is the practitioner evidence most likely to survive review.

Until (1) is answered the practitioner column stays marked candidate. Until (2)
is answered the phrase in Section III should not stand as written.

### Corpus inventory

`sample/Enterprise-AI-Reference/` — 10 documents, 19,097 words.

| ID | Document | Words |
|:---|:---|---:|
| D01 | Enterprise AI Architecture Principles (10 principles) | 2,399 |
| D02 | AI Platform Capability Model (10 domains) | 1,859 |
| D03 | Enterprise RAG & GraphRAG Patterns | 2,268 |
| D04 | Enterprise Agentic AI Design Patterns (10 patterns) | 1,990 |
| D05 | Enterprise AI Evaluation Framework | 2,065 |
| D06 | Enterprise AI Governance & Security | 2,178 |
| D07 | Architecture Decision Records (ADR-001…010) | 968 |
| D08 | Enterprise AI Platform Maturity Model | 1,084 |
| D09 | Glossary | 2,718 |
| D10 | References and Further Reading | 1,568 |

D02's sections are the paper's ten capability domains, in the paper's order.
D01's ten principles are near-verbatim antecedents of several requirements
(*Technology Neutrality*, *Governance by Design*, *Security by Default*,
*Observability by Default*, *Evaluation as a Platform Capability*, *Human
Accountability*, *Developer Experience*, *Continuous Evolution*). An earlier,
roughly 30% shorter generation of five of these documents is recoverable from
git at `image/Enterprise-AI-Reference/`.

Implementations, by capability domain:

| System | Scale | Domains |
|:---|:---|:---|
| `Enterprise_AI_Control_Plane` | 72 Java files | Governance (approval, audit, registry, security, observability) |
| `Enterprise_AI_Guardrail_Service` | 82 | Governance, Security (policy, orchestrator, evidence, input/output) |
| `Enterprise_AI_Runtime_Service` | 171 | AI Runtime |
| `Model_Gateway` | 139 | Model Services (routing, rate limiting) |
| `Enterprise_AI_SDK` | 47 | Developer Experience |
| `Adaptive_Multi-Agent_Code_Review_System` | 210 Python | Agent Services — this is Scenario 3 |
| `Project_Synapse`, `self-hosted-llm-benchmark` | 33 Python | Model Services (quantization, local inference) |
| `Tethera_Eval`, `Cohort Brain` | 37 Python | Evaluation; Knowledge Services |


## Open questions

1. Did the corpus documents and implementations precede the requirements, or
   were they developed alongside them? (Determines C1 vs C3 placement.)
2. ~~Is there material outside this repository that informed the work?~~
   **Answered: yes.** Prior professional experience designing and implementing
   enterprise AI platform architecture in an industry setting. It cannot be
   shared, and Section III of the manuscript now names it as the practice source.
3. Which implementations genuinely bear on the architecture? `Cohort Brain` and
   `Stock_Market_Analysis_App` may be unrelated and should be struck if so.
4. How should the corpus be characterized? **Neither claim is made.** The
   confirmed grounding is the professional experience, not these files; the
   corpus is retained as candidate context whose chronology is unestablished.
