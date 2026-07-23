---
name: screen-pubmed-abstracts
description: Screen a PubMed plain-text export for a systematic review or meta-analysis and produce a balanced CSV shortlist.
disable-model-invocation: true
---

# Screen PubMed Abstracts

Run **inspect → grill → calibrate → screen once → audit → export**. Use the
model-invoked `grilling` skill for the interview. This is title-and-abstract triage,
not final eligibility assessment.

## Gate 1 — Inspect

Prepare the PubMed plain-text export:

```text
python <skill-dir>/scripts/pubmed_screen.py prepare <input.txt> --output <work-dir>/records.jsonl
```

Report record and missing-field counts. Inspect records from the beginning, middle,
and end. Resolve parsing errors until the source and prepared counts reconcile and
sampled fields are faithful.

## Gate 2 — Confirm the charter

Extract criteria from any supplied protocol or registration. Interview the user one
decision at a time, giving a recommended answer and short rationale. Resolve:

- the objective, review type, and PICO, PECO, PICOS, or better-fitting framework;
- eligible study designs, report types, populations, interventions or exposures,
  comparators, outcomes, settings, dates, languages, and publication statuses;
- whether noncomparative, single-arm, cross-sectional, utilization, eligibility,
  adherence, protocol, secondary-analysis, and conference reports qualify;
- rules for mixed populations or interventions and separable subgroup data;
- ordered exclusion reasons and which criteria are observable at abstract stage;
- handling of missing abstracts, duplicates, and multiple reports from one study;
- known eligible PMIDs and known ineligible records for calibration.

Translate fuzzy terms into observable rules and test edge cases. Distinguish a study
from its reports and “not reported” from “not eligible.” Save the confirmed charter as
`<output-stem>-screening-charter.md` with the source SHA-256, criteria, controls,
edge-case resolutions, and model/tool versions. Begin only after user confirmation.

## Decision contract — balanced triage

Judge each hard criterion as:

- `yes`: the title or abstract affirmatively supports eligibility;
- `no`: the title or abstract affirmatively contradicts eligibility;
- `unclear`: a named fact remains missing or genuinely ambiguous after reading the
  complete record;
- `not_applicable`: the charter makes the criterion irrelevant.

Derive the record decision from those judgments:

- any `no` → `exclude`;
- no `no` and at least one `unclear` → `maybe`;
- otherwise → `probable_include`.

An abstract can affirm a `no` by completely describing a different population,
intervention, comparison, or design; topical background language does not override
the stated objective and methods. When comparison is required, an explicitly
single-arm, uncontrolled, descriptive, or non-exposure-contrasted study fails the
comparator criterion. A utilization, adherence, eligibility, or prevalence study
fails the intervention/exposure criterion when its stated analysis does not assess
the target intervention or exposure.

Use `maybe` only when the record has a concrete plausible route to eligibility and
name both that route and the exact unresolved fact. Mere topical relevance does not
earn retention. For a complete abstract, read the objective and methods before
assigning `unclear`; a stated different focus supports `no`, while genuine
underreporting supports `unclear`. Missing or truncated abstracts remain `maybe`
unless the available title or metadata affirmatively establishes an exclusion.

Deduplicate exact PMIDs, or exact DOIs when PMIDs are absent, after retaining one
complete record. Retain and flag fuzzy matches and possible companion reports.

## Gate 3 — Calibrate

Pilot 8–12 varied records before the remaining records; expand only when needed to
include additional positive controls, with an absolute maximum of 20. Include clear
exclusions, common false-positive patterns, sparse records, and a missing abstract
when available. Set `screening_phase` to `pilot` on these decisions and record their
IDs in the charter. Pilot decisions are final and are not read again.

Require every positive control to be retained. Correct any control miss or unsupported
exclusion from the evidence already captured in its decision object. Calibration ends
when all pilot decisions obey the contract and the charter records the final edge-case
rules. Apply those rules prospectively to the remaining records.

## Gate 4 — Screen each remaining record once

Read at most 20 records per batch:

```text
python <skill-dir>/scripts/pubmed_screen.py batch <work-dir>/records.jsonl --start 1 --size 20
```

During that single read, evaluate the complete title and abstract in this order:

1. report design;
2. population;
3. intervention or exposure;
4. comparator or exposure contrast;
5. outcome measurement and other charter criteria.

Do not stop at the first ambiguous phrase. Finish the record, then write exactly one
JSON object to `<work-dir>/decisions.jsonl`. Set `screening_phase` to `main` for every
non-pilot record and copy a short verbatim title/abstract excerpt into
`supporting_text`:

```json
{"record_id": 1, "screening_phase": "main", "decision": "maybe", "reason": "The population and intervention fit, but the abstract does not state whether a comparator was used.", "concern": "Comparator unreported.", "criteria": {"population": "yes", "intervention_exposure": "yes", "comparator": "unclear", "study_design": "yes", "outcome_measurement": "yes", "other": "yes"}, "supporting_text": "Adults with HFrEF received dapagliflozin.", "related_report": ""}
```

Judge against the charter rather than a target shortlist size. Keep batch output in
the live session; the work directory should contain only durable screening artifacts.
Each record, including pilot records, is read once and receives one immutable content
decision. Complete the pass only after every source record has one decision.

## Gate 5 — Audit and export

Audit the final log:

```text
python <skill-dir>/scripts/pubmed_screen.py audit <work-dir>/records.jsonl <work-dir>/decisions.jsonl
```

Confirm all positive controls remain retained using their recorded decisions. The
audit is structural: verify counts, identifiers, schema, criterion/decision
consistency, 8–20 pilot decisions, and that every supporting excerpt occurs verbatim
in its source title or abstract. Perform these checks without reopening records for
content judgment.

Export:

```text
python <skill-dir>/scripts/pubmed_screen.py export <work-dir>/records.jsonl <work-dir>/decisions.jsonl <output.csv>
```

The command writes the candidate CSV and `<output-stem>-audit.csv` containing all
records. Report decision counts, retained percentage, control recall, structural
audit corrections, and paths. Deliver both CSVs and the charter. Call retained rows
candidates for human screening; final eligibility still requires human full-text
review.
