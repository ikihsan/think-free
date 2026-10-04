<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# VM execution

How a task gets executed on another machine. The design constraint is that the
system must be useful **before** any coordination infrastructure exists, so that
the GitHub App is an accelerator rather than a prerequisite.

Task protocol: [`../process/task-lifecycle.md`](../process/task-lifecycle.md).
Dispatch design: [`github-app.md`](github-app.md).
Scheduling: [`scheduling-and-supervision.md`](scheduling-and-supervision.md).

## Model

Git is the only shared state. Every VM clones the repository, claims a task,
works, and pushes a branch. There is no central scheduler, no shared
filesystem, and no queue service.

```
task claimed ──▶ VM works ──▶ verification passes ──▶ branch pushed
      │                                                 │
      └── stale claim ──▶ honest takeover, logged        └── merged to main
```

## The sequence

```bash
git clone <repo> && cd <repo>

# 1. Can this machine do the work at all?
tools/origin doctor                     # writes .origin/doctor.json
tools/origin preflight                  # lint + skills + session integrity

# 2. Identify yourself honestly in the record
export ORIGIN_AGENT="opencode-headless" # or codex, claude, ...

# 3. Take a task, in its own worktree
tools/origin task list
TASK=$(tools/origin task list --status open | head -1 | cut -d' ' -f1)
tools/origin task claim "$TASK" --agent "$ORIGIN_AGENT" --vm "$(hostname)"
tools/origin worktree add "$TASK"
cd ".worktrees/$TASK"
tools/origin session start --goal "execute $TASK" --task "$TASK"

# 4. Work, logging as you go
tools/x -- ./tools/origin doctor --offline

# 5. Verify with the task's own command
tools/origin task verify "$TASK"

# 6. Close honestly, whatever happened
tools/origin task complete "$TASK" --summary "…" --evidence …
tools/origin doc index
tools/origin session finish --outcome worked --summary "…" --next "…" --push

# 7. Land the branch onto the shared base
tools/origin sync land
```

`tools/origin task verify` exits `3` when the declared command fails. That is
the signal to stop, not to proceed anyway.

## Why one event file per session

Sessions write `sessions/<id>/events.jsonl` inside their own directory. Two VMs
working on different tasks therefore never touch the same file, so their logs
merge without conflict. The generated `sessions/INDEX.md` and `tasks/INDEX.md`
can conflict; regenerate them after merging rather than hand-resolving them.

This is the main reason the record is per-session rather than a single global
log. A single global `events.jsonl` would conflict on every concurrent run.

## Safety properties

- **Claims prevent duplicate work.** A second agent claiming a held task fails.
- **Verification decides completion.** No agent's confidence is involved.
- **Failure is visible.** Every run ends with `session finish`, including failed
  ones. `session verify` reports any session whose last event is not
  `session_end`, which is exactly the signal a supervisor needs.
- **Secrets do not land.** `doctor` reports only credential *presence*; captured
  output is redacted; artifacts containing credentials are refused.
- **Nothing is pushed without authorization.** Pushing to a remote requires the
  user's permission per `../policy/permissions-and-safety.md`.

## What is not solved

| Problem | Current state |
|---|---|
| Stale claims from a dead VM | `task claim --takeover REASON`; the dead session finished honestly first |
| Task-to-VM matching | Manual. An agent picks a task and claims it |
| Budget and quota across VMs | Unimplemented. `doctor` reports resources per machine only |
| Retry policy | Unimplemented. A failed session is a human decision to resume or cancel |
| Secrets distribution | Unimplemented. App private keys must never enter the repository |
| Parallel execution conflicts | Rare by design: one file per task, one directory per session |

## Requirements on a VM

Checked with `doctor` rather than assumed. What is actually exercised:

- **CPython 3.8 or newer.** `observed`: the full suite is green on 3.8.10
  (`instance-20260717-0944`, git 2.25.1) and CI is green on 3.12. Nothing in
  `tools/originlib` uses syntax newer than 3.8. An earlier version of this
  document demanded 3.11 and was wrong: it would have refused a machine the
  tooling supports, on the strength of the development machine's version rather
  than a test. The machine-readable authority is
  [`../../tests/python-versions.json`](../../tests/python-versions.json), and
  reading it is how you learn what is **not** covered: no interpreter between
  3.8 and 3.12 has ever run this suite, and nothing predicts that 3.13 or 3.14
  will.
- `git`. No package installation step: the tooling is standard library only.
- Network access to the git remote, and to public sources for research tasks.
- Sufficient disk for the experiment. `doctor` reports free bytes.

Not required, and their absence is not a blocker: a GPU, Docker, `gh` CLI,
pytest, or any system-wide install.

**What the record does not do.** `python-versions.json` states what the suite
has actually run on, per version, and `tests/test_pythonversions.py` fails when a
version has no scope, when the floor claims a minor version no entry recorded,
or when the unexercised list is empty. It does **not** compare this VM's
interpreter against it, which is the remaining half of defect 6 in
[`../../STATE-defects.md`](../../STATE-defects.md): a VM on 3.9 is not warned,
it is merely undocumented. `doctor` reads the git half of this record and not the
Python half.