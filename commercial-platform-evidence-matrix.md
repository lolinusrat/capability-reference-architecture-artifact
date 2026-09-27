# Commercial Platform Coverage — Evidence Matrix

Supporting dataset for **Table 4** of *A Capability-Based Reference Architecture
for Enterprise AI Platforms*. It records how each of the 40 capability-coverage
ratings was derived, so the comparison is reproducible rather than an author
impression.

> **Status: FROZEN, re-rated 24 September 2026.** All four vendors collected and
> calibrated. Table 4 now carries **36 substantial, 4 partial, 0 limited**, after
> all forty cells were counted against the Table 1 responsibilities: six were
> raised and one lowered — see **Re-rating — 24 September 2026** below. The original, pre-recheck assessment was
> 31 substantial and 9 partial. Any change here must be mirrored in Table 4 and
> vice versa.

## Snapshot date

**Resolved: 15 August 2026**, matching §X-A of the manuscript. All evidence
was read on that date.

The rule adopted: the stated snapshot date is the actual completion date of the
evidence collection, not a predeclared date. A snapshot cannot claim an
observation date later than the day the evidence was read, and a reviewer
checking an archive capture would find the discrepancy.

## What the ratings measure

The rubric scores **documented** coverage, not actual capability. Where a
vendor's documentation cannot be located or retrieved, the rating falls, by
design. This is the intended behavior — the comparison is of what an enterprise
architect can establish from published material — but it means a low rating is
evidence about documentation as much as about the product. Retrieval problems
affected Google Operations and three IBM cells at the original snapshot; all
were later resolved, as recorded below.

Only **official vendor documentation** is admissible. Blog posts, conference
talks, analyst reports and third-party summaries are not.

**Inclusion rule.** Related first-party services count only where they form part
of the assessed platform's documented capability surface. Separately licensed
adjacent governance, compliance or audit products — Microsoft Purview, Google
Security Command Center, AWS Audit Manager — are excluded, consistently across
vendors, as are separately billed products documented outside the assessed
platform, such as Google API Gateway's model routing. A vendor's official
technical documentation on its own documentation site is admissible (for
example Google's `adk.dev` for the Agent Development Kit). Documented Preview features count, since the rubric scores documented
capability rather than general availability.

## Scoring rubric

Fixed before rating, so symbols are reproducible.

| Rating | Rule |
|:---|:---|
| **● Substantial** | The vendor provides a clearly documented first-party capability covering most of the responsibilities defined for that domain. |
| **◐ Partial** | Relevant capability exists, but coverage is fragmented, narrower than the domain definition, limited to certain products or workloads, or lacks major responsibilities. |
| **○ Limited** | Official documentation provides little evidence of first-party coverage for the domain as defined. |

"As defined" means the responsibilities listed for that domain in Section 5 of
the manuscript. The rating is of **architectural coverage**, not product
quality, maturity or market position.

### Rubric asymmetry — stated in the paper (§XI-B)

The domains do not enumerate equal numbers of responsibilities. In Table 1
Governance lists five and Platform Management seven, and Knowledge Services
eight, so all three are strict; Security and Model
Services are comparatively permissive. A pattern of `◐` in the wide domains is
therefore partly an artifact of how the domain definitions were written, not
purely a finding about vendors. §XI-B now discloses this, noting that
cross-domain comparisons should be read qualitatively rather than as equivalent
numerical scores.

### Anchoring risk

Vendors are collected sequentially but **rated finally only after all four are
in**. Scoring vendor *n* against the standard implicitly set by vendor *n−1*
would make the first vendor collected the yardstick. A cross-check pass over
all 40 cells was completed before Table 4 was finalized.

## Vendor mapping

Table 4 now names the four products directly; the A–D labels below are retained
only as internal section keys for this document.

| Column | Vendor | Products assessed |
|:---|:---|:---|
| A | Amazon Web Services | Amazon Bedrock, Amazon Bedrock AgentCore |
| B | Microsoft | Microsoft Foundry, Foundry Control Plane |
| C | Google Cloud | Vertex AI / Gemini Enterprise Agent Platform |
| D | IBM | watsonx.ai, watsonx.governance, watsonx Orchestrate |

## Prior ratings (unverified baseline)

Preserved for diffing. These are the ratings in the manuscript before this
exercise (then numbered Table 3); their derivation was not recorded.

| Domain | A | B | C | D |
|:---|:---:|:---:|:---:|:---:|
| Developer Experience | ● | ● | ● | ◐ |
| AI Runtime | ● | ● | ◐ | ◐ |
| Model Services | ● | ● | ● | ◐ |
| Knowledge Services | ● | ● | ◐ | ● |
| Agent Services | ◐ | ◐ | ◐ | ◐ |
| Governance | ◐ | ◐ | ◐ | ● |
| Security | ● | ● | ● | ● |
| Evaluation | ◐ | ◐ | ○ | ◐ |
| Operations | ● | ● | ● | ◐ |
| Platform Management | ○ | ○ | ○ | ○ |

---

## A — Amazon Web Services (Bedrock, AgentCore)

Final Table 4 row: **● ● ● ● ● ◐ ● ● ● ●** (Platform Management re-rated ◐→● on 24 Sep 2026; the table below is the original assessment)
Changes from baseline: **Agent Services ◐→●, Evaluation ◐→●, Platform Management ○→◐**

| Domain | Prior | Proposed | Evidence | Verification |
|:---|:---:|:---:|:---|:---|
| Developer Experience | ● | ● | Bedrock APIs and SDKs across Java, JavaScript, Python/Boto3, Go, .NET, C++, Kotlin; API reference and code examples. AgentCore CLI scaffolding for agents, memory, gateways, credentials, evaluators. | not independently re-checked |
| AI Runtime | ● | ● | AgentCore Runtime: managed serverless agent runtime, session isolation, async execution, multimodal and multi-agent workloads. Harness: orchestration, tool execution, memory management, response generation. | **confirmed** — Harness text verified verbatim |
| Model Services | ● | ● | Access to many foundation models with documented model swapping; model lifecycle states (Active/Legacy/EOL) exposed via API; token accounting, quotas, provisioned throughput. | not independently re-checked |
| Knowledge Services | ● | ● | Knowledge Bases: managed RAG, vector stores, structured data stores, Neptune Analytics GraphRAG; metadata filtering including recency; RetrieveAndGenerate returns citations to source chunks. | not independently re-checked |
| Agent Services | ◐ | ● ⚠ | AgentCore Runtime, Harness, Memory (short/long term), Gateway (MCP/tools), Identity, Registry, Evaluations, Observability, multi-agent support, governed tool access. | **confirmed with qualification** — see note below |
| Governance | ◐ | ◐ | Guardrails: content policies, denied topics, sensitive-information protection, contextual grounding, prompt-attack protection, automated reasoning checks; account-level enforcement. Registry adds governed publishing/approval. Domain also requires risk classification, usage policy and compliance reporting, not evidenced as first-party. | agreed — rating consistent with rubric |
| Security | ● | ● | Guardrails prompt-injection, jailbreak and prompt-leakage detection; AgentCore Identity with fine-grained access control; Gateway governs tool/service access; IAM and CloudTrail over Bedrock API activity. | not independently re-checked |
| Evaluation | ◐ | ● | Bedrock evaluations cover models **and** knowledge bases, plus models and RAG sources *outside* Bedrock; automatic, human and LLM-as-judge evaluation; custom datasets and metrics. AgentCore Evaluations is a purpose-built agent evaluation service operating on sessions, traces and spans. | **confirmed** — both pages verified |
| Operations | ● | ● | Model invocation logging to CloudWatch Logs and S3; CloudWatch metrics including token and cache usage; AgentCore Observability with traces, workflow-step visualization, latency, token usage, errors, OTEL-compatible telemetry. | not independently re-checked |
| Platform Management | ○ | ◐ | AgentCore Registry: centralized catalog for agents, MCP servers, tools and skills across the organization, with publish/review/approval workflows. Bedrock control-plane APIs for model management, lifecycle, configuration and quotas. Domain also requires tenancy, environments, feature management, platform releases, platform metrics and roadmap — not evidenced as a unified capability. | **confirmed** — Registry text verified verbatim |

### ⚠ Agent Services — why `●` is marginal

The domain enumerates eight responsibilities: planning and task decomposition;
tool registry and tool permissions; agent registry; agent memory; reflection;
multi-agent collaboration; human approval integration; agent monitoring.

AgentCore documents first-party coverage of five — tool registry and
permissions, agent registry, memory, multi-agent, monitoring. **Planning, task
decomposition and reflection do not appear**, and neither does human approval
integration. The overview instead states that Runtime "works with custom
frameworks and any open-source framework, including CrewAI, LangGraph,
LlamaIndex, Google ADK".

`●` is defensible under "most of the responsibilities" (5 of 8), but the
rationale must record the delegation, because a reviewer checking for
"planning" will not find it.

> **Superseded, 24 September 2026.** The eight-responsibility list above is not
> Table 1's, which lists five: planning, tool invocation, agent memory,
> reflection and multi-agent collaboration. And the delegation claim is wrong
> for the snapshot. AgentCore Harness is "A managed agent loop" that
> "handles orchestration, tool execution, memory management, and response
> generation" (GA June 2026), and episodic memory documents reflections that
> "analyz[e] past episodes to surface insights, patterns, and higher level
> conclusions" (December 2025). Bedrock Agent Services is 5 of 5 and stays ●.
> AWS supplies agent reasoning first-party *and* hosts third-party frameworks
> on the same runtime; the paragraph below is kept as the original reading.

---

## C — Google Cloud (Vertex AI / Gemini Enterprise Agent Platform)

Final Table 4 row: **● ● ◐ ● ● ◐ ● ● ● ●** (Knowledge Services and Platform Management re-rated ◐→●, and Model Services ●→◐, on 24 Sep 2026; the table below is the original assessment)
Changes from baseline: **AI Runtime ◐→●, Agent Services ◐→●, Evaluation ○→●,
Platform Management ○→◐**  
*(Operations was provisionally lowered to ◐, then restored to ● when the relocated observability documentation was found — see the Operations row.)*

All evidence below is official Google documentation, read from page **body
text**, collected 2026-08-15.

| Domain | Prior | Proposed | Evidence | Note |
|:---|:---:|:---:|:---|:---|
| Developer Experience | ● | ● | Gen AI SDK: "unified interface" across the Gemini Developer API and Agent Platform; code portable between them "without rewriting your code". Model Garden discover/test/customize/deploy. Colab, Colab Enterprise, Workbench notebooks; GitHub samples. | |
| AI Runtime | ◐ | ● | Agent Runtime (managed, serverless); Sessions provide execution state; Agent Gateway; asynchronous and bidirectional streaming. | retry/fallback and human approval not evidenced |
| Model Services | ● | ● | Model Garden: single library of Google and partner models, consistent deployment pattern, integrated tuning/evaluation/serving. Documented model lifecycle with retirement dates and migration paths. Per-region and per-model quotas with token metrics. | |
| Knowledge Services | ◐ | ◐ | RAG Engine: multiple vector database choices (RagManagedDb, Vector Search, Pinecone), metadata-search filtering, reranking, cross-corpus retrieval, Document AI and LLM parsers, CMEK/VPC-SC. | **no graph retrieval and no citation support found** — a real divergence from AWS |
| Agent Services | ◐ | ● | Memory Bank (generation, revisions, profiles, IAM-scoped access), Sessions, Skill Registry, Agent Identity, Managed Agents API, sandbox environment, Agent2Agent, first-party ADK. | planning is first-party via ADK, unlike AWS |
| Governance | ◐ | ◐ | Model Armor enforces AI safety and security policies consistently across applications and supports compliance; configurable safety filters; IAM. | model/prompt/agent approval and risk classification not evidenced |
| Security | ● | ● | Model Armor screens LLM prompts and responses, prevents malicious input, verifies content safety, protects sensitive data — including across other cloud providers. CMEK, VPC-SC, IAM, Agent Identity. | |
| Evaluation | ○ | ● ✔ | **Resolved 2026-08-15.** Canonical page: *Gen AI evaluation service overview* — "Gemini Enterprise Agent Platform provides evaluation for agents, predictive AI models, and generative AI models… The Gen AI evaluation service provides enterprise-grade tools for objective, data-driven assessment of generative AI models", supporting model migrations, prompt editing and fine-tuning. Separate agent-evaluation and model-evaluation paths documented. | evidence gap closed |
| Operations | ● | ● ✔ | *Agent observability*: "comprehensive visibility into the performance, behavior, and health of your deployed agents and MCP servers", with telemetry sent "in the OpenTelemetry format"; *Traces*: distributed tracing via Cloud Trace, Cloud Logging and Telemetry APIs, where a trace comprises spans representing "a function call or an interaction with an LLM". Request-response logging to BigQuery is additionally available (Preview). | **resolved.** An initial pass recorded "searched, not found" and provisionally lowered this to ◐; that was a retrieval failure, not absent capability. Google's documentation had moved to `/gemini-enterprise-agent-platform/` on a different host, and the pages were located by following navigation links rather than guessing paths. Restored to ● |
| Platform Management | ○ | ◐ | Agent Platform is "a fully managed environment for developers to handle testing, release management, and reliability at a global scale"; configurable quotas; Model Garden and Skill Registry as catalogs; published model retirement schedule. | tenancy, environments, feature management and platform metrics not evidenced |

### Architectural contrast worth keeping

*Withdrawn 24 September 2026.* This section contrasted Google supplying agent
reasoning first-party with AWS delegating it to third-party frameworks. AWS
documents a first-party managed agent loop (AgentCore Harness) before the
snapshot, so the contrast does not hold, and §10.1 of the manuscript no longer
uses it. Both vendors supply agent reasoning first-party; AWS additionally
hosts third-party frameworks on the same runtime.

### ⚠ Google has reorganized the product

Pages formerly under Vertex AI generative AI now render under **"Gemini
Enterprise Agent Platform"**. The RAG page is titled *"RAG Engine on Gemini
Enterprise Agent Platform overview"*, and the documentation breadcrumb reads
*Home › Documentation › AI and ML › Gemini Enterprise Agent Platform › Agents*.

Two consequences:

1. **The Vertex AI reference** is currently *"Google Cloud: Vertex AI documentation"*.
   The product naming needs rechecking before submission, and the cited URL must
   resolve to what the citation claims.
2. This is the strongest churn data point collected so far — a whole-platform
   reorganization inside the paper's own writing window, alongside Bedrock
   Agents Classic entering maintenance mode. Both belong in §XI-C, once the
   matrix is complete.

### Observed, first-party

| Area | Documented features |
|:---|:---|
| Retrieval | RAG Engine: vector database choices (RagManagedDb, Vector Search, Pinecone), metadata-search filtering, reranking, cross-corpus retrieval, Document AI / LLM parsers, CMEK and VPC-SC controls |
| Agents | Agent Runtime (managed, serverless), Sessions, Memory Bank (memory generation, revisions, profiles, IAM-controlled access), Skill Registry, Agent Identity, Agent Gateway, Managed Agents API, sandbox environment, Feedback service |
| Evaluation | Gen AI evaluation service; "Evaluate agents" documented as a distinct capability |
| Runtime/lifecycle | Agent Platform described as a managed environment for "testing, release management, and reliability at a global scale" |

### Not yet established (historical — all resolved before Table 4 was finalized)

Governance specifics, Operations and monitoring breadth, Platform Management
scope, Developer Experience breadth, and Model Services (Model Garden, routing,
quotas). These require targeted page-level evidence before any rating.

### Method note

Google's documentation pages return their full left-hand navigation to a plain
fetch, so keyword hits can reflect **navigation links rather than page body**.
Ratings must be taken from body text, not from the presence of a nav entry. The
observations above were re-extracted from page bodies for this reason.

---

## B — Microsoft (Foundry, Foundry Control Plane)

Final Table 4 row: **● ● ● ● ● ● ● ● ● ●** (Governance re-rated ◐→● on 24 Sep 2026; the table below is the original assessment)
Changes from baseline: **Agent Services ◐→●, Evaluation ◐→●, Platform
Management ○→●**

Evidence read from page body text, 2026-08-15.

| Domain | Prior | Proposed | Evidence |
|:---|:---:|:---:|:---|
| Developer Experience | ● | ● | Foundry SDK: "A Foundry resource provides unified access to models, agents, and tools"; per-scenario SDK and endpoint guidance |
| AI Runtime | ● | ● | Agent Service: "a managed platform for building, deploying, and scaling AI agents. Use any framework, any supported model from the Foundry model catalog" |
| Model Services | ● | ● | Foundry model catalog with unified endpoint access |
| Knowledge Services | ● | ● | **Foundry IQ** — "the managed knowledge layer that transforms enterprise content into reusable, permission-aware knowledge bases for agents", built on Azure AI Search |
| Agent Services | ◐ | ● | Agent Service plus Control Plane fleet management across multi-agent estates and multiple projects |
| Governance | ◐ | ◐ | Control Plane covers "governance… compliance enforcement"; Content Safety supplies policy. Approval workflows and risk classification not directly evidenced — **see the governance calibration note** |
| Security | ● | ● | **Prompt Shields**: "detects and blocks adversarial user input attacks on large language models… analyzing prompts **and documents** before content is generated" — covers indirect injection; Content Safety text/image APIs |
| Evaluation | ◐ | ● | Observability doc: "robust evaluation frameworks", "integrate automated quality gates into CI/CD pipelines", production monitoring |
| Operations | ● | ● | "You can trace, evaluate… and collect signals such as evaluation metrics, logs, traces, and model outputs to gain visibility into performance, quality, safety, and operational health" — the most explicit AI-specific observability of the four |
| Platform Management | ○ | ● | Control Plane "centralizes management for your AI agent fleet, from build to production" across projects, with fleet management, observability, compliance enforcement and security |

**Note.** Microsoft Learn pages emit an "Access to this page requires
authorization" banner on every page fetched, including SDK and observability.
It is boilerplate, not gating; an earlier concern that the Control Plane page
specifically was access-restricted was wrong.

### Governance calibration — resolved

AWS and Microsoft are both at `◐`, but for non-comparable reasons. AWS's
Registry documents **publishing, review and approval workflows** — that is the
"model, prompt and agent approval" responsibility, met directly. Microsoft
documents **compliance enforcement** — a different responsibility, also met
directly. Neither evidences risk classification. Giving both `◐` may be
defensible, but a reviewer can reasonably ask why documented approval workflows
did not earn credit. Either both rise to `●`, or the `◐` needs a stated
rationale.

**Resolution — rationale stated, ratings unchanged.** The Governance domain
enumerates five responsibilities: policy, approval, risk classification, audit
and compliance. The rubric awards `●` where documented first-party capabilities
address *most* of a domain's responsibilities. AWS evidences policy (Guardrails)
and approval (Registry publishing and review); Microsoft evidences policy
(Content Safety) and compliance enforcement (Control Plane). Neither evidences
risk classification, and neither documents a first-party governance audit record
for the domain as a whole. Two of five responsibilities is not most, so both
remain `◐`. The evidence differs in kind while producing the same rubric
outcome, which answers why documented approval workflows did not by themselves
earn `●`. This is an instance of the rubric asymmetry the paper records in
§XI-B: the substantial threshold is stricter for domains that enumerate more
responsibilities.

## D — IBM (watsonx.ai, watsonx.governance, watsonx Orchestrate)

Final Table 4 row: **● ● ● ◐ ● ● ● ● ● ●** (Evaluation and Operations re-rated ◐→● on 24 Sep 2026; the table below is the original assessment)
Changes from baseline: **Developer Experience ◐→●, AI Runtime ◐→●, Model
Services ◐→●, Agent Services ◐→●, Evaluation ◐→◐ (held), Operations ◐→◐ (held),
Platform Management ○→●**

**Verification provenance differs per cell for this vendor — see the
accessibility note.**

| Domain | Prior | Proposed | Evidence | Verification |
|:---|:---:|:---:|:---|:---|
| Developer Experience | ◐ | ● | Orchestrate ADK "packaged as a Python library and command line tool"; Developer Edition "supports running agents locally on your laptop"; Environments management for importing agents and tools | **content-verified** |
| AI Runtime | ◐ | ● | Goal-driven autonomous agents, tool use, human-in-the-loop workflows that pause, capture context, resume and preserve audit traceability | author-read |
| Model Services | ◐ | ● | IBM and third-party foundation models, custom-model deployment, token-based inference, documented model lifecycle with retirement notice and migration expectations | title-level only |
| Knowledge Services | ● | ◐ ↓ | Vector indexes, RAG pattern, knowledge bases, built-in and external knowledge sources, programmatic vector-index management. No first-party evidence for graph retrieval, citation-returning retrieval, or freshness/versioning across the domain | title-level only |
| Agent Services | ◐ | ● | ADK "supports modular design, multi-agent orchestration, and integration with external tools and frameworks" | **content-verified** |
| Governance | ● | ● | watsonx.governance: "end-to-end monitoring for machine learning and generative AI models… from request to production"; facts from models built with "IBM tools **or third-party providers**" in a single dashboard; OpenPages integration | **content-verified** |
| Security | ● | ● | IAM and access groups, encryption at rest and in motion, customer-managed keys, tenant isolation. AI-specific attack-surface evidence less explicit than AWS or Google | title-level only |
| Evaluation | ◐ | ◐ | Agent evaluation and regression testing, governance monitoring. Domain also requires groundedness, hallucination, relevance, safety, cost and latency, business outcomes — not evidenced as a whole | author-read |
| Operations | ◐ | ◐ | Monitoring in watsonx.governance, agent monitoring and analytics. No evidence of AI-specific traces, prompts, retrieved evidence, tool execution, policy decisions or token/cost telemetry at the breadth the domain requires | author-read |
| Platform Management | ○ | ● | Orchestrate agent control plane: "a centralized operational layer to observe, govern and optimize AI agents across your enterprise, **no matter where they were built or where they run**"; governed catalog, enterprise-wide agent and tool discovery, environments, model lifecycle | **content-verified** (control plane, environments) |

### ⚠ Documentation accessibility is not uniform — threat to validity

IBM's documentation is split across `ibm.com/docs`, `dataplatform.cloud.ibm.com`
and the Orchestrate developer site. The `dataplatform` pages are a JavaScript
single-page application that returns only the app shell to automated retrieval,
so three IBM cells are recorded at title level rather than content-verified,
while AWS, Google and Microsoft cells were read from body text.

This is a measurement asymmetry, not a capability finding. It should be
disclosed in §XI-B alongside the existing snapshot limitation, because a column
assembled from thinner evidence than its neighbors is a reviewable weakness —
and IBM is the vendor whose baseline row carried the most `◐`.

---

## 40-cell evidence register

Every rating with its evidence source, access date and verification provenance,
as promised in §X-A of the manuscript. Provenance is recorded honestly rather
than uniformly:

- **verified** — page body retrieved and the supporting text read directly.
- **author-read** — read by the author in a browser; not re-retrieved here.
- **title-level** — page exists and its title matches the claim, but the body
  could not be retrieved (IBM's `dataplatform` docs are a JavaScript
  single-page application). These three cells rest on the author's reading.

**Evidence strength was not uniform at the original snapshot.** Two
`●` ratings — IBM Model Services and IBM Security — rested on title-level
evidence alone, meaning the cited page existed and was titled as claimed but its
body could not be retrieved for independent confirmation. IBM Knowledge Services
was also title-level, and carries `◐`. The Provenance column records provenance
at the 15 August snapshot; all forty cells, including these three, were
content-verified on 22 September 2026 (see *Evidence re-verification* below).
The Rating column carries the 24 September 2026 re-rating: 36 substantial,
4 partial.

All 40 ratings were assigned by a **single rater** (the author), as disclosed in §XI-B, where single-rater bias is stated as a
threat to validity. The register exists so that
an independent reader can re-derive each rating from the cited source rather
than take the rating on trust.

| Vendor | Capability domain | Rating | Evidence and rationale | Evidence source | Accessed | Provenance |
|:---|:---|:---:|:---|:---|:---|:---|
| Amazon Bedrock | Developer Experience | ● | Bedrock APIs and SDKs across Java, JavaScript, Python/Boto3, Go, .NET, C++, Kotlin; API reference and code examples. AgentCore CLI scaffolding for agents, memory, gateways, credentials, evaluators. | <https://docs.aws.amazon.com/bedrock/latest/userguide/api-reference-overview.html> <br> <https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-get-started-cli.html> | 2026-08-15 | author-read |
| Amazon Bedrock | AI Runtime | ● | AgentCore Runtime: managed serverless agent runtime, session isolation, async execution, multimodal and multi-agent workloads. Harness: orchestration, tool execution, memory management, response generation. | <https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html> | 2026-08-15 | verified |
| Amazon Bedrock | Model Services | ● | Access to many foundation models with documented model swapping; model lifecycle states (Active/Legacy/EOL) exposed via API; token accounting, quotas, provisioned throughput. | <https://docs.aws.amazon.com/bedrock/latest/userguide/model-lifecycle.html> <br> <https://docs.aws.amazon.com/bedrock/latest/userguide/quotas.html> | 2026-08-15 | author-read |
| Amazon Bedrock | Knowledge Services | ● | Knowledge Bases: managed RAG, vector stores, structured data stores, Neptune Analytics GraphRAG; metadata filtering including recency; RetrieveAndGenerate returns citations to source chunks. | <https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html> <br> <https://docs.aws.amazon.com/bedrock/latest/userguide/kb-how-retrieval.html> | 2026-08-15 | author-read |
| Amazon Bedrock | Agent Services | ● | AgentCore Runtime, Harness, Memory (short/long term), Gateway (MCP/tools), Identity, Registry, Evaluations, Observability, multi-agent support, governed tool access. | <https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html> | 2026-08-15 | verified |
| Amazon Bedrock | Governance | ◐ | Against Table 1 (policy, approval rules, risk classification, audit, compliance): **policy** — Guardrails, and AgentCore Policy evaluating Gateway traffic against Cedar policies; **approval** — Registry "control access through an approval workflow". **Audit partial** — Policy decision logs, model invocation logging and CloudTrail reconstruct participants, context and policy decisions, but no first-party record of human involvement (R12). Risk classification and compliance reporting not evidenced; AWS Audit Manager is a separately licensed adjacent service and is excluded. 2 of 5 firm. | <https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html> <br> <https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html> <br> <https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry.html> | 2026-08-15; re-rated 2026-09-24 | verified |
| Amazon Bedrock | Security | ● | Guardrails prompt-injection, jailbreak and prompt-leakage detection; AgentCore Identity with fine-grained access control; Gateway governs tool/service access; IAM and CloudTrail over Bedrock API activity. | <https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-prompt-attack.html> <br> <https://docs.aws.amazon.com/bedrock/latest/userguide/logging-using-cloudtrail.html> | 2026-08-15 | author-read |
| Amazon Bedrock | Evaluation | ● | Bedrock evaluations cover models **and** knowledge bases, plus models and RAG sources *outside* Bedrock; automatic, human and LLM-as-judge evaluation; custom datasets and metrics. AgentCore Evaluations is a purpose-built agent evaluation service operating on sessions, traces and spans. | <https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation.html> | 2026-08-15 | verified |
| Amazon Bedrock | Operations | ● | Model invocation logging to CloudWatch Logs and S3; CloudWatch metrics including token and cache usage; AgentCore Observability with traces, workflow-step visualization, latency, token usage, errors, OTEL-compatible telemetry. | <https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html> <br> <https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html> | 2026-08-15 | author-read |
| Amazon Bedrock | Platform Management | ● | Against Table 1 (tenancy, configuration, deployment, versioning, release, catalog, lifecycle evolution): **versioning** — "Each update to the AgentCore Runtime creates a new version with a complete, self-contained configuration"; "Versions are immutable once created"; **release** — "Endpoints can point to specific versions, allowing you to maintain different environments (e.g., development, staging, production)"; **deployment** — AgentCore Runtime; **configuration** — per-version configuration, quotas; **catalog** — Registry "a centralized catalog for organizing, curating, and discovering resources across your organization"; **lifecycle evolution** — model Active/Legacy/EOL states. **Tenancy partial** — per-session microVM isolation, no platform tenancy construct. 6 of 7 firm. Originally ◐ against responsibilities (feature management, roadmap, platform metrics) that are not in Table 1. | <https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agent-runtime-versioning.html> <br> <https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry.html> <br> <https://docs.aws.amazon.com/bedrock/latest/userguide/model-lifecycle.html> | 2026-08-15; re-rated 2026-09-24 | verified |
| Microsoft Foundry | Developer Experience | ● | Foundry SDK: "A Foundry resource provides unified access to models, agents, and tools"; per-scenario SDK and endpoint guidance | <https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/sdk-overview> | 2026-08-15 | verified |
| Microsoft Foundry | AI Runtime | ● | Agent Service: "a managed platform for building, deploying, and scaling AI agents. Use any framework, any supported model from the Foundry model catalog" | <https://learn.microsoft.com/en-us/azure/foundry/agents/overview> | 2026-08-15 | verified |
| Microsoft Foundry | Model Services | ● | Foundry model catalog with unified endpoint access | <https://learn.microsoft.com/en-us/azure/foundry/agents/overview> | 2026-08-15 | verified |
| Microsoft Foundry | Knowledge Services | ● | **Foundry IQ** — "the managed knowledge layer that transforms enterprise content into reusable, permission-aware knowledge bases for agents", built on Azure AI Search | <https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview> | 2026-08-15 | verified |
| Microsoft Foundry | Agent Services | ● | Agent Service plus Control Plane fleet management across multi-agent estates and multiple projects | <https://learn.microsoft.com/en-us/azure/foundry/agents/overview> <br> <https://learn.microsoft.com/en-us/azure/foundry/control-plane/overview> | 2026-08-15 | verified |
| Microsoft Foundry | Governance | ● | Against Table 1: **policy** — Control Plane: "Define enterprise-wide guardrail policies for safety, compliance, and quality"; **compliance** — "Monitor compliance posture in real time, so that you can surface noncompliant assets and enable bulk remediation"; **approval** — built-in policy "[Preview]: Azure Machine Learning Deployments should only use approved Registry Models", restricting deployments to an approved list. **Audit partial** — "Apply versioned policies and track assignments to maintain full auditability and traceability across agents and environments"; the fuller AI-interaction audit requires Microsoft Purview, a separately licensed adjacent product, which is excluded. Risk classification not evidenced. 3 of 5 firm. | <https://learn.microsoft.com/en-us/azure/foundry/control-plane/overview> (ms.date 2026-05-06) <br> <https://learn.microsoft.com/en-us/azure/foundry-classic/how-to/built-in-policy-model-deployment> (ms.date 2026-02-02) | 2026-08-15; re-rated 2026-09-24 | verified |
| Microsoft Foundry | Security | ● | **Prompt Shields**: "detects and blocks adversarial user input attacks on large language models… analyzing prompts **and documents** before content is generated" — covers indirect injection; Content Safety text/image APIs | <https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/jailbreak-detection> | 2026-08-15 | verified |
| Microsoft Foundry | Evaluation | ● | Observability doc: "robust evaluation frameworks", "integrate automated quality gates into CI/CD pipelines", production monitoring | <https://learn.microsoft.com/en-us/azure/foundry/concepts/observability> | 2026-08-15 | verified |
| Microsoft Foundry | Operations | ● | "You can trace, evaluate… and collect signals such as evaluation metrics, logs, traces, and model outputs to gain visibility into performance, quality, safety, and operational health" — the most explicit AI-specific observability of the four | <https://learn.microsoft.com/en-us/azure/foundry/concepts/observability> | 2026-08-15 | verified |
| Microsoft Foundry | Platform Management | ● | Control Plane "centralizes management for your AI agent fleet, from build to production" across projects, with fleet management, observability, compliance enforcement and security | <https://learn.microsoft.com/en-us/azure/foundry/control-plane/overview> | 2026-08-15 | verified |
| Google Vertex AI | Developer Experience | ● | Gen AI SDK: "unified interface" across the Gemini Developer API and Agent Platform; code portable between them "without rewriting your code". Model Garden discover/test/customize/deploy. Colab, Colab Enterprise, Workbench notebooks; GitHub samples. | <https://cloud.google.com/vertex-ai/generative-ai/docs/sdks/overview> | 2026-08-15 | verified |
| Google Vertex AI | AI Runtime | ● | Agent Runtime (managed, serverless); Sessions provide execution state; Agent Gateway; asynchronous and bidirectional streaming. | <https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview> | 2026-08-15 | verified |
| Google Vertex AI | Model Services | ◐ | Against Table 1 (registry, provider abstraction, routing, quota, fallback, consumption accounting): **registry** — Model Garden "helps you discover, test, customize, and deploy models and assets from Google and Google partners"; **quota** — documented quotas and system limits for generative AI models, adjustable on request; **consumption accounting** — model observability metrics from which "you can also estimate costs for running each model". **Provider abstraction partial** — the OpenAI-compatible Chat Completions endpoint serves Gemini and several partner and open models, but Claude uses Anthropic's native format; the same endpoint is not the same interface. **Routing partial** — regional routing through the global endpoint only; the Model Optimizer page was withdrawn before the snapshot. **Fallback partial** — client retry on the same model; Provisioned Throughput overflow is a billing fallback, not a model fallback. API Gateway model routing (Preview, 3 Aug 2026) is a separately billed product documented outside the Agent Platform and is excluded under the inclusion rule. 3 of 6 firm — exactly half, so ◐. | <https://docs.cloud.google.com/vertex-ai/generative-ai/docs/model-garden/explore-models> <br> <https://docs.cloud.google.com/vertex-ai/generative-ai/docs/quotas> <br> <https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-partner-models> | 2026-08-15; re-rated 2026-09-24 | verified |
| Google Vertex AI | Knowledge Services | ● | Against Table 1 (ingestion, indexing, refresh, structured, vector and graph retrieval, metadata filtering, attribution and citation): **ingestion** — "Ingest data from different data sources. For example, local files, Cloud Storage, and Google Drive"; **indexing** — "RAG Engine creates an index called a corpus"; **refresh** — incremental re-import skips a file when "The file has already been imported. The file hasn't changed"; **vector** — RagManagedDb, Vector Search, Pinecone and others; **metadata filtering** — `filter.metadata_filter` "using Common Expression Language (CEL)" (Preview); **citation** — "A successful response returns the generated content with citations." Graph retrieval absent (Spanner GraphRAG is an Architecture Center pattern, not a feature); structured retrieval only through the separately branded Agent Search, not credited. 6 of 8 firm. The original "no citation support found" was a retrieval error. | <https://docs.cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-overview> <br> <https://docs.cloud.google.com/vertex-ai/generative-ai/docs/model-reference/rag-api> | 2026-08-15; re-rated 2026-09-24 | verified |
| Google Vertex AI | Agent Services | ● | Memory Bank (generation, revisions, profiles, IAM-scoped access), Sessions, Skill Registry, Agent Identity, Managed Agents API, sandbox environment, Agent2Agent, first-party ADK. | <https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview> | 2026-08-15 | verified |
| Google Vertex AI | Governance | ◐ | Against Table 1: **policy** — Model Armor; **approval** — the `vertexai.allowedModels` organization policy restricts users to an approved model set (credited on the same basis as Foundry's approved-models policy). **Audit partial** — Data Access audit logs (disabled by default) and Model Armor interceptions in traces; no record of human involvement. **Compliance partial** — the compliance widget depends on Security Command Center Premium/Enterprise, a separately licensed product, excluded. Risk classification not evidenced (SCC "AI risks by severity" ranks security posture, not AI use cases). 2 of 5 firm. | <https://cloud.google.com/security-command-center/docs/model-armor-overview> <br> <https://docs.cloud.google.com/vertex-ai/generative-ai/docs/control-model-access> | 2026-08-15; re-rated 2026-09-24 | verified |
| Google Vertex AI | Security | ● | Model Armor screens LLM prompts and responses, prevents malicious input, verifies content safety, protects sensitive data — including across other cloud providers. CMEK, VPC-SC, IAM, Agent Identity. | <https://cloud.google.com/security-command-center/docs/model-armor-overview> | 2026-08-15 | verified |
| Google Vertex AI | Evaluation | ● | **Resolved 2026-08-15.** Canonical page: *Gen AI evaluation service overview* — "Gemini Enterprise Agent Platform provides evaluation for agents, predictive AI models, and generative AI models… The Gen AI evaluation service provides enterprise-grade tools for objective, data-driven assessment of generative AI models", supporting model migrations, prompt editing and fine-tuning. Separate agent-evaluation and model-evaluation paths documented. | <https://cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-overview> | 2026-08-15 | verified |
| Google Vertex AI | Operations | ● | *Agent observability*: "comprehensive visibility into the performance, behavior, and health of your deployed agents and MCP servers", with telemetry sent "in the OpenTelemetry format"; *Traces*: distributed tracing via Cloud Trace, Cloud Logging and Telemetry APIs, where a trace comprises spans representing "a function call or an interaction with an LLM". Request-response logging to BigQuery is additionally available (Preview). | <https://docs.cloud.google.com/gemini-enterprise-agent-platform/optimize/observability/overview> <br> <https://docs.cloud.google.com/gemini-enterprise-agent-platform/optimize/observability/traces> | 2026-08-15 | verified |
| Google Vertex AI | Platform Management | ● | Against Table 1: **deployment** — deploy an agent to Agent Runtime; **configuration** — agent environment variables via `env_vars=`, project-level RagEngineConfig; **versioning** — "A model alias is a mutable, named reference to a model version"; **catalog** — Model Garden "helps you discover, test, customize, and deploy models", Agent Registry (GA 18 Jun 2026); **lifecycle evolution** — published retirement dates that "won't be moved to an earlier date than what is listed". **Release partial** — revision traffic splitting is Preview with no established launch date, not credited. **Tenancy partial** — Architecture Center guidance only. 5 of 7 firm. Originally ◐ against responsibilities not in Table 1. | <https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/deploy-an-agent> <br> <https://docs.cloud.google.com/vertex-ai/docs/model-registry/model-alias> <br> <https://docs.cloud.google.com/vertex-ai/generative-ai/docs/model-garden/explore-models> <br> <https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/model-versions> | 2026-08-15; re-rated 2026-09-24 | verified |
| IBM watsonx | Developer Experience | ● | Orchestrate ADK "packaged as a Python library and command line tool"; Developer Edition "supports running agents locally on your laptop"; Environments management for importing agents and tools | <https://www.ibm.com/docs/en/watsonx/watson-orchestrate/base?topic=agents-building-using-adk> <br> <https://developer.watson-orchestrate.ibm.com/> | 2026-08-15 | verified |
| IBM watsonx | AI Runtime | ● | Goal-driven autonomous agents, tool use, human-in-the-loop workflows that pause, capture context, resume and preserve audit traceability | <https://www.ibm.com/docs/en/watsonx/watson-orchestrate/base?topic=agents-building-using-adk> | 2026-08-15 | author-read |
| IBM watsonx | Model Services | ● | IBM and third-party foundation models, custom-model deployment, token-based inference, documented model lifecycle with retirement notice and migration expectations | <https://dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/fm-models.html?context=wx> | 2026-08-15 | title-level |
| IBM watsonx | Knowledge Services | ◐ | Against Table 1: **ingestion** — knowledge-base document upload; **indexing** — built-in Milvus and watsonx.ai vector indexes; **vector retrieval** — Milvus, Elasticsearch and other stores; **citation** — "Use the citations_shown parameter to control how many citations appear during the interaction". **Metadata filtering partial** — a `filter` field in the configuration of an externally hosted store, not a platform filter; **refresh partial** — re-import only. Graph and structured retrieval not evidenced in admissible documentation. 4 of 8 firm. The original rationale's "no citation-returning retrieval" is withdrawn; the rating holds. | <https://developer.watson-orchestrate.ibm.com/knowledge_base/build_kb> <br> <https://www.ibm.com/docs/en/watsonx/saas?topic=data-retrieval-augmented-generation> (since moved to `?topic=solutions-retrieval-augmented-generation`) | 2026-08-15; re-rated 2026-09-24 | verified |
| IBM watsonx | Agent Services | ● | ADK "supports modular design, multi-agent orchestration, and integration with external tools and frameworks" | <https://www.ibm.com/docs/en/watsonx/watson-orchestrate/base?topic=agents-building-using-adk> | 2026-08-15 | verified |
| IBM watsonx | Governance | ● | watsonx.governance: "end-to-end monitoring for machine learning and generative AI models… from request to production"; facts from models built with "IBM tools **or third-party providers**" in a single dashboard; OpenPages integration | <https://www.ibm.com/docs/en/watsonx/saas?topic=governing-ai> | 2026-08-15 | verified |
| IBM watsonx | Security | ● | IAM and access groups, encryption at rest and in motion, customer-managed keys, tenant isolation. AI-specific attack-surface evidence less explicit than AWS or Google | <https://dataplatform.cloud.ibm.com/docs/content/wsj/getting-started/security-overview.html?context=wx> | 2026-08-15 | title-level |
| IBM watsonx | Evaluation | ● | Against Table 1 (offline and online evaluation, correctness, groundedness, safety, outcomes): **offline** — the ADK evaluation framework assesses agent behavior "by comparing simulated agent interactions, referred to as trajectories, against a predefined set of reference data"; **online** — "Agentic runtime monitoring provides a governance capability for agentic AI services that run in production environments" (GA 11 Dec 2025); **correctness** — Text Match, Tool Call Precision/Recall, answer similarity; **groundedness** — Faithfulness, Answer relevance, Context relevance; **safety** — Input/Output HAP, Input/Output PII, Prompt safety risk; **outcomes** — Journey Success (task-level, not business KPIs). 6 of 6. Originally ◐ on a product page that names no metric. | <https://developer.watson-orchestrate.ibm.com/evaluate/overview> <br> <https://developer.watson-orchestrate.ibm.com/evaluate/evaluate> <br> <https://www.ibm.com/docs/en/watsonx/saas?topic=models-evaluating-agents-agentic-applications> | 2026-08-15; re-rated 2026-09-24 | verified |
| IBM watsonx | Operations | ● | Against Table 1 (tracing, logging, AI-specific execution telemetry, policy and evaluation signals, provenance, cost and capacity): **tracing** — runtime monitoring "continuously collects execution traces"; ADK traces "visualize the complete path a request takes through the agent" (ADK 2.5.0, 27 Feb 2026); **logging** — activity tracking events "to report on activities that change the state of a service", including `agent-release.create` and `tool.run`; **AI telemetry** — input and output token count, tool call accuracy, conversation duration; **policy and evaluation signals** — evaluation metrics and HAP/PII guardrail detections feed watsonx.governance dashboards and alerts (runtime monitoring GA 11 Dec 2025). **Cost and capacity partial** — throughput and latency are documented in model health monitoring, but the "Estimated cost" metric cannot be dated before the snapshot, and the FinOps cost dashboard is post-snapshot (late Aug 2026); **provenance partial**. 4 of 6 firm. Policy-enforcement spans in traces (Sep 2026) are excluded. Originally ◐ on a product page. | <https://www.ibm.com/docs/en/watsonx/saas?topic=models-evaluating-agents-agentic-applications> <br> <https://developer.watson-orchestrate.ibm.com/traces/overview> <br> <https://www.ibm.com/docs/en/watsonx/watson-orchestrate/base?topic=logs-list-events-activity-tracking> | 2026-08-15; re-rated 2026-09-24 | verified |
| IBM watsonx | Platform Management | ● | Orchestrate agent control plane: "a centralized operational layer to observe, govern and optimize AI agents across your enterprise, **no matter where they were built or where they run**"; governed catalog, enterprise-wide agent and tool discovery, environments, model lifecycle | <https://www.ibm.com/products/watsonx-orchestrate/agent-control-plane> | 2026-08-15 | verified |

---

## Evidence re-verification — 22 September 2026

**Original assessment snapshot: 15 August 2026.** The 40-cell register above, its
ratings, rubric and access dates are unchanged by this pass and remain the
assessment of record.

Three IBM watsonx cells were originally recorded at **title level** because the
`dataplatform.cloud.ibm.com` pages are a JavaScript single-page application that
returns only the app shell to automated retrieval. Those pages still behave that
way. The same content is, however, mirrored statically under `ibm.com/docs`, and
the three cells were re-verified there on 22 September 2026.

This pass strengthens evidence provenance. It did not change any rating, so the
headline result stands at 31 substantial, 9 partial, 0 limited.

| Cell | Original | Re-verified | Rating |
|:---|:---|:---|:---|
| IBM watsonx / Model Services | title-level | content-verified | ● unchanged |
| IBM watsonx / Knowledge Services | title-level | content-verified | ◐ unchanged |
| IBM watsonx / Security | title-level | content-verified, with the qualification in §R3 | ● unchanged |

### R1 — Model Services (●)

All four elements of the original rationale are now supported by body text.

- IBM and third-party models: *"You can work with third-party and IBM foundation
  models in IBM watsonx.ai."*
  <https://www.ibm.com/docs/en/watsonx/saas?topic=solutions-supported-foundation-models>
- Token-based inference: per-1,000-token input and output rates are tabulated for
  each model on the same page.
- Custom-model deployment: documented separately at
  <https://www.ibm.com/docs/en/watsonx/saas?topic=assets-deploying-custom-foundation-model>.
  It is **not** on the originally cited page, which is why the first re-check
  returned nothing for it.
- Lifecycle with notice and migration expectation: *"older versions remain
  available for you to use for at least 90 days after an updated model is
  introduced"*; *"You are given at least 90 days notice before foundation models
  from third-party providers are removed from watsonx.ai"*; *"You must choose an
  alternative supported foundation model to use if any of the following saved
  resources submit input to a foundation model that is withdrawn."*
  <https://www.ibm.com/docs/en/watsonx/saas?topic=models-foundation-model-lifecycle>

### R2 — Knowledge Services (◐)

Both halves of the original rationale are confirmed, the negative half included,
which is what holds this cell at ◐ rather than ●.

- Present: vector indexes, RAG, knowledge bases, external vector stores (Milvus,
  Elasticsearch, Chroma) and programmatic index creation.
- Absent: graph retrieval, citation-returning retrieval, and index
  freshness/refresh/versioning. None is documented.
  <https://www.ibm.com/docs/en/watsonx/saas?topic=data-retrieval-augmented-generation>
  (IBM has since moved this page to
  <https://www.ibm.com/docs/en/watsonx/saas?topic=solutions-retrieval-augmented-generation>,
  checked 2026-09-26.)
- *Superseded in part on 24 September 2026:* citation-returning retrieval **is**
  documented, for watsonx Orchestrate knowledge bases (`citations_shown`); see the
  register row for this cell. Refresh is documented only as re-import. Graph and
  structured retrieval remain absent, so the rating stays ◐.

### R3 — Security (●), with a recorded qualification

Conventional security is confirmed verbatim: *"at rest data (data that is stored)
is encrypted with randomly generated keys that are managed by IBM"*; *"Encryption
methods such as HTTPS, SSL, and TLS are used to protect data in motion"*; *"you
can create and manage your own keys with the IBM Key Protect service"*; and IAM
over storage access.
<https://www.ibm.com/docs/en/watsonx-as-a-service?topic=security-data>

Two findings this pass added to the record.

**A plan restriction not previously noted.** *"Custom encryption keys can be used
with the watsonx.ai Studio Professional plan only."* The rubric scores documented
first-party capability coverage rather than availability on every commercial
tier, so this is recorded in the evidence rather than treated as a downgrade.

**AI-specific controls are documented, but not on the security pages.** The data
security page addresses no AI-specific attack surface. The controls exist in the
governance and model documentation, which is in scope: the vendor mapping assesses
IBM as watsonx.ai, watsonx.governance and watsonx Orchestrate together.

- PII, harm and HAP detectors, configurable over model input and output:
  <https://www.ibm.com/docs/en/watsonx/w-and-w/2.2.0?topic=content-configuring-ai-guardrails-in-watsonxgovernance>
- Jailbreaking named and defined as a detected risk — *"deliberate instances of
  manipulating AI to generate harmful, undesired, or inappropriate content"* —
  alongside social bias, violence, profanity, unethical behaviour and, for agentic
  workflows, function-calling hallucination:
  <https://www.ibm.com/docs/en/watsonx/w-and-w/2.1.0?topic=models-granite-guardian-30-8b-model-card>

Against R6's four surfaces the coverage is uneven, and the rating is held at ●
with that stated: sensitive-data exposure and model abuse are directly covered;
**prompt injection is not named as a distinct control**, with jailbreaking the
nearest documented equivalent; and tool misuse is only indirectly addressed,
through function-calling hallucination as a detected risk rather than through
enforced tool permissions.

Two caveats on this sub-pass. The AI-specific evidence comes from the `w-and-w`
software-edition documentation and a model card, not the SaaS pages the other IBM
cells cite; the SaaS guardrails detail page could not be retrieved in either form.
And IBM's `think/` explainer and announcement pages were excluded throughout —
they describe the threats rather than document a first-party control.

### R4 — The nine author-read cells, content-verified

The 22 September pass was extended to the nine cells whose original provenance
was **author-read** — read in a browser at assessment time but not independently
re-retrieved. All nine were re-retrieved and read at body level. **No rating
changed.** With the three title-level cells above, all forty cells are now
content-verified and the headline stands at 31 substantial, 9 partial, 0 limited.

| Cell | Outcome |
|:---|:---|
| Bedrock / Developer Experience ● | confirmed — SDKs for C++, Go, Java, JavaScript, Kotlin, .NET, Python/Boto3 named, with API reference and code examples |
| Bedrock / Model Services ● | confirmed — Active, Legacy and End-of-Life states, exposed in the `modelLifecycle` field of `GetFoundationModel` and `ListFoundationModels`; migration required before EOL and *"will not happen automatically"* |
| Bedrock / Knowledge Services ● | confirmed — `RetrieveAndGenerate` *"Includes citations to specific source chunks from the data"*; `GenerateQuery` for structured stores; reranking |
| Bedrock / Governance ◐ | confirmed both ways — content filters, denied topics, word filters, sensitive information filters, contextual grounding and Automated Reasoning checks are documented; risk classification, usage-policy management and compliance reporting are not |
| Bedrock / Security ● | confirmed — Jailbreaks, Prompt Injection and Prompt Leakage each named and defined, with Block or Detect actions. See the two qualifications below |
| Bedrock / Operations ● | confirmed — invocation logs to CloudWatch Logs and Amazon S3, carrying `input.inputTokenCount`, `output.outputTokenCount`, `identity.arn` and request metadata |
| watsonx / AI Runtime ● | partly confirmed — see the correction below |
| watsonx / Evaluation ◐ | confirmed — *"comprehensive evaluation framework to validate agent behavior, identify regressions"*, with no evaluation dimension named, which is what holds the cell at partial |
| watsonx / Operations ◐ | confirmed — real-time performance, cost and audit claims, with no AI-specific traces, prompts, retrieved evidence, tool-execution records, policy decisions or token-level cost telemetry documented |

#### Corrections and qualifications this pass produced

**watsonx / AI Runtime — the rationale overstates its evidence.** Goal-driven
agents and tool use are documented, and human-in-the-loop is documented in the
Orchestrate ADK material (*"Human-in-the-loop interaction is needed for approvals
or decision-making"*, with user-activity nodes that require user input). But
*"capture context, resume and preserve audit traceability"*, as the original
rationale puts it, is **not** documented: the ADK material describes no
suspension-and-resumption mechanics, no state persistence across a human step,
and no approval audit trail. Those words come from IBM's announcement and product
pages, which are excluded as evidence here. The rating is held at ● on agents,
tool use and human-in-the-loop; the audit-traceability element of the rationale is
withdrawn.

**Bedrock / Security — two qualifications now on the record.** Prompt Leakage
detection is *"Standard tier only"*. More materially for R6, the prompt-attack
filter has a documented scope limit: *"The prompt attack filter does not evaluate
tool results. Content in `messages[].content[].toolResult` is not assessed for
prompt attacks, and neither are the tool definitions in
`toolConfig.tools[].toolSpec`."* That is precisely the indirect-prompt-injection
and tool-misuse surface R6 names, so the ● rests on direct prompt attacks rather
than the full surface.

**Two watsonx cells are evidenced by product pages, not documentation.**
Evaluation and Operations cite `ibm.com/products/...`, which is marketing
material. Both cells are partial, and both rationales turn on what is *absent*,
so the weaker source class does not inflate either rating — a marketing page that
declines to name a metric is reasonable evidence that the metric is not
documented. It is recorded because it is a different provenance weakness from the
title-level problem and it affects two further cells.

**Bedrock model-lifecycle documentation changed after the snapshot.** The page now
states the policy for models launched *"on or after September 7, 2026"*, with
earlier models covered by a separate legacy page. The three lifecycle states and
their API exposure are unchanged, so the rating is unaffected, but this is a
concrete instance of the volatility the manuscript's snapshot limitation
describes, and a reason the 15 August assessment is retained rather than replaced.

#### Evidence provenance after this pass

| | Original snapshot | After re-verification |
|:---|---:|---:|
| Content-verified | 28 | **40** |
| Author-read | 9 | 0 |
| Title-level | 3 | 0 |

The rubric, the ratings and the 15 August access dates are unchanged. Only the
strength of the evidence behind them has changed.

## Re-rating — 24 September 2026

**Snapshot unchanged: 15 August 2026.** This is a correction to the scoring
under the rubric already fixed, not a new assessment. Each cell was re-scored
by counting, responsibility by responsibility, the principal responsibilities
listed for its domain in **Table 1** of the manuscript. A cell was raised only
where the supporting capability is documented in admissible sources **and**
existed by the snapshot date, as shown by page dates, release notes or dated
announcements (announcements were used for dating only, never as evidence of
capability). Features documented as launching after 15 August were excluded.

### Why the original ratings were too low

Two causes, neither a finding about the vendors.

1. **Scoring against an earlier domain definition.** Several rationales cited
   responsibilities that Table 1 does not list — "feature management, platform
   releases, platform metrics and roadmap" for Platform Management, "usage
   policy" for Governance, an eight-responsibility list for Agent Services. The
   rubric-asymmetry note above said Governance listed six responsibilities and
   Platform Management nine; Table 1 lists five and seven.
2. **Weaker or mistaken evidence.** watsonx Evaluation and Operations rested on
   product pages that name no metric; Vertex AI Knowledge Services recorded "no
   citation support found", which was a retrieval error.

### Counting rules, stated so the re-score is mechanical

- **Most** means more than half of the Table 1 responsibilities.
- Only **firmly documented** responsibilities count toward "most". A partial
  one — present but narrower than the responsibility, or dependent on an
  excluded product — is recorded and not counted.
- The **inclusion rule** and the Preview rule in *What the ratings measure*
  apply to every vendor.

### Cells changed (◐ → ●)

| Cell | Firm / listed | Firm | Partial or absent | Pre-snapshot dating |
|:---|:---:|:---|:---|:---|
| Microsoft Foundry / Governance | 3 / 5 | policy, compliance, approval (approved-models policy) | audit partial without Purview; risk classification absent | Control Plane overview ms.date 2026-05-06; approved-models policy page ms.date 2026-02-02 |
| Amazon Bedrock / Platform Management | 6 / 7 | versioning, release, deployment, configuration, catalog, lifecycle evolution | tenancy partial | AgentCore Runtime versioning since the 2025 preview; Registry public preview April 2026 |
| Google Vertex AI / Knowledge Services | 6 / 8 | ingestion, indexing, refresh, vector, metadata filtering, citation | graph absent; structured only via Agent Search, not credited | RAG API citation and incremental-import text present in a 12 Mar 2026 archive capture; metadata search in an 11 Apr 2026 capture* |
| Google Vertex AI / Platform Management | 6 / 7 | deployment, configuration, versioning, release, catalog, lifecycle evolution | tenancy partial. Release was first recorded as undated; the release notes date revision traffic splitting to public preview on 19 May 2026 | Model Registry aliases, Model Garden and the model-versions page predate 2026; Agent Registry GA 18 Jun 2026 |
| IBM watsonx / Evaluation | 6 / 6 | offline, online, correctness, groundedness, safety, outcomes | outcomes is task-level (Journey Success), not business KPIs | agent runtime monitoring GA 11 Dec 2025 (IBM announcement, used for dating) |
| IBM watsonx / Operations | 4 / 6 | tracing, logging, AI-specific telemetry, policy and evaluation signals | cost and capacity partial (Estimated cost undated; FinOps dashboard post-snapshot); provenance partial | runtime monitoring GA 11 Dec 2025; ADK traces from ADK 2.5.0, 27 Feb 2026 (an earlier version of this row misdated ADK 2.14.0) |

\* The archive captures were reported by the verification pass; they could not
be re-fetched on 24 September because the Wayback Machine rate-limited the
request. The quoted text was confirmed verbatim on the live pages.

### Cells held at ◐, with the reason on the record

| Cell | Firm / listed | Firm | Why not ● |
|:---|:---:|:---|:---|
| Amazon Bedrock / Governance | 2 / 5 | policy (Guardrails, AgentCore Policy), approval (Registry approval workflow) | audit partial — no first-party record of human involvement; risk classification and compliance reporting absent; Audit Manager excluded |
| Google Vertex AI / Governance | 2 / 5 | policy (Model Armor), approval (`vertexai.allowedModels`) | audit partial; compliance depends on Security Command Center, excluded; risk classification absent |
| IBM watsonx / Knowledge Services | 4 / 8 | ingestion, indexing, vector, citation | metadata filtering is a field of an externally hosted store's configuration, not a platform filter; refresh is re-import only; graph and structured retrieval absent |

Foundry Governance and the two hyperscaler Governance cells now differ on a
stated ground: Foundry documents compliance posture monitoring and remediation
natively in the Control Plane, while AWS and Google document compliance only
through separately licensed products.

### Cell lowered (● → ◐)

| Cell | Firm / listed | Firm | Partial or absent |
|:---|:---:|:---|:---|
| Google Vertex AI / Model Services | 3 / 6 | registry, quota, consumption accounting | provider abstraction partial (Claude outside the common interface); routing partial (regional only); fallback partial (same-model retry). API Gateway model routing excluded under the inclusion rule |

The original ● rested on Model Garden, model lifecycle and quotas, which cover
registry, quota and consumption accounting only. Provider abstraction, routing
and fallback are the responsibilities through which Model Services discharges
R1, so the lower rating is substantive rather than clerical.

### Verification of the other ● cells

All forty cells have now been counted against Table 1 under the counting rules
above. The first pass counted the cells in question and some neighbours; a
second pass on 24 September 2026, one agent per vendor, counted the rest.
Every ● other than Vertex AI Model Services held:

| Platform | Counts (firm / listed) |
|:---|:---|
| Bedrock | Developer Experience 5/5, AI Runtime 6/6, Model Services 5/6 (fallback partial), Security 6/7, Agent Services 5/5, Knowledge Services 8/8, Evaluation 6/6, Operations 5/6 |
| Foundry | Developer Experience 5/5, AI Runtime 6/6, Model Services 6/6, Security 7/7, Agent Services 3/5 (thinnest), Knowledge Services 6/8, Evaluation 6/6, Operations 5/6, Platform Management 7/7 |
| Vertex AI | Developer Experience 5/5, AI Runtime 6/6, Security 6/7, Agent Services 5/5, Evaluation 6/6 |
| watsonx | Developer Experience 5/5, AI Runtime 6/6, Model Services 5/6 (quota partial), Security 6/7, Agent Services 5/5, Governance 5/5, Platform Management 7/7 |

Corrections this pass made to earlier notes:
- **Vertex AI Runtime:** human approval *is* documented (ADK 2.0 human-input
  nodes, GA 19 May 2026, on `adk.dev`). Retry and fallback are not AI Runtime
  responsibilities in Table 1.
- **Vertex AI Agent Services:** the matrix note that "planning is first-party
  via ADK" is supported by `adk.dev` rather than the cloud-domain pages. From
  cloud-domain pages alone the count is 3/5, still ●.
- **Bedrock:** fallback is not documented as model or provider failover. The
  prompt router's "fallback model" is a quality anchor, and AWS leaves Regional
  failover to the customer. The manuscript should not claim fallback for AWS,
  and does not.
- **Bedrock Operations:** CloudWatch and CloudTrail are treated as the
  platform's own telemetry base, not as excluded adjacent products. AgentCore
  Observability is documented as "powered by Amazon CloudWatch".

**Addendum (25 September 2026) — Vertex AI Operations count.** The table above
omits one cell: Google Vertex AI / Operations was never given a firm/listed count,
although the text says all forty were counted. Counted now from the evidence
already in its register row, not re-read from the live pages: **4 / 6** — tracing
(Cloud Trace), logging (Cloud Logging), AI-specific execution telemetry (spans for
LLM interactions, OpenTelemetry format), provenance (request-response logging to
BigQuery, Preview, admissible under the Preview rule). Policy and evaluation
signals and cost and capacity are not evidenced in the row. More than half, so
**● holds** and the 36 / 4 total is unchanged. With this cell, every one of the
forty ratings now has a recorded count.

The watsonx Platform Management rationale no longer depends on the marketing
page it cited. Environments, draft-to-live deployment, agent versions, the
Discover catalog and the foundation-model lifecycle are all documented in
admissible sources.

### Evidence excluded as post-snapshot

- IBM ADK `orchestrate controls` (2.15.0, 17 Aug 2026).
- IBM ADK agent-version CLI (2.17.0, 15 Sep 2026).
- IBM custom LLM-as-a-judge and Trace Inspector (GA 17 Aug 2026).
- IBM model-control enforcement spans in traces (September 2026).
- Google IAM Unified Access Policies (GA 31 Aug 2026).
- Azure SQL knowledge source for Foundry IQ (2026-08-01-preview API).
- The revised Bedrock model-lifecycle policy (models launched on or after
  7 Sep 2026).

### Agent reasoning finding — resolved

The Agent Services note above says AWS delegates planning and reflection to
third-party frameworks. The re-check found both documented first-party before
the snapshot:

- AgentCore Harness is "a managed agent loop" (preview April 2026, GA June 2026).
- Episodic memory "generates reflections" (December 2025).

The Bedrock ● is unaffected, since the cell is now 5 of 5. But the manuscript's
§10.1 contrast ("agent reasoning is delegated to third-party frameworks by one
vendor and supplied first-party by another"), Alternative B's substitutability
reasoning and F2's packaging example all rested on that delegation. All three
were corrected in the same pass. §10.1 drops the example and keeps the
cost-placement one. Alternative B now rests on the Table 1 responsibilities,
with AWS evidenced as offering both first-party and third-party agent
realizations over one runtime. F2's example is replaced, and its result is
unchanged, for the reason given in `falsification-assessment.md` §3.1.

### Consequence for Table 2

Alternative D (absorb Platform Management into Operations) was rejected partly
because the register showed the two domains dissociating in opposite directions
across three platforms. After this re-rating all four platforms are ● on both,
so that evidence no longer exists. `alternative-decompositions.md` and Table 2
now record assessment as not discriminating for Alternative D. It remains
rejected, on substitutability.

## Falsification observations from this comparison

Recorded in full in `falsification-assessment.md`; summarised here because both
observations arise from these forty cells.

- **F1, completeness — not met.** All forty ratings were assigned without
  widening any domain definition, and no platform documented a first-party
  responsibility that had no architectural home. Note the direction of the test:
  it ran from vendor documentation *to* the domains, so it shows the domains
  absorb what vendors document. It does not test the converse — whether the
  domains demand responsibilities that no platform provides.
- **F2, boundaries — not met, with one exception.** The packaging differences
  visible across these cells (agent orchestration offered as a first-party
  managed loop and through third-party frameworks on one runtime by one vendor,
  and through its own kit by another; platform management as a fleet control
  plane in two platforms and as registry, versioning and quota APIs in the
  others) follow each vendor's commercial surface rather than disputing the
  proposed boundaries. The exception is **cost placement**: one platform treats
  cost as an input to routing, another as an observability concern reported
  afterwards. No single cell here turns on that, so it is a reading across the
  documentation rather than a rating that can be checked line by line, and its
  corroboration is internal — finding B3 in `requirements-traceability.md`
  records the same dual ownership inside the architecture itself.

## Finding: the neutrality claim needs qualifying

Two manuscript passages assert that vendor architectures cannot span providers.
The evidence contradicts both.

**§2.2:** "an architecture expressed in one provider's services **cannot** be
used to reason about a portfolio spanning several, which is the common
enterprise condition."

**§XI-C:** "the capability model can describe a portfolio spanning several
providers, **which no single vendor architecture can**."

Against this:

- IBM watsonx.governance collects facts about models built with "IBM tools **or
  third-party providers**", and the Orchestrate control plane governs agents "no
  matter where they were built or where they run".
- Google Model Armor enforces AI safety and security policies "whether you are
  deploying AI in Google Cloud **or other cloud providers**".

Proposed revision: **no single vendor architecture provides the full
technology-neutral capability frame proposed here.** Vendors cross provider
boundaries within *specific* capabilities — governance, policy screening, agent
control — but none offers the complete frame. This is a sharper claim than the
original and it survives the evidence.

---

## Earlier notes (historical, superseded by the register)

- **Microsoft Platform Management** — Foundry Control Plane is documented as "a
  unified management interface that provides visibility, governance, and control
  for AI agents, models, and tools across your Foundry enterprise". Verified
  2026-08-15. Against the AWS `◐` this likely warrants `●`, which is precisely
  the anchoring problem: do not fix either until both are scored together. One
  caveat — that Learn page emits an "Access to this page requires authorization"
  notice, so an accessible corroborating URL should be captured for the cell.
- **Google Agent Services / Operations / Platform Management** need targeted
  official evidence before rating.

---

## Consequence for the manuscript

**Resolved.** §XII previously asserted a finding derived from the pre-evidence table:

> …a comparative assessment showing that commercial platforms cover execution
> and security well, **evaluation and platform management poorly, and none
> neutrally**.

The AWS row alone moves Evaluation to `●` and Platform Management to `◐`, and
the Microsoft evidence points the same way. This sentence must be re-derived
from the completed matrix, not carried forward. The "none neutrally" clause is
unaffected — it follows from the vendors' own scoping, not from the ratings.

**§XI-B already carries the right hedge** ("reflects published documentation at
one point in time for products that change quarterly… should be read as
motivating the need for a neutral frame, not as a durable evaluation of any
product"). That limitation is strengthened, not weakened, by this exercise:
Bedrock Agents Classic entered maintenance mode on 30 July 2026, so a rating
taken from the older documentation would already be stale. That is the churn
argument demonstrated on the paper's own comparison — usable in §XI-C once the
matrix is complete, but not before.
