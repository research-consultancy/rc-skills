# Worked examples

These three fictionalized teaching cases demonstrate the evidence-first voice, density, section placement, and good-versus-bad reasoning. Clinical wording below is newly written and illustrative; it does not reproduce a qbank stem or explanation. Each output is a question note with YAML properties, Markdown sections and Obsidian links. Replace every illustrative detail with the supplied attempt record and source. The examples correspond to: an incorrect answer without cross-outs; an incorrect answer after crossing out the correct choice; and a correct, unmarked answer with a useful connection.

Use the note template as the canonical property list. The excerpted notes below show how the fields are populated and where the review prose belongs. Captured evidence preserves what was actually supplied; Personalized review contains the teaching; Verification records the independent audit.

# Example 1: Incorrect attempt, no cross-outs

## Evidence used to draft

A young infant has infrequent firm stools, delayed first stool after birth, poor weight gain and sleepiness during feeds. Examination records a broad fontanelle, puffy features and low tone, with a soft abdomen and reassuring rectal examination. The learner selected a test for cystic fibrosis; thyroid studies are correct. The attempt was unmarked, with no cross-outs. The learner highlighted the delayed first stool and the unusual facial and neurologic findings. The source explanation links the pattern to congenital hypothyroidism, notes that many affected infants look well at birth, and states that testing shows high TSH with low T4. It recommends prompt levothyroxine. Competing explanations include obstruction or Hirschsprung disease, cystic fibrosis and functional constipation.

The good reasoning notices that a plausible bowel clue and poor growth do not explain the whole examination. The error is not simply “missed diagnosis”: the review should identify how the selected answer leaves the fontanelle, facial appearance and tone findings unaccounted for. A contrasting weaker reconstruction would claim the learner ignored all neonatal history or knowingly chose an answer they had crossed out; neither is supported by this record.

## Output note

---
platform: "Illustrative qbank"
block: "practice-block-a"
qid: "infant-bowel-case"
system: "Pediatrics"
subject: "Gastrointestinal & Nutrition"
topic: "Neonatal constipation"
result: incorrect
physician_task: "Establish the diagnosis"
decision_error: discrimination
decision_error_confidence: supported
likely_cause: weak discriminator
likely_cause_confidence: likely
time_s: 132
pct_correct: 67
date: 2026-10-31
status: final
tags:
  - qbank-review
---

## Captured evidence

- Selected: cystic fibrosis testing. Correct: thyroid function studies. No options were crossed out; the attempt was not marked.
- Highlights included the delayed first stool and the broad fontanelle, puffy facial appearance and low tone. The timing of first stool, weight trajectory, feeding behavior, temperature, heart rate and examination should be retained as recorded.
- Source citation: supplied explanation and its diagnostic summary.
- Deciding findings: delayed meconium passage plus a cluster of enlarged fontanelle, puffy face and hypotonia. Source support: congenital hypothyroidism can cause delayed passage and the listed hypometabolic / developmental findings.

## Attempt card

The infant with delayed stool passage, poor growth and a characteristic low-metabolic examination was asked which test would establish the cause. The likely misstep was allowing constipation and growth concerns to make cystic fibrosis seem sufficient while leaving the fontanelle, facial appearance and tone unexplained.

## Classification

The lead-in asks for a diagnosis-establishing test, so physician task is the exact task category supported by the source taxonomy. The selected test split from the correct path when comparing candidates against the distinguishing physical findings. Weak discriminator is a likely cause, not an observed fact: the record supports that the winning explanation did not account for all highlighted findings.

## Personalized review

### Congenital hypothyroidism presenting as neonatal constipation

**Bottom line.** A young infant with delayed passage of the first stool, persistent constipation, feeding difficulty and little weight gain has a broad fontanelle, puffy features and reduced tone. The question asks which test establishes the diagnosis. This constellation points to congenital hypothyroidism; thyroid studies show increased TSH with decreased T4. Begin levothyroxine promptly because treatment in the neonatal period prevents lasting neurologic harm.

- Delayed passage of meconium is abnormal for most newborns. Hirschsprung disease and cystic fibrosis account for many cases; the physical examination helps distinguish other causes.
- **When a highlighted finding does not fit the leading answer, reopen the differential and account for it before committing.**

**Clinical explanation.** Thyroid dysgenesis, including absent, underdeveloped or ectopic gland tissue, is the commonest cause. Many newborns initially appear well because maternal thyroid hormone crosses the placenta; symptoms can emerge over the following weeks as that contribution falls. A minority have reduced gut motility early, with delayed passage of stool. Reduced metabolism can cause a low heart rate and temperature, lethargy, poor feeding, hypotonia, constipation, prolonged jaundice and poor growth. Mucopolysaccharide accumulation contributes to a puffy face, enlarged tongue and umbilical hernia. Delayed skeletal maturation enlarges the fontanelles. Untreated disease can impair development and growth.

| Cause | Findings that support it | Useful evaluation |
|---|---|---|
| Congenital hypothyroidism | Broad fontanelle, puffy features, low tone, feeding and growth difficulty | TSH and T4 |
| Cystic fibrosis with meconium ileus | Delayed stool and poor growth; characteristic facial and fontanelle findings are not expected | Sweat chloride testing when indicated |
| Hirschsprung disease | Obstructive symptoms, distension or abnormal rectal findings | Imaging and confirmatory rectal biopsy as indicated |
| Functional constipation | Hard, infrequent stools with otherwise reassuring examination and no organic warning signs | No further testing when criteria are met |

- **Selected option: cystic fibrosis testing.** It could explain delayed stool and poor growth, but does not account for the fontanelle, puffy features and hypotonia.
- **Correct option: thyroid function studies.** Increased TSH with decreased T4 confirms the suspected disorder.
- Abdominal imaging or rectal biopsy addresses obstruction or Hirschsprung disease; the benign abdominal and rectal examination makes those less compelling here.
- No further testing is appropriate only when the presentation supports functional constipation without warning findings.

### Likely thought path

**Observed.** The learner highlighted delayed stool passage and the fontanelle / face / tone cluster. No cross-outs or guess mark were recorded.

**Inferred.** Delayed stool passage may have brought cystic fibrosis to mind, and poor growth made that candidate plausible. The examination's soft abdomen and normal rectal findings reduced support for an obstructive process. The path diverged when the unusual fontanelle, facial appearance and tone were not used to compare cystic fibrosis with a systemic cause.

**Less likely.** The learner may have recognized hypothyroidism but chosen a bowel-focused test because the presenting complaint was constipation; the supplied annotations do not establish this.

**Connection.** An earlier infant question about delayed stool passage and obstructive findings would connect only if its supplied card shows the same specific decision boundary. Link it here as [[obstructive-infant-case|the earlier infant case]] and describe the shared feature without asserting an unsupported pattern.

> **Take away.** In an infant with delayed stool passage, a broad fontanelle, puffy features and hypotonia should prompt thyroid studies rather than an explanation limited to bowel symptoms.

### Tempting but weak alternatives

**Weak:** “You forgot the diagnosis because you do not know pediatrics.” This invents a knowledge deficit and gives no actionable trigger. **Stronger:** “The bowel and growth clues made cystic fibrosis plausible, but the highlighted fontanelle and tone findings were not reconciled with it.” This is tied to this attempt and identifies the missed comparison.

# Example 2: Incorrect attempt, correct answer crossed out

## Evidence used to draft

An older adult with several months of persistent upper abdominal discomfort, nausea, possible weight loss and microcytic anemia has an enlarged liver, low albumin and abnormal liver enzymes. Bilirubin and lipase are not elevated, and eosinophils are not increased. The patient has lived in East Asia earlier in life and visits family there. The learner selected a parasitic infection and crossed out gastric malignancy, along with several other options. The source explanation connects the anemia and upper abdominal symptoms to gastric cancer and the liver findings to metastases. It describes evaluation by upper endoscopy with biopsy followed by staging imaging.

This example demonstrates why the review must mention the correct answer’s cross-out explicitly. A negative history of visible bleeding does not rule out slow occult blood loss. The travel history makes a parasite conceivable, but it does not explain the full liver profile; the low eosinophil count also weakens that choice. A sound reconstruction accounts for both the incorrect selection and why the right option was rejected, while keeping inference labeled as inference.

## Output note

---
platform: "Illustrative qbank"
block: "practice-block-b"
qid: "upper-abdominal-anemia-case"
system: "Medicine"
subject: "Gastrointestinal & Nutrition"
topic: "Gastric malignancy"
result: incorrect
physician_task: "Identify the most likely cause"
decision_error: discrimination
decision_error_confidence: supported
likely_cause: weak discriminator
likely_cause_confidence: likely
time_s: 206
pct_correct: 40
date: 2026-10-31
status: final
tags:
  - qbank-review
---

## Captured evidence

- Selected: hookworm infection. Correct: gastric cancer. The learner crossed out the correct option and several alternatives.
- Highlighted: persistent epigastric symptoms, possible weight loss, travel history, enlarged liver, anemia measures, albumin and liver enzymes. Eosinophil count and absence of visible bleeding were not highlighted.
- Deciding findings: persistent epigastric symptoms with microcytic anemia, plus hepatomegaly and abnormal liver tests. Source supports gastric cancer with occult bleeding and liver spread.

## Attempt card

An older adult with persistent epigastric symptoms, microcytic anemia and liver abnormalities was asked for the most likely cause. The likely misstep was crossing out gastric cancer after treating travel as a stronger explanation than the anemia and liver findings together.

## Classification

Use the exact physician-task category supported by the lead-in. The answer split occurred while discriminating among candidate causes. A weak discriminator is a likely interpretation; travel and the selected answer are observed, whereas the weighting of those clues is inferred.

## Personalized review

### Gastric cancer with likely liver involvement

**Bottom line.** An older adult with persistent epigastric discomfort, nausea, possible weight loss, microcytic anemia, hepatomegaly, low albumin and abnormal liver enzymes is asked for the likely cause. Gastric cancer can explain slow occult blood loss and liver involvement. Evaluation generally starts with upper endoscopy and biopsy, followed by imaging to assess spread.

- In older adults, newly recognized iron-deficiency anemia warrants evaluation for gastrointestinal blood loss even without visible blood. A negative stool blood test alone does not exclude an occult source.
- **Before eliminating an option, check that the remaining choice explains each important abnormality.**

**Clinical explanation.** Gastric cancer risk is elevated in people from several regions, including East Asia; diet, Helicobacter pylori, pernicious anemia and smoking are among associated risks. Symptoms often become apparent after a tumor has grown: persistent upper abdominal pain, reduced intake or early satiety, weight loss, nausea or vomiting. Slow bleeding from fragile tumor vessels can produce iron-deficiency anemia without obvious gastrointestinal blood. Liver spread can cause hepatomegaly, abnormal alkaline phosphatase and transaminases, and reduced albumin. Endoscopy permits visualization and biopsy; staging imaging follows to assess metastatic disease.

| Candidate | Pain pattern | Liver or blood clues | Fit to this case |
|---|---|---|---|
| Gastric cancer | Persistent epigastric discomfort | Microcytic anemia from slow blood loss; liver findings can reflect spread | Explains the combined pattern |
| Hookworm | Abdominal symptoms may occur | Chronic blood loss can cause anemia; eosinophilia is common | Low eosinophils and liver abnormalities weaken it |
| Pancreatic cancer | Often radiates toward the back | Biliary obstruction often raises bilirubin; gut bleeding is not typical | Normal bilirubin and anemia pattern weaken it |
| Chronic pancreatitis | Often radiates to the back and worsens after meals | Anemia and hepatomegaly are not typical | Missing usual history and pattern |
| Chronic viral hepatitis | Nausea and weight loss may occur | Mild transaminase elevation | Does not account well for focal epigastric symptoms and anemia |
| Duodenal ulcer | Pain often occurs hours after eating | Liver abnormalities are not expected | Food-independent symptoms and liver findings argue against it |

- **Correct option: gastric cancer (crossed out).** It accounts for the progressive upper abdominal symptoms, anemia and liver abnormalities.
- **Selected option: hookworm.** It can cause gastrointestinal blood loss and anemia, but the low eosinophil fraction and liver findings are poorly explained.
- Pancreatic cancer may affect liver tests when it blocks bile flow, usually with jaundice; it does not typically explain occult gastrointestinal blood loss.
- Chronic pancreatitis more often causes back-radiating, meal-related pain and has different risk factors.
- Chronic hepatitis can produce mild enzyme changes but does not fit the whole symptom and anemia pattern.
- Duodenal ulcer pain has a characteristic relation to meals; it does not explain hepatomegaly and liver enzyme changes.

### Likely thought path

**Observed.** The learner selected hookworm and crossed out gastric cancer. Travel, weight change, hepatomegaly, anemia and liver tests were highlighted. Eosinophils and the lack of visible bleeding were not highlighted.

**Inferred.** Travel may have made a parasite salient, and microcytic anemia seemed to support chronic intestinal blood loss. The liver findings could then have been treated as separate or incidental. The path diverged when gastric cancer was removed despite its ability to explain the anemia and liver abnormalities together.

**Less likely.** The learner may have decided that malignancy was unlikely because the patient did not report visible bleeding; the record does not establish that this was the reason for the cross-out.

**Your pattern.** Add a pattern only if supplied memory entries show the same concrete trigger and action across two distinct questions. A broad statement such as “travel distracts you” is not established by this single card.

> **Take away.** In an older adult with microcytic anemia, persistent epigastric symptoms and liver abnormalities, keep gastric cancer in consideration even without visible bleeding.

### Weak and strong reconstruction contrast

**Weak:** “You always choose parasites when you see travel.” One item cannot support “always,” and travel history is not the same as a demonstrated repeated pattern. **Strong:** “Travel and anemia made hookworm plausible, but the selected answer left hepatomegaly and abnormal liver tests unexplained; gastric cancer could account for both the anemia and liver findings.” This explains the choice and the crossed-out correct answer while preserving uncertainty.

# Example 3: Correct attempt, useful connection

## Evidence used to draft

An older woman reports fatigue and exertional breathlessness. Laboratory testing shows microcytosis, low ferritin and low serum iron with elevated iron-binding capacity. A stool blood test is negative once. The question asks for the next management step. She selects bidirectional endoscopy, which is correct. The source explanation says older adults with iron-deficiency anemia should be evaluated for gastrointestinal blood loss despite one negative occult blood test. It distinguishes this from marrow biopsy, evaluation for celiac disease in a fitting presentation, echocardiography for suspected severe valve disease, and localization scans for active bleeding. A related supplied question note concerns an older man whose anemia and no-visible-blood history led him away from gastric cancer.

A correct compact review reinforces the decision without turning into a full lecture. Its connection should name the shared lesson and link the other note, but leave the previous outcome to the link. “You were right” is not the lesson; the reusable rule is that one negative occult blood test cannot close the investigation in a patient with new iron deficiency.

## Output note

---
platform: "Illustrative qbank"
block: "practice-block-c"
qid: "older-adult-iron-deficiency-case"
system: "Medicine"
subject: "Hematology"
topic: "Iron-deficiency anemia"
result: correct
physician_task: "Determine the next step in management"
decision_error: unclear
decision_error_confidence: unknown
likely_cause: unknown
likely_cause_confidence: unknown
time_s: 124
pct_correct: 64
date: 2026-10-31
status: final
tags:
  - qbank-review
---

## Captured evidence

- Selected and correct: colonoscopy and upper endoscopy. Not marked. A single stool occult-blood test was negative.
- Highlights included age, fatigue and breathlessness, murmur, hemoglobin, MCV, ferritin, serum iron, iron-binding capacity and the management lead-in.
- Source citation: supplied anemia evaluation explanation.

## Attempt card

An older woman with laboratory-confirmed iron-deficiency anemia and one negative stool blood test was asked for the next management step.

## Classification

Classify the task using the exact supported physician-task category. Because the answer was correct and unmarked, record `unclear` for decision_error when no split from the correct path occurred; do not invent an error cause for a correct unmarked attempt.

## Personalized review

### New iron deficiency in an older adult

**Bottom line.** An older woman with fatigue and exertional breathlessness has microcytosis, low ferritin and serum iron, and elevated iron-binding capacity. The question asks for the next step. New iron-deficiency anemia in an older adult warrants evaluation for gastrointestinal blood loss with colonoscopy and upper endoscopy, even after one negative stool blood test.

- **Colonoscopy and upper endoscopy (selected and correct).** They evaluate for gastrointestinal causes such as polyps, cancer and vascular lesions. A single negative occult-blood test does not rule out intermittent or occult bleeding.
- **Echocardiography.** A systolic murmur can have several causes; the supplied examination detail does not override the established iron-deficiency workup.
- **Celiac serology.** Consider when age and associated gastrointestinal symptoms support malabsorption.
- **Tagged red-cell imaging.** This localizes active bleeding and is not the initial evaluation of chronic iron deficiency without active hemorrhage.
- **Bone marrow biopsy.** It is generally unnecessary to establish iron deficiency; investigate the cause instead.

**Connection.** In [[upper-abdominal-anemia-case|the earlier older-adult anemia case]], a history without visible blood did not exclude occult gastrointestinal loss. The same principle supports endoscopic evaluation here despite a negative stool test.

> **Take away.** A single negative occult-blood test does not exclude gastrointestinal bleeding; evaluate new iron-deficiency anemia in an older adult with upper and lower endoscopy.

### Why this compact review is enough

The bottom line states the decisive laboratory pattern, the question asked and the management choice. Option entries give concise discriminators rather than restating a full pathophysiology lesson. The connection adds one applicable memory cue, while the linked note carries its own answer and outcome. A longer account of every cause of anemia would bury the decision and exceed the compact review’s purpose.

### Common overstatement to avoid

**Too absolute:** “Every older patient with any anemia needs scopes, regardless of findings.” The source supports evaluation for newly identified iron-deficiency anemia in this clinical setting and specifically cautions that one negative occult blood test is insufficient. **Accurate and actionable:** “In an older adult with new iron-deficiency anemia, perform bidirectional endoscopy despite one negative occult blood test.” Preserve the source’s patient group and condition.

## Verification

| Unit | Basis | Verdict | Type | Problem | Correction |
|---:|---|---|---|---|---|
| 1 | Stem and supplied laboratory values | OK |  |  |  |
| 2 | Source: evaluation recommendation despite one negative test | OK |  |  |  |
| 3 | Attempt record: selected answer | OK |  |  |  |
| 4 | Linked question note: anemia without visible bleeding | OK |  |  |  |
