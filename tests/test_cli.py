"""CLI surface: exit codes, dispatch, and the parts a VM script depends on."""

from __future__ import annotations

import os
import unittest

from harness import RepoTest

from originlib import cli, docindex, report, tasks


class ExitCodeTest(RepoTest):
    def test_documented_exit_codes(self) -> None:
        self.assertEqual(
            (cli.EXIT_OK, cli.EXIT_USAGE, cli.EXIT_LINT, cli.EXIT_VERIFY, cli.EXIT_INTEGRITY),
            (0, 1, 2, 3, 4),
        )

    def test_session_start_returns_zero(self) -> None:
        self.assertEqual(self.cli("session", "start", "--goal", "exit code check"), 0)

    def test_missing_active_session_is_a_usage_error(self) -> None:
        self.assertEqual(self.cli("session", "step", "nothing active"), 1)

    def test_unknown_task_is_a_usage_error(self) -> None:
        self.assertEqual(self.cli("task", "claim", "T-9999", "--agent", "x"), 1)

    def test_lint_fails_with_two(self) -> None:
        (self.repo / "docs" / "policy" / "toobig.md").write_text(
            "# Too big\n\n<!-- origin-meta\nowner: docs/INDEX.md\nstatus: active\n"
            "last-verified: 2026-10-03\n-->\n\n" + "x\n" * 400,
            encoding="utf-8",
        )
        self.assertEqual(self.cli("doc", "lint"), 2)

    def test_lint_quiet_prints_nothing_when_clean(self) -> None:
        self.write_generated()
        code = self.cli("doc", "lint", "--quiet")
        self.assertEqual(code, 0)
        self.assertEqual(self.output(), "")

    def test_task_verification_failure_returns_three(self) -> None:
        tasks.create("will fail", "exit 9")
        self.assertEqual(self.cli("task", "verify", "T-0001"), 3)

    def test_session_verify_returns_four_on_integrity_problem(self) -> None:
        self.cli("session", "start", "--goal", "left unfinished")
        self.assertEqual(self.cli("session", "verify"), 4)

    def test_session_verify_returns_zero_after_finish(self) -> None:
        self.cli("session", "start", "--goal", "finished cleanly")
        self.cli("session", "finish", "--outcome", "no-change", "--summary", "nothing", "--next", "none")
        self.cli("doc", "index")
        self.assertEqual(self.cli("session", "verify"), 0)

    def test_bad_outcome_is_rejected_by_the_parser(self) -> None:
        with self.assertRaises(SystemExit):
            self.cli("session", "finish", "--outcome", "brilliant", "--summary", "x", "--next", "y")


class IndexCommandTest(RepoTest):
    def test_index_command_writes_all_three(self) -> None:
        self.assertEqual(self.cli("doc", "index"), 0)
        for name in ("docs/INDEX.md", "sessions/INDEX.md", "tasks/INDEX.md"):
            self.assertTrue((self.repo / name).exists(), name)

    def test_index_check_detects_staleness(self) -> None:
        self.write_generated()
        self.assertEqual(self.cli("doc", "index", "--check"), 0)
        index = self.repo / "tasks" / "INDEX.md"
        index.write_text(index.read_text(encoding="utf-8") + "\nmanual edit\n", encoding="utf-8")
        self.assertEqual(self.cli("doc", "index", "--check"), 2)

    def test_index_check_does_not_modify_files(self) -> None:
        self.write_generated()
        before = {
            name: (self.repo / name).read_text(encoding="utf-8")
            for name in ("docs/INDEX.md", "sessions/INDEX.md", "tasks/INDEX.md")
        }
        self.cli("doc", "index", "--check")
        for name, content in before.items():
            self.assertEqual((self.repo / name).read_text(encoding="utf-8"), content, name)

    def test_index_command_is_idempotent(self) -> None:
        self.cli("doc", "index")
        before = (self.repo / "docs" / "INDEX.md").read_text(encoding="utf-8")
        self.cli("doc", "index")
        after = (self.repo / "docs" / "INDEX.md").read_text(encoding="utf-8")
        self.assertEqual(before, after)


class DoctorTest(RepoTest):
    def test_offline_doctor_reports_the_environment(self) -> None:
        self.assertEqual(self.cli("doctor", "--offline"), 0)
        self.assertIn("platform", self.output())
        self.assertIn("cpus", self.output())

    def test_doctor_writes_raw_json(self) -> None:
        self.cli("doctor", "--offline")
        import json

        raw = json.loads((self.repo / ".origin" / "doctor.json").read_text(encoding="utf-8"))
        self.assertEqual(raw["schema"], "origin.doctor/1")
        self.assertIn("credentials_present", raw)

    def test_doctor_never_records_credential_values(self) -> None:
        os.environ["SOME_FAKE_TOKEN"] = "super-secret-value-not-for-disk"
        self.addCleanup(lambda: os.environ.pop("SOME_FAKE_TOKEN", None))
        self.cli("doctor", "--offline")
        written = (self.repo / ".origin" / "doctor.json").read_text(encoding="utf-8")
        self.assertNotIn("super-secret-value-not-for-disk", written)

    def test_preflight_fails_when_lint_fails(self) -> None:
        (self.repo / "docs" / "policy" / "bad.md").write_text(
            "# Bad\n\n<!-- origin-meta\nowner: docs/INDEX.md\nstatus: active\n"
            "last-verified: 2026-10-03\n-->\n\n" + "x\n" * 400,
            encoding="utf-8",
        )
        self.assertEqual(self.cli("preflight"), 2)


if __name__ == "__main__":
    unittest.main()