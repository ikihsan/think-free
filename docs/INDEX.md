# Documentation index

<!-- origin-meta
owner: docs/README.md
status: active
last-verified: 2026-10-03
-->

<!-- generated-by: origin; do not edit by hand -->

Every document in the repository, grouped by zone, with the index that owns it.
Regenerate with `tools/origin doc index`. Policies that govern these documents
are in [`policy/doc-standards.md`](policy/doc-standards.md).

Skill bodies under `.agents/skills/` are indexed by
[`reference/skill-inventory.md`](reference/skill-inventory.md) instead.

## Start here

| Document | Purpose |
|---|---|
| [`../AGENTS.md`](../AGENTS.md) | Canonical agent contract. Read first. |
| [`../STATE.md`](../STATE.md) | Verified current state and next actions. The reload point. |
| [`../MISSION.md`](../MISSION.md) | Objective, boundaries, stopping rules. |
| [`../RELEASE-MANIFEST.md`](../RELEASE-MANIFEST.md) | What is public and what is internal. |
| [`../README.md`](../README.md) | Human front door. |

## docs/policy

| Document | Owner index | Status | Verified | Summary |
|---|---|---|---|---|
| [`docs/policy/evidence-labels.md`](policy/evidence-labels.md) | `docs/INDEX.md` | active | 2026-10-03 | Every claim carries one of these labels. They are not decoration: an unlabelled |
| [`docs/policy/logging-standard.md`](policy/logging-standard.md) | `docs/INDEX.md` | active | 2026-10-03 | What must be recorded, in what form, and what is deliberately exempt. The |
| [`docs/policy/permissions-and-safety.md`](policy/permissions-and-safety.md) | `docs/INDEX.md` | active | 2026-10-03 | What an agent may do without asking, what needs explicit authorization, and |

## docs/process

| Document | Owner index | Status | Verified | Summary |
|---|---|---|---|---|
| [`docs/process/experiment-protocol.md`](process/experiment-protocol.md) | `docs/INDEX.md` | active | 2026-10-03 | How an experiment is designed, run, and judged. Read this before writing code |
| [`docs/process/hypothesis-lifecycle.md`](process/hypothesis-lifecycle.md) | `docs/INDEX.md` | active | 2026-10-03 | How a candidate becomes a decision. The aim is that no candidate is ever |
| [`docs/process/multi-vm-coordination.md`](process/multi-vm-coordination.md) | `docs/INDEX.md` | active | 2026-10-03 | How several machines share this repository safely. The invariant: git is the |
| [`docs/process/review-protocol.md`](process/review-protocol.md) | `docs/INDEX.md` | active | 2026-10-03 | The adversarial step. Its purpose is not to confirm work but to find the reason |
| [`docs/process/session-protocol.md`](process/session-protocol.md) | `docs/INDEX.md` | active | 2026-10-03 | Every working session follows these steps. The goal is that a session's record |
| [`docs/process/task-lifecycle.md`](process/task-lifecycle.md) | `docs/INDEX.md` | active | 2026-10-03 | A task is a unit of work another machine can pick up without asking a question. |

## docs/operations

| Document | Owner index | Status | Verified | Summary |
|---|---|---|---|---|
| [`docs/operations/bootstrap.md`](operations/bootstrap.md) | `docs/INDEX.md` | active | 2026-10-03 | Getting a fresh machine able to work on this repository. The design goal is that |
| [`docs/operations/ci.md`](operations/ci.md) | `docs/INDEX.md` | active | 2026-10-03 | Runs on every push and pull request. The gates are the same ones a session must |
| [`docs/operations/github-app.md`](operations/github-app.md) | `docs/INDEX.md` | active | 2026-10-03 | Status: design, not implemented. No GitHub App exists yet. Nothing in this |
| [`docs/operations/scheduling-and-supervision.md`](operations/scheduling-and-supervision.md) | `docs/INDEX.md` | active | 2026-10-03 | Whether agent work can run unattended, and what has actually been verified. The |
| [`docs/operations/vm-execution.md`](operations/vm-execution.md) | `docs/INDEX.md` | active | 2026-10-03 | How a task gets executed on another machine. The design constraint is that the |

## docs/reference

| Document | Owner index | Status | Verified | Summary |
|---|---|---|---|---|
| [`docs/reference/cli-reference.md`](reference/cli-reference.md) | `docs/INDEX.md` | active | 2026-10-03 | Every command the repository's tooling provides. Stdlib Python only, so no |
| [`docs/reference/skill-inventory.md`](reference/skill-inventory.md) | `docs/INDEX.md` | active | 2026-10-03 | Twenty-one skills in .agents/skills/<name>/SKILL.md, mirrored into |

## sessions

| Document | Owner index | Status | Verified | Summary |
|---|---|---|---|---|
| [`sessions/README.md`](../sessions/README.md) | `docs/INDEX.md` | active | 2026-10-03 | The append-only record of every working session in this repository. |

## tasks

| Document | Owner index | Status | Verified | Summary |
|---|---|---|---|---|
| [`tasks/README.md`](../tasks/README.md) | `docs/INDEX.md` | active | 2026-10-03 | Dispatchable units of work. One Markdown file per task, each declaring a |
| [`tasks/T-0001-write-falsification-kill-gates-for-the-three-hel.md`](../tasks/T-0001-write-falsification-kill-gates-for-the-three-hel.md) | `tasks/INDEX.md` | active | 2026-10-03 | ## Goal |
| [`tasks/T-0002-run-investigation-e-the-experimental-engineer-ro.md`](../tasks/T-0002-run-investigation-e-the-experimental-engineer-ro.md) | `tasks/INDEX.md` | active | 2026-10-03 | ## Goal |
| [`tasks/T-0003-run-investigation-f-the-adoption-researcher-role.md`](../tasks/T-0003-run-investigation-f-the-adoption-researcher-role.md) | `tasks/INDEX.md` | active | 2026-10-03 | ## Goal |
| [`tasks/T-0004-make-concurrent-multi-vm-sessions-safe-isolated.md`](../tasks/T-0004-make-concurrent-multi-vm-sessions-safe-isolated.md) | `tasks/INDEX.md` | active | 2026-10-03 | ## Goal |
| [`tasks/T-0005-a1-run-the-bounded-sidewalk-survey-masking-exper.md`](../tasks/T-0005-a1-run-the-bounded-sidewalk-survey-masking-exper.md) | `tasks/INDEX.md` | active | 2026-10-03 | ## Goal |
| [`tasks/T-0006-002-a1-masking-sensitivity-sweep-over-budget-k-a.md`](../tasks/T-0006-002-a1-masking-sensitivity-sweep-over-budget-k-a.md) | `tasks/INDEX.md` | active | 2026-10-03 | ## Goal |
| [`tasks/T-0007-002-a1-masking-distance-limited-fieldwork-cost-b.md`](../tasks/T-0007-002-a1-masking-distance-limited-fieldwork-cost-b.md) | `tasks/INDEX.md` | active | 2026-10-03 | ## Goal |
| [`tasks/T-0008-apply-the-information-sufficiency-witness-to-the.md`](../tasks/T-0008-apply-the-information-sufficiency-witness-to-the.md) | `tasks/INDEX.md` | active | 2026-10-03 | ## Goal |
| [`tasks/T-0009-repair-the-knitting-witness-input-set-by-adding.md`](../tasks/T-0009-repair-the-knitting-witness-input-set-by-adding.md) | `tasks/INDEX.md` | active | 2026-10-03 | ## Goal |

## RESEARCH

| Document | Owner index | Status | Verified | Summary |
|---|---|---|---|---|
| [`RESEARCH/A.md`](../RESEARCH/A.md) | `RESEARCH.md` | sealed | 2026-10-03 | owner: RESEARCH.md |
| [`RESEARCH/B.md`](../RESEARCH/B.md) | `RESEARCH.md` | sealed | 2026-10-03 | owner: RESEARCH.md |
| [`RESEARCH/C.md`](../RESEARCH/C.md) | `RESEARCH.md` | sealed | 2026-10-03 | owner: RESEARCH.md |
| [`RESEARCH/D.md`](../RESEARCH/D.md) | `RESEARCH.md` | sealed | 2026-10-03 | owner: RESEARCH.md |
| [`RESEARCH/E.md`](../RESEARCH/E.md) | `RESEARCH.md` | sealed | 2026-10-03 | Independent report. Written 2026-10-03 after reading MISSION.md only. The |
| [`RESEARCH/EXPERIMENT-PROTOCOL.md`](../RESEARCH/EXPERIMENT-PROTOCOL.md) | `docs/process/experiment-protocol.md` | archived | 2026-10-03 | The canonical text is now |
| [`RESEARCH/F.md`](../RESEARCH/F.md) | `RESEARCH.md` | sealed | 2026-10-03 | Independent report. Written 2026-10-03 after reading MISSION.md only; |
| [`RESEARCH/README.md`](../RESEARCH/README.md) | `RESEARCH.md` | active | 2026-10-03 | owner: RESEARCH.md |
| [`RESEARCH/ROOT-SCOUTING.md`](../RESEARCH/ROOT-SCOUTING.md) | `RESEARCH.md` | sealed | 2026-10-03 | owner: RESEARCH.md |

## EXPERIMENTS

| Document | Owner index | Status | Verified | Summary |
|---|---|---|---|---|
| [`EXPERIMENTS/000-capabilities/README.md`](../EXPERIMENTS/000-capabilities/README.md) | `EXPERIMENTS/PLAN.md` | sealed | 2026-10-03 | owner: EXPERIMENTS/PLAN.md |
| [`EXPERIMENTS/001-photo-baseline/README.md`](../EXPERIMENTS/001-photo-baseline/README.md) | `EXPERIMENTS/PLAN.md` | sealed | 2026-10-03 | owner: EXPERIMENTS/PLAN.md |
| [`EXPERIMENTS/002-a1-masking/README.md`](../EXPERIMENTS/002-a1-masking/README.md) | `EXPERIMENTS/README.md` | active | 2026-10-03 | Bounded A1 masking experiment over the PPNA Seattle crossings extract. |
| [`EXPERIMENTS/003-information-sufficiency/README.md`](../EXPERIMENTS/003-information-sufficiency/README.md) | `EXPERIMENTS/README.md` | active | 2026-10-03 | Applies the information-sufficiency witness (the cheap pre-implementation gate in |
| [`EXPERIMENTS/PLAN.md`](../EXPERIMENTS/PLAN.md) | `EXPERIMENTS/PLAN.md` | active | 2026-10-03 | owner: EXPERIMENTS/PLAN.md |
| [`EXPERIMENTS/README.md`](../EXPERIMENTS/README.md) | `EXPERIMENTS/PLAN.md` | active | 2026-10-03 | owner: EXPERIMENTS/PLAN.md |

## Generated maps

| Map | Purpose |
|---|---|
| `docs/INDEX.md` | This map. |
| `sessions/INDEX.md` | Every recorded session and its outcome. |
| `tasks/INDEX.md` | Dispatchable tasks and their claims. |

## Adding a document

1. Give it an `origin-meta` block with its owning index.
2. Link it from exactly one index; orphans fail `doc lint`.
3. Keep it under 300 lines. Split at 250.
