"""Defect 24, second half: one `session finish` at a time.

The stream lock alone would leave the record well-formed and reconciled twice:
two `session_end` events, two full `unlogged_change` sweeps over the same paths.
`session finish` therefore takes its own lock across the whole operation.

The gap this file exists to close. The first draft of these tests exercised
`sessionlock` directly, so deleting the `with sessionlock.single_finish()` from
`finish` left every one of them green while the defect remained. `sessionlock`
can be perfect and the defect still ships if nothing asserts the caller uses
it. Two tests here ask about `finish` itself, and both were falsified by
mutation before being believed.

A third lesson is recorded in the refusal test: two processes racing each other
can be *serialized* by the scheduler, which is correct behaviour and reads as a
failure if a test assumes it must collide. The collision is therefore arranged
rather than raced for.
"""


from __future__ import annotations

import json
import multiprocessing
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from originlib import events  # noqa: E402


class FinishLockTests(unittest.TestCase):
    """The second of two overlapping `finish` runs must be refused, not merged.

    The stream lock alone is not enough: it would leave the record well-formed
    and reconciled twice. This is the second half of defect 24's repair.
    """

    def setUp(self) -> None:
        from originlib import paths

        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self._real_root = paths.repo_root
        paths.repo_root = lambda: Path(self.dir.name)
        self.addCleanup(self._restore_root)

    def _restore_root(self) -> None:
        from originlib import paths

        paths.repo_root = self._real_root

    def _write_active(self) -> str:
        from originlib import activestate

        session = "2026-10-08-014-finish-lock"
        directory = Path(self.dir.name) / "sessions" / session
        directory.mkdir(parents=True)
        (directory / "events.jsonl").write_text(
            json.dumps(
                {
                    "schema": "origin.session.event/1",
                    "seq": 1,
                    "ts": "2026-10-08T00:00:00+00:00",
                    "session": session,
                    "kind": "session_start",
                    "data": {"goal": "g", "agent": "a"},
                }
            )
            + "\n",
            encoding="utf-8",
        )
        activestate.write_pointer(
            activestate.ActiveSession(
                session=session,
                goal="g",
                agent="a",
                task="",
                started_at="2026-10-08T00:00:00+00:00",
                started_epoch=0.0,
                start_head="h",
                branch="b",
                host="host",
            )
        )
        self.addCleanup(activestate.clear_pointer)
        return session

    def test_the_second_of_two_held_finishes_is_refused(self) -> None:
        from originlib import sessionlock
        from originlib.activestate import SessionError

        self._write_active()
        with sessionlock.single_finish():
            with self.assertRaises(SessionError) as caught:
                with sessionlock.single_finish():
                    pass  # pragma: no cover - the inner hold must never enter
        self.assertIn("already running", str(caught.exception))

    def test_a_second_process_is_refused_while_a_finish_holds(self) -> None:
        from originlib import sessionlock
        from originlib.activestate import SessionError

        self._write_active()
        context = multiprocessing.get_context("fork")
        ready = multiprocessing.Event()
        release = multiprocessing.Event()
        report = context.Queue()

        def holder() -> None:
            with sessionlock.single_finish():
                ready.set()
                release.wait(30)

        def prober() -> None:
            from originlib import paths

            paths.repo_root = lambda: Path(self.dir.name)
            ready.wait(30)
            try:
                with sessionlock.single_finish():
                    report.put({"entered": True, "error": ""})
            except SessionError as error:
                report.put({"entered": False, "error": str(error)})
            release.set()

        first = context.Process(target=holder)
        second = context.Process(target=prober)
        first.start()
        second.start()
        first.join(60)
        second.join(60)
        self.assertEqual(first.exitcode, 0)
        self.assertEqual(second.exitcode, 0)
        observed = report.get(timeout=5)
        self.assertFalse(observed["entered"], observed["error"])
        self.assertIn("already running", observed["error"])

    def test_the_lock_is_not_created_where_git_would_see_it(self) -> None:
        """A committed lock is a lock nothing holds, so it must be ignorable."""
        repo = Path(__file__).resolve().parents[1]
        ignore = (repo / ".gitignore").read_text(encoding="utf-8").splitlines()
        self.assertIn(".finish.lock", ignore)

    def test_finish_holds_the_lock_while_its_body_runs(self) -> None:
        """`finish` must take the lock, not merely have one available.

        Testing `sessionlock` alone left the whole repair unverified: removing
        the `with sessionlock.single_finish()` from `finish` left every test in
        this file green, because nothing asserted that the caller used it. So
        this replaces the body with a probe and asks what the lock's state is
        while `finish` is running.
        """
        import fcntl

        from originlib import paths, session as session_module

        session = self._write_active()
        observed = {}

        def probe(outcome, summary, next_steps, push):
            handle = open(
                paths.session_dir(session) / ".finish.lock", "a+", encoding="utf-8"
            )
            try:
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                observed["held"] = False
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
            except OSError:
                observed["held"] = True
            finally:
                handle.close()
            return {"session": session, "outcome": outcome, "seq": 99}

        original = session_module._finish_locked
        session_module._finish_locked = probe
        self.addCleanup(setattr, session_module, "_finish_locked", original)
        session_module.finish("worked", "s", "n")
        self.assertTrue(
            observed.get("held"),
            "finish ran its body without holding the lock another process needs",
        )

    def test_a_finish_is_refused_while_another_holds_the_lock(self) -> None:
        """The end-to-end shape: a lock held, then `finish` called anyway.

        Deterministic on purpose. An earlier version here raced two finishes
        against each other and read the *serialization* as a defect: the second
        waited, found the lock free, and correctly succeeded. Which is the right
        behaviour and a flaky test. So the collision is arranged here instead —
        the holder is this process, the newcomer is a child — and what is
        asserted is the refusal and the absence of a second end.
        """
        from originlib import events, session as session_module, sessionlock
        from originlib.activestate import SessionError

        session = self._write_active()
        original = session_module._finish_locked
        session_module._finish_locked = lambda *a, **k: {
            "session": session,
            "outcome": "worked",
            "seq": 99,
        }
        self.addCleanup(setattr, session_module, "_finish_locked", original)

        context = multiprocessing.get_context("fork")
        report = context.Queue()

        def run() -> None:
            from originlib import paths as child_paths

            child_paths.repo_root = lambda: Path(self.dir.name)
            try:
                session_module.finish("worked", "from child", "n")
                report.put("accepted")
            except SessionError as error:
                report.put(f"refused: {error}")

        with sessionlock.single_finish():
            child = context.Process(target=run)
            child.start()
            child.join(60)
        self.assertEqual(child.exitcode, 0)
        self.assertTrue(
            report.get(timeout=5).startswith("refused:"),
            "finish ran its body while another process held the lock",
        )
        ends = [
            e
            for e in events.read(
                Path(self.dir.name) / "sessions" / session / "events.jsonl"
            )
            if e.get("kind") == "session_end"
        ]
        self.assertEqual(len(ends), 0, f"a refused finish still ended the session: {ends}")
