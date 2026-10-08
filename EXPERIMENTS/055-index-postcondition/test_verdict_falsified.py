#!/usr/bin/env python3
"""E055's verdict: KILL-C computed from rows, arms degrading, provenance binding.

Split out of `test_gates_falsified.py` by invariant. This module holds the tests
for the three things that turn rows into an answer — `kill_c`, `summarise`, and the
provenance stamp — rather than for the instruments that produce the rows.

The distinction matters because the failure modes are opposite. A control that
cannot fire makes a number meaningless (F010: an arm that never started reads as
an arm that passed). A gate that can only fire is the same defect seen from the
other side, and it is the reason every row in `TestKillCIsAFunctionOfTheRows` is a
synthetic row set chosen to flip the verdict for a stated reason.

    python3 -m unittest discover -s . -t . -p 'test_*.py'
"""

import json
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import arms                                                      # noqa: E402
import provenance                                                # noqa: E402
import run                                                       # noqa: E402

class TestKillCIsAFunctionOfTheRows(unittest.TestCase):
    """KILL-C must be able to return `do_not_build`, not only `build`.

    A gate that can only fire is the shape F010 records. Each row below is a
    synthetic row set, and each one must flip the verdict for the stated reason.
    """

    @staticmethod
    def _row(arm, exit_code, holds, silent=None, probe=None, case="c", ctx=3,
             sha=None):
        row = {"arm": arm, "case": case, "diff_context": ctx, "counted": True,
               "exit": exit_code, "index_holds_intent": holds,
               "silent": (not holds and exit_code == 0) if silent is None else silent,
               "index_sha256": sha or ("sha-" + case), "out": ""}
        if probe is not None:
            row["k3"] = probe
        return row

    @staticmethod
    def _claims_exactly():
        """A probe that saw lines, and the tool claimed only the wanted one."""
        return {"wrote_lines": [4], "removed_old_lines": [],
                "named_lines_beyond_want": [],
                "claims_only_the_wanted_line": True,
                "caller_can_derive_the_verdict": False, "saw_any_line": True}

    @staticmethod
    def _reports_superset():
        """A probe that saw lines, and the tool named another one as well."""
        return {"wrote_lines": [1, 2], "removed_old_lines": [],
                "named_lines_beyond_want": [1],
                "claims_only_the_wanted_line": False,
                "caller_can_derive_the_verdict": True, "saw_any_line": True}

    @staticmethod
    def _controls(fired):
        return [{"name": "c", "fired": fired}]

    def test_builds_when_all_three_hold(self):
        rows = [self._row("filterdiff", 0, False, probe=self._claims_exactly())]
        self.assertEqual(run.kill_c(rows, self._controls(True))["verdict"], "build")

    def test_no_build_when_k3_does_not_hold(self):
        """A strict superset is derivable by the caller, so K3 fails: do not build."""
        rows = [self._row("filterdiff", 0, False, probe=self._reports_superset())]
        verdict = run.kill_c(rows, self._controls(True))
        self.assertTrue(verdict["K2_a_shipped_arm_exited_0_on_a_wrong_index"])
        self.assertFalse(verdict["K3_a_shipped_arm_claimed_exactly_what_it_did_not_stage"])
        self.assertEqual(verdict["verdict"], "do_not_build")

    def test_no_build_when_a_control_did_not_fire(self):
        rows = [self._row("filterdiff", 0, False, probe=self._claims_exactly())]
        self.assertEqual(run.kill_c(rows, self._controls(False))["verdict"],
                         "do_not_build")

    def test_no_build_when_only_a_non_shipped_arm_was_wrong(self):
        rows = [self._row("pty_driver", 0, False, probe=self._claims_exactly())]
        verdict = run.kill_c(rows, self._controls(True))
        self.assertFalse(verdict["K2_a_shipped_arm_exited_0_on_a_wrong_index"],
                         "a harness that is not an incumbent must not carry a gate "
                         "about an incumbent (run.py SHIPPED)")

    def test_a_refusal_never_counts_as_silent(self):
        rows = [self._row("filterdiff", 128, False)]
        self.assertEqual(run.summarise(rows)["filterdiff"]["silent_wrong"], 0)
        self.assertEqual(run.summarise(rows)["filterdiff"]["refused_nonzero"], 1)

    def test_k3_counts_index_bytes_not_case_names(self):
        """Two case names, one wrong index state: the state count must be 1.

        F052's shape. E038 carries cases with identical base and identical intent, so a
        count taken over case names would read one observation as six. Both directions
        are asserted, because a counter keyed on the wrong field passes either test
        alone.
        """
        probe = self._reports_superset()
        same_state = [self._row("filterdiff", 0, False, probe=probe, case="one",
                                sha="sha-same"),
                      self._row("filterdiff", 0, False, probe=probe, case="two",
                                sha="sha-same")]
        self.assertEqual(run.kill_c(same_state, self._controls(True))
                         ["silent_wrong_distinct_index_states"], 1)

        one_name_two_states = [self._row("filterdiff", 0, False, probe=probe,
                                         case="same", sha="sha-a"),
                               self._row("filterdiff", 0, False, probe=probe,
                                         case="same", sha="sha-b")]
        self.assertEqual(run.kill_c(one_name_two_states, self._controls(True))
                         ["silent_wrong_distinct_index_states"], 2,
                         "two digests are two states even under one case name")


class TestArmsDegradeQuietlyNeverCleanly(unittest.TestCase):
    """F010's shape: an arm that cannot run must not look like an arm that passed."""

    def test_missing_tool_is_not_evaluated_not_pass(self):
        original = arms.FILTERDIFF
        try:
            arms.FILTERDIFF = "definitely-not-installed-xyz"
            row = arms.arm_filterdiff("/", 1, {})
            self.assertIn("not_evaluated", row)
            self.assertNotIn("exit", row)
        finally:
            arms.FILTERDIFF = original

    def test_gah_is_declared_unmeasured(self):
        row = arms.arm_gah("/", 1, {})
        self.assertIn("not_evaluated", row)
        self.assertIn("no release binary", row["not_evaluated"])

    def test_results_json_is_parseable_and_carries_the_verdict(self):
        """`doc lint` reads this file; a results.json that cannot parse is a violation."""
        path = os.path.join(HERE, "raw", "results.json")
        if not os.path.exists(path):
            self.skipTest("no results.json yet; run run.py first")
        with open(path) as fh:
            doc = json.load(fh)
        self.assertIn("KILL_C", doc)
        self.assertIn(doc["KILL_C"]["verdict"], ("build", "do_not_build"))
        self.assertIn("controls", doc)
        self.assertTrue(all("fired" in c for c in doc["controls"]))


class TestProvenanceCanSeeADriftedScript(unittest.TestCase):
    """The check must fire on edited bytes *and* pass on unedited ones.

    Two directions, because a check that always reports a difference is as useless as
    one that never does. `ceiling.py` was edited ten seconds after writing
    `raw/ceiling.json`; if this test only ever asserted "reports a difference", a
    check that returned True unconditionally would pass it.
    """

    def _artifact(self, recorded):
        d = tempfile.mkdtemp(prefix="e055-prov-")
        self.addCleanup(shutil.rmtree, d, True)
        path = os.path.join(d, "artifact.json")
        with open(path, "w") as fh:
            json.dump({"provenance": {"scripts": recorded}}, fh)
        return path

    def test_it_passes_when_the_bytes_agree(self):
        path = self._artifact(provenance.stamp())
        ok, diff, note = provenance.check(path)
        self.assertTrue(ok, "unmodified scripts must pass: %s" % note)
        self.assertEqual(diff, [])

    def test_it_fires_when_a_script_changes(self):
        recorded = dict(provenance.stamp())
        name = sorted(recorded)[0]
        recorded[name] = "0" * 64
        ok, diff, note = provenance.check(self._artifact(recorded))
        self.assertFalse(ok)
        self.assertEqual(diff, [name])
        self.assertIn("differ", note)

    def test_an_artifact_with_no_provenance_block_is_reported_not_assumed(self):
        """The artifact written before this check existed is not a pass."""
        d = tempfile.mkdtemp(prefix="e055-prov-")
        self.addCleanup(shutil.rmtree, d, True)
        path = os.path.join(d, "old.json")
        with open(path, "w") as fh:
            json.dump({"rows": []}, fh)
        ok, _diff, note = provenance.check(path)
        self.assertFalse(ok)
        self.assertIn("predates", note)

    def test_tests_are_excluded_so_editing_one_does_not_look_like_a_new_measurement(self):
        self.assertNotIn("test_gates_falsified.py", provenance.scripts())
        self.assertIn("run.py", provenance.scripts())
        self.assertIn("provenance.py", provenance.scripts())

    def test_the_shipped_artifact_is_bound_to_the_current_bytes(self):
        """The real check, on the real file. Skipped, never failed, when absent."""
        path = os.path.join(HERE, "raw", "results.json")
        if not os.path.exists(path):
            self.skipTest("no results.json yet; run run.py first")
        ok, diff, note = provenance.check(path)
        self.assertTrue(ok, "raw/results.json is not bound to these bytes: %s %s"
                        % (note, diff))


if __name__ == "__main__":
    unittest.main(verbosity=2)
