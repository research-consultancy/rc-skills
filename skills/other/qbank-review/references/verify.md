# Verify reference (step V)

You fact-check one finished review before the learner sees it. The learner trusts every sentence to build the medicine they will use on the exam. A wrong fact that reaches them is the worst outcome the qbank review can contain, worse than any omission.

You have the stem, source explanation and figures, attempt record, related question notes, supplied memory entries and the finished review. The source is the authority on medicine. Mark teaching added beyond the source with †; it must reflect established Step 2 CK medicine. Review units are numbered sentences and table rows (including their headers). Record the audit in the note’s Verification section as a Markdown table with columns Unit, Basis, Verdict, Type, Problem and Correction; omit error-only cells when a unit is correct.

## For each unit, in order

1. **Trace** it to what it rests on, and write that in the Basis column, quoting a short span (12 words or fewer) where one exists:
   - stem wording, source wording or a figure reference for a clinical claim;
   - the Attempt card or Captured evidence property and its recorded value for the learner's answer, cross-outs, highlights, time or mark;
   - the linked question note’s recorded outcome and answer for a unit ending in `[card <ID>]`;
   - the linked memory entry and its statement for a pattern;
   - † supplemental for a † claim;
   - application of a stated source fact to the stem for reasoning that applies a source fact to this stem.
   A table row is traced cell by cell; give the basis of the cell most likely to be wrong.
2. **Judge** the unit against that basis. It is an error when it does any of these:
   - **Contradicts** the stem, the source or a figure.
   - **Misattributes**: it gives a fact to the wrong option, drug, organism, disease or test. For example, a reason the source gives for one drug appears under another.
   - **Distorts**: it changes a threshold, number, sequence, timing or condition, flips a negation, or adds, drops or changes a qualifier such as "usually", "as early as" or "always", in a way that would change a decision.
   - **Is unsupported**: it states a clinical fact and its only basis is your own knowledge, with no † mark.
   - **Is wrong supplemental teaching**: a † claim that is inaccurate, disputed, or not how Step 2 CK tests the topic.
   - **Misstates the attempt**: it reports an answer, cross-out, highlight, time or mark that the record does not show, or retells a related attempt differently from its card.
   - **Is garbled**: it is ungrammatical, truncated or nonsensical, or a pronoun or modifier could attach a fact to the wrong entity, in a way that could mislead.

A faithful paraphrase or compression of the source is correct, and so is reasoning that applies a source fact to this stem's findings. Inferred and Less likely are hypotheses about the learner's thinking, so judge only the facts they cite and the medicine they state. A pattern is an error when the memory entries it cites do not support it.

## Output

Record one row per unit, in order, with its number, basis and verdict (OK or Error). For an error, fill the Type, Problem and Correction columns: choose a listed error type, state the issue in one sentence, and give what the stem, source, record or card actually says, quoted verbatim when available.

Done when every unit carries a basis and a verdict.


## Qualification checklist

Before release, confirm that every sentence and table row has a basis and verdict; every clinical claim is sourced or marked †; no unit contradicts, misattributes or distorts a finding, threshold, number, order, timing, condition or qualifier; no unsupported supplemental claim remains; and every account of the attempt or linked case matches its note. Check that faithful paraphrase and source-based application are accepted, hypotheses about thought are judged on their cited facts and medicine, and memory-pattern claims are supported by the cited entries. For errors, record the problem in one sentence and give the correct statement from the stem, source, attempt record or linked card. Remove an incorrect sentence if it cannot be repaired in place.


## Qualification review checklist

When qualifying a reviewer workflow, inspect both challenge cases and clean controls. Confirm that planted factual and attribution errors are identified, that valid reviews pass without unnecessary rewrites, and that clean calls do not produce false alarms. Record the number of challenge errors caught, valid reviews accepted, clean calls, and false alarms in the qualification record. Review the underlying examples when a miss or false alarm occurs; do not treat a high aggregate score as a substitute for examining the specific failure. Keep qualification evidence as a human-readable checklist alongside the verification guidance, with no application-specific transport or storage requirements.
