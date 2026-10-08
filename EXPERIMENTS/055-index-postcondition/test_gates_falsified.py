#!/usr/bin/env python3
"""E055's controls, held falsifiable in both directions (D025, docs/policy/gate-falsification.md).

A gate that fires proves it can fail. Only a gate that stays silent on the case it
is *meant* to accept proves it can be satisfied, and that second direction is the
one that is easy to leave out. Each test here breaks one half of the instrument and
asserts the corresponding control notices:

    python3 test_gates_falsified.py
"""

import inspect
import json
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import arms                                                      # noqa: E402
import controls                                                  # noqa: E402
import indexcheck                                                # noqa: E402
from testharness import scratch                            # noqa: E402
# testharness first: it is what puts E038's oracle directory on sys.path.
from compare import CASES as E038_CASES                          # noqa: E402
from gitenv import STG, git_ok, sh                              # noqa: E402



class TestVersionRule(unittest.TestCase):
    """The rule must fire on the version that cannot run and pass the one that can."""

    def test_refuses_the_host_version(self):
        self.assertFalse(git_ok("2.25.1"),
                         "2.25.1 must be refused: git-hunk needs --no-relative")

    def test_accepts_a_newer_version(self):
        self.assertTrue(git_ok("2.56.0"))
        self.assertTrue(git_ok("3.0.1"))

    def test_unparseable_version_is_refused_not_assumed(self):
        for bad in ("none", "", "2", "unknown"):
            self.assertFalse(git_ok(bad), "%r must not read as satisfied" % bad)


class TestGraderIsArmBlind(unittest.TestCase):
    """The grader must be unable to know what an arm said."""

    def test_check_takes_a_repository_and_an_intent_only(self):
        params = list(inspect.signature(indexcheck.check).parameters)
        self.assertEqual(params, ["repo", "intent"])

    def test_grader_does_not_import_the_arms(self):
        with open(indexcheck.__file__) as fh:
            source = fh.read()
        self.assertNotIn("arms", source,
                         "indexcheck.py must not reach the arms; a grader that "
                         "knows an arm's vocabulary can be right about it by "
                         "construction (PROTOCOL.md)")

    def test_a_verdict_depends_only_on_bytes(self):
        """Same index, two intents: the verdict must follow the intent, not the run."""
        _, base, edited, want, want_content = E038_CASES[0]
        got = {}

        def exercise(root):
            d = controls.make_repo(base, edited, root, "blind")
            try:
                sh([sys.executable, STG, "stage", "f.txt:%d" % want], d)
                got["holds"] = controls.score(d, want_content)[2]
                got["wrong"] = controls.score(d, base)[2]
            finally:
                shutil.rmtree(d, ignore_errors=True)

        scratch(exercise)
        self.assertTrue(got["holds"], "the declared intent must hold once staged")
        self.assertFalse(got["wrong"],
                         "scoring the same index against a different intent must "
                         "fail, or the verdict is not a function of the bytes")


class TestRecoveryControlCanFail(unittest.TestCase):
    """C1 must notice a grader that rejects a state E038's oracle accepts."""

    def test_control_recovery_fires_on_the_real_checker(self):
        result = scratch(controls.control_recovery, E038_CASES)
        self.assertTrue(result["fired"])
        self.assertEqual(result["failed"], [])

    def test_control_recovery_fails_when_the_intent_is_wrong(self):
        """The same correct index, declared as the wrong intent: C1 must notice."""
        original = controls.score
        try:
            controls.score = lambda repo, want: original(repo, want + "\nNOT-IT\n")
            result = scratch(controls.control_recovery, E038_CASES)
            self.assertFalse(result["fired"],
                             "C1 accepted a grader that rejects a correct index")
            self.assertTrue(result["failed"])
        finally:
            controls.score = original


class TestSensitivityControlCanFail(unittest.TestCase):
    """C2 must notice a grader that accepts everything, which passes C1 as well."""

    def test_control_sensitivity_fires_on_the_real_checker(self):
        result = scratch(controls.control_sensitivity, E038_CASES)
        self.assertTrue(result["fired"])
        self.assertEqual(result["missed"], [])
        self.assertGreaterEqual(result["injected"], 20,
                                "C2 must exercise enough wrong states to mean "
                                "something; a control that runs on two rows is "
                                "F073's all-zero curve waiting to happen")

    def test_control_sensitivity_fails_when_the_grader_accepts_everything(self):
        original = controls.check
        try:
            controls.check = lambda repo, intent: (
                [{"path": p, "verdict": "holds", "kind": "text"} for p in intent], True)
            result = scratch(controls.control_sensitivity, E038_CASES)
            self.assertFalse(result["fired"],
                             "C2 accepted a grader that never rejects anything")
            self.assertEqual(result["flagged"], 0)
        finally:
            controls.check = original

    def test_injections_cover_the_four_named_shapes(self):
        name, base, edited, want, _ = E038_CASES[0]
        patches = controls.wrong_patches("@@ -1,1 +1,2 @@\n-x\n+y\n+z\n", want)
        self.assertEqual(sorted(patches),
                         ["all_changes", "doubled_run", "invented_line",
                          "nothing_staged"])
        self.assertEqual(patches["nothing_staged"], "",
                         "the nothing-staged shape is an empty patch by "
                         "construction, which is why it is skipped on apply")


class TestSelectorMappingCanDisagree(unittest.TestCase):
    """C4 must be able to say the two readers differ, or it asserts nothing."""

    def test_body_position_reports_a_changed_line(self):
        name, base, edited, want, _ = E038_CASES[4]   # append-at-eof

        def exercise(root):
            d = controls.make_repo(base, edited, root, "map")
            try:
                return arms.body_position(d, want)
            finally:
                shutil.rmtree(d, ignore_errors=True)

        pos, why = scratch(exercise)
        self.assertIsNotNone(pos, "no position found: %s" % why)

    def test_body_position_refuses_a_context_line(self):
        name, base, edited, _want, _ = E038_CASES[0]

        def exercise(root):
            d = controls.make_repo(base, edited, root, "ctx")
            try:
                # Line 7 of that case is unchanged in both texts.
                return arms.body_position(d, 7)
            finally:
                shutil.rmtree(d, ignore_errors=True)

        pos, why = scratch(exercise)
        self.assertIsNone(pos)
        self.assertIn("context", why)

    def test_mapping_control_reports_its_comparisons(self):
        result = scratch(controls.control_mapping, E038_CASES)
        self.assertIn("detail", result)
        self.assertTrue(result["detail"])
        for row in result["detail"]:
            if row.get("agree") is not None:
                self.assertIn("harness_position", row)
                self.assertIn("shown_position", row)


if __name__ == "__main__":
    unittest.main(verbosity=2)
