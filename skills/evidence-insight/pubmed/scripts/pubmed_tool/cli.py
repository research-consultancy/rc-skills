from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
from typing import Any

from .client import NCBIClient
from .commands import (
    capabilities,
    cite_match,
    fetch,
    id_convert,
    related,
    search,
    verify,
)
from .errors import ConfigurationError, PubMedError


class JSONArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise ConfigurationError(message)


def summarize_result(result: dict[str, Any]) -> dict[str, Any]:
    """Return a context-efficient view when the complete payload is persisted."""
    if not result.get("artifacts"):
        raise ConfigurationError(
            "Summary output requires --output-dir so no data is lost"
        )
    summary = dict(result)
    large_fields = {
        "search": ("pmids", "partitions"),
        "fetch": ("records", "requested_pmids"),
        "verify": ("records",),
        "related": ("links",),
    }
    for field in large_fields.get(str(result.get("command")), ()):
        summary.pop(field, None)
    summary["output_mode"] = "summary"
    return summary


def _pmids(args: argparse.Namespace) -> list[str]:
    values = list(args.pmids or [])
    if getattr(args, "pmid_file", None):
        text = Path(args.pmid_file).read_text(encoding="utf-8")
        if args.pmid_file.lower().endswith(".json"):
            payload = json.loads(text)
            values.extend(
                payload.get("pmids", payload) if isinstance(payload, dict) else payload
            )
        else:
            values.extend(text.replace(",", " ").split())
    return [str(value).strip() for value in values if str(value).strip()]


def parser() -> argparse.ArgumentParser:
    root = JSONArgumentParser(
        prog="pubmed", description="Deterministic PubMed tool for AI agents"
    )
    root.add_argument("--email", help="Optional NCBI contact email (or NCBI_EMAIL)")
    root.add_argument("--timeout", type=float, default=30)
    commands = root.add_subparsers(dest="command", required=True)

    commands.add_parser(
        "capabilities", help="Describe commands, limits, and configuration as JSON"
    )

    search_p = commands.add_parser(
        "search", help="Execute an already-formed PubMed query"
    )
    search_p.add_argument("query")
    search_p.add_argument("--sort", default="relevance")
    search_p.add_argument(
        "--partition-file", help="JSON array of explicit non-overlapping queries"
    )
    search_p.add_argument("--output-dir", type=Path)
    search_p.add_argument("--summary-only", action="store_true")

    for name in ("fetch", "verify", "related"):
        command = commands.add_parser(name)
        command.add_argument("--pmids", nargs="*")
        command.add_argument("--pmid-file")
        if name in ("fetch", "verify", "related"):
            command.add_argument("--output-dir", type=Path)
            command.add_argument("--summary-only", action="store_true")
        if name == "fetch":
            command.add_argument("--batch-size", type=int, default=200)
        if name == "verify":
            command.add_argument("--expected-file", type=Path)
        if name == "related":
            command.add_argument("--link-name", default="pubmed_pubmed")

    cite = commands.add_parser("cite-match")
    cite.add_argument(
        "citations_file", type=Path, help="JSON array of structured citations"
    )

    convert = commands.add_parser("id-convert")
    convert.add_argument("ids", nargs="+")
    convert.add_argument(
        "--id-type", required=True, choices=("pmid", "pmcid", "doi", "mid")
    )
    return root


def run(args: argparse.Namespace) -> dict[str, Any]:
    if args.command == "capabilities":
        return capabilities()
    if getattr(args, "summary_only", False) and not getattr(args, "output_dir", None):
        raise ConfigurationError("--summary-only requires --output-dir")
    client = NCBIClient(email=args.email, timeout=args.timeout)
    if args.command == "search":
        partitions = (
            json.loads(Path(args.partition_file).read_text(encoding="utf-8"))
            if args.partition_file
            else None
        )
        result = search(client, args.query, args.sort, args.output_dir, partitions)
        return summarize_result(result) if args.summary_only else result
    if args.command == "fetch":
        result = fetch(client, _pmids(args), args.output_dir, args.batch_size)
        return summarize_result(result) if args.summary_only else result
    if args.command == "verify":
        result = verify(client, _pmids(args), args.output_dir, args.expected_file)
        return summarize_result(result) if args.summary_only else result
    if args.command == "related":
        result = related(client, _pmids(args), args.link_name, args.output_dir)
        return summarize_result(result) if args.summary_only else result
    if args.command == "cite-match":
        return cite_match(client, args.citations_file)
    if args.command == "id-convert":
        return id_convert(client, args.ids, args.id_type)
    raise AssertionError(args.command)


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    try:
        result = run(parser().parse_args(argv))
        json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        if result.get("valid") is False:
            return 2
        return 0
    except (PubMedError, OSError, ValueError, json.JSONDecodeError) as error:
        json.dump(
            {
                "schema_version": "1.0",
                "error": {
                    "code": getattr(error, "code", "input_error"),
                    "message": str(error),
                },
            },
            sys.stderr,
        )
        sys.stderr.write("\n")
        return 1
