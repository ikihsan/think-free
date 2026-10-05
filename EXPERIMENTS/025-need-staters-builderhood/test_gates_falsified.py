#!/usr/bin/env python3
"""Falsification for E025's own instruments, per docs/policy/gate-falsification.md.

A gate that has never been watched fail is a gate nobody can trust. Each check
below asserts the property against a fixture chosen to BREAK it, and one check
asserts the naive rule is green on the defect it replaced.
"""
import json
import math
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import stats  # noqa: E402


class WilsonTest(unittest.TestCase):
    def test_zero_of_24_has_the_interval_the_record_states(self):
        """F042's 0/24 is quoted in the record with CI95 [0.0, 0.138]. If this
        disagreed, every comparison in results.json would move silently."""
        p, lo, hi = stats.wilson(0, 24)
        self.assertEqual(p, 0.0)
        self.assertAlmostEqual(hi, 0.1380, places=3)

    def test_ceiling_is_below_the_normal_approximation(self):
        """The reason Wilson is used: at a boundary the normal interval for 0/24
        is exactly zero, which reads as certainty."""
        p = 0.0
        n = 24.0
        z = 1.96
        normal_hi = p + z * math.sqrt(p * (1 - p) / n)
        self.assertEqual(normal_hi, 0.0)
        self.assertGreater(stats.wilson(0, 24)[2], 0.10)

    def test_empty_arm_returns_none_rather_than_a_zero(self):
        """A population nobody read must not read as 0. This is the defect that
        made 017's H2 thresholds pass on an empty read (STATE-constraints.md)."""
        p, lo, hi = stats.wilson(0, 0)
        self.assertIsNone(p)
        self.assertIsNone(lo)
        self.assertIsNone(hi)


class ArmStatsTest(unittest.TestCase):
    def _rows(self, spec):
        return {a: {"author": a, "status": "ok", "nb_show_hn": n} for a, n in spec}

    def test_a_refused_fetch_is_not_counted_as_a_non_builder(self):
        """The decisive one. If a refusal became a 0, a rate-limited hour would
        read as a population that does not build -- a clean confident wrong
        finding, which is the F041 defect-6 shape."""
        rows = self._rows([("a", 0), ("b", 0)])
        rows["c"] = {"author": "c", "status": "rate_limited", "nb_show_hn": None}
        s = stats.arm_stats(rows, "test")
        self.assertEqual(s["authors_fetched_ok"], 2)
        self.assertEqual(s["authors_refused"], 1)
        self.assertEqual(s["authors_with_at_least_one_show_hn"], 0)
        # and it must be visible, not silently dropped
        self.assertIn("c", s["refused_authors"])

    def test_a_null_count_is_excluded_from_the_denominator(self):
        rows = self._rows([("a", 1)])
        rows["b"] = {"author": "b", "status": "ok", "nb_show_hn": None}
        s = stats.arm_stats(rows, "test")
        self.assertEqual(s["authors_fetched_ok"], 1)
        self.assertEqual(s["raw_rate"], 1.0)

    def test_rate_is_k_over_n(self):
        s = stats.arm_stats(self._rows([("a", 0), ("b", 0), ("c", 3), ("d", 0)]), "t")
        self.assertEqual(s["authors_fetched_ok"], 4)
        self.assertEqual(s["authors_with_at_least_one_show_hn"], 1)
        self.assertEqual(s["raw_rate"], 0.25)

    def test_more_than_one_show_hn_still_counts_once(self):
        """The unit is authors, not posts. An author with 152 posts must not
        outweigh an author with 1."""
        s = stats.arm_stats(self._rows([("a", 152), ("b", 1), ("c", 0)]), "t")
        self.assertEqual(s["authors_with_at_least_one_show_hn"], 2)


class OverlapTest(unittest.TestCase):
    def _a(self, lo, hi):
        return {"ci95_low": lo, "ci95_high": hi}

    def test_overlapping_intervals_are_reported_as_overlapping(self):
        self.assertTrue(stats.overlap(self._a(0.10, 0.40), self._a(0.20, 0.50)))

    def test_disjoint_intervals_are_reported_as_disjoint(self):
        self.assertFalse(stats.overlap(self._a(0.01, 0.10), self._a(0.30, 0.50)))

    def test_touching_intervals_overlap(self):
        self.assertTrue(stats.overlap(self._a(0.0, 0.30), self._a(0.30, 0.60)))

    def test_an_unread_arm_is_neither_overlapping_nor_disjoint(self):
        """Three-valued: a gate with a binary answer here would read 'no overlap'
        from a population nobody read."""
        self.assertIsNone(stats.overlap({"ci95_low": None, "ci95_high": None},
                                        self._a(0.3, 0.5)))


class LoadTest(unittest.TestCase):
    def test_a_later_row_supersedes_an_earlier_one(self):
        """The fetcher appends a second row per author when it fills in the
        footprint. Without this, the file has two rows for one author and the
        arm denominator is inflated by however many authors were touched twice."""
        with tempfile.TemporaryDirectory() as d:
            raw = os.path.join(d, "raw")
            os.makedirs(raw)
            p = os.path.join(raw, "need_arm.jsonl")
            with open(p, "w") as f:
                f.write(json.dumps({"author": "a", "status": "ok",
                                    "nb_show_hn": 0, "total_items_by_author": None}) + "\n")
                f.write(json.dumps({"author": "a", "status": "ok",
                                    "nb_show_hn": 0, "total_items_by_author": 42}) + "\n")
                f.write(json.dumps({"author": "b", "status": "ok",
                                    "nb_show_hn": 1, "total_items_by_author": None}) + "\n")
            old = stats.RAW
            stats.RAW = raw
            try:
                rows = stats.load("need_arm.jsonl")
            finally:
                stats.RAW = old
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows["a"]["total_items_by_author"], 42)

    def test_a_malformed_line_does_not_abort_the_load(self):
        """Raw captures are append-only and a partial line must not silently
        shorten a denominator."""
        with tempfile.TemporaryDirectory() as d:
            raw = os.path.join(d, "raw")
            os.makedirs(raw)
            p = os.path.join(raw, "need_arm.jsonl")
            with open(p, "w") as f:
                f.write('{"author": "a", "status": "ok", "nb_show_hn": 0}\n')
                f.write("{not json\n")
                f.write('{"author": "b", "status": "ok", "nb_show_hn": 1}\n')
            old = stats.RAW
            stats.RAW = raw
            try:
                rows = stats.load("need_arm.jsonl")
            finally:
                stats.RAW = old
            self.assertEqual(sorted(rows), ["a", "b"])


class GateA1ControlSelectionTest(unittest.TestCase):
    def test_the_original_control_set_would_have_failed_and_the_instrument_did_not(self):
        """The instrument defect, asserted rather than narrated.

        PROTOCOL.md named four controls believed positive. Two of them have no
        Show HN post at all, so the set fails its own gate. The capture keeps
        their zeros. If a future reader restores them, this test is the record
        that they were checked and found empty.
        """
        p = os.path.join(HERE, "raw", "gate_a1_controls.jsonl")
        if not os.path.exists(p):
            self.skipTest("capture not present")
        rows = {}
        with open(p) as f:
            for line in f:
                line = line.strip()
                if line:
                    d = json.loads(line)
                    rows[d["author"]] = d["nb_show_hn"]
        empty = [a for a in ("patio11", "chromium") if rows.get(a) == 0]
        self.assertEqual(sorted(empty), ["chromium", "patio11"],
                         "the two controls recorded as 0 must stay recorded as 0")
        self.assertGreater(rows.get("pg"), 0)
        self.assertGreater(rows.get("antirez"), 0)

    def test_nonsense_control_reads_zero(self):
        p = os.path.join(HERE, "raw", "gate_a1_controls.jsonl")
        if not os.path.exists(p):
            self.skipTest("capture not present")
        rows = {}
        with open(p) as f:
            for line in f:
                line = line.strip()
                if line:
                    d = json.loads(line)
                    rows[d["author"]] = d["nb_show_hn"]
        self.assertEqual(rows.get("zzqqxxnonsensecontrol"), 0)


if __name__ == "__main__":
    unittest.main()
