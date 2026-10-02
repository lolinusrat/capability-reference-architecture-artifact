# Extension tests T1–T4

> **Current status (2 October 2026): T3 and T4 are complete and accepted by
> review.** T3's runs are in `t3-runs/`, T4's in `t4-runs/p2/`. T1 and T2 were
> screened out after T4 and will not be run in this study
> (`t1-t2-screening-decision.md`). No further substitution experiments are
> planned. Earlier versions of this file are in the git history.

Three further technology-substitution tests, drafted 30 September 2026 after the
F3 result, the negative control and the corrected screening record
(`technology-substitution-results.md` §11, correction of 30 September 2026).

| Test | Domain | Substitution | Kind |
|:---|:---|:---|:---|
| T1 | Model Services | Add a Cohere provider that does not exist today | Introducing a new realization |
| T2 | Model Services | Cohere embeddings, which require a query/document purpose the contract cannot carry | Stress test: incompatible semantics |
| T3 | AI Runtime | Caffeine response cache → live Redis | Second boundary; first run of the Redis path (**complete**) |
| T4 | Knowledge Services | pgvector ↔ Qdrant, built against the pre-existing `Retriever` contract | Implementation against a frozen contract, then substitution (**complete**) |

The identifiers are new. `E5` remains the Governance Support criterion and `F3`
keeps its meaning; T1–T4 are not relabelled F3 runs. T4 was added on
30 September 2026 (evaluation plan: target three completed experiments, F3, T3
and T4).

## Status

**T3 (AI Runtime response cache, Caffeine to live Redis): complete.** Three runs,
each under its own freeze, all reported separately:

| Run | Freeze | Outcome | Report |
|:---|:---|:---|:---|
| Initial, attempt 1 | `bdbed44` | Aborted before measurement (tooling path defect); no result | `t3-runs/initial-attempt-1/ABORTED-BEFORE-MEASUREMENT.md` |
| Initial, attempt 2 | `bdbed44` | Redis realization not selectable as built (client libraries not packaged); B1–B7 not assessed | `t3-runs/initial-attempt-2/INITIAL-RUN-REPORT.md` |
| Post-repair | `03ec627` | After repair 1: within-instance PASSes; cross-instance B5a and B5b FAIL; B4 INCOMPLETE | `t3-runs/post-repair/POST-REPAIR-RUN-REPORT.md` |
| Revision 3 | `57761c0` (reviewed `0ee4edb`) | After repair 2: all B1–B7 PASS; two B3 inputs not exercisable | `t3-runs/revision-3/REVISION-3-RUN-REPORT.md` |

No protected surface changed in any run, and both repairs stayed inside the
permitted cache component. The results were accepted by review on 30 September
2026 and are reported in the paper, §10.4. The revision-3 `results.json` carries
the harness label `post-repair`; that run is identified by its directory and its
frozen record.

The freeze packages and frozen records (`t3-freeze-package.md`,
`t3-post-repair/POST-REPAIR-PACKAGE.md`, `t3-revision-3/REVISION-3-PACKAGE.md` and
the `*.frozen.sha256.md` files) state their status **as at the time of each
freeze**, "FROZEN — NOT RUN". They are kept unchanged as records; the runs that
followed are the ones in the table above.

**T4 (Knowledge Services, pgvector ↔ Qdrant): complete, accepted by review on
2 October 2026.**

| Phase | Record | Outcome |
|:---|:---|:---|
| P0 | `t4.frozen.sha256.md` (`87392da`) | Protocol, corpus, queries, 15-surface inventory and baseline frozen before any adapter |
| P1 | `t4-p1/` (`9b4a2ac`) | Both adapters built in the permitted engine package. Finding P1-1: an R2DBC driver broke startup application-wide, invisibly to the inventory. Deviation P1-D1: JDBC |
| P2 | `t4-p2.frozen.sha256.md` (`2fb49a3`); `t4-runs/p2/attempt-1/` | Containment PASS. K1, K2, K4 and K7 PASS for both engines. K5 FAIL for both: the pre-existing consumer returns raw engine error text. K6 FAIL by its composite rule; the switch itself held. K3 is a contract limitation (no entitlement beyond tenant) |
| P3 | `t4-runs/p2/T4-REPORT.md`; `T4-REVIEW-DECISION.md` | Accepted as is. K5 reported without repair (option c) |

`t4-engine-config.md` gained rows in P1 and P2, as its design allows; its P0 text is
in git at `87392da`.

**T1 and T2: screened out, not run** (`t1-t2-screening-decision.md`). Nothing
about them is a result. Their drafts remain as unexecuted records and are not
included in the replication package.

## Order and baselines

As drafted: T1 first, then T2 from T1's completed revision. Both were screened
out. T3 and T4 are independent of each other and of T1 and T2.

## Freezing procedure (once each protocol is approved)

1. Resolve the open decisions and remove the DRAFT markers.
2. Write that test's inventory script as a **new file**. `freeze_interface_inventory.py`
   is not edited: its digest is part of the F3 record.
3. Record the source revision of every repository involved.
4. Compute SHA-256 digests of the protocol, the script and the before-inventory,
   record them in `<test>.frozen.sha256.md`, and commit before any
   implementation or configuration change is made.
5. Execute, then report every outcome, including failures, under the protocol's
   reporting rules.

## Rules common to all tests

- **One researcher.** The author implements, runs and classifies. The protocols
  constrain that judgement in advance; they do not remove it.
- **Effort is logged as work happens**, in `<test>-effort-log.md`, not
  reconstructed afterwards.
- **Secrets never enter the repository or the replication package.** The Cohere
  key is read from `COHERE_API_KEY`; recorded fixtures are redacted before they
  are committed.
- **A zero-change count means nothing unless the behavioural assertions pass.**
  A realization that silently stops working can look perfectly contained.
- **Failures are results.** A test that meets its failure condition is reported
  as such, not repaired and rerun without disclosure.
