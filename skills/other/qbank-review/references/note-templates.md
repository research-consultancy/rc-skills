# Obsidian note templates

## Question note

Filename: `<qid> - <short topic>.md`. Keep the `qid` property and `aliases` property; include `source_url` and a visible `[Open in <platform>](<source_url>)` link under Links.

```yaml
---
platform: "<platform>"
block: "<block-id>"
qid: "<stable-qid>"
aliases:
  - "<qid> - <short topic>"
source_url: "<review-mode question URL or block URL + item number>"
system: "<system or Unknown>"
subject: "<subject or Unknown>"
topic: "<topic or Unknown>"
result: incorrect # correct | incorrect | marked-correct | marked-incorrect | omitted
physician_task: "<task category or unknown>"
decision_error: "<stage or unclear>"
decision_error_confidence: supported # supported | likely | unknown
likely_cause: "<cause or unknown>"
likely_cause_confidence: supported # supported | likely | unknown
time_s: 0
pct_correct: 0
date: 2026-01-01
status: final # draft | final
tags:
  - qbank-review
---
```

Write headings exactly as shown; never prefix a heading with another heading marker.

Unavailable numbers are YAML 
ull`; unavailable classifications use `unknown`. Values: decision error is one of `lead-in`, `patient picture`, `candidates`, `discrimination`, `sequence or threshold`, `data and calculation`, `correct but unstable`, `unclear`; cause is `knowledge gap`, `weak discriminator`, 
ot transferred`, `process slip`, `unknown`. Include headings: Captured evidence, Attempt card, Classification, Personalized review, Verification, Links. Store the stem/source or a durable citation sufficient to audit claims. In Captured evidence, include a Source coverage table with columns Unit, Home, Keep and Source citation; list exact numbers, thresholds, comparison signs and qualifiers in Keep. Preserve each unit’s facts in its named section. Notes with `status: final` are immutable and skipped on rerun.

## Dashboard.base

Save the following as `<root>/Dashboard.base`. This uses Bases' documented `filters`, `formulas`, `views`, `filters`, `groupBy`, `sort` and `properties` structure. Filter `file.folder` to the question-note folder; use the resolved `<root>`.

```yaml
filters:
  and:
    - 'file.inFolder("<root>")'
    - 'status == "final"'
formulas:
  review_result: 'if(result == "incorrect" || result == "marked-incorrect" || result == "marked-correct" || result == "omitted", "Review", "Reinforce")'
properties:
  file.name:
    displayName: Question
  physician_task:
    displayName: Physician task
  decision_error:
    displayName: Decision error
  likely_cause:
    displayName: Likely cause
views:
  - type: table
    name: By system
    groupBy:
      property: system
      direction: ASC
    order:
      - file.name
      - date
      - result
      - physician_task
      - decision_error
  - type: table
    name: By physician task
    groupBy:
      property: physician_task
      direction: ASC
    order:
      - file.name
      - date
      - result
      - system
      - decision_error
  - type: table
    name: By decision error
    groupBy:
      property: decision_error
      direction: ASC
    order:
      - file.name
      - date
      - system
      - physician_task
      - likely_cause
  - type: table
    name: Incorrect and marked
    filters:
      or:
        - 'result == "incorrect"'
        - 'result == "marked-incorrect"'
        - 'result == "marked-correct"'
        - 'result == "omitted"'
    sort:
      - property: date
        direction: DESC
    order:
      - file.name
      - date
      - system
      - physician_task
      - decision_error
      - likely_cause
```

## Dataview fallback

Add to `<root>/Dashboard.md` when Bases is unavailable:

```dataview
TABLE date, result, physician_task, decision_error, likely_cause
FROM "<root>"
WHERE status = "final"
GROUP BY system
SORT date DESC
```

```dataview
TABLE date, system, result, decision_error, likely_cause
FROM "<root>"
WHERE status = "final"
GROUP BY physician_task
SORT date DESC
```

```dataview
TABLE date, system, result, physician_task, likely_cause
FROM "<root>"
WHERE status = "final"
GROUP BY decision_error
SORT date DESC
```

```dataview
TABLE date, system, physician_task, decision_error, likely_cause
FROM "<root>"
WHERE status = "final" AND (result = "incorrect" OR result = "marked-incorrect" OR result = "marked-correct" OR result = "omitted")
SORT date DESC
```

## Summary

Include score and denominator, links to every question, capture gaps, memory delta link, and evidence-backed patterns/rules held. The block summary is written after all question notes are final.

## Flashcards

Save cards in `<root>/flashcards/<platform>-<block>.md` and include the `#flashcards` tag. Create one card per correction rule from finalized incorrect or marked attempts, using the Spaced Repetition single-line syntax `question::answer`. End each card with a wikilink to its question note.

Example:

```markdown
#flashcards

When [specific trigger], what action applies and what boundary changes it?::[Action and boundary.] [[<qid> - <short topic>]]
```