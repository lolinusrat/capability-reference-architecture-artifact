# Documentary Triangulation of the Architectural Propositions

This register records the documentary triangulation reported in Section 10.2 of
the paper. It is the full evidence behind the summary table; the paper states
only the result.

## 1 Question

The requirements traceability (`requirements-traceability.md`) establishes that
the architecture is internally consistent with its own requirements. The
commercial-platform comparison (`commercial-platform-evidence-matrix.md`)
establishes that the capability domains provide a frame into which four
independently developed vendor platforms can be mapped. Neither answers a
narrower question:

> Do sources developed outside this work, and outside the four commercial
> platforms, corroborate the architectural propositions on which the reference
> architecture rests?

**The two families are not equally external to the derivation.** The governance
family — S1-S3, the NIST AI RMF with its Generative AI Profile, the EU AI Act and
ISO/IEC 42001 — is partly internal to the requirements of Section 4: R4, R5, R6, R7, R8
and R12 cite S1 and S2. ISO/IEC 42001 (S3) is cited by no requirement. Where S1 and S2 corroborate a proposition they partly
restate an input to it, and their ratings should be read as consistency rather
than as confirmation. The structural family — S4-S6 — is largely independent of the requirements:
S4 and S5 are cited by no requirement, while the Lu et al. taxonomy carried in
S6 is cited by R1. It therefore carries most of the independent structural
weight of the check for P1, P3 and P6. This is why the exercise
is named triangulation and not independent validation.

This check answers that question. It is a corroboration exercise, not a
systematic literature review, and it does not sample a population.

## 2 Propositions tested

Six propositions were extracted from the architecture. Each is a claim the
architecture makes about how an enterprise AI platform should be structured, and
each is stated so that a source can be judged to address it or not.

| ID | Proposition | Where the paper asserts it |
|:---|:---|:---|
| **P1** | An enterprise AI platform should be organised as a set of reusable **capability domains** rather than as products, components or services. | §5, D1 |
| **P2** | Capability definitions should be **technology-independent**, so that the implementing technology can be substituted without changing the capability structure. | §5 (domain definitions), D2, E2 |
| **P3** | Each capability should carry an **explicit responsibility boundary and a consumable interface**, so that it can be consumed without knowledge of its implementation. | §5 (interfaces/dependencies per domain), §6, E3 |
| **P4** | Assurance controls should be applied **on the execution path** — per request, as execution proceeds — rather than only through periodic assessment. | R5, D3, §7, E5 |
| **P5** | **Feedback relationships** between capabilities are architecturally significant and must be represented, not only the forward request path. | §7 (governance→runtime, evaluation→developer experience, operations→model services) |
| **P6** | Capabilities should be **owned, versioned and managed through a lifecycle** independently of their consumers. | D4, Table 1 (Platform Management), §8 |

P1, P2 and P6 are propositions the paper explicitly does **not** claim as novel
(§2.2, §2.5). P3, P4 and P5 are where the paper locates its contribution. The
triangulation is therefore as informative when it fails to corroborate as when
it succeeds.

## 3 Source selection

Six sources were selected before any assessment was made, against three
criteria: (i) developed independently of this work and of its author, which is
not the same as being absent from the requirement derivation — see §1; (ii)
addressing enterprise AI structure, governance or architecture as a whole rather
than one technique; (iii) publicly retrievable, so that the check is
reproducible. Two families were chosen deliberately — governance frameworks and
regulation, which constrain what a platform must do, and capability models and
reference architectures, which propose how it should be structured — because a
proposition corroborated by both families is better supported than one
corroborated within a single tradition.

| ID | Source | Family | Independence | Retrieved | Provenance |
|:---|:---|:---|:---|:---|:---|
| **S1** | NIST AI Risk Management Framework 1.0 (NIST AI 100-1), with the Generative AI Profile (NIST AI 600-1) | Governance framework | US federal standards body; no relation to this work | 2026-08-31 | verified — full text retrieved and inspected |
| **S2** | Regulation (EU) 2024/1689 (Artificial Intelligence Act) | Regulation | EU legislature | 2026-08-31 | verified — Articles 9 and 14 retrieved verbatim; remaining Articles cited by number |
| **S3** | ISO/IEC 42001:2023, AI management systems | Management-system standard | ISO/IEC joint technical committee | 2026-08-31 | author-read — clause and Annex A structure confirmed from published summaries of the standard; the standard itself is paywalled and was not retrieved in full |
| **S4** | IBM Generative AI Capability Model | Vendor-authored capability model | IBM; authored by named IBM contributors, last updated 30 April 2025 | 2026-08-31 | verified — page retrieved and inspected |
| **S5** | Enterprise AI Operating Framework (EAIOF), Enterprise AI Platform Capabilities and Enterprise AI Reference Architecture | Practitioner framework | Single-author framework by Jorge Nascimento; unaffiliated with this work | 2026-08-31 | verified — page retrieved and inspected |
| **S6** | Lu et al., reference architectures for foundation-model-based systems and agents, and the associated taxonomy | Peer-reviewed research | CSIRO Data61 research group | 2026-08-31 | verified — abstracts retrieved; full papers as cited in the manuscript |

**On S4 and S5.** S4 is vendor-authored and S5 is a single-author practitioner
framework, so neither is peer-reviewed and both carry the biases of their
origin. They are included because they are the only two sources in either family
that attempt a capability decomposition of an enterprise AI platform at the same
altitude as this work, which is precisely what P1 and P3 require a source to do.
Their limitations are treated in §6 below. S4 overlaps one of the four platforms
in the commercial comparison (IBM watsonx); the capability model is a distinct
artefact from the product documentation assessed there, but the overlap is
recorded rather than ignored.

## 4 Rubric

Applied per source per proposition, before cross-source comparison:

- **● corroborated** — the source states the proposition, or operationalises it
  in specific controls, clauses or named structures.
- **◐ partial** — the source supports part of the proposition, or implies it
  without stating it, or states it for a narrower unit of analysis than the
  shared enterprise platform.
- **○ not addressed** — the source is silent on the proposition, or its structure
  is organised on a basis that does not engage it.

A rating of ○ is a finding about the source's scope, not a criticism of it.

## 5 Result

| Source | P1 capability | P2 tech-independent | P3 boundary/interface | P4 execution path | P5 feedback | P6 ownership/lifecycle |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **S1** NIST AI RMF + GenAI Profile | ○ | ◐ | ◐ | ◐ | ◐ | ◐ |
| **S2** EU AI Act | ○ | ◐ | ◐ | ◐ | ◐ | ◐ |
| **S3** ISO/IEC 42001 | ○ | ◐ | ◐ | ◐ | ◐ | ◐ |
| **S4** IBM GenAI Capability Model | ● | ◐ | ◐ | ● | ◐ | ◐ |
| **S5** EAIOF | ● | ● | ● | ● | ◐ | ● |
| **S6** Lu et al. | ◐ | ◐ | ◐ | ● | ◐ | ○ |
| **Corroborated (●)** | 2 | 1 | 1 | 3 | 0 | 1 |

### 5.1 The 36-row evidence register

One row per source per proposition. **Evidence** gives the supporting passage or
a concise statement of what the source does, with the tightest locator
available; **Rationale** says why that evidence earns the rating under the §4
rubric. Quotation marks indicate verbatim text from the source.

#### S1 — NIST AI RMF 1.0 (AI 100-1) and Generative AI Profile (AI 600-1)

| Prop | Rating | Evidence (locator) | Rationale |
|:--|:--:|:---|:---|
| P1 | ○ | The Core is organised as four risk-management functions — GOVERN, MAP, MEASURE, MANAGE (§5) | The unit of organisation is the function, not the capability; no platform decomposition is proposed |
| P2 | ◐ | "voluntary, rights-preserving, non-sector-specific, and use-case agnostic, providing flexibility to organizations of all sizes and in all sectors" (§1) | The framework is itself stated independently of sector, use case and technology, but it neither states nor operationalises technology-independent capability definitions; the quoted attributes concern sector and use case, so it implies the proposition without stating it |
| P3 | ◐ | MAP requires intended purpose, context and system dependencies to be established and documented (MAP 1–2) | Establishes system boundaries; specifies no interface or consumption contract between capabilities |
| P4 | ◐ | MANAGE 2.4: "mechanisms are in place and applied, and responsibilities are assigned and understood, to supersede, disengage, or deactivate AI systems"; MANAGE 4.1 post-deployment monitoring plans | Runtime controls are required, but no placement in a request path is prescribed |
| P5 | ◐ | "Governance is designed to be a cross-cutting function to inform and be infused throughout the other three functions" (§5); "the process should be iterative, with cross-referencing between functions as necessary" (§5); MEASURE 3.3; MANAGE 4.2 | Feedback is structural to the framework, but as iteration among risk-management functions — a process — rather than as named relationships between platform capabilities |
| P6 | ◐ | GOVERN 2.1: "roles and responsibilities and lines of communication" documented and understood; GOVERN 2.3 executive accountability | Ownership of and accountability for AI risk are required outcomes; versioning and lifecycle management of capabilities independently of their consumers are not addressed |

#### S2 — Regulation (EU) 2024/1689 (AI Act)

| Prop | Rating | Evidence (locator) | Rationale |
|:--|:--:|:---|:---|
| P1 | ○ | Obligations attach to roles — provider, deployer, importer, distributor — and to risk classes | No capability decomposition of a platform is offered |
| P2 | ◐ | Accuracy, robustness and cybersecurity (Art. 15); logging (Art. 12); transparency (Art. 13) | Requirements are stated as outcomes without reference to implementing technology, which implies the proposition without stating it |
| P3 | ◐ | Responsibilities along the AI value chain (Art. 25); instructions for use sufficient to interpret output (Art. 13) | A boundary and contract between parties, not between capabilities |
| P4 | ◐ | Art. 14(1): systems "designed and developed in such a way … that they can be effectively overseen by natural persons during the period in which they are in use"; Art. 14(4): "intervene in the operation … or interrupt the system through a 'stop' button or a similar procedure"; Art. 12 automatic logging; Art. 26 deployer monitoring | Oversight, intervention and logging are required during use, but — as for S1 — no per-request control and no placement on the execution path is prescribed |
| P5 | ◐ | Art. 9(2): the risk management system "shall be understood as a continuous iterative process planned and run throughout the entire lifecycle of a high-risk AI system, requiring regular systematic review and updating"; Art. 9(2)(c) with post-market monitoring (Art. 72) | Operational evidence is required to flow back into risk decisions, as a lifecycle process rather than as relationships between capabilities |
| P6 | ◐ | Quality management system (Art. 17); provider obligations and value-chain responsibilities (Arts. 16, 25) | Ownership and lifecycle management of the AI system are mandatory; versioning of capabilities independently of their consumers is not addressed |

#### S3 — ISO/IEC 42001:2023

| Prop | Rating | Evidence (locator) | Rationale |
|:--|:--:|:---|:---|
| P1 | ○ | Annex A: 38 controls in nine objectives, A.2–A.10, covering AI policy, internal organisation, resources, impact assessment, life cycle, data, information for interested parties, use, and third-party relationships | Annex A decomposes management and control objectives thematically; it does not organise the shared platform by capabilities, so it does not engage P1 (re-rated from ◐, 25 September 2026) |
| P2 | ◐ | A management-system standard applicable to any organisation providing or using AI systems | Stated independently of implementing technology by construction, which implies the proposition without stating it |
| P3 | ◐ | A.3 requires roles and responsibilities to be defined and allocated; A.10 allocates responsibility across supplier and customer boundaries | Organisational boundaries, not technical interfaces |
| P4 | ◐ | A.6 covers the AI system life cycle including operation and monitoring; A.9 covers responsible use | Operation and monitoring are required life-cycle controls, comparable to S1's post-deployment monitoring; where controls sit relative to a request is not addressed |
| P5 | ◐ | Plan–do–check–act structure; performance evaluation (Clause 9); continual improvement (Clause 10) | Feedback is a required element of the management system, as organisational process (plan–do–check–act) — the basis on which S5 P5 is also partial |
| P6 | ◐ | Roles, responsibilities and authorities (Clause 5.3); internal organisation (A.3); life cycle to retirement (A.6) | Ownership and the AI system life cycle are explicit requirements; versioning of capabilities independently of their consumers is not |

#### S4 — IBM Generative AI Capability Model

| Prop | Rating | Evidence (locator) | Rationale |
|:--|:--:|:---|:---|
| P1 | ● | "six major categories" and "the level 1, 2, and 3 enterprise capabilities required to effectively deploy and manage generative AI solutions" (Overview) | Capability is the unit of organisation, at three levels |
| P2 | ◐ | Capabilities described functionally, but presented as part of IBM's Generative AI Architecture and elaborated in IBM's own architecture tooling; "typically this capability will be realized using a cloud platform" (Model Customization) | No technology-independence claim; realisation assumptions appear in the text |
| P3 | ◐ | Capability groups are named and described; Model Hosting refers to "API-enabled services" | Each capability is named with a described responsibility, and hosting is exposed as API-enabled services; interfaces, inter-group dependencies and boundary criteria are not stated |
| P4 | ● | HAP Detection: "the ability to detect and filter hate, abuse, and profanity in both prompts submitted by users and in responses generated by the model"; Prompt Monitoring and Security against prompt injection; Model Access Policy Management; Model Monitoring described as operating in real time | Controls are applied inline on inputs and outputs |
| P5 | ◐ | Data Management includes "capabilities to log and rate model responses for auditing purposes, and as input to further model tuning and refinement" | One explicit feedback path, into tuning rather than into runtime policy or developer-facing signals |
| P6 | ◐ | GenAI Operations includes "managing the lifecycle of models once deployed" | The lifecycle managed is the model's; no capability ownership or platform versioning independent of consumers |

#### S5 — Enterprise AI Operating Framework, Platform Capabilities

| Prop | Rating | Evidence (locator) | Rationale |
|:--|:--:|:---|:---|
| P1 | ● | The capability model "organizes the platform's capabilities into coherent groups aligned with the architectural layers and dimensions", distinguishing layered capabilities — infrastructure and runtime, model and reasoning, orchestration and agents, knowledge and data — from cross-cutting ones (The Enterprise AI Platform Capability Model) | An explicit capability decomposition of a shared enterprise platform |
| P2 | ● | "The Enterprise AI Reference Architecture defines a technology-independent structure"; building blocks are defined "by their responsibilities and boundaries, without prescribing the technologies that implement them"; a capability is "a stable service contract wrapped around an evolving implementation" (Introduction; What Is a Platform Capability) | States the proposition directly and operationalises it as a contract |
| P3 | ● | A capability "must have a clear and stable interface, a well-defined responsibility, and boundaries that allow it to be consumed without knowledge of its internal implementation"; composability depends "on the same disciplined boundaries that make capabilities reusable and governable" (Characteristics) | Boundary and interface are stated as design criteria |
| P4 | ● | Guardrails are "applied at the points where behavior enters and leaves the system and where actions are taken"; the Policy Engine enforces policies "consistently wherever they apply"; the AI Gateway is "a single, governed point through which model access flows"; "policy that cannot be enforced is merely aspiration" (Trust, Security and Governance; The Platform as Foundation) | Assurance is placed on the execution path and argued for explicitly |
| P5 | ◐ | Adoption measurement "provides the feedback through which the platform learns which capabilities to invest in and how to improve them" (Platform Capabilities as Products); continual improvement in the operational domain | Feedback appears as organisational learning; runtime feedback edges between capabilities are not specified as architectural relationships |
| P6 | ● | A capability "can be assigned an owner, subjected to policy, monitored, versioned, and held accountable for its behavior"; capabilities are provided as products that are "owned, managed through their lifecycle, and measured by adoption" (What Is a Platform Capability; As Products) | Ownership, versioning and lifecycle are stated requirements |

#### S6 — Lu et al., reference architectures and taxonomy

| Prop | Rating | Evidence (locator) | Rationale |
|:--|:--:|:---|:---|
| P1 | ◐ | A taxonomy of foundation-model-based systems through an architectural lens, and pattern-oriented reference architectures for systems and agents | Architectural decomposition, but the unit is the individual system or agent, not the shared platform |
| P2 | ◐ | Pattern-oriented architectures not tied to a particular model or vendor | Organised around the foundation model as a component rather than around technology-independent capability domains |
| P3 | ◐ | The growing capabilities of foundation models "can eventually absorb other components of AI systems, posing challenges of moving boundary and interface evolution in architecture design" (FM-systems reference architecture, abstract) | Boundary and interface evolution is a named architectural concern with a dedicated design decision, but between components of an individual system — the narrower unit on which S6 P1 is also partial |
| P4 | ● | Both architectures target responsible foundation-model systems and agents, addressing responsible-AI quality attributes "such as security and accountability" through patterns applied around the model and the agent; the agent architecture is evaluated by mapping to two real-world agents | Controls are placed architecturally around execution |
| P5 | ◐ | Continuous validation and monitoring appear among the patterns | Feedback is not presented as a distinct set of architectural relationships |
| P6 | ○ | Ownership and an operating model are not addressed. Versioning appears as a co-versioning registry and AIBOM audit traceability; accountability is named as a responsible-AI quality attribute | Accountability and co-versioning are engaged, but not ownership and lifecycle of capabilities independently of their consumers: the structure is organised on a basis that does not engage P6 (second clause of the §4 ○ definition). Rationale corrected 22 September 2026; rating unchanged |

### 5.2 Negative and qualifying findings, retained

These are the results that do **not** support the architecture, kept together so
they cannot be lost in the per-source detail.

1. **Feedback relationships are poorly corroborated as architecture.** All three
   governance sources require feedback as *process* (S1 P5, S2 P5, S3 P5); none
   of the three architecture and capability sources represents it as a set of
   named relationships between capabilities (S4, S5, S6 all ◐, each on the
   strength of a single loop). Section 7 of the paper is therefore unsupported
   by independent architecture sources, though also uncontradicted.
2. **EAIOF weakens the novelty of the boundary criteria.** S5's stated
   characteristics — reusability, being "governed as a unit", and being
   "versioned and evolvable" — parallel the paper's criteria of independent
   substitutability, ownership and assessment closely enough that the criteria
   must be described as corroborated rather than introduced here.
3. **IBM supplies an alternative assurance decomposition.** S4 groups assurance
   by the asset protected — application, model and data security — where this
   architecture groups it by concern, and has no separate evaluation domain.
   This is a genuine competing decomposition of the same responsibilities.
4. **Capability-based organisation is corroborated thinly.** Only S4 and S5
   reach ● on P1, and neither is peer-reviewed.

## Evidence re-verification — S6, 22 September 2026

**Original assessment snapshot: 31 August 2026.** The six ratings for S6, the
rubric and the access date are unchanged by this pass and remain the assessment
of record.

S6 was originally recorded as *"verified — abstracts retrieved; full papers as
cited in the manuscript"*. Because S6 carries weight for P3 in §6, and because the
P3 quotation was taken from an abstract, all three papers were retrieved in full
and re-read on 22 September 2026:

- Lu et al., *A Taxonomy of Foundation Model based Systems through the Lens of
  Software Architecture* — <https://arxiv.org/abs/2305.05352>
- Lu et al., *A Reference Architecture for Designing Foundation Model based
  Systems* — <https://arxiv.org/abs/2304.11090>
- Lu et al., *Towards Responsible Generative AI: A Reference Architecture for
  Designing Foundation Model based Agents* — <https://arxiv.org/abs/2311.13148>

**No rating changed.** Provenance for S6 moves from abstract-level to full-text.

| Prop | Rating | Full-text outcome |
|:--|:--:|:---|
| **P1** | ◐ | Confirmed. The unit is the individual system or agent: the taxonomy organises *"design options of individual foundation-model-based systems"*, and the agent architecture is evaluated at agent level. Neither addresses a shared multi-application platform. |
| **P2** | ◐ | Confirmed, and the body is less technology-independent than the abstracts suggest: the taxonomy names LLMs, ChatGPT, GPT-4, LoRA, Pinecone and Milvus directly. The pattern-oriented architectures remain vendor-neutral, which is what holds the cell at partial rather than moving it down. |
| **P3** | ● | **Confirmed and strengthened.** The moving-boundary and interface-evolution concern is not only in the abstract: it appears in the introduction of the FM-systems architecture and has a dedicated design decision, *"Responsibilities of external components"*, in §3.3. The rating no longer rests on abstract text. |
| **P4** | ● | Confirmed. Guardrails are applied at preprocessing, intermediate process and postprocessing stages, with a continuous risk assessor, black box recorder and verifier; the architecture is evaluated by mapping to two real-world agents, MetaGPT and HuggingGPT. One qualification: these components are presented as *plugins* rather than mandatory execution-path elements. |
| **P5** | ◐ | Confirmed. Reflection and monitoring patterns exist, but feedback is not named as a set of architectural relationships between components. |
| **P6** | ○ | Rating held, **rationale corrected** — see below. |

### Correction to P6's rationale

The original rationale read *"Ownership, capability versioning and an operating
model are not addressed."* The versioning clause is wrong. Both the agent
architecture (§3.6) and the taxonomy document a **co-versioning registry**, and the
agent architecture adds N-version programming; the taxonomy also carries an AIBOM
for traceability.

The rating is nonetheless held at ○, under the second clause of the rubric's ○
definition rather than the first: the source is not silent, but its structure is
organised on a basis that does not engage the proposition. P6 asks that
capabilities be owned, versioned and managed through a lifecycle **independently of
their consumers**. Co-versioning is the opposite arrangement — artifacts versioned
*together* — and the taxonomy's versioning *"appears only as an audit mechanism
tied to accountability"* rather than as independent lifecycle management.
Ownership and an operating model are absent from both papers.

The rationale should therefore read: *ownership and an operating model are not
addressed, and versioning appears as co-versioning and audit traceability rather
than as independent capability lifecycle.*

### S2 and S3 are not retrieved in full

ISO/IEC 42001:2023 is paywalled and was assessed from the published clause and
Annex A structure. That cannot be resolved without purchasing the standard, and
limitation 4 of §7 continues to record that its cells carry lower confidence than
the sources retrieved in full. After this pass, four of six sources are
verified in full text. S2 is verified verbatim only for Articles 9 and 14, and
S3 from its clause and Annex A structure.

## Consistency re-rating — 24 September 2026

**Original assessment snapshot: 31 August 2026; sources unchanged.** A
consistency check found the §4 rubric applied unevenly across the two families.
The capability sources were held to the partial clause — *supports part of the
proposition, implies it without stating it, or states it for a narrower unit of
analysis* — and the governance sources were not. S4 P2 is partial for making "no
technology-independence claim". S4 P6 is partial because "the lifecycle managed
is the model's". S5 P5 is partial because its feedback "appears as organisational
learning". The governance sources had been rated ● on exactly those grounds.
Thirteen cells were re-rated under the same rubric; no source was re-read and no
evidence changed.

| Cell | Was | Now | Reason |
|:---|:--:|:--:|:---|
| S1, S2, S3 / P2 | ● | ◐ | Technology-neutral themselves, but none states technology-independent capability definitions — implied, not stated |
| S1, S2, S3 / P5 | ● | ◐ | Feedback required as process, not as relationships between capabilities — the ground on which S5 P5 is partial |
| S1, S2, S3 / P6 | ● | ◐ | Ownership and AI-system lifecycle required; capability versioning independent of consumers absent — the ground on which S4 P6 is partial |
| S2 / P4 | ● | ◐ | Same kind of evidence as S1 P4 (oversight and intervention during use, no execution-path placement), which was partial |
| S3 / P4 | ○ | ◐ | Operation and monitoring controls, comparable to S1 P4; lower confidence, as S3 was assessed from its structure |
| S4 / P3 | ○ | ◐ | Capabilities carry described responsibilities and API-enabled hosting — part of the proposition |
| S6 / P3 | ● | ◐ | Boundaries between components of an individual system — the narrower-unit ground on which S6 P1 is partial |

Totals move from 19 ●, 12 ◐, 5 ○ to **8 ●, 25 ◐, 3 ○**. The ● counts by
proposition move from P1–P6 = 2, 4, 2, 4, 3, 4 to **2, 1, 1, 3, 0, 1**.

**What changes in the findings.** Finding 1 is rewritten: P2 and P6 are no longer the
best-corroborated propositions. P4 is, and Finding 2 now reports it with three sources.
Finding 3's substance is unchanged, and its cells now match it. Finding 4 is recounted. Finding 5 is
unchanged.

## Consistency re-rating — 25 September 2026

**Original assessment snapshot: 31 August 2026; sources unchanged.** One further
cell was found applied unevenly. NIST P1 is ○ because its Core is organised by
risk-management function rather than capability; ISO/IEC 42001 P1 was ◐ on the
ground that Annex A is "a decomposition of responsibilities, but thematic rather
than of platform capabilities". Both are decompositions of responsibilities on a
non-capability basis, which is the second clause of the §4 ○ definition — the
source's structure "is organised on a basis that does not engage it". No source
was re-read and no evidence changed.

| Cell | Was | Now | Reason |
|:---|:--:|:--:|:---|
| S3 / P1 | ◐ | ○ | Annex A decomposes control objectives thematically; it does not organise the platform by capabilities — the same ground as S1 P1 |

Totals move from 8 ●, 25 ◐, 3 ○ to **8 ●, 24 ◐, 4 ○**. The ● counts by
proposition are unchanged (P1–P6 = 2, 1, 1, 3, 0, 1). Across the 24 and 25
September passes, fourteen cells have been re-rated. The rubric is now printed in
the Table 5 caption, so the asymmetry would have been visible to a reader.

**What changes in the findings.** None in substance. Finding 5 now reports all three
governance sources as not organising on a capability basis, which strengthens its
conclusion that P1 is corroborated thinly.

## 6 Findings

**Finding 1 — Full corroboration comes only from the capability sources.** Every ● in
the matrix is held by S4, S5 or S6. The governance family supports each
proposition it addresses only partially, because it states obligations for AI
systems and organisations rather than properties of platform capabilities.
Technology independence (P2) and capability ownership and lifecycle (P6), which
the paper does not claim as novel (§2.2, §2.5), are fully corroborated only by EAIOF
and partially by four or five other sources. An earlier version of this finding
reported both as the best corroborated, with four ● each; that rested on
governance-family ratings that did not apply the rubric's partial clause as it
was applied to S4–S6, and was corrected on 24 September 2026.

**Finding 2 — Execution-path assurance is well corroborated, but as an obligation
rather than as an architectural placement.** Three sources (S4, S5, S6) corroborate P4, which makes it the best-corroborated
proposition, and they do so from different directions: IBM filters prompts and
responses inline, EAIOF applies guardrails where behaviour enters and leaves the
system, and Lu et al. place responsible-AI patterns around the model at runtime.
The three governance sources require oversight, intervention or monitoring
during use without placing controls on the execution path, and are partial. What none of them
specifies is *where* in a multi-capability request path each control is applied
and by which capability. This supports the paper's D3 consequence — that an
architecture must state where each control is applied — and it is also the
reason D2 is stated as coordination rather than as a single point of
application: the corroborating sources place controls at gateways, at model
boundaries, at agent action points and at data access, not at one location.

**Finding 3 — Feedback is universally required as process and largely absent as
architecture.** All three governance sources support P5 (S1, S2, S3) only
partially, because all three do so as a requirement for iteration, review and continual improvement
over a lifecycle. None of the three architecture and capability sources (S4, S5,
S6) represents feedback as a set of named relationships between capabilities;
each reaches ◐ on the strength of a single loop (response logging into tuning;
adoption into platform investment; continuous validation as a pattern). The
paper's §7 treatment of three specific runtime feedback edges is therefore not
contradicted by any source, and is not supplied by any of them either. This is
the clearest point of differentiation the triangulation produces.

**Finding 4 — Boundary criteria are corroborated more strongly than expected.** P3
receives one ● and five ◐. EAIOF in particular states capability characteristics
— reusability, being "governed as a unit", and being "versioned and evolvable" —
that closely parallel the paper's boundary criteria of independent
substitutability, ownership and assessment (§3, §5). This is genuine independent
corroboration of the criterion, and it correspondingly weakens any claim that the
criterion is novel. The paper's narrower claim — that boundaries should be drawn
by an explicit stated criterion and the derivation made traceable — survives,
since no source publishes a traceable derivation from requirements to
boundaries; but the criterion itself should be described as corroborated rather
than as introduced here.

**Finding 5 — Capability-based organisation of an enterprise AI platform is attempted
by few independent sources.** Only S4 and S5 reach ● on P1, and both are outside
peer review. NIST, the EU AI Act and ISO/IEC 42001 do not organise on this basis at
all (○) — ISO's Annex A decomposes control objectives thematically, not into
platform capabilities; and Lu et al. work at the system rather than platform
altitude (◐). The proposition is therefore corroborated but thinly, and the paper
should not represent it as broadly established.

## 7 Limitations

1. **Not a systematic review.** Six sources were selected purposively against
   stated criteria. They are not a sample, and no claim of coverage or
   saturation is made. A different six sources could yield different marginal
   counts, though Findings 1–3 rest on patterns visible across both families rather
   than on individual cells.
2. **Single rater.** All 36 cells were rated by the same person who derived the
   propositions and wrote the architecture. This is the same threat recorded for
   the commercial-platform comparison in §11.2 of the paper, and it is more
   acute here because the propositions were extracted from the author's own
   artefact. The rubric was fixed before assessment and the evidence for every
   cell is recorded above so that a reader can re-rate independently.
3. **Confirmation direction.** The propositions were written after the
   architecture, not before. The exercise can corroborate the propositions; it
   cannot show that a different decomposition would fail to be corroborated by
   the same sources. Several sources would in fact corroborate P2 and P6 for
   almost any well-formed platform architecture.
4. **Uneven provenance.** S3 was assessed from the published clause and Annex A
   structure rather than from the full paywalled text, and its cells carry lower
   confidence than the four sources retrieved in full. S2 is cited by Article
   number throughout but only Articles 9 and 14 were retrieved verbatim.
5. **Two sources are not peer-reviewed.** S4 is vendor-authored and S5 is a
   single-author practitioner framework. They carry the most weight on P1 and P3,
   which are the propositions with the weakest independent support overall. That
   the two strongest corroborations of capability-based organisation come from
   outside peer review is itself part of the finding (Finding 5), not a defect concealed
   by it.
6. **Snapshot.** S4 and S5 are living web documents, retrieved on 31 August 2026.
   S4 records a last update of 30 April 2025. Both may change.

## 8 Reproducing this check

1. Take the six propositions in §2 and the rubric in §4 as given.
2. Retrieve the six sources listed in §3.
3. Rate each source against each proposition before comparing across sources.
4. Compare the result with the matrix in §5 and with Table 5 of the paper.

Disagreement on individual cells is expected; the findings in §6 depend on the
distribution across the two source families rather than on any single rating.
