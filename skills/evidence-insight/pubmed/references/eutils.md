# NCBI E-utilities for PubMed

Read this reference when no purpose-built PubMed connector is available.

## Request sequence

Use the official base URL:

`https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`

1. Call `esearch.fcgi` with `db=pubmed`, the URL-encoded `term`, `retmode=json`, and `usehistory=y`.
2. Capture `count`, `querykey`, and `webenv`. Page IDs or records with `retstart` and `retmax` instead of issuing one request per paper.
3. Call `efetch.fcgi` with `db=pubmed`, `query_key`, `WebEnv`, and `retmode=xml` to retrieve complete PubMed records in batches.
4. Use HTTP POST for very long queries and for UID lists larger than roughly 200 identifiers.

For PubMed retrieval above 10,000 records, use NCBI's EDirect workflow or split the query into non-overlapping date ranges and document the method.

## Identification and rate limits

Include a descriptive `tool` and contact `email` with automated requests. Include `api_key` when available and keep it out of logs, prompts, and committed files.

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
