Skills in this repository are intended for Research Consultancy (RC) medical research workflows.

Skill categories under `skills/`:

- `evidence-insight/`
- `protocol-design/`
- `data-analysis/`
- `academic-writing/`
- `other/`

Each distributed skill should be a downloadable `.skill` file placed in one of the five categories above.

Invocation model (Pocock-style):

- Each category `README.md` must keep separate sections for **User-invoked** and **Model-invoked** skills.
- User-invoked skills are intended to be explicitly triggered by the user.
- Model-invoked skills are reusable skills that can be invoked by the model when appropriate.

Supporting buckets are also available under `skills/`:

- `misc/`, `personal/`, `in-progress/`, `deprecated/`

Conventions:

- Keep category listings up to date in top-level `README.md`.
- Keep `.claude-plugin/plugin.json` metadata aligned with repository purpose.
