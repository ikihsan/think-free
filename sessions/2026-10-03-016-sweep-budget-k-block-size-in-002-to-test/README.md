# Session 2026-10-03-016-sweep-budget-k-block-size-in-002-to-test

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `opencode`
- **Started:** 2026-10-03T16:16:36+00:00
- **Duration:** 148.4s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Sweep budget/K/block-size in 002 to test sensitivity of the A1 masking result

## Summary

Completed T-0006 sensitivity sweep of 002-a1-masking; boundary result recorded

## Next

Consider a distance-limited (fieldwork-tour) budget variant of A1

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/002-a1-masking/masking.py | c7843112023c | 9993 |
| EXPERIMENTS/002-a1-masking/sensitivity.json | af029f6c1e74 | 7869 |
| EXPERIMENTS/002-a1-masking/README.md | 2cee64e381e4 | 2361 |
| STATE.md | ca67e419bb09 | 7373 |

## Commands

1 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', 'EXPERIMENTS/002-a1-masking/masking.py', '--sweep'] | 0 | 53191 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 1 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | tasks/T-0006-002-a1-masking-sensitivity-sweep-over-budget-k-a.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 16:16:36 | session_start | Sweep budget/K/block-size in 002 to test sensitivity of the A1 masking result |
| 2 | 16:18:35 | command | $ python3 EXPERIMENTS/002-a1-masking/masking.py --sweep |
| 3 | 16:19:02 | artifact | wrote EXPERIMENTS/002-a1-masking/masking.py |
| 4 | 16:19:03 | artifact | wrote EXPERIMENTS/002-a1-masking/sensitivity.json |
| 5 | 16:19:03 | artifact | wrote EXPERIMENTS/002-a1-masking/README.md |
| 6 | 16:19:04 | artifact | wrote STATE.md |
| 7 | 16:19:05 | unlogged_change | changed but never declared as an artifact: tasks/T-0006-002-a1-masking-sensitivity-sweep-over-budget-k-a.md |
| 8 | 16:19:05 | doc_update | updated STATE.md |
| 9 | 16:19:05 | session_end | Completed T-0006 sensitivity sweep of 002-a1-masking; boundary result recorded |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-03-016-sweep-budget-k-block-size-in-002-to-test/events.jsonl
```
