# Research Decision Record Format

Research decision records live in `docs/decisions/` and use sequential numbering: `0001-slug.md`, `0002-slug.md`, and so on. Create the directory when the first qualifying decision is made.

## Template

```md
# {Short title of the decision}

{In 1–3 sentences: the research context, the decision, and why this option best serves the intended inference.}
```

## Optional sections

Add these only when they preserve information a future collaborator will need:

- **Status** (`proposed | accepted | deprecated | superseded by decision-NNNN`)
- **Evidence or authority** — guideline, methods source, pilot finding, or empirical check that shaped the choice
- **Considered options** — credible alternatives worth remembering
- **Consequences** — effects on validity, feasibility, interpretation, or comparability

## Numbering

Scan `docs/decisions/` for the highest existing number and increment it.

## Qualifying decisions

Record a choice only when it is hard to reverse, non-obvious without context, and based on a real trade-off. Examples include:

- defining the primary endpoint or estimand;
- choosing index time, follow-up, censoring, or a competing-risk strategy;
- setting consequential cohort, exposure, comparator, or outcome boundaries;
- resolving overlapping cohorts or multiple eligible estimates;
- choosing a synthesis model or a defensible departure from a registered protocol;
- adopting an external clinical definition that materially changes eligibility or interpretation;
- selecting a missing-data, multiplicity, or sensitivity-analysis strategy central to the primary inference.

Routine wording edits, conventional defaults, and easily reversible exploratory choices stay out of the decision log.
