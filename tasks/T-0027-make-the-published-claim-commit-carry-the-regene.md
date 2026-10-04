<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0027
status: done
created: 2026-10-04
claim-agent: opencode
claim-session: 
claim-vm: instance-20260717-0947
verify: PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint
-->

# T-0027 — Make the published claim commit carry the regenerated indexes, and tel

## Goal

Make the published claim commit carry the regenerated indexes, and tell the agent how to publish a new task without orphaning it

## Why this matters

T-0026 made task new rebuild the generated indexes, and its own verification passed - yet four CI runs after it were red on Documentation lint (37165502352, 37165507351, 37165802926, 37165807196). The cause is the same defect one step later: taskremote.claim stages only the task file and the claim ledger, so the indexes T-0026 rebuilt are left unstaged, and the claim commit - the first thing every other VM sees - is red. Read from the tree at a2f5ca0: 'orphan document' for the task file, plus a stale docs/INDEX.md and tasks/INDEX.md.

## Preconditions

T-0026 already provides tasks.write_index() and docindex.write_index(); this task is about who stages them, not about regenerating them.

## Steps

1. Falsification first (D025). Kill gate: on two real clones with a bare remote, publish a task, claim it from vm-a, then have vm-b pull and lint. Without the fix vm-b's tree reports tasks/INDEX.md stale and the task file orphaned; with it, neither appears. 2. taskremote.claim and taskremote.release rebuild the indexes and stage them in the claim commit, which is the commit every other VM reads first. 3. 'task new' prints the publish command that keeps the tree lintable, because the create commit is made by the agent and no tool can own it. 4. Docs: task-lifecycle.md, cli-reference.md, STATE-defects.md defect 4, ROADMAP.md.

## Acceptance criteria

- [x] Two clones: after a published claim, the other VM's fetched tree lints with no orphan and no stale index.
- [x] Removing the rebuild makes that test fail (captured).
- [x] 'task new' prints a publish command that stages the generated indexes.
- [x] Full suite, doc lint, release check, skills check and session verify all exit 0.

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint
```

## Rollback

Revert `tools/originlib/taskremote.py` and `tools/originlib/cli_task.py`; the
T-0026 rebuild stays, so the indexes are written again but left unstaged, which is
the pre-T-0027 behaviour.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

**T-0026's verification passed and the defect was still live.** That is the
finding worth keeping: the gate this task inherited (`task verify T-0026`) ran the
suite and the lint on a tree where the indexes had already been rebuilt by hand,
so it could not see that the *claim* commit left them unstaged. Four red runs
(`37165502352`, `37165507351`, `37165802926`, `37165807196`) came after it. The
new test lints a *fetched* tree on a second clone, which is the only way to see
what the claim commit actually published.

**Falsified:** with `refresh_indexes()` removed from the claim path, vm-b's lint
reports `tasks/INDEX.md: generated file is stale`; the other six tests do not
move. Suite: 276 tests.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.
