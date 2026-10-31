# Review reference (step B)

You write one attempt's review and its card. The question note carries the attempt header and option labels, selection/correctness and peer percentages in Captured evidence. Write the review in Personalized review; use `[[qid|case description]]` wikilinks for related notes.

## Two kinds of review

- **Compact**: a correct, unmarked attempt. It **reinforces**. Read it as the educational objective plus a glance at the other options, in about a minute: **150 words at most**. Map to the Source coverage table in Captured evidence every source unit that does not fit and does not decide this question or an option's discriminator.
- **Full**: an incorrect, Marked or omitted attempt. It is built for the **a-ha**: the learner sees the medicine, then sees where their own reasoning left it, and leaves with the rule that would have saved them. It carries the whole source and has about five minutes and **600 words maximum of review prose**.

Both use the same sections in the same order, and each fact has one home. A later section names an earlier fact ("the fontanelle findings") rather than teaching it again. The Take away is the home of the rule this attempt turned on.

## Steps

1. **Read the source until you could teach every point in it**: its prose, every table row, every figure panel, each option's explanation and its educational objective. Done when you know where each point will go in the review, or, in a compact review, which few you will leave to the source citation because they bear on neither this decision nor any option's discriminator.
2. **Reconstruct the thought path** (full reviews). Find the most likely decision path that produces the selected answer and every cross-out. Use everything recorded:
   - what the learner highlighted, and what they passed over;
   - what they crossed out, and what they left standing;
   - their time against their usual pace;
   - the guess mark;
   - how peers answered;
   - their memory and related attempts.

   Done when the path explains the choice and every cross-out, contradicts no highlight, and names the moment it left the correct path.
3. **Write the sections.**
   Count words before finalizing; trim to the applicable budget (150 words maximum for compact reviews, 600 words maximum for full review prose).
4. **Map the source.** The source comes split into numbered units: each sentence, and each table row with its column headers. In Source coverage table, give every unit its home: the section that carries its facts (Bottom line, Correction rules, Clinical explanation, Options entry for <label>, Likely thought path or Take away). List in `keep` the unit's exact numbers, thresholds and comparison signs (">3 months"), and its hedge and frequency words ("likely", "usually", "occasionally", "as early as"). Write each `keep` item into its home verbatim. An association stays an association, a list of examples stays a list, and cause runs in the direction the source states. A unit that teaches nothing — an abbreviation key, an image credit, a table caption that repeats its rows — goes to the source citation in Captured evidence in any review. In a compact review only, a unit may instead go to the source citation in Captured evidence, when it bears on neither this decision nor any option's discriminator. Then reread each home, and confirm that it states the unit's facts with the source's numbers and qualifiers ("as early as", "usually", "severe") and about the same entity. Done when every unit has a home that holds it, and every clinical sentence in the review states the source's fact.

## Sections

**Title.** One line naming the diagnosis or decision: "Congenital hypothyroidism presenting as neonatal constipation".

**Bottom line.** Open with the case in one sentence: the patient, the deciding findings with the stem's numbers, and what the question asked. Then give the answer and why this patient's findings make it the answer, naming every finding the source cites as a reason, including responses to treatment. A full review adds the key management point.

**Correction rules** (full). Further decisions the learner can apply to the next question, each with its trigger, action and boundary, plus timing and sequence for management. List none when the Take away is the only rule the attempt teaches.

**Clinical explanation** (full). The source teaching that has no other home, in the order Step 2 asks about it: recognition, the confirming test, management, then complications.
- Group findings so they recall as a set.
- When three or more causes or options compare on the same features, end with a Markdown table, and keep each option's entry to its verdict.
- For a video exhibit, teach from the source's description, and say once that the video was not analyzed.

**Options.** One entry per option, starting with the clinical point.

- **Compact.** The correct answer's entry carries the source's remaining Step 2 points for this decision. Each wrong option gets one sentence naming what it is and its discriminator, with every member of a discriminating set, such as the HUS triad.
- **Full.** The selected answer, the correct answer and every option left standing get enough to settle the choice: what the option is, and the stem finding that rules it in or out. A crossed-out option gets one line. A crossed-out correct answer gets the full treatment.
- **When the clinical explanation has a comparison table**, the table holds the options' features. Each option entry then applies its row to this stem in one sentence, and adds only source teaching about that option that the table lacks.
- The strongest wrong-option line names the feature that would have made it right: "That fits functional constipation, which means hard, infrequent stools with a normal exam."

**Likely thought path** (full). This is where the learner meets their own reasoning, so it refers to the medicine by name and spends its words on the path.

- *Observed*: The Captured evidence and Attempt card sections record the answer, cross-outs, mark, time and peer split. You write what the highlights show: quote or name only text inside a highlight, and describe a deciding finding outside every highlight as unhighlighted. An omitted attempt has only this part.
- *Inferred*: the reconstruction in two to four decisive sentences, ending on the moment the path diverged. For a Marked correct attempt, explain what most likely made the learner unsure.
- *Less likely*: one alternative path in one sentence.
- *Your pattern*: available only when memory entries are supplied. Cite the entries it rests on, state the principle, then retell at most two cases that show it. The linked question note carries its own answer and outcome. State why that case connects here, preserving the card's hedge; leave its answer and outcome to the wikilink.

**Connection** (compact). One or two sentences that retell a related attempt or pattern and link it to this case, when one qualifies. The linked question note carries its own answer and outcome. State why that case connects here, preserving the card's hedge; leave its answer and outcome to the wikilink.

**Take away.** One sentence: the rule this attempt turned on, general enough to use on the next question and specific enough to act on. It ends the review.

## Card

The question note is the durable record of this attempt:
The Attempt card section contains a one-sentence case recap and, for incorrect or marked attempts, a one-sentence likely reconstruction grounded in recorded evidence. In Classification, record the ADR 0010 physician task, decision error and likely cause as three distinct YAML properties; do not use legacy weakness labels.

## Fixing a review

State the medicine itself. The learner never sees the word "source"; write the fact, not who said it.

Rewrite the flagged sentence so it states the correct fact in the review's voice; use `correct` for the facts, not as text to quote.

When the fact-check returns errors, you receive your review and the list. Rewrite only the flagged sentences so each says what the stem or source says, using the `correct` text. When a sentence cannot be made correct in its place, delete it. Leave every other sentence exactly as it was.
