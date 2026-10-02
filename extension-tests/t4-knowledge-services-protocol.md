# T4 — Knowledge Services: Implementing Against a Frozen Contract

**Frozen at the end of P0, before any adapter was written.** F3 and T3 and their
evidence are untouched.

## 1 The question

> Can a retrieval contract defined before any implementation existed accommodate
> two materially different retrieval engines without any change outside
> Knowledge Services, and can the platform then switch between them by
> configuration alone?

**This is not a swap of existing implementations, unlike F3 and T3.** The
`Retriever` interface exists (first committed `a68e2b06`, 5 August 2026) and has
**no implementations**. T4 is an **implementation-against-a-frozen-contract**
experiment, followed by a substitution. The manuscript must say so. If the
contract proves insufficient, that identifies a limitation of this boundary as
originally specified; it is not a general failure of the architecture, and it
is preserved as evidence rather than repaired during the test.

## 2 The contract and its consumers, as found in P0

- **Contract:** `Retriever`, with `strategy()`, `retrieve(ExecutionContext, int topK)` returning
  `Flux<RetrievedDocument>`, and `supports(ExecutionContext)`. A `RetrievedDocument`
  carries `id`, `version`, `content`, `score`, `source` and `metadata`.
- **Consumer:** `DefaultContextBuilder` (in `runtime-retrieval`) takes every `Retriever`
  bean, calls the applicable ones concurrently, fuses multiple rankings, and puts
  the result on the execution context. The prompt composer then appends each
  document to the system prompt as `[source: …]`.
- **Query:** the caller's `rag.query`, through `ChatInvocation.RetrievalOptions`.
- **What a retriever knows about the caller:** `CallerIdentity`, which has tenant,
  user, application, use case, environment, region, session and free-form
  `tags`. **There are no roles, permissions or Security decisions.**
- **Failure handling:** by default (`runtime.retrieval.fail-on-error=false`), a failing
  retriever is logged, the request is marked `retrieval.degraded`, and the request
  continues **without context**. That is a silent degradation, analogous to the
  Redis cache's silent miss in T3.
- **Embeddings:** available to an adapter only through the existing gateway client
  (`ModelGatewayClient.embeddings`). Its request carries `modelProfile`, `inputs` and
  `attributes`, and has no field for embedding purpose.
- **Indexing is outside the contract.** `Retriever` only reads. T4 therefore tests the
  query path; corpus loading is harness tooling, not part of either realization.

## 3 Implementations to be built (in P1, not now)

| | Engine | Deployment | Access |
|:---|:---|:---|:---|
| **A** | PostgreSQL 16 with pgvector | `pgvector/pgvector:0.8.6-pg16@sha256:ccc6e83d6e35e931dc7c5def2022729d5a6c370318d099181995567ff1fb4d6b` | R2DBC (non-blocking, fitting the reactive contract) |
| **B** | Qdrant | `qdrant/qdrant:v1.19.1@sha256:12364fe851b9f17356fc88189fc06d1b521262e04659ec7345975b00c9246a10` | REST through Spring's `WebClient`; no new client library |

Both engines run as real containers, referenced by digest, and both receive
identical corpus and query inputs.

Both live **inside Knowledge Services' permitted surface** (§5): new files in a new
package `…/runtime/retrieval/engine/`, registered by their own configuration class
and selected by a property (`runtime.retrieval.engine=pgvector|qdrant`), set through
the environment. Build pgvector first and freeze its footprint; then build Qdrant
against the same frozen contract.

## 4 What counts as failure (containment)

**T4 fails if either implementation, or switching between them, requires any
change to a protected surface (§5).** In particular:

1. **Any change to the `Retriever` contract or the retrieval model**
   (`RetrievedContext`, `RetrievedDocument`), or to any other `runtime-common` type.
2. **Any change to an existing consumer:** the `runtime-retrieval` sources as found in
   P0, orchestration, the outward API or its configuration.
3. **Any change to the application's build** (root or `runtime-api` `pom.xml`) or to a
   neighbouring domain.
4. **Concealment.** Carrying information the contract lacks through a channel not
   meant for it counts as failure, and is reported as such. Examples:
   - embedding purpose, or any other semantic parameter, in gateway `attributes`;
   - authorization inferred from caller-supplied `tags`.

**The contract is not extended during the test.** If an implementation cannot be
completed without such a change, it stops. The missing information is recorded,
and the result is reported as a contract limitation.

## 5 Surfaces (captured by `freeze_interface_inventory_t4.py`)

| Surface | Class |
|:---|:---|
| Shared kernel: `runtime-common/src/main/java`, including `Retriever`, `RetrievedContext`, `ExecutionContext`, `CallerIdentity` | protected |
| AI Runtime consumers: `runtime-retrieval/src/main/java` **outside** the `engine` package | protected (no file may be added, changed or removed) |
| `runtime-retrieval/src/main/resources`, every file type (none exist at P0; engines register by component scan) | protected |
| Orchestration: `runtime-orchestration/src/main/java` | protected |
| Outward contract and configuration: `runtime-api/src/main/java`, `application.yml` | protected |
| Gateway client: `runtime-inference/.../gateway` | protected |
| Application build: root `pom.xml`, `runtime-common/pom.xml`, `runtime-api/pom.xml` | protected |
| Existing retrieval tests: `runtime-retrieval/src/test/java` | protected-existing |
| Neighbours, as F3 and T3: Developer Experience, Governance and Security, Evaluation, Model Services outward contract | protected |
| Knowledge Services realizations: `…/runtime/retrieval/engine/` (empty at P0) | permitted |
| `runtime-retrieval/pom.xml` (engine drivers, and a dependency on the gateway client) | permitted |
| `docker-compose.yml` | permitted |

**Placement judgments, recorded before any code is written:**

- The `runtime-retrieval` module holds both the **consumer** (context building, AI
  Runtime) and, after P1, the **realizations** (Knowledge Services). Everything outside
  the new `engine` package is the consumer and is fully protected: a new file there
  could alter the consumer's behaviour. Only the `engine` package may gain files.
- **`runtime-retrieval/pom.xml` is permitted.** The application already depends on
  `runtime-retrieval`, so adapters placed there are packaged without touching the
  application's build. This is the packaging question T3 raised; it is decided here,
  in advance, rather than after a failure.

## 6 Behavioural assertions (evaluated in P2, for each engine)

**How retrieval is observed.** Because a failing retriever degrades silently,
success must be observed positively. The primary evidence is the stubbed model
gateway's request journal: the system prompt it receives lists each retrieved
document as `[source: …]`. A test-only recorder may wrap `Retriever` beans (the T3
approach), non-interfering, and is subject to the same integrity rules. An HTTP 200
with no retrieved sources is a **silent degradation, never a pass**.

- **K1 Retrieval.** For every query in `t4-queries.json`, each document listed as
  `required` appears among the retrieved sources.
- **K2 Tenant isolation.** No query ever surfaces a document belonging to another
  tenant. This includes a query whose distinctive terms also occur in another
  tenant's document.
- **K3 Access control beyond tenant.** The corpus marks one document
  `classification: restricted`. **Prediction P-acl (fixed now):** the contract cannot
  express a caller's entitlement to it, because `CallerIdentity` carries no roles,
  permissions or Security decisions. K3 records whether the restricted document is
  returned to an unentitled caller, and states what information would be needed.
  It is reported as a finding about the contract; neither engine may invent
  entitlements (§4.4). This directly tests the paper's Scenario 1 statement that
  Knowledge Services applies Security's access decisions at query time.
- **K4 Citation metadata.** Each retrieved document's `source` and `metadata.title`
  equal the corpus values, for both engines.
- **K5 Failure behaviour.** With the engine stopped:
  - with `fail-on-error=false`, the request is served and marked degraded, with no
    retrieved sources;
  - with `fail-on-error=true` (set through the environment), the request fails
    with the declared retrieval error.

  In neither case may a raw engine error reach the API.
- **K6 Substitution.** Switching from pgvector to Qdrant is configuration only, and the
  API response structure is identical. K1, K2, K4 and K5 hold for both engines.
- **K7 Cross-engine consistency.** Each query's required documents are retrieved by
  both engines. **Ranking equality is not required**, since different engines may
  legitimately order results differently.

**Embeddings and T2.** Embeddings come from a deterministic, harness-owned stub
that implements the existing gateway embeddings endpoint
(`POST /v1/inference/embeddings`). Each text is lower-cased and split on
non-alphanumeric characters; each token is hashed (SHA-256) to one of 256
dimensions, with a sign bit; the counts are L2-normalized. The same function
serves queries and documents, so it is **symmetric**. **T4 therefore does not test
query-versus-document embedding semantics**; that question stays with T2 and is
reported as outside T4's scope. Encoding a purpose in `attributes` remains
concealment (§4.4).

**Two separations, required throughout.**

- **Behaviour and containment are reported separately.** An unchanged protected
  surface does not mean an implementation meets its functional obligations, and a
  failed behavioural assertion is not a containment failure. Each K assertion has
  its own outcome, and containment has its own.
- **Engine configuration and corpus loading are recorded, so they cannot hide
  protected changes.**
  - Every property and environment variable used for each engine is listed in
    `t4-engine-config.md`, with its value (secrets excepted).
  - Corpus loaders are harness files in `t4-harness/`, with their digests recorded
    in each phase's inventory record.
  - A setting that could only be applied by editing a protected file, such as
    `application.yml`, is a containment failure, not configuration.

## 7 Procedure

1. **P0** (this phase): protocol, corpus, queries, inventory script, baseline. Review, then freeze.
2. **P1**, separately authorized:
   - implement pgvector; capture the inventory; record its footprint and effort;
   - implement Qdrant against the same frozen contract; capture the inventory again;
   - never modify a protected surface to make an engine work.
3. **P2**, separately authorized: run K1–K7 for both engines, and the containment comparison.
4. **P3/P4:** report, and submit for review before any manuscript claim.

Effort is logged as work happens. Each phase writes to its own directory, and no
earlier evidence is overwritten.

## 8 Prior knowledge, disclosed

While preparing P0, the following were read in code: the contract, its consumer,
the failure handling, `CallerIdentity`, the embedding request, and the absence of
any existing implementation or vector store. Predictions P-acl (K3) and the
embedding-purpose scope note follow directly from that reading, and are fixed
before any adapter exists.

## 9 Reporting

Containment is reported separately from behaviour. The **introduction footprint of
each engine** is reported separately (what building it changed), and the
substitution result (what switching changed) separately again. A contract
limitation (§4) is reported as a finding, never as a repaired pass.

## 10 Decisions (resolved on P0 review, 30 September 2026)

1. **Embeddings:** the deterministic, symmetric stub specified in §6. Embedding
   asymmetry is T2's question.
2. **Engine access:** R2DBC for pgvector; REST through `WebClient` for Qdrant. Both
   engines run as real containers.
3. **Images:** pinned by digest (§3). Floating tags are not used.
4. **Corpus and queries:** as in `t4-corpus.json` (12 synthetic documents, two
   tenants, one restricted) and `t4-queries.json` (6 queries).
5. **`topK` = 3**, fixed here and in `t4-queries.json`. For each query and engine,
   the returned document ids are recorded. **Identical rankings are not required.**
6. **Effort:** hours logged per engine as work happens.

Also fixed on review:

- **P-acl stays a predicted limitation.** Authorization data the contract cannot
  express is not invented.
- **Observed retrieval evidence is mandatory for K1.** An HTTP 200 alone never
  satisfies it.
