# Attempt classification (ADR 0010)

Record three separate properties. Do not use the superseded six weakness labels.

## Physician task

Classify the lead-in using USMLE Step 2 CK physician-task categories, matching the exact category wording in the question's source or current official taxonomy. This describes what the question asks, not why the learner missed it. Store one task. If the lead-in cannot be classified, use `unknown` and explain in evidence.

## Decision error

Record exactly one stage where the selected answer split from the correct path: `lead-in`, `patient picture`, `candidates`, `discrimination`, `sequence or threshold`, `data and calculation`, `correct but unstable`, or `unclear`. A correct guess-marked attempt uses `correct but unstable`. Use annotations to distinguish stages where possible; cross-outs are strongest evidence. Otherwise choose one stage and set `decision_error_confidence: likely`. Do not infer premature closure or a differential failure from highlights alone.

## Likely cause

Record one of `knowledge gap`, `weak discriminator`, `not transferred`, `process slip`, or `unknown`, with evidence and confidence (`supported` or `likely`). `Not transferred` requires memory evidence that an earlier rule covered this decision. These are hypotheses, never observed facts. If evidence does not support a cause, use unknown.

## Evidence discipline

The attempt record establishes answers, highlights, cross-outs, mark and time. The decision stage and cause are interpretations. Cite the specific record, related attempt or memory entry supporting each interpretation. Keep task, error and cause distinct; do not combine them into a single label. Old attempt cards using legacy weakness types remain historical evidence and are not rewritten.
