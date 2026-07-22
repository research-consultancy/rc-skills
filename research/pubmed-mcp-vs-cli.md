# Claude PubMed MCP versus the bundled PubMed CLI

Research date: 2026-07-22

## Decision

Keep the bundled CLI as the primary path for reproducible searches, batch retrieval, and bibliographic verification. Use Claude's PubMed MCP opportunistically for rapid interactive lookup and for its two capabilities the CLI does not currently provide: PMC full text and copyright/licence lookup. Do not make the MCP the silent primary path merely because it is available.

The MCP is a useful convenience layer, not a substitute for the CLI's evidence-grade controls. A safe routing rule is capability-based:

| Need                                                      | Preferred path                                | Reason                                                                                                                                                     |
| --------------------------------------------------------- | --------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Reproducible search or evidence-review retrieval          | Bundled CLI                                   | Complete ordered PMID manifest up to the PubMed ceiling, warnings, durable artifacts, raw-response hashes, retries, and explicit failure on incompleteness |
| Fetch/verify a known PMID set                             | Bundled CLI                                   | Checks every requested identifier, reports deleted/missing/unexpected records, and supports deterministic verification                                     |
| Quick ad hoc search when the MCP is installed and healthy | PubMed MCP                                    | Lower agent/tool friction and structured results                                                                                                           |
| PMC full text                                             | PubMed MCP                                    | `get_full_text_article`; the CLI has no equivalent command                                                                                                 |
| Copyright/licence status                                  | PubMed MCP                                    | `get_copyright_status`; the CLI has no equivalent command                                                                                                  |
| Related articles, citation matching, or ID conversion     | CLI by default; MCP acceptable for ad hoc use | Both expose the capability, but only the CLI supplies versioned envelopes and local provenance                                                             |

## What “built in” means

PubMed is not an unconditional core Claude Code tool. Anthropic offers an official read-only PubMed connector for Claude, Claude Code, and the Claude API, and also publishes it as the credential-free remote MCP plugin `pubmed@life-sciences`. A user can connect it through Claude's connector settings, or add the Life Sciences marketplace, install the plugin, and restart Claude Code. The marketplace says PubMed has no service-specific authentication requirements. Its plugin manifest points to `https://pubmed.mcp.claude.com/mcp` and identifies server version `1.0.0`. [Official PubMed connector page](https://claude.com/connectors/pubmed) · [Anthropic Life Sciences marketplace](https://github.com/anthropics/life-sciences#quick-start) · [PubMed plugin manifest](https://github.com/anthropics/life-sciences/blob/main/pubmed/.claude-plugin/plugin.json)

Claude Code exposes only configured and connected MCP servers. Connectors from claude.ai appear automatically only when Claude Code is authenticated through the corresponding claude.ai subscription; Anthropic documents exclusions including API-key/token, Bedrock, Vertex, and setup-token authentication. Organizations can also allow or block connectors. Anthropic directs users to `/mcp` (or `claude mcp list`) to see server status, tool names, and schemas; deferred MCP tools may be discovered through tool search rather than loaded up front. Therefore the skill should detect actual tool availability, not assume it from the Claude host alone. [Claude Code: use MCP servers from claude.ai](https://code.claude.com/docs/en/mcp#use-mcp-servers-from-claudeai) · [Claude Code MCP integration guidance](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/mcp-integration/references/tool-usage.md) · [Claude Code changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)

## Observed MCP contract

The following was obtained on 2026-07-22 from the public endpoint's MCP `initialize` and `tools/list` methods. It is live endpoint observation, not a versioned public API specification, so callers must discover the current schema at runtime.

| MCP tool                     | Main inputs                                                                                          | Declared output                                                                                                                  |
| ---------------------------- | ---------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `search_articles`            | `query`; optional `max_results` (default 20), `sort`, `date_from`, `date_to`, `retstart`, `datetype` | PMIDs, total/returned counts, original query, query translation, `has_more`                                                      |
| `get_article_metadata`       | PMID array                                                                                           | Articles with identifiers, title, abstract, journal, authors, publication date, keywords, MeSH, publication types, citation data |
| `find_related_articles`      | PMID array; optional link type and maximum                                                           | Link sets and linked IDs                                                                                                         |
| `lookup_article_by_citation` | Citation objects                                                                                     | Matched PMID or null per citation                                                                                                |
| `convert_article_ids`        | IDs and declared type                                                                                | PMID, PMCID, DOI records                                                                                                         |
| `get_full_text_article`      | PMCID array                                                                                          | Metadata plus PMC full text                                                                                                      |
| `get_copyright_status`       | PMID array                                                                                           | Copyright/licence fields, source, availability URLs, summary                                                                     |

The search interface has explicit offset pagination via `retstart` and reports `has_more`. Live parameter probing found a maximum page size of 200, although the published schema does not state that maximum. It exposes PubMed's query translation. It does **not** declare search warnings/errors, a History `WebEnv`/query key, a complete PMID manifest, a 10,000-result safety rule, a stable snapshot, a schema version, retrieval timestamp, raw response, or checksum. Live probes at `retstart=9999` and `retstart=10000` produced successful empty results with `total_count: 0`, rather than a clear ceiling error, so callers cannot safely infer completeness near or beyond the PubMed retrieval ceiling.

The metadata interface does not declare correction/retraction links, deleted-PMID accounting, an input maximum, or a guarantee that every requested PMID appears exactly once. In a live probe with one valid and one nonexistent PMID, it returned only the valid record and `count: 1`; it did not identify the missing PMID. Its normalization was also observably lossy for markup: species names disappeared from parts of one title/abstract. These observations are sufficient to reject it as the sole verifier, but they are not a comprehensive quality benchmark.

The MCP responses include both MCP text content and structured content. Metadata and full-text responses also inject an attribution/DOI-link instruction. That instruction affects agent output but is not a retrieval-integrity mechanism.

## Bundled CLI contract

The repository CLI exposes `search`, `fetch`, `verify`, `related`, `cite-match`, and `id-convert`. Its output has `schema_version`, tool version, command, and UTC retrieval time. Search persists the exact query, translated query, warnings, count, sort, History handle, and ordered PMIDs. Fetch batches complete PubMed XML, checks requested/returned/deleted identifiers, stores raw XML and SHA-256 hashes, writes normalized JSONL, and resumes validated batches. Verify additionally reports duplicates and bibliographic discrepancies. See [`skills/evidence-insight/pubmed/references/cli.md`](../skills/evidence-insight/pubmed/references/cli.md) and the implementation under [`scripts/pubmed_tool`](../skills/evidence-insight/pubmed/scripts/pubmed_tool/).

The CLI fails closed when PubMed reports more than 10,000 matches unless the caller supplies explicit non-overlapping partitions. This matches NCBI's documented fact that PubMed ESearch can retrieve only the first 10,000 matching records; NCBI recommends segmenting the query or using EDirect beyond that point. [NCBI E-utilities reference](https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch)

The CLI also preserves ESearch warnings. This matters because PubMed itself displays warnings for syntax errors, terms not found, and invalid tags, while query translation may add MeSH terms, spellings, and synonyms. The MCP's current search output exposes translation but not warnings. [PubMed Help: Search Details](https://pubmed.ncbi.nlm.nih.gov/help/#search-details)

## Limits, rate policy, and reliability

NCBI documents a limit of three E-utility requests per second without an API key and ten per second with a key. It also recommends identifying software with `tool` and `email`, particularly so NCBI can contact a developer before blocking abusive traffic. The CLI implements client-side 3/10 request-per-second throttling, a fixed tool identity, optional email/key, five attempts, jittered backoff, `Retry-After`, and retry handling for 408, 429, and common 5xx responses. [NCBI usage guidelines](https://www.ncbi.nlm.nih.gov/books/NBK25497/#chapter2.Frequency_Timing_and_Registration)

The MCP marketplace requires no credentials, but neither its manifest nor its tool schemas publish upstream rate limits, throttling, retry behavior, timeout behavior, service-level guarantees, or a way to supply an NCBI API key/email. Because the remote service is an extra dependency between Claude and NCBI, its operational policy and availability cannot be inferred from NCBI's E-utilities documentation. Treat those properties as unverified.

Claude Code additionally warns on MCP output above 10,000 tokens and uses a default maximum of 25,000 tokens unless a tool declares a different limit. This is relevant to full-text articles and large metadata batches and is another reason to keep MCP calls bounded. [Claude Code MCP output limits](https://code.claude.com/docs/en/mcp#mcp-output-limits-and-warnings)

## Recommended skill behavior

1. Discover the PubMed MCP at runtime; never assume it exists merely because the host is Claude Code.
2. Route by task, not availability alone:
   - use the CLI for reproducible search, exhaustive PMID collection, batch metadata retrieval, verification, and saved evidence artifacts;
   - use the MCP for ad hoc lookup, PMC full text, and copyright/licence status;
   - if Python cannot run, use the MCP as the next retrieval fallback, while stating that CLI provenance/completeness checks were unavailable.
3. When MCP search is used, always inspect `query_translation`, page explicitly with `retstart`, and never claim an exhaustive set above 10,000 or when all pages were not collected.
4. When MCP metadata is used for multiple requested PMIDs, reconcile requested IDs against returned `identifiers.pmid`; fetch or verify missing records with the CLI when possible.
5. Preserve the existing raw E-utilities fallback after both paths fail.

This policy keeps the skill predictable: the retrieval standard does not change with ambient connector availability, while agents can still exploit MCP-only capabilities.

## Facts that remain unverified

- The MCP server's source code and deployment configuration are not public in Anthropic's marketplace repository.
- Maximum values and batch limits for every MCP input are not declared.
- Behavior at and beyond PubMed's 10,000-record ESearch ceiling has not been formally documented by Anthropic.
- Whether the server forwards ESearch warnings internally but drops them, or never requests them, is unknown.
- Retry, throttle, cache, timeout, snapshot, logging, retention, and uptime policies are unpublished.
- Full fidelity of metadata/XML normalization, especially inline markup, corrections/retractions, collective authors, dates, and deleted citations, has not been systematically benchmarked.
- Tool schemas may change independently of the marketplace plugin's `1.0.0` manifest; runtime discovery remains necessary.
