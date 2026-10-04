<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0048
status: open
created: 2026-10-04
claim-agent:
claim-session:
claim-vm:
verify: PYTHONPATH=tools:tests python3 -m unittest tests.test_land -q && tools/origin preflight
-->

# T-0048 — Teach sync land to finish a paused rebase whose conflicts are already 

## Goal

Teach sync land to finish a paused rebase whose conflicts are already resolved, so its own instruction is executable

## Why this matters

sync land stopped on a real content conflict in tasks/CLAIMS.jsonl and said 'resolve it and land again'. The second land refuses on the dirty tree the resolution leaves, so the instruction cannot be followed: the only way out is a hand-run git rebase --continue, which records no base_advance, so every path that arrived from the base is attributed to the session that resolved the conflict. That is defect 2's stated ceiling, reached through the tool's own refusal message rather than by a mistake. Land already knows how to continue a rebase non-interactively for the generated files it auto-resolves; this is the same call for the case a human had to resolve.

## Preconditions

Two VMs publishing into tasks/CLAIMS.jsonl in the same hour, which is the normal case and has stopped a rebase more than once

## Steps

1. Read how land auto-resolves a generated conflict and reuses GIT_EDITOR=true; the resume path is the same call reached from a different state.
2. Detect a rebase already in progress with no unresolved path, continue it with the same non-interactive environment, and report what it completed.
3. Record the base_advance for the commits that arrived, so their paths are not attributed to this session - the half of defect 2 that a tooling-performed continuation can still close.
4. Falsify first: with the resume call removed, a two-clone fixture that resolves a CLAIMS.jsonl conflict cannot land at all.
5. Say what is still refused: an unresolved conflict, and a rebase land did not start.
6. Update docs/process/multi-vm-coordination.md, which documents the resolution but not the completion, and tests/README.md.

## Acceptance criteria

- [ ] land completes a paused rebase with every conflict already resolved, and refuses one that still has an unresolved path.
- [ ] The completion is non-interactive, using the same GIT_EDITOR mechanism the generated-file path already uses, and it is exercised by a test that would hang or fail without it.
- [ ] The arriving commits are recorded as a base advance, so the paths they brought are not attributed to the session that resolved the conflict.
- [ ] Falsified against the unmodified code, in a two-clone fixture that resolves a real tasks/CLAIMS.jsonl conflict.
- [ ] multi-vm-coordination.md documents the whole procedure, and says what is still refused.
- [ ] The suite and all four preflight gates are green.

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest tests.test_land -q && tools/origin preflight
```

## Rollback

Revert the resume branch in tools/originlib/syncland.py; the generated-file path it shares is unchanged and a real conflict still stops.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.
