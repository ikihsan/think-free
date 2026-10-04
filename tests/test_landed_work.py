"""Whose change is it, when another VM's commits land in the middle of a session.

Session 029 (T-0016) closed with exit 4 and nine `unlogged_change` events, every
one naming a file that session never touched. The reflog shows the cause: `sync
land` rebased the branch onto the other VM's commits while the session was open,
and reconciliation compared the tree against the session's *starting* commit, so
it attributed the base move to the session.

These tests replay that sequence on two real clones and pin both directions: work
that arrived from the base is not the session's, and work the session did is.
"""

from __future__ import annotations

import unittest
from pathlib import Path

from harness import RepoTest, git, make_fleet

from originlib import session, sync, syncland, taskops


class LandedWorkTest(RepoTest):
    def setUp(self) -> None:
        super().setUp()
        self.fleet = make_fleet(self)
        self.seed = self.fleet / "seed"
        self.vm_a = self.fleet / "vm-a"
        self.vm_b = self.fleet / "vm-b"
        self.use(self.seed)
        taskops.create("landed work attribution", "true")
        git(self.seed, "add", "-A")
        git(self.seed, "commit", "-qm", "add task")
        git(self.seed, "push", "-q", "origin", "research/origin")
        for clone in (self.vm_a, self.vm_b):
            git(clone, "pull", "-q", "--ff-only")

    # ------------------------------------------------------------- helpers
    def write_on(self, clone: Path, relative: str, content: str) -> None:
        path = clone / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def commit_on(self, clone: Path, message: str) -> None:
        git(clone, "add", "-A")
        git(clone, "commit", "-qm", message)

    def push_from(self, clone: Path) -> None:
        git(clone, "push", "-q", "origin", "research/origin")

    def other_vm_lands_work(self) -> str:
        """VM B changes two files, commits, and pushes them to the shared base."""
        self.write_on(self.vm_b, "vm-b/notes.md", "vm b work\n")
        self.write_on(self.vm_b, "STATE.md", "state as vm b left it\n")
        self.commit_on(self.vm_b, "vm-b: work this session never touched")
        self.push_from(self.vm_b)
        return git(self.vm_b, "rev-parse", "HEAD")

    def open_session(self):
        self.use(self.vm_a)
        return session.start("land the other VM's work", agent="tester", task="T-0001")

    def declare_own_work(self, name: str = "a.md") -> str:
        """VM A writes a file, declares it, and commits it."""
        relative = f"vm-a/{name}"
        self.write_on(self.vm_a, relative, "vm a work\n")
        session.artifact(relative)
        self.commit_on(self.vm_a, f"vm-a: {relative}")
        return relative

    def unlogged(self, session_id: str) -> list[str]:
        return [
            event["data"]["path"]
            for event in self.session_events(session_id)
            if event["kind"] == "unlogged_change"
        ]

    def events_of(self, session_id: str, kind: str) -> list[dict]:
        return [e for e in self.session_events(session_id) if e["kind"] == kind]

    # ---------------------------------------------------------------- the defect
    def test_landed_work_is_not_reported_as_this_session_s_own(self) -> None:
        active = self.open_session()
        self.declare_own_work()
        self.other_vm_lands_work()
        syncland.land()
        result = session.finish("worked", "landed the base", "none")
        self.assertEqual(result["unlogged"], [])
        self.assertEqual(self.unlogged(active.session), [])
        self.assertNotIn("STATE.md", self.unlogged(active.session))

    def test_own_undeclared_change_is_still_reported_alongside_landed_work(self) -> None:
        active = self.open_session()
        self.declare_own_work()
        self.other_vm_lands_work()
        syncland.land()
        self.write_on(self.vm_a, "vm-a/scratch.md", "never declared\n")
        result = session.finish("worked", "landed the base", "none")
        self.assertEqual(result["unlogged"], ["vm-a/scratch.md"])
        self.assertEqual(self.unlogged(active.session), ["vm-a/scratch.md"])

    def test_a_landed_file_edited_after_landing_is_still_reported(self) -> None:
        # Attribution follows the newest commit that touched the path, not the
        # existence of a landed commit: this session's own later edit is its own.
        active = self.open_session()
        self.declare_own_work()
        self.other_vm_lands_work()
        syncland.land()
        self.write_on(self.vm_a, "STATE.md", "and this session's own line\n")
        result = session.finish("worked", "landed the base", "none")
        self.assertEqual(result["unlogged"], ["STATE.md"])

    def test_an_unrecorded_base_move_keeps_reporting_what_it_cannot_prove(self) -> None:
        # Only a base move the tooling performed is recorded. A rebase run by hand
        # leaves the same tree and no record, so its paths stay reported: the
        # tooling never silences a file it cannot prove belongs to someone else.
        active = self.open_session()
        self.declare_own_work()
        self.other_vm_lands_work()
        git(self.vm_a, "fetch", "-q", "origin")
        git(self.vm_a, "rebase", "-q", "origin/research/origin")
        result = session.finish("worked", "rebased by hand", "none")
        self.assertEqual(sorted(result["unlogged"]), ["STATE.md", "vm-b/notes.md"])
        self.assertEqual(self.unlogged(active.session),
                         sorted(["STATE.md", "vm-b/notes.md"]))

    def test_the_landing_is_recorded_with_the_commits_that_arrived(self) -> None:
        active = self.open_session()
        self.declare_own_work()
        arrived = self.other_vm_lands_work()
        syncland.land()
        session.finish("worked", "landed the base", "none")
        recorded = self.events_of(active.session, "base_advance")
        self.assertEqual(len(recorded), 1)
        data = recorded[0]["data"]
        self.assertIn(arrived, data["commits"])
        self.assertEqual(data["commit_count"], len(data["commits"]))
        self.assertFalse(data["truncated"])
        self.assertEqual(data["reason"], "sync land")
        self.assertNotEqual(data["from"], data["to"])
        # The rebase rewrote this session's own commit, so the old tip is named
        # as the start rather than being mistaken for something that arrived.
        self.assertNotIn(data["from"], data["commits"])

    def test_landing_outside_a_session_records_nothing(self) -> None:
        self.use(self.vm_a)
        self.write_on(self.vm_a, "vm-a/late.md", "no session open\n")
        self.commit_on(self.vm_a, "vm-a: late commit")
        self.other_vm_lands_work()
        syncland.land()
        self.assertFalse((self.vm_a / "sessions" / "active.json").exists())
        # No session, so there is no record to write into; the landing must not
        # invent one. The base still moved, which is what this checks.
        status = sync.status()
        self.assertEqual(status["ahead"], 0)
        self.assertEqual(status["behind"], 0)
        # The other VM's commit is now an ancestor: the base moved under it.
        self.assertEqual(
            git(self.vm_a, "merge-base", "--is-ancestor",
                git(self.vm_b, "rev-parse", "HEAD"), "HEAD"),
            "",
        )


if __name__ == "__main__":
    unittest.main()