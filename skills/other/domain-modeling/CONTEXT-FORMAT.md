# CONTEXT.md Format

`CONTEXT.md` is the canonical conceptual language for a medical research project. It is a glossary, not a protocol, data dictionary, or analysis plan.

## Structure

```md
# {Study, review, or research program}

{One or two sentences describing the research context and intended inference.}

## Population

**Target population**:
The population to which the study intends to generalize its primary inference.
_Avoid_: Study population, sample

**Analysis population**:
The participants whose observations contribute to a specified analysis after applying its rules.
_Avoid_: Cohort when referring to the analyzed subset

## Time

**Index time**:
The event or instant that starts eligibility-aligned follow-up for a participant.
_Avoid_: Baseline when the intended meaning is time zero

## Outcomes

**Primary outcome**:
The prespecified outcome that anchors the study's principal inference.
_Avoid_: Primary endpoint unless the project adopts that term canonically
```

## Rules

- **Choose one canonical term.** List plausible competing terms under `_Avoid_`.
- **Define the concept, not its implementation.** Put thresholds, code lists, algorithms, transformations, and analysis procedures in the protocol, data dictionary, extraction form, or analysis plan.
- **Preserve authoritative terminology.** Align validated clinical definitions, reporting standards, and methodological terms with their source; record project-specific departures explicitly.
- **Keep definitions tight.** Use one or two sentences and distinguish neighboring concepts directly.
- **Cross-reference operational homes when useful.** For example: `_Operationalized in: SAP §4.2_`.
- **Group naturally.** Common headings include Population, Intervention or Exposure, Comparator, Outcomes, Time, Causal Structure, and Synthesis.

## Single and multiple contexts

Use one root `CONTEXT.md` for most projects. For a research program with distinct studies or review and analysis contexts, use a root `CONTEXT-MAP.md`:

```md
# Context Map

## Contexts

- [Clinical cohort](./studies/cohort/CONTEXT.md) — defines participants, exposures, outcomes, and follow-up
- [Evidence synthesis](./reviews/CONTEXT.md) — maps reports and comparisons to review eligibility
- [Statistical analysis](./analysis/CONTEXT.md) — defines estimands and analysis populations

## Relationships

- **Clinical cohort → Statistical analysis**: conceptual constructs are operationalized into variables and estimands.
- **Evidence synthesis ↔ Clinical cohort**: eligibility concepts determine whether study populations and outcomes are comparable.
```

If `CONTEXT-MAP.md` exists, update the relevant context. If only root `CONTEXT.md` exists, use it. Create a root `CONTEXT.md` when the first canonical term is resolved.
