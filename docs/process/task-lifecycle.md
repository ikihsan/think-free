<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# Task lifecycle

A task is a unit of work another machine can pick up without asking a question.
It is a Markdown file with a runnable verification command, so completion is
decided by evidence rather than by an agent's confidence.

Skill: [`task-execution`](../../.agents/skills/task-execution/SKILL.md).
Map: [`tasks/INDEX.md`](../../tasks/INDEX.md).

## The shared-state model

Git is the only shared state. There is no database and no coordination service.

| State | Where | Merge behaviour |
|---|---|---|
| Task definition | `tasks/T-NNNN-slug.md` | Normal merge; one file per task |
| Claim history | `tasks/CLAIMS.jsonl` | Append-only; two agents appending different lines merge cleanly |
| Progress | `sessions/<id>/` | One directory per session; no overlap |
| Generated map | `tasks/INDEX.md` | Regenerated; may need rebuilding after a merge |

This is deliberate. It means the system works before any infrastructure exists,
works offline, and leaves a history that survives the loss of the machine that
produced it. The cost is that a stale claim is possible, which is handled
politely rather than technically — see *Stale claims* below.

## Writing a task

```bash
tools/origin task new \
  --goal "one imperative sentence" \
  --verify "tools/origin doc lint" \
  --rationale "why this matters now" \
  --preconditions "what must be true first" \
  --steps "1. …" \
  --acceptance "- [ ] …" \
  --rollback "how to undo a bad outcome"
```

**The number comes from the shared base, and the command says so.**

```
created T-0032  T-0032-do-the-thing.md
  number allocated from: origin/research/origin@d1ffad0 and this working tree (highest T-0031)
```

`task new` fetches first and reads the task files *and* `tasks/CLAIMS.jsonl` at
`origin/<base>`, then takes one above the highest number either side defines. It
used to list this VM's `tasks/` directory and add one, which is how two VMs took
the same number twelve times in two days: a working tree is one VM's opinion of
the task list and nothing recorded how old that opinion was. Read the line
printed above `verify:` — it is the record of which copy of the ledger decided
the number, and it is the only place that answer exists.

Two states are worth reading carefully, because they are not the same claim:

| Line | What it means | What to do |
|---|---|---|
| `…@<sha> and this working tree` | The base was read and is current | Nothing |
| `…, last seen before a fetch failed (…)` | The last snapshot is being used; it may already be stale | Push and check before relying on the number |
| `this working tree only (…)` | No base, or none readable | The number is this VM's opinion. Land your work, then re-read |

The residual race is stated in [`../reference/identifier-allocation.md`](../reference/identifier-allocation.md):
two VMs that allocate between their own fetches still collide, and the detector
that refuses such a commit is T-0030. A finding or a decision number is
allocated the same way, by hand or by command:

```bash
tools/origin id next F        # also D and T; --json prints every number read
```

The `--verify` command is the important field. It must:

- exit non-zero when the work is not done;
- be a single command, runnable from the repository root;
- include everything the acceptance criteria require, not just the easy part;
- not require the machine that has no access to the result.

A task whose verification cannot fail is worse than no task, because it produces
false completion signals at scale.

**Creating a task also rebuilds the indexes.** `task new`, `task claim`,
`task complete` and `task release` rewrite `tasks/INDEX.md` and `docs/INDEX.md`,
because a task file is a document and `doc lint` calls an unlinked document an
orphan. Skipping that step is not a faster route to a green tree: it is what
turned two CI runs red on 2026-10-03, when a VM pushed the cheapest possible
sequence — create a task, commit it, push it — and the Documentation lint step
failed on the file the VM had just created.

Two different commits can carry that repair, and only one of them is the tool's:

| Commit | Who makes it | What it must include |
|---|---|---|
| create the task | you | the task file, `tasks/CLAIMS.jsonl`, **and both indexes** — `task new` prints the command |
| claim the task | `task claim` | the task file, the ledger, and both indexes; the tool stages all four |

A rebuilt index left unstaged is the same defect one commit later, and it cost
four more red runs on 2026-10-04 before the claim path was fixed (T-0027).

## Statuses

```
open ──claim──▶ claimed ──complete──▶ done
                   │
                   └──cancel──▶ cancelled
```

`blocked` exists for work that cannot proceed. Record the blocker in the task's
Notes section and in the session log, so the next agent inherits the reason
rather than repeating the discovery.

## Claiming

```bash
tools/origin task claim T-0001 --agent "$AGENT" --vm "$HOSTNAME"
```

A claim is written and then pushed atomically; when the claim has been pushed,
the remote is the authority. A second agent claiming a held task fails with
exit `1` and names the holder. This is the main concurrency control, and it is
enough for a fleet that respects claims. An unpushed claim protects nothing —
whatever it shows locally is invisible to every other machine.

Work happens in its own directory and branch:
`tools/origin worktree add T-0001` puts the task in `.worktrees/T-0001/`.

**Stale claims.** A claim whose holder has disappeared blocks the task. Do not
take it silently. Finish the dead session honestly first:

```bash
tools/origin session verify                 # find the unfinished session
tools/origin session finish --outcome partial --summary "…" --next "…"
```

then claim the task with a takeover note recording why the old claim is dead:

```bash
tools/origin task claim T-0001 --agent "$AGENT" --vm "$HOSTNAME" --takeover "holder VM gone since 2026-10-03"
```

The audit trail shows the gap honestly instead of hiding it. The same rule
applies to a session that was claimed but never finished: verify first, then
take over.

## Verification

```bash
tools/origin task verify T-0001
```

Runs the declared command, prints the tail of the output on failure, and exits
`3` when the command ran and failed. Exit `1` means there was no `verify` field,
which is a task-authoring error.

Never complete a task whose verification has not run in the session that claims
it. Never edit `verify` to make a failing task pass; fix the work or cancel the
task with a reason.

## Completion

```bash
tools/origin task complete T-0001 --summary "…" --evidence paths/to/artifacts/
```

Completion writes the status, appends to the claim ledger, and prints a reminder
that `STATE.md` and `ROADMAP.md` may need updating. That reminder is not
advisory: a session that completes a task and does not update `STATE.md` leaves
the reload point lying to the next agent.

## A task is not a research record

A task says what to do. What was learned goes in `HYPOTHESES.md`,
`FAILURES.md`, `DECISIONS.md`, or an `EXPERIMENTS/` directory, and the session
log ties them together. Keeping findings in the task file means they are lost
when the file is closed.

## Automation

See [`operations/vm-execution.md`](../operations/vm-execution.md) for the VM
sequence and [`operations/github-app.md`](../operations/github-app.md) for the
dispatch mechanism. The invariant that makes unattended runs safe is that every
run ends with `session finish`, including failed runs, so an interrupted run is
visible as unfinished rather than invisible.