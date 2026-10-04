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

Two directions are falsified. The first is mutation: remove the clause that
consults the rewrite and the defect returns; remove only the digest bound and
the hand-edit controls fail. The second is the record's own bytes: session
2026-10-04-019 declared seven artifacts and closed with exit 4 on its own task
file, and that stream carries no `task_rewrite`, so the rule reads it as
declaring nothing rather than as silent by default.
"""

from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

from harness import RepoTest

from originlib import session, taskops, tasks

# A closed session that did everything right and was still reported. Read out
# of git by `CommittedDefectTest`, not written here, so the shape under test is
# the one the fleet published rather than one written after the repair.
RECORDED_SESSION = "2026-10-04-019-t-0039-make-acceptance-and-steps-append"
RECORDED_TASK_FILE = "tasks/T-0039-make-acceptance-and-steps-append-on-task-new-so.md"


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
        # an excluded path they cannot check (D028).
        self.assertEqual(result["rewritten"], [self.task_path()])
        recorded = self.rewrites()
        self.assertEqual([entry["status"] for entry in recorded], ["claimed", "done"])
        for entry in recorded:
            self.assertEqual(len(entry["meta_sha256"]), 64)
            self.assertEqual(len(entry["body_sha256"]), 64)
            self.assertEqual(entry["task"], "T-0001")

    def test_the_command_line_names_the_rewritten_file(self) -> None:
        self.declare_work()
        self.run_task()
        code = self.cli(
            "session", "finish", "--outcome", "worked", "--summary", "ran a task", "--next", "none"
        )
        self.assertEqual(code, 0)
        self.assertIn("REWRITTEN by task commands (1)", self.output())
        self.assertIn(self.task_path(), self.output())

    def test_a_second_identical_write_is_not_recorded_twice(self) -> None:
        # `taskremote.claim` retries inside a loop and rewrites the same bytes on
        # each attempt. The record is a sequence of what happened, but a retry
        # that changed nothing is not an event worth reading.
        self.declare_work()
        taskops.claim("T-0001", "tester", "vm-x", self.active.session)
        taskops.claim("T-0001", "tester", "vm-x", self.active.session)
        self.assertEqual(len(self.rewrites()), 1)

    # ------------------------------------------------------------ the controls
    def test_an_edit_to_the_body_after_the_command_is_reported_again(self) -> None:
        self.declare_work()
        self.run_task()
        self.write(self.task_path(), self.read(self.task_path()) + "\nA later note.\n")
        result = session.finish("worked", "ran a task and wrote a note", "none")
        self.assertEqual(result["unlogged"], [self.task_path()])
        self.assertEqual(result["rewritten"], [])

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
        self.assertEqual(result["rewritten"], [self.task_path("T-0001")])

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
        self.assertEqual(result["unlogged"], [path])
        self.assertEqual(result["rewritten"], [])
        self.assertEqual(active.task, "")


class CommittedDefectTest(unittest.TestCase):
    """The defect as the fleet published it, read out of git.

    A stream with no `task_rewrite` event must still be read as declaring
    nothing. That is the direction a rule like this fails in silently: a parser
    that quietly stops matching looks exactly like a clean tree (defect 10).
    """

    def root(self) -> Path:
        here = Path(__file__).resolve()
        for parent in [here.parent, *here.parent.parents]:
            if (parent / "tasks").is_dir() and (parent / "tools").is_dir():
                return parent
        raise AssertionError("could not locate the repository root")

    def stream(self) -> list[dict] | None:
        result = subprocess.run(
            ["git", "show", f"HEAD:sessions/{RECORDED_SESSION}/events.jsonl"],
            cwd=str(self.root()), capture_output=True, text=True,
        )
        if result.returncode != 0:
            return None
        return [json.loads(line) for line in result.stdout.splitlines() if line.strip()]

    def test_the_recorded_session_reported_its_own_task_file(self) -> None:
        events = self.stream()
        if events is None:
            self.skipTest(f"session {RECORDED_SESSION} is not in this history")
        unlogged = [e["data"].get("path") for e in events if e["kind"] == "unlogged_change"]
        self.assertEqual(unlogged, [RECORDED_TASK_FILE])
        # It declared seven artifacts and was reported anyway, so this is a false
        # positive rather than a missing declaration.
        declared = [e["data"]["path"] for e in events if e["kind"] == "artifact"]
        self.assertEqual(len(declared), 7, declared)
        end = next(e for e in events if e["kind"] == "session_end")
        self.assertEqual(end["data"]["outcome"], "worked")
        self.assertEqual(end["data"]["unlogged_changes"], 1)

    def test_that_stream_declares_no_rewrite_so_the_rule_cannot_cover_it(self) -> None:
        events = self.stream()
        if events is None:
            self.skipTest(f"session {RECORDED_SESSION} is not in this history")
        self.assertEqual([e for e in events if e["kind"] == "task_rewrite"], [])
        # And the rule reads bytes, so a stream without the digests cannot be
        # honoured whatever its kind.
        self.assertFalse(tasks.digests_match(self.root() / RECORDED_TASK_FILE, {}))

    def test_a_digest_that_does_not_match_is_not_honoured(self) -> None:
        target = self.root() / RECORDED_TASK_FILE
        real = tasks.meta_digests(target)
        self.assertTrue(tasks.digests_match(target, real))
        for key in ("meta_sha256", "body_sha256"):
            wrong = dict(real)
            wrong[key] = "0" * 64
            self.assertFalse(tasks.digests_match(target, wrong), key)
        self.assertFalse(tasks.digests_match(self.root() / "tasks/README.md", real))


if __name__ == "__main__":
    unittest.main()