<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- task-meta
id: T-0004
status: claimed
created: 2026-10-03
claim-agent: opencode
claim-session: 
claim-vm: instance-20260717-0944
verify: PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint
-->

# T-0004 — Make concurrent multi-VM sessions safe: isolated worktrees, atomic cla

## Goal

Make concurrent multi-VM sessions safe: isolated worktrees, atomic claims, sync at session boundaries

## Why this matters

Several VMs share this repository through one GitHub remote. Claims were local-only, sessions started from stale trees, and every VM shared one working tree, so two agents could duplicate or cross work with no detection.

## Preconditions

GitHub remote reachable; existing session, task, and doc tooling understood.

## Steps

1. Add fleet test harness (bare remote plus two clones) and failing tests. 2. Implement sync status/pull/push/land. 3. Implement worktree add/list/remove. 4. Implement remote-truth task claims with atomic push. 5. Harden session start and finish. 6. Update process docs, operations docs, CLI reference, AGENTS.md, and skills.

## Acceptance criteria

- [ ] Two clones cannot both hold one task: the loser is told who won
- [ ] A VM works in its own worktree and branch, and worktrees are gitignored
- [ ] session start fetches, fast-forwards, and refuses a stale or dirty tree
- [ ] session finish --push commits the session record and pushes the branch
- [ ] Generated index conflicts after a merge are resolved by regeneration
- [ ] Full test suite and doc lint exit 0

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint
```

## Rollback

Revert the commits adding tools/originlib/{sync,worktree,taskremote}.py and the CLI groups; the previous commands keep working with --no-sync.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

### 2026-10-03, session 009: implementation committed, verification outstanding

Implemented: `sync.py` (status, pull, push, land), `worktree.py` (add, list,
remove), `taskremote.py` (remote-truth claims, atomic push, takeover, release),
`sessionflow.py` (fetch-and-fast-forward on start, push-the-record on finish),
`cli_sync.py`, and `gitutil.state(root)`. Tests: `tests/test_fleet.py` and
`tests/test_sync.py` run two clones of a local bare remote, so the claim race is
exercised with real git ref updates rather than mocks. `harness.make_fleet`
exists for them.

**Verified at commit time:** nothing new. The last complete run reported six
failures in the new suites; four were diagnosed and fixed (porcelain collapsing
untracked directories, `SyncStartError` not being a `SessionError`, a stale
remote-tracking ref in `status`, a non-fetching `holder`), and the re-run was
interrupted before it finished. `tools/origin task verify T-0004` therefore still
fails. Do not treat the multi-VM flow as working until it exits 0.

**Known environment gap:** this VM has Python 3.8.10 and git 2.25.1, so the code
avoids `git init -b` and post-3.10 syntax; `vm-execution.md` claims 3.11+ and
should be corrected or the requirement relaxed.

**Still to do:** documentation (a process doc for the flow, `session-protocol.md`,
`task-lifecycle.md`, `operations/vm-execution.md`, `reference/cli-reference.md`,
`AGENTS.md`), the `session-lifecycle` and `task-execution` skills, and
`tests/README.md` coverage notes.
