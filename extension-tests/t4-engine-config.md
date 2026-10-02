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
| *Rows added in P2 (attempt 1). Values as used by `t4-harness/run_t4.py`.* | | | |
| `RUNTIME_RETRIEVAL_ENGINES_PGVECTOR_URL` | `jdbc:postgresql://127.0.0.1:15432/knowledge` | not set | environment |
| `RUNTIME_RETRIEVAL_ENGINES_PGVECTOR_USERNAME` | `knowledge` | not set | environment |
| `RUNTIME_RETRIEVAL_ENGINES_PGVECTOR_PASSWORD` | test-only, random per run, not recorded | not set | environment |
| `RUNTIME_RETRIEVAL_ENGINES_QDRANT_URL` | set but unused (`http://127.0.0.1:16333`) | `http://127.0.0.1:16333` | environment |
| Table / collection | `documents` (property default) | `documents` (property default) | default in `EngineProperties` (engine package) |
| Embedding profile, timeout | `enterprise-embeddings`, 5 s (defaults) | same | default in `EngineProperties` (engine package) |
| `MODEL_GATEWAY_URL` (value) | `http://127.0.0.1:18180` (harness stub) | same | environment |
| Other runtime settings | `SERVER_PORT=18181`, `RUNTIME_ENVIRONMENT=integration`, `RUNTIME_SECURITY_MODE=NONE`, `RUNTIME_CACHE_PROVIDER=caffeine` | same | environment |

The only setting that differs between the two engines' runs is `RUNTIME_RETRIEVAL_ENGINE`.
Both runs used one runtime jar (sha256 `32d4f0f7…1c102`, recorded in `t4-runs/p2/attempt-1/results.json`).

**Corpus loaders:** harness files under `t4-harness/`, written in P1. Their digests
are recorded in each phase's inventory record.

Rows are added in P1 as each engine's settings become known. Nothing is removed.
