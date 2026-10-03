"""Session lifecycle, git reconciliation, and command capture."""

# origin-allow-secret-patterns: github-token
from __future__ import annotations

import unittest

from harness import RepoTest, git

from originlib import paths, recorder, session


class LifecycleTest(RepoTest):
    def test_start_writes_a_pointer_and_an_event(self) -> None:
        active = session.start("first goal", agent="tester")
        self.assertTrue((self.repo / "sessions" / "active.json").exists())
        self.assertEqual(self.kinds(active.session)[0], "session_start")
        self.assertRegex(active.session, r"^\d{4}-\d{2}-\d{2}-001-")

    def test_second_start_is_refused(self) -> None:
        session.start("first goal", agent="tester")
        with self.assertRaises(session.SessionError):
            session.start("second goal", agent="tester")

    def test_require_active_without_a_session_raises(self) -> None:
        with self.assertRaises(session.SessionError):
            session.require_active()

    def test_empty_goal_is_refused(self) -> None:
        with self.assertRaises(session.SessionError):
            session.start("   ")

    def test_session_ids_increment_within_a_day(self) -> None:
        first = session.start("alpha goal", agent="tester")
        session.finish("worked", "done", "next")
        second = session.start("beta goal", agent="tester")
        self.assertNotEqual(first.session, second.session)
        self.assertTrue(first.session.endswith("-alpha-goal"), first.session)
        self.assertTrue(second.session.endswith("-beta-goal"), second.session)

    def test_finish_clears_the_pointer_and_closes_the_stream(self) -> None:
        active = session.start("closing goal", agent="tester")
        result = session.finish("partial", "half done", "carry on")
        self.assertFalse((self.repo / "sessions" / "active.json").exists())
        self.assertEqual(self.kinds(active.session)[-1], "session_end")
        self.assertEqual(result["outcome"], "partial")

    def test_finish_rejects_an_unknown_outcome(self) -> None:
        session.start("bad outcome", agent="tester")
        with self.assertRaises(session.SessionError):
            session.finish("brilliant", "x", "y")

    def test_status_reports_the_active_session(self) -> None:
        session.start("status goal", agent="tester")
        state = session.status()
        self.assertTrue(state["active"])
        self.assertEqual(state["agent"], "tester")
        self.assertEqual(state["events"], 1)

    def test_status_is_quiet_without_a_session(self) -> None:
        self.assertEqual(session.status(), {"active": False})


class ReconciliationTest(RepoTest):
    def test_declared_artifact_is_not_reported(self) -> None:
        active = session.start("declared work", agent="tester")
        path = self.write("declared.txt", "content\n")
        session.artifact(str(path))
        result = session.finish("worked", "ok", "none")
        self.assertEqual(result["unlogged"], [])

    def test_undeclared_change_is_detected(self) -> None:
        session.start("undeclared work", agent="tester")
        self.write("surprise.txt", "not declared\n")
        result = session.finish("worked", "ok", "none")
        self.assertEqual(result["unlogged"], ["surprise.txt"])

    def test_undeclared_change_emits_an_event(self) -> None:
        active = session.start("undeclared work", agent="tester")
        self.write("surprise.txt", "not declared\n")
        session.finish("worked", "ok", "none")
        unlogged = [e for e in self.session_events(active.session) if e["kind"] == "unlogged_change"]
        self.assertEqual(len(unlogged), 1)
        self.assertEqual(unlogged[0]["data"]["path"], "surprise.txt")

    def test_deleted_artifact_is_reported(self) -> None:
        active = session.start("deleted artifact", agent="tester")
        path = self.write("temporary.txt", "here\n")
        session.artifact(str(path))
        path.unlink()
        result = session.finish("worked", "ok", "none")
        self.assertEqual(result["missing"], ["temporary.txt"])
        self.assertIn("integrity_error", self.kinds(active.session))

    def test_session_bookkeeping_is_not_flagged(self) -> None:
        session.start("bookkeeping", agent="tester")
        result = session.finish("worked", "ok", "none")
        self.assertEqual(result["unlogged"], [])

    def test_decision_implies_decisions_md(self) -> None:
        active = session.start("decision without doc update", agent="tester")
        session.decision("chose approach X")
        session.finish("worked", "ok", "none")
        gaps = [e for e in self.session_events(active.session) if e["kind"] == "integrity_error"]
        self.assertTrue(gaps)
        self.assertEqual(gaps[0]["data"]["action"], "documentation-gap")
        self.assertEqual(gaps[0]["data"]["path"], "DECISIONS.md")

    def test_updating_decisions_md_clears_the_gap(self) -> None:
        self.write("DECISIONS.md", "# Decisions\n\n<!-- origin-meta\nowner: docs/INDEX.md\n"
                                  "status: active\nlast-verified: 2026-10-03\n-->\n\nD004.\n")
        session.start("decision with doc update", agent="tester")
        session.decision("chose approach X")
        result = session.finish("worked", "ok", "none")
        self.assertEqual(result["documentation_gaps"], {})

    def test_doc_update_events_record_changed_mission_records(self) -> None:
        active = session.start("state update", agent="tester")
        self.write("STATE.md", "# State\n\n<!-- origin-meta\nowner: docs/INDEX.md\n"
                               "status: active\nlast-verified: 2026-10-03\n-->\n\nchanged\n")
        session.finish("worked", "ok", "none")
        updates = [e for e in self.session_events(active.session) if e["kind"] == "doc_update"]
        self.assertEqual([e["data"]["path"] for e in updates], ["STATE.md"])


class CommandCaptureTest(RepoTest):
    def test_command_is_logged_with_line_range_and_exit_code(self) -> None:
        active = session.start("capture commands", agent="tester")
        result = recorder.record_command(["echo", "hi"], 0, 7, "hi\n", str(self.repo))
        self.assertTrue(result["recorded"])
        log = (self.repo / "sessions" / active.session / "commands.log").read_text(encoding="utf-8")
        self.assertIn("exit: 0", log)
        self.assertIn("duration_ms: 7", log)
        payload = [e for e in self.session_events(active.session) if e["kind"] == "command"][0]
        self.assertEqual(payload["data"]["exit_code"], 0)
        self.assertEqual(payload["data"]["log_line_start"], 1)
        slice_lines = recorder.read_slice(
            self.repo / "sessions" / active.session / "commands.log",
            payload["data"]["log_line_start"],
            payload["data"]["log_line_end"],
        )
        self.assertTrue(any("hi" in line for line in slice_lines))

    def test_non_zero_exit_is_preserved(self) -> None:
        session.start("failing command", agent="tester")
        recorder.record_command(["false"], 1, 3, "", str(self.repo))
        events = [e for e in self.session_events(session.load_active().session) if e["kind"] == "command"]
        self.assertEqual(events[0]["data"]["exit_code"], 1)

    def test_secret_in_output_is_redacted_before_disk(self) -> None:
        active = session.start("secret output", agent="tester")
        recorder.record_command(
            ["deploy"], 0, 1, "using ghp_abcdefghijklmnopqrstuvwxyz012345 now\n", str(self.repo)
        )
        log = (self.repo / "sessions" / active.session / "commands.log").read_text(encoding="utf-8")
        self.assertNotIn("ghp_abcdefghijklmnopqrstuvwxyz012345", log)
        self.assertIn("REDACTED:github-token", log)
        self.assertIn("redaction", self.kinds(active.session))

    def test_without_a_session_nothing_is_recorded(self) -> None:
        result = recorder.record_command(["echo"], 0, 1, "out", str(self.repo))
        self.assertFalse(result["recorded"])


class GeneratedReportTest(RepoTest):
    def test_report_is_generated_and_within_the_line_cap(self) -> None:
        from originlib import report

        active = session.start("report generation", agent="tester")
        path = self.write("produced.txt", "x\n")
        session.artifact(str(path))
        session.step("halfway")
        session.finish("worked", "generated", "review it")
        report.regenerate_session(active.session)
        report.regenerate_sessions_index()
        text = (self.repo / "sessions" / active.session / "README.md").read_text(encoding="utf-8")
        self.assertIn("# Session " + active.session, text)
        self.assertIn("generated-by: origin", text)
        self.assertIn("produced.txt", text)
        self.assertLessEqual(len(text.splitlines()), 300)

    def test_report_regeneration_is_idempotent(self) -> None:
        from originlib import report

        active = session.start("idempotent report", agent="tester")
        session.finish("worked", "done", "none")
        report.regenerate_session(active.session)
        first = paths.session_report(active.session).read_text(encoding="utf-8")
        report.write_if_changed(paths.session_report(active.session), report.render_session_report(active.session))
        second = paths.session_report(active.session).read_text(encoding="utf-8")
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()

class ArtifactBatchTest(RepoTest):
    """Declaration ergonomics, added after session 002 under-declared 55 files."""

    def test_multiple_paths_are_declared_individually(self) -> None:
        session.start("batch declaration", agent="tester")
        self.write("one.txt", "one\n")
        self.write("two.txt", "two\n")
        code = self.cli("session", "artifact", "one.txt", "two.txt")
        self.assertEqual(code, 0)
        paths = [
            event["data"]["path"]
            for event in self.session_events(session.load_active().session)
            if event["kind"] == "artifact"
        ]
        self.assertEqual(paths, ["one.txt", "two.txt"])

    def test_directory_expands_to_files(self) -> None:
        session.start("directory declaration", agent="tester")
        self.write("docs/policy/alpha.md", "a\n")
        self.write("docs/policy/beta.md", "b\n")
        self.write("docs/policy/nested/gamma.md", "c\n")
        self.assertEqual(self.cli("session", "artifact", "--dir", "docs/policy"), 0)
        paths = sorted(
            event["data"]["path"]
            for event in self.session_events(session.load_active().session)
            if event["kind"] == "artifact"
        )
        # docs/policy/doc-standards.md already exists in the fixture.
        self.assertEqual(paths, ["docs/policy/alpha.md", "docs/policy/beta.md",
                                 "docs/policy/doc-standards.md",
                                 "docs/policy/nested/gamma.md"])

    def test_no_arguments_is_a_usage_error(self) -> None:
        session.start("empty declaration", agent="tester")
        self.assertEqual(self.cli("session", "artifact"), 1)

    def test_missing_directory_is_a_usage_error(self) -> None:
        session.start("bad directory", agent="tester")
        self.assertEqual(self.cli("session", "artifact", "--dir", "nope"), 1)

    def test_duplicate_paths_are_declared_once(self) -> None:
        session.start("duplicate declaration", agent="tester")
        self.write("dup.txt", "x\n")
        self.cli("session", "artifact", "dup.txt", "dup.txt")
        artifacts = [
            event
            for event in self.session_events(session.load_active().session)
            if event["kind"] == "artifact"
        ]
        self.assertEqual(len(artifacts), 1)


class IgnoredArtifactTest(RepoTest):
    """Gitignored files are never declared: build output is not evidence."""

    IGNORED = ("__pycache__/", "*.py[cod]\n")

    def test_ignored_file_is_refused(self) -> None:
        from originlib import session

        (self.repo / ".gitignore").write_text("*.log\n", encoding="utf-8")
        session.start("refuse ignored", agent="tester")
        path = self.write("build.log", "compiled output\n")
        with self.assertRaises(session.SessionError) as caught:
            session.artifact(str(path))
        self.assertIn("gitignore", str(caught.exception))

    def test_directory_sweep_skips_ignored_files(self) -> None:
        (self.repo / ".gitignore").write_text("*.log\n", encoding="utf-8")
        session.start("sweep skips ignored", agent="tester")
        self.write("src/real.txt", "real\n")
        self.write("src/noise.log", "noise\n")
        self.cli("session", "artifact", "--dir", "src")
        artifacts = [
            event["data"]["path"]
            for event in self.session_events(session.load_active().session)
            if event["kind"] == "artifact"
        ]
        self.assertEqual(artifacts, ["src/real.txt"])
        self.assertIn("skipped (gitignored)  src/noise.log", self.output())

    def test_explicit_ignored_path_is_skipped_not_fatal(self) -> None:
        (self.repo / ".gitignore").write_text("*.log\n", encoding="utf-8")
        session.start("explicit ignored", agent="tester")
        self.write("thing.log", "noise\n")
        code = self.cli("session", "artifact", "thing.log")
        self.assertEqual(code, 0)
        artifacts = [
            event
            for event in self.session_events(session.load_active().session)
            if event["kind"] == "artifact"
        ]
        self.assertEqual(artifacts, [])
