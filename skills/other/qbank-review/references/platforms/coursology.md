# Coursology

Base URL: https://coursology-qbank.com
Login URL: https://coursology-qbank.com/login
Observed review paths: `/qbanks/usmle2/tests/<testId>`; results `/qbanks/usmle2/dashboard/performance/test/<testId>/results`; analysis `/qbanks/usmle2/dashboard/performance/test/<testId>/analysis`.

screenshots: prohibited

Use only completed tests in review mode. Pensieve observed paths: /qbanks/usmle2/tests/<testId>; results and analysis paths: /qbanks/usmle2/dashboard/performance/test/<testId>/results and /analysis. Verify current UI on first run; selectors can change.

Capture hints from Pensieve source:
- Body identity: “Item N of M Question Id: <id>”; numbered buttons navigate.
- Stem: #question-text. Explanation: #question-explanation.
- Choices: .group/choice; selected state is a direct child div in choice button; correctness uses svg[data-icon="check"]; cross-out uses .line-through; peer percent may appear in choice text wrapper p.
- Guess mark: [data-icon="flag"] in numbered sidebar button; sidebar outcome uses check/xmark icons.
- Colored mark elements in stem/explanation represent annotations; distinguish learner highlights from crowd “Suggested Highlights”.
- Review body may show “REVIEW … Time Elapsed”. Capture per-question timing/peer percentage only if explicitly shown.
- Medical-library metadata may load after stem/explanation. Inspect objective and taxonomy there.
- Images may be in explanation HTML or modal. Download source files only when allowed; never screenshot.

Treat these as discovery hints. Reverify current page and note unavailable fields. Do not change answers or annotations.
