<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-05
-->

<!-- task-meta
id: T-0070
status: claimed
created: 2026-10-05
claim-agent: unknown-agent
claim-session: 2026-10-05-014-measure-the-structure-of-the-589-never-a
claim-vm: 
verify: test -f EXPERIMENTS/026-unserved-need-structure/results.json && python3 -c "import json;d=json.load(open('EXPERIMENTS/026-unserved-need-structure/results.json'));assert 'answered' in str(d.keys()) or 'arms' in d" && tools/origin doc lint
-->

# T-0070 — Classify the 589 never-answered need statements in the E022 corpus

## Goal

Classify the 589 never-answered need statements in the E022 corpus

## Why this matters

The corpus's last open reading: does the unserved tail carry structure (trigger, length, story) or is it diffuse noise?

## Preconditions



## Steps



## Acceptance criteria



## Verification

```bash
test -f EXPERIMENTS/026-unserved-need-structure/results.json && python3 -c "import json;d=json.load(open('EXPERIMENTS/026-unserved-need-structure/results.json'));assert 'answered' in str(d.keys()) or 'arms' in d" && tools/origin doc lint
```

## Rollback



## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.
