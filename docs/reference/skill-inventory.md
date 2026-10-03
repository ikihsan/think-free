<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# Skill inventory

Twenty-one skills in `.agents/skills/<name>/SKILL.md`, mirrored into
`.claude/skills/<name>` so Claude Code finds the same files. Full naming and
mirroring rules are enforced by `tools/origin skills check`.

## How discovery works

| Directory | Read by |
|---|---|
| `.agents/skills/` | Codex, Gemini CLI, Cursor, OpenCode — the canonical location |
| `.claude/skills/` | Claude Code, OpenCode |
| `.opencode/skills/` | OpenCode (not needed here; the two above are enough) |

Each `.claude/skills/<name>` entry is a **per-skill symlink** to
`../../.agents/skills/<name>`. The whole `skills/` directory is never symlinked,
because Codex writes internal files there. On a filesystem without symlinks,
run `tools/origin skills sync --copy` and treat the copies as build artefacts.

Edit the real file in `.agents/skills/`, never the mirror.

## Authored skills

These encode this repository's own rules. They exist because a rule written only
in a document is not applied when an agent does not read that document.

| Skill | Use when | Enforced by |
|---|---|---|
| [`session-lifecycle`](../../.agents/skills/session-lifecycle/SKILL.md) | Any session that edits files or runs evidence-producing commands | `session finish` reconciliation |
| [`evidence-record`](../../.agents/skills/evidence-record/SKILL.md) | Writing a hypothesis, experiment, decision, or failure record | `session finish` documentation gaps |
| [`falsification-design`](../../.agents/skills/falsification-design/SKILL.md) | Before implementing any claim that could be wrong | Kill gate written first |
| [`prior-art-check`](../../.agents/skills/prior-art-check/SKILL.md) | Before claiming novelty or naming a candidate | Three-vocabulary search |
| [`doc-keeper`](../../.agents/skills/doc-keeper/SKILL.md) | After changing behaviour, docs, or structure | `origin doc lint` |
| [`task-execution`](../../.agents/skills/task-execution/SKILL.md) | Claiming and executing a task, including headless VM runs | `origin task verify` |
| [`honest-reporting`](../../.agents/skills/honest-reporting/SKILL.md) | Writing any report, summary, or claim of result | `review-protocol.md` |

## Vendored skills

Superpowers v6.2.0 by Jesse Vincent, MIT. Byte-identical to upstream, verified at
vendoring time. Provenance, licences, local divergences, and the update
procedure: [`../../vendor/MANIFEST.md`](../../vendor/MANIFEST.md).

| Skill | Purpose |
|---|---|
| [`brainstorming`](../../.agents/skills/brainstorming/SKILL.md) | Explore intent and requirements before building |
| [`writing-plans`](../../.agents/skills/writing-plans/SKILL.md) | Produce an executable written plan |
| [`executing-plans`](../../.agents/skills/executing-plans/SKILL.md) | Execute a plan with review checkpoints |
| [`subagent-driven-development`](../../.agents/skills/subagent-driven-development/SKILL.md) | Run independent plan tasks in separate subagents |
| [`dispatching-parallel-agents`](../../.agents/skills/dispatching-parallel-agents/SKILL.md) | Parallelise independent work |
| [`test-driven-development`](../../.agents/skills/test-driven-development/SKILL.md) | Write a failing test before implementation |
| [`systematic-debugging`](../../.agents/skills/systematic-debugging/SKILL.md) | Diagnose before fixing |
| [`verification-before-completion`](../../.agents/skills/verification-before-completion/SKILL.md) | Run verification before claiming success |
| [`requesting-code-review`](../../.agents/skills/requesting-code-review/SKILL.md) | Request review at completion |
| [`receiving-code-review`](../../.agents/skills/receiving-code-review/SKILL.md) | Process review feedback with rigour |
| [`using-git-worktrees`](../../.agents/skills/using-git-worktrees/SKILL.md) | Isolate work in a worktree |
| [`finishing-a-development-branch`](../../.agents/skills/finishing-a-development-branch/SKILL.md) | Integrate a completed branch |
| [`writing-skills`](../../.agents/skills/writing-skills/SKILL.md) | Author and validate skills |
| [`using-superpowers`](../../.agents/skills/using-superpowers/SKILL.md) | Bootstrap skill discovery |

## Local overrides

Vendored skills behave as upstream except where `AGENTS.md` says otherwise:

- **Plan location.** `docs/superpowers/plans/` becomes `tasks/` or `docs/`. This
  repository has its own task system and document graph.
- **Design approval.** `brainstorming` and `writing-plans` no longer pause for
  human approval on research, experiment, and infrastructure work, per decision
  `D003`. They still produce a written design, in `docs/process/` or the task
  file. Ask the human when an action needs **authorization**, not for ordinary
  design review.
- **Discovery.** Skills come from the repository, not from plugin metadata.

## Adding a skill

```bash
mkdir -p .agents/skills/<name>
$EDITOR .agents/skills/<name>/SKILL.md
tools/origin skills sync
tools/origin skills check
```

Rules the checker enforces: the directory name and the frontmatter `name` must
match and match `^[a-z0-9]+(-[a-z0-9]+)*$`; `description` is required and at most
1024 characters; `synced` and `anthropic-skills` are reserved. Frontmatter keys
outside the Agent Skills specification produce a warning, because Claude Code's
packaging path rejects them.

Record the trigger precisely. A vague description is a skill the agent never
loads.