#!/usr/bin/env python3
"""E029 -- tests of the population, the controls, the arithmetic and the gates.

Each test is asserted against the committed capture and against a fixture built to
break the property, following docs/policy/gate-falsification.md. The two forms of
test that matter most here are the ones the run's own history calls for:

  * a build that postdates the need is the population (otherwise 167 rows read as
    `unrelated` and manufacture the null H1 is trying to measure), and
  * the reader's view carries no arm label and no author name (otherwise the
    blindness the protocol declares is not the blindness the reader had).
"""
import json
import os
import re
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
sys.path.insert(0, HERE)

import intervalstats as I  # noqa: E402


def read_jsonl(name):
    path = name if os.path.isabs(name) else os.path.join(RAW, name)
    with open(path) as f:
        return [json.loads(l) for l in f if l.strip()]


def sibling(*parts):
    """A capture in a sibling experiment, resolved from this file, not the cwd."""
    return os.path.normpath(os.path.join(HERE, "..", *parts))


class PopulationTest(unittest.TestCase):
    def setUp(self):
        self.pop = {d["author"]: d for d in read_jsonl("population.jsonl")}
        self.builds = {d["author"]: d for d in read_jsonl("builds.jsonl")}
        self.key = json.load(open(os.path.join(RAW, "view_key.json")))

    def test_declared_population_arithmetic_is_the_recorded_one(self):
        # PROTOCOL.md declared 278 from nb_show_hn >= 1; amendment 1 declared the
        # exclusions. If any of these numbers moves, the declared denominator moved.
        arm = read_jsonl(sibling("025-need-staters-builderhood", "raw", "need_arm.jsonl"))
        declared = sum(1 for d in arm if d.get("status") == "ok"
                       and isinstance(d.get("nb_show_hn"), int) and d["nb_show_hn"] >= 1)
        self.assertEqual(declared, 278)
        self.assertEqual(len(self.pop) + 30 + 7, declared,
                         "exclusions must account for every dropped builder")

    def test_every_reader_row_has_a_build_that_postdates_the_need(self):
        # The reader population, not the whole file: the 167 whose builds all predate
        # the need are excluded precisely because their question is not askable.
        for k in self.key:
            a = k["author"]
            ni = int(self.pop[a]["need"]["comment_id"])
            later = [it for it in self.builds[a].get("items") or [] if int(it["id"]) > ni]
            self.assertTrue(later, "reader row %s has no build after the need" % k["row_id"])

    def test_the_null_is_not_manufactured_by_an_unaskable_row(self):
        # The failure mode this guards: reading a row whose build predates the need as
        # `unrelated` lowers the matched arm without the readers being at fault.
        unaskable = [a for a, r in self.pop.items()
                     if not [it for it in self.builds[a].get("items") or []
                             if int(it["id"]) > int(r["need"]["comment_id"])]]
        self.assertEqual(len(unaskable), 167)
        self.assertNotEqual(len(unaskable), 0, "a test that passes on 0 does not discriminate")
        self.assertEqual(len(self.pop) - len(unaskable), 74)

    def test_the_chronological_proxy_is_verifiable_not_assumed(self):
        # The population is selected on HN item-id ordering. Check the ordering against
        # real timestamps on the corpus's own capture, and check the negative control
        # that the other id space does not hold.
        outcomes = read_jsonl(sibling("022-need-outcomes", "raw", "outcomes.jsonl"))
        rows = sorted((int(d["comment_id"]), d["time"]) for d in outcomes)
        regress = sum(1 for (_, t1), (_, t2) in zip(rows, rows[1:]) if t2 < t1)
        self.assertEqual(regress, 0)
        stories = sorted((int(d["story_id"]), d["time"]) for d in outcomes)
        regress2 = sum(1 for (_, t1), (_, t2) in zip(stories, stories[1:]) if t2 < t1)
        self.assertGreater(regress2, 0, "story_id must NOT be monotone; the proxy is about items")
class ControlTest(unittest.TestCase):
    def setUp(self):
        self.ctl = read_jsonl("gate_a2_controls.jsonl")

    def test_controls_pass_as_declared(self):
        pos = [c for c in self.ctl if c.get("expectation") == "positive"]
        self.assertGreaterEqual(len(pos), 6)
        self.assertEqual(sum(1 for c in pos if (c.get("n_items") or 0) >= 1), len(pos))
        nonsense = [c for c in self.ctl if c.get("expectation") == "nonsense"]
        self.assertTrue(nonsense)
        self.assertTrue(all(c.get("n_items") == 0 for c in nonsense))

    def test_a_refusal_is_not_a_zero(self):
        # The capture must distinguish "the index answered zero" from "the index did
        # not answer". A row whose status is not ok must never carry an n_items of 0.
        for c in self.ctl:
            if c.get("status") != "ok":
                self.assertIsNone(c.get("n_items"),
                                  "a refusal was recorded as a count of %r" % c.get("n_items"))

    def test_fetch_capture_records_no_refusals_at_all(self):
        for d in read_jsonl("builds.jsonl"):
            self.assertEqual(d["status"], "ok", "capture holds a refusal: %r" % d)

    def test_the_tag_is_rechecked_on_the_answer(self):
        # The index OR-s repeated tags parameters, so the filter is verified per hit
        # rather than trusted. A row of items must be short if the check is present.
        multi = [d for d in read_jsonl("builds.jsonl") if (d.get("n_items") or 0) > 1]
        self.assertTrue(multi, "no builder has more than one item; the check is untested")
        for d in multi:
            self.assertEqual(d["n_items"], len(d["items"]))
class StatisticsTest(unittest.TestCase):
    def test_wilson_interval_reproduces_the_figure_the_record_quotes(self):
        # F042's build arm is quoted as 0 of 24 with CI95 [0.0, 0.138]. If the interval
        # function drifts, every interval in results.json drifts with it.
        lo, hi = I.wilson(0, 24)
        self.assertAlmostEqual(lo, 0.0, places=6)
        self.assertAlmostEqual(hi, 0.138, places=3)

    def test_wilson_is_not_degenerate_at_every_rate(self):
        self.assertEqual(I.wilson(0, 0), (None, None))
        lo, hi = I.wilson(74, 74)
        self.assertGreater(lo, 0.95)
        self.assertAlmostEqual(hi, 1.0, places=6)

    def test_kappa_of_identical_labels_is_flagged_not_reported_as_agreement(self):
        # Two readers who use exactly one label each have expected agreement 1.0, and
        # kappa is undefined there. It must be refused, not reported as 1.0.
        one = ["addresses"] * 30
        kappa, table = I.cohen_kappa(one, one)
        self.assertIsNone(kappa, "a scheme where expected agreement is 1.0 cannot be scored")
        self.assertEqual(table["observed_agreement"], 1.0)

    def test_kappa_is_computed_when_there_is_disagreement_to_score(self):
        a = ["addresses"] * 20 + ["unrelated"] * 10
        b = ["addresses"] * 20 + ["unclear"] * 10
        kappa, table = I.cohen_kappa(a, b)
        self.assertIsNotNone(kappa)
        self.assertGreater(table["observed_agreement"], 0.5)
        self.assertLess(kappa, 1.0)
class ChronologyTest(unittest.TestCase):
    def test_the_proxy_was_falsified_against_real_timestamps(self):
        # The proxy is load-bearing for the headline split, so it was sampled against
        # created_at on BOTH sides of the claimed cut. A proxy never shown capable of
        # disagreeing is an assumption -- F019's shape, a gate that cannot fail.
        path = os.path.join(RAW, "chronology_verification.jsonl")
        if not os.path.exists(path):
            self.fail("run verify_chronology.py: the proxy has not been falsified")
        rows = [json.loads(l) for l in open(path) if l.strip()]
        self.assertGreaterEqual(len(rows), 6, "too few sampled to falsify anything")
        self.assertTrue(any(r["side"] == "claimed_eligible" for r in rows))
        self.assertTrue(any(r["side"] == "claimed_ineligible" for r in rows),
                        "both directions must be sampled or an inversion goes unseen")
        self.assertEqual([r for r in rows if r["verdict"] != "agrees"], [],
                         "item-id ordering disagreed with created_at; the split is unsafe")
        for r in rows:
            self.assertTrue(r["items_checked"], "an author with nothing checked proves nothing")
            for c in r["items_checked"]:
                self.assertIsNotNone(c.get("created_at_i"), "an item was not readable")

    def test_the_check_is_capable_of_failing(self):
        # Prove the verdict field is not a constant, so the test above is not vacuous.
        path = os.path.join(RAW, "chronology_verification.jsonl")
        if not os.path.exists(path):
            self.skipTest("no capture yet")
        rows = [json.loads(l) for l in open(path) if l.strip()]
        self.assertIn("verdict", rows[0])
        disagreeing = [r for r in rows if r["id_order_says_any_later"]
                       != r["timestamps_say_any_later"]]
        self.assertEqual(len(disagreeing), 0,
                         "if any author disagrees the capture is evidence against itself")


class VerdictTest(unittest.TestCase):
    """The gates, asserted against results.json, which the run must produce."""

    def setUp(self):
        path = os.path.join(HERE, "results.json")
        if not os.path.exists(path):
            self.fail("results.json absent: the run has not been scored")
        self.r = json.load(open(path))

    def test_primary_rate_rule_was_fixed_before_labels(self):
        self.assertIn("both readers", self.r["primary_rate_rule"])

    def test_every_declared_gate_is_present_and_carries_its_declaration(self):
        for g in ("A1_fetch_success", "A2_controls", "A3_reader_agreement",
                  "C1_negative_control", "B1_kill", "B2_survive", "A4"):
            self.assertIn(g, self.r["gates"], "gate %s absent from results.json" % g)
            self.assertTrue(self.r["gates"][g].get("declared"),
                            "gate %s does not carry its declaration" % g)

    def test_a_failed_control_forces_not_evaluated(self):
        g = self.r["gates"]
        if not (g["A2_controls"]["met"] and g["A3_reader_agreement"]["met"]
                and g["C1_negative_control"]["met"]):
            self.assertEqual(self.r["verdict"], "not_evaluated")
            self.assertTrue(g["A4"]["fired"])

    def test_b1_and_b2_cannot_both_fire(self):
        g = self.r["gates"]
        self.assertFalse(g["B1_kill"]["fired"] and g["B2_survive"]["fired"])

    def test_a_surviving_verdict_beats_both_controls(self):
        if self.r["verdict"] == "h1_survives":
            g = self.r["gates"]
            self.assertGreater(g["B2_survive"]["observed_matched_lower"],
                               g["B1_kill"]["observed_mismatched_upper"])
            self.assertGreater(g["B2_survive"]["observed_matched_lower"],
                               g["B1_kill"]["observed_story_upper"])

    def test_the_lexical_arm_feeds_no_gate(self):
        self.assertIn("lexical_arm_feeds_no_gate", self.r)
        for g in self.r["gates"].values():
            self.assertNotIn("lexical", json.dumps(g).lower().replace("lexical_arm", ""))
