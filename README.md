# rc-skills

Research Consultancy (RC) skills for AI agents, focused on medical research workflows.

## Install

```bash
npx skills@latest add AliSalman-et-al/rc-skills
```

## Skill categories

1. **Evidence Insight** — search strategy design, database selection, evidence-level prioritization, critical appraisal, literature synthesis, and gap identification.
2. **Protocol Design** — experimental design generation, study type selection, causal inference planning, statistical power calculation, and validation strategy.
3. **Data Analysis** — R/Python bioinformatics code generation, statistical modeling, data cleaning pipelines, machine learning workflows, and result visualization.
4. **Academic Writing** — SCI manuscript drafting, methods/results/discussion writing, meta-analysis narrative, cover letters, and abstract generation.
5. **Other (General / Non-Research)** — general skills that do not fall into categories 1–4.

Each category maintains separate **User-invoked** and **Model-invoked** sections in its `README.md`.

## Repository layout

- `skills/evidence-insight` — Evidence Insight `.skill` files
- `skills/protocol-design` — Protocol Design `.skill` files
- `skills/data-analysis` — Data Analysis `.skill` files
- `skills/academic-writing` — Academic Writing `.skill` files
- `skills/other` — General/non-research `.skill` files
- `skills/misc`, `skills/personal`, `skills/in-progress`, `skills/deprecated` — supporting buckets
- `.claude-plugin/` — Claude plugin metadata for marketplace installs

## Inspiration

- https://github.com/FreedomIntelligence/OpenClaw-Medical-Skills
- https://github.com/aipoch/medical-research-skills
- https://github.com/Aperivue/medsci-skills
