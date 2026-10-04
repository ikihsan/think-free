"""Moving commits between VMs: fetch, pull, push, land.

The failure this prevents is work that reaches one machine and stops there, or a
land that quietly does something other than what it says. The session-side
boundary tests live in `test_session_flow.py`.
"""

from __future__ import annotations

import unittest
import json
import os

from harness import RepoTest, git, make_fleet

from originlib import sync, syncland
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


if __name__ == "__main__":
    unittest.main()
