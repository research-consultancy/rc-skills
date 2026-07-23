import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("pubmed_screen.py")
SPEC = importlib.util.spec_from_file_location("pubmed_screen", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


SAMPLE = (Path(__file__).parent / "fixtures" / "sample-export.txt").read_text(
    encoding="utf-8"
)


class PubmedScreenTests(unittest.TestCase):
    def test_sequential_split_ignores_wrapped_number(self):
        text = SAMPLE.replace("METHODS:", "9.\nMETHODS:")
        records = MODULE.split_records(text)
        self.assertEqual(len(records), 6)

    def test_parse_fields_and_missing_abstract(self):
        raw = MODULE.split_records(SAMPLE)
        first = MODULE.parse_record(1, raw[0])
        second = MODULE.parse_record(2, raw[1])
        self.assertEqual(first["pmid"], "10000001")
        self.assertEqual(first["doi"], "10.1000/eligible")
        self.assertIn("Empagliflozin versus placebo", first["title"])
        self.assertIn("randomized", first["abstract"])
        self.assertEqual(second["abstract"], "")

    def test_validate_requires_complete_unique_decisions(self):
        records = [
            {
                "record_id": 1,
                "title": "Randomized eligible trial.",
                "abstract": "Adults were randomized.",
            },
            {
                "record_id": 2,
                "title": "Pilot trial in chronic heart failure.",
                "abstract": "",
            },
        ]
        decisions = [
            {
                "record_id": 1,
                "screening_phase": "pilot",
                "decision": "probable_include",
                "reason": "Likely eligible.",
                "supporting_text": "Randomized eligible trial.",
                "criteria": {key: "yes" for key in MODULE.CRITERIA},
            },
            {
                "record_id": 2,
                "screening_phase": "pilot",
                "decision": "maybe",
                "reason": "Sparse report.",
                "concern": "Comparator not reported.",
                "supporting_text": "Pilot trial in chronic heart failure.",
                "criteria": {key: "unclear" for key in MODULE.CRITERIA},
            },
        ]
        counts = MODULE.validate(records, decisions)
        self.assertEqual(counts["probable_include"], 1)
        with self.assertRaises(MODULE.ScreeningError):
            MODULE.validate(records, decisions[:1])

    def test_validate_enforces_decision_contract(self):
        records = [
            {
                "record_id": 1,
                "title": "Mixed population.",
                "abstract": "HFrEF and HFmrEF were enrolled.",
            }
        ]
        inconsistent = [
            {
                "record_id": 1,
                "screening_phase": "pilot",
                "decision": "probable_include",
                "reason": "Mixed population.",
                "supporting_text": "HFrEF and HFmrEF were enrolled.",
                "criteria": {
                    **{key: "yes" for key in MODULE.CRITERIA},
                    "population": "unclear",
                },
            }
        ]
        with self.assertRaisesRegex(MODULE.ScreeningError, "conflicts with criteria"):
            MODULE.validate(records, inconsistent)

    def test_validate_requires_verbatim_supporting_text(self):
        records = [
            {
                "record_id": 1,
                "title": "Eligible trial.",
                "abstract": "Adults with HFrEF were randomized.",
            }
        ]
        decision = [
            {
                "record_id": 1,
                "screening_phase": "pilot",
                "decision": "probable_include",
                "reason": "Eligible trial.",
                "supporting_text": "This sentence was invented.",
                "criteria": {key: "yes" for key in MODULE.CRITERIA},
            }
        ]
        with self.assertRaisesRegex(MODULE.ScreeningError, "not a verbatim"):
            MODULE.validate(records, decision)

    def test_validate_requires_minimum_pilot(self):
        records = [
            {"record_id": record_id, "title": f"Record {record_id}", "abstract": ""}
            for record_id in range(1, 9)
        ]
        decisions = [
            {
                "record_id": record_id,
                "screening_phase": "pilot" if record_id <= 7 else "main",
                "decision": "probable_include",
                "reason": "Eligible.",
                "supporting_text": f"Record {record_id}",
                "criteria": {key: "yes" for key in MODULE.CRITERIA},
            }
            for record_id in range(1, 9)
        ]
        with self.assertRaisesRegex(MODULE.ScreeningError, "pilot decisions must number"):
            MODULE.validate(records, decisions)

    def test_batch_rejects_more_than_twenty_records(self):
        with tempfile.TemporaryDirectory() as directory:
            records_path = Path(directory) / "records.jsonl"
            MODULE.write_jsonl(
                records_path,
                [
                    {
                        "record_id": 1,
                        "citation": "",
                        "title": "Test",
                        "abstract": "Test",
                        "pmid": "",
                        "doi": "",
                    }
                ],
            )
            args = type(
                "Args",
                (),
                {"records": str(records_path), "start": 1, "size": 21},
            )()
            with self.assertRaisesRegex(MODULE.ScreeningError, "between 1 and 20"):
                MODULE.command_batch(args)

    def test_export_retains_probable_include_and_maybe(self):
        records = [
            {
                "record_id": 1,
                "citation": "J Test. 2024.",
                "year": "2024",
                "title": "Include",
                "authors": "Smith J",
                "abstract": "Eligible population and intervention.",
                "pmid": "1",
                "doi": "",
            },
            {
                "record_id": 2,
                "citation": "J Test. 2023.",
                "year": "2023",
                "title": "Exclude",
                "authors": "Jones A",
                "abstract": "Mice were studied.",
                "pmid": "2",
                "doi": "",
            },
        ]
        decisions = [
            {
                "record_id": 1,
                "screening_phase": "pilot",
                "decision": "maybe",
                "reason": "Could qualify.",
                "concern": "Comparator not reported.",
                "supporting_text": "Eligible population and intervention.",
                "criteria": {key: "unclear" for key in MODULE.CRITERIA},
            },
            {
                "record_id": 2,
                "screening_phase": "pilot",
                "decision": "exclude",
                "reason": "Wrong population.",
                "supporting_text": "Mice were studied.",
                "criteria": {
                    **{key: "yes" for key in MODULE.CRITERIA},
                    "population": "no",
                },
            },
        ]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            records_path = root / "records.jsonl"
            decisions_path = root / "decisions.jsonl"
            output_path = root / "shortlist.csv"
            MODULE.write_jsonl(records_path, records)
            MODULE.write_jsonl(decisions_path, decisions)
            MODULE.command_export(
                type(
                    "Args",
                    (),
                    {
                        "records": str(records_path),
                        "decisions": str(decisions_path),
                        "output": str(output_path),
                    },
                )()
            )
            with output_path.open(encoding="utf-8-sig", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["screening_phase"], "pilot")
            self.assertEqual(rows[0]["screening_decision"], "maybe")
            with output_path.with_name("shortlist-audit.csv").open(
                encoding="utf-8-sig", newline=""
            ) as handle:
                audit_rows = list(csv.DictReader(handle))
            self.assertEqual(len(audit_rows), 2)


if __name__ == "__main__":
    unittest.main()
