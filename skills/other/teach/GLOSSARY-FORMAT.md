# GLOSSARY.md Format

`GLOSSARY.md` is the canonical language for this teaching workspace. All explainers, exercises, and learning records should adhere to its terminology. Building it is itself part of learning: compressing a concept into a tight definition is evidence the user understands it.

## Structure

```md
# {Topic} Glossary

{One or two sentence description of the topic this glossary covers.}

## Terms

**Effect estimate**:
A numerical summary of the magnitude and direction of an association or intervention effect in a study or synthesis.
_Avoid_: Result, effect size when the estimand is unclear

**Risk ratio**:
The risk of an outcome in one group divided by the risk in another group over a defined period.
_Avoid_: Relative risk reduction

**Heterogeneity**:
Variation among study results beyond the fact that each study is a separate estimate; its clinical, methodological, and statistical forms require distinct interpretation.
_Avoid_: Inconsistency when the intended meaning is broader
```

## Rules

- **Add a term only when the user understands it.** The glossary is a record of compressed knowledge, not a dictionary the user reads to learn. If the user has just been introduced to a concept, wait until they can use it correctly before promoting it here.
- **Be opinionated.** When several words exist for the same concept, pick the best one and list the rest as aliases to avoid. This is how language compresses.
- **Keep definitions tight.** One or two sentences. Define what the term IS, not what it does or how to do it.
- **Use the glossary's own terms inside definitions.** Once a term is in the glossary, prefer it everywhere — including inside other definitions. This is what makes complex terms easier to grasp later.
- **Group under subheadings** when natural clusters emerge (e.g. `## Study Design`, `## Effect Measures`, `## Bias`). A flat list is fine when terms cohere.
- **Flag ambiguities explicitly.** If a term is used loosely in the literature, resolve it for the workspace: "Here, outcome means the measured endpoint; estimand means the treatment-effect quantity being targeted."
- **Revise as understanding deepens.** A definition the user wrote in week one may be wrong by week six. Update in place; do not leave stale entries.
