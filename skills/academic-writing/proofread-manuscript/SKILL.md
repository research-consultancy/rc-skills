---
name: proofread-manuscript
description: Exhaustively audit a medical manuscript for language, scientific consistency, citation support, tables and figures, journal compliance, and hidden revisions. Use for proofreading, full pre-submission review, or revision-package verification.
---

# Proofread a Medical Manuscript

Run a hostile-reader preflight adapted from the thorough manuscript review. Preserve the author's scientific meaning while finding every error that could weaken trust or block submission.

## Inventory and scope

Classify every input: manuscript, supplement, tables or figures, analysis output, cover letter, response letter, or journal instructions. Resolve ambiguous file roles before selecting the clean manuscript. Establish the target journal and whether the user wants a findings report, an edited file, or both. State which checks cannot run when a source file, analysis output, or target journal is absent.

Read the applicable document/PDF/spreadsheet skill before extraction. Read every section, table, footnote, legend, reference, and supplement in full. For DOCX files, inspect the OOXML as well as rendered text so tracked insertions, deletions, and comments remain visible. Render document pages when layout affects the judgment.

Inventory is complete when every provided file has a role and every requested review surface is accessible.

## Apply the audit

Read [references/checklist.md](references/checklist.md) completely, then work through every applicable item. Re-derive arithmetic and trace repeated statistics across the abstract, text, tables, figures, supplement, and analysis output. Use the model-invoked `pubmed` skill and primary full text to verify important cited claims. If a response letter is present, match each claimed revision and quoted passage to the current manuscript.

When a target journal is named, retrieve its current official author instructions and compare exact limits, structure, declarations, reference style, and submission-file requirements.

Apply edits only when authorized. Keep technical terms, effect direction, denominators, uncertainty, citations, and author voice intact. Flag scientifically ambiguous passages for author decision rather than silently choosing a meaning.

For a scoped line edit, apply every language check and identify which broader checks were outside scope. For a full review, the audit is complete only when every checklist item is verified, reported as a finding, or explicitly marked uncheckable.

## Deliver findings

Group findings by severity:

- **Critical**: factually wrong, unsupported, submission-blocking, or hidden tracked content.
- **Major**: likely reviewer objection, material ambiguity, or cross-document inconsistency.
- **Minor**: grammar, style, formatting, or polish.

For each finding give the location, a short quote, the problem, and a specific fix. Separate required corrections from discretionary editorial suggestions. For a full review, add only material, non-duplicative editorial recommendations that strengthen the paper beyond correctness; omit this section when none are warranted. End with a coverage note listing passed checks and checks that could not be performed.

If editing a file, preserve the original, return the corrected artifact, and summarize material changes.
