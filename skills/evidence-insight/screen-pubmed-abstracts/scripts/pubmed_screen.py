#!/usr/bin/env python3
"""Prepare PubMed plain-text exports and validate balanced abstract screening."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


START_RE = re.compile(r"^(\d+)\.\s+(.*)$")
PMID_RE = re.compile(r"^PMID:\s*(\d+)", re.MULTILINE)
DOI_LINE_RE = re.compile(r"^DOI:\s*(10\.\d{4,9}/\S+)", re.MULTILINE | re.IGNORECASE)
DOI_ANY_RE = re.compile(r"\b(10\.\d{4,9}/[^\s]+)", re.IGNORECASE)
YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")
DECISIONS = {"probable_include", "maybe", "exclude"}
JUDGMENTS = {"yes", "no", "unclear", "not_applicable"}
SCREENING_PHASES = {"pilot", "main"}
CRITERIA = (
    "population",
    "intervention_exposure",
    "comparator",
    "study_design",
    "outcome_measurement",
    "other",
)

RELATION_PREFIXES = (
    "associated data",
    "comment in",
    "comment on",
    "corrected and republished",
    "erratum in",
    "expression of concern in",
    "reprint in",
    "retraction in",
    "update in",
    "update of",
)
TERMINAL_PREFIXES = (
    "©",
    "copyright ",
    "conflict of interest statement:",
    "doi:",
    "pmcid:",
    "pmid:",
    "publication types:",
    "mesh terms:",
    "substances:",
    "grant support:",
)


class ScreeningError(ValueError):
    """A user-correctable input or decision error."""


def split_records(text: str) -> list[list[str]]:
    """Split numbered PubMed records without mistaking wrapped citation lines for starts."""
    records: list[list[str]] = []
    current: list[str] | None = None
    expected = 1

    for line in text.splitlines():
        match = START_RE.match(line)
        if match and int(match.group(1)) == expected:
            if current is not None:
                records.append(current)
            current = [match.group(2)]
            expected += 1
        elif current is not None:
            current.append(line)

    if current is not None:
        records.append(current)
    if not records:
        raise ScreeningError("No sequential numbered PubMed records were found.")
    return records


def paragraphs(lines: Iterable[str]) -> list[str]:
    blocks: list[str] = []
    buffer: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped:
            buffer.append(stripped)
        elif buffer:
            blocks.append(" ".join(buffer))
            buffer = []
    if buffer:
        blocks.append(" ".join(buffer))
    return blocks


def clean_doi(value: str) -> str:
    return value.rstrip(".,;)]}")


def parse_record(record_id: int, lines: list[str]) -> dict[str, Any]:
    blocks = paragraphs(lines)
    citation = blocks[0] if blocks else ""
    title = blocks[1] if len(blocks) > 1 else ""
    joined = "\n".join(lines)

    pmid_match = PMID_RE.search(joined)
    doi_match = DOI_LINE_RE.search(joined) or DOI_ANY_RE.search(citation)
    year_match = YEAR_RE.search(citation)

    author_info_index = next(
        (index for index, block in enumerate(blocks) if block.startswith("Author information:")),
        None,
    )
    authors = ""
    abstract_start = 2
    if author_info_index is not None:
        for candidate in reversed(blocks[2:author_info_index]):
            if not candidate.startswith("["):
                authors = candidate
                break
        abstract_start = author_info_index + 1

    abstract_blocks: list[str] = []
    for block in blocks[abstract_start:]:
        lowered = block.lower()
        if lowered.startswith(TERMINAL_PREFIXES):
            continue
        if lowered.startswith(RELATION_PREFIXES):
            continue
        if block == authors or block == title:
            continue
        abstract_blocks.append(block)

    return {
        "record_id": record_id,
        "citation": citation,
        "year": year_match.group(0) if year_match else "",
        "title": title,
        "authors": authors,
        "abstract": "\n\n".join(abstract_blocks),
        "pmid": pmid_match.group(1) if pmid_match else "",
        "doi": clean_doi(doi_match.group(1)) if doi_match else "",
    }


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ScreeningError(f"{path}:{line_number}: invalid JSON: {exc.msg}") from exc
            if not isinstance(value, dict):
                raise ScreeningError(f"{path}:{line_number}: expected a JSON object.")
            rows.append(value)
    return rows


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def normalize_evidence(value: str) -> str:
    return " ".join(value.split()).casefold()


def validate(records: list[dict[str, Any]], decisions: list[dict[str, Any]]) -> Counter[str]:
    record_ids = {row.get("record_id") for row in records}
    if len(record_ids) != len(records) or None in record_ids:
        raise ScreeningError("Prepared records contain missing or duplicate record_id values.")

    seen: set[Any] = set()
    errors: list[str] = []
    counts: Counter[str] = Counter()
    records_by_id = {row["record_id"]: row for row in records}
    phase_counts: Counter[str] = Counter()
    for index, row in enumerate(decisions, 1):
        record_id = row.get("record_id")
        decision = row.get("decision")
        if record_id not in record_ids:
            errors.append(f"decision line {index}: unknown record_id {record_id!r}")
        if record_id in seen:
            errors.append(f"decision line {index}: duplicate record_id {record_id!r}")
        seen.add(record_id)
        if decision not in DECISIONS:
            errors.append(f"decision line {index}: invalid decision {decision!r}")
        else:
            counts[decision] += 1
        if not str(row.get("reason", "")).strip():
            errors.append(f"decision line {index}: reason is required")
        phase = row.get("screening_phase")
        if phase not in SCREENING_PHASES:
            errors.append(f"decision line {index}: invalid screening_phase {phase!r}")
        else:
            phase_counts[phase] += 1
        supporting_text = str(row.get("supporting_text", "")).strip()
        if not supporting_text:
            errors.append(f"decision line {index}: supporting_text is required")
        elif len(supporting_text) > 500:
            errors.append(
                f"decision line {index}: supporting_text exceeds 500 characters"
            )
        elif record_id in records_by_id:
            source = records_by_id[record_id]
            source_text = f"{source.get('title', '')}\n{source.get('abstract', '')}"
            if normalize_evidence(supporting_text) not in normalize_evidence(source_text):
                errors.append(
                    f"decision line {index}: supporting_text is not a verbatim "
                    "title/abstract excerpt"
                )
        if decision == "maybe" and not str(row.get("concern", "")).strip():
            errors.append(f"decision line {index}: maybe requires a specific concern")
        criteria = row.get("criteria")
        if not isinstance(criteria, dict):
            errors.append(f"decision line {index}: criteria must be an object")
        else:
            judgments: list[str] = []
            for criterion in CRITERIA:
                judgment = criteria.get(criterion)
                if judgment not in JUDGMENTS:
                    errors.append(
                        f"decision line {index}: criteria.{criterion} has invalid "
                        f"judgment {judgment!r}"
                    )
                else:
                    judgments.append(judgment)
            if len(judgments) == len(CRITERIA) and decision in DECISIONS:
                has_no = "no" in judgments
                has_unclear = "unclear" in judgments
                expected = (
                    "exclude"
                    if has_no
                    else "maybe"
                    if has_unclear
                    else "probable_include"
                )
                if decision != expected:
                    errors.append(
                        f"decision line {index}: {decision!r} conflicts with criteria; "
                        f"expected {expected!r}"
                    )

    missing = sorted(record_ids - seen)
    if missing:
        preview = ", ".join(map(str, missing[:20]))
        suffix = " ..." if len(missing) > 20 else ""
        errors.append(f"missing decisions for {len(missing)} record(s): {preview}{suffix}")
    minimum_pilot = min(8, len(records))
    maximum_pilot = min(20, len(records))
    if not minimum_pilot <= phase_counts["pilot"] <= maximum_pilot:
        errors.append(
            f"pilot decisions must number {minimum_pilot}–{maximum_pilot}; "
            f"found {phase_counts['pilot']}"
        )
    if errors:
        raise ScreeningError("\n".join(errors))
    return counts


def command_prepare(args: argparse.Namespace) -> None:
    input_path = Path(args.input)
    output_path = Path(args.output)
    text = input_path.read_text(encoding="utf-8-sig")
    records = [
        parse_record(record_id, lines)
        for record_id, lines in enumerate(split_records(text), 1)
    ]
    write_jsonl(output_path, records)
    print(f"Prepared {len(records)} records -> {output_path}")
    print(f"Source SHA-256: {hashlib.sha256(input_path.read_bytes()).hexdigest()}")
    print(f"Missing PMID: {sum(not row['pmid'] for row in records)}")
    print(f"Missing DOI: {sum(not row['doi'] for row in records)}")
    print(f"Missing abstract: {sum(not row['abstract'] for row in records)}")


def command_batch(args: argparse.Namespace) -> None:
    records = load_jsonl(Path(args.records))
    start_index = args.start - 1
    if start_index < 0:
        raise ScreeningError("--start must be at least 1.")
    if args.size < 1 or args.size > 20:
        raise ScreeningError("--size must be between 1 and 20.")
    selected = records[start_index : start_index + args.size]
    if not selected:
        raise ScreeningError("--start is beyond the final record.")
    for row in selected:
        print(f"## Record {row['record_id']}")
        print(f"PMID: {row['pmid'] or '[missing]'} | DOI: {row['doi'] or '[missing]'}")
        print(f"Citation: {row['citation']}")
        print(f"Title: {row['title']}")
        print("Abstract:")
        print(row["abstract"] or "[No abstract in export]")
        print()


def command_audit(args: argparse.Namespace) -> None:
    records = load_jsonl(Path(args.records))
    decisions = load_jsonl(Path(args.decisions))
    counts = validate(records, decisions)
    retained = counts["probable_include"] + counts["maybe"]
    print(f"Audit passed: {len(records)} records, {retained} retained")
    print(f"pilot: {sum(row.get('screening_phase') == 'pilot' for row in decisions)}")
    print(f"main: {sum(row.get('screening_phase') == 'main' for row in decisions)}")
    for decision in ("probable_include", "maybe", "exclude"):
        print(f"{decision}: {counts[decision]}")


def command_export(args: argparse.Namespace) -> None:
    records = load_jsonl(Path(args.records))
    decisions = load_jsonl(Path(args.decisions))
    counts = validate(records, decisions)
    decisions_by_id = {row["record_id"]: row for row in decisions}
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    candidate_fieldnames = [
        "screening_id",
        "screening_phase",
        "screening_decision",
        "title",
        "authors",
        "journal_citation",
        "year",
        "pmid",
        "doi",
        "pubmed_url",
        "abstract",
        "reason_for_retention",
        "potential_exclusion_concern",
        "population_judgment",
        "intervention_exposure_judgment",
        "comparator_judgment",
        "study_design_judgment",
        "outcome_measurement_judgment",
        "other_criteria_judgment",
        "supporting_text",
        "duplicate_or_related_report",
        "human_review_status",
    ]
    audit_fieldnames = candidate_fieldnames + ["primary_exclusion_reason"]
    audit_path = output_path.with_name(f"{output_path.stem}-audit.csv")

    def output_row(record: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
        criteria = decision["criteria"]
        return {
            "screening_id": record["record_id"],
            "screening_phase": decision["screening_phase"],
            "screening_decision": decision["decision"],
            "title": record["title"],
            "authors": record["authors"],
            "journal_citation": record["citation"],
            "year": record["year"],
            "pmid": record["pmid"],
            "doi": record["doi"],
            "pubmed_url": (
                f"https://pubmed.ncbi.nlm.nih.gov/{record['pmid']}/"
                if record["pmid"]
                else ""
            ),
            "abstract": record["abstract"],
            "reason_for_retention": (
                decision["reason"] if decision["decision"] != "exclude" else ""
            ),
            "potential_exclusion_concern": decision.get("concern", ""),
            "population_judgment": criteria["population"],
            "intervention_exposure_judgment": criteria["intervention_exposure"],
            "comparator_judgment": criteria["comparator"],
            "study_design_judgment": criteria["study_design"],
            "outcome_measurement_judgment": criteria["outcome_measurement"],
            "other_criteria_judgment": criteria["other"],
            "supporting_text": decision.get("supporting_text", ""),
            "duplicate_or_related_report": decision.get("related_report", ""),
            "human_review_status": "pending" if decision["decision"] != "exclude" else "",
        }

    with output_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=candidate_fieldnames)
        writer.writeheader()
        for record in records:
            decision = decisions_by_id[record["record_id"]]
            if decision["decision"] == "exclude":
                continue
            writer.writerow(output_row(record, decision))

    with audit_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=audit_fieldnames)
        writer.writeheader()
        for record in records:
            decision = decisions_by_id[record["record_id"]]
            row = output_row(record, decision)
            row["primary_exclusion_reason"] = (
                decision["reason"] if decision["decision"] == "exclude" else ""
            )
            writer.writerow(row)

    retained = counts["probable_include"] + counts["maybe"]
    print(f"Exported {retained} retained records -> {output_path}")
    print(f"Exported {len(records)} audit records -> {audit_path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Prepare, batch, audit, and export PubMed abstract screening."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare = subparsers.add_parser("prepare", help="Parse a PubMed plain-text export.")
    prepare.add_argument("input")
    prepare.add_argument("--output", required=True)
    prepare.set_defaults(func=command_prepare)

    batch = subparsers.add_parser("batch", help="Print a readable record batch.")
    batch.add_argument("records")
    batch.add_argument("--start", type=int, default=1)
    batch.add_argument("--size", type=int, default=20)
    batch.set_defaults(func=command_batch)

    audit = subparsers.add_parser("audit", help="Validate that all records have decisions.")
    audit.add_argument("records")
    audit.add_argument("decisions")
    audit.set_defaults(func=command_audit)

    export = subparsers.add_parser("export", help="Write include and uncertain records to CSV.")
    export.add_argument("records")
    export.add_argument("decisions")
    export.add_argument("output")
    export.set_defaults(func=command_export)
    return parser


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except (OSError, ScreeningError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
