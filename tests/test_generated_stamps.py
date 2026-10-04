"""Generated files must be functions of the tree, not of the clock.

`doc lint` compares a committed generated file with what the generator produces
now and fails when they differ. On 2026-10-04 that check failed on 42 committed
session reports and all three indexes, because each stamped `last-verified` with
the render date: nothing about them had changed except the day. Any push after
local midnight would have reddened CI for every VM.

These tests pin the property that makes the check meaningful. The clock is moved
forward in place, so a stamp taken from `now` fails them.
"""

from __future__ import annotations

import unittest

from harness import RepoTest

from originlib import docindex, events, report, session, tasks


class _Clock:
    """Context manager that moves `events.now_iso` forward without touching time."""

    def __init__(self, test: unittest.TestCase, when: str) -> None:
        self.test = test
        self.when = when
        self.original = events.now_iso

    def __enter__(self) -> "_Clock":
        events.now_iso = lambda: self.when  # type: ignore[assignment]
        self.test.addCleanup(self.restore)
        return self

    def __exit__(self, *exc: object) -> None:
        self.restore()

    def restore(self) -> None:
        events.now_iso = self.original  # type: ignore[assignment]


class GeneratedStampTest(RepoTest):
    def setUp(self) -> None:
        super().setUp()
        self.active = session.start("stamp the record from content", agent="tester")
        session.note("a milestone")
        session.finish("worked", "done", "none")
        report.regenerate_session(self.active.session)
        self.write_generated()
        self.rendered = {
            "session": report.render_session_report(self.active.session),
            "sessions": report.render_sessions_index(),
            "tasks": tasks.render_tasks_index(),
            "docs": docindex.render(),
        }

    def test_rendering_a_day_later_changes_nothing(self) -> None:
        with _Clock(self, "2031-12-24T09:00:00+00:00"):
            again = {
                "session": report.render_session_report(self.active.session),
                "sessions": report.render_sessions_index(),
                "tasks": tasks.render_tasks_index(),
                "docs": docindex.render(),
            }
        for name, before in self.rendered.items():
            self.assertEqual(before, again[name], f"{name} changed with the clock")

    def test_lint_passes_when_the_committed_file_is_from_an_earlier_day(self) -> None:
        # The recorded bytes are written at today's date; linting them tomorrow
        # must still pass, or the gate measures the calendar rather than the tree.
        with _Clock(self, "2031-12-24T09:00:00+00:00"):
            result = self.cli("doc", "lint")
        self.assertEqual(result, 0, self.output())

    def test_a_session_report_is_stamped_with_its_own_last_event(self) -> None:
        today = events.now_iso()[:10]
        self.assertIn(f"last-verified: {today}", report.render_session_report(self.active.session))
        # The index carries the newest session's date, not the render date.
        self.assertIn(f"last-verified: {today}", report.render_sessions_index())

    def test_an_index_with_nothing_to_index_says_unknown_rather_than_today(self) -> None:
        # A stamp nobody can support would claim a verification that never
        # happened. An empty ledger and an empty document set both say so.
        self.assertEqual(tasks.index_stamp(), "unknown")
        self.assertEqual(docindex.index_stamp([]), "unknown")


if __name__ == "__main__":
    unittest.main()