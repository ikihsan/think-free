"""Session boundaries in a fleet: fetch on the way in, push on the way out.

The failure this prevents is a VM that starts from a stale tree, or finishes a
session whose record never leaves the machine, so the next VM reads a history
that does not contain the work.
"""

from __future__ import annotations

import unittest

from harness import RepoTest, git, make_fleet

from originlib import sync
from originlib.activestate import SessionError
from originlib.sync import SyncError


class SyncTest(RepoTest):
    def setUp(self) -> None:
        super().setUp()
        self.fleet = make_fleet(self)
        self.vm_a = self.fleet / "vm-a"
        self.vm_b = self.fleet / "vm-b"

    def commit_on(self, clone, name: str, content: str) -> None:
        (clone / name).write_text(content, encoding="utf-8")
        git(clone, "add", "-A")
        git(clone, "commit", "-qm", f"add {name}")
        git(clone, "push", "-q", "origin", "research/origin")

    def test_status_reports_divergence_from_the_remote(self) -> None:
        self.use(self.vm_a)
        self.commit_on(self.vm_b, "from-b.md", "b\n")
        report = sync.status()
        self.assertEqual(report["behind"], 1)
        self.assertEqual(report["ahead"], 0)
        self.assertEqual(report["remote"], "origin")

    def test_pull_fast_forwards_the_base_branch(self) -> None:
        self.use(self.vm_a)
        self.commit_on(self.vm_b, "from-b.md", "b\n")
        outcome = sync.pull()
        self.assertEqual(outcome["behind_before"], 1)
        self.assertTrue(outcome["fast_forwarded"])
        self.assertEqual(
            git(self.vm_a, "rev-parse", "HEAD"), git(self.vm_b, "rev-parse", "HEAD")
        )

    def test_pull_is_a_no_op_when_already_current(self) -> None:
        self.use(self.vm_a)
        outcome = sync.pull()
        self.assertEqual(outcome["behind_before"], 0)
        self.assertFalse(outcome["fast_forwarded"])

    def test_pull_refuses_a_dirty_tree(self) -> None:
        self.use(self.vm_a)
        (self.vm_a / "dirty.md").write_text("uncommitted\n", encoding="utf-8")
        self.commit_on(self.vm_b, "from-b.md", "b\n")
        with self.assertRaises(SyncError) as caught:
            sync.pull()
        self.assertIn("dirty.md", str(caught.exception))

    def test_pull_refuses_when_local_commits_would_be_lost(self) -> None:
        self.use(self.vm_a)
        self.commit_on(self.vm_b, "from-b.md", "b\n")
        (self.vm_a / "local.md").write_text("local\n", encoding="utf-8")
        git(self.vm_a, "add", "-A")
        git(self.vm_a, "commit", "-qm", "local work")
        with self.assertRaises(SyncError) as caught:
            sync.pull()
        self.assertIn("sync land", str(caught.exception))

    def test_push_publishes_the_current_branch(self) -> None:
        self.use(self.vm_a)
        git(self.vm_a, "checkout", "-q", "-b", "task/T-0001-vm-a")
        (self.vm_a / "work.md").write_text("done\n", encoding="utf-8")
        git(self.vm_a, "add", "-A")
        git(self.vm_a, "commit", "-qm", "work")
        outcome = sync.push()
        self.assertTrue(outcome["pushed"])
        self.assertEqual(
            git(self.vm_a, "rev-parse", "refs/remotes/origin/task/T-0001-vm-a"),
            git(self.vm_a, "rev-parse", "HEAD"),
        )

    def test_push_never_forces(self) -> None:
        self.use(self.vm_a)
        git(self.vm_a, "checkout", "-q", "-b", "task/T-0001-vm-a")
        (self.vm_a / "work.md").write_text("mine\n", encoding="utf-8")
        git(self.vm_a, "add", "-A")
        git(self.vm_a, "commit", "-qm", "mine")
        # Another VM publishes to the same branch name first.
        git(self.vm_b, "fetch", "-q", "origin")
        git(self.vm_b, "checkout", "-q", "-b", "task/T-0001-vm-a", "origin/research/origin")
        (self.vm_b / "work.md").write_text("theirs\n", encoding="utf-8")
        git(self.vm_b, "add", "-A")
        git(self.vm_b, "commit", "-qm", "theirs")
        git(self.vm_b, "push", "-q", "origin", "task/T-0001-vm-a")
        with self.assertRaises(SyncError) as caught:
            sync.push()
        self.assertIn("non-fast-forward", str(caught.exception))
        # The rejected push changed nothing on the remote.
        self.assertEqual(
            git(self.vm_a, "ls-remote", "origin", "refs/heads/task/T-0001-vm-a").split()[0],
            git(self.vm_b, "rev-parse", "HEAD"),
        )

    def test_land_rebases_onto_the_base_and_pushes(self) -> None:
        self.use(self.vm_a)
        git(self.vm_a, "fetch", "-q", "origin")
        git(self.vm_a, "checkout", "-q", "-b", "task/T-0001-vm-a", "origin/research/origin")
        (self.vm_a / "work.md").write_text("mine\n", encoding="utf-8")
        git(self.vm_a, "add", "-A")
        git(self.vm_a, "commit", "-qm", "mine")
        self.commit_on(self.vm_b, "from-b.md", "b\n")
        outcome = sync.land()
        self.assertTrue(outcome["pushed"])
        self.assertEqual(
            git(self.vm_a, "rev-parse", "origin/research/origin"),
            git(self.vm_a, "rev-parse", "HEAD"),
        )
        self.assertTrue((self.vm_a / "from-b.md").exists())

    def test_land_resolves_generated_index_conflicts_by_regenerating(self) -> None:
        self.use(self.vm_a)
        git(self.vm_a, "fetch", "-q", "origin")
        git(self.vm_a, "checkout", "-q", "-b", "task/T-0001-vm-a", "origin/research/origin")
        # Both VMs regenerate the same generated file with different content,
        # which is what two concurrent sessions actually produce.
        (self.vm_a / "sessions" / "INDEX.md").write_text(
            "# Sessions index\n\n<!-- origin-meta\nowner: docs/INDEX.md\nstatus: active\nlast-verified: 2026-10-03\n-->\n\nfrom a\n",
            encoding="utf-8",
        )
        git(self.vm_a, "add", "-A")
        git(self.vm_a, "commit", "-qm", "regenerate index on a")
        git(self.vm_b, "pull", "-q", "--ff-only")
        (self.vm_b / "sessions" / "INDEX.md").write_text(
            "# Sessions index\n\n<!-- origin-meta\nowner: docs/INDEX.md\nstatus: active\nlast-verified: 2026-10-03\n-->\n\nfrom b\n",
            encoding="utf-8",
        )
        git(self.vm_b, "add", "-A")
        git(self.vm_b, "commit", "-qm", "regenerate index on b")
        git(self.vm_b, "push", "-q", "origin", "research/origin")
        outcome = sync.land()
        self.assertTrue(outcome["resolved"])
        self.assertIn("sessions/INDEX.md", " ".join(outcome["resolved"]))
        from originlib import report

        regenerated = report.render_sessions_index()
        self.assertEqual((self.vm_a / "sessions" / "INDEX.md").read_text(encoding="utf-8"), regenerated)

    def test_land_reports_a_real_content_conflict_and_keeps_the_work(self) -> None:
        self.use(self.vm_a)
        git(self.vm_a, "fetch", "-q", "origin")
        git(self.vm_a, "checkout", "-q", "-b", "task/T-0001-vm-a", "origin/research/origin")
        (self.vm_a / "shared.md").write_text("mine\n", encoding="utf-8")
        git(self.vm_a, "add", "-A")
        git(self.vm_a, "commit", "-qm", "mine")
        (self.vm_b / "shared.md").write_text("theirs\n", encoding="utf-8")
        git(self.vm_b, "add", "-A")
        git(self.vm_b, "commit", "-qm", "theirs")
        git(self.vm_b, "push", "-q", "origin", "research/origin")
        with self.assertRaises(SyncError) as caught:
            sync.land()
        self.assertIn("shared.md", str(caught.exception))
        self.assertIn("mine", (self.vm_a / "shared.md").read_text(encoding="utf-8"))
        # The rebase is left for a human to inspect rather than thrown away.
        self.assertTrue(sync.status()["rebase_in_progress"])


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
