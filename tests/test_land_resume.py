"""`sync land` finishes a rebase it stopped on, once the conflict is resolved.

Split out of `test_land.py` on 2026-10-04 (T-0048) at the line cap, and by
invariant: `test_land` holds what `land` does to a rebase it starts, and this
file holds what it does to a rebase it already stopped.

The defect is in the refusal message rather than in the code. `land` stops on a
real content conflict in `tasks/CLAIMS.jsonl` — the normal case whenever two VMs
append a claim in the same hour — and tells the reader to *resolve it and land
again*. The second `land` cannot do that: it refuses on a dirty tree, and
resolving the conflict is what makes the tree dirty. So the only way out is
`git rebase --continue` by hand, which records no `base_advance`, and every path
the base brought is then attributed to the session that resolved the conflict.
That is defect 2's stated ceiling, reached through the tool's own instruction
instead of by a mistake.

Both halves are falsifiable against the unmodified code. Without the resume, the
second `land` raises the dirty-tree refusal and nothing is published; and without
the pre-rebase tip read from git's own `orig-head`, the arrival is recorded
against a `HEAD` that has already moved onto the base, which is how a session
inherits a colleague's files as its own.
"""

from __future__ import annotations

import os

from harness import RepoTest, git, make_fleet

from originlib import sync, syncland
from originlib.sync import SyncError


class ResumeTest(RepoTest):
    def setUp(self) -> None:
        super().setUp()
        self.fleet = make_fleet(self)
        self.vm_a = self.fleet / "vm-a"
        self.vm_b = self.fleet / "vm-b"

    def stop_on_a_ledger_conflict(self) -> str:
        """Two VMs append to `tasks/CLAIMS.jsonl`; leave vm-a mid-rebase."""
        git(self.vm_a, "fetch", "-q", "origin")
        git(self.vm_a, "checkout", "-q", "-b", "task/T-0001-vm-a", "origin/research/origin")
        (self.vm_a / "tasks").mkdir(exist_ok=True)
        (self.vm_a / "tasks" / "CLAIMS.jsonl").write_text(
            '{"action": "create", "schema": "origin.task.claim/1", "task": "T-0001", '
            '"ts": "2026-10-04T10:00:00+00:00"}\n',
            encoding="utf-8",
        )
        git(self.vm_a, "add", "-A")
        git(self.vm_a, "commit", "-qm", "claim from a")
        (self.vm_b / "tasks").mkdir(exist_ok=True)
        (self.vm_b / "tasks" / "CLAIMS.jsonl").write_text(
            '{"action": "create", "schema": "origin.task.claim/1", "task": "T-0002", '
            '"ts": "2026-10-04T10:00:01+00:00"}\n',
            encoding="utf-8",
        )
        git(self.vm_b, "add", "-A")
        git(self.vm_b, "commit", "-qm", "claim from b")
        git(self.vm_b, "push", "-q", "origin", "research/origin")
        return self.land_and_fail()

    def land_and_fail(self) -> str:
        self.use(self.vm_a)
        with self.assertRaises(SyncError) as caught:
            syncland.land()
        message = str(caught.exception)
        self.assertIn("tasks/CLAIMS.jsonl", message)
        self.assertIn("land again", message)
        self.assertTrue(sync.status()["rebase_in_progress"])
        return message

    def resolve_keeping_both_lines(self) -> None:
        """What [`multi-vm-coordination.md`](docs) tells the reader to do."""
        ledger = self.vm_a / "tasks" / "CLAIMS.jsonl"
        kept = [
            line for line in ledger.read_text(encoding="utf-8").splitlines()
            if not line.startswith(("<<<<<<<", "=======", ">>>>>>>"))
        ]
        self.assertEqual(len(kept), 2, kept)
        ledger.write_text("\n".join(kept) + "\n", encoding="utf-8")
        git(self.vm_a, "add", "--", "tasks/CLAIMS.jsonl")

    def test_its_own_instruction_is_followable_once_the_conflict_is_resolved(self) -> None:
        self.stop_on_a_ledger_conflict()
        self.resolve_keeping_both_lines()
        outcome = syncland.land()
        self.assertTrue(outcome["resumed"], outcome)
        self.assertTrue(outcome["pushed"])
        self.assertEqual(
            git(self.vm_a, "rev-parse", "origin/research/origin"),
            git(self.vm_a, "rev-parse", "HEAD"),
        )
        self.assertFalse(sync.status()["rebase_in_progress"])
        # Both claims survive: the ledger is a sequence of events, so the union is
        # correct and only the order was in question.
        ledger = (self.vm_a / "tasks" / "CLAIMS.jsonl").read_text(encoding="utf-8")
        self.assertIn("T-0001", ledger)
        self.assertIn("T-0002", ledger)
        self.assertNotIn("<<<<<<<", ledger)

    def test_a_conflict_still_unresolved_is_still_refused_with_the_same_words(self) -> None:
        # The reader runs `land` again before touching anything, which is the
        # obvious thing to do and used to be indistinguishable from the case it
        # now handles. The refusal must still be the conflict one, not the
        # dirty-tree one and not a silent continuation.
        self.stop_on_a_ledger_conflict()
        with self.assertRaises(SyncError) as caught:
            syncland.land()
        self.assertIn("rebase stopped on a real content conflict", str(caught.exception))
        self.assertIn("resolve it", str(caught.exception))
        self.assertTrue(sync.status()["rebase_in_progress"])

    def test_the_arrival_is_recorded_against_the_pre_rebase_tip(self) -> None:
        # The half of defect 2 a tooling-performed continuation can still close.
        # Mid-rebase `HEAD` is the base with this branch's earlier commits on it,
        # so `before..base` read from `HEAD` would name nothing and every arriving
        # path would look like this session's own change.
        self.stop_on_a_ledger_conflict()
        self.resolve_keeping_both_lines()
        recorded: list[dict] = []
        original = syncland.record_arrival

        def capture(action, before, after, root=None, arrived=None):
            recorded.append({"before": before, "after": after, "arrived": list(arrived or [])})
            return original(action, before, after, root=root, arrived=arrived)

        syncland.record_arrival = capture
        self.addCleanup(setattr, syncland, "record_arrival", original)
        syncland.land()
        self.assertEqual(len(recorded), 1, recorded)
        self.assertTrue(recorded[0]["arrived"], "no arrival recorded for a resumed rebase")
        arrival = git(self.vm_a, "log", "--no-patch", "--format=%s", recorded[0]["arrived"][0])
        self.assertIn("claim from b", arrival)

    def test_it_never_opens_an_editor_to_finish_one(self) -> None:
        # The same obligation the generated-file continuation has, reached from a
        # different state. `git rebase --continue` opens an editor for the commit
        # message on git 2.26 and later, so a sentinel editor is the only thing
        # that can see it happen.
        self.stop_on_a_ledger_conflict()
        self.resolve_keeping_both_lines()
        # Outside the clone, because the continuation refuses a dirty-and-unstaged
        # path rather than sweeping it into the rebase's commit, and a sentinel
        # left in the working tree would be exactly that.
        marker = self.fleet / "editor-was-opened"
        editor = self.fleet / "sentinel-editor.sh"
        editor.write_text(f"#!/bin/sh\ntouch {marker}\n", encoding="utf-8")
        editor.chmod(0o755)
        for name in ("GIT_EDITOR", "EDITOR", "VISUAL"):
            previous = os.environ.get(name)
            os.environ[name] = str(editor)
            if previous is None:
                self.addCleanup(os.environ.pop, name, None)
            else:
                self.addCleanup(os.environ.__setitem__, name, previous)
        syncland.land()
        self.assertFalse(marker.exists(), "land let git open an editor to resume a rebase")