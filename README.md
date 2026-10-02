# Replication package — version 2

**Paper:** *From Requirements to Testable Boundaries: Measuring Change Containment
Under Technology Substitution in Enterprise AI Platforms* (Zenodo preprint). The
paper was earlier titled *A Capability-Based Reference Architecture for
Enterprise AI Platforms*; version 1 of this package accompanied that version.

Version 2 **preserves version 1** and adds:

1. **Two dated corrections to `technology-substitution-results.md`** (the Model
   Services test, F3). They are additions only; every line of the version-1 file
   is unchanged. §4 lists three configuration changes the original footprint
   list omitted, and §11 corrects the screening record, which had missed the
   response-cache candidate.
2. **The complete record of the second substitution test, T3** (AI Runtime
   response cache, in-process Caffeine to networked Redis), under
   `extension-tests/`, laid out as the research folder was, so every frozen
   record verifies in place. **All three runs are included, including the two
   unsuccessful ones**, which are the evidence of the two defects and of the
   contained repairs that followed.
3. **The complete record of the third test, T4** (Knowledge Services: pgvector
   and Qdrant built against the pre-existing `Retriever` contract, then switched
   by configuration), in the same tree.
   - **Containment held:** no protected surface changed, and switching changed
     no file.
   - **Two behavioural assertions failed:**
     - K5, for both engines: the pre-existing consumer returns raw engine error
       text to the caller.
     - K6, by its composite rule.
   - **K3 recorded a contract limitation.**
   - **All of it is reported as recorded and was not repaired**
     (`T4-REVIEW-DECISION.md`).
4. **The screening decision for T1 and T2** (`t1-t2-screening-decision.md`):
   both drafted tests were screened out and were not run.

The version-1 README follows below the line; its instructions for F3 and the
other evidence are unchanged.

## Contents of `extension-tests/`: T3

| Path | What it is |
|:---|:---|
| `t3-response-cache-protocol.md` | The protocol, at its final (revision-3) text, with every revision recorded in its §11 |
| `freeze_interface_inventory_t3.py`, `t3.before.sha256` | The 13-surface interface inventory script and the frozen pre-repair before-inventory |
| `t3-histories.json` | The 20 fixed conversation histories |
| `t3-harness/` | The harness (`run_t3.py`), the test-only recorder (source and build script), the independent key probe, and the preparation smoke-run script |
| `t3.frozen.sha256.md`, `t3-freeze-package.md` | Original freeze (commit `bdbed44`) |
| `t3-post-repair/` | First repair (packaging), its verification and its freeze (`03ec627`) |
| `t3-revision-3/` | Second repair (cache key), regression tests, sensitivity check and its freeze (`57761c0`; reviewed revision `0ee4edb`) |
| `frozen-versions/<commit>/` | Files as they were at an earlier freeze, where they later changed, so each frozen record can be checked against its own versions |
| `t3-runs/initial-attempt-1/` | Initial run, aborted before measurement (tooling path defect) |
| `t3-runs/initial-attempt-2/` | Initial run: the Redis realization was not selectable as built (B1–B7 not assessed) |
| `t3-runs/post-repair/` | After repair 1: within-instance PASSes; cross-instance B5a and B5b FAIL; B4 INCOMPLETE |
| `t3-runs/revision-3/` | After repair 2: all B1–B7 PASS; two B3 inputs not exercisable. Its `results.json` carries the harness label `post-repair`; it is identified by this directory and its frozen record. |
| `t3-smoke-run.md`, `t3-smoke/` | Preparation smoke runs (Caffeine only; not part of T3), including the recorder non-interference check |
| `README.md` | The research folder's own overview, covering T3 and T4. It also mentions the T1 and T2 drafts, which are not included (see below). |

Each run directory holds its report, `results.json`, the harness log, the
recorder's event files, the Redis `MONITOR` log, the API responses, the key-probe
outputs, the after-inventory and the containment comparison, where the run
produced them.

## Contents of `extension-tests/`: T4

| Path | What it is |
|:---|:---|
| `t4-knowledge-services-protocol.md`, `t4-p0-package.md` | The protocol (question, contract as found, failure rules, surfaces, assertions K1–K7) and the P0 package |
| `t4-corpus.json`, `t4-queries.json` | The 12 synthetic documents (two tenants, one restricted) and the six queries |
| `freeze_interface_inventory_t4.py`, `t4.baseline.sha256` | The 15-surface interface inventory script and the baseline, captured before any adapter |
| `t4.frozen.sha256.md` | P0 freeze (`87392da`) |
| `t4-engine-config.md` | Every setting used for each engine, secrets excepted. Rows were added in P1 and P2, as designed; the P0 text is in `frozen-versions/87392da/` |
| `t4-effort-log.md` | Effort, logged as work happened |
| `t4-p1/` | Introduction of both adapters: findings and deviations (P1-1: R2DBC broke startup application-wide; P1-D1: JDBC), copies of the engine sources (`engine-src/`), the abandoned R2DBC attempt with its startup-failure excerpt, the build-file diff, and the inventories and comparisons after each engine |
| `t4-harness/` | The P2 harness (`run_t4.py`), deterministic embedding, stub gateway, corpus loader, and the test-only recorder (source and build script) |
| `t4-p2.frozen.sha256.md` | P2 harness freeze, before any run (`2fb49a3`) |
| `t4-runs/p2/attempt-1/` | The run: `results.json`, harness log, recorder events, every API response, runtime-log excerpts, after-inventory and containment comparison |
| `t4-runs/p2/T4-REPORT.md`, `T4-REVIEW-DECISION.md` | The report, and the reviewer's acceptance (K5 reported as is) |
| `t1-t2-screening-decision.md` | Why T1 and T2 were not run |

**Verifying T4's records:**
- `t4.frozen.sha256.md` verifies from `extension-tests/`, with
  `t4-engine-config.md` checked against `frozen-versions/87392da/`.
- `t4-p2.frozen.sha256.md` verifies from `extension-tests/` for its harness files
  and inputs. Its engine-package entries are runtime-relative paths: they verify
  against the copies in `t4-p1/engine-src/`. The runtime build file is
  represented by `t4-p1/runtime-retrieval-pom.diff`.

## Reconciliation with the paper (§10.4 and data availability)

| Statement in the paper | Evidence |
|:---|:---|
| The cache contract predates the experiment | `technology-substitution-results.md` §11 correction (contract first committed 5 August 2026) |
| Placement of caching in AI Runtime was a judgment recorded before freezing | `t3-response-cache-protocol.md` §2 |
| Protocol, 13-surface inventory and 20 histories frozen before execution | `t3.frozen.sha256.md`; `t3.before.sha256` (13 surfaces); `t3-histories.json` |
| A hit counts only with `cached` true and no gateway call | `t3-harness/run_t3.py`; each run's `results.json` |
| Seven behavioral assertions | Protocol §7 (B1–B7) |
| Recorder and `MONITOR` recorded each instance's key | `t3-harness/recorder/`; `recorder-*.jsonl` and `redis-monitor.log` in each run |
| Initial run: runtime could not start with Redis selected | `t3-runs/initial-attempt-2/INITIAL-RUN-REPORT.md`; `runtime-A-redis.excerpt.txt` |
| First repair removed the optional declaration in the cache component's build file | `t3-post-repair/repair.diff`; bean check in `t3-post-repair/bean-check/` |
| No entry shared across instances in any of 21 cases | `t3-runs/post-repair/results.json` (B5a, and B5b with all 20 missed) |
| Expiry not assessed after the first repair, owing to a harness defect | `t3-runs/post-repair/POST-REPAIR-RUN-REPORT.md`, finding 2 |
| Second repair encodes history from role names and content | `t3-revision-3/key-repair.diff` |
| Regression test: pre-repair key diverges across JVMs, repaired key does not | `t3-revision-3/ResponseCacheKeyCrossProcessTest.java`, `CrossProcessKeyComputer.java`, `sensitivity-old-factory.log` |
| After the second repair every assertion passed, including 20/20 sharing and expiry at 300 s | `t3-runs/revision-3/results.json`; `REVISION-3-RUN-REPORT.md` |
| Two isolation inputs not exercisable | `t3-runs/revision-3/results.json` (B3) |
| No protected surface changed in any run | `containment-comparison.txt` in `initial-attempt-2/`, `post-repair/` and `revision-3/` |
| A repair in the application's build file would have been a containment failure | `t3-freeze-package.md` §4 (manifest) |
| T3 material is included in the next package version | This version |

T4 is reported in revision 2 of the preprint (Section 10.5 and Table 6), which is
published after this package version. Its statements correspond to:

- `t4-runs/p2/T4-REPORT.md`: outcomes, findings P2-1 to P2-3, and footprints;
- `t4-runs/p2/T4-REVIEW-DECISION.md`: K5 reported as is;
- `t4-p1/P1-FINDINGS-AND-DEVIATIONS.md`: the startup coupling the inventory did
  not detect, and the move to JDBC.

The screening of T1 and T2 in that revision's Section 11.2 corresponds to
`t1-t2-screening-decision.md`.

## What was left out, and why

Listed file by file in `EXCLUDED-FILES.txt`:

- **Build artefacts** (`*.jar`, `*.class`, `classpath.txt`). They are reproducible
  from the included sources, and the classpath files list local build paths. The
  recorder jar's digest for each run is in that run's `results.json`.
- **Raw runtime logs** (`runtime*.log`). Where a log is itself evidence, a short
  excerpt of the relevant lines is included as `*.excerpt.txt`, with the original
  file's SHA-256, so a holder of the full research repository can verify it:
  - the initial run's startup failure;
  - smoke attempt 2's class-version failure;
  - smoke attempt 5's deliberate recorder-failure lines;
  - the post-repair bean check;
  - T4's four runtime starts (startup, recorder diagnostics, degraded-retrieval
    lines);
  - T4-P1's R2DBC startup failure. That excerpt was made during P1 and is
    tracked in the research folder.
- **The T1 and T2 protocol drafts and the T1 baseline.** Both tests were screened
  out and never run. Their screening decision is included.
- **The two classpath files moved out of the runtime repository after initial
  attempt 1.** Their handling is described in that attempt's
  `ABORTED-BEFORE-MEASUREMENT.md`.

## Personal information, credentials and redaction

- **No credentials are included.** Model-provider settings in the prototypes are
  environment-variable references only.
- **This public copy is redacted.** Four kinds of identifying local detail are
  replaced:
  - the author's local prototypes path → `<prototypes-root>`, including its
    URL-encoded form (T3 and T4 inventories, logs and excerpts);
  - the home directory → `<home>`, for example in build classpaths;
  - the machine hostname in key-probe headers → `<host>`;
  - the operating-system account name in log lines → `<user>`.

  No measured value, key, digest listing or result is changed.
- **The unredacted evidence is kept privately**, exactly as recorded, with its own
  manifest. It is not published.
- **`REDACTIONS.txt`** lists every redacted file, with the SHA-256 of its private
  original and of this public copy.
- **Frozen records are not altered.** They list the digests of the originals, so a
  redacted file here does not match its frozen record. Its original digest, in
  the first column of `REDACTIONS.txt`, is the one the frozen record lists.
- Version 1 of this package was published earlier and unredacted. It is not
  changed by this version.

## Verifying version 2

- **Integrity of this copy:** `shasum -a 256 -c MANIFEST.sha256` checks every file as
  published.
- **Frozen records:** each T3 frozen record verifies from `extension-tests/` against
  the files of its own revision (for T4, see "Verifying T4's records" above).
  - The revision-3 record verifies against the current files.
  - The two earlier records verify against `frozen-versions/<commit>/` for the
    files that later changed, and against the current files for the rest.
  - **Files listed in `REDACTIONS.txt` are checked through that file:** their
    frozen-record digest appears there as the original digest. Every other file
    verifies directly.
- **Runtime changes:** the two T3 repairs and regression tests, and the T4 engine
  package, live in the prototypes repository, which is not included, as for F3.
  Their diffs, copies or before-and-after versions, and their digests are included.

---

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

**Terminology.** The frozen protocol (`technology-substitution-protocol.md`, kept
byte-exact) uses "pre-registered" to mean internally pre-specified and frozen
before execution; no external preregistration registry was used. The paper and
the other artifact files say "pre-specified" or "fixed before execution".

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
