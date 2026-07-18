---
name: setup-rc-skills
description: Configure repository-level defaults used by the rest of the rc-skills workflows.
disable-model-invocation: true
---

Run this once per repository before using other skills.

## Setup checklist

1. Ask which issue tracker should be treated as source of truth (GitHub Issues, Linear, or local files).
2. Ask which labels represent triage states in this repository.
3. Ask where generated docs should be saved.
4. Confirm the selected defaults back to the user.

Do not make assumptions if any of the three values are missing.
