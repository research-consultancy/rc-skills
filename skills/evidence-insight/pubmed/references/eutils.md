# NCBI E-utilities for PubMed

Read this reference only when neither the bundled CLI nor a purpose-built PubMed connector can run.

## Request sequence

Use the official base URL:

`https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`

1. Call `esearch.fcgi` with `db=pubmed`, the URL-encoded `term`, `retmode=json`, and `usehistory=y`.
2. Capture `count`, `querykey`, and `webenv`. Page IDs or records with `retstart` and `retmax` instead of issuing one request per paper.
3. Call `efetch.fcgi` with `db=pubmed`, `query_key`, `WebEnv`, and `retmode=xml` to retrieve complete PubMed records in batches.
4. Use HTTP POST for very long queries and for UID lists larger than roughly 200 identifiers.

PubMed ESearch cannot expose PMIDs beyond the first 10,000 by incrementing `retstart`. Above that ceiling, use EDirect or explicit non-overlapping partitions, validate each partition below 10,000, reconcile counts, detect overlap, and document every query. Date partitions can miss incompletely dated records; never claim completeness without accounting for that limitation.

## Identification and rate limits

Include a descriptive `tool`. Include a contact `email` and `api_key` when configured, keeping the key out of logs, prompts, and committed files. Requests can run without either optional value.

- Without an API key: at most 3 requests per second per IP.
- With a standard API key: at most 10 requests per second per IP.
- Batch large jobs and run them during NCBI's recommended off-peak window when practical.
- Retry transient failures with bounded exponential backoff; preserve the query and pagination state.

## Search behavior

- Use `[mh]` for MeSH terms and `[tiab]` for title/abstract terms.
- Use `[pt]` cautiously because recently supplied citations may not yet be fully MEDLINE-indexed.
- Use `[dp]` for publication dates; record the exact inclusive date range.
- Inspect PubMed Search Details whenever possible to catch unexpected Automatic Term Mapping.
- Preserve the unmodified query string, retrieval date, result count, and all limits in the output.

Primary documentation:

- https://www.ncbi.nlm.nih.gov/books/NBK25497/
- https://www.ncbi.nlm.nih.gov/books/NBK25499/
- https://pubmed.ncbi.nlm.nih.gov/help/
