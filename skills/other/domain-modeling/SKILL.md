---
name: domain-modeling
description: Build and sharpen a medical research project's domain model. Use when the user wants to pin down research terminology or a ubiquitous language, record a consequential methodological decision, or when another skill needs to maintain the domain model.
---

# Domain Modeling

Actively build and sharpen the research project's domain model as you design. This is the _active_ discipline — challenging terms, inventing edge-case scenarios, and writing the glossary and decisions down the moment they crystallise. (Merely _reading_ `CONTEXT.md` for vocabulary is not this skill — that's a one-line habit any skill can do. This skill is for when you're changing the model, not just consuming it.)

## File structure

Most research projects have a single context:

```text
/
├── CONTEXT.md
├── docs/
│   └── decisions/
│       ├── 0001-define-index-time.md
│       └── 0002-select-primary-estimand.md
└── analysis/
```

If a `CONTEXT-MAP.md` exists at the root, the project has multiple contexts. The map points to where each one lives:

```text
/
├── CONTEXT-MAP.md
├── docs/
│   └── decisions/                    ← project-wide decisions
├── studies/
│   └── cohort/
│       ├── CONTEXT.md
│       └── docs/decisions/           ← study-specific decisions
└── reviews/
    └── meta-analysis/
        ├── CONTEXT.md
        └── docs/decisions/
```

Create files lazily — only when you have something to write. If no `CONTEXT.md` exists, create one when the first term is resolved. If no `docs/decisions/` exists, create it when the first research decision record is needed.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `CONTEXT.md`, call it out immediately. "Your glossary defines 'baseline' as the covariate-assessment period, but you seem to mean the index date — which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'cohort' — do you mean the target population, study population, or analysis population? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts. For reviews and meta-analyses, include multiple reports from one cohort, multi-arm trials, repeated time points, composite outcomes, and several eligible effect estimates.

### Cross-reference with research artifacts

When the user states how something works, check whether the protocol, registration, data dictionary, extraction form, statistical analysis plan, analysis code, tables, and manuscript agree. If you find a contradiction, surface it: "Your protocol starts follow-up at treatment initiation, but the analysis uses enrollment — which is right?"

### Update CONTEXT.md inline

Before the first edit in a session, show the proposed canonical changes and ask for authorization to update the research files. Once authorized, when a term is resolved, update `CONTEXT.md` right there. Don't batch these up — capture them as they happen. Use the format in [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md).

`CONTEXT.md` should be totally devoid of operational details. Do not treat `CONTEXT.md` as a protocol, data dictionary, statistical analysis plan, or a repository for procedural decisions. It is a glossary and nothing else.

### Offer research decision records sparingly

Only offer to create a research decision record when all three are true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future collaborator will wonder "why did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the decision record. Use the format in [DECISION-FORMAT.md](./DECISION-FORMAT.md).
