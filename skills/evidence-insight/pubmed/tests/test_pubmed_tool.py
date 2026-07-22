from __future__ import annotations

import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(ROOT))

from pubmed_tool.client import NCBIClient
from pubmed_tool.cli import summarize_result
from pubmed_tool.commands import cite_match, fetch, id_convert, related, search, verify
from pubmed_tool.errors import CompletenessError, ResponseError, SearchLimitError
from pubmed_tool.xml_parser import parse_pubmed_xml


FIXTURES = Path(__file__).parent / "fixtures"


class FakeClient:
    def __init__(self, json_values=None, bodies=None):
        self.json_values = list(json_values or [])
        self.bodies = list(bodies or [])

    def json(self, endpoint, params, **kwargs):
        return self.json_values.pop(0)

    def request(self, endpoint, params, **kwargs):
        return self.bodies.pop(0)


class XMLTests(unittest.TestCase):
    def test_parses_mixed_content_collective_author_ids_and_relations(self):
        records, deleted = parse_pubmed_xml(
            (FIXTURES / "pubmed-records.xml").read_bytes()
        )
        self.assertEqual(deleted, ["99999999"])
        record = records[0]
        self.assertEqual(record["pmid"], "12345678")
        self.assertEqual(record["pmid_version"], "1")
        self.assertEqual(record["title"], "Testing structured PubMed records")
        self.assertEqual(record["authors"], ["Ada Lovelace", "Evidence Group"])
        self.assertIn("RESULTS: A mixed-content result.", record["abstract"])
        self.assertEqual(record["identifiers"]["doi"], ["10.1000/test"])
        self.assertEqual(record["identifiers"]["pubmed"], ["12345678"])
        self.assertNotIn("10.1000/cited", record["identifiers"]["doi"])
        self.assertEqual(record["corrections_retractions"][0]["type"], "RetractionIn")


class SearchTests(unittest.TestCase):
    def test_rejects_a_blank_query_before_requesting_ncbi(self):
        with self.assertRaises(CompletenessError):
            search(FakeClient(), "   ", "relevance", None)

    def test_preserves_translation_and_warning(self):
        payload = json.loads((FIXTURES / "esearch-warning.json").read_text())
        client = FakeClient([payload, payload])
        result = search(client, "reliablest", "relevance", None)
        self.assertEqual(result["translated_query"], "reliable[All Fields]")
        self.assertEqual(result["pmids"], ["12345678"])
        self.assertTrue(result["warnings"])

    def test_rejects_a_sort_that_pubmed_ignored(self):
        payload = {
            "esearchresult": {
                "count": "0",
                "idlist": [],
                "querytranslation": "34713412[UID]",
                "warninglist": {
                    "outputmessages": ["Unknown sort schema 'bad-sort' ignored"]
                },
            }
        }
        with self.assertRaises(ResponseError):
            search(FakeClient([payload]), "34713412[pmid]", "bad-sort", None)

    def test_reports_absolute_search_artifact_path(self):
        payload = {
            "esearchresult": {"count": "0", "idlist": [], "querytranslation": "x"}
        }
        with tempfile.TemporaryDirectory() as directory:
            result = search(FakeClient([payload]), "x", "relevance", Path(directory))
            self.assertEqual(
                result["artifacts"]["search"],
                str((Path(directory) / "search.json").resolve()),
            )

    def test_returns_zero_results_with_term_diagnostics(self):
        payload = {
            "esearchresult": {
                "count": "0",
                "idlist": [],
                "webenv": "w",
                "querykey": "1",
                "querytranslation": "reliablestnonexistentterm[Title/Abstract]",
                "errorlist": {
                    "phrasesnotfound": ["reliablestnonexistentterm"],
                    "fieldsnotfound": [],
                },
            }
        }
        result = search(
            FakeClient([payload]), "reliablestnonexistentterm[tiab]", "relevance", None
        )
        self.assertEqual(result["count"], 0)
        self.assertTrue(result["complete_manifest"])
        self.assertEqual(
            result["errors"]["phrasesnotfound"], ["reliablestnonexistentterm"]
        )

    def test_refuses_unpartitioned_large_result(self):
        payload = {
            "esearchresult": {
                "count": "10001",
                "querytranslation": "all",
                "webenv": "w",
                "querykey": "1",
            }
        }
        with self.assertRaises(SearchLimitError):
            search(FakeClient([payload]), "all", "relevance", None)

    def test_rejects_overlapping_partitions(self):
        large = {"esearchresult": {"count": "10001", "webenv": "w", "querykey": "1"}}
        part_a = {
            "esearchresult": {
                "count": "1",
                "idlist": [],
                "webenv": "a",
                "querykey": "1",
            }
        }
        part_a_ids = {
            "esearchresult": {
                "count": "1",
                "idlist": ["1"],
                "webenv": "a",
                "querykey": "1",
            }
        }
        part_b = {
            "esearchresult": {
                "count": "1",
                "idlist": [],
                "webenv": "b",
                "querykey": "1",
            }
        }
        part_b_ids = {
            "esearchresult": {
                "count": "1",
                "idlist": ["1"],
                "webenv": "b",
                "querykey": "1",
            }
        }
        with self.assertRaises(CompletenessError):
            search(
                FakeClient([large, part_a, part_a_ids, part_b, part_b_ids]),
                "large",
                "relevance",
                None,
                ["a", "b"],
            )

    def test_rejects_partitions_that_do_not_cover_original_count(self):
        large = {"esearchresult": {"count": "10001", "webenv": "w", "querykey": "1"}}
        part_a = {
            "esearchresult": {
                "count": "1",
                "idlist": [],
                "webenv": "a",
                "querykey": "1",
            }
        }
        part_a_ids = {
            "esearchresult": {
                "count": "1",
                "idlist": ["1"],
                "webenv": "a",
                "querykey": "1",
            }
        }
        part_b = {
            "esearchresult": {
                "count": "1",
                "idlist": [],
                "webenv": "b",
                "querykey": "1",
            }
        }
        part_b_ids = {
            "esearchresult": {
                "count": "1",
                "idlist": ["2"],
                "webenv": "b",
                "querykey": "1",
            }
        }
        with self.assertRaises(CompletenessError):
            search(
                FakeClient([large, part_a, part_a_ids, part_b, part_b_ids]),
                "large",
                "relevance",
                None,
                ["a", "b"],
            )


class FetchTests(unittest.TestCase):
    def test_rejects_non_numeric_pmids_before_requesting_ncbi(self):
        with self.assertRaises(CompletenessError):
            fetch(FakeClient(), ["not-a-pmid"], None)

    def test_reports_duplicate_input_pmids_after_deduplication(self):
        client = FakeClient(bodies=[(FIXTURES / "pubmed-records.xml").read_bytes()])
        result = fetch(client, ["12345678", "12345678", "99999999"], None)
        self.assertEqual(result["input_count"], 3)
        self.assertEqual(result["requested_pmids"], ["12345678", "99999999"])
        self.assertEqual(result["duplicate_pmids"], ["12345678"])

    def test_persists_raw_and_normalized_records(self):
        client = FakeClient(bodies=[(FIXTURES / "pubmed-records.xml").read_bytes()])
        with tempfile.TemporaryDirectory() as directory:
            result = fetch(client, ["12345678", "99999999"], Path(directory))
            self.assertEqual(result["record_count"], 1)
            self.assertTrue((Path(directory) / "raw" / "efetch-000000.xml").exists())
            self.assertTrue((Path(directory) / "records.jsonl").exists())
            self.assertEqual(
                result["artifacts"]["records"],
                str((Path(directory) / "records.jsonl").resolve()),
            )
            self.assertEqual(
                result["artifacts"]["raw_directory"],
                str((Path(directory) / "raw").resolve()),
            )

    def test_detects_missing_records(self):
        client = FakeClient(bodies=[(FIXTURES / "pubmed-records.xml").read_bytes()])
        with self.assertRaises(CompletenessError):
            fetch(client, ["12345678", "11111111"], None)

    def test_resumes_from_validated_raw_batch(self):
        with tempfile.TemporaryDirectory() as directory:
            raw = Path(directory) / "raw" / "efetch-000000.xml"
            raw.parent.mkdir()
            raw.write_bytes((FIXTURES / "pubmed-records.xml").read_bytes())
            result = fetch(FakeClient(), ["12345678", "99999999"], Path(directory))
            self.assertTrue(result["batches"][0]["resumed"])

    def test_refetches_a_corrupt_cached_batch(self):
        client = FakeClient(bodies=[(FIXTURES / "pubmed-records.xml").read_bytes()])
        with tempfile.TemporaryDirectory() as directory:
            raw = Path(directory) / "raw" / "efetch-000000.xml"
            raw.parent.mkdir()
            raw.write_bytes(b"<broken>")
            result = fetch(client, ["12345678", "99999999"], Path(directory))
            self.assertFalse(result["batches"][0]["resumed"])
            self.assertIn(b"<PubmedArticleSet>", raw.read_bytes())

    def test_refetches_a_cached_batch_for_different_pmids(self):
        replacement = b"""<PubmedArticleSet><PubmedArticle><MedlineCitation Status=\"MEDLINE\"><PMID Version=\"1\">11111111</PMID><Article><Journal><Title>Replacement Journal</Title></Journal><ArticleTitle>Replacement record</ArticleTitle></Article></MedlineCitation></PubmedArticle></PubmedArticleSet>"""
        client = FakeClient(bodies=[replacement])
        with tempfile.TemporaryDirectory() as directory:
            raw = Path(directory) / "raw" / "efetch-000000.xml"
            raw.parent.mkdir()
            raw.write_bytes((FIXTURES / "pubmed-records.xml").read_bytes())
            result = fetch(client, ["11111111"], Path(directory))
            self.assertFalse(result["batches"][0]["resumed"])
            self.assertEqual(result["records"][0]["pmid"], "11111111")


class RelatedTests(unittest.TestCase):
    def test_rejects_non_numeric_source_pmids(self):
        with self.assertRaises(CompletenessError):
            related(FakeClient(), ["not-a-pmid"])

    def test_labels_pmc_links_as_pmcids(self):
        payload = {
            "linksets": [
                {
                    "ids": ["34713412"],
                    "linksetdbs": [
                        {"dbto": "pmc", "linkname": "pubmed_pmc", "links": ["9046468"]}
                    ],
                }
            ]
        }
        result = related(FakeClient([payload]), ["34713412"], "pubmed_pmc")
        link = result["links"][0]
        self.assertEqual(link["target_database"], "pmc")
        self.assertEqual(link["target_id"], "9046468")
        self.assertEqual(link["pmcid"], "PMC9046468")
        self.assertNotIn("pmid", link)

    def test_persists_related_links_and_reports_artifacts(self):
        payload = {
            "linksets": [
                {
                    "ids": ["34713412"],
                    "linksetdbs": [{"dbto": "pubmed", "links": ["27586375"]}],
                }
            ]
        }
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            result = related(FakeClient([payload]), ["34713412"], output_dir=output)
            self.assertEqual(result["link_count"], 1)
            self.assertEqual(
                result["artifacts"]["links"], str((output / "links.jsonl").resolve())
            )
            self.assertTrue((output / "related.json").exists())
            self.assertTrue((output / "links.jsonl").exists())


class ConvertTests(unittest.TestCase):
    def test_limits_converter_batch(self):
        with self.assertRaises(CompletenessError):
            id_convert(FakeClient(), [str(i) for i in range(201)], "pmid")

    def test_rejects_identifiers_that_do_not_match_declared_type(self):
        with self.assertRaises(CompletenessError):
            id_convert(FakeClient(), ["12345678", "PMC9046468"], "pmid")

    def test_returns_converted_identifiers(self):
        payload = {
            "records": [
                {
                    "requested-id": "PMC9046468",
                    "pmid": 34713412,
                    "pmcid": "PMC9046468",
                    "doi": "10.1007/s12529-021-10032-y",
                }
            ]
        }
        result = id_convert(FakeClient([payload]), ["PMC9046468"], "pmcid")
        self.assertEqual(result["records"][0]["pmid"], 34713412)

    def test_reports_explicit_no_match_records_as_invalid(self):
        payload = {
            "records": [
                {
                    "requested-id": "10.9999/not-real",
                    "doi": "10.9999/not-real",
                    "status": "error",
                    "errmsg": "Identifier not found in PMC",
                }
            ]
        }
        result = id_convert(FakeClient([payload]), ["10.9999/not-real"], "doi")
        self.assertFalse(result["valid"])
        self.assertEqual(result["unresolved_ids"], ["10.9999/not-real"])

    def test_rejects_a_partial_converter_response(self):
        with self.assertRaises(CompletenessError):
            id_convert(FakeClient([{"records": []}]), ["PMC9046468"], "pmcid")


class CitationTests(unittest.TestCase):
    def test_rejects_an_empty_citation_list_before_requesting_ncbi(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "citations.json"
            path.write_text("[]", encoding="utf-8")
            with self.assertRaises(CompletenessError):
                cite_match(FakeClient(), path)

    def test_rejects_citation_fields_that_break_the_wire_format(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "citations.json"
            path.write_text(
                json.dumps([{"journal": "Nature|Science", "year": 2020}]),
                encoding="utf-8",
            )
            with self.assertRaises(CompletenessError):
                cite_match(FakeClient(), path)

    def test_returns_a_positive_citation_match(self):
        body = b"Nature|2020|580|123|Smith|reference-1|32123456\n"
        result = cite_match(FakeClient(bodies=[body]), FIXTURES / "citations.json")
        self.assertTrue(result["matches"][0]["matched"])
        self.assertEqual(result["matches"][0]["key"], "reference-1")
        self.assertEqual(result["matches"][0]["pmid"], "32123456")

    def test_reports_an_accounted_unmatched_citation_as_invalid(self):
        body = b"Nature|2020|580|123|Smith|reference-1|NOT_FOUND\n"
        result = cite_match(FakeClient(bodies=[body]), FIXTURES / "citations.json")
        self.assertFalse(result["valid"])
        self.assertEqual(result["unresolved_keys"], ["reference-1"])

    def test_rejects_a_response_that_does_not_account_for_every_citation(self):
        with self.assertRaises(CompletenessError):
            cite_match(FakeClient(bodies=[b""]), FIXTURES / "citations.json")


class VerifyTests(unittest.TestCase):
    @staticmethod
    def _xml_without_unrelated_delete() -> bytes:
        text = (FIXTURES / "pubmed-records.xml").read_text(encoding="utf-8")
        return re.sub(
            r"\s*<DeleteCitation>.*?</DeleteCitation>", "", text, flags=re.S
        ).encode()

    def test_accepts_matching_expected_metadata(self):
        expected = [
            {
                "pmid": "12345678",
                "title": "Testing structured PubMed records",
                "journal": "Journal of Reliable Evidence",
                "year": "2025",
                "first_author": "Ada Lovelace",
                "doi": "10.1000/test",
            }
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "expected.json"
            path.write_text(json.dumps(expected), encoding="utf-8")
            output = Path(directory) / "audit"
            result = verify(
                FakeClient(bodies=[self._xml_without_unrelated_delete()]),
                ["12345678"],
                output,
                path,
            )
            self.assertEqual(
                result["artifacts"]["verification"],
                str((output / "verification.json").resolve()),
            )
        self.assertTrue(result["valid"])

    def test_accepts_a_citation_style_first_author_surname(self):
        expected = [{"pmid": "12345678", "first_author": "Lovelace"}]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "expected.json"
            path.write_text(json.dumps(expected), encoding="utf-8")
            result = verify(
                FakeClient(bodies=[self._xml_without_unrelated_delete()]),
                ["12345678"],
                None,
                path,
            )
        self.assertTrue(result["valid"])

    def test_reports_a_metadata_mismatch(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "expected.json"
            path.write_text(
                json.dumps([{"pmid": "12345678", "title": "Wrong"}]), encoding="utf-8"
            )
            result = verify(
                FakeClient(bodies=[self._xml_without_unrelated_delete()]),
                ["12345678"],
                None,
                path,
            )
        self.assertFalse(result["valid"])
        self.assertEqual(result["discrepancies"][0]["field"], "title")

    def test_reports_unresolved_pmids_without_aborting_verification(self):
        result = verify(
            FakeClient(bodies=[b"<PubmedArticleSet />"]), ["34554661"], None
        )
        self.assertFalse(result["valid"])
        self.assertEqual(result["unresolved_pmids"], ["34554661"])


class SummaryTests(unittest.TestCase):
    def test_replaces_large_arrays_with_counts_when_artifacts_exist(self):
        result = {
            "command": "related",
            "links": [{"pmid": "1"}, {"pmid": "2"}],
            "link_count": 2,
            "artifacts": {"links": "C:/tmp/links.jsonl"},
        }
        summary = summarize_result(result)
        self.assertNotIn("links", summary)
        self.assertEqual(summary["link_count"], 2)
        self.assertEqual(summary["artifacts"]["links"], "C:/tmp/links.jsonl")


class CLITests(unittest.TestCase):
    def test_capabilities_are_machine_discoverable_without_network_access(self):
        entry = ROOT / "pubmed.py"
        completed = subprocess.run(
            [sys.executable, str(entry), "capabilities"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["schema_version"], "1.0")
        self.assertEqual(payload["command"], "capabilities")
        self.assertEqual(payload["limits"]["max_complete_search_results"], 10_000)
        self.assertEqual(payload["limits"]["max_fetch_batch_size"], 200)
        self.assertIn("search", payload["commands"])
        self.assertIn("NCBI_API_KEY", payload["configuration"]["optional_environment"])

    def test_package_supports_standard_python_module_invocation(self):
        environment = dict(os.environ, PYTHONPATH=str(ROOT))
        completed = subprocess.run(
            [sys.executable, "-m", "pubmed_tool", "capabilities"],
            text=True,
            capture_output=True,
            check=False,
            env=environment,
        )
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(json.loads(completed.stdout)["command"], "capabilities")

    def test_argument_errors_are_json_with_exit_one(self):
        entry = ROOT / "pubmed.py"
        completed = subprocess.run(
            [sys.executable, str(entry), "fetch", "--unknown"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 1)
        payload = json.loads(completed.stderr)
        self.assertEqual(payload["schema_version"], "1.0")
        self.assertEqual(payload["error"]["code"], "configuration_error")

    def test_summary_only_requires_durable_artifacts(self):
        entry = ROOT / "pubmed.py"
        completed = subprocess.run(
            [
                sys.executable,
                str(entry),
                "related",
                "--pmids",
                "34713412",
                "--summary-only",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 1)
        payload = json.loads(completed.stderr)
        self.assertEqual(payload["error"]["code"], "configuration_error")

    def test_negative_batch_size_fails_instead_of_returning_empty_success(self):
        entry = ROOT / "pubmed.py"
        completed = subprocess.run(
            [
                sys.executable,
                str(entry),
                "fetch",
                "--pmids",
                "12345678",
                "--batch-size",
                "-1",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 1)
        payload = json.loads(completed.stderr)
        self.assertEqual(payload["error"]["code"], "completeness_error")

    def test_json_errors_are_utf8_even_under_a_legacy_console_encoding(self):
        entry = ROOT / "pubmed.py"
        environment = dict(os.environ, PYTHONIOENCODING="cp1252")
        completed = subprocess.run(
            [sys.executable, str(entry), "cite-match", "≥-missing.json"],
            capture_output=True,
            check=False,
            env=environment,
        )
        self.assertEqual(completed.returncode, 1)
        payload = json.loads(completed.stderr.decode("utf-8"))
        self.assertIn("≥-missing.json", payload["error"]["message"])

    def test_success_json_is_utf8_even_under_a_legacy_console_encoding(self):
        environment = dict(os.environ, PYTHONIOENCODING="cp1252", PYTHONPATH=str(ROOT))
        code = (
            "import pubmed_tool.cli as cli; "
            "cli.run=lambda args: {'value':'≥'}; "
            "raise SystemExit(cli.main(['fetch']))"
        )
        completed = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            check=False,
            env=environment,
        )
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(json.loads(completed.stdout.decode("utf-8"))["value"], "≥")


if __name__ == "__main__":
    unittest.main()
