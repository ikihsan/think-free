"""Defect 24, first half: one sequence number per line, whoever is writing.

Session 008's stream carried 181 lines over 162 sequence numbers, which
`session verify` rejects and no later commit could land. `seq` was allocated by
reading the file's tail and adding one, and the append happened outside the lock
scope, so two writers both read the same tail and both wrote the same number.

These tests run the racing shape for real: separate processes, real files, a
real `flock`. A lock that looked right but did not cover the write would pass
on a machine that interleaved cleanly and corrupt the log on one that did not,
so the raw bytes are read back and the numbering is asserted, not the source.
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


APPENDS_PER_PROCESS = 12
PROCESSES = 4


def _append_many(args) -> None:
    """Run in a child process: append many events to one shared stream."""
    path, session, count, start = args
    for index in range(count):
        events.append(
            session,
            "note",
            {"summary": f"p{start}-{index}", "n": index},
            path=path,
        )


class StreamConcurrencyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.path = Path(self.dir.name) / "events.jsonl"

    def _seqs(self) -> list[int]:
        return [e["seq"] for e in events.read(self.path)]

    def test_concurrent_appends_from_separate_processes_stay_contiguous(self) -> None:
        context = multiprocessing.get_context("fork")
        jobs = [
            (self.path, "s", APPENDS_PER_PROCESS, worker)
            for worker in range(PROCESSES)
        ]
        procs = [context.Process(target=_append_many, args=(job,)) for job in jobs]
        for proc in procs:
            proc.start()
        for proc in procs:
            proc.join(60)
            self.assertEqual(proc.exitcode, 0, "a writer process died")

        expected = PROCESSES * APPENDS_PER_PROCESS
        seqs = self._seqs()
        self.assertEqual(
            seqs,
            list(range(1, expected + 1)),
            "sequence numbers must be 1..n with no duplicate and no gap",
        )

    def test_every_concurrent_line_is_intact_json(self) -> None:
        """The lock must serialise the write too, not only the number.

        A lock held around the allocation but released before the append would
        pass the test above on a machine that interleaved cleanly and corrupt
        the log on one that did not, so the raw bytes are read back.
        """
        context = multiprocessing.get_context("fork")
        jobs = [
            (self.path, "s", APPENDS_PER_PROCESS, worker) for worker in range(PROCESSES)
        ]
        procs = [context.Process(target=_append_many, args=(job,)) for job in jobs]
        for proc in procs:
            proc.start()
        for proc in procs:
            proc.join(60)

        raw = self.path.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(raw), PROCESSES * APPENDS_PER_PROCESS)
        for line in raw:
            try:
                parsed = json.loads(line)
            except json.JSONDecodeError as error:  # pragma: no cover
                self.fail(f"interleaved write produced unparsable line: {error}")
            self.assertEqual(parsed["kind"], "note")
            self.assertIn(parsed["data"]["summary"], {f"p{w}-{i}"
                for w in range(PROCESSES) for i in range(APPENDS_PER_PROCESS)})

    def test_hold_stream_rejects_a_second_writer_while_held(self) -> None:
        """The lock is real: a second process cannot take it mid-hold."""
        context = multiprocessing.get_context("fork")
        ready = multiprocessing.Event()
        release = multiprocessing.Event()
        # A forked child gets a *copy* of the parent's dict, so an assertion on
        # a dict the child wrote is vacuously true. Results come back through a
        # queue, which is the only one of these three channels a child can write
        # that the parent actually reads.
        report = context.Queue()

        def holder() -> None:
            with events.hold_stream(self.path):
                ready.set()
                release.wait(30)

        def blocked() -> None:
            import fcntl

            ready.wait(30)
            handle = open(self.path, "a+", encoding="utf-8")
            try:
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                report.put({"acquired": True})
            except OSError:
                report.put({"acquired": False})
            finally:
                handle.close()
            release.set()

        first = context.Process(target=holder)
        second = context.Process(target=blocked)
        first.start()
        second.start()
        first.join(60)
        second.join(60)
        self.assertEqual(first.exitcode, 0)
        self.assertEqual(second.exitcode, 0)
        observed = report.get(timeout=5)
        self.assertIs(
            observed["acquired"],
            False,
            "a second process took the stream lock while the first held it",
        )

    def test_next_seq_is_a_preview_and_says_so(self) -> None:
        self.assertEqual(events.next_seq(self.path), 1)
        events.append("s", "note", {"summary": "one"}, path=self.path)
        self.assertEqual(events.next_seq(self.path), 2)

    def test_append_rejects_an_unknown_kind_and_writes_nothing(self) -> None:
        with self.assertRaises(ValueError):
            events.append("s", "not-a-kind", {}, path=self.path)
        self.assertFalse(self.path.exists())

if __name__ == "__main__":
    unittest.main()
