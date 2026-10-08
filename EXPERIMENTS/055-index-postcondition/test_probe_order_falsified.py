#!/usr/bin/env python3
"""E055's probe ordering: the K3 probe must see the fixture before the arm runs.

Split out of `test_gates_falsified.py` by invariant. Run 2's first version probed
*after* the arm had staged, so `git diff` no longer showed the selected lines,
every probe came back empty, and K3 was decided by an instrument that had seen
nothing — which reads exactly like a clean negative. C5 did not catch it because
C5 probes a pristine repository, a different configuration from the one the run
uses.

These tests assert both halves of the ordering, so moving the probe back after the
arm fails here instead of quietly emptying the field. The related verdict tests
are in `test_verdict_falsified.py`.

    python3 -m unittest discover -s . -t . -p 'test_*.py'
"""

import os
import shutil
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import arms                                                      # noqa: E402
import controls                                                   # noqa: E402
import k3probe                                                    # noqa: E402
import probecontrols                                              # noqa: E402
import run                                                       # noqa: E402
from testharness import scratch                                   # noqa: E402
# testharness first: it is what puts E038's oracle directory on sys.path.
from compare import CASES as E038_CASES                           # noqa: E402
from gitenv import sh                                             # noqa: E402

class TestProbeOrderIsLoadBearing(unittest.TestCase):
    """The probe must see the pristine fixture, and the run must say so out loud.

    Run 2's first version probed after the arm had staged, so every probe read empty
    and K3 was decided by a blind instrument. C5 did not catch it, because C5 probes
    a pristine repository -- a different configuration from the one the run uses. The
    control below asserts both halves, so moving the probe back after the arm fails
    here instead of quietly emptying the field.
    """

    def test_pristine_probe_sees_the_selection_and_post_staging_does_not(self):
        name, base, edited, want, _ = [c for c in E038_CASES
                                       if c[0] == controls.OVER_STAGES[0]][0]

        def exercise(root):
            d = controls.make_repo(base, edited, root, "order")
            try:
                before = k3probe.derive_verdict(d, want)
                sh(["bash", "-c",
                    "git diff -U0 | filterdiff --lines=%d | "
                    "git apply --cached --unidiff-zero" % want], d)
                after = k3probe.derive_verdict(d, want)
                return before, after
            finally:
                shutil.rmtree(d, ignore_errors=True)

        before, after = scratch(exercise)
        self.assertTrue(before["saw_any_line"],
                        "the pristine probe must see the selection")
        self.assertTrue(before["named_lines_beyond_want"],
                        "the pristine probe must see the carried line 1")
        self.assertFalse(after["saw_any_line"],
                         "this is the failure the ordering exists to prevent: after "
                         "staging, `git diff` no longer shows the selected lines")

    def test_run_arms_probes_before_the_arm(self):
        """The recorded probe for a silent-wrong row must not be empty."""
        cases = [c for c in E038_CASES if c[0] == controls.OVER_STAGES[0]]

        def exercise(root):
            return run.run_arms(root, cases=cases, arms=[("filterdiff",
                                                          arms.arm_filterdiff)])

        rows = scratch(exercise)
        silent = [r for r in rows if r.get("silent")]
        self.assertTrue(silent, "expected the over-staging fixture to be silent-wrong")
        for row in silent:
            self.assertTrue(row["k3"]["saw_any_line"],
                            "a silent-wrong row with an empty probe means the probe "
                            "ran after the arm: %r" % row["k3"])

    def test_a_deletion_bearing_fixture_is_not_in_the_e038_family(self):
        """Why C7 needs its own fixture: no E038 case has the shape it needs.

        If an E038 case ever did, C7 could use it and the two controls would not be
        testing different things.
        """
        base, edited, want = probecontrols.DELETION_ADJACENT
        for name, cbase, cedited, cwant, _ in E038_CASES:
            if cwant != want:
                continue
            removed = len(cbase.split("\n")) - len(cedited.split("\n"))
            if removed > 0:
                self.assertNotEqual(
                    (cbase, cedited), (base, edited),
                    "%s now matches C7's fixture; use it in C7 instead" % name)

    def test_an_empty_probe_makes_the_verdict_undecided_not_clean(self):
        """A blind probe must not be readable as a failed K3."""
        blind = {"wrote_lines": [], "removed_old_lines": [],
                 "named_lines_beyond_want": [],
                 "claims_only_the_wanted_line": None, "saw_any_line": False}
        rows = [{"arm": "filterdiff", "case": "adjacent", "diff_context": 3,
                 "counted": True, "exit": 0, "index_holds_intent": False,
                 "silent": True, "index_sha256": "sha-one", "out": "",
                 "k3": blind}]
        verdict = run.kill_c(rows, [{"name": "c", "fired": True}])
        self.assertEqual(verdict["verdict"], "undecided")
        self.assertEqual(len(verdict["k3_rows_undecided"]), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
