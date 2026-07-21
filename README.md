# Skills for Rigorous Medical Research

[![skills.sh](https://skills.sh/b/AliSalman-et-al/rc-skills)](https://skills.sh/AliSalman-et-al/rc-skills)

Practical agent skills for planning, searching, reviewing, and communicating medical research.

Good research depends on decisions that an agent should not make silently: what question is actually being asked, whether a synthesis is worth doing, how evidence will be found, and whether a manuscript supports its claims. These skills turn those decisions into explicit, repeatable workflows while keeping the researcher in control.

The initial collection focuses on meta-analysis topic development, PubMed searching, evidence discovery, shared research terminology, teaching, and manuscript review. Skills are small, composable, and work with agents that support the Agent Skills format.

## Quickstart (30-second setup)

1. Run the installer:

```bash
npx skills@latest add AliSalman-et-al/rc-skills
```

2. Choose the skills and supported agents you want to install them into.

3. Invoke a user-invoked skill, such as `/build-pubmed-search` or `/grill-meta-analysis-topic`, from your agent.

## Install as a Claude Code plugin

Use the native plugin when you want the complete collection as a managed bundle.

Inside Claude Code:

```text
/plugin marketplace add AliSalman-et-al/rc-skills
/plugin install rc-skills@AliSalman-et-al
```

Or from your shell:

```bash
claude plugin marketplace add AliSalman-et-al/rc-skills --scope user
claude plugin install rc-skills@AliSalman-et-al --scope user
```

The default `user` scope makes the skills available across projects. Use `--scope project` to share the configuration with collaborators in one project, or `--scope local` for one local checkout.

Plugin skills use the plugin namespace. For example:

```text
/rc-skills:build-pubmed-search
/rc-skills:grill-meta-analysis-topic
/rc-skills:teach
```

Check or update the installation from your shell:

```bash
claude plugin list
claude plugin update rc-skills@AliSalman-et-al --scope user
```

Restart Claude Code after an update.

Two installation styles are available:

- **[skills.sh](https://skills.sh/AliSalman-et-al/rc-skills)** copies selected skills into your environment so you can inspect and adapt them.
- **The Claude Code plugin** installs the repository as a managed collection that follows published updates.

## Why these skills exist

### The research question is still ambiguous

A plausible topic can conceal unresolved choices about the population, exposure or intervention, comparator, outcomes, study designs, and contribution. Starting the protocol before resolving them pushes ambiguity downstream.

Use [`/grill-meta-analysis-topic`](./skills/protocol-design/grill-meta-analysis-topic/SKILL.md) to sharpen the question, investigate prior syntheses, and determine whether the proposed meta-analysis is distinct and feasible.

### The search looks reasonable but misses evidence

A few keywords are not a reproducible search strategy. PubMed searches need explicit concept blocks, controlled vocabulary, free-text synonyms, validation against known studies, and checks for indexing lag and unintended query translation.

Use [`/build-pubmed-search`](./skills/evidence-insight/build-pubmed-search/SKILL.md) for a guided search-design session. It grills the topic, constructs the query, tests it against live PubMed results, and returns a copy-ready search string. The reusable [`pubmed`](./skills/evidence-insight/pubmed/SKILL.md) skill handles literature retrieval and verification.

### The project uses the same words for different things

Terms such as _baseline_, _cohort_, _outcome_, and _effect_ can silently change meaning across a protocol, registry, extraction form, analysis plan, and manuscript.

The model-invoked [`domain-modeling`](./skills/other/domain-modeling/SKILL.md) skill aligns constructs, estimands, cohort boundaries, and consequential methodological decisions into a shared language.

### The manuscript is polished but not submission-ready

Grammar is only one layer of manuscript quality. Claims must match the results, statistical reporting must be coherent, tables and figures must agree with the text, and the submission package must be complete.

Use [`proofread-manuscript`](./skills/academic-writing/proofread-manuscript/SKILL.md) for a structured pre-submission audit.

## Reference

Skills are divided by who can invoke them:

- **User-invoked skills** run when you explicitly select them. They orchestrate an interactive research workflow.
- **Model-invoked skills** can be selected automatically when a task matches their purpose. They provide reusable research disciplines that other skills can call.

A user-invoked skill may call model-invoked skills, but not another user-invoked skill.

### Evidence Insight

Literature discovery, search design, and evidence verification.

**User-invoked**

- **[build-pubmed-search](./skills/evidence-insight/build-pubmed-search/SKILL.md)** — Grill a meta-analysis question and produce a tested, copy-ready PubMed search string.

**Model-invoked**

- **[pubmed](./skills/evidence-insight/pubmed/SKILL.md)** — Search and verify biomedical literature with reproducible PubMed queries.
- **[research](./skills/evidence-insight/research/SKILL.md)** — Investigate a medical research question from high-trust primary sources and save cited findings.

### Protocol Design

Research-question refinement, feasibility, and study planning.

**User-invoked**

- **[grill-meta-analysis-topic](./skills/protocol-design/grill-meta-analysis-topic/SKILL.md)** — Test whether a meta-analysis topic is distinct, meaningful, and feasible against published and registered research.

### Academic Writing

Manuscript quality control and submission readiness.

**Model-invoked**

- **[proofread-manuscript](./skills/academic-writing/proofread-manuscript/SKILL.md)** — Audit a medical manuscript and submission package before journal submission.

### Cross-cutting

Reusable practices that support multiple stages of medical research.

**User-invoked**

- **[grill-me](./skills/other/grill-me/SKILL.md)** — Start a relentless one-question-at-a-time interview about a plan or decision.
- **[teach](./skills/other/teach/SKILL.md)** — Learn medical research methods through a stateful, evidence-grounded teaching workspace.

**Model-invoked**

- **[grilling](./skills/other/grilling/SKILL.md)** — Apply the reusable one-question-at-a-time grilling discipline.
- **[domain-modeling](./skills/other/domain-modeling/SKILL.md)** — Align medical research terminology, constructs, estimands, and consequential decisions.

## Repository structure

Skills live under `skills/` in five categories:

- `evidence-insight/`
- `protocol-design/`
- `data-analysis/`
- `academic-writing/`
- `other/`

Each skill is an expanded directory containing `SKILL.md` and any references or agent metadata it needs. Claude Code distribution metadata lives in `.claude-plugin/`.
