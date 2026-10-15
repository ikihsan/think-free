#!/usr/bin/env python3
"""E124 -- tests that falsify the instrument, not tests that agree with it.

Two jobs. The injected-defect suite (K3) asks whether the checks catch defects
they were not designed around, on a fixture that is sound until it is broken.
The rest asks whether the checks can be made to answer "OK" when they should
not, which is the failure that would matter if this tool were trusted.

Standard library only. Python 3.8.
"""

import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

from preflight import alternate_form_fp, concordance, control_arm, render, wilson  # noqa: E402


def sound_key(n=8):
    return [{"account_id": "A%03d" % i, "arm": "R", "answer": "x"} for i in range(1, n + 1)]


def sound_answers(n=8):
    return [{"account_id": "A%03d" % i, "answer": "x"} for i in range(1, n + 1)]


def sound_verifier(item):
    """Clears anything whose value is in `item["truth"]`, whatever its form."""
    return "grounded" if item["value"] in item.get("truth", "") else "ungrounded_value"


class SoundFixture(unittest.TestCase):
    """The baseline the injected defects are measured against."""

    def test_sound_fixture_is_silent_and_reports(self):
        checks = [
            concordance(sound_key(), sound_answers()),
            alternate_form_fp([{"arm": "a", "value": "1,000", "correct": True},
                               {"arm": "a", "value": "2,000", "correct": False}],
                              lambda i: "grounded" if i["correct"] else "ungrounded_value"),
            control_arm([{"id": "a"}, {"id": "b"}], lambda r: False),
        ]
        text, code = render(checks, rate="recall 1.0000")
        self.assertEqual(code, 0, text)
        self.assertIn("recall 1.0000", text)


class InjectedDefects(unittest.TestCase):
    """K3: four defects on the sound fixture, one per check."""

    def test_key_ids_are_the_wrong_type(self):
        key = [{"account_id": i} for i in range(1, 9)]
        result = concordance(key, sound_answers())
        self.assertEqual(result["verdict"], "SILENT_NO_MATCH")
        self.assertEqual(result["best_rate"], 0.0)

    def test_key_field_is_renamed_so_nothing_is_shared(self):
        key = [{"subject": r["account_id"]} for r in sound_key()]
        result = concordance(key, sound_answers())
        self.assertEqual(result["verdict"], "SILENT_NO_MATCH")
        self.assertIn("share no field name", result["reason"])

    def test_type_conflict_is_named_not_only_counted(self):
        key = [{"account_id": i} for i in range(1, 9)]
        result = concordance(key, sound_answers())
        conflicts = result["type_conflicts"]
        self.assertEqual(len(conflicts), 1)
        self.assertEqual(conflicts[0]["field"], "account_id")
        self.assertEqual(conflicts[0]["key_types"], ["int"])
        self.assertEqual(conflicts[0]["output_types"], ["str"])
        self.assertIn("int", result["reason"])

    def test_a_constant_field_cannot_pass_for_a_clean_join(self):
        rows = [{"account_id": "A001", "status": "ok"}] * 4
        result = concordance(rows, list(rows))
        self.assertEqual(result["verdict"], "NO_DISCRIMINATING_PAIRING")
        self.assertIn("status", result["degenerate_pairings"])

    def test_verifier_that_matches_only_the_exact_form(self):
        items = [{"arm": "a", "value": "1,000", "correct": True},
                 {"arm": "a", "value": "$1000", "correct": True},
                 {"arm": "a", "value": "9,999", "correct": False}]
        result = alternate_form_fp(items, lambda i: "grounded" if i["value"] in ("1,000", "9,999") else "ungrounded_value")
        self.assertEqual(result["verdict"], "ALTERNATE_FORM_FP")
        self.assertAlmostEqual(result["arms"]["a"]["correct_items"]["rate"], 0.5, places=4)

    def test_control_arm_holds_a_positive(self):
        rows = [{"id": "a", "evidence": "monthly on the 5th, identical amount 20.00, 12 months"},
                {"id": "b"}, {"id": "c"}, {"id": "d"}]
        result = control_arm(rows, lambda r: "monthly" in r.get("evidence", ""))
        self.assertEqual(result["verdict"], "CONTROL_NOT_EMPTY")
        self.assertEqual(result["positives"], 1)

    def test_every_injected_defect_withholds_the_rate(self):
        cases = [
            concordance([{"account_id": i} for i in range(1, 9)], sound_answers()),
            alternate_form_fp([{"arm": "a", "value": "1,000", "correct": True},
                               {"arm": "a", "value": "$1000", "correct": True},
                               {"arm": "a", "value": "9,999", "correct": False}],
                              lambda i: "grounded" if i["value"] in ("1,000", "9,999") else "ungrounded_value"),
            control_arm([{"id": "a", "evidence": "monthly identical amount, 24 months"}],
                        lambda r: "monthly" in r.get("evidence", "")),
        ]
        for check in cases:
            _text, code = render([check], rate="accuracy 0.97")
            self.assertEqual(code, 3, check["check"])


class Falsification(unittest.TestCase):
    """The ways this tool could be made to say OK while the instrument is broken."""

    def test_no_labelled_correct_items_reports_that_it_measured_nothing(self):
        result = alternate_form_fp([{"arm": "a", "value": "1", "correct": False}], sound_verifier)
        self.assertEqual(result["verdict"], "NO_LABELLED_CORRECT_ITEMS")
        _text, code = render([result], rate="fp 0.0")
        # E124 asserted exit 0 here, on the reasoning that a check which measured
        # nothing condemns nothing. E134 ran this check against a published
        # lm-eval run and got exactly that green light from a flagger that flagged
        # nothing, and a rate printed against it. "Measured nothing" now withholds;
        # see D110 and preflight/test_vacuous_passes.py.
        self.assertEqual(code, 3)

    def test_a_flagger_that_says_nothing_is_not_a_false_positive_rate(self):
        result = alternate_form_fp([{"arm": "a", "value": "1", "correct": True}], lambda i: None)
        self.assertEqual(result["verdict"], "NO_LABELLED_INCORRECT_ITEMS")
        self.assertEqual(result["arms"]["a"]["correct_items"]["flagged"], 0)

    def test_ungrounded_claim_counts_as_condemnation(self):
        result = alternate_form_fp([{"arm": "a", "value": "1", "correct": True}],
                                   lambda i: "ungrounded_claim")
        self.assertEqual(result["verdict"], "ALTERNATE_FORM_FP")

    def test_a_declared_premise_above_the_observed_rate_does_not_fire(self):
        rows = [{"id": "a", "e": "monthly"}, {"id": "b"}]
        result = control_arm(rows, lambda r: "monthly" in r.get("e", ""), premise=0.9)
        self.assertEqual(result["verdict"], "OK")

    def test_an_empty_control_arm_is_reported_as_empty(self):
        result = control_arm([], lambda r: True)
        self.assertEqual(result["verdict"], "NO_CONTROL_ROWS")

    def test_anyway_reports_the_number_but_says_so(self):
        text, code = render([concordance([{"id": 1}], [{"id": "1"}])], rate="acc 0.9", anyway=True)
        self.assertEqual(code, 0)
        self.assertIn("--anyway", text)

    def test_partial_overlap_is_not_reported_as_a_clean_join(self):
        rows = sound_answers(8)
        rows[0]["account_id"] = "Z999"
        result = concordance(sound_key(), rows)
        self.assertEqual(result["verdict"], "PARTIAL_MATCH")

    def test_wilson_brackets_the_estimate_and_handles_degenerate_cells(self):
        lo, hi = wilson(0, 0)
        self.assertEqual((lo, hi), (0.0, 0.0))
        # 10/10 still leaves a real lower bound: the interval never claims certainty.
        lo, hi = wilson(10, 10)
        self.assertLess(lo, 0.73)
        self.assertGreater(lo, 0.72)
        self.assertGreaterEqual(hi, 1.0)
        lo, hi = wilson(65, 330)
        self.assertLess(lo, 65 / 330.0)
        self.assertGreater(hi, 65 / 330.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)