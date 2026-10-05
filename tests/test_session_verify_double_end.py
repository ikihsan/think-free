"""A second `session_end` is a note when the stream still ends with one.

Session 014's finish ran twice: the first `session_end` carried
`unlogged_changes: 11`, the intervening doc updates were logged, and a second
`session_end` closed the stream with `unlogged_changes: 0`. The old rule
failed any stream with two ends, so that truthful record read as broken and
strict verify stayed red. The rule now admits the re-finish shape while
still failing a stream whose last event is not `session_end`.
"""

from __future__ import annotations

import unittest

from harness import RepoTest

from originlib import events, report, sessionverify

SID = "2026-10-05-777-double-end"


def make_stream(kinds_data):
    events.append(SID, "session_start", {"goal": "g", "agent": "a", "task": ""})
    for kind, data in kinds_data:
        events.append(SID, kind, data)
    report.regenerate_session(SID)


class DoubleEndTest(RepoTest):
    def setUp(self):
        super().setUp()
        # session_report also checks the generated indexes exist.
        (self.repo / "sessions" / "INDEX.md").write_text("# Sessions\n")
        (self.repo / "tasks" / "INDEX.md").write_text("# Tasks\n")

    def problems(self):
        _report, problems = sessionverify.session_report()
        return [str(p) for p in problems]

    def test_two_ends_with_terminal_end_is_not_a_failure(self):
        make_stream(
            [
                ("session_end", {"outcome": "worked", "unlogged_changes": 11}),
                ("doc_update", {"summary": "x", "path": "STATE.md"}),
                ("session_end", {"outcome": "worked", "unlogged_changes": 0}),
            ]
        )
        self.assertEqual(self.problems(), [])

    def test_work_after_final_end_still_fails(self):
        make_stream(
            [
                ("session_end", {"outcome": "worked", "unlogged_changes": 0}),
                ("note", {"summary": "late work"}),
            ]
        )
        self.assertTrue(any("unfinished" in m for m in self.problems()))

    def test_single_end_still_ok(self):
        make_stream([("session_end", {"outcome": "worked", "unlogged_changes": 0})])
        self.assertEqual(self.problems(), [])


if __name__ == "__main__":
    unittest.main()
