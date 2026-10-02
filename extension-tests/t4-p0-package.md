# T4-P0 Package — Knowledge Services

**STATUS: FROZEN 2 October 2026 (author's authorization; the reviewer's line-by-line review was not completed). Frozen digests: `t4.frozen.sha256.md`. P1 authorized by the author.**

Prepared 30 September 2026. F3 and T3, and all their evidence, are untouched.

## 1 What P0 contains

| File | SHA-256 |
|:---|:---|
| `t4-knowledge-services-protocol.DRAFT.md` | `29eee3652d3f121c09e00130d898c0c5a0fedcf79d58901481d249e1cef133f6` |
| `t4-corpus.json` (12 synthetic documents, two tenants, one `restricted`) | `8bbab1d1e51bdc8364ea82b59be711e07f35da9d19fb47acb453d5a7cbefa785` |
| `t4-queries.json` (6 queries; `topK` = 3) | `18de6fff99050eae8e341ec5e8b521be4e5fcef1260693b820fa209fb2d8d7bc` |
| `t4-engine-config.md` (engine configuration record; rows added in P1) | `c304a5625957ec6246a2bbf0754ac794a65390d95eedceee442cf0b5c485f349` |
| `freeze_interface_inventory_t4.py` (14 surfaces; derived from T3's script, which is unchanged) | `a3dac801641035b5d82343a2b6b7e9a28f3b5955ec80d91bdcc962a0dc527d5b` |
| `t4.baseline.sha256` (baseline inventory; the engine package holds 0 files) | `4b6488ae2d3d7c33b1e10131ee0743b49b467e96a87791f59b47eb34bc8f1ddd` |

Contract under test: `runtime-common/.../spi/Retriever.java`, SHA-256
`91ee23489fc9136419e22d839f31a1df89db63975c4276080319d24c26448e9e`, first committed
`a68e2b06` (5 August 2026), with **no implementation**.

## 2 Starting state of the runtime

Prototypes monorepo `7e44342b2fe82414f297f4fcf517c858c6428257`, plus T3's four
frozen, uncommitted changes (the two repairs and two regression tests), all in
`runtime-cache`, which is outside every T4 surface. `runtime-retrieval` and
`runtime-common` are unmodified.

## 3 Findings from reading the code, and the predictions fixed from them

1. **Access control beyond tenant cannot be expressed.** A retriever receives only
   `CallerIdentity` (tenant, user, application, use case, environment, region,
   session, free-form tags); no roles, permissions or Security decisions.
   **Prediction P-acl:** tenant isolation is achievable; entitlement to a
   restricted document is not. This tests the paper's Scenario 1 statement that
   Knowledge Services applies Security's access decisions at query time.
2. **Retrieval failure degrades silently by default.** The request continues
   without context and is marked `retrieval.degraded`. **Success must therefore be
   observed positively:** the retrieved sources in the prompt the gateway receives,
   with an optional non-interfering recorder.
3. **The embedding request has no purpose field.** Its free-form `attributes` map
   could carry one. **Doing so is defined in advance as concealment**, T2's issue by
   another route. With the recommended symmetric stub embeddings, T4 does not test
   embedding semantics; that stays with T2.
4. **Indexing is outside the contract.** T4 tests the query path only, and corpus
   loading is harness tooling.
5. **The packaging question T3 raised is decided in advance.** Adapters go in a new
   `engine` package inside `runtime-retrieval`, which the application already
   packages. `runtime-retrieval/pom.xml` is permitted; the application's build files
   are protected.

## 4 Checks performed

- The baseline inventory captures all 14 surfaces, and a self-comparison reports no
  change.
- On a doctored copy, a change to `Retriever.java` gives **FAIL**, and a new file in
  the engine package gives a **permitted** change.
- T3's inventory script is unchanged.

## 5 Decisions, resolved on review (protocol §10)

1. **Embeddings:** a deterministic, symmetric stub, with its algorithm fixed in
   protocol §6. Asymmetry is T2's question.
2. **Engines:** real containers, with identical inputs; R2DBC for pgvector, REST
   through `WebClient` for Qdrant.
3. **Images, pinned by digest:**
   - `pgvector/pgvector:0.8.6-pg16@sha256:ccc6e83d…fb4d6b`, which is the same index as
     the current floating `pg16` tag;
   - `qdrant/qdrant:v1.19.1@sha256:12364fe8…246a10`, the latest release.
4. **Corpus and queries:** as drafted.
5. **`topK` = 3**, fixed in the protocol and in `t4-queries.json`. Returned ids are
   recorded; identical rankings are not required.
6. **Effort:** hours logged per engine.

Also fixed: P-acl stays a predicted limitation; observed retrieval evidence is
mandatory for K1; behaviour and containment are reported separately; engine
configuration and corpus loading are recorded (`t4-engine-config.md`, harness
digests).

## 5a Corrections made while checking the baseline against the protocol

- **The consumer surface was too permissive.** It was "existing files protected",
  which would have admitted a new file anywhere in `runtime-retrieval`, including
  one that alters the consumer. It is now **fully protected, with the `engine`
  package carved out**, and the protocol's §5 says the same.
- Checked on a doctored inventory: a new file outside `engine` gives **FAIL**; a new
  file inside `engine` gives a **permitted** change. The carve-out filter was checked
  on sample paths: it excludes `engine` and its subpackages, and keeps a
  look-alike `engineering/` in the protected surface.
- The script's 14 surfaces match protocol §5's 11 rows (the four neighbours share
  one row) class for class.
- The recaptured baseline matches the runtime, and `runtime-retrieval` is unmodified.

## 6 Next

Line-by-line review of these files, then a freeze. **P1 (implementing the adapters)
requires separate authorization.**
