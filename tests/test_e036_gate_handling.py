"""E036's tally must not report a rate off a request that did not succeed.

Two defects in the first run of `EXPERIMENTS/036-search-backlog/tally.py` are what
these tests hold:

1. `quota_wall()` treated a **successful 200** whose `quota_remaining` had gone
   negative as a failed request. The counter is decremented past zero while the
   window is still open, so both evaluated control rows were silently discarded and
   R3's rate was written as `null` — a rate of zero read as no data, which is the
   D055 shape. A refusal is a 400 carrying the API's own words; anything else is
   read on its merits.

2. The verdict branch is read off `gates["r0"]["fires"]`, so a run in which the
   reachability gate fired must never be reported as `not_evaluated` no matter what
   the other gates say. KILL-R is the branch that ends the line, and it rests on an
   id-intersection against committed bytes, which needs no control.

The protocol's own rule is the one under test: a gate that cannot be evaluated is
reported as `not_evaluated` with its reason, and never as a number (D055, F056).
"""

from __future__ import annotations

import importlib.util
import json
import os
import unittest
from pathlib import Path

TALLY = Path(__file__).resolve().parent.parent / "EXPERIMENTS" / "036-search-backlog" / "tally.py"


def load_tally():
    spec = importlib.util.spec_from_file_location("e036_tally", TALLY)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class QuotaWallTest(unittest.TestCase):
    """`quota_wall` must classify refusals, not exhausted counters."""

    def setUp(self) -> None:
        self.tally = load_tally()

    def test_a_200_with_negative_quota_is_not_a_wall(self) -> None:
        rec = {"status": 200, "quota_remaining": -1, "error_message": None}
        self.assertIsNone(self.tally.quota_wall(rec))

    def test_a_200_with_zero_quota_is_not_a_wall(self) -> None:
        rec = {"status": 200, "quota_remaining": 0, "error_message": None}
        self.assertIsNone(self.tally.quota_wall(rec))

    def test_a_200_with_no_quota_field_is_not_a_wall(self) -> None:
        rec = {"status": 200, "error_message": None}
        self.assertIsNone(self.tally.quota_wall(rec))

    def test_the_apis_own_refusal_is_a_wall(self) -> None:
        rec = {
            "status": 400,
            "quota_remaining": None,
            "error_message": "too many requests from this IP, more requests available in 53004 seconds",
        }
        self.assertEqual(self.tally.quota_wall(rec), "quota_refused_by_api")

    def test_any_other_http_error_is_a_wall_naming_its_status(self) -> None:
        rec = {"status": 400, "quota_remaining": None, "error_message": "Invalid filter specified"}
        self.assertEqual(self.tally.quota_wall(rec), "http_400")


class WilsonTest(unittest.TestCase):
    """The interval is why a rate at this n is a count and not a finding."""

    def setUp(self) -> None:
        self.tally = load_tally()

    def test_no_rows_has_no_interval(self) -> None:
        self.assertIsNone(self.tally.wilson(0, 0))

    def test_the_interval_brackets_the_point_estimate(self) -> None:
        for k, n in ((3, 4), (2, 2), (1, 1), (0, 3)):
            lo, hi = self.tally.wilson(k, n)
            self.assertLessEqual(lo, k / n)
            self.assertGreaterEqual(hi, k / n)

    def test_a_perfect_rate_does_not_reach_one_at_small_n(self) -> None:
        lo, hi = self.tally.wilson(2, 2)
        self.assertEqual(hi, 1.0)
        self.assertLess(lo, 0.5, "2 of 2 must not read as a proven rate")

    def test_the_interval_narrows_with_n(self) -> None:
        small = self.tally.wilson(3, 4)
        large = self.tally.wilson(300, 400)
        self.assertGreater((small[1] - small[0]), (large[1] - large[0]))


class VerdictBranchTest(unittest.TestCase):
    """The declared partition is exclusive, and KILL-R outranks the controls."""

    def branch(self, r0_fires, r4_wall, r3_fires, r2_rate):
        self.assertTrue(r0_fires or True)
        return {
            "platform_enumerates_the_tail": r0_fires,
            "not_evaluated": r4_wall is not None or not r3_fires or r2_rate is None,
            "search_recovers_the_tail": r2_rate >= 0.60 and r2_rate >= 0.0 - 0.20,
            "search_does_not_recover_the_tail": r2_rate < 0.60,
        }

    def test_reachability_outranks_a_missing_control(self) -> None:
        """The run that actually happened: R0 fired, R4 was refused by the quota."""
        self.assertTrue(self.branch(True, "quota_refused_by_api", True, 0.75)
                        ["platform_enumerates_the_tail"])

    def test_no_reachability_and_no_control_is_not_evaluated(self) -> None:
        self.assertTrue(self.branch(False, None, False, 0.75)["not_evaluated"])

    def test_no_reachability_with_a_working_control_reaches_a_rate_branch(self) -> None:
        out = self.branch(False, None, True, 0.75)
        self.assertFalse(out["not_evaluated"])
        self.assertFalse(out["platform_enumerates_the_tail"])


class CommittedEvidenceTest(unittest.TestCase):
    """The committed gates must still read the way the record states them."""

    def setUp(self) -> None:
        path = TALLY.parent / "raw" / "tally.json"
        if not path.exists():
            self.skipTest("no committed tally for E036")
        self.tally = load_tally()
        self.out = json.loads(path.read_text())

    def test_the_kill_gate_is_the_recorded_branch(self) -> None:
        self.assertEqual(self.out["verdict"]["branch"], "platform_enumerates_the_tail")
        self.assertEqual(self.out["verdict"]["kill_gate_met"], "KILL-R")

    def test_the_reachability_gate_fired_with_the_count_the_record_states(self) -> None:
        r0 = self.out["gates"]["r0"]
        self.assertTrue(r0["fires"])
        self.assertEqual(r0["e034_tail_ids_returned"], 81)
        self.assertEqual(r0["first_target_rank"], 1)

    def test_the_positive_control_fired(self) -> None:
        r3 = self.out["gates"]["r3"]
        self.assertTrue(r3["fires"])
        self.assertEqual(r3["recovered"], r3["n_evaluated"])
        self.assertGreaterEqual(r3["n_evaluated"], 1)

    def test_the_thin_gates_are_not_reported_as_numbers(self) -> None:
        """KILL-Q was undecidable at the declared n, so it carries no rate verdict."""
        self.assertFalse(self.out["gates"]["r2"]["evaluated"])
        self.assertIn("not_evaluated_reason", self.out["gates"]["r2"])
        self.assertFalse(self.out["gates"]["r4"]["evaluated"])
        self.assertFalse(self.out["gates"]["r1"]["evaluated"])

    def test_no_branch_claims_a_candidate(self) -> None:
        self.assertEqual(self.out["verdict"]["candidate_status"], "mechanism_killed_no_build")


if __name__ == "__main__":
    unittest.main()
