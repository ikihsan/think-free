"""Moving commits between VMs: fetch, pull, push, land.

The failure this prevents is work that reaches one machine and stops there, or a
land that quietly does something other than what it says. The session-side
boundary tests live in `test_session_flow.py`.
"""

from __future__ import annotations

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

    def test_land_rebases_onto_the_base_and_pushes(self) -> None:
        self.use(self.vm_a)
        git(self.vm_a, "fetch", "-q", "origin")
        git(self.vm_a, "checkout", "-q", "-b", "task/T-0001-vm-a", "origin/research/origin")
        (self.vm_a / "work.md").write_text("mine\n", encoding="utf-8")
        git(self.vm_a, "add", "-A")
        git(self.vm_a, "commit", "-qm", "mine")
        self.commit_on(self.vm_b, "from-b.md", "b\n")
        outcome = syncland.land()
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
        (self.vm_a / "sessions").mkdir(exist_ok=True)
        (self.vm_b / "sessions").mkdir(exist_ok=True)
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
        outcome = syncland.land()
        self.assertTrue(outcome["resolved"])
        self.assertIn("sessions/INDEX.md", " ".join(outcome["resolved"]))
        from originlib import report

        regenerated = report.render_sessions_index()
        self.assertEqual((self.vm_a / "sessions" / "INDEX.md").read_text(encoding="utf-8"), regenerated)

    def test_land_never_opens_an_editor_to_continue_a_rebase(self) -> None:
        """`git rebase --continue` is interactive from git 2.5x; land must not be.

        This is the test that CI could not run: with an editor to open, a VM
        whose stdin is an inherited pipe blocks until the 60 s timeout and a CI
        runner fails the step outright, so `land` refused to land on exactly the
        push every other VM depends on. The sentinel editor records any attempt,
        including one inherited from the caller's own environment.

        On git older than 2.26 `rebase --continue` did not open an editor, so
        this test passes there either way. It is the *modern* git run that is
        the evidence: see the git version this VM reports.
        """
        self.use(self.vm_a)
        git(self.vm_a, "fetch", "-q", "origin")
        git(self.vm_a, "checkout", "-q", "-b", "task/T-0002-vm-a", "origin/research/origin")
        marker = self.vm_a / "editor-was-opened"
        editor = self.vm_a / "sentinel-editor.sh"
        editor.write_text(f"#!/bin/sh\ntouch {marker}\n", encoding="utf-8")
        editor.chmod(0o755)
        for name in ("GIT_EDITOR", "EDITOR", "VISUAL"):
            previous = os.environ.get(name)
            os.environ[name] = str(editor)

            def restore(value=previous, key=name) -> None:
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value

            self.addCleanup(restore)
        for name in ("sessions",):
            (self.vm_a / name).mkdir(exist_ok=True)
            (self.vm_b / name).mkdir(exist_ok=True)
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
        outcome = syncland.land()
        self.assertIn("sessions/INDEX.md", " ".join(outcome["resolved"]))
        self.assertFalse(
            marker.exists(),
            "land let git open an editor to continue the rebase; the continue must be non-interactive",
        )

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
            syncland.land()
        self.assertIn("shared.md", str(caught.exception))
        self.assertIn("mine", (self.vm_a / "shared.md").read_text(encoding="utf-8"))
        # The rebase is left for a human to inspect rather than thrown away.
        self.assertTrue(sync.status()["rebase_in_progress"])
