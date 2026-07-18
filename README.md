# rc-skills

Research Consultancy (RC) skills for AI agents, focused on medical research workflows.

This repository is modelled after the structure used in [`mattpocock/skills`](https://github.com/mattpocock/skills) so skills can be distributed and reused consistently.

## Install

```bash
npx skills@latest add AliSalman-et-al/rc-skills
```

## Repository layout

- `skills/engineering` — promoted engineering bucket (currently unused)
- `skills/productivity` — promoted productivity bucket (used for RC medical research skills)
- `skills/misc`, `skills/personal`, `skills/in-progress`, `skills/deprecated` — non-promoted buckets
- `docs/` — human-facing docs for promoted skills
- `.claude-plugin/` — Claude plugin metadata for marketplace installs

## Current promoted skills

### Productivity

**User-invoked**

- **[setup-rc-skills](./skills/productivity/setup-rc-skills/SKILL.md)** — one-time setup for configuring issue tracking, triage labels, and document location for RC medical research workflows.
