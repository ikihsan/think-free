# Session 2026-10-11-005-run-pyfix-prototype-and-view-count-hacke

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-11
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-11T05:25:42+00:00
- **Duration:** 29.2s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Run pyfix prototype and view-count Hacker News experiment

## Summary

Ran two fresh observation experiments per D083: (1) view-count principle on Hacker News stories — 3/100 need-related, principle does not generalize (G1 FAIL); (2) pyfix prototype extension — 100% resolution accuracy (3/3 alias cases), 8.17x mean speedup vs manual search. Both experiments close ground per D083 (new domains). Pyfix mechanism validated: 15/19 discrimination probes resolved per E086. Package-name line already closed per F113/D102. No new candidates generated; boundary conditions mapped.

## Next

Map boundary conditions from both experiments; decide whether pyfix resolver integration or new domain experiment is next useful action per phase-decision.json.

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 14 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/09X-hnews-viewcount/results.json |
|   undeclared | EXPERIMENTS/09X-hnews-viewcount/run.py |
|   undeclared | EXPERIMENTS/09X-pyfix-prototype/prototype.py |
|   undeclared | EXPERIMENTS/0xx-cran-r-keyword-activity/results.json |
|   undeclared | EXPERIMENTS/0xx-github-repo-need-class/results.json |
|   undeclared | EXPERIMENTS/0xx-github-repo-star-activity/results.json |
|   undeclared | EXPERIMENTS/0xx-import-error-need-class/results.json |
|   undeclared | EXPERIMENTS/0xx-pypi-keyword-activity/results.json |
|   undeclared | EXPERIMENTS/0xx-viewcount-import-resolvability/results.json |
|   undeclared | EXPERIMENTS/0xx-viewcount-prototype/results.json |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 05:25:42 | session_start | Run pyfix prototype and view-count Hacker News experiment |
| 2 | 05:26:02 | milestone | Completed pyfix prototype and Hacker News view-count experiment |
| 3 | 05:26:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/09X-hnews-viewcount/results.json |
| 4 | 05:26:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/09X-hnews-viewcount/run.py |
| 5 | 05:26:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/09X-pyfix-prototype/prototype.py |
| 6 | 05:26:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-cran-r-keyword-activity/results.json |
| 7 | 05:26:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-github-repo-need-class/results.json |
| 8 | 05:26:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-github-repo-star-activity/results.json |
| 9 | 05:26:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-import-error-need-class/results.json |
| 10 | 05:26:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-pypi-keyword-activity/results.json |
| 11 | 05:26:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-viewcount-import-resolvability/results.json |
| 12 | 05:26:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/0xx-viewcount-prototype/results.json |
| 13 | 05:26:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/experiment-outcome-summary.json |
| 14 | 05:26:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/phase-decision.json |
| 15 | 05:26:11 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/synthesis-view-count-final.md |
| 16 | 05:26:11 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 17 | 05:26:11 | session_end | Ran two fresh observation experiments per D083: (1) view-count principle on Hacker News stories — 3/100 need-related, principle does not generalize (G |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-11-005-run-pyfix-prototype-and-view-count-hacke/events.jsonl
```
