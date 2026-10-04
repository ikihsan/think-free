"""Whose change is a task file that `task complete` just rewrote?

Defect 12: reconciliation reports a file this session changed without declaring
it, and `task claim`, `task complete` and `task release` all rewrite the task
file they manage. Every one of them therefore closed its session with exit 4
naming the tooling's own write — 37 such reports across the 21 closed sessions
in this repository's history, `observed` 2026-10-04.

The repair is not an exemption. `_set_meta` records a `task_rewrite` event
carrying the two digests of what it wrote — the meta block, and everything
outside it — and reconciliation honours it only while the file still holds those
bytes. So the file is silent for the command's write and reported again for the
agent's next one, which is the trade-off defect 12 refused to accept: a
declaration that covered the *file* would silence every later edit to it,
including ticking an acceptance checkbox.

The same lifecycle also appends to `tasks/CLAIMS.jsonl`, which T-0050 gave the
same treatment with a whole-file digest: a `.jsonl` path was invisible to the
report for a different reason — its suffix — and a second append ends the first
declaration's validity, so each one is declared as it happens. Every count in
this file therefore names the ledger too, because that is what a task command
actually writes.

Two directions are falsified. The first is mutation: remove the clause that
consults the rewrite and the defect returns; remove only the digest bound and
the hand-edit controls fail. The second is the record's own bytes, and it now
lives in `test_task_rewrite_recorded.py`.
"""

from __future__ import annotations

import subprocess
import unittest

from harness import RepoTest

from originlib import session, taskops, tasks

# The second file a task command writes, declared the same way since T-0050.
LEDGER = "tasks/CLAIMS.jsonl"


class TaskRewriteTest(RepoTest):
    """A command's own write is not an undeclared change, and nothing else is."""

    def setUp(self) -> None:
        super().setUp()
        taskops.create("attribute a rewritten task file", "true")
        self.commit("add task")
        self.active = session.start("run a task to completion", agent="tester", task="T-0001")

    # -------------------------------------------------------------- helpers
    def git(self, *args: str) -> None:
        subprocess.run(["git", *args], cwd=str(self.repo), check=True,
                       capture_output=True, text=True)

    def commit(self, message: str) -> None:
        self.git("add", "-A")
        self.git("commit", "-qm", message)

    def declare_work(self, name: str = "notes.md") -> str:
        relative = f"work/{name}"
        self.write(relative, "the real work\n")
        session.artifact(relative)
        self.commit(f"work: {relative}")
        return relative

    def run_task(self) -> None:
        """The commands a task's lifecycle is made of, with a commit each."""
        taskops.claim("T-0001", "tester", "vm-x", self.active.session)
        self.commit("claim")
        taskops.transition("T-0001", "done", "done")
        self.commit("complete")

    def task_path(self, task_id: str = "T-0001") -> str:
        return f"tasks/{tasks.find(task_id).path.name}"

    def rewrite(self, old: str, new: str, path: str | None = None) -> None:
        target = path or self.task_path()
        self.write(target, self.read(target).replace(old, new))

    def events(self, kind: str) -> list[dict]:
        return [
            event["data"]
            for event in self.session_events(self.active.session)
            if event["kind"] == kind
        ]

    def unlogged(self) -> list[str]:
        return [entry.get("path") for entry in self.events("unlogged_change")]

    def rewrites(self) -> list[dict]:
        return self.events("task_rewrite")

    def rewrites_of(self, path: str) -> list[dict]:
        return [entry for entry in self.rewrites() if entry["path"] == path]

    # ------------------------------------------------------- the defect, repaired
    def test_a_task_file_the_command_rewrote_is_not_reported(self) -> None:
        self.declare_work()
        self.run_task()
        result = session.finish("worked", "ran a task", "none")
        self.assertEqual(result["unlogged"], [], result["unlogged"])
        self.assertEqual(self.unlogged(), [])

    def test_the_rewrite_is_recorded_with_the_bytes_it_wrote(self) -> None:
        self.declare_work()
        self.run_task()
        result = session.finish("worked", "ran a task", "none")
        # Named rather than dropped: an excluded path an operator cannot see is
        # an excluded path they cannot check (D028). Both files are named because
        # a task lifecycle writes both.
        self.assertEqual(result["rewritten"], [LEDGER, self.task_path()])
        recorded = self.rewrites_of(self.task_path())
        self.assertEqual([entry["status"] for entry in recorded], ["claimed", "done"])
        for entry in recorded:
            self.assertEqual(len(entry["meta_sha256"]), 64)
            self.assertEqual(len(entry["body_sha256"]), 64)
            self.assertEqual(entry["task"], "T-0001")
        # The ledger carries one digest and a size rather than the meta pair: it
        # has no task-meta block, and the shapes are told apart by their keys.
        # Only the newest append's declaration still describes the file, which is
        # why this reads the last one rather than all of them.
        entries = self.rewrites_of(LEDGER)
        self.assertEqual(len(entries), 2)
        newest = entries[-1]
        self.assertEqual(len(newest["sha256"]), 64)
        self.assertEqual(newest["size"], (self.repo / LEDGER).stat().st_size)
        self.assertEqual(newest["action"], "complete")
        self.assertNotIn("meta_sha256", newest)

    def test_the_command_line_names_the_rewritten_file(self) -> None:
        self.declare_work()
        self.run_task()
        code = self.cli(
            "session", "finish", "--outcome", "worked", "--summary", "ran a task", "--next", "none"
        )
        self.assertEqual(code, 0)
        self.assertIn("REWRITTEN by task commands (2)", self.output())
        self.assertIn(self.task_path(), self.output())
        self.assertIn(LEDGER, self.output())

    def test_a_second_identical_write_is_not_recorded_twice(self) -> None:
        # `taskremote.claim` retries inside a loop and rewrites the same bytes on
        # each attempt. The record is a sequence of what happened, but a retry
        # that changed nothing is not an event worth reading. Counted on the task
        # file: the ledger's second line differs because it carries a new `ts`,
        # so it is a real second write and is declared as one.
        self.declare_work()
        taskops.claim("T-0001", "tester", "vm-x", self.active.session)
        taskops.claim("T-0001", "tester", "vm-x", self.active.session)
        self.assertEqual(len(self.rewrites_of(self.task_path())), 1)
        self.assertEqual(len(self.rewrites_of(LEDGER)), 2)

    # ------------------------------------------------------------ the controls
    def test_an_edit_to_the_body_after_the_command_is_reported_again(self) -> None:
        self.declare_work()
        self.run_task()
        self.write(self.task_path(), self.read(self.task_path()) + "\nA later note.\n")
        result = session.finish("worked", "ran a task and wrote a note", "none")
        self.assertEqual(result["unlogged"], [self.task_path()])
        self.assertNotIn(self.task_path(), result["rewritten"])

    def test_an_edit_to_the_meta_block_after_the_command_is_reported_again(self) -> None:
        # The control a blanket exemption fails: a path-based exemption matches
        # on the file's *name*, so only the digests catch this.
        self.declare_work()
        self.run_task()
        self.rewrite("status: done", "status: cancelled")
        result = session.finish("worked", "ran a task", "none")
        self.assertEqual(result["unlogged"], [self.task_path()])

    def test_a_task_file_changed_with_no_command_at_all_is_reported(self) -> None:
        self.declare_work()
        self.rewrite("status: open", "status: blocked")
        result = session.finish("worked", "touched a task file by hand", "none")
        self.assertEqual(result["unlogged"], [self.task_path()])
        self.assertEqual(self.rewrites(), [])

    def test_a_rewrite_of_one_task_does_not_cover_another(self) -> None:
        # The declaration names one path, so it cannot become a rule about
        # `tasks/*.md` — which is the form that would silence real work.
        taskops.create("a second task", "true")
        self.commit("add a second task")
        self.declare_work()
        taskops.transition("T-0001", "done", "done")
        self.commit("complete the first")
        self.rewrite("status: open", "status: blocked", self.task_path("T-0002"))
        result = session.finish("worked", "completed one task and touched the other", "none")
        self.assertEqual(result["unlogged"], [self.task_path("T-0002")])
        self.assertIn(self.task_path("T-0001"), result["rewritten"])
        self.assertNotIn(self.task_path("T-0002"), result["rewritten"])

    def test_undeclared_work_is_still_reported_alongside_a_rewrite(self) -> None:
        self.declare_work()
        self.run_task()
        self.write("work/scratch.md", "never declared\n")
        result = session.finish("worked", "ran a task and left a scratch file", "none")
        self.assertEqual(result["unlogged"], ["work/scratch.md"])


class CommandOutsideASessionTest(RepoTest):
    """No session, no record to write into, and nothing invented."""

    def test_a_command_run_with_no_session_open_records_nothing(self) -> None:
        taskops.create("attribute a rewritten task file", "true")
        subprocess.run(["git", "add", "-A"], cwd=str(self.repo), check=True,
                       capture_output=True)
        subprocess.run(["git", "commit", "-qm", "add task"], cwd=str(self.repo), check=True,
                       capture_output=True)
        taskops.transition("T-0001", "claimed", "")
        streams = list((self.repo / "sessions").glob("*/events.jsonl"))
        self.assertEqual(streams, [], streams)

    def test_the_next_session_reports_a_command_run_before_it_opened(self) -> None:
        taskops.create("attribute a rewritten task file", "true")
        subprocess.run(["git", "add", "-A"], cwd=str(self.repo), check=True,
                       capture_output=True)
        subprocess.run(["git", "commit", "-qm", "add task"], cwd=str(self.repo), check=True,
                       capture_output=True)
        taskops.transition("T-0001", "claimed", "")
        active = session.start("a session that did not run the command", agent="tester")
        path = f"tasks/{tasks.find('T-0001').path.name}"
        result = session.finish("worked", "the command ran outside the session", "none")
        # Both files the command wrote, and both reported: a declaration has to be
        # written while the session that made the change is open, so an append
        # made outside one is as undeclared as the meta rewrite beside it.
        self.assertEqual(result["unlogged"], [LEDGER, path])
        self.assertEqual(result["rewritten"], [])
        self.assertEqual(active.task, "")


if __name__ == "__main__":
    unittest.main()