# Contract for skills that call PubMed

Use this contract when a current or future skill delegates biomedical literature work to `$pubmed`. Call the skill, not NCBI endpoints, the bundled script, or a particular MCP server. PubMed owns backend selection and may combine paths.

## What the caller supplies

- the information need and intended use;
- the guarantee tier: **bounded lookup** for a small convenience search, or **evidence-grade** when completeness, reproducibility, citation verification, or durable artifacts matter;
- an exact query when one already exists, otherwise the concepts, constraints, and known terminology needed to construct it;
- known PMIDs, structured citations, or positive-control studies when applicable;
- the required deliverable, including whether another workflow needs machine-readable artifacts.

The caller retains responsibility for the research question, eligibility criteria, screening, appraisal, synthesis, and claim interpretation.

## What PubMed guarantees

PubMed discovers available capabilities, selects MCP, CLI, or raw E-utilities by required guarantee, and returns a common evidence contract. It owns query-translation inspection, identifier validation, batching, response accounting, retries, provenance, and explicit warnings or failures. Evidence-grade work fails closed when completeness cannot be demonstrated.

The result reports:

1. the exact query, search date, count, sort, and limits;
2. verified records and stable identifiers;
3. coverage, indexing, correction, retraction, and full-text caveats;
4. machine-readable artifact paths when artifacts were requested. For potentially large results, callers request summary-only stdout and read only the needed artifact records. If host tools must reopen them, the caller supplies an authorized workspace directory rather than an OS-temporary path.

Do not claim that a PubMed-only search is exhaustive across the biomedical literature.

## Caller patterns

- `build-pubmed-search`: request evidence-grade search diagnostics, query translation, count, complete PMID accounting, and positive-control recall for every tested strategy.
- `grill-meta-analysis-topic`: request evidence-grade discovery plus related-record expansion; use the returned evidence to challenge novelty and feasibility.
- `research`: request evidence-grade discovery and fetch; verify primary-source metadata before synthesis.
- `proofread-manuscript`: verify known citations and identifiers; use accessible full text only when needed to check claim support.
- `teach`: use bounded lookup for examples and orientation; upgrade to evidence-grade whenever the lesson makes reproducibility or coverage claims.

## Prohibited coupling

Caller skills must not parse PubMed XML, call E-utilities directly, assume an MCP server exists, depend on MCP-specific response fields, or reconstruct CLI artifact names. If a new workflow needs a capability absent from this contract, deepen `$pubmed` first and expose it through the capability manifest.
