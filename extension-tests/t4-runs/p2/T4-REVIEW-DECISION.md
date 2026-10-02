# T4 — Review Decision (2 October 2026)

**Reviewer decision: T4-P2 attempt 1 accepted as a valid experimental result,
including its failures. No rerun.** Report: `T4-REPORT.md` (755ca4a).

## Decisions

1. **K5, Finding P2-1: option (c), report as is.** No repair before reporting.
   - (a) Adapter-side sanitisation was rejected: it would put a platform concern
     into every realization and make the experiment greener.
   - (b) Consumer-side repair was rejected for T4: it changes a protected surface
     and would be a post-test repair, not part of the T4 result.
2. **K6 stays FAIL** under its frozen composite rule. It is reported with the
   fact that the engine switch itself held: one jar, one setting, zero files
   changed.
3. **K3 (P-acl held) is retained** as an architectural limitation discovered by
   the experiment. The missing information is a Security decision or caller
   entitlements reachable from `ExecutionContext`. It is not an engine comparison.
4. **Observation P2-3** (zero-similarity documents fill top-K, no relevance
   threshold) is retained as secondary.

## Framing required in the manuscript

T4 must not be presented as "a third boundary passed." The accurate finding: the
interface boundary contained the technology substitution (containment PASS),
while the behavioural test exposed pre-existing contract and error-handling
limitations (K5 FAIL for both realizations, hence K6 FAIL; K3 limitation).

Reviewer's wording, for the evaluation:

> The substitution was structurally contained, but the experiment exposed a
> pre-existing cross-boundary behavioral deficiency: realization-specific failure
> details leaked through the consumer's error path. Because the frozen behavioral
> criterion prohibited this, K5 failed for both realizations and consequently K6
> failed under its composite pass rule.

## Programme decision

Stop adding experiments. Next, in order:
1. the T1/T2 screening decision;
2. publish the complete Zenodo v2 evidence;
3. rewrite the manuscript around the expanded evidence (F3, T3, T4).
