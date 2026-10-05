<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-05
-->

<!-- task-meta
id: T-0069
status: claimed
created: 2026-10-05
claim-agent: unknown-agent
claim-session: 2026-10-05-013-measure-whether-the-1250-people-who-publ
claim-vm: 
verify: python3 EXPERIMENTS/025-need-staters-builderhood/stats.py > /dev/null && python3 -m unittest discover -s EXPERIMENTS/025-need-staters-builderhood -p 'test_*.py' -t EXPERIMENTS/025-need-staters-builderhood && tools/origin doc lint
-->

# T-0069 — measure whether the people who publicly stated a need are people who b

## Goal

measure whether the people who publicly stated a need are people who build

## Why this matters

F042's 0-of-24 build arm was labelled a floor on disclosure, but STATE-next-actions item 0 carried it as a fact about people. Reading the missing channel decides whether the corpus closure stands. Identifier was allocated as T-0069 before the task file existed.

## Preconditions



## Steps

1. PROTOCOL.md written before any fetch 2. Gate A1 controls run first 3. 1250 need authors and 500 control authors fetched 4. Wilson intervals computed from raw captures 5. every gate falsified against a breaking fixture

## Acceptance criteria

H1 survives at 2x with disjoint intervals, or B1 fires with overlapping ones, or C1 reports not_evaluated; a refused fetch is never counted as a zero

## Verification

```bash
python3 EXPERIMENTS/025-need-staters-builderhood/stats.py > /dev/null && python3 -m unittest discover -s EXPERIMENTS/025-need-staters-builderhood -p 'test_*.py' -t EXPERIMENTS/025-need-staters-builderhood && tools/origin doc lint
```

## Rollback



## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.
