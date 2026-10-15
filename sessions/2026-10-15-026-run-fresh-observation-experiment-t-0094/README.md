# Session 2026-10-15-026-run-fresh-observation-experiment-t-0094

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-15
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-15T21:17:17+00:00
- **Duration:** 1873.3s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Run fresh observation experiment T-0094: test view-count principle across PyPI popularity and age tiers

## Summary

Completed E165: PyPI view-count principle tier analysis. Tested G1-G4 gates across popularity tiers (by number of releases) and age tiers (by first release year). All gates pass in all tiers. G1 ratios range 91-116% across cross-tabulation cells. Principle is robust across tiers on PyPI but effect size is modest due to high baseline activity rates (description+version binary metric).

## Next

Fresh observation in a new domain per STATE-next-actions.md: Chrome Web Store, GitHub follower counts, Homebrew, Pub.dev, or CocoaPods

## Artifacts

_none_

## Commands

2 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 3 | ['tools/origin', 'session', 'step', 'Created experiment directory, starting implementation'] | 0 | 1289 |
| 4 | ['tools/origin', 'session', 'artifact', 'EXPERIMENTS/165-pypi-tier-analysis/results.json'] | 0 | 603 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 5 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/165-pypi-tier-analysis/RESULT.md |
|   undeclared | EXPERIMENTS/165-pypi-tier-analysis/gates.py |
|   undeclared | EXPERIMENTS/165-pypi-tier-analysis/pypi_client.py |
|   undeclared | EXPERIMENTS/165-pypi-tier-analysis/run.py |
|   undeclared | EXPERIMENTS/165-pypi-tier-analysis/vocab.py |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 21:17:17 | session_start | Run fresh observation experiment T-0094: test view-count principle across PyPI popularity and age tiers |
| 2 | 21:19:19 | milestone | Created experiment directory, starting implementation |
| 3 | 21:19:20 | command | $ tools/origin session step Created experiment directory, starting implementation |
| 4 | 21:31:20 | command | $ tools/origin session artifact EXPERIMENTS/165-pypi-tier-analysis/results.json |
| 5 | 21:48:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/165-pypi-tier-analysis/RESULT.md |
| 6 | 21:48:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/165-pypi-tier-analysis/gates.py |
| 7 | 21:48:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/165-pypi-tier-analysis/pypi_client.py |
| 8 | 21:48:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/165-pypi-tier-analysis/run.py |
| 9 | 21:48:30 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/165-pypi-tier-analysis/vocab.py |
| 10 | 21:48:31 | session_end | Completed E165: PyPI view-count principle tier analysis. Tested G1-G4 gates across popularity tiers (by number of releases) and age tiers (by first re |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-15-026-run-fresh-observation-experiment-t-0094/events.jsonl
```
