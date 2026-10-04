<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# Multi-VM coordination

How several machines share this repository safely. The invariant: git is the
only shared state, every task is held by exactly one agent at a time as far as
the remote can tell, and no session starts from stale code or ends with
unpublished record.

## The moving parts

| Piece | Command | Contract |
|---|---|---|
| Claim visibility | `task claim --push` (default when a remote exists) | A claim nobody has fetched is invisible; the push makes it authoritative |
| Takeover | `task claim ID --takeover "reason"` | Replaces a dead holder's claim; the reason is recorded |
| Isolation | `worktree add T-0004` | Each task gets its own directory and branch; gitignored via `.worktrees/`. Refuses a claim held by *another* VM, not this one's |
| Fetch on start | `session start` | Fetches and fast-forwards onto the base; refuses a stale or dirty tree instead of merging |
| Publish on finish | `session finish --push` | Commits the session record, then pushes the branch; refuses if your own uncommitted work would travel silently |
| Sync | `sync status` / `pull` / `push` / `land` | Never forces; `land` rebases the task branch onto the base, refuses a colliding identifier record, then pushes it |

## One task, one holder

`task claim` writes the claim and pushes it atomically. When two machines race,
the second push is rejected by the remote and the loser is told who won. A claim
held in a dirty tree on a dead VM blocks the task; release it with
`task release` or take it over with `--takeover`, never silently.

A claim is a lease, not a lock: it is *in force* until it is released,
completed, or taken over, and `session verify` treats an unfinished session as
in flight only while its claim is in force and younger than 12 hours
(`--lease-hours`, D025). Past that the session is abandoned and fails the gate,
which is how a dead VM is noticed without anyone watching the list.

Because `claim` must be published on top of the base branch, and publishing it
requires HEAD to equal the base, **a claiming VM pushes its session start first**.
An unfinished session on the shared branch is therefore normal, not a defect.

## One task, one directory

Two agents sharing one working tree share one index and one
`sessions/active.json`, which cross-contaminates everything. `worktree add`
creates `.worktrees/<T-0004>/` with its own branch; the main checkout stays on
`research/origin`. Worktrees are removed with `worktree remove` after the
branch is landed.

## Session boundaries

Start: fetch, fast-forward, verify the tree is clean, then record the remote
head the session branched from. If the remote has moved, the session either
fast-forwards or refuses to start — it never merges.

Finish: reconcile the declared artifacts against git, then with `--push` commit
only the session's own files (`sessions/<id>/`, the generated indexes) and push
the branch. Your own changes belong in their own commit with a message that
says what they are; the tooling will not publish them for you, and `--push`
refuses while they sit uncommitted so the record and the work travel together.

## Landing a colleague's work without claiming it

`land` rebases this branch onto the shared base, which drags the other VMs'
commits into this session's diff. Reconciliation would otherwise report those
files as undeclared changes by this session — nine false reports and four false
`doc_update` events in session 029.

So `pull` and `land` record the arrival: a `base_advance` event naming the
commits that came from the base, written after the push so the tree is still
clean when `push` checks it. Reconciliation attributes a path to the base only
when the newest thing to touch it is one of those commits; a path this session
edits afterwards is its own again.

**Use `tools/origin sync land` or `tools/origin sync pull` to move the base.** A
rebase or pull run by hand leaves the same tree and no record, so its paths stay
reported as undeclared. That is the intended direction of failure: an extra
report costs a minute of reading, a wrongly silenced file costs the record.

## One number, one meaning

F, D and T identifiers are allocated from the shared base, never from one VM's
working tree. `task new` and `origin id next` both fetch first, read the numbered
records at `origin/<base>`, and print which record decided the number. **A
collision is still caught before publication, not only prevented**: `land` refuses
to push a tree whose identifier record collides, naming both definitions and
their lines, because a collision is created by the *merge* — each branch is
internally consistent and each VM's own lint sees nothing. `doc lint` rule 7 is
the backstop for a branch pushed by any other route.

`push` and `task claim` are deliberately **not** gated. Refusing them would stop a
VM publishing the session record it needs in order to renumber its way out, which
would hold the defect in place instead of reporting it.

The residual race is two VMs allocating between their own fetches. It is caught by
the push rejection and by the detector, not prevented here, so a collision still
has to be renumbered on the side that has not been pushed. The allocation rule is
in [`../reference/identifier-allocation.md`](../reference/identifier-allocation.md);
the two decisions are D031 and D032 in
[`DECISIONS-PRACTICE.md`](../../DECISIONS-PRACTICE.md) and
[`DECISIONS-GATING.md`](../../DECISIONS-GATING.md).

## Generated-file conflicts

Two sessions can both regenerate `sessions/INDEX.md` or `docs/INDEX.md` with
different content. These are deterministic functions of the tree, so conflicts
between them are resolved by deleting and regenerating — `sync land` does this
automatically rather than leaving an unanswerable conflict.

## Failure handling

- Stale session: `session verify` reports an unfinished session as in flight
  while its claim is live, and as abandoned once the claim is gone, closed, or
  past the lease. Finish it honestly with `session finish --outcome partial`
  before resuming.
- Rejected push: another VM landed first. `sync pull`, re-run verification,
  push again. Do not force.
- Rebase conflict in real content: `sync land` leaves the rebase for a human to
  inspect; the remote is never modified.
- Refusal (`exit 1`): every refusal the fleet flow is meant to produce prints
  one line on stderr, not a traceback. If you see a traceback, that is a bug.

See [`../operations/vm-execution.md`](../operations/vm-execution.md) for the
full machine sequence and [`../reference/cli-reference.md`](../reference/cli-reference.md)
for the commands.
