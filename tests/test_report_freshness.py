"""The generated session report must be current whenever the tree can be committed.

`doc lint` fails when a committed generated file differs from what its generator
produces, and the session report is generated from the event stream. So every
append to that stream invalidates the report, and any commit made before the next
regeneration publishes a stale one. That is not hypothetical: run 37180487906 had
all seven `Tests` jobs green and `Documentation lint` red on
`sessions/2026-10-04-012-.../README.md`, because a `tools/x` capture and an
artifact had been recorded after the last write and the tree was committed in
between.

T-0026 and T-0027 fixed the same class of defect for the *task* and *docs*
indexes by making the task commands rebuild them. Those repairs did not reach
this file, because the appender here is not a task command. The fix therefore
sits in the appenders — `sessionlog.log`, `sessionlog.artifact`,
`recorder.record_command` — and the tests below call the **module** API rather
than the CLI on purpose: a repair in the CLI would leave every module caller able
to break the invariant again, which is what the first attempt did.

Split out of `test_session.py` on 2026-10-04 when that file reached the 300-line
cap. One concern, one falsification, and a caller that already had a file.
"""

from __future__ import annotations

import unittest

from harness import RepoTest

from originlib import paths, recorder, report, session


class ReportCurrentAfterEveryAppendTest(RepoTest):
    """One property, five appenders: the report on disk equals the render now."""

    def assert_report_current(self, session_id: str) -> None:
        on_disk = paths.session_report(session_id).read_text(encoding="utf-8")
        self.assertEqual(on_disk, report.render_session_report(session_id))

    def test_a_capture_leaves_the_report_current(self) -> None:
        # The instance behind run 37180487906: a `tools/x` capture recorded after
        # the last regeneration, then a commit. Only `session start` and `finish`
        # rewrote the report, so any commit in between published a stale file.
        active = session.start("capture keeps the report current", agent="tester")
        self.assert_report_current(active.session)
        recorder.record_command(["true"], 0, 1, "ok", str(self.repo))
        self.assert_report_current(active.session)

    def test_a_redaction_leaves_the_report_current(self) -> None:
        # The second event `record_command` may append, on a different path
        # through the same function.
        active = session.start("redaction keeps the report current", agent="tester")
        recorder.record_command(["true"], 0, 1, "token ghp_" + "a" * 36, str(self.repo))
        self.assert_report_current(active.session)

    def test_an_artifact_leaves_the_report_current(self) -> None:
        active = session.start("artifact keeps the report current", agent="tester")
        path = self.write("declared.txt", "x\n")
        session.artifact(str(path))
        self.assert_report_current(active.session)

    def test_a_step_leaves_the_report_current(self) -> None:
        # One test for `sessionlog.log`, which is the single choke point the
        # other four wrappers go through.
        active = session.start("step keeps the report current", agent="tester")
        session.step("a milestone")
        self.assert_report_current(active.session)

    def test_the_report_is_stale_when_the_generator_is_not_run(self) -> None:
        # The control the four above need: appending without regenerating really
        # does leave the file different, or the assertions above are vacuous.
        active = session.start("control", agent="tester")
        session.step("before")
        path = paths.session_report(active.session)
        path.write_text(path.read_text(encoding="utf-8") + "\nstale\n", encoding="utf-8")
        self.assertNotEqual(
            path.read_text(encoding="utf-8"), report.render_session_report(active.session)
        )
        report.regenerate_session(active.session)
        self.assert_report_current(active.session)


if __name__ == "__main__":
    unittest.main()