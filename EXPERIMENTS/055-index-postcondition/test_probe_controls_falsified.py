#!/usr/bin/env python3
"""E055's k3probe controls: can the `--as-numbered-lines` probe see what it must?

Split out of `test_gates_falsified.py` by invariant. C5, C6 and C7 bound the probe
that reads `--as-numbered-lines`; the tests for the second reader (`patchwalk`,
Amendment 3) are in `test_probe_readers_falsified.py` and the ordering tests in
`test_probe_order_falsified.py`.

C7 is the one that changed a verdict. The first probe read only
`--as-numbered-lines=after`, which cannot see a carried deletion: it reported a
strict superset on rows where the tool had in fact claimed exactly the wanted
line, which read as a failed K3. Each test here breaks one half of the probe and
asserts the corresponding control notices.

    python3 -m unittest discover -s . -t . -p 'test_*.py'
"""

import os
import shutil
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import controls                                                   # noqa: E402
import k3probe                                                    # noqa: E402
import probecontrols                                              # noqa: E402
from testharness import scratch                                   # noqa: E402
# testharness first: it is what puts E038's oracle directory on sys.path.
from compare import CASES as E038_CASES                           # noqa: E402
from gitenv import sh                                             # noqa: E402

class TestProbeControlsCanFail(unittest.TestCase):
    """C5, C6 and C7 must be able to say the probe is blind or the probe is wrong.

    K3's answer comes from a probe this experiment's author also wrote, so these
    controls are the only thing standing between a measurement and a reading. C7 is
    the one that changed the verdict: `after` reporting alone cannot see a carried
    deletion, so the first probe called a superset where the tool had claimed exactly
    the wanted line.
    """

    @staticmethod
    def _fake(before_side):
        """A `carried_lines` stub returning only one side, as the first probe did."""
        def stub(repo, want, env=None):
            return ({want: "x"} if before_side == "after" else {}, {}, None, "")
        return stub

    def test_c5_fires_on_the_real_probe(self):
        result = scratch(probecontrols.control_probe_sees_overstage, E038_CASES)
        self.assertTrue(result["fired"],
                        "the probe could not see a carried addition, so a negative "
                        "K3 would be blindness, not a measurement: %r" % result)

    def test_c5_fails_when_only_the_after_side_is_read(self):
        """The first probe's fault, pinned as a control so it cannot come back."""
        original = k3probe.carried_lines
        try:
            k3probe.carried_lines = self._fake("after")
            result = scratch(probecontrols.control_probe_sees_overstage, E038_CASES)
            self.assertFalse(result["fired"],
                             "C5 accepted a probe blind to a carried addition")
        finally:
            k3probe.carried_lines = original

    def test_c6_fires_on_the_real_probe(self):
        result = scratch(probecontrols.control_probe_reads_exact, E038_CASES)
        self.assertTrue(result["fired"],
                        "the probe misread a correct selection: %r" % result)

    def test_c6_fails_when_the_probe_reports_an_extra_line(self):
        original = k3probe.carried_lines
        try:
            k3probe.carried_lines = lambda repo, want, env=None: (
                {want: "x", want + 1: "y"}, {}, None, "")
            result = scratch(probecontrols.control_probe_reads_exact, E038_CASES)
            self.assertFalse(result["fired"],
                             "C6 accepted a probe that invents an extra line")
        finally:
            k3probe.carried_lines = original

    def test_c7_fires_on_the_real_probe(self):
        result = scratch(probecontrols.control_probe_sees_carried_deletion, E038_CASES)
        self.assertTrue(result["fired"],
                        "the probe could not see a carried deletion: %r" % result)

    def test_c7_fails_when_only_the_after_side_is_read(self):
        """`after` alone reports exactly the wanted line while a deletion is carried."""
        original = k3probe.carried_lines
        try:
            k3probe.carried_lines = self._fake("after")
            result = scratch(probecontrols.control_probe_sees_carried_deletion, E038_CASES)
            self.assertFalse(result["fired"],
                             "C7 accepted a probe that cannot see a carried deletion")
        finally:
            k3probe.carried_lines = original

    def test_the_carried_deletion_fixture_really_deletes(self):
        """C7 asserts a probe is not merely wrong, so the fixture must carry the fault."""
        base, edited, want = probecontrols.DELETION_ADJACENT
        # The declared intent, written out by hand from the case's own two texts:
        # the base with ONLY the wanted line's change applied. It is deliberately not
        # `edited`, which is the whole-file post-image and would make the assertion
        # below pass for the wrong reason.
        intent_lines = base.split("\n")
        intent_lines[want - 1] = edited.split("\n")[want - 1]
        want_content = "\n".join(intent_lines)
        base_lines = base.split("\n")

        def exercise(root):
            d = controls.make_repo(base, edited, root, "c7fix")
            try:
                sh(["bash", "-c",
                    "git diff -U0 | filterdiff --lines=%d | "
                    "git apply --cached --unidiff-zero" % want], d)
                return controls.index_bytes(d)
            finally:
                shutil.rmtree(d, ignore_errors=True)

        got = scratch(exercise)
        self.assertIsNotNone(got)
        self.assertNotEqual(got.decode(), want_content,
                            "the fixture no longer over-stages, so C7 would be "
                            "asserting a shape the tool no longer produces")
        self.assertNotIn(base_lines[1], got.decode().split("\n"),
                         "the carried deletion should have removed line 2")

    def test_probe_parses_only_the_numbered_lines(self):
        """`--as-numbered-lines` also prints diff headers; they must not be read."""
        text = ("diff --git a/f.txt b/f.txt\n--- a/f.txt\n+++ b/f.txt\n"
                "4\t:FOUR\n")
        self.assertEqual(k3probe._lines(text), {4: "FOUR"})

    def test_c8_fires_on_the_real_probe(self):
        """The probe's two reports together must name the whole selection.

        K3's negative answer is only worth anything if the tool's output is a
        complete description of what it staged, not merely a hint that something
        else moved.
        """
        result = scratch(probecontrols.control_probe_describes_the_selection, E038_CASES)
        self.assertEqual(result["disagreements"], [],
                         "the probe under-reports the selection: %r"
                         % result["disagreements"])
        self.assertTrue(result["fired"])
        self.assertEqual(result["agreed"], result["decidable"])

    def test_c8_can_disagree(self):
        """A probe that under-reports must be caught, so C8 has a failing direction."""
        original = k3probe.derive_verdict
        try:
            def under_report(repo, want, env=None):
                got = original(repo, want, env)
                return dict(got, wrote_lines=[], before_lines=[])
            k3probe.derive_verdict = under_report
            result = scratch(probecontrols.control_probe_describes_the_selection,
                             E038_CASES)
            self.assertFalse(result["fired"],
                             "C8 accepted a probe that reported nothing")
            self.assertTrue(result["disagreements"])
        finally:
            k3probe.derive_verdict = original

    def test_patch_footprint_reads_git_not_the_tool(self):
        """The comparison must be against git's own statement, not filterdiff's."""
        name, base, edited, want, _ = E038_CASES[0]

        def exercise(root):
            d = controls.make_repo(base, edited, root, "fp")
            try:
                empty = probecontrols._patch_footprint(d)
                sh(["bash", "-c",
                    "git diff -U0 | filterdiff --lines=%d | "
                    "git apply --cached --unidiff-zero" % want], d)
                return empty, probecontrols._patch_footprint(d)
            finally:
                shutil.rmtree(d, ignore_errors=True)

        before, after = scratch(exercise)
        self.assertEqual(before, (set(), set()),
                         "nothing is staged before the pipeline runs")
        old, new = after
        self.assertTrue(old or new, "the pipeline must stage something")


if __name__ == "__main__":
    unittest.main(verbosity=2)
