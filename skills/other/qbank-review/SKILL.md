---
name: qbank-review
description: Turn a completed question-bank block into evidence-grounded personalized reviews and an evolving Obsidian learning memory.
disable-model-invocation: true
---

# Qbank review

Use only when explicitly invoked. Work in the user's Obsidian vault and follow these stages in order. See linked references for detailed writing, memory and verification rules.

## Procedure

1. **Set up.** Read the platform guide in `references/platforms/`. Use the verified browser path: Playwright MCP with a persistent signed-in profile. Prefer the host agent browser (Claude in Chrome / Codex browser) when available and connected; otherwise use Playwright MCP. For Claude Code, configure it with `claude mcp add playwright npx @playwright/mcp@latest -- --user-data-dir <persistent-profile-path>`. Never request, enter, store or handle credentials. Use the named platform guide and its login URL; honor a user-named output folder, otherwise use vault-root `qbank-review/`. Have the user log in themselves. Confirm a completed block in review mode. Never capture an active test. Follow browser, screenshot and image policies in the platform guide.
2. **Load memory and prior attempts.** Before reviewing, read `qbank-review/memory/` index, active rules and patterns, and prior attempt notes for this platform/block and related topics. Use those notes as evidence, not as independent clinical authority. Select up to two related prior attempts for each review when they materially clarify a repeated decision; link them. Never claim a memory pattern without its cited evidence.
3. **Capture evidence.** Record stable QID, stem, choices, selected/correct answer, explanation, objective, highlights, cross-outs, marked status, time, peer percentages and images. Preserve exact evidence; use `unknown`/`not shown` when unavailable. Obey screenshots policy; do not infer missing fields. See platform guides.
4. **Draft cards for the block.** Record a one-sentence case recap and, when incorrect/marked/omitted, the likely decision reconstruction. Classify with the current three-part scheme in `references/classification.md`: physician task, decision error and likely cause. Keep observed facts distinct from inference.
5. **Review in batches.** Process about 5–10 questions at a time. Skip any QID whose note has `status: final`; resume the rest. Read the complete source, including options, tables and figures, for each item. Draft compact reinforcement for correct unmarked attempts and full review for incorrect, marked or omitted attempts. Apply `references/review.md`, `references/stem-annotations.md`, and `references/examples.md`.
6. **Verify and finalize each note.** Apply `references/verify.md` independently. Fix errors, then write each verified question note immediately with `status: final`, evidence, card, review, classification and links. Do not mark a failed or incomplete review final.
7. **Apply memory once per block.** For a full run, apply memory only after every question note in the block is final. For a requested first N (or other subset), review and finalize that subset, then apply memory deltas only from those reviewed items at run end; record `scope: partial (N of M)` in the summary. A later run on the rest skips `status: final` notes and applies its own deltas. Never claim block-level patterns from a partial set. Never rewrite attempt notes or reviews as memory evolves. Follow `references/memory.md`.
8. **Write summary and dashboard.** Add score, links, capture gaps and memory delta to the block summary. Create/update `qbank-review/Dashboard.base` from `references/note-templates.md`, or its Dataview fallback. Group by system, physician task and decision error; include incorrect/marked items by date.

## Layout and completion

Use `qbank-review/<platform>/<block-id>/<qid> - <short topic>.md`, `summary.md`, `qbank-review/memory/`, platform maps under `qbank-review/platforms/`, and `qbank-review/Dashboard.base`. Follow `references/note-templates.md` exactly for properties and sections.

Complete when the requested subset has verified final notes, the scoped summary, flashcards and dashboard are updated, subset memory deltas have been applied once after finalization, and links resolve. Report the block path and evidence gaps. If login or required source access is unavailable, stop that dependent work and report the obstacle.
