#!/usr/bin/env python3
"""test_e143.py — checks the E143 numbers depend on."""
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))


class TestE143(unittest.TestCase):
    def setUp(self):
        self.arms_path = os.path.join(HERE, "arms.jsonl")
        self.gates_path = os.path.join(HERE, "gates.json")
        self.misses_path = os.path.join(HERE, "misses.json")

    def test_arms_exist(self):
        self.assertTrue(os.path.exists(self.arms_path), "arms.jsonl not found")
        with open(self.arms_path) as f:
            arms = [json.loads(line) for line in f]
        self.assertGreater(len(arms), 0, "no arms in arms.jsonl")
        for arm in arms:
            self.assertIn("document_number", arm)
            self.assertIn("preamble", arm)
            self.assertIn("cfr_amendments", arm)
            self.assertIn("has_digit", arm)

    def test_gates_exist(self):
        self.assertTrue(os.path.exists(self.gates_path), "gates.json not found")
        with open(self.gates_path) as f:
            gates = json.load(f)
        self.assertIn("results", gates)
        self.assertIn("gates", gates)
        self.assertIn("summary", gates)

    def test_gate_verdicts_present(self):
        with open(self.gates_path) as f:
            gates = json.load(f)
        for gate_name, gate_data in gates["gates"].items():
            self.assertIn("verdict", gate_data, f"gate {gate_name} missing verdict")

    def test_misses_exist(self):
        self.assertTrue(os.path.exists(self.misses_path), "misses.json not found")
        with open(self.misses_path) as f:
            misses = json.load(f)
        self.assertIn("misses", misses)
        self.assertIn("false_positives", misses)
        self.assertIn("counts", misses)

    def test_population_size(self):
        """Verify we have a reasonable population."""
        with open(self.arms_path) as f:
            arms = [json.loads(line) for line in f]
        # Should have fetched 20 documents
        self.assertGreaterEqual(len(arms), 10, "expected at least 10 documents with preamble/CFR boundary")


if __name__ == "__main__":
    unittest.main()