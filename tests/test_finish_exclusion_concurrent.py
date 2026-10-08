"""Defect 24, third half: two real overlapping finishes must never share a stream.

Split out of `test_finish_exclusion.py` when that file reached the 300-line
cap. The division is the one the file's docstring names: this is the
together-either-way case, the other file holds the refusal cases.
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


class ConcurrentFinishTests(unittest.TestCase):

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


    def test_two_finishes_running_together_never_share_the_stream(self) -> None:
        """When two bodies really do overlap, the stream stays well-formed.

        Unlike the refusal test this does not assume the second is turned away:
        it starts both at once and measures the outcome that matters either way,
        which is one `session_end` and sequence numbers `1..n`. Runs where the
        lock serialised them produce one end; runs where both entered would
        produce two and a gap, which is the defect.
        """
        from originlib import events, session as session_module

        session = self._write_active()
        context = multiprocessing.get_context("fork")
        gate = context.Event()
        report = context.Queue()

        def stub(outcome, summary, next_steps, push):
            # Widen the window: hold here so both processes are inside `finish`
            # at once if the lock does not stop the second one.
            gate.wait(30)
            for _ in range(20):
                events.append(
                    session,
                    "unlogged_change",
                    {"summary": f"{summary} step", "path": f"{summary}.txt"},
                    host="host",
                )
            events.append(
                session,
                "session_end",
                {"summary": summary, "outcome": outcome},
                host="host",
            )
            return {"session": session, "outcome": outcome, "seq": 0}

        def run(tag: str) -> None:
            from originlib import paths as child_paths

            child_paths.repo_root = lambda: Path(self.dir.name)
            try:
                session_module.finish("worked", tag, "n")
                report.put(f"{tag}:ok")
            except Exception as error:  # noqa: BLE001 - the message is the datum
                report.put(f"{tag}:{type(error).__name__}")

        original = session_module._finish_locked
        session_module._finish_locked = stub
        self.addCleanup(setattr, session_module, "_finish_locked", original)

        procs = [context.Process(target=run, args=(f"p{i}",)) for i in range(2)]
        for proc in procs:
            proc.start()
        gate.set()
        for proc in procs:
            proc.join(60)
            self.assertEqual(proc.exitcode, 0)
        results = [report.get(timeout=5) for _ in procs]

        stream = events.read(
            Path(self.dir.name) / "sessions" / session / "events.jsonl"
        )
        numbers = [e["seq"] for e in stream]
        self.assertEqual(
            numbers,
            list(range(1, len(numbers) + 1)),
            f"sequence not 1..n contiguous after two finishes: {results}",
        )
        ends = [e for e in stream if e.get("kind") == "session_end"]
        self.assertEqual(
            len(ends), 1, f"two finishes produced {len(ends)} ends: {results}"
        )

if __name__ == "__main__":
    unittest.main()
