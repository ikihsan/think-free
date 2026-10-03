# Session 2026-10-03-019-t-0007-distance-budget-variant-of-002-a1

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-03T16:44:12+00:00
- **Duration:** 353.2s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

T-0007: distance-budget variant of 002-a1-masking

## Summary

T-0007: decision-directed regret 85.2 flat across D∈{40,80,160}km, centrality 16.3→0; gate fails 6/6; F006 recorded; negative result for A1 in the fieldwork-cost regime

## Next

Compare the six sealed investigations and feed surviving candidates into the information-sufficiency witness; or apply it to the three held candidates

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/002-a1-masking/distance.py | 1237f34cae9d | 6563 |
| EXPERIMENTS/002-a1-masking/distance.json | 4ebfef00a2e1 | 5607 |
| EXPERIMENTS/002-a1-masking/README.md | d0060abc5ef7 | 3267 |
| FAILURES.md | 77c2d55da5b4 | 11023 |
| STATE.md | 7e2f973a64cf | 7413 |

## Commands

5 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', 'EXPERIMENTS/002-a1-masking/distance.py'] | 0 | 43746 |
| 3 | ['python3', 'EXPERIMENTS/002-a1-masking/distance.py'] | 0 | 74605 |
| 10 | ['tools/origin', 'doc', 'index'] | 0 | 1131 |
| 11 | ['tools/origin', 'doc', 'lint'] | 0 | 1284 |
| 12 | ['tools/origin', 'task', 'verify', 'T-0007'] | 0 | 375 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 1 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | tasks/T-0007-002-a1-masking-distance-limited-fieldwork-cost-b.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 16:44:12 | session_start | T-0007: distance-budget variant of 002-a1-masking |
| 2 | 16:46:02 | command | $ python3 EXPERIMENTS/002-a1-masking/distance.py |
| 3 | 16:48:54 | command | $ python3 EXPERIMENTS/002-a1-masking/distance.py |
| 4 | 16:49:51 | artifact | wrote EXPERIMENTS/002-a1-masking/distance.py |
| 5 | 16:49:51 | artifact | wrote EXPERIMENTS/002-a1-masking/distance.json |
| 6 | 16:49:51 | artifact | wrote EXPERIMENTS/002-a1-masking/README.md |
| 7 | 16:49:51 | artifact | wrote FAILURES.md |
| 8 | 16:49:51 | artifact | wrote STATE.md |
| 9 | 16:49:51 | milestone | distance-budget variant run: DD gate fails 6/6, centrality wins; recorded F006 |
| 10 | 16:49:57 | command | $ tools/origin doc index |
| 11 | 16:49:58 | command | $ tools/origin doc lint |
| 12 | 16:49:59 | command | $ tools/origin task verify T-0007 |
| 13 | 16:50:05 | unlogged_change | changed but never declared as an artifact: tasks/T-0007-002-a1-masking-distance-limited-fieldwork-cost-b.md |
| 14 | 16:50:05 | doc_update | updated FAILURES.md |
| 15 | 16:50:05 | doc_update | updated STATE.md |
| 16 | 16:50:05 | session_end | T-0007: decision-directed regret 85.2 flat across D∈{40,80,160}km, centrality 16.3→0; gate fails 6/6; F006 recorded; negative result for A1 in the fie |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-03-019-t-0007-distance-budget-variant-of-002-a1/events.jsonl
```
