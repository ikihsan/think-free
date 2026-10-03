---
name: task-execution
description: Claim, execute, verify, and complete a dispatchable task from tasks/, including on a remote VM or in a headless agent run. Use when picking up a task, when asked to work on a task file, or when setting up unattended or automated execution. Triggers - "claim T-", "work on task", "run this task", "headless run", "on the VM", "what tasks are open", or any unattended agent execution in this repository.
license: MIT
compatibility: agent-agnostic
metadata:
  scope: operations
  enforcement: tools/origin task verify
---

# Task execution

A task file is a contract: a goal, acceptance criteria, and a **runnable
verification command**. If the verification command does not prove the goal, the
task is not finished.

Protocol: [`docs/process/task-lifecycle.md`](../../../docs/process/task-lifecycle.md).
Map: [`tasks/INDEX.md`](../../../tasks/INDEX.md).

## Shape of a task

```markdown
<!-- task-meta
id: T-0001
status: open
created: 2026-10-03
claim-agent:
claim-vm:
verify: tools/origin doc lint
-->
```

Statuses: `open`, `claimed`, `blocked`, `done`, `cancelled`.

The `verify` field is the important one. It must be a single command whose exit
code decides completion, and it must fail when the work is not done. A task
whose verification always passes is worse than no task.

## Claiming

```bash
tools/origin task list
tools/origin task claim T-0001 --agent "$AGENT" --vm "$HOSTNAME"
tools/origin worktree add T-0001
tools/origin session start --goal "…" --task T-0001 --agent "$AGENT"
```

A second agent claiming a task that another agent holds **fails**. That is the
whole mechanism: the claim is pushed atomically and the remote is the
authority. A claim nobody has pushed protects nothing, so never use
`--no-push` for real work. Take over a dead holder's claim with
`task claim --takeover REASON`, after that session is verified and finished
honestly.

If you find a task claimed by an agent that is clearly gone, do not take it
silently. Record your takeover in the session log with the evidence that the
previous holder stopped.

## Working

Follow the task file. Log as you go:

```bash
tools/origin session step "verification now fails on the missing mirror"
tools/x -- ./tools/origin doc lint
```

Keep the working tree honest. Files you change that are not part of the task are
either in scope or must be reverted; `session finish` will list undeclared
changes.

## Verifying

```bash
tools/origin task verify T-0001
```

This runs the declared command, records the exit code and duration, prints the
tail of the output on failure, and returns `3` when the command fails. Exit `3`
means the verification ran and did not pass. That is information, not an
obstacle to reporting.

Never complete a task whose verification has not been run in this session.

## Completing

```bash
tools/origin task complete T-0001 --summary "what changed" --evidence paths/
tools/origin doc index
tools/origin session finish --outcome worked --summary "…" --next "…" --push
tools/origin sync land
```

Completion is a claim about the evidence, not about the effort. If the
verification passes but the goal is only partly met, leave the task claimed and
write down what remains.

## Headless and VM runs

```bash
tools/origin doctor --offline     # can this machine do the work at all?
tools/origin preflight            # lint + skills + session integrity
```

Run `doctor` **before** claiming a task on a new machine. An environment
limitation found at claim time is a fact; the same limitation found halfway
through is a lost session.

Set these explicitly in an automated run, so the record says what actually ran:

```bash
export ORIGIN_AGENT="opencode-headless"    # or codex, claude, etc.
```

Every automated run must finish with `session finish`, including failed runs. An
unfinished session is reported by `session verify` and shows up as unfinished in
`sessions/INDEX.md`, which is exactly the signal a supervisor needs.

## Cancellation

```bash
tools/origin task cancel T-0001 --reason "already solved by T-0002"
```

Cancel rather than abandon silently. An abandoned task with no record will be
picked up again by the next agent, wasting the work of finding out it was
finished.

## Rules

1. Never claim a task you are not going to work on.
2. Never mark a task done without its verification passing.
3. Never edit `tasks/CLAIMS.jsonl` by hand.
4. Never weaken a `verify` command to make a task pass.
5. Every session on a task ends with `session finish`, whatever the outcome.