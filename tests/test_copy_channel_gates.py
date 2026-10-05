"""The gates and controls of E020, read from the committed artifacts.

Split from `tests/test_copy_channel.py` at the 300-line cap. That file holds the
instrument's own properties -- what a capture on disk means and cannot be made to
mean. This one holds what the run concluded: both declared gates, all four
controls, and the refusal H2 could not be answered from.

Every assertion reads `EXPERIMENTS/020-copied-artifact-serving/` rather than a
fixture, so a test cannot pass against bytes the experiment did not produce.
"""

import importlib.util
import json
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPERIMENT = os.path.join(ROOT, "EXPERIMENTS", "020-copied-artifact-serving")
sys.path.insert(0, EXPERIMENT)


def _load(filename):
    spec = importlib.util.spec_from_file_location(
        "e020t_" + filename[:-3], os.path.join(EXPERIMENT, filename))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


forkstatus = _load("forkstatus.py")
tally = _load("tally.py")
captureformat = _load("captureformat.py")
RAW = os.path.join(EXPERIMENT, "raw")


def load(name):
    with open(os.path.join(EXPERIMENT, name)) as handle:
        return json.load(handle)


class SingleNamingRuleTest(unittest.TestCase):
    """Defect 3: two copies of one rule, and all 22 configurations lost."""

    def test_writer_and_reader_agree_on_the_capture_name(self):
        pattern = "^\\.claude/hooks/"
        name = forkstatus.slug_for(pattern)
        self.assertTrue(
            os.path.exists(os.path.join(RAW, name + ".sse")),
            "the consumer looks for a file the writer never wrote",
        )

    def test_every_declared_pattern_resolves_to_a_capture(self):
        for _key, pattern in forkstatus.PATTERNS:
            name = forkstatus.slug_for(pattern)
            self.assertTrue(
                os.path.exists(os.path.join(RAW, name + ".sse")),
                "no capture on disk for %s" % pattern,
            )


class CoverageControlTest(unittest.TestCase):
    """C2 -- the control that can refuse the experiment."""

    def setUp(self):
        self.cov = load("coverage.json")

    def test_no_row_is_left_unanswered(self):
        for arm, block in self.cov["coverage"].items():
            self.assertEqual(
                block["unanswered"], 0,
                "arm %s has rows this session never obtained an answer for" % arm,
            )

    def test_young_arm_is_covered_so_h1_is_evaluable(self):
        block = self.cov["coverage"]["young"]
        self.assertGreaterEqual(
            block["in_index"] / float(block["n"]), 0.9,
            "the young arm is mostly outside the index, so H1 would be a "
            "statement about the instrument rather than the field",
        )

    def test_placebo_arm_is_invisible_and_that_is_recorded(self):
        """The second finding: this instrument cannot see unpopular work."""
        block = self.cov["coverage"]["placebo"]
        self.assertEqual(block["in_index"], 0)
        results = load("results.json")
        self.assertEqual(results["c2_coverage"]["placebo"]["in_index"], 0)


class GateTest(unittest.TestCase):
    """Both declared gates, read from results.json, in one direction each."""

    def setUp(self):
        self.results = load("results.json")

    def test_h1_is_dead_and_the_ratio_is_below_the_declared_floor(self):
        h1 = self.results["h1"]
        self.assertEqual(h1["verdict"], "dead")
        self.assertLessEqual(h1["ratio"], tally.H1_DEAD_RATIO)
        self.assertEqual(h1["copies"], 1026)

    def test_h2_is_not_evaluated_and_says_why(self):
        h2 = self.results["h2"]
        self.assertEqual(h2["verdict"], "not_evaluated")
        self.assertTrue(h2.get("reason"))
        self.assertEqual(h2["high_n"], 9)
        self.assertEqual(h2["low_n"], 0)

    def test_a_single_band_is_not_reported_as_a_rate(self):
        """The blind rule for this gate: compute it over the high band alone.

        Checked against `tally.py`'s own decision, not only against the committed
        results.json. Reading the artifact alone would pass on a stale file --
        reintroducing the defect in the code changed nothing the test could see,
        which is exactly the blindness this test exists to prevent.
        """
        h2 = self.results["h2"]
        self.assertNotIn("rate", h2,
                         "a rate was computed over one band, which is not the "
                         "rate the protocol declares")

        rows = load("forkstatus.json")["rows"]
        decided = tally.h2_from_rows(rows)
        self.assertEqual(decided["verdict"], "not_evaluated",
                         "the gate computed something from a single band")
        self.assertNotIn("rate", decided)
        self.assertTrue(decided["high_n"] >= 9)
        self.assertEqual(decided["low_n"], 0)

    @staticmethod
    def _bands(high_rows, low_rows):
        return [{"state": "ok", "copies": c, "fork": f, "is_template": t}
                for c, f, t in high_rows + low_rows]

    def test_the_gate_computes_a_rate_when_both_bands_are_present(self):
        """The rule must not be 'never answer' -- it answers when it can.

        Three cases spanning the declared thresholds: 1 of 5 forked (0.20) is
        `survives`, 2 of 5 (0.40) is `inconclusive`, 4 of 5 (0.80) is `dead`. The
        middle one is the one that matters, because a gate that only ever answers
        at the extremes is not measuring anything.
        """
        survives = tally.h2_from_rows(GateTest._bands(
            [(500, False, False), (300, True, False), (200, False, False),
             (150, False, False), (120, False, False)],
            [(3, False, False), (2, True, True)]))
        self.assertEqual(survives["verdict"], "survives")
        self.assertAlmostEqual(survives["rate"], 0.2)

        middle = tally.h2_from_rows(GateTest._bands(
            [(500, False, False), (300, True, False), (200, False, False),
             (150, True, False), (120, False, False)],
            [(3, False, False)]))
        self.assertEqual(middle["verdict"], "inconclusive")
        self.assertAlmostEqual(middle["rate"], 0.4)

        dead = tally.h2_from_rows(GateTest._bands(
            [(500, True, False), (300, False, True), (200, True, False),
             (150, False, False), (120, True, True)],
            [(1, False, False)]))
        self.assertEqual(dead["verdict"], "dead")
        self.assertAlmostEqual(dead["rate"], 0.8)

    def test_a_row_outside_both_bands_is_not_counted(self):
        """The declared gap: a band this wide cannot order anything."""
        decided = tally.h2_from_rows(GateTest._bands(
            [(500, False, False), (300, False, False)],
            [(50, True, True), (42, False, False)]))
        self.assertEqual(decided["high_n"], 2)
        self.assertEqual(decided["low_n"], 0,
                         "a configuration at 42 copies is not in the <=5 band")

    def test_every_control_is_reported(self):
        for key in ("c1_calibration", "c2_coverage", "c3_mature_control"):
            self.assertIn(key, self.results)
            self.assertTrue(self.results[key])

    def test_ceilings_travel_with_the_numbers(self):
        notes = self.results["instrument"]["ceilings"]
        self.assertTrue(any("floor" in c for c in notes))
        self.assertFalse(self.results["instrument"]["authenticated"])


class MatureControlTest(unittest.TestCase):
    """C3 -- the strong baseline, not a weak one."""

    def test_a_mature_hook_script_outranks_the_young_one(self):
        c3 = load("results.json")["c3_mature_control"]
        self.assertGreater(c3["mature hook script"]["count"], 1026)

    def test_mature_configurations_are_copied_more_than_young_ones(self):
        c3 = load("results.json")["c3_mature_control"]
        self.assertGreater(c3["mature hook runner configuration"]["count"], 1026)


class RebuiltIndexTest(unittest.TestCase):
    """Defects 4 and 5: the index is derived from raw, and raw carries its query."""

    def test_index_is_rebuildable_from_raw(self):
        records = captureformat.rebuild_index()
        self.assertGreater(len(records), 50)
        self.assertTrue(any(r["state"] == "ok" and r["count"] == 1026 for r in records))

    def test_rebuild_does_not_lose_counts(self):
        """A rebuild must recover every count a prior build held.

        The index is derived from raw, so this is the property that makes raw the
        ground truth. It is asserted against counts, not against a file count,
        because a rebuild that kept every filename while losing a value would
        still look intact.
        """
        before = {}
        path = os.path.join(EXPERIMENT, "copycount.json")
        if os.path.exists(path):
            with open(path) as handle:
                before = {r["name"]: r.get("count") for r in json.load(handle)["records"]}
        records = captureformat.rebuild_index()
        after = {r["name"]: r.get("count") for r in records}
        for name, value in before.items():
            if value is not None:
                self.assertEqual(after.get(name), value,
                                 "rebuild changed %s from %s to %s" % (name, value, after.get(name)))
        self.assertTrue(any(v == 1026 for v in after.values()) or
                        load("results.json")["h1"].get("capture_lost"))

    def test_headerless_captures_are_marked_as_such(self):
        legacy = tally.headerless_captures()
        self.assertTrue(legacy, "the pre-header captures are not identified")
        for rec in legacy.values():
            self.assertEqual(rec["attributed_by"], "slug")


class LowBandDeclarationTest(unittest.TestCase):
    """The low band is a mechanical slice, so a rerun needs no new decisions."""

    def test_slice_is_deterministic(self):
        self.assertEqual(forkstatus.low_band_paths(), forkstatus.low_band_paths())

    def test_slice_is_non_empty_and_draws_from_real_paths(self):
        sample = forkstatus.low_band_paths()
        self.assertTrue(sample)
        for _key, pattern in sample:
            self.assertTrue(pattern.startswith("^\\.claude/hooks/"),
                            "a low-band pattern outside the declared population")


if __name__ == "__main__":
    unittest.main()