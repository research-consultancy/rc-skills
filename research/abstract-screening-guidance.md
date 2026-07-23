# Designing sensitivity-first abstract screening

Research date: 2026-07-23

Scope: primary guidance relevant to a skill that screens titles and abstracts exported from PubMed, asks the review team to operationalize eligibility, and returns a shorter CSV for human review. Sources are the current Cochrane Handbook, PRISMA 2020, and PRISMA-S. PRISMA and PRISMA-S are reporting guidelines rather than conduct standards; the behavioral recommendations below are therefore anchored mainly in Cochrane and use PRISMA to define the audit information worth preserving.

## Executive recommendation

Treat the skill as a **high-sensitivity triage assistant**, not an autonomous study selector. Before screening, convert the review question into explicit, pre-specified eligibility rules and pilot them on a small mixed sample. During screening, assess each rule as `yes`, `no`, or `unclear`; retain both `probable_include` and `maybe` records in the candidate CSV; and assign `exclude` only when the title/abstract contains explicit evidence that a hard criterion is not met. Missing, ambiguous, poorly reported, or conflicting information must become `unclear`, never an inferred exclusion.

This operationalizes Cochrane's instruction that title/abstract screening should remove only **obviously irrelevant** reports and should generally be over-inclusive. Cochrane also places final eligibility decisions at the full-text stage, ideally with two independent reviewers, and does not recommend automatic elimination based on active-learning stopping rules because safe stopping remains difficult to establish ([Cochrane Handbook, Chapter 4 §§4.6.3–4.6.6](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-04)).

## Eligibility interview

The interview should produce a versioned, human-readable eligibility specification before classification begins. At minimum, ask for:

- review type and target study-design features (not merely potentially inconsistent design labels);
- population or condition, diagnostic definition, age or other demographic limits, severity, setting and geography where relevant;
- intervention or exposure, including acceptable variants, dose/intensity, duration, delivery mode and co-interventions where relevant;
- eligible comparator(s), including whether no comparator is acceptable;
- whether **measurement** of an outcome domain is required for eligibility, distinct from whether usable outcome results are reported;
- eligible publication status, language and date range, with a rationale for restrictions;
- rules for mixed populations or mixed interventions when only a subset is eligible;
- known hard exclusions and the ordered list used to choose one primary exclusion reason;
- borderline examples, synonyms, historical terminology and acceptable indirect descriptions.

Cochrane defines review eligibility mainly from population, intervention, comparator and study design. Outcomes are rarely appropriate as eligibility criteria: a study should not be excluded merely because it does not report usable results for an outcome, although requiring that an outcome was measured can sometimes be justified. Cochrane also recommends defining population criteria in advance, including diagnosis, setting and demographics, and pre-specifying how mixed populations will be handled ([Cochrane Handbook, Chapter 3 §§3.1–3.4](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-03)).

Pilot the resulting rules on roughly six to eight records spanning clear inclusions, clear exclusions and doubtful cases. Revise ambiguous rules before the full run and preserve the final criteria version. This follows Cochrane's explicit recommendation to pilot eligibility criteria to improve clarity, training and consistency ([Cochrane Handbook, Chapter 4 §4.6.4](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-04)).

## Conservative classification contract

Use this record-level logic:

1. Evaluate every hard eligibility criterion as `yes`, `no`, or `unclear`, and record a short abstract-grounded rationale.
2. `probable_include`: all assessable hard criteria are `yes`; any remaining uncertainty is non-disqualifying.
3. `maybe`: no hard criterion is explicitly `no`, but at least one criterion is unclear, conflicting, or absent.
4. `exclude`: at least one hard criterion is explicitly contradicted by the title/abstract. Record the first failed criterion in the team's pre-specified order as the primary reason.
5. Export both `probable_include` and `maybe` to the candidate CSV. Never convert a low confidence score, missing abstract, non-English abstract, vague design description, missing outcome results, or low ranking into `exclude`.
6. If the parser cannot reliably delimit a PubMed record, retain it as `maybe` with `parse_warning`; do not silently drop it.

The asymmetric error policy should be stated explicitly in the skill: when evidence supports both exclusion and uncertainty, uncertainty wins. Cochrane says authors should generally be over-inclusive during title/abstract screening, allows studies to remain “awaiting assessment” when information is insufficient, and says studies must not be excluded solely because outcome data are unusable or unreported ([Cochrane Handbook, Chapter 4 §§4.6.3–4.6.4](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-04)).

Do not call retained rows “included studies.” Use “candidates for human screening” or “potentially eligible reports.” Cochrane distinguishes reports from studies and requires final decisions to be based on full texts when possible; PRISMA likewise separates records screened, reports retrieved, reports excluded and studies included ([Cochrane Handbook, Chapter 4 §§4.6.1–4.6.4](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-04); [PRISMA 2020 expanded checklist, items 8 and 16a](https://www.prisma-statement.org/s/PRISMA_2020_expanded_checklist-yc78.pdf)).

## Duplicate records and multiple reports

Handle two different relationships separately:

- **Duplicate records of the same report:** deduplicate conservatively using PMID first, then DOI, then a normalized bibliographic match. Preserve the retained record, all source-row identifiers, the matching key/method, and a duplicate count. Do not auto-merge fuzzy title matches without a stable identifier; flag them for review.
- **Multiple reports of the same study:** do not discard them. Assign a `possible_study_cluster_id` and explain the linkage evidence (trial registration number, overlapping authors, setting, intervention details, sample size and dates). Secondary reports can contain distinct outcomes, time points or methods.

Cochrane requires removal of duplicate records before screening but also requires multiple reports of one study to be collated rather than discarded, because the study—not the report—is the unit ultimately included in a review ([Cochrane Handbook, Chapter 4 §§4.6.1–4.6.3](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-04)). PRISMA-S item 16 requires reporting the deduplication process and software because methods differ in sensitivity and may remove false-positive duplicates ([PRISMA-S, item 16](https://pmc.ncbi.nlm.nih.gov/articles/PMC8270366/#Sec37)).

## Audit trail and run summary

Preserve enough information to reconstruct the screening and complete a PRISMA flow diagram:

- source filename, file hash, PubMed export format if known, run timestamp and record count before parsing;
- eligibility-specification text/version and any criteria changed after piloting;
- automation/model/tool name and version, prompt/skill version, and the rule that both retained classes were exported;
- parsed count, parse-failure count, exact-duplicate count, unique records screened, counts by decision, and candidate CSV row count;
- per-record decision, criterion-level judgments, primary reason, confidence used only for ordering, and warnings;
- a separate audit CSV or JSONL containing **all** records, including exclusions and duplicate mappings, even if the user-facing candidate CSV contains only retained records.

Cochrane requires decisions for all identified records to be documented sufficiently to populate the flow diagram; broad categories are sufficient at initial screening, while plausibly eligible studies excluded after detailed assessment need an explicit reason ([Cochrane Handbook, Chapter 4 §4.6.4, MECIR C41](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-04)). PRISMA 2020 asks authors to report reviewer arrangements, how automation was integrated, tool/version and validation details, records marked ineligible by automation, and stage-by-stage counts ([PRISMA 2020 explanation and elaboration, items 8 and 16a](https://www.bmj.com/content/372/bmj.n160); [official expanded checklist](https://www.prisma-statement.org/s/PRISMA_2020_expanded_checklist-yc78.pdf)). PRISMA-S additionally asks for total records per source and the deduplication method/software ([PRISMA-S, items 15–16](https://pmc.ncbi.nlm.nih.gov/articles/PMC8270366/)).

## Recommended candidate CSV

One row should represent one retained **report**, not a claimed unique study. Recommended fields:

| Field | Purpose |
| --- | --- |
| `source_record_id` | Stable row/index from the input export |
| `pmid`, `doi` | Persistent identifiers when present |
| `title`, `authors`, `journal`, `publication_year`, `abstract` | Human screening and citation lookup; preserve the supplied abstract for the private handoff artifact |
| `screening_decision` | `probable_include` or `maybe` |
| `priority_rank` | Review order only; never an exclusion threshold |
| `confidence` | Optional calibrated aid for ranking, not eligibility |
| `primary_reason` | Concise reason the report was retained |
| `population_judgment`, `intervention_exposure_judgment`, `comparator_judgment`, `study_design_judgment`, `outcome_measurement_judgment`, `other_criteria_judgment` | Criterion-level `yes`/`no`/`unclear` trace |
| `uncertainties` | Missing or ambiguous facts requiring full text |
| `supporting_text` | Short title/abstract evidence supporting the classification |
| `possible_study_cluster_id`, `possible_companion_reports` | Preserve possible multiple-report relationships |
| `duplicate_count`, `duplicate_source_ids`, `deduplication_method` | Trace exact-record deduplication |
| `parse_warning`, `screening_notes` | Data-quality and reviewer handoff |
| `pubmed_url` | Direct retrieval link when PMID exists |
| `criteria_version`, `model_tool_version`, `screened_at` | Per-row provenance when the CSV may be separated from the run manifest |
| `human_review_status` | Blank or `pending` on export; supports the downstream manual workflow |

The separate full audit artifact should add `exclude` rows plus `primary_exclusion_reason`, `failed_criterion`, and any automation error fields. Keeping the candidate CSV compact while retaining a complete machine-readable audit reconciles the user's workload-reduction goal with Cochrane and PRISMA documentation needs.

## Boundaries for the skill

- It may prioritize candidate records, highlight PICO information, and shorten the manual queue.
- It must not claim that abstract screening establishes final eligibility or meta-analytic suitability.
- It must not stop early or eliminate the unreviewed tail based solely on a learned relevance ranking. Cochrane notes that safe stopping is difficult and does not recommend automatic elimination through active-learning stopping rules in current guidance ([Cochrane Handbook, Chapter 4 §4.6.6.2](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-04)).
- Human reviewers should inspect every exported candidate at full text, resolve possible companion reports, and make final study-level decisions. Ideally, two reviewers work independently for final eligibility, with a predefined disagreement process ([Cochrane Handbook, Chapter 4 §4.6.4](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-04)).
- Any automation used should be described as integrated support, with its version and validation/calibration process recorded, as required by PRISMA 2020 item 8.

## Bottom line

The safest useful abstraction is **rules-first, tri-state, over-inclusive triage**. Grill the team until the hard criteria and mixed-case policies are explicit; pilot those rules; retain every record without an explicit hard contradiction; rank retained records without allowing the rank to exclude; keep exact duplicates separate from possible companion reports; and save an all-record audit alongside the shorter candidate CSV.
