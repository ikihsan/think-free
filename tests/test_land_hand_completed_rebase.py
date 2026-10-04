"""`sync land` used to be the only way a base move was recorded. A reader who
came back from a real conflict to `git rebase --continue` by hand got a tree
whose arrival no event named, and every path the base brought was attributed to
the session that resolved the conflict (defect 2's ceiling).

`recover` closes that: git leaves `ORIG_HEAD` holding the pre-rebase tip and
`git cherry` separates the base's genuinely new commits (`+`) from this
branch's own replayed ones (`-`), so the arrival is recoverable after the
fact. These tests replay the hand-run completion on a two-VM fleet.
"""

from __future__ import annotations

from harness import RepoTest, git, make_fleet

from originlib import landrebase, session, sync, taskops


class HandCompletedRebaseTest(RepoTest):
    def setUp(self) -> None:
        super().setUp()
        self.fleet = make_fleet(self)
        self.seed = self.fleet / "seed"
        self.vm_a = self.fleet / "vm-a"
        self.vm_b = self.fleet / "vm-b"
        self.use(self.seed)
        taskops.create("hand-completed rebase attribution", "true")
        git(self.seed, "add", "-A")
        git(self.seed, "commit", "-qm", "add task")
        git(self.seed, "push", "-q", "origin", "research/origin")
        for clone in (self.vm_a, self.vm_b):
            git(clone, "pull", "-q", "--ff-only")

    def other_vm_advances(self) -> str:
        """VM B adds a commit to the shared base that VM A has not seen."""
        (self.vm_b / "vm-b").mkdir(exist_ok=True)
        (self.vm_b / "vm-b" / "notes.md").write_text("vm b work\n", encoding="utf-8")
        git(self.vm_b, "add", "-A")
        git(self.vm_b, "commit", "-qm", "vm-b: work this session never touched")
        git(self.vm_b, "push", "-q", "origin", "research/origin")
        return git(self.vm_b, "rev-parse", "HEAD")

    def conflict_and_hand_complete(self) -> str:
        """VM A's own commit, a conflicted rebase, and a *hand-run* continue."""
        self.use(self.vm_a)
        git(self.vm_a, "checkout", "-q", "-b", "task/T-0001-vm-a", "origin/research/origin")
        (self.vm_a / "tasks").mkdir(exist_ok=True)
        (self.vm_a / "tasks" / "CLAIMS.jsonl").write_text(
            '{"action": "create", "task": "T-0001"}\n', encoding="utf-8"
        )
        git(self.vm_a, "add", "-A")
        git(self.vm_a, "commit", "-qm", "claim from a")
        (self.vm_b / "tasks").mkdir(exist_ok=True)
        (self.vm_b / "tasks" / "CLAIMS.jsonl").write_text(
            '{"action": "create", "task": "T-0002"}\n', encoding="utf-8"
        )
        git(self.vm_b, "add", "-A")
        git(self.vm_b, "commit", "-qm", "claim from b")
        git(self.vm_b, "push", "-q", "origin", "research/origin")
        git(self.vm_a, "fetch", "-q", "origin")
        # The conflict, reproduced the way land's own tests reproduce it: both
        # VMs appended to the same new file.
        with self.assertRaises(Exception):
            git(self.vm_a, "rebase", "origin/research/origin")
        self.assertTrue(sync.status()["rebase_in_progress"])
        ledger = self.vm_a / "tasks" / "CLAIMS.jsonl"
        lines = [
            line
            for line in ledger.read_text(encoding="utf-8").splitlines()
            if not line.startswith(("<<<<<<<", "=======", ">>>>>>>"))
        ]
        ledger.write_text("\n".join(lines) + "\n", encoding="utf-8")
        git(self.vm_a, "add", "--", "tasks/CLAIMS.jsonl")
        # The human completes it, by hand, without `land` — the case the
        # tooling used to leave with no record at all.
        git(self.vm_a, "-c", "core.editor=true", "rebase", "--continue")
        self.assertFalse(sync.status()["rebase_in_progress"])
        return git(self.vm_b, "rev-parse", "HEAD")

    def test_the_hand_completed_arrival_is_recorded_once(self) -> None:
        self.use(self.vm_a)
        active = session.start("repair the record", agent="tester", task="T-0001")
        arrived_sha = self.conflict_and_hand_complete()
        event = landrebase.recover()
        self.assertIsNotNone(event, "recover found no arrival to record")
        self.assertEqual(event["commits"], [arrived_sha], event["commits"])
        # Idempotent: a second read of the same ORIG_HEAD records nothing new.
        self.assertIsNone(landrebase.recover())
        base_advances = [
            e for e in self.session_events(active.session) if e["kind"] == "base_advance"
        ]
        self.assertEqual(len(base_advances), 1, base_advances)
        self.assertIn("rebase completed outside land", base_advances[0]["data"]["reason"])

    def test_the_arrival_is_attributed_to_the_base_at_finish(self) -> None:
        self.use(self.vm_a)
        active = session.start("repair the record", agent="tester", task="T-0001")
        self.other_vm_advances()
        self.conflict_and_hand_complete()
        session.artifact("tasks/CLAIMS.jsonl")
        git(self.vm_a, "add", "-A")
        git(self.vm_a, "commit", "-qm", "resolve and finish")
        result = session.finish("worked", "resolved the conflict", "none")
        unlogged = [
            e["data"]["path"]
            for e in self.session_events(active.session)
            if e["kind"] == "unlogged_change"
        ]
        self.assertNotIn("vm-b/notes.md", unlogged, unlogged)
        self.assertEqual(unlogged, [], unlogged)
        self.assertIn("vm-b/notes.md", result["landed"], result)

    def test_a_merge_is_not_recovered_as_a_rebase(self) -> None:
        self.use(self.vm_a)
        git(self.vm_a, "checkout", "-q", "-b", "feature", "origin/research/origin")
        (self.vm_a / "own.md").write_text("own\n", encoding="utf-8")
        git(self.vm_a, "add", "-A")
        git(self.vm_a, "commit", "-qm", "own work")
        self.other_vm_advances()
        git(self.vm_a, "fetch", "-q", "origin")
        git(self.vm_a, "merge", "-q", "--no-edit", "origin/research/origin")
        self.assertIsNone(landrebase.recover())

    def test_a_fast_forward_is_not_recovered_as_a_rebase(self) -> None:
        self.use(self.vm_a)
        self.other_vm_advances()
        git(self.vm_a, "fetch", "-q", "origin")
        git(self.vm_a, "merge", "-q", "--ff-only", "origin/research/origin")
        self.assertIsNone(landrebase.recover())
