#!/usr/bin/env python3
"""test_e143.py — unit tests for E143 gates and mechanisms.

Standard library only. These tests assert the properties the numbers depend on.
"""
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))


class TestE143Gates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        gates_path = os.path.join(HERE, "gates.json")
        if not os.path.exists(gates_path):
            raise FileNotFoundError("gates.json not found. Run score.py first.")
        with open(gates_path) as f:
            cls.gates = json.load(f)

        scored_path = os.path.join(HERE, "scored_arms.jsonl")
        if not os.path.exists(scored_path):
            raise FileNotFoundError("scored_arms.jsonl not found. Run score.py first.")
        cls.arms = [json.loads(l) for l in open(scored_path) if l.strip()]

        misses_path = os.path.join(HERE, "misses.json")
        if os.path.exists(misses_path):
            with open(misses_path) as f:
                cls.misses = json.load(f)
        else:
            cls.misses = None

    def test_gates_exist(self):
        """All declared gates are present in the output."""
        for gate in ["K1", "K2", "K3", "K4_A_and_D", "K4_B_and_D", "K5"]:
            self.assertIn(gate, self.gates, f"Gate {gate} missing from gates.json")

    def test_k1_verdict_reproducible(self):
        """K1 verdict matches the declared threshold."""
        k1 = self.gates["K1"]
        if k1["verdict"] != "NOT_EVALUATED":
            expected = "PASS" if k1["rate"] >= 0.95 else "FAIL"
            self.assertEqual(k1["verdict"], expected, "K1 verdict does not match rate")

    def test_k2_verdict_reproducible(self):
        """K2 verdict matches the declared threshold."""
        k2 = self.gates["K2"]
        if k2["verdict"] != "NOT_EVALUATED":
            expected = "PASS" if k2["rate"] <= 0.02 else "FAIL"
            self.assertEqual(k2["verdict"], expected, "K2 verdict does not match rate")

    def test_k3_verdict_reproducible(self):
        """K3 verdict matches the declared threshold."""
        k3 = self.gates["K3"]
        if k3["verdict"] != "NOT_EVALUATED":
            expected = "PASS" if k3["rate"] >= 0.30 else "FAIL"
            self.assertEqual(k3["verdict"], expected, "K3 verdict does not match rate")

    def test_k5_verdict_reproducible(self):
        """K5 verdict matches the declared threshold."""
        k5 = self.gates["K5"]
        if k5["verdict"] != "NOT_EVALUATED":
            expected = "PASS" if k5["rate"] >= 0.30 else "FAIL"
            self.assertEqual(k5["verdict"], expected, "K5 verdict does not match rate")

    def test_arms_consistent_with_gates(self):
        """Gate counts match direct computation from scored_arms.jsonl."""
        a_arms = [a for a in self.arms if not a["genuinely_unsupported"]]
        b_arms = [a for a in self.arms if a["genuinely_unsupported"]]

        # K1: detection on B
        if b_arms:
            detected = sum(1 for a in b_arms if a["m2_verdict"] == "condemn")
            self.assertEqual(self.gates["K1"]["detected"], detected)
            self.assertEqual(self.gates["K1"]["total"], len(b_arms))

        # K2: FP on A
        if a_arms:
            fp = sum(1 for a in a_arms if a["m2_verdict"] == "condemn")
            self.assertEqual(self.gates["K2"]["fp"], fp)
            self.assertEqual(self.gates["K2"]["total"], len(a_arms))

        # K3: coverage on A
        if a_arms:
            covered = sum(1 for a in a_arms if a["m2_has_value"])
            self.assertEqual(self.gates["K3"]["covered"], covered)
            self.assertEqual(self.gates["K3"]["total"], len(a_arms))

        # K5: conditional coverage
        n_arms = [a for a in self.arms if a["has_digit"]]
        if n_arms:
            covered = sum(1 for a in n_arms if a["m2_has_value"])
            self.assertEqual(self.gates["K5"]["covered"], covered)
            self.assertEqual(self.gates["K5"]["total"], len(n_arms))

    def test_triage_categories_exhaustive_and_disjoint(self):
        """Triage categories sum to total and are mutually exclusive."""
        total = len(self.arms)
        condemn = sum(1 for a in self.arms if a["m2_verdict"] == "condemn")
        defer = sum(1 for a in self.arms if not a["m2_has_value"])
        clear = total - condemn - defer

        self.assertEqual(self.gates["triage"]["total"], total)
        self.assertEqual(self.gates["triage"]["condemn"], condemn)
        self.assertEqual(self.gates["triage"]["defer"], defer)
        self.assertEqual(self.gates["triage"]["clear"], clear)
        # No arm can be both condemn and defer
        for a in self.arms:
            if a["m2_verdict"] == "condemn":
                self.assertTrue(a["m2_has_value"], "condemn arm must have values")

    def test_miss_mechanisms_sum_to_total(self):
        """If misses exist, mechanisms sum to n_misses."""
        if self.misses and self.misses["n_misses"] > 0:
            mech_sum = sum(self.misses["mechanisms"].values())
            self.assertEqual(mech_sum, self.misses["n_misses"])


if __name__ == "__main__":
    unittest.main()