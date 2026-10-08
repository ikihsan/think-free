<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-07
-->

<!-- task-meta
id: T-0086
status: done
created: 2026-10-07
claim-agent: unknown-agent
claim-session: 2026-10-07-013-land-e049-evidence-from-sessions-011-012
claim-vm: 
verify: python3 EXPERIMENTS/050-registry-mechanisms/harness.py --verify
-->

# T-0086 — E2 registry mechanisms: (a) re-run E049 Part B control; (b) check ever

## Goal

E2 registry mechanisms: (a) re-run E049 Part B control; (b) check every (name,version) pinned in E049's 10 old PyPI lockfile snapshots for yank/absence today

## Why this matters

E049 Part A conflated project-updates with resolution drift; the registry half of E2 (same pinned inputs -> broken or changed artifacts later) has one mechanism measurable today: PyPI yanking or deleting a pinned version. If 0 of ~828 pinned versions across 10 snapshots are yanked or absent, the registry-breakage mechanism is dead at this population and E2's registry claim survives only as the time-gated Part B re-run.

## Preconditions

E049 raw/ snapshots committed; network access to pypi.org

## Steps



## Acceptance criteria

results.json with per-pair status, a counted verdict, and the harness self-verify passing

## Verification

```bash
python3 EXPERIMENTS/050-registry-mechanisms/harness.py --verify
```

## Rollback



## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.
