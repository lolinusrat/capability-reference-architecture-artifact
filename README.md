# Artifact for: A Capability-Based Reference Architecture for Enterprise AI Platforms

This artifact supports the derivation, evaluation and reproducibility claims made
in the accompanying paper. It is intended to be read on its own: no knowledge of
how the work developed is required.

## Contents

| File | Supports | Contents |
|:---|:---|:---|
| `requirements-traceability.md` | C1 | Traces each of the twelve requirements to its architectural concern, its literature and practitioner evidence, its principal capability domain and the evaluation criterion it supports; records the normalization, consolidation and separation decisions behind the twelve, with the test applied to them; and records the four boundary challenges raised against the decomposition together with their resolutions. |
| `commercial-platform-evidence-matrix.md` | C3 | The 40-cell commercial-platform comparison behind Table 4, with rating, evidence source, access date, rationale and provenance for every platform–domain cell. |
| `documentary-triangulation.md` | C3 | The six-source documentary triangulation behind Table 5, with the six architectural propositions, the rating rubric, the supporting text and locator for every one of the 36 ratings, and the record that the governance family also informed the requirement derivation. |
| `falsification-assessment.md` | C3 | How the three falsification conditions in Section X were assessed, the evidence behind each outcome, and the two recorded near-misses: the cost-placement disagreement and IBM's alternative assurance decomposition. |
| `alternative-decompositions.md` | C1 | Four competing decompositions built from the same twelve requirements and tested against the three boundary criteria, including the one alternative the criteria prefer over the ten-domain model and the reason it is not adopted. |
| `technology-substitution-protocol.md` | C3 | The F3 experiment as it was fixed **before** the substitution: the realizations to be exchanged, the interface surfaces to be held fixed, what counts as a technology-independence failure and what is permitted as within-domain change. The experiment-defining content is unchanged. The final, non-methodological paragraph was amended after execution to record that the prototype repositories are not included; that amendment, and the frozen and amended digests, are documented in `technology-substitution-frozen.sha256.md`. Being a pre-substitution document it also uses the section numbering the manuscript had at freeze time ("§11.2" for what is now §XI-B); that reference is left as written, because it falls inside the methodology-core lines whose digest evidences that the experiment definition is unchanged. |
| `technology-substitution-results.md` | C3 | What the substitution actually produced, reported as observed: the change footprint, the interface-inventory comparison, the neighbouring test results, the discrimination case, and the two deviations from the protocol. |
| `technology-substitution-frozen.sha256.md` | C3 | SHA-256 digests of the protocol, the before-inventory and the inventory script, recorded 2026-09-05 before the substitution. The file states plainly that digests establish integrity rather than chronology, and identifies which of the three verify from this copy. |
| `technology-substitution.before.sha256`, `technology-substitution.after.sha256` | C3 | The interface inventory of the five capability surfaces, 111 files, hashed before and after the substitution. Both files' records are byte-identical, which is the F3 result. |
| `boundary-containment-negative-control-protocol.md`, `boundary-containment-negative-control-results.md` | C3 | The negative control for the containment measurement, frozen before execution and reported as observed: the planted cross-boundary dependency, the detection, and the revert. Digests in `boundary-containment-negative-control.frozen.sha256`, inventories in `negative-control.before.sha256` and `negative-control.after.sha256`. |
| `freeze_interface_inventory.py` | C3 | The script that produced the inventories, shipped unmodified so that its frozen digest verifies. |

## Verifying the headline claims in twenty minutes

Every quantitative claim the paper makes can be checked against this artifact
without re-doing the assessment. Each row names the claim, where its evidence
lives, and what you should find.

| Paper claim | Check against | Expected | Time |
|:---|:---|:---|:--|
| Twelve requirements, each with a principal capability domain (C1, Table 1) | `requirements-traceability.md`, Matrix | 12 requirements, each mapped to at least one principal capability domain, none unmapped, and four recorded boundary challenges with resolutions | 4 min |
| Forty vendor ratings (Table 4) | `commercial-platform-evidence-matrix.md`, 40-cell evidence register | **36 ●, 4 ◐, 0 ○**, and every row carrying rating, rationale, source URL, access date and provenance | 4 min |
| All forty ratings content-verified (§XI-B) | `commercial-platform-evidence-matrix.md`, *Evidence re-verification* | 40 cells verified at body level, 12 of them in the 22 September pass; provenance 28/9/3 before, 40/0/0 after; no rating changed | 3 min |
| Thirty-six documentary ratings (Table 5) | `documentary-triangulation.md` §5.1 | **8 ●, 24 ◐, 4 ○**, matching the matrix reproduced below | 4 min |
| S6 rated from full papers, not abstracts (§X-B) | `documentary-triangulation.md`, *Evidence re-verification — S6* | All three Lu et al. papers retrieved in full; P3 moves off abstract text to a body locator; no rating changed; S3 remains paywalled | 3 min |
| Falsification outcomes (§X, §X-A, §X-B, §X-C) | `falsification-assessment.md` §5 | F1–F3 assessed and none met (F1 and F2 organize evidence retrospectively; F3 was tested against a criterion fixed in advance); one recorded exception each for F2's two assessments | 3 min |
| Technology substitution executed, not argued (§X-C) | `technology-substitution-frozen.sha256.md`, then `technology-substitution-results.md` | The inventory script and the before-inventory reproduce their frozen digests exactly; the protocol's methodology (lines 1-233) is unchanged since freezing, as the amendment note in that file shows; and both interface inventories share one records-only digest. The results record the substitution as **OpenAI → Ollama** | 4 min |
| **0 cross-boundary interface changes** (§X-C) | `technology-substitution-results.md` §1 and §6 | All five interface surfaces byte-identical across 111 files; 0 files modified in the four neighbouring domains; **1** file changed within Model Services, in configuration | 4 min |
| Measurement discriminates a violation (§X-C) | `boundary-containment-negative-control-results.md` §1 and §4 | A planted realization-specific field changes **1** AI Runtime interface file and its surface aggregate; the other four surfaces byte-identical; the tree restored after revert | 3 min |
| Boundary criteria do real but incomplete work (§5) | `alternative-decompositions.md` §5 | A, B and D rejected (B and D with separation supported but not compelled); **C preferred on the criteria and not adopted** | 3 min |

The sections that follow give the full procedure for *re-deriving* each result
rather than merely checking it.

## Reproducing the requirements traceability

1. Start with requirements R1–R12 in Section IV of the paper.
2. Compare each requirement with the literature sources recorded in
   `requirements-traceability.md`. Where a requirement extends beyond what its
   sources establish, the matrix says so explicitly rather than implying the
   source carries the whole obligation.
3. Verify the principal capability-domain mapping against **Table 1** of the paper.
4. Table 1 of the paper records only the domain that *principally* discharges
   each requirement. Secondary responsibility is visible in Table 1's dependency
   column and in the interaction model of Section VII; the matrix does not
   enumerate contributing domains separately.
5. Check the four boundary challenges (B1–B4) and their recorded resolutions.
   B2 and B3 are the two the manuscript also states as open judgment calls.

## Reproducing the commercial-platform comparison

1. Use the ten capability-domain responsibilities in **Table 1** as the
   assessment criteria.
2. For each of the four platforms, inspect the official vendor documentation
   recorded in the 40-cell evidence register in
   `commercial-platform-evidence-matrix.md`.
3. Apply the predefined rubric:
   - **● substantial** — firmly documented first-party coverage of more than
     half of the responsibilities Table 1 defines for the domain, excluding
     separately licensed or billed adjacent products.
   - **◐ partial** — coverage exists but is narrower, fragmented, or omits major
     responsibilities.
   - **○ limited** — little first-party coverage is documented (defined by the
     rubric but not observed in the final Table 4 ratings).
4. Compare the resulting 40 ratings with **Table 4** of the paper.

**Expected result: 36 ●, 4 ◐, 0 ○.** Every platform reaches at least partial
coverage in all ten domains; the four partial ratings are Governance (Bedrock,
Vertex AI), Knowledge Services (watsonx) and Model Services (Vertex AI). This is the result after the
24 September 2026 re-rating; the original, pre-recheck assessment of 31 ●, 9 ◐ and the reason
for each of the seven changes are kept in the evidence matrix. Separately licensed
adjacent products (Microsoft Purview, Google Security Command Center, AWS Audit
Manager) are excluded for every vendor. If your totals differ by more than two or three cells, the
disagreement is with the rubric rather than with the evidence, and the per-cell
rationale column is where to look first.


Only official vendor documentation is admissible. Blog posts, analyst reports
and third-party summaries were not used.

## Reproducing the documentary triangulation

1. Take the six architectural propositions (P1–P6) and the rating rubric from
   `documentary-triangulation.md`, both fixed before assessment.
2. Retrieve the six sources listed there: the NIST AI Risk Management Framework
   with its Generative AI Profile, the EU AI Act, ISO/IEC 42001, IBM's
   Generative AI Capability Model, the Enterprise AI Operating Framework, and
   the reference architectures of Lu et al.
3. Rate each source against each proposition — corroborated, partial or not
   addressed — before comparing across sources.
4. Compare the resulting 36 ratings with **Table 5** of the paper.

**Expected result: 8 ●, 24 ◐, 4 ○.** Reading the matrix by proposition, the
corroboration counts are P1 = 2, P2 = 1, P3 = 1, P4 = 3, P5 = 0, P6 = 1. The
four ○ ratings are NIST/P1, EU AI Act/P1, ISO/IEC 42001/P1 and Lu et al./P6. This is the result
after the 24 and 25 September 2026 consistency re-ratings; the original 19 ●, 12 ◐, 5 ○
and the reason for each of the fourteen changes are kept in
`documentary-triangulation.md`.

The full expected matrix:

| Source | P1 | P2 | P3 | P4 | P5 | P6 |
|:---|:--:|:--:|:--:|:--:|:--:|:--:|
| NIST AI RMF and GenAI Profile | ○ | ◐ | ◐ | ◐ | ◐ | ◐ |
| EU AI Act | ○ | ◐ | ◐ | ◐ | ◐ | ◐ |
| ISO/IEC 42001 | ○ | ◐ | ◐ | ◐ | ◐ | ◐ |
| IBM GenAI Capability Model | ● | ◐ | ◐ | ● | ◐ | ◐ |
| Enterprise AI Operating Framework | ● | ● | ● | ● | ◐ | ● |
| Lu et al. reference architectures | ◐ | ◐ | ◐ | ● | ◐ | ○ |


The sources were selected purposively against stated independence criteria, not
sampled. Two are outside peer review, and one (ISO/IEC 42001) was assessed from
its published clause and Annex A structure rather than from the paywalled full
text; `documentary-triangulation.md` records this per source. Web sources were
retrieved on **31 August 2026**.

## Reproducing the alternative-decomposition analysis

1. Take the three boundary criteria from Section V of the paper and the twelve
   requirements from Section IV.
2. Construct the four alternatives in `alternative-decompositions.md` §2–§5 —
   merging Governance, Security and Evaluation; merging the AI Runtime with
   Agent Services; splitting Platform Management; absorbing it into Operations — or others of your own.
3. Apply each criterion using the evidence already in this artifact.
4. Compare with the result table in `alternative-decompositions.md` §6.

**Expected result: three alternatives rejected — one outright, two with
separation supported but not compelled — and one preferred on the criteria
but not adopted.** The third is the
interesting case and is reported in full: splitting Platform Management is
better on substitutability and assessment, and is rejected because a
product-management domain would not be a technical capability. Ownership fails
to discriminate in two of the four alternatives.

## Reproducing the falsification assessment

1. Take the three conditions — completeness, boundary and
   technology-independence failure — from `falsification-assessment.md` §1.
2. For completeness and boundaries, re-work the 40 commercial-platform ratings
   and the 36 documentary ratings and judge each difference between an
   independent architecture and the proposed domains as commercial packaging or
   architectural disagreement.
3. For technology independence, read `technology-substitution-protocol.md`
   first and `technology-substitution-results.md` second, in that order. The
   protocol fixes the failure criterion; `technology-substitution-frozen.sha256.md`
   carries its digest as recorded before the substitution, so the criterion can
   be shown to precede the result. Diff `technology-substitution.before.sha256`
   against `technology-substitution.after.sha256` to confirm the five interface
   surfaces are unchanged. Re-running the substitution itself requires the
   reference implementations, which are not part of this artifact.
4. Compare the outcomes with `falsification-assessment.md` §5 and with Sections
   10.1, 10.2 and 10.3 of the paper.

Two qualifications are stated in the paper and repeated in the assessment. The
conditions were formulated after the evaluation rather than pre-registered,
except the technology-independence criterion, which was frozen before its
experiment was run. And F3 is an implementation-based falsification test against
reference implementations built from the proposed boundaries by the same
author — it tests an architectural prediction, and is not independent
validation; the commercial-platform and documentary assessments are where the
external evidence lies.

## Evidence provenance

Provenance is recorded per cell. In the original assessment it was **not
uniform**:

- **verified** — the source body was retrieved and the supporting text inspected.
- **author-read** — the source was read manually where automated retrieval was
  unreliable.
- **title-level** — the source endpoint and title were confirmed, but page
  content could not be reliably retrieved.

That mix (28 verified, 9 author-read, 3 title-level) is the assessment history. The
re-verification recorded in `commercial-platform-evidence-matrix.md` brought all
40 commercial-platform cells to content-verified provenance (40 / 0 / 0) without
changing any rating.

All 40 commercial-platform ratings and all 36 documentary-triangulation ratings
were assigned by a single rater. The paper discloses both in §XI-B, where
single-rater bias is stated as a threat to validity: the 40 commercial-platform
ratings in the Table 4 paragraph, and the 36 documentary ratings in the purposive
documentary check.

## Snapshot

Commercial-platform evidence reflects documentation available on
**15 August 2026**. These products change frequently; the comparison is a
snapshot of documented architectural coverage, not an evaluation of product
quality.

## Evaluation status

The manuscript's evaluation comprises requirements traceability, three reference
scenarios, eight evaluation criteria, the commercial-platform comparison and the
six-source documentary triangulation, and the technology-substitution experiment
of Section X-C. It is analytical, scenario-based and documentary except for that
experiment, which was executed against a reference instantiation of the
architecture; no human participants were involved at any stage.

**Independent practitioner evaluation of the capability boundaries was not
conducted and contributes no evidence to this manuscript. It is future research,
not pending work**, and no ethics or consent pathway is
being pursued for it. The paper states the corresponding limitation directly:
the evaluation establishes internal consistency, capability coverage and one
bounded containment result, not effectiveness in practice.
