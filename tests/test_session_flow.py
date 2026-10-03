"""Session boundaries in a fleet: a session that starts stale, or finishes local.

Split out of `test_sync.py` when that file reached the 300-line cap: the
transport tests (fetch, pull, push, land) are about moving commits, these are
about when a session's own record enters and leaves a machine. Both use the
same two-clone fleet harness.
"""

from __future__ import annotations

import unittest

from harness import RepoTest, git, make_fleet

from originlib import session
from originlib.activestate import SessionError


class SessionBoundaryTest(RepoTest):
    def setUp(self) -> None:
        super().setUp()
        self.fleet = make_fleet(self)
        self.vm_a = self.fleet / "vm-a"
        self.vm_b = self.fleet / "vm-b"

    def test_start_fast_forwards_a_behind_vm(self) -> None:
        (self.vm_b / "from-b.md").write_text("b\n", encoding="utf-8")
        git(self.vm_b, "add", "-A")
        git(self.vm_b, "commit", "-qm", "add from-b")
        git(self.vm_b, "push", "-q", "origin", "research/origin")
        self.use(self.vm_a)
        from originlib import session

        active = session.start("start from the newest commit", agent="agent-a")
        self.assertEqual(active.start_head, git(self.vm_b, "rev-parse", "HEAD"))
        session.finish("no-change", "verified", "none")

    def test_start_refuses_a_dirty_tree_when_the_remote_moved(self) -> None:
        (self.vm_b / "from-b.md").write_text("b\n", encoding="utf-8")
        git(self.vm_b, "add", "-A")
        git(self.vm_b, "commit", "-qm", "add from-b")
        git(self.vm_b, "push", "-q", "origin", "research/origin")
        self.use(self.vm_a)
        (self.vm_a / "dirty.md").write_text("uncommitted\n", encoding="utf-8")
        from originlib import session

        with self.assertRaises(SessionError) as caught:
            session.start("must not start dirty", agent="agent-a")
        self.assertIn("dirty.md", str(caught.exception))

    def test_start_records_the_remote_state_it_synced_to(self) -> None:
        self.use(self.vm_a)
        from originlib import session

        active = session.start("record the sync point", agent="agent-a")
        events = self.session_events(active.session)
        data = next(e for e in events if e["kind"] == "session_start")["data"]
        self.assertEqual(data["remote"], "origin")
        self.assertEqual(data["base_branch"], "research/origin")
        session.finish("no-change", "recorded", "none")

    def test_finish_with_push_publishes_the_record(self) -> None:
        self.use(self.vm_a)
        from originlib import session

        session.start("push at the end", agent="agent-a")
        result = session.finish("no-change", "nothing changed", "none", push=True)
        self.assertTrue(result["pushed"])
        git(self.vm_b, "fetch", "-q", "origin")
        sessions = git(self.vm_b, "ls-tree", "--name-only", "origin/research/origin", "sessions/")
        self.assertIn(result["session"], sessions)

    def test_finish_with_push_refuses_uncommitted_work(self) -> None:
        self.use(self.vm_a)
        from originlib import session

        session.start("must commit first", agent="agent-a")
        (self.vm_a / "uncommitted.md").write_text("work\n", encoding="utf-8")
        with self.assertRaises(SessionError) as caught:
            session.finish("worked", "tried to push", "none", push=True)
        self.assertIn("uncommitted.md", str(caught.exception))
        # The session is still open, so the record can still be finished honestly.
        self.assertTrue(session.status()["active"])

    def test_finish_without_push_leaves_the_branch_local(self) -> None:
        self.use(self.vm_a)
        from originlib import session

        session.start("no push requested", agent="agent-a")
        result = session.finish("no-change", "kept local", "none")
        self.assertEqual(result["pushed"], "")
        git(self.vm_b, "fetch", "-q", "origin")
        head = git(self.vm_b, "rev-parse", "origin/research/origin")
        self.assertNotIn(result["session"], git(self.vm_b, "ls-tree", "--name-only", head, "sessions/"))


if __name__ == "__main__":
    unittest.main()
