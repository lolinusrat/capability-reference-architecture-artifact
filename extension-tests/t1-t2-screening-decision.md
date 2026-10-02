# T1/T2 Screening Decision (2 October 2026)

**Decision: neither T1 nor T2 proceeds to execution in the present study. Both
are retained as future work. No further substitution experiments are planned for
this study.** Screening was done after T4, as the evaluation plan requires
(30 September 2026). Proposed by the author's assistant; agreed by the reviewer.

> **T1/T2 screening decision.** Neither candidate will proceed to execution in the
> present study. T1 would test another substitution at the Model Services boundary
> already exercised by F3 and, without live Cohere access, would rely on recorded
> fixtures; its incremental evidential value is therefore limited. T2 concerns
> embedding purpose, but T4 established that the existing embedding contract
> provides no explicit field for purpose. Encoding purpose indirectly in
> attributes would violate the study's concealment constraint, while adding an
> explicit field would modify the contract and constitute a different
> architectural intervention. Both candidates are therefore retained as future
> work rather than executed as additional tests. No further substitution
> experiments are planned for this study.

## Screening criteria (evaluation plan) applied

| Criterion | T1 (Cohere provider) | T2 (embedding purpose) |
|:---|:---|:---|
| Existing contract? | Yes (Model Services provider SPI) | No: the purpose field is absent (T4, protocol §2 and §4.4) |
| Materially different substitution? | No: same boundary as F3 | Not a substitution: needs a contract change |
| Feasible as specified? | Fixture-only (no live Cohere key) | Only by concealment (forbidden) or contract extension |
| Distinct question? | Largely duplicates F3 | A design study, not an evaluation of the frozen architecture |

## Status of the drafts

`t1-cohere-provider-protocol.DRAFT.md`, `t2-embedding-purpose-protocol.DRAFT.md`
and `t1-baseline/` remain in the repository as unexecuted drafts. They were never
frozen or run. They stay excluded from the replication package, and the
manuscript will not report them as experiments. The manuscript may name them as
future work. Evidence IDs remain F3, T3 and T4; the EXP1–EXP5 numbering is not
used.
