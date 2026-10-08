# Session 2026-10-08-015-design-and-run-a-fresh-observation-exper

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-08
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-08T15:03:39+00:00
- **Duration:** 2680.1s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Design and run a fresh observation experiment on ArXiv computational paper reproducibility

## Summary

Designed and ran E067: fresh observation experiment measuring ArXiv computational paper reproducibility. Harvested 15,397 papers from 6 categories (2024), found 1,682 with code links (10.9%), sampled 34. Assessed 25/34 repos (9 rate-limited). Results: only 11.8% (4/34) have machine-runnable environment specs (A1), 52.9% have no environment info (A4). All kill gates passed (K1: population≥20, K2: A1 rate<0.50, K3: A4 rate>0.10, K4: baseline). Problem is real and severe.

## Next

Consider whether to expand E067 with authenticated GitHub API to eliminate rate limits and increase sample size, or pivot to a different fresh observation per D080

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/067-arxiv-code-repro/PROTOCOL.md | 46af57798bc7 | 4928 |
| EXPERIMENTS/067-arxiv-code-repro/fetch.py | 3df0071ef554 | 7614 |
| EXPERIMENTS/067-arxiv-code-repro/assess.py | 638e60aadf9e | 11662 |
| EXPERIMENTS/067-arxiv-code-repro/report.py | c099190de81f | 2722 |
| EXPERIMENTS/067-arxiv-code-repro/test_assess.py | 64dd5b8d95eb | 6047 |
| EXPERIMENTS/067-arxiv-code-repro/run.py | bfaebe395dd1 | 1446 |
| EXPERIMENTS/067-arxiv-code-repro/README.md | fc55c6ceb6e4 | 2214 |
| EXPERIMENTS/067-arxiv-code-repro/raw/SOURCES.md | 0de755bae37b | 2601 |
| EXPERIMENTS/067-arxiv-code-repro/raw/papers.json | 8bcb82ad1fdc | 70143 |
| EXPERIMENTS/067-arxiv-code-repro/raw/assessment.json | f56261a11ddf | 16645 |
| EXPERIMENTS/067-arxiv-code-repro/raw/SOURCES.md | 0de755bae37b | 2601 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 1 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/067-arxiv-code-repro/classifier.py |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 15:03:39 | session_start | Design and run a fresh observation experiment on ArXiv computational paper reproducibility |
| 2 | 15:04:24 | milestone | Started new session for fresh observation experiment design |
| 3 | 15:05:31 | artifact | wrote EXPERIMENTS/067-arxiv-code-repro/PROTOCOL.md |
| 4 | 15:14:14 | artifact | wrote EXPERIMENTS/067-arxiv-code-repro/fetch.py |
| 5 | 15:14:14 | artifact | wrote EXPERIMENTS/067-arxiv-code-repro/assess.py |
| 6 | 15:14:15 | artifact | wrote EXPERIMENTS/067-arxiv-code-repro/report.py |
| 7 | 15:14:16 | artifact | wrote EXPERIMENTS/067-arxiv-code-repro/test_assess.py |
| 8 | 15:14:16 | artifact | wrote EXPERIMENTS/067-arxiv-code-repro/run.py |
| 9 | 15:14:17 | artifact | wrote EXPERIMENTS/067-arxiv-code-repro/README.md |
| 10 | 15:14:18 | artifact | wrote EXPERIMENTS/067-arxiv-code-repro/raw/SOURCES.md |
| 11 | 15:36:49 | artifact | wrote EXPERIMENTS/067-arxiv-code-repro/raw/papers.json |
| 12 | 15:36:49 | artifact | wrote EXPERIMENTS/067-arxiv-code-repro/raw/assessment.json |
| 13 | 15:36:50 | artifact | wrote EXPERIMENTS/067-arxiv-code-repro/raw/SOURCES.md |
| 14 | 15:48:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/067-arxiv-code-repro/classifier.py |
| 15 | 15:48:19 | session_end | Designed and ran E067: fresh observation experiment measuring ArXiv computational paper reproducibility. Harvested 15,397 papers from 6 categories (20 |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-08-015-design-and-run-a-fresh-observation-exper/events.jsonl
```
