# PubMed MCP routing

Read this reference when PubMed MCP tools are visible or discoverable in the current agent environment. The connector is optional: use it when already connected and healthy; continue through the bundled CLI when it is absent. Connector installation and enablement remain outside this skill.

## Discover capabilities

Discover the current MCP tool schema at runtime because server prefixes and schemas vary by host and can change independently of this skill. Claude's PubMed connector currently exposes tools corresponding to:

- `search_articles`;
- `get_article_metadata`;
- `find_related_articles`;
- `lookup_article_by_citation`;
- `convert_article_ids`;
- `get_full_text_article`;
- `get_copyright_status`.

Tool names commonly receive a host-specific MCP prefix. Match the discovered description and input schema as well as the suffix; never assume that the connector exists merely because the host is Claude.

## Route by capability

Use the MCP for:

- a **bounded lookup** returning at most 200 records with no completeness claim;
- PMC full text through `get_full_text_article`;
- copyright and licence status through `get_copyright_status`;
- ad hoc metadata, related-article, citation-match, or identifier-conversion requests where durable provenance is unnecessary;
- retrieval when Python cannot run, while stating that CLI completeness and provenance checks were unavailable.

Use the bundled CLI for **evidence-grade retrieval**:

- reproducible or systematic-search contributions;
- complete PMID collection, positive-control auditing, or pagination beyond 200 records;
- batch record retrieval and bibliographic verification;
- missing, deleted, duplicate, correction, or retraction accounting;
- durable manifests, raw responses, checksums, checkpoints, or exact replay;
- any query approaching or exceeding PubMed's 10,000-record ESearch ceiling.

When either path can perform an ad hoc operation, prefer the CLI when later auditing is plausible. Raw E-utilities remain the final fallback after both the CLI and MCP are unavailable.

## Reconcile MCP output

Inspect `query_translation` for every MCP search. A bounded lookup ends after at most 200 returned records and must be labelled non-exhaustive; `has_more` means the result is incomplete, not permission to claim coverage.

For MCP metadata or full text used in evidence-grade reporting, reconcile every returned PMID and DOI against CLI `fetch` or `verify` when Python is available. Account explicitly for every requested PMID because the connector can omit missing identifiers without reporting them. Cite the PubMed record and DOI as required by the connector response.

For MCP citation lookup, require a numeric `pmid` and exact round-trip of the input tracking `key`. A live connector version has returned those two fields swapped; route any malformed or unaccounted response through CLI `cite-match`.

Treat MCP full text as PMC content, not as proof that the article supports a claim. Appraise the relevant passage and preserve the PMCID alongside the PMID and DOI.

## Known contract limits

The current MCP search schema exposes the original query, query translation, total count, returned count, offset pagination, and `has_more`. It does not declare PubMed warnings, History handles, complete manifests, retrieval timestamps, raw responses, checksums, or a 10,000-result safety rule.

The current metadata schema does not declare correction/retraction links, PMID-version or record-status fields, or exact requested-to-returned accounting. Its retry, throttle, cache, timeout, retention, and service-level policies are unpublished. These absences define the routing boundary; ambient availability alone never upgrades a bounded lookup to evidence-grade retrieval.
