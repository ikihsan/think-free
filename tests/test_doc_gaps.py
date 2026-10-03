"""Documentation-gap reconciliation: an event that implies a record that did not move.

Split out of `test_session.py` because the decision log is itself split, and
these tests are about which records a single event kind implicates.

The invariant under test: an implication is a *group*. The event demands that at
least one record in the group changed. Demanding every member would report a
gap on every correct session, because no event says which entry was written.
"""

from __future__ import annotations

import unittest

from harness import RepoTest

from originlib import session

META = ("<!-- origin-meta\nowner: docs/INDEX.md\nstatus: active\n"
        "last-verified: 2026-10-03\n-->\n")


class DecisionGapTest(RepoTest):
    def _record(self, relative: str, body: str) -> None:
        self.write(relative, f"# Log\n\n{META}\n{body}\n")

    def _decision_session(self, goal: str) -> object:
        active = session.start(goal, agent="tester")
        session.decision("chose approach X")
        return active

    def test_decision_without_any_record_change_is_reported(self) -> None:
        active = self._decision_session("decision without doc update")
        session.finish("worked", "ok", "none")
        gaps = [e for e in self.session_events(active.session)
                if e["kind"] == "integrity_error"]
        self.assertTrue(gaps)
        self.assertEqual(gaps[0]["data"]["action"], "documentation-gap")
        self.assertEqual(gaps[0]["data"]["path"], "DECISIONS.md")

    def test_updating_the_index_record_clears_the_gap(self) -> None:
        self._record("DECISIONS.md", "D004.")
        self._decision_session("decision with doc update")
        result = session.finish("worked", "ok", "none")
        self.assertEqual(result["documentation_gaps"], {})

    def test_updating_the_practice_record_clears_the_gap(self) -> None:
        self._record("DECISIONS-PRACTICE.md", "D020.")
        self._decision_session("decision into the practice record")
        result = session.finish("worked", "ok", "none")
        self.assertEqual(result["documentation_gaps"], {})

    def test_updating_the_foundation_record_clears_the_gap(self) -> None:
        self._record("DECISIONS-FOUNDATION.md", "D001.")
        self._decision_session("decision into the foundation record")
        result = session.finish("worked", "ok", "none")
        self.assertEqual(result["documentation_gaps"], {})

    def test_group_reports_one_path_not_three(self) -> None:
        active = self._decision_session("decision without any doc update")
        result = session.finish("worked", "ok", "none")
        self.assertEqual(list(result["documentation_gaps"]), ["DECISIONS.md"])
        reported = {e["data"]["path"] for e in self.session_events(active.session)
                    if e["kind"] == "integrity_error"}
        self.assertEqual(reported, {"DECISIONS.md"})


class ExperimentGapTest(RepoTest):
    """Both records are demanded, not either: a result may be a hypothesis or a failure."""

    def test_experiment_result_without_records_is_reported(self) -> None:
        active = session.start("result with no records", agent="tester")
        session.experiment_result("E002", "gate met")
        result = session.finish("worked", "ok", "none")
        self.assertEqual(sorted(result["documentation_gaps"]),
                         ["FAILURES.md", "HYPOTHESES.md"])

    def test_writing_only_the_failure_record_still_reports_the_gap(self) -> None:
        self.write("FAILURES.md", f"# Failures\n\n{META}\nF008.\n")
        session.start("result recorded as a failure only", agent="tester")
        session.experiment_result("E002", "gate met")
        result = session.finish("worked", "ok", "none")
        self.assertEqual(list(result["documentation_gaps"]), ["HYPOTHESES.md"])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()