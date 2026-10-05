<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-05
-->

<!-- task-meta
id: T-0071
status: open
created: 2026-10-05
claim-agent:
claim-session:
claim-vm:
verify: test -f EXPERIMENTS/026-unserved-need-structure/results.json && tools/origin doc lint
-->

# T-0071 — Classify the 589 never-answered need statements in the E022 corpus

## Goal

Classify the 589 never-answered need statements in the E022 corpus

## Why this matters

The corpus's last open reading: does the unserved tail carry structure (trigger, length, story) or is it diffuse noise?

## Preconditions



## Steps



## Acceptance criteria



## Verification

```bash
test -f EXPERIMENTS/026-unserved-need-structure/results.json && tools/origin doc lint
```

## Rollback



## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.
