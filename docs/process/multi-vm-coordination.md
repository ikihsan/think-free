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
| Isolation | `worktree add T-0004` | Each task gets its own directory and branch; gitignored via `.worktrees/` |
| Fetch on start | `session start` | Fetches and fast-forwards onto the base; refuses a stale or dirty tree instead of merging |
| Publish on finish | `session finish --push` | Commits the session record, then pushes the branch; refuses if your own uncommitted work would travel silently |
| Sync | `sync status` / `pull` / `push` / `land` | Never forces; `land` rebases the task branch onto the base and pushes it |

## One task, one holder

`task claim` writes the claim and pushes it atomically. When two machines race,
the second push is rejected by the remote and the loser is told who won. A claim
held in a dirty tree on a dead VM blocks the task; release it with
`task release` or take it over with `--takeover`, never silently.

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

## Generated-file conflicts

Two sessions can both regenerate `sessions/INDEX.md` or `docs/INDEX.md` with
different content. These are deterministic functions of the tree, so conflicts
between them are resolved by deleting and regenerating — `sync land` does this
automatically rather than leaving an unanswerable conflict.

## Failure handling

- Stale session: `session verify` reports unfinished sessions; finish them
  honestly with `session finish --outcome partial` before resuming.
- Rejected push: another VM landed first. `sync pull`, re-run verification,
  push again. Do not force.
- Rebase conflict in real content: `sync land` leaves the rebase for a human to
  inspect; the remote is never modified.

See [`../operations/vm-execution.md`](../operations/vm-execution.md) for the
full machine sequence and [`../reference/cli-reference.md`](../reference/cli-reference.md)
for the commands.
