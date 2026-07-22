from __future__ import annotations

from datetime import datetime, timezone
from collections import Counter
import json
from pathlib import Path
import re
from typing import Any, Iterable

from . import SCHEMA_VERSION, __version__
from .client import NCBIClient, PMC_ID_URL
from .errors import CompletenessError, ResponseError, SearchLimitError
from .storage import atomic_write, sha256, write_json, write_jsonl
from .xml_parser import parse_pubmed_xml


def envelope(command: str) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "tool_version": __version__,
        "command": command,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
    }


def capabilities() -> dict[str, Any]:
    """Describe the stable agent-facing interface without making a network request."""
    return {
        **envelope("capabilities"),
        "commands": {
            "capabilities": {
                "purpose": "Describe this interface without network access"
            },
            "search": {
                "purpose": "Reproducible PubMed discovery with complete PMID accounting",
                "supports_artifacts": True,
                "supports_summary_output": True,
            },
            "fetch": {
                "purpose": "Batch retrieval of normalized PubMed records",
                "supports_artifacts": True,
                "supports_summary_output": True,
            },
            "verify": {
                "purpose": "Validate known PMIDs and optional expected metadata",
                "supports_artifacts": True,
                "supports_summary_output": True,
            },
            "related": {
                "purpose": "Retrieve NCBI-computed related-record links",
                "supports_artifacts": True,
                "supports_summary_output": True,
            },
            "cite-match": {"purpose": "Resolve structured citations to PMIDs"},
            "id-convert": {
                "purpose": "Convert PMID, PMCID, DOI, and NIHMS identifiers"
            },
        },
        "limits": {
            "max_complete_search_results": 10_000,
            "max_fetch_batch_size": 200,
            "max_id_conversion_batch": 200,
        },
        "configuration": {
            "required_environment": [],
            "optional_environment": ["NCBI_EMAIL", "NCBI_API_KEY"],
            "credentials_required": False,
        },
        "exit_codes": {"success": 0, "error": 1, "invalid_or_partial_result": 2},
        "output": {
            "format": "json",
            "schema_version": SCHEMA_VERSION,
            "artifact_paths_are_absolute": True,
        },
    }


def _esearch(client: NCBIClient, query: str, sort: str) -> dict[str, Any]:
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "usehistory": "y",
        "retmax": 0,
        "sort": sort,
    }
    payload = client.json(
        "esearch.fcgi", params, method="POST" if len(query) > 400 else "GET"
    )
    result = payload.get("esearchresult")
    if not isinstance(result, dict):
        raise ResponseError("ESearch response has no esearchresult")
    count = int(result.get("count", 0))
    warnings = result.get("warninglist", {})
    errors = result.get("errorlist", {})
    output_messages = (
        warnings.get("outputmessages", []) if isinstance(warnings, dict) else []
    )
    ignored_sort = [
        message
        for message in output_messages
        if "sort" in str(message).casefold() and "ignored" in str(message).casefold()
    ]
    if ignored_sort:
        raise ResponseError(
            f"PubMed did not apply the requested sort: {ignored_sort[0]}"
        )
    fatal_error = result.get("ERROR") or result.get("error")
    if fatal_error:
        raise ResponseError(f"PubMed rejected the query: {fatal_error}")
    ids: list[str] = []
    if count <= 10_000 and count:
        page_params = {**params, "retmax": count}
        page = client.json(
            "esearch.fcgi", page_params, method="POST" if len(query) > 400 else "GET"
        )
        page_result = page.get("esearchresult", {})
        ids = [str(value) for value in page_result.get("idlist", [])]
        if len(ids) != count:
            raise CompletenessError(
                f"ESearch reported {count} records but returned {len(ids)} PMIDs"
            )
        result = {
            **result,
            "webenv": page_result.get("webenv", result.get("webenv")),
            "querykey": page_result.get("querykey", result.get("querykey")),
        }
    return {
        "query": query,
        "translated_query": result.get("querytranslation"),
        "warnings": warnings,
        "errors": errors,
        "count": count,
        "sort": sort,
        "pmids": ids,
        "history": {
            "webenv": result.get("webenv"),
            "query_key": result.get("querykey"),
        },
        "complete_manifest": count <= 10_000,
    }


def search(
    client: NCBIClient,
    query: str,
    sort: str,
    output_dir: Path | None,
    partitions: list[str] | None = None,
) -> dict[str, Any]:
    if not query.strip():
        raise CompletenessError("PubMed query cannot be blank")
    result = {**envelope("search"), **_esearch(client, query, sort)}
    if result["count"] > 10_000:
        if not partitions:
            raise SearchLimitError(
                f"PubMed found {result['count']} records; a complete PMID manifest requires explicit partitions"
            )
        partition_results = [_esearch(client, value, sort) for value in partitions]
        oversized = [
            value["query"] for value in partition_results if value["count"] > 10_000
        ]
        if oversized:
            raise SearchLimitError(
                f"Partitions still exceed 10,000 records: {oversized}"
            )
        flat = [pmid for value in partition_results for pmid in value["pmids"]]
        duplicates = sorted(pmid for pmid, count in Counter(flat).items() if count > 1)
        if duplicates:
            raise CompletenessError(f"Partitions overlap on {len(duplicates)} PMIDs")
        if len(flat) != sum(value["count"] for value in partition_results):
            raise CompletenessError("Partition counts do not reconcile")
        if len(flat) != result["count"]:
            raise CompletenessError(
                f"Partitions cover {len(flat)} unique PMIDs but the original query reported {result['count']}"
            )
        result.update(
            {"partitions": partition_results, "pmids": flat, "complete_manifest": True}
        )
    if output_dir:
        result["artifacts"] = {"search": str((output_dir / "search.json").resolve())}
        write_json(output_dir / "search.json", result)
    return result


def _batches(values: list[str], size: int) -> Iterable[tuple[int, list[str]]]:
    for offset in range(0, len(values), size):
        yield offset, values[offset : offset + size]


def fetch(
    client: NCBIClient,
    pmids: list[str],
    output_dir: Path | None,
    batch_size: int = 200,
    allow_missing: bool = False,
) -> dict[str, Any]:
    if not 1 <= batch_size <= 200:
        raise CompletenessError("Fetch batch size must be between 1 and 200")
    supplied = [str(value).strip() for value in pmids if str(value).strip()]
    requested = list(dict.fromkeys(supplied))
    duplicate_pmids = sorted(
        value for value, count in Counter(supplied).items() if count > 1
    )
    if not requested:
        raise CompletenessError("At least one PMID is required")
    invalid_pmids = [value for value in requested if not value.isdigit()]
    if invalid_pmids:
        raise CompletenessError(f"PMIDs must contain digits only: {invalid_pmids}")
    records: list[dict[str, Any]] = []
    deleted: list[str] = []
    unresolved: list[str] = []
    batches = []
    for offset, batch in _batches(requested, batch_size):
        raw_path = (
            output_dir / "raw" / f"efetch-{offset:06d}.xml" if output_dir else None
        )
        resumed = bool(raw_path and raw_path.exists())
        request_params = {"db": "pubmed", "id": ",".join(batch), "retmode": "xml"}
        body = (
            raw_path.read_bytes()
            if resumed
            else client.request("efetch.fcgi", request_params, method="POST")
        )
        try:
            parsed, removed = parse_pubmed_xml(body)
        except ResponseError:
            if not resumed:
                raise
            resumed = False
            body = client.request("efetch.fcgi", request_params, method="POST")
            parsed, removed = parse_pubmed_xml(body)
        returned = [value["pmid"] for value in parsed] + removed
        missing = sorted(set(batch) - set(returned))
        unexpected = sorted(set(returned) - set(batch))
        if resumed and (missing or unexpected or len(returned) != len(set(returned))):
            resumed = False
            body = client.request("efetch.fcgi", request_params, method="POST")
            parsed, removed = parse_pubmed_xml(body)
            returned = [value["pmid"] for value in parsed] + removed
            missing = sorted(set(batch) - set(returned))
            unexpected = sorted(set(returned) - set(batch))
        duplicates = len(returned) != len(set(returned))
        if unexpected or duplicates or (missing and not allow_missing):
            raise CompletenessError(
                f"Batch {offset} failed accounting (missing={missing}, unexpected={unexpected})"
            )
        unresolved.extend(missing)
        records.extend(parsed)
        deleted.extend(removed)
        batch_meta = {
            "offset": offset,
            "requested": batch,
            "sha256": sha256(body),
            "resumed": resumed,
        }
        batches.append(batch_meta)
        if output_dir:
            if not resumed:
                atomic_write(raw_path, body)
            write_json(output_dir / "checkpoint.json", {"completed_batches": batches})
    result = {
        **envelope("fetch"),
        "input_count": len(supplied),
        "requested_pmids": requested,
        "duplicate_pmids": duplicate_pmids,
        "records": records,
        "deleted_pmids": deleted,
        "unresolved_pmids": unresolved,
        "record_count": len(records),
        "batches": batches,
    }
    if output_dir:
        result["artifacts"] = {
            "summary": str((output_dir / "fetch.json").resolve()),
            "records": str((output_dir / "records.jsonl").resolve()),
            "checkpoint": str((output_dir / "checkpoint.json").resolve()),
            "raw_directory": str((output_dir / "raw").resolve()),
        }
        write_jsonl(output_dir / "records.jsonl", records)
        write_json(
            output_dir / "fetch.json",
            {**result, "records": None, "records_file": "records.jsonl"},
        )
    return result


def verify(
    client: NCBIClient,
    pmids: list[str],
    output_dir: Path | None,
    expected_file: Path | None = None,
) -> dict[str, Any]:
    duplicates = sorted({value for value in pmids if pmids.count(value) > 1})
    fetched = fetch(
        client, pmids, output_dir / "fetch" if output_dir else None, allow_missing=True
    )
    actual = {value["pmid"]: value for value in fetched["records"]}
    expected = (
        json.loads(expected_file.read_text(encoding="utf-8")) if expected_file else []
    )
    discrepancies: list[dict[str, Any]] = []
    fields = ("title", "journal", "doi", "year", "first_author")
    for item in expected:
        record = actual.get(str(item.get("pmid")))
        if record is None:
            discrepancies.append(
                {"pmid": item.get("pmid"), "field": "pmid", "issue": "missing"}
            )
            continue
        actual_view = {
            "title": record.get("title"),
            "journal": record.get("journal"),
            "doi": (record.get("identifiers", {}).get("doi") or [None])[0],
            "year": record.get("publication_date", {}).get("year"),
            "first_author": (record.get("authors") or [None])[0],
        }
        for field in fields:
            if item.get(field) is None:
                continue
            expected_value = str(item[field]).casefold()
            actual_value = str(actual_view[field]).casefold()
            matches = expected_value == actual_value
            if field == "first_author" and " " not in expected_value:
                matches = matches or expected_value == actual_value.rsplit(" ", 1)[-1]
            if not matches:
                discrepancies.append(
                    {
                        "pmid": item.get("pmid"),
                        "field": field,
                        "expected": item[field],
                        "actual": actual_view[field],
                    }
                )
    result = {
        **envelope("verify"),
        "requested_count": len(pmids),
        "unique_count": len(set(pmids)),
        "duplicate_pmids": duplicates,
        "deleted_pmids": fetched["deleted_pmids"],
        "unresolved_pmids": fetched["unresolved_pmids"],
        "discrepancies": discrepancies,
        "valid": not duplicates
        and not fetched["deleted_pmids"]
        and not fetched["unresolved_pmids"]
        and not discrepancies,
        "records": fetched["records"],
    }
    if output_dir:
        result["artifacts"] = {
            "verification": str((output_dir / "verification.json").resolve()),
            "fetch": fetched.get("artifacts", {}),
        }
        write_json(output_dir / "verification.json", {**result, "records": None})
    return result


def related(
    client: NCBIClient,
    pmids: list[str],
    link_name: str = "pubmed_pubmed",
    output_dir: Path | None = None,
) -> dict[str, Any]:
    if not pmids:
        raise CompletenessError("At least one PMID is required")
    invalid_pmids = [value for value in pmids if not value.isdigit()]
    if invalid_pmids:
        raise CompletenessError(f"PMIDs must contain digits only: {invalid_pmids}")
    payload = client.json(
        "elink.fcgi",
        {
            "dbfrom": "pubmed",
            "db": "pubmed",
            "id": pmids,
            "cmd": "neighbor_score",
            "linkname": link_name,
            "retmode": "json",
        },
        method="POST",
    )
    links = []
    for linkset in payload.get("linksets", []):
        source_ids = linkset.get("ids", [])
        for database in linkset.get("linksetdbs", []):
            for link in database.get("links", []):
                target_database = database.get("dbto")
                if isinstance(link, dict):
                    target_id = str(link.get("id"))
                    item = {
                        "source_pmids": source_ids,
                        "target_id": target_id,
                        "target_database": target_database,
                        "score": link.get("score"),
                        "link_name": database.get("linkname"),
                    }
                else:
                    target_id = str(link)
                    item = {
                        "source_pmids": source_ids,
                        "target_id": target_id,
                        "target_database": target_database,
                        "score": None,
                        "link_name": database.get("linkname"),
                    }
                if target_database == "pubmed":
                    item["pmid"] = target_id
                elif target_database == "pmc":
                    item["pmcid"] = (
                        target_id
                        if target_id.upper().startswith("PMC")
                        else f"PMC{target_id}"
                    )
                links.append(item)
    result = {
        **envelope("related"),
        "source_pmids": pmids,
        "requested_link_name": link_name,
        "link_count": len(links),
        "links": links,
    }
    if output_dir:
        result["artifacts"] = {
            "summary": str((output_dir / "related.json").resolve()),
            "links": str((output_dir / "links.jsonl").resolve()),
        }
        write_jsonl(output_dir / "links.jsonl", links)
        write_json(
            output_dir / "related.json",
            {**result, "links": None, "links_file": "links.jsonl"},
        )
    return result


def cite_match(client: NCBIClient, citations_file: Path) -> dict[str, Any]:
    citations = json.loads(citations_file.read_text(encoding="utf-8"))
    if not isinstance(citations, list) or not citations:
        raise CompletenessError("Citation input must be a non-empty JSON array")
    lines = []
    expected_keys = []
    for index, item in enumerate(citations):
        if not isinstance(item, dict):
            raise CompletenessError(f"Citation {index} must be a JSON object")
        key = str(item.get("key", index))
        wire_values = [
            str(item.get(field, ""))
            for field in ("journal", "year", "volume", "first_page", "author")
        ] + [key]
        if any(
            any(delimiter in value for delimiter in ("|", "\r", "\n"))
            for value in wire_values
        ):
            raise CompletenessError(f"Citation {index} contains a reserved delimiter")
        expected_keys.append(key)
        lines.append("|".join(wire_values) + "|")
    body = client.request(
        "ecitmatch.cgi",
        {"db": "pubmed", "retmode": "ref", "bdata": "\r".join(lines)},
        method="POST",
    )
    matches = []
    for line in body.decode("utf-8", errors="replace").splitlines():
        parts = line.split("|")
        matches.append(
            {
                "raw": line,
                "key": parts[-2] if len(parts) > 2 else None,
                "pmid": parts[-1] if parts and parts[-1].isdigit() else None,
                "matched": bool(parts and parts[-1].isdigit()),
            }
        )
    returned_keys = [value["key"] for value in matches]
    missing = sorted(set(expected_keys) - set(returned_keys))
    unexpected = sorted(set(returned_keys) - set(expected_keys))
    duplicates = sorted(
        key for key, count in Counter(returned_keys).items() if count > 1
    )
    if missing or unexpected or duplicates:
        raise CompletenessError(
            f"Citation response failed accounting (missing={missing}, unexpected={unexpected}, duplicates={duplicates})"
        )
    unresolved_keys = [str(value["key"]) for value in matches if not value["matched"]]
    return {
        **envelope("cite-match"),
        "matches": matches,
        "unresolved_keys": unresolved_keys,
        "valid": not unresolved_keys,
    }


def id_convert(
    client: NCBIClient, ids: list[str], id_type: str | None
) -> dict[str, Any]:
    if not 1 <= len(ids) <= 200:
        raise CompletenessError("ID conversion accepts between 1 and 200 identifiers")
    patterns = {
        "pmid": r"\d+",
        "pmcid": r"PMC\d+",
        "doi": r"10\.\d{4,9}/\S+",
        "mid": r"NIHMS\d+",
    }
    if id_type not in patterns:
        raise CompletenessError("ID conversion requires one declared identifier type")
    invalid = [
        value
        for value in ids
        if not re.fullmatch(patterns[id_type], value, re.IGNORECASE)
    ]
    if invalid:
        raise CompletenessError(
            f"Identifiers do not match declared type {id_type}: {invalid}"
        )
    params = {
        "ids": ",".join(ids),
        "format": "json",
        "versions": "yes",
        "idtype": id_type,
    }
    payload = client.json("", params, base_url=PMC_ID_URL)
    records = payload.get("records", [])
    requested = [value.casefold() for value in ids]
    returned = [str(value.get("requested-id", "")).casefold() for value in records]
    missing = sorted(set(requested) - set(returned))
    unexpected = sorted(set(returned) - set(requested))
    duplicates = sorted(
        value for value, count in Counter(returned).items() if count > 1
    )
    if missing or unexpected or duplicates:
        raise CompletenessError(
            f"ID conversion failed accounting (missing={missing}, unexpected={unexpected}, duplicates={duplicates})"
        )
    unresolved_ids = [
        str(record.get("requested-id"))
        for record in records
        if str(record.get("status", "")).casefold() == "error"
    ]
    return {
        **envelope("id-convert"),
        "requested_ids": ids,
        "records": records,
        "unresolved_ids": unresolved_ids,
        "valid": not unresolved_ids,
        "warnings": payload.get("warnings", []),
    }
