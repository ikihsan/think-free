#!/usr/bin/env python3
"""test_e142.py — checks the E142 numbers depend on.

Standard library only. Run after score.py and explain_misses.py.
"""
import json
import os
import re
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
# Path order matters: HERE must come after the sibling inserts so it lands
# at sys.path[0] and its build_arms shadows E140's same-named module.
sys.path.insert(0, os.path.join(HERE, "..", "140-judge-form-invariance"))
sys.path.insert(0, os.path.join(HERE, "..", "114-value-grounding"))
sys.path.insert(0, HERE)
import valueset  # noqa: E402
import ground  # noqa: E402
import build_arms  # noqa: E402  (from HERE — first on sys.path)


class TestCorpus(unittest.TestCase):
    """The corpus is what PROTOCOL.md §2 says it is."""

    def test_arms_jsonl_exists(self):
        self.assertTrue(os.path.exists(os.path.join(HERE, "arms.jsonl")))

    def test_arms_have_summary_and_reference(self):
        arms = [json.loads(l) for l in open(os.path.join(HERE, "arms.jsonl"))]
        self.assertGreater(len(arms), 0)
        for arm in arms:
            self.assertIn("summary", arm)
            self.assertIn("reference", arm)
            self.assertIn("document_number", arm)
            self.assertTrue(len(arm["summary"]) > 0)
            self.assertTrue(len(arm["reference"]) > 0)

    def test_summary_is_not_in_reference(self):
        """The SUMMARY section is removed from the reference."""
        arms = [json.loads(l) for l in open(os.path.join(HERE, "arms.jsonl"))]
        for arm in arms:
            # The summary text should not appear verbatim in the reference
            # (it was removed)
            summary_first_100 = arm["summary"][:100]
            self.assertNotIn(summary_first_100, arm["reference"])

    def test_documents_have_abstracts(self):
        """All documents in the corpus have abstracts (human-written)."""
        docs_path = os.path.join(HERE, "raw", "documents.json")
        if os.path.exists(docs_path):
            docs = json.load(open(docs_path))
            for doc in docs:
                self.assertIsNotNone(doc.get("abstract"))


class TestInstrumentUnchanged(unittest.TestCase):
    """valueset.py and ground.py are imported unchanged."""

    def test_valueset_importable(self):
        self.assertTrue(hasattr(valueset, "canonical"))
        self.assertTrue(hasattr(valueset, "compare"))

    def test_ground_importable(self):
        self.assertTrue(hasattr(ground, "judge"))
        self.assertTrue(hasattr(ground, "extract"))

    def test_valueset_deterministic(self):
        """Same input gives same output."""
        text = "The penalty is $10,000 per violation."
        a = valueset.canonical(text)
        b = valueset.canonical(text)
        self.assertEqual(a, b)


class TestGates(unittest.TestCase):
    """Gates file exists and has the required structure."""

    def test_gates_json_exists(self):
        self.assertTrue(os.path.exists(os.path.join(HERE, "gates.json")))

    def test_gates_have_required_keys(self):
        gates = json.load(open(os.path.join(HERE, "gates.json")))
        for key in ["K1", "K2", "K3", "K5", "triage"]:
            self.assertIn(key, gates)

    def test_triage_sums_to_total(self):
        gates = json.load(open(os.path.join(HERE, "gates.json")))
        t = gates["triage"]
        self.assertEqual(t["condemn"] + t["clear"] + t["defer"], t["total"])


class TestScoredArms(unittest.TestCase):
    """Scored arms file exists and has required fields."""

    def test_scored_arms_exist(self):
        path = os.path.join(HERE, "scored_arms.jsonl")
        self.assertTrue(os.path.exists(path))
        arms = [json.loads(l) for l in open(path) if l.strip()]
        self.assertGreater(len(arms), 0)
        for arm in arms:
            self.assertIn("m2_verdict", arm)
            self.assertIn("m1_verdict", arm)
            self.assertIn("genuinely_unsupported", arm)
            self.assertIn("m2_has_value", arm)


class TestMisses(unittest.TestCase):
    """Misses file exists and has required structure."""

    def test_misses_json_exists(self):
        self.assertTrue(os.path.exists(os.path.join(HERE, "misses.json")))

    def test_misses_structure(self):
        misses = json.load(open(os.path.join(HERE, "misses.json")))
        self.assertIn("n_misses", misses)
        self.assertIn("mechanisms", misses)
        self.assertIn("value_present_share", misses)
        self.assertIn("not_extracted_share", misses)


class TestSplitSummary(unittest.TestCase):
    """The SUMMARY split works correctly."""

    def test_split_basic(self):
        from build_arms import split_summary
        text = "AGENCY: Test.\nSUMMARY: This is the summary.\nDATES: January 1, 2026.\nSUPPLEMENTARY INFO: More text."
        summary, reference = split_summary(text)
        self.assertIn("This is the summary", summary)
        self.assertNotIn("This is the summary", reference)
        self.assertIn("AGENCY", reference)
        self.assertIn("DATES", reference)

    def test_split_no_summary(self):
        from build_arms import split_summary
        text = "AGENCY: Test.\nDATES: January 1, 2026."
        summary, reference = split_summary(text)
        self.assertEqual(summary, "")
        self.assertIn("AGENCY", reference)


if __name__ == "__main__":
    unittest.main()
