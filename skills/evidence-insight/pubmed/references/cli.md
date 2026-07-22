# Bundled PubMed CLI

Read this reference before executing evidence-grade PubMed retrieval. The CLI uses only the Python standard library and emits schema-versioned JSON. When PubMed MCP tools are available, [route by capability](mcp.md) before choosing the execution path.

## Invoke it

From an installed Claude Code plugin:

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/evidence-insight/pubmed/scripts/pubmed.py" --help
```

When `${CLAUDE_PLUGIN_ROOT}` is unavailable, resolve `scripts/pubmed.py` relative to this skill's `SKILL.md`. On systems where `python` is not Python 3, use `python3` or the Windows `py -3` launcher.

The package also supports `python -m pubmed_tool` when `scripts/` is the current directory or is present on `PYTHONPATH`. The `pubmed.py` wrapper remains the most portable plugin entry point.

NCBI access works without configuration at the three-request-per-second limit. Set `NCBI_EMAIL` to identify a contact and `NCBI_API_KEY` to use the standard ten-request-per-second limit. Never put an API key in a command argument, prompt, log, or committed file.

All commands print JSON to stdout and errors as JSON to stderr. Commands exit `2` when they complete with a structured invalid or partial result, such as verification discrepancies, an unmatched citation, or an unresolved identifier. Input, transport, response, and completeness failures exit `1`.

For `search`, `fetch`, `verify`, and `related`, combine `--output-dir DIR --summary-only` to keep stdout small while preserving the complete result in durable artifacts. Summary mode refuses to run without an output directory so records cannot be silently discarded.

Choose an output directory inside the caller's authorized workspace when Claude must reopen artifacts with `Read`, `Grep`, or another host tool. Host permissions may block OS-temporary directories even though the CLI can write them. Use OS temp only for shell-local inspection or disposable tests.

Agents should begin unfamiliar integrations with `python pubmed.py capabilities`. This makes commands, limits, optional environment variables, output schema, and exit codes discoverable without network access. Do not scrape `--help` when the JSON manifest is available.

## Commands

### `capabilities`

```bash
python pubmed.py capabilities
```

This is a zero-network machine-readable description of the installed interface. It requires no email, API key, or other configuration.

### `search`

```bash
python pubmed.py search '("Heart Failure"[mh] OR heart failure[tiab])' \
  --sort relevance --output-dir pubmed-run
```

This records the exact query, translation, warnings, term/field diagnostics, explicit sort, count, History handle, and complete ordered PMID manifest for result sets up to 10,000. Term or field diagnostics accompany a valid zero-result artifact; payload-level query failures remain fatal. If PubMed ignores the requested sort, the command fails instead of falsely recording that sort as applied. A query over the ceiling fails closed. Supply a JSON array of explicit, non-overlapping partition queries with `--partition-file`; the tool rejects oversized, overlapping, or count-mismatched partitions.

### `fetch`

```bash
python pubmed.py fetch --pmids 12345678 23456789 --output-dir pubmed-run/fetch
python pubmed.py fetch --pmid-file pubmed-run/search.json --output-dir pubmed-run/fetch
```

This retrieves complete PubMed XML in batches of 1–200, verifies that every numeric PMID is accounted for, preserves raw XML and SHA-256 checksums, and writes normalized records to `records.jsonl`. Duplicate inputs are deduplicated for transport but reported in `duplicate_pmids` with the original `input_count`. Re-running the same command validates and reuses matching raw batches; malformed or stale batches are refetched atomically.

### `verify`

```bash
python pubmed.py verify --pmids 12345678 --expected-file expected.json --output-dir audit
```

The optional expected file is a JSON array whose objects may contain `pmid`, `title`, `journal`, `year`, `first_author`, and `doi`. Fields use exact case-insensitive comparison, except that `first_author` may be either the normalized full display name or the citation-style surname alone. The command reports discrepancies, duplicate inputs, deleted records, and corrections/retractions. It verifies bibliographic consistency, not scientific claim support.

An unresolved PMID is returned in `unresolved_pmids` with `valid: false` and exit code `2`; verification does not abort. Strict `fetch` still exits `1` when any requested PMID is unaccounted for.

### `related`

```bash
python pubmed.py related --pmids 12345678 --output-dir related-run --summary-only
```

This returns `pubmed_pubmed` neighbors by default while preserving ordering and scores when NCBI supplies them. Every link contains `target_id` and `target_database`; PubMed targets add `pmid`, while PMC targets add normalized `pmcid`. With an output directory, complete links are written to `links.jsonl` and the run summary to `related.json`. Use `--link-name` for another explicit ELink relationship. The agent interprets relevance.

### `cite-match`

```bash
python pubmed.py cite-match citations.json
```

The input is a non-empty JSON array with `journal`, `year`, `volume`, `first_page`, `author`, and an optional `key`. Reserved wire-format delimiters are rejected before the request. Every input key must be accounted for exactly once. Ambiguous and unmatched citations return `valid: false`, list `unresolved_keys`, and exit `2`; the agent must not guess.

### `id-convert`

```bash
python pubmed.py id-convert --id-type doi 10.1000/example
```

This converts at most 200 identifiers through the PMC ID Converter. `--id-type` is required; every identifier must match that type and receive exactly one response record. Explicit no-match records return `valid: false`, list `unresolved_ids`, and exit `2`. Preserve no-match warnings and error messages.

## Durable artifacts

Commands accepting `--output-dir` write atomically and return absolute paths in an `artifacts` object. A search directory contains `search.json`; a fetch directory contains raw XML batches, `checkpoint.json`, `records.jsonl`, and `fetch.json`; verification adds `verification.json`; related-record retrieval contains `related.json` and `links.jsonl`. Callers consume the reported paths rather than reconstructing filenames. Exact replay uses the saved PMID manifest and raw XML. Re-running the query is a new search because PubMed changes continuously.
