"""Regression tests for the two vacuous passes E134 found by running the package
on a foreign harness's real output.

Both defects are the same shape and were found the same way: not by reading
`preflight`, but by pointing it at bytes it had never seen and reading the
verdict. Each defect is one line of input that a caller can produce by accident
-- an adapter that could not build a key, a control set with no wrong answers --
and each produced `OK`, which is in `report.CLEAN`, which means "this check
passed" and lets the rate be printed.

Falsified against the pre-fix code: 4 of 4 defect cases reported a
non-blocking `OK`; 0 of 4 do after the repair.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from preflight import alternate_form_fp, concordance, may_report  # noqa: E402


def _row(doc_id, task, target, **extra):
    row = {"doc_id": doc_id, "task": task, "target": target}
    row.update(extra)
    return row


class ConcordanceEmptyKey(unittest.TestCase):
    """E134: C1 returned OK with 0 key rows and 5 output rows."""

    def test_empty_key_with_output_rows_blocks(self):
        out_rows = [_row(i, "openbookqa", "1", acc=0.0) for i in range(5)]
        result = concordance([], out_rows)
        self.assertEqual(result["verdict"], "NO_KEY_ROWS")
        self.assertEqual(result["key_rows"], 0)
        self.assertEqual(result["output_rows"], 5)
        self.assertFalse(may_report([result]),
                         "a join against nothing is not a passing join")

    def test_empty_key_reason_names_the_consequence(self):
        out_rows = [_row(0, "openbookqa", "1", acc=0.0)]
        reason = concordance([], out_rows)["reason"]
        self.assertIn("0", reason)
        self.assertIn("nothing", reason)

    def test_no_rows_on_either_side_blocks(self):
        result = concordance([], [])
        self.assertEqual(result["verdict"], "NOTHING_TO_COMPARE")
        self.assertFalse(may_report([result]))

    def test_nonempty_both_sides_still_passes_when_the_join_works(self):
        rows = [_row(i, "piqa", "0", acc=0.0) for i in range(5)]
        result = concordance(rows, [dict(r) for r in rows])
        self.assertEqual(result["verdict"], "OK")
        self.assertTrue(may_report([result]))


class AlternateFormMissingArm(unittest.TestCase):
    """E134: C2 returned OK on 200 correct rows, 0 incorrect, a flagger that
    flagged nothing."""

    def _items(self, n_correct, n_incorrect):
        items = [{"arm": "a", "value": "right-%d" % i, "index": i, "correct": True}
                 for i in range(n_correct)]
        items += [{"arm": "a", "value": "wrong-%d" % i, "index": i, "correct": False}
                  for i in range(n_incorrect)]
        return items

    def test_empty_incorrect_arm_blocks_even_with_many_correct_rows(self):
        """E134's exact shape: a flagger that would catch a wrong item if one
        existed, 200 correct rows, and no wrong row to catch."""
        result = alternate_form_fp(
            self._items(200, 0),
            lambda item: "right" if item["correct"] else "flagged")
        self.assertEqual(result["verdict"], "NO_LABELLED_INCORRECT_ITEMS")
        self.assertEqual(result["arms"]["a"]["correct_items"]["flagged"], 0)
        self.assertEqual(result["arms"]["a"]["recall_on_incorrect"], None)
        self.assertFalse(may_report([result]))

    def test_a_flagger_that_flags_nothing_no_longer_passes(self):
        result = alternate_form_fp(self._items(200, 0), lambda item: "right")
        self.assertEqual(result["arms"]["a"]["correct_items"]["flagged"], 0)
        self.assertFalse(may_report([result]),
                         "a flagger with no output scored a perfect pass on E134")

    def test_empty_correct_arm_blocks_too(self):
        result = alternate_form_fp(self._items(0, 20), lambda item: "flagged")
        self.assertEqual(result["verdict"], "NO_LABELLED_CORRECT_ITEMS")
        self.assertFalse(may_report([result]),
                         "this verdict already said 'measured nothing' and did not block")

    def test_both_arms_present_still_passes_when_the_flagger_is_clean(self):
        result = alternate_form_fp(
            self._items(20, 20), lambda item: "right" if item["correct"] else "flagged")
        self.assertEqual(result["verdict"], "OK")
        self.assertEqual(result["arms"]["a"]["recall_on_incorrect"], 1.0)
        self.assertEqual(result["arms"]["a"]["miss_rate_on_incorrect"], 0.0)
        self.assertTrue(may_report([result]))

    def test_recall_is_recall_and_not_its_complement(self):
        """E134: the field named ``recall_on_incorrect`` computed ``1 - recall``.

        A flagger that condemns every wrong item reported ``recall 0.0`` and one
        that condemns none reported ``1.0``. Nothing in E124 or E134 quoted the
        field -- both read the *correct* arm -- so the number had not propagated;
        it was still wrong, and it was the package's own stated subject.
        """
        def catches(every_nth):
            def flagger(item):
                if item["correct"]:
                    return "right"
                return "flagged" if item["index"] % every_nth == 0 else "right"
            return flagger

        for every_nth, expected in ((1, 1.0), (2, 0.5), (4, 0.25), (20, 0.05)):
            result = alternate_form_fp(self._items(20, 20), catches(every_nth))
            self.assertEqual(result["arms"]["a"]["recall_on_incorrect"], round(expected, 4),
                             "every %dth wrong item" % every_nth)
            self.assertEqual(result["arms"]["a"]["miss_rate_on_incorrect"],
                             round(1.0 - expected, 4))


if __name__ == "__main__":
    unittest.main()
