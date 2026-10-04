"""`task claim` from inside an open session.

The claim is the fleet's only concurrency control, and it is published by the
command that writes it. So the tree has to be publishable at the moment the claim
is made, and an open session guarantees it is not: `session start` writes
`sessions/INDEX.md` and a session directory, and every later event dirties them
again. `sync.push` refuses a dirty tree, so `taskremote.claim` committed the claim
and then refused to push it, naming the session's own record among the dirty paths
(defect 21, T-0055).

The consequence is not the exit code. The claim commit stayed local and unpushed,
so no other VM could see it and the exclusivity the claim exists to provide was
not in force; each retry appended another line to the append-only ledger; and the
refusal's own remedy — commit or revert the named paths — is the one action an
agent must not take by hand on its own record. Session 038 hit this on the shared
base: three refusals, three identical `claim` lines for T-0053.

Properties this file holds, each a test:

* a claim made with a session open reaches the remote base in one command
  (`test_a_claim_publishes_while_a_session_is_open`);
* uncommitted work that is **not** the session's own record is still refused, and
  a refused claim appends nothing to the ledger
  (`test_a_claim_is_still_refused_on_foreign_uncommitted_work`).
"""

from __future__ import annotations

from harness import RepoTest, git, make_fleet

from originlib import gitutil


class ClaimInSessionTest(RepoTest):
    def setUp(self) -> None:
        super().setUp()
        self.fleet = make_fleet(self, vm_names=("vm-a",))
        self.vm_a = self.fleet / "vm-a"
        self.use(self.vm_a)
        self.seed_task()

    def seed_task(self) -> None:
        """One open task on the shared base, published the way the protocol says."""
        self.assertEqual(
            self.cli("task", "new", "--goal", "claim it", "--verify", "true"), 0, self.errors()
        )
        git(self.vm_a, "add", "-A")
        git(self.vm_a, "commit", "-qm", "task: create T-0001")
        git(self.vm_a, "push", "-q", "origin", "research/origin")
        git(self.vm_a, "fetch", "-q", "origin")

    def ledger_at_remote(self) -> str:
        return git(self.vm_a, "show", "origin/research/origin:tasks/CLAIMS.jsonl")

    def open_session(self) -> None:
        self.assertEqual(self.cli("session", "start", "--goal", "claim a task"), 0, self.errors())

    def test_a_claim_publishes_while_a_session_is_open(self) -> None:
        """The defect's own shape: the session record is dirty, and the claim lands."""
        self.open_session()
        # The precondition is the thing that broke it: `session start` leaves the
        # tree dirty in exactly the paths the push used to refuse on.
        dirty = gitutil.dirty_paths()
        self.assertTrue(
            [p for p in dirty if p.startswith("sessions/")],
            f"expected a dirty session record, got {dirty}",
        )

        self.assertEqual(
            self.cli("task", "claim", "T-0001", "--agent", "vm-a", "--vm", "vm-a"),
            0,
            self.errors(),
        )

        # Published, not merely committed: the remote is the authority, so a
        # claim only exists if the remote holds it.
        self.assertIn('"task": "T-0001"', self.ledger_at_remote())
        status = git(
            self.vm_a,
            "show",
            "origin/research/origin:tasks/T-0001-claim-it.md",
        )
        self.assertIn("status: claimed", status)
        self.assertEqual(
            git(self.vm_a, "rev-parse", "HEAD"),
            git(self.vm_a, "rev-parse", "origin/research/origin"),
        )

    def test_a_claim_is_still_refused_on_foreign_uncommitted_work(self) -> None:
        """The control. The session's own record is not a blank cheque for the tree."""
        self.open_session()
        (self.vm_a / "work.md").write_text("uncommitted work\n", encoding="utf-8")

        before = self.ledger_at_remote()
        self.assertEqual(
            self.cli("task", "claim", "T-0001", "--agent", "vm-a", "--vm", "vm-a"), 1
        )
        refusal = self.errors()
        self.assertIn("work.md", refusal)
        self.assertNotIn("sessions/", refusal)
        # A refused claim must leave no trace in the append-only ledger, and must
        # not leave the branch one commit ahead of the base: both were observed on
        # the shared base as three identical `claim` lines and one stuck commit.
        self.assertEqual(self.ledger_at_remote(), before)
        self.assertEqual(
            git(self.vm_a, "rev-list", "--count", "origin/research/origin..HEAD"), "0"
        )