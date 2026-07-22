Skills are organized into bucket folders under `skills/`:

- `evidence-insight/` — literature discovery, appraisal, synthesis, and gap identification
- `protocol-design/` — research-question refinement, study design, and analysis planning
- `data-analysis/` — statistical programming, modeling, data preparation, and visualization
- `academic-writing/` — manuscripts, reporting, revision, and publication readiness
- `other/` — promoted general-purpose skills used in RC workflows
- `misc/` — retained but rarely used, not promoted
- `personal/` — environment-specific, not promoted
- `in-progress/` — drafts not ready to ship
- `deprecated/` — retired skills kept for historical reference

The first five buckets are promoted. Every skill in a promoted bucket must have:

1. a direct link to its `SKILL.md` in the top-level `README.md`;
2. a one-line entry linked to `SKILL.md` in its bucket `README.md`; and
3. an entry in `.claude-plugin/plugin.json`'s `skills` array.

Skills in non-promoted buckets must not appear in the top-level skill list or plugin manifest.

This repository is a single-plugin Claude Code marketplace. `.claude-plugin/marketplace.json` must list the `rc-skills` plugin with source `./`. Treat `.claude-plugin/plugin.json` as the shipped skill set and release manifest. After changing either manifest, run `claude plugin validate .`, confirm every referenced path exists, and test the plugin locally when the Claude Code CLI is available.

Each promoted bucket `README.md` must list every skill in that bucket under separate **User-invoked** and **Model-invoked** sections. Non-promoted bucket READMEs use a flat list when they contain skills.

Every skill is an expanded directory whose root contains `SKILL.md`. Supporting `agents/`, `references/`, `scripts/`, and `assets/` files belong inside that directory. Keep references one level from `SKILL.md` where practical.

Every `SKILL.md` is either:

- **User-invoked:** include `disable-model-invocation: true` and set `policy.allow_implicit_invocation: false` in `agents/openai.yaml`.
- **Model-invoked:** omit `disable-model-invocation`; keep it reachable by both the model and the user.

When adding, renaming, moving, or removing a skill, update the bucket README, top-level README, and plugin manifest in the same change. Keep `.claude-plugin/marketplace.json` and `.claude-plugin/plugin.json` aligned with the repository name, purpose, and release metadata.

## Agent skills

### Issue tracker

Issues are tracked in GitHub Issues. See `docs/agents/issue-tracker.md`.

### Triage labels

Use the five default triage labels. See `docs/agents/triage-labels.md`.

### Domain docs

This is a single-context repository. See `docs/agents/domain.md`.
