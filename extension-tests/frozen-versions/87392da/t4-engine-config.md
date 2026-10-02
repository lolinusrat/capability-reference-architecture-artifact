# T4 Engine Configuration Record (frozen at P0; rows are added in P1, none removed)

Every property and environment variable used for each engine is recorded here
before it is used (protocol §6). A setting that could only be applied by editing a
protected file is a containment failure, not configuration. Secrets are never
recorded; credentials for the local containers are test-only values generated at
run time.

| Setting | pgvector | Qdrant | Set through |
|:---|:---|:---|:---|
| `RUNTIME_RETRIEVAL_ENGINE` | `pgvector` | `qdrant` | environment |
| Engine endpoint | to be recorded in P1 | to be recorded in P1 | environment |
| `RUNTIME_RETRIEVAL_FAIL_ON_ERROR` | `false`, and `true` for K5's second case | same | environment |
| `MODEL_GATEWAY_URL` | harness stub (chat and embeddings) | same | environment |

**Corpus loaders:** harness files under `t4-harness/`, written in P1. Their digests
are recorded in each phase's inventory record.

Rows are added in P1 as each engine's settings become known. Nothing is removed.
