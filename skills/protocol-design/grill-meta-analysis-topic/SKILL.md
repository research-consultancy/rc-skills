---
name: grill-meta-analysis-topic
description: Validate a proposed meta-analysis topic against the published evidence.
disable-model-invocation: true
---

# Validate a Meta-Analysis Topic

Run a gated viability loop: **grill → research → appraisal → overlap verdict → re-grill**. Use the model-invoked `grilling` skill for the interview and the model-invoked `pubmed` skill for reproducible biomedical searches.

## Gate 1 — Reach a shared baseline

Interview the user one decision at a time. Give your recommended answer with a short methodological rationale. Retrieve factual answers; ask the user only for judgments, constraints, and choices.

Resolve:

- the review type: intervention, exposure, diagnostic, prognostic, prevalence, network, dose-response, or another justified synthesis;
- population, condition, setting, and exclusions;
- intervention or exposure and comparator;
- primary and secondary outcomes, measurement windows, and intended effect measures;
- eligible study designs, dates, languages, and publication status;
- the clinical or methodological contribution the user expects;

Maintain a live one-sentence question, working title, and PICO/PECO/PICOS. When an answer changes one element, revisit every dependent choice.

Present the baseline formulation and ask the user to confirm it. Begin the viability audit only after confirmation.

## Gate 2 — Audit the published landscape

Search broadly enough to falsify novelty, not merely support it.

### Find prior syntheses

Run reproducible PubMed searches for exact and adjacent systematic reviews and meta-analyses. Vary terminology, MeSH terms, acronyms, spelling, intervention or exposure class, population breadth, outcomes, and review type. Inspect reference lists and related articles to find reviews missed by the first query.

Search the wider web for:

- Cochrane reviews and protocols;
- PROSPERO, OSF, and other relevant registrations;
- journal sites, DOI records, preprints, conference material, and specialty-society publications;
- non-PubMed-indexed reviews and recent online-first publications.

Record every exact query, source, search date, result count when available, and link. Separate published reviews from protocols, registrations, and ongoing work.

For each serious overlap candidate, extract:

- last search date and publication date;
- review question and eligibility criteria;
- included studies and sample size;
- outcomes, subgroups, effect measures, and synthesis methods;
- conclusions, limitations, and author-stated research gaps.

Appraise whether each close review deserves to constrain the proposed topic. Use ROBIS to judge risk of bias and AMSTAR 2 when its scope fits the review. Examine protocol or registration concordance, search coverage and recency, duplicate screening and extraction, excluded-study handling, risk-of-bias methods, synthesis choices, publication-bias assessment, conflicts, and certainty of evidence. Report domain judgments rather than converting the tools into a single score.

Call a review **high quality** only when the structured appraisal supports that judgment. A close but unreliable review may create a replication or methods-improvement opportunity rather than making the topic non-viable.

### Test analytical feasibility

Locate the likely primary studies and determine whether enough independent, sufficiently comparable data exist. Check outcome definitions, time points, effect measures, duplicate cohorts, extractable data, clinical and methodological heterogeneity, and whether one study would dominate the synthesis.

The audit is complete only when exact duplicates, adjacent reviews, registered or ongoing reviews, close-review quality, and primary-study feasibility have all been checked.

## Gate 3 — Give an overlap verdict

Classify the baseline topic:

- **Viable:** no close synthesis exists, a defensible contribution remains, and the primary evidence can support it.
- **Viable if modified:** overlap exists, but a clinically or methodologically justified distinction can be tested.
- **Not currently viable:** a recent high-quality review answers essentially the same question, or the primary evidence cannot support the proposed synthesis.

Show an overlap matrix comparing the proposed topic with the closest reviews across population, intervention/exposure, comparator, outcomes, study designs, search date, and synthesis method. Cite the strongest evidence for the verdict and label inference explicitly.

Novelty alone is insufficient. A viable topic must also be clinically meaningful, methodologically coherent, and feasible with the available evidence.

## Gate 4 — Re-grill every proposed pivot

If the topic is already covered or not feasible, continue the one-question-at-a-time interview. Offer a recommended pivot grounded in the gaps found, then wait for the user's choice.

Consider only distinctions with a defensible rationale, such as:

- a materially different population, setting, comparator, outcome, or follow-up period;
- evidence published after the prior review's search date;
- a neglected subgroup that can be defined without arbitrary slicing;
- a different eligible design or estimand;
- dose-response, diagnostic, prognostic, network, individual-participant-data, cumulative, or living synthesis when the data and question justify it;
- resolving a documented methodological weakness in prior reviews.

After each accepted change, rewrite the question and repeat the relevant searches. Treat a pivot as viable only after research shows that it is distinct and feasible. Continue until the user confirms a formulation supported by the audit, or accepts that no defensible version is currently available.

## Deliver the viability brief

Return:

1. final working title and one-sentence question;
2. compact PICO/PECO/PICOS and review type;
3. verdict with confidence and rationale;
4. closest published and registered overlaps with citations, links, and structured quality judgments;
5. exact search log and cutoff date;
6. primary-study feasibility, anticipated heterogeneity, and major risks;
7. the defensible contribution or the reason to stop.

Leave protocol drafting for a separate request.
