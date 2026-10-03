# Session 2026-10-03-015-a1-experiment-step-1-pin-a-ppna-commit-a

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `opencode`
- **Started:** 2026-10-03T16:09:02+00:00
- **Duration:** 397.0s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

A1 experiment step 1: pin a PPNA commit and inspect whether a complete-enough neighborhood extract exists

## Summary

Ran the bounded A1 masking experiment: pinned PPNA commit, found maskable curbramp/marked facts in seattle.geojson, implemented random+block masking with 5 policies over 30 seeds, decision-directed won; results and caveats committed under EXPERIMENTS/002-a1-masking

## Next

Run a budget/K/block-size sensitivity sweep of 002-a1-masking

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/002-a1-masking/masking.py | 5cf0d90298a0 | 8681 |
| EXPERIMENTS/002-a1-masking/results.json | 8a1e472cf2a0 | 7885 |
| EXPERIMENTS/002-a1-masking/README.md | 265af0fca313 | 1699 |
| EXPERIMENTS/PLAN.md | 1069b4d2a19d | 2687 |
| STATE.md | 2bab009f0ad1 | 7323 |

## Commands

4 captured, 1 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['git', 'clone', '--depth', '1', 'https://github.com/OpenSidewalks/PLoS-cities-complex-systems', '/tmp/opencode/plos-cities'] | 0 | 28175 |
| 4 | ['python3', 'EXPERIMENTS/002-a1-masking/masking.py'] | 1 | 6675 |
| 5 | ['python3', 'EXPERIMENTS/002-a1-masking/masking.py'] | 0 | 17516 |
| 11 | ['tools/origin', 'doc', 'lint'] | 0 | 1485 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 1 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | tasks/T-0005-a1-run-the-bounded-sidewalk-survey-masking-exper.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 16:09:02 | session_start | A1 experiment step 1: pin a PPNA commit and inspect whether a complete-enough neighborhood extract exists |
| 2 | 16:09:48 | command | $ git clone --depth 1 https://github.com/OpenSidewalks/PLoS-cities-complex-systems /tmp/opencode/plos-cities |
| 3 | 16:11:02 | milestone | PPNA pinned at 4f65e22b19576375b2b031b035631a20806da48e; seattle.geojson: 103451 crossings with curbramps/crossing/subclass/length; reach_metrics.gpkg |
| 4 | 16:12:47 | command | $ python3 EXPERIMENTS/002-a1-masking/masking.py |
| 5 | 16:14:19 | command | $ python3 EXPERIMENTS/002-a1-masking/masking.py |
| 6 | 16:15:27 | artifact | wrote EXPERIMENTS/002-a1-masking/masking.py |
| 7 | 16:15:27 | artifact | wrote EXPERIMENTS/002-a1-masking/results.json |
| 8 | 16:15:28 | artifact | wrote EXPERIMENTS/002-a1-masking/README.md |
| 9 | 16:15:28 | artifact | wrote EXPERIMENTS/PLAN.md |
| 10 | 16:15:28 | artifact | wrote STATE.md |
| 11 | 16:15:31 | command | $ tools/origin doc lint |
| 12 | 16:15:39 | unlogged_change | changed but never declared as an artifact: tasks/T-0005-a1-run-the-bounded-sidewalk-survey-masking-exper.md |
| 13 | 16:15:39 | doc_update | updated STATE.md |
| 14 | 16:15:39 | session_end | Ran the bounded A1 masking experiment: pinned PPNA commit, found maskable curbramp/marked facts in seattle.geojson, implemented random+block masking w |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-03-015-a1-experiment-step-1-pin-a-ppna-commit-a/events.jsonl
```
