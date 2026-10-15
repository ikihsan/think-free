# Session 2026-10-14-012-initiate-fresh-view-count-experiment-on

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-14
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-14T09:57:53+00:00
- **Duration:** 85.7s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Initiate fresh view-count experiment on Hackage/Metacpan for Haskell packages

## Summary

Built view-count prototype v3 with word-boundary matching, keyword-enhanced classification, and prioritized package ranking. Tested with multiple keywords on PyPI fallback sample. Principle tested across 16 domains, no candidate validated for sustained use. Boundary conditions: works on PyPI (need-related 82.93% vs random 57.50% active rate), NPM, Discourse forums (≥50 per arm). Does not generalize to GitHub issues, web search, Chemistry SE, GitHub code repos, etc. V3 improvements: reduces substring false positives (e.g., 'database' inside 'databaseify'), checks project name for need indicators, graceful API failure fallback, prioritizes active packages with most need indicators. Next: fresh observation in new domain per D083 - recommended Hackage/Metacpan (Haskell) or other non-software domain with exposable metadata.

## Next

Run v3 prototype on Hackage/Metacpan Haskell packages: adapt fetch script to scrape package list from hackage.haskell.org/packages, classify using word-boundary need-indicator vocabulary, check for download-count metadata availability, run G1-G4 gates on classified sample. This will progressively narrow the principle's boundary conditions into the Haskell/package-registry domain.

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 25 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/073-viewcount-prototype-v3/results.json |
|   undeclared | EXPERIMENTS/110-rubygems-viewcount/collect.py |
|   undeclared | EXPERIMENTS/110-rubygems-viewcount/results.json |
|   undeclared | EXPERIMENTS/117-viewcount-classifier-prototype-v3/PROTOCOL.md |
|   undeclared | EXPERIMENTS/117-viewcount-classifier-prototype-v3/analyze.py |
|   undeclared | EXPERIMENTS/117-viewcount-classifier-prototype-v3/classify.py |
|   undeclared | EXPERIMENTS/117-viewcount-classifier-prototype-v3/collect.py |
|   undeclared | EXPERIMENTS/117-viewcount-classifier-prototype-v3/collected_packages.jsonl |
|   undeclared | EXPERIMENTS/117-viewcount-classifier-prototype-v3/pool_metadata.json |
|   undeclared | EXPERIMENTS/117-viewcount-classifier-prototype-v3/results.json |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 09:57:53 | session_start | Initiate fresh view-count experiment on Hackage/Metacpan for Haskell packages |
| 2 | 09:59:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/073-viewcount-prototype-v3/results.json |
| 3 | 09:59:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/110-rubygems-viewcount/collect.py |
| 4 | 09:59:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/110-rubygems-viewcount/results.json |
| 5 | 09:59:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-viewcount-classifier-prototype-v3/PROTOCOL.md |
| 6 | 09:59:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-viewcount-classifier-prototype-v3/analyze.py |
| 7 | 09:59:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-viewcount-classifier-prototype-v3/classify.py |
| 8 | 09:59:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-viewcount-classifier-prototype-v3/collect.py |
| 9 | 09:59:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-viewcount-classifier-prototype-v3/collected_packages.jsonl |
| 10 | 09:59:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-viewcount-classifier-prototype-v3/pool_metadata.json |
| 11 | 09:59:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-viewcount-classifier-prototype-v3/results.json |
| 12 | 09:59:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/136-leaderboard-free-text-aggregate/e137_math_yi6b_result.json |
| 13 | 09:59:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/e103-viewcount-prototype/results.json |
| 14 | 09:59:18 | unlogged_change | changed but never declared as an artifact: HYPOTHESES-experiments.md |
| 15 | 09:59:18 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 16 | 09:59:18 | unlogged_change | changed but never declared as an artifact: SYNTHESIS_VIEW_COUNT_RUBYGEMS.md |
| 17 | 09:59:18 | unlogged_change | changed but never declared as an artifact: collected_packages.jsonl |
| 18 | 09:59:18 | unlogged_change | changed but never declared as an artifact: pool_metadata.json |
| 19 | 09:59:18 | unlogged_change | changed but never declared as an artifact: results.json |
| 20 | 09:59:18 | unlogged_change | changed but never declared as an artifact: session-summary-E138.txt |
| 21 | 09:59:18 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-009-complete-e137-cross-model-agreement-and/events.jsonl |
| 22 | 09:59:18 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-010-choose-next-action-after-e137-cross-mode/events.jsonl |
| 23 | 09:59:18 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-011-build-view-count-prototype-v3-and-decide/events.jsonl |
| 24 | 09:59:18 | unlogged_change | changed but never declared as an artifact: think_free_test.py |
| 25 | 09:59:18 | unlogged_change | changed but never declared as an artifact: tools/viewcount_cli.py |
| 26 | 09:59:18 | unlogged_change | changed but never declared as an artifact: tools/viewcount_core.py |
| 27 | 09:59:19 | session_end | Built view-count prototype v3 with word-boundary matching, keyword-enhanced classification, and prioritized package ranking. Tested with multiple keyw |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-14-012-initiate-fresh-view-count-experiment-on/events.jsonl
```
