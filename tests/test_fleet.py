"""Two VMs, one remote: claims must be exclusive and work must be isolated.

Every test here builds a bare repository and two clones of it, so the git
behaviour under test is the real one: fetch, fast-forward, non-fast-forward
push rejection. No network, no mocks.
"""

from __future__ import annotations

import unittest
from pathlib import Path

from harness import RepoTest, git, make_fleet

from originlib import session, taskops, taskremote, tasks, worktree
from originlib.tasks import TaskError
from originlib.worktree import WorktreeError


class FleetTest(RepoTest):
    def setUp(self) -> None:
        super().setUp()
        self.fleet = make_fleet(self)
        self.seed = self.fleet / "seed"
        self.vm_a = self.fleet / "vm-a"
        self.vm_b = self.fleet / "vm-b"
        self.use(self.seed)
        taskops.create("contended task", "true")
        git(self.seed, "add", "-A")
        git(self.seed, "commit", "-qm", "add task")
        git(self.seed, "push", "-q", "origin", "research/origin")
        # A real VM syncs before it reads the task list; the clones were made
        # before the task existed.
        for clone in (self.vm_a, self.vm_b):
            git(clone, "pull", "-q", "--ff-only")

    def head_of(self, clone: Path, ref: str = "HEAD") -> str:
        return git(clone, "rev-parse", ref)

    def branch_of(self, clone: Path) -> str:
        return git(clone, "rev-parse", "--abbrev-ref", "HEAD")


class RemoteTruthClaimTest(FleetTest):
    def test_claim_pushes_and_is_visible_to_the_other_vm(self) -> None:
        self.use(self.vm_a)
        taskremote.claim("T-0001", agent="agent-a", vm="vm-a")
        self.use(self.vm_b)
        # `holder` fetches, because a claim nobody has fetched is invisible.
        self.assertEqual(taskremote.holder("T-0001").get("agent"), "agent-a")
        self.assertEqual(taskremote.holder("T-0001").get("vm"), "vm-a")

    def test_second_vm_is_refused_and_learns_who_won(self) -> None:
        self.use(self.vm_a)
        taskremote.claim("T-0001", agent="agent-a", vm="vm-a")
        self.use(self.vm_b)
        with self.assertRaises(TaskError) as caught:
            taskremote.claim("T-0001", agent="agent-b", vm="vm-b")
        message = str(caught.exception)
        self.assertIn("agent-a", message)
        self.assertIn("vm-a", message)

    def test_losing_vm_leaves_no_claim_commit(self) -> None:
        self.use(self.vm_a)
        taskremote.claim("T-0001", agent="agent-a", vm="vm-a")
        self.use(self.vm_b)
        with self.assertRaises(TaskError):
            taskremote.claim("T-0001", agent="agent-b", vm="vm-b")
        log = git(self.vm_b, "log", "--oneline", "-5")
        self.assertNotIn("by agent-b", log)

    def test_unpushed_local_claim_does_not_lock_the_task(self) -> None:
        # This is why a claim must be pushed: a local-only claim is invisible
        # to every other VM, so it protects nothing.
        self.use(self.vm_a)
        taskops.claim("T-0001", agent="agent-a", vm="vm-a")
        self.use(self.vm_b)
        claimed = taskremote.claim("T-0001", agent="agent-b", vm="vm-b")
        self.assertEqual(claimed.meta["claim-agent"], "agent-b")

    def test_claim_requires_a_branch_at_the_remote_base(self) -> None:
        self.use(self.vm_a)
        git(self.vm_a, "checkout", "-q", "-b", "side")
        self.write_on(self.vm_a, "notes.md", "work in progress\n")
        git(self.vm_a, "add", "-A")
        git(self.vm_a, "commit", "-qm", "unrelated work")
        with self.assertRaises(TaskError) as caught:
            taskremote.claim("T-0001", agent="agent-a", vm="vm-a")
        self.assertIn("sync", str(caught.exception).lower())

    def test_takeover_requires_a_reason_and_is_recorded(self) -> None:
        self.use(self.vm_a)
        taskremote.claim("T-0001", agent="agent-a", vm="vm-a")
        self.use(self.vm_b)
        with self.assertRaises(TaskError):
            taskremote.claim("T-0001", agent="agent-b", vm="vm-b", takeover="")
        taken = taskremote.claim("T-0001", agent="agent-b", vm="vm-b", takeover="vm-a is gone")
        self.assertEqual(taken.meta["claim-agent"], "agent-b")
        ledger = taskremote.remote_claims("origin/research/origin")
        self.assertTrue(any(e.get("action") == "takeover" for e in ledger))

    def test_release_makes_the_task_available_again(self) -> None:
        self.use(self.vm_a)
        taskremote.claim("T-0001", agent="agent-a", vm="vm-a")
        taskremote.release("T-0001", agent="agent-a", vm="vm-a")
        self.use(self.vm_b)
        again = taskremote.claim("T-0001", agent="agent-b", vm="vm-b")
        self.assertEqual(again.meta["claim-agent"], "agent-b")

    def write_on(self, clone: Path, relative: str, content: str) -> None:
        path = clone / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


class ClaimUnderOpenSessionExclusionTest(FleetTest):
    """Exclusivity and an open session, in the order the protocol documents them.

    Two separate properties, each covered on its own after T-0055 and neither of
    them covering the other: `tests/test_claim_in_session.py` proves a claim made
    with a session open reaches the remote, and `RemoteTruthClaimTest` above proves
    a published claim excludes the other VM — but with no session open in either.
    The composition is the one the fleet actually runs, because `session start` must
    precede `task claim` for the claim to be publishable at all. It is also the
    composition the defect lived in: a claim that could not be published protected
    nothing, so "it is published" and "it excludes" have to hold together or the
    first is not the property anyone wanted.
    """

    def test_a_claim_made_under_a_session_still_excludes_the_other_vm(self) -> None:
        self.use(self.vm_a)
        active = session.start("claim it for real", agent="agent-a", sync_remote=False)
        taskremote.claim("T-0001", agent="agent-a", vm="vm-a", session=active.session)

        self.use(self.vm_b)
        git(self.vm_b, "fetch", "-q")
        with self.assertRaises(TaskError) as caught:
            taskremote.claim("T-0001", agent="agent-b", vm="vm-b")
        self.assertIn("agent-a", str(caught.exception))
        self.assertIn("vm-a", str(caught.exception))


class RemoteListingTest(FleetTest):
    def test_list_remote_shows_claims_made_elsewhere(self) -> None:
        self.use(self.vm_a)
        taskremote.claim("T-0001", agent="agent-a", vm="vm-a")
        self.use(self.vm_b)
        self.assertIn("agent-a", taskremote.render_remote_list(""))

    def test_remote_list_shows_a_task_pushed_by_another_vm(self) -> None:
        self.use(self.vm_a)
        (self.vm_a / "tasks" / "T-0009-only-here.md").write_text(
            "<!-- task-meta\nid: T-0009\nstatus: open\ncreated: 2026-10-03\nverify: true\n-->\n",
            encoding="utf-8",
        )
        git(self.vm_a, "add", "-A")
        git(self.vm_a, "commit", "-qm", "add task from a")
        git(self.vm_a, "push", "-q", "origin", "research/origin")
        self.use(self.vm_b)
        self.assertIn("T-0009", taskremote.render_remote_list(""))


class WorktreeIsolationTest(FleetTest):
    def test_add_creates_a_branch_and_a_directory(self) -> None:
        self.use(self.vm_a)
        info = worktree.add("T-0001", vm="vm-a")
        self.assertTrue(info.path.is_dir())
        self.assertEqual(info.branch, "task/T-0001-vm-a")
        self.assertEqual(git(info.path, "rev-parse", "--abbrev-ref", "HEAD"), "task/T-0001-vm-a")

    def test_worktree_directory_is_gitignored(self) -> None:
        self.use(self.vm_a)
        info = worktree.add("T-0001", vm="vm-a")
        result = git(self.vm_a, "check-ignore", "-q", str(info.path))
        # check-ignore exits 0 when ignored; git() raises otherwise, so a clean
        # return proves the worktree cannot be committed by accident.
        self.assertTrue(result == "")

    def test_worktree_starts_from_the_remote_base(self) -> None:
        self.use(self.vm_a)
        info = worktree.add("T-0001", vm="vm-a")
        self.assertEqual(
            self.head_of(info.path), git(self.vm_a, "rev-parse", "origin/research/origin")
        )

    def test_second_worktree_for_the_same_task_on_one_vm_is_refused(self) -> None:
        self.use(self.vm_a)
        worktree.add("T-0001", vm="vm-a")
        with self.assertRaises(WorktreeError):
            worktree.add("T-0001", vm="vm-a")

    def test_worktree_refused_when_another_vm_holds_the_claim(self) -> None:
        self.use(self.vm_a)
        taskremote.claim("T-0001", agent="agent-a", vm="vm-a")
        self.use(self.vm_b)
        with self.assertRaises(WorktreeError) as caught:
            worktree.add("T-0001", vm="vm-b")
        self.assertIn("agent-a", str(caught.exception))

    def test_worktree_allowed_after_this_vm_claimed_the_task(self) -> None:
        # docs/operations/vm-execution.md sequences claim before worktree add,
        # so refusing our own claim made the documented flow impossible (F012).
        self.use(self.vm_a)
        taskremote.claim("T-0001", agent="agent-a", vm="vm-a")
        info = worktree.add("T-0001", vm="vm-a")
        self.assertTrue(info.path.is_dir())

    def test_worktree_refused_when_the_claim_records_no_vm(self) -> None:
        # An unattributable claim cannot be shown to be ours.
        self.use(self.vm_a)
        taskremote.claim("T-0001", agent="agent-a", vm="")
        with self.assertRaises(WorktreeError):
            worktree.add("T-0001", vm="vm-a")

    def test_a_refusal_exits_one_without_a_traceback(self) -> None:
        # A refusal the flow is meant to produce is not a crash (F012).
        self.use(self.vm_a)
        taskremote.claim("T-0001", agent="agent-a", vm="vm-a")
        self.use(self.vm_b)
        self.assertEqual(self.cli("worktree", "add", "T-0001", "--vm", "vm-b"), 1)
        self.assertNotIn("Traceback", self.errors())
        self.assertIn("agent-a", self.errors())

    def test_two_vms_get_separate_directories_for_one_task(self) -> None:
        self.use(self.vm_a)
        first = worktree.add("T-0001", vm="vm-a")
        self.use(self.vm_b)
        second = worktree.add("T-0001", vm="vm-b")
        self.assertNotEqual(first.path, second.path)
        self.assertNotEqual(first.branch, second.branch)

    def test_list_reports_registered_worktrees(self) -> None:
        self.use(self.vm_a)
        worktree.add("T-0001", vm="vm-a")
        rows = worktree.list_worktrees()
        self.assertTrue(any(row.branch == "task/T-0001-vm-a" for row in rows))

    def test_remove_refuses_a_dirty_worktree(self) -> None:
        self.use(self.vm_a)
        info = worktree.add("T-0001", vm="vm-a")
        (info.path / "scratch.md").write_text("work\n", encoding="utf-8")
        with self.assertRaises(WorktreeError):
            worktree.remove(info.path)
        worktree.remove(info.path, force=True)
        self.assertFalse(info.path.exists())

    def test_remove_rejects_a_path_outside_the_worktree_root(self) -> None:
        self.use(self.vm_a)
        with self.assertRaises(WorktreeError):
            worktree.remove(Path("/tmp"))


class LocalOnlyClaimRegressionTest(RepoTest):
    def test_local_claim_still_works_without_a_remote(self) -> None:
        taskops.create("offline task", "true")
        claimed = taskops.claim("T-0001", agent="agent-a", vm="vm-a")
        self.assertEqual(claimed.status, "claimed")
        self.assertEqual(tasks.active_claims()["T-0001"]["agent"], "agent-a")


if __name__ == "__main__":
    unittest.main()
