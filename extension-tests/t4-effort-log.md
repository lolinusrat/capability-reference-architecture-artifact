# T4 Effort Log

Logged as work happens (protocol §7). Times are UTC.

| When | Phase | Engine | Activity |
|:---|:---|:---|:---|
| 2026-10-02T10:26Z | P1 | pgvector | Start: dependencies and adapter |
| 2026-10-02T10:32Z | P1 | pgvector | Adapter complete (JDBC after finding P1-1); startup checked with no engine and with pgvector; inventory captured |
| 2026-10-02T10:35Z | P1 | qdrant | Adapter complete; startup checked for none/qdrant/pgvector; inventories captured |
| 2026-10-02T10:36Z | P2 | both | Harness: run_t4.py written; checked against runtime paths, headers and protocol K5 wording |
| 2026-10-02T10:42Z | P2 | both | Harness frozen (2fb49a3) before any run |
| 2026-10-02T10:43Z | P2 | both | Attempt 1 run (≈1.5 min); complete; no recorder errors |
| 2026-10-02T10:50Z | P3 | both | Report written; submitted for review |
