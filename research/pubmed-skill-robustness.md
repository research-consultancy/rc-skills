# Making the PubMed skill robust

Research date: 2026-07-22

Scope: the current `skills/evidence-insight/pubmed` skill, its E-utilities fallback, and skills that depend on it. Sources are limited to official NCBI, NLM, PubMed, and PMC documentation. Context7 was queried first, as required by the repository, but returned only third-party Go clients rather than official NCBI documentation; those results were not used.

## Executive recommendation

Keep scientific search design, MeSH/synonym judgment, query interpretation, evidence appraisal, and synthesis in the agent instructions. Add a small, dependency-light Python CLI that makes retrieval mechanical, deterministic, inspectable, and testable. Its core should be only `search`, `fetch`, and `verify`; add narrowly scoped identifier and citation utilities only when a downstream workflow needs them.

The most important correction to the existing reference is that PubMed ESearch cannot expose records beyond the first 10,000 matches by incrementing `retstart`. Retrieval over that boundary must be rejected unless the caller supplies an explicit, non-overlapping segmentation plan (normally date partitions) or uses EDirect. NCBI states this PubMed/PMC-specific ceiling directly ([E-utilities in depth, ESearch `retmax`](https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch)).

## What the current skill already gets right

The existing skill correctly requires an exact query, search date, count, limits, verified PMIDs, and complete PubMed records. Its fallback correctly prefers ESearch with `usehistory=y`, batched EFetch XML, POST for long queries/large UID lists, `tool`/`email`, API-key-aware rates, and bounded retries.

These guarantees are important to several dependents:

- `build-pubmed-search` needs query translation, warnings, counts for every iteration, and positive-control recall.
- `grill-meta-analysis-topic` needs reproducible searches for overlapping reviews and related-article exploration.
- `research`, `proofread-manuscript`, and `teach` need reliable PMID and citation verification.

The current gap is execution: prose does not ensure correct URL encoding, global throttling, complete pagination, recovery after partial failure, XML edge-case handling, or a durable provenance artifact.

## Recommended CLI surface

### Core commands

| Command         | Official service                                                                                          | Responsibility                                                                                                                                                                                                                                         | Why core                                                                                                                                                             |
| --------------- | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `pubmed search` | [`esearch.fcgi`](https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch), `db=pubmed`              | Accept an already-formed query; request `usehistory=y`; capture `Count`, `WebEnv`, `QueryKey`, ordered PMIDs when requested, `QueryTranslation`, warnings/errors, explicit sort, and request provenance. Refuse an unsegmented result set over 10,000. | Every dependent begins here; it exposes PubMed's actual interpretation without trying to invent a query.                                                             |
| `pubmed fetch`  | [`efetch.fcgi`](https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EFetch), `db=pubmed`, `retmode=xml` | Fetch complete records from a PMID list or a History-server handle in resumable batches; preserve raw XML and emit normalized JSONL.                                                                                                                   | Full PubMed XML, not a document summary, is needed to verify authors, abstracts, publication types, MeSH, identifiers, and correction/retraction links.              |
| `pubmed verify` | EFetch, optionally ESearch for an input query                                                             | Validate that requested PMIDs are unique and accounted for; check parsed records and produce a compact audit table plus discrepancies.                                                                                                                 | Directly serves citation checking, manuscript proofreading, and positive-control recall. It can be an orchestration command over `fetch`, not a new API abstraction. |

Suggested machine-readable contracts:

- `search` writes `search.json` with query as entered, translated query, warnings/errors, UTC timestamp, count, explicit sort, History handle, ordered PMID manifest, request parameters with the API key redacted, and CLI version.
- `fetch` writes raw batch XML plus `records.jsonl`; a checkpoint lists completed batch offsets/checksums so an interrupted run resumes without repeating successful work.
- `verify` writes `verification.json` and exits nonzero for missing, duplicate, malformed, deleted, or mismatched records.

### Optional commands

| Command             | Official service                                                                                          | Use                                                               | Boundary                                                                                                                                      |
| ------------------- | --------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `pubmed summary`    | [`esummary.fcgi`](https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESummary), preferably version 2.0 | Fast compact display or triage.                                   | Optional and overlapping with `fetch`; never use it as the authoritative complete record.                                                     |
| `pubmed related`    | [`elink.fcgi`](https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ELink)                               | Related PubMed records or PubMed-to-PMC links.                    | Useful to overlap/gap discovery, but keep ranking interpretation in the agent. Preserve link name and scores/order.                           |
| `pubmed cite-match` | [`ecitmatch.cgi`](https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ECitMatch)                        | Resolve structured citation strings to PMIDs in batches.          | Useful for bibliography audits; report ambiguous/no-match results rather than guessing.                                                       |
| `pubmed id-convert` | [PMC ID Converter API](https://pmc.ncbi.nlm.nih.gov/tools/id-converter-api/)                              | Validated conversion among PMID, PMCID, DOI, and manuscript IDs.  | Maximum 200 IDs/request; do not mix identifier types in one request. This is preferable to heuristic DOI parsing when conversion is the task. |
| `pubmed spell`      | [`espell.fcgi`](https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESpell)                             | Return PubMed spelling suggestions.                               | Advisory only. The agent decides whether a suggestion is scientifically appropriate.                                                          |
| `pubmed info`       | [`einfo.fcgi`](https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EInfo), version 2.0                  | Inspect live fields and whether fields are truncatable/rangeable. | Mostly a diagnostics/test command, not part of normal retrieval.                                                                              |

Do not add a Python `build-query`, `expand-mesh`, `screen`, `synthesize`, or `interpret` command. PubMed's search semantics are contextual, and the current agent workflows already own PICO decomposition, MeSH/free-text choices, calibration, eligibility, and conclusions.

## API behavior the implementation must enforce

### Request identity, transport, and throttling

Use the HTTPS base `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`. Send `tool` (no internal spaces) and a valid `email` on every request. NCBI limits aggregate traffic from an IP to three requests/second without an API key and ten requests/second by default with a key; it recommends History-server batching and schedules large jobs for weekends or 21:00–05:00 US Eastern on weekdays ([NCBI E-utilities usage guidelines](https://www.ncbi.nlm.nih.gov/books/NBK25497/)).

Implement one process-wide token bucket shared by every command and worker. Throttle request starts, including retries. Read the key from an environment variable or secret input, never a CLI argument likely to enter shell history; redact it from logs, errors, manifests, and fixtures. Use the HTTP client's parameter/form encoder instead of building URLs by string concatenation. Use POST for queries longer than several hundred characters and for direct UID lists above roughly 200, as NCBI advises ([E-utilities in depth](https://www.ncbi.nlm.nih.gov/books/NBK25499/)).

### Search and query translation

Always set `db=pubmed`, `usehistory=y`, and an explicit `sort`. The ESearch API default can differ from the PubMed website; documented PubMed values include `pub_date`, `Author`, `JournalName`, and `relevance` ([ESearch sort](https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch)). For an initial history-only request, `retmax=0` avoids accidentally treating the default first 20 IDs as complete.

Store both the exact input and ESearch's translated query plus every warning/error. PubMed Automatic Term Mapping can add MeSH, spelling variants, plurals, and synonyms. Field tags bypass ATM; tagging multiple words attempts a phrase; quoted phrases and wildcards also change mapping. PubMed can report syntax errors, invalid tags, terms not found, and ignored phrases, all of which must be surfaced to the agent ([PubMed Help: Search Details and field tags](https://pubmed.ncbi.nlm.nih.gov/help/)). A successful HTTP status with a warning-bearing or error-bearing payload is not an unqualified success.

### History server, pagination, and large sets

The standard sequence is:

1. ESearch with `usehistory=y` to obtain `Count`, `WebEnv`, and `QueryKey`.
2. EFetch or ESummary with both `query_key` and `WebEnv`.
3. Iterate `retstart` and `retmax` while preserving the explicit sort and checking the expected total.

`WebEnv` and `QueryKey` are opaque, temporary server state, not durable provenance. Persist the complete ordered PMID list as soon as practical and checkpoint each successful fetch batch. If the history state expires or becomes invalid, rebuild it from the saved query only after warning that a dynamic rerun can differ; for exact continuation, EPost the saved PMID manifest.

ESearch exposes at most the first 10,000 PubMed/PMC matches. The CLI should fail closed above 10,000 unless the caller supplies partitions that are demonstrably non-overlapping and each below the ceiling, then union and deduplicate by PMID while retaining partition provenance. Publication-date partitions can omit records whose relevant date is incomplete and can shift as PubMed changes, so verify summed partition counts and preserve every partition query. NCBI's alternative is EDirect, which contains special batching logic ([ESearch retrieval limits](https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch)).

### Record retrieval and XML model

Use EFetch PubMed XML for authoritative records. Default to batches of 200, configurable downward; this follows NCBI's advice to POST direct UID lists above about 200 while remaining easy to retry. After every batch, assert that all expected PMIDs appear exactly once or are explicitly represented as deleted/unavailable. ESummary v2 is useful for compact discovery, but NCBI describes it as document summaries, whereas EFetch returns formatted database records ([ESummary and EFetch functions](https://www.ncbi.nlm.nih.gov/books/NBK25499/)).

The parser must tolerate optional and repeated elements, mixed-content/labelled `AbstractText`, collective authors, multiple affiliations and identifiers, partial publication dates, electronic-location IDs, and correction/retraction relations. Preserve the original XML fragment or batch so normalization bugs remain auditable. The official PubMed XML documentation includes PMID `Version`, article identifiers, record status, and deleted citations ([NLM PubMed XML element descriptions](https://www.nlm.nih.gov/bsd/licensee/data_elements_doc.html); [required elements](https://www.nlm.nih.gov/bsd/licensee/elements_required.html)).

### Identifiers

Treat PMID as the canonical PubMed UID: NLM states that PMIDs do not change during processing and are never reused ([PubMed Help: PMID](https://pubmed.ncbi.nlm.nih.gov/help/#pmid-pmid)). Retain PMID `Version` separately because the XML schema exposes it. Extract DOI, PII, PMCID, and other IDs with their declared type; never assume every `ELocationID` is a DOI, normalize away only a leading `doi:`/URL representation, and do not manufacture a DOI.

For cross-system validation use the [PMC ID Converter](https://pmc.ncbi.nlm.nih.gov/tools/id-converter-api/) or ELink's `pubmed_pmc` relationship, and retain no-match/multiple-match status.

## Failures, retries, and resumability

Validate HTTP status, content type, body size, and parsed payload. NCBI rate-limit failures can be JSON error bodies, and ESearch can return warnings/errors inside an otherwise parseable response ([NCBI usage guidelines](https://www.ncbi.nlm.nih.gov/books/NBK25497/); [PubMed query warnings](https://pubmed.ncbi.nlm.nih.gov/help/)).

Recommended engineering policy, clearly labeled as local policy rather than an NCBI guarantee:

- Retry connection failures, timeouts, HTTP 408/429, and 5xx only.
- Honor `Retry-After`; otherwise use capped exponential backoff with full jitter (for example, five attempts with caps near 1, 2, 4, 8, and 16 seconds).
- Do not retry malformed queries or other 4xx responses.
- Pass every retry through the same global rate limiter.
- Treat malformed/truncated XML as a failed batch and retry the whole idempotent request.
- If one batch repeatedly fails, split it recursively to isolate an offending PMID while continuing safe records; exit nonzero and report the isolated failures.
- Write responses to temporary files and atomically rename only after parsing and completeness checks; checkpoints must never mark a partial batch complete.

## Reproducibility contract

PubMed is updated continually: NLM publishes annual baseline XML plus daily files containing new, revised, and deleted citations ([PubMed data downloads](https://pubmed.ncbi.nlm.nih.gov/download/)). Therefore an exact query and date are necessary but insufficient for an exact future rerun.

Every run should persist:

- retrieval timestamp in UTC and CLI/parser version;
- exact query, translated query, warnings/errors, database, explicit sort, limits, and partition queries;
- total count and complete ordered PMID manifest;
- request parameters with secrets redacted, batch boundaries, retry/error log, and raw-response SHA-256 checksums;
- raw XML or a documented cache path plus normalized JSONL;
- per-record PMID, PMID Version, record status, identifiers, and correction/retraction relations.

An exact replay uses the PMID manifest and saved raw XML. Rerunning only the query is a new search and must receive a new timestamp/count/manifest.

## Tests and fixtures

Use immutable local fixtures made from small official ESearch/EPost/ESummary/EFetch/ELink/ID-Converter responses. Store the source endpoint/parameters, retrieval date, expected checksum, and redact credentials. Unit tests must be offline and deterministic; optional network smoke tests should be explicitly enabled, globally rate-limited, and assert schema invariants rather than mutable titles or counts.

Minimum test matrix:

- ATM translation; ignored/not-found phrase; invalid tag; zero results; long-query POST.
- Exactly 10,000 versus 10,001 results; refusal without partitions; partition union, overlap detection, and count reconciliation.
- History pagination order, resume after interruption, expired History handle, duplicate/missing PMID detection.
- API-key and no-key throttle behavior across concurrent workers.
- 429 JSON error, `Retry-After`, 500 then success, timeout, bad content type, empty body, truncated/malformed XML, and persistent single-ID failure.
- Missing abstract/DOI/author; collective author; structured or multilingual abstract; partial dates; multiple affiliations/IDs; PMID Version; deleted citation; correction/retraction links.
- ID converter match, no match, mixed-type rejection, and partial response.
- Golden normalized JSON plus round-trip evidence that every normalized field can be traced to raw XML.

## Proposed implementation order

1. Build the shared HTTP client, configuration, redaction, rate limiter, retry policy, atomic cache, and typed errors.
2. Implement `search` and its provenance schema, including translation/warning capture and a hard 10,000-result guard.
3. Implement History/direct-ID `fetch`, raw XML caching, checkpoints, completeness checks, and a tolerant parser.
4. Implement `verify` as orchestration over stored manifests and fetched records.
5. Add offline fixtures and failure-injection tests before optional commands.
6. Add `related`, `cite-match`, or `id-convert` only when a dependent workflow demonstrates the need; keep `summary`, `spell`, and `info` as diagnostic conveniences.

This sequence turns the PubMed skill into a dependable substrate without moving scientific judgment into a brittle Python rules engine.
