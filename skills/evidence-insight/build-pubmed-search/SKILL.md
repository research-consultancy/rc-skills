---
name: build-pubmed-search
description: Build and validate a PubMed search string for a meta-analysis.
disable-model-invocation: true
---

# Build a PubMed Search

Run a gated **grill → draft → test → calibrate → handoff** sequence. Use the model-invoked `grilling` skill for the interview and the model-invoked `pubmed` skill for live searches and record verification.

## Gate 1 — Reach a shared search question

Interview the user one decision at a time. Give a recommended answer with a short methodological rationale. Retrieve facts from available sources; ask the user for judgments, constraints, and choices.

Resolve:

- the review type and one-sentence objective;
- population or condition, intervention or exposure, comparator, outcomes, and eligible study designs;
- inclusion boundaries such as setting, age, disease stage, treatment line, follow-up, publication dates, languages, and publication status;
- whether this is a new search or an update, and the screening capacity available for planning the review;
- known eligible papers, prior reviews, protocols, or PMIDs that can serve as positive controls;
- exclusions that are both important and realistically searchable.

Maintain a live eligibility statement and PICO, PECO, PICOS, or other appropriate concept model. Distinguish eligibility criteria from concepts that belong in the electronic search. For a meta-analysis, optimize the search for sensitivity; treat screening burden as a feasibility constraint to report, not a reason to silently sacrifice eligible studies.

Present the shared search question, eligibility statement, searchable concept blocks, and likely non-searchable criteria. Drafting begins only after the user confirms them.

## Gate 2 — Draft the concept blocks

Use the `pubmed` skill to verify current MeSH headings, field behavior, and syntax. For every searchable concept, build one parenthesized `OR` block containing:

- verified current MeSH headings;
- unindexed title-and-abstract terms;
- abbreviations, spelling variants, older names, drug or intervention names, and clinically meaningful synonyms;
- narrower terms needed to retrieve eligible variants not reliably covered by the chosen MeSH heading.

Tag controlled vocabulary with `[mh]` and free text with `[tiab]`. Join concept blocks with `AND`. Use the fewest concepts needed to represent the question sensitively. Population and intervention or exposure usually anchor the search. Add comparator, outcome, or study-design blocks only when they are indispensable to identifying the eligible evidence and validation shows that relevant records remain retrievable.

Represent justified date limits explicitly with `[dp]`. Record other interface filters as limits rather than silently embedding them. Keep each meaning in one block so the query remains auditable.

The draft is complete when every included term maps to a confirmed concept and every confirmed searchable concept has both controlled-vocabulary and free-text coverage where PubMed supports them.

## Gate 3 — Test in PubMed

Invoke the `pubmed` skill and run the query against the live PubMed database.

Test each concept block alone, then the combined query. Record the exact query, search date, and result count for every material iteration. Inspect PubMed Search Details or query translation when available and correct unintended mappings, invalid tags, syntax errors, or terms that retrieve nothing for the wrong reason.

Calibrate with evidence:

1. Confirm that every available positive-control PMID is retrieved.
2. Inspect a varied sample of retrieved records to identify dominant false-positive patterns and missing terminology.
3. Compare MeSH and title/abstract contributions, accounting for recent records that may not yet be indexed.
4. Remove or add one block or restriction at a time and measure its effect on positive-control recall and result count.
5. Verify any proposed study-design filter against the eligible designs and recent unindexed records.

When no positive controls were supplied, locate likely eligible primary studies through relevant reviews or broad PubMed searches and verify their records before using them as provisional controls. Label that set provisional.

Repeat drafting and testing until the final query executes successfully, every available control is retrieved or each miss is explained, major false-positive patterns have been assessed, and every restrictive block is indispensable and has survived a documented recall test. Treat an unexplained positive-control miss as a failed strategy.

## Gate 4 — Hand off the final search

Give the user:

1. a single copy-ready PubMed search string in a code block;
2. the search date, final result count, and applied limits;
3. a compact concept table mapping each block to its MeSH and free-text terms;
4. the positive-control recall result and important calibration changes;
5. a short note explaining how to paste and run the string on the PubMed website;
6. limitations, including uncertain terminology, indexing lag, and criteria handled during screening rather than searching.

State that a PubMed query is one database-specific component of a meta-analysis search. Recommend translating and validating the strategy for every additional database required by the protocol. For a protocol-grade search, recommend independent PRESS-style review by a medical librarian or information specialist before the strategy is locked.
