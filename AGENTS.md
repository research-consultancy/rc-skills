Skills are organized into bucket folders under `skills/`:

- `engineering/` — promoted engineering skills
- `productivity/` — promoted productivity skills
- `misc/`, `personal/`, `in-progress/`, `deprecated/` — non-promoted buckets

Conventions:

- Every skill lives in `skills/<bucket>/<skill-name>/SKILL.md`.
- Promoted skills (`engineering/`, `productivity/`) are listed in:
  - top-level `README.md`
  - `.claude-plugin/plugin.json` `skills` array
- Promoted skills also have docs pages under `docs/<bucket>/<skill-name>.md`.
