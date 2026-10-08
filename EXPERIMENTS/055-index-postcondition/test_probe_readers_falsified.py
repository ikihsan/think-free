#!/usr/bin/env python3
"""E055's probe controls and readers, held falsifiable in both directions.

Split out of `test_gates_falsified.py` by invariant. The tests kept there bound
the **grader** and the **arms**; the tests here bound the two instruments that
read the *tool's own output* — the `--as-numbered-lines` probe (`k3probe`) and the
primary-output reader (`patchwalk`) — plus the controls `ceiling.py` computes from
the second one.

They are separated because they fail for different reasons and are fixed by
different evidence. A grader that accepts a wrong index is a defect in the
referee; a probe that cannot see a carried deletion is a defect in the
instrument, and the record already has the instance: Amendment 1's probe read only
`--as-numbered-lines=after`, could not see a carried deletion, and read K3 as
failed on rows where the tool had in fact claimed exactly the wanted line.

    python3 -m unittest discover -s . -t . -p 'test_*.py'
"""

import os
import shutil
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import ceiling                                                     # noqa: E402
import controls                                                   # noqa: E402
import patchwalk                                                  # noqa: E402
from testharness import scratch                                   # noqa: E402
# testharness first: it is what puts E038's oracle directory on sys.path.
from compare import CASES as E038_CASES                           # noqa: E402
from gitenv import sh                                             # noqa: E402


class TestPatchWalkIsFalsifiable(unittest.TestCase):
    """Amendment 3's reader must be able to be wrong, in both directions.

    The whole Amendment 3 rests on one claim about a text format: in a unified
    diff a `+`/`-` body line is a carried line and a space-prefixed line is
    context. If `walk` reported every line it saw, C11 would still agree with git
    on the over-staging rows and K3 would become unfalsifiable in the one
    direction that decides the gate — which is exactly what C12 exists to catch.
    These tests pin both directions on hand-written patches, with no tool and no
    repository involved, so a reader defect is distinguishable from a tool
    behaviour.
    """

    #: one replacement, one context line, one more replacement
    THREE = ("diff --git a/f.txt b/f.txt\n"
             "index 1111111..2222222 100644\n"
             "--- a/f.txt\n+++ b/f.txt\n"
             "@@ -1,5 +1,5 @@\n"
             " a\n"
             "-b\n"
             "+B\n"
             " c\n"
             "-d\n"
             "+D\n"
             " e\n")

    def test_marks_only_plus_and_minus(self):
        old, new = patchwalk.walk(self.THREE)
        self.assertEqual(old, {2, 4})
        self.assertEqual(new, {2, 4})

    def test_context_lines_are_not_carried(self):
        """The defect C12 exists to catch: a reader that returns the whole hunk."""
        _, new = patchwalk.walk(self.THREE)
        self.assertNotIn(1, new, "line 1 is context and must not be reported")
        self.assertNotIn(5, new, "line 5 is context and must not be reported")

    def test_counts_positions_across_context(self):
        """A context line advances both counters, so a later change is numbered right."""
        self.assertIn(4, patchwalk.walk(self.THREE)[0],
                      "the second change follows two context lines")

    def test_a_pure_deletion_carries_only_the_old_number(self):
        text = ("@@ -1,4 +1,3 @@\n"
                " a\n"
                "-b\n"
                " c\n"
                " d\n")
        old, new = patchwalk.walk(text)
        self.assertEqual(old, {2})
        self.assertEqual(new, set(),
                         "a deleted line has no new-file number; reporting one "
                         "would be the `after` blindness Amendment 1 recorded")

    def test_a_pure_addition_carries_only_the_new_number(self):
        text = ("@@ -1,2 +1,3 @@\n"
                " a\n"
                " b\n"
                "+B2\n")
        old, new = patchwalk.walk(text)
        self.assertEqual(old, set())
        self.assertEqual(new, {3})

    def test_a_second_hunk_restarts_from_its_own_header(self):
        """Two hunks in one selection: the second must not continue the first."""
        text = ("@@ -1,2 +1,2 @@\n"
                " a\n"
                "-b\n"
                "+B\n"
                "@@ -10,2 +10,2 @@\n"
                " j\n"
                "-k\n"
                "+K\n")
        old, new = patchwalk.walk(text)
        self.assertEqual(old, {2, 11})
        self.assertEqual(new, {2, 11})

    def test_no_newline_marker_is_not_a_context_line(self):
        """git writes `\\ No newline at end of file`; counting it shifts later lines."""
        text = ("@@ -1,2 +1,2 @@\n"
                " a\n"
                "-b\n"
                "\\ No newline at end of file\n"
                "+B\n"
                "\\ No newline at end of file\n")
        old, new = patchwalk.walk(text)
        self.assertEqual(old, {2})
        self.assertEqual(new, {2})

    def test_an_empty_selection_is_empty_not_everything(self):
        old, new = patchwalk.walk("diff --git a/f.txt b/f.txt\n")
        self.assertEqual((old, new), (set(), set()))

    def test_verdict_reads_an_exact_selection_as_exact(self):
        got = patchwalk.verdict(({4}, {4}, None, ""), 4)
        self.assertTrue(got["claims_only_the_wanted_line"])
        self.assertFalse(got["caller_can_derive_the_verdict"])

    def test_verdict_reads_a_carried_line_as_derivable(self):
        got = patchwalk.verdict(({1, 2}, {1, 2}, None, ""), 2)
        self.assertFalse(got["claims_only_the_wanted_line"])
        self.assertTrue(got["caller_can_derive_the_verdict"])
        self.assertEqual(got["named_lines_beyond_want"], [1])

    def test_a_failed_run_is_undecided_not_a_clean_negative(self):
        """The run-2 shape: an instrument that saw nothing must not read as a pass."""
        got = patchwalk.verdict((None, None, "filterdiff exited 127", ""), 2)
        self.assertIsNone(got["claims_only_the_wanted_line"])
        self.assertFalse(got["saw_any_line"])


class TestCeilingControlsCanFail(unittest.TestCase):
    """C11 and C12 must have a failing direction, or the ceiling is not evidence.

    The same discipline the grader's controls are held to, pointed at the second
    reader: `ceiling.py` records `K3_away_from_U0` from these two, so a check that
    could only pass would let a broken walk decide the gate.
    """

    def test_c11_compares_the_walk_against_git_not_against_the_probe(self):
        """Both footprints are read independently; neither is derived from the other."""
        name, base, edited, want, _ = E038_CASES[0]

        def exercise(root):
            d = controls.make_repo(base, edited, root, "c11")
            try:
                old, new, _why, _raw = patchwalk.carried(d, want, 0)
                sh(["bash", "-c", "git diff -U0 | filterdiff --lines=%d | "
                    "git apply --cached --unidiff-zero" % want], d)
                g_old, g_new = ceiling.git_footprint(d)
                return (old, new), (g_old, g_new)
            finally:
                shutil.rmtree(d, ignore_errors=True)

        (walked), git_said = scratch(exercise)
        self.assertEqual(walked, git_said,
                         "the walk must equal git's own statement of the index")

    def test_c11_can_disagree(self):
        """A walk that under-reports must be caught, so C11 has a failing direction."""
        rows = [{"walk_old_lines": [2], "walk_new_lines": [2],
                 "git_old_lines": [2, 3], "git_new_lines": [2], "walk_matches_git":
                 False, "case": "x", "diff_context": 0}]
        self.assertFalse(all(r["walk_matches_git"] for r in rows))

    def test_c12_reads_an_exact_selection_as_exactly_that_line(self):
        name, base, edited, want, _ = [
            c for c in E038_CASES if c[0] == "modify-one-of-three"][0]

        def exercise(root):
            d = controls.make_repo(base, edited, root, "c12")
            try:
                return patchwalk.derive_verdict(d, want, 0)
            finally:
                shutil.rmtree(d, ignore_errors=True)

        got = scratch(exercise)
        self.assertTrue(got["claims_only_the_wanted_line"],
                        "an exact selection must read as exact, or C12 is not met: %r"
                        % got)
        self.assertEqual(got["carried_new_lines"], [want])


if __name__ == "__main__":
    unittest.main(verbosity=2)
