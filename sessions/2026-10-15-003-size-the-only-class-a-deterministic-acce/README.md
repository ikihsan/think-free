# Session 2026-10-15-003-size-the-only-class-a-deterministic-acce

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-15
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-15T04:38:13+00:00
- **Duration:** 11914.7s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e141-valueset-second-genre`

## Goal

size the only class a deterministic accessibility tool could ever serve: with generated anchors excluded, what is the composition of real WCAG defects on a larger population, and how many of them have a name derivable from authored text

## Summary

Explored E162 results and identified next action: measure content-bearing accessibility defects on population chosen for defect density

## Next

Design experiment to crawl and rank pages by violation density, then filter plumbing and measure composition

## Artifacts

_none_

## Commands

4 captured, 1 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['node', 'EXPERIMENTS/163-a11y-content-defect-composition/fetch.js'] | 0 | 62383 |
| 4 | ['tools/origin', 'task', 'new', '--goal', "E164: measure the damaging-cell rate of a real spreadsheet engine's CSV round-trip over a larger sample of  | 0 | 66500 |
| 6 | ['python3', '/tmp/opencode/priorart163_probe.py'] | 0 | 23205 |
| 7 | ['node', 'EXPERIMENTS/163-a11y-content-defect-composition/run-oracle.js'] | 143 | 8235913 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 12 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/163-a11y-content-defect-composition/PRIOR-ART.md |
|   undeclared | EXPERIMENTS/163-a11y-content-defect-composition/PROTOCOL.md |
|   undeclared | EXPERIMENTS/163-a11y-content-defect-composition/corpus-manifest.json |
|   undeclared | EXPERIMENTS/163-a11y-content-defect-composition/derive.js |
|   undeclared | EXPERIMENTS/163-a11y-content-defect-composition/fetch.js |
|   undeclared | EXPERIMENTS/163-a11y-content-defect-composition/node_modules |
|   undeclared | EXPERIMENTS/163-a11y-content-defect-composition/package.json |
|   undeclared | EXPERIMENTS/163-a11y-content-defect-composition/page-runner.js |
|   undeclared | EXPERIMENTS/163-a11y-content-defect-composition/results-arm0.json |
|   undeclared | EXPERIMENTS/163-a11y-content-defect-composition/run-oracle.js |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 04:38:13 | session_start | size the only class a deterministic accessibility tool could ever serve: with generated anchors excluded, what is the composition of real WCAG defects |
| 2 | 04:39:55 | command | $ node EXPERIMENTS/163-a11y-content-defect-composition/fetch.js |
| 3 | 04:51:00 | task_rewrite | appended a create record for T-0097 |
| 4 | 04:52:03 | command | $ tools/origin task new --goal E164: measure the damaging-cell rate of a real spreadsheet engine's CSV round-trip over a larger sample of publ |
| 5 | 06:45:34 | milestone | resumed after server restart: oracle PID 4101437 survived detached and is still measuring arm-2 pages (24/45 done at resume); results durable in resul |
| 6 | 06:46:58 | command | $ python3 /tmp/opencode/priorart163_probe.py |
| 7 | 06:57:35 | command | $ node EXPERIMENTS/163-a11y-content-defect-composition/run-oracle.js |
| 8 | 06:57:36 | milestone | killed stuck oracle (PID 4101437, >15min in axe.run on page 025 with event loop blocked); repairing instrument with per-page subprocess + 300s externa |
| 9 | 07:56:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/163-a11y-content-defect-composition/PRIOR-ART.md |
| 10 | 07:56:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/163-a11y-content-defect-composition/PROTOCOL.md |
| 11 | 07:56:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/163-a11y-content-defect-composition/corpus-manifest.json |
| 12 | 07:56:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/163-a11y-content-defect-composition/derive.js |
| 13 | 07:56:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/163-a11y-content-defect-composition/fetch.js |
| 14 | 07:56:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/163-a11y-content-defect-composition/node_modules |
| 15 | 07:56:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/163-a11y-content-defect-composition/package.json |
| 16 | 07:56:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/163-a11y-content-defect-composition/page-runner.js |
| 17 | 07:56:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/163-a11y-content-defect-composition/results-arm0.json |
| 18 | 07:56:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/163-a11y-content-defect-composition/run-oracle.js |
| 19 | 07:56:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/163-a11y-content-defect-composition/run-pages-sub.js |
| 20 | 07:56:48 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-15-002-measure-whether-real-accessibility-defec/events.jsonl |
| 21 | 07:56:48 | session_end | Explored E162 results and identified next action: measure content-bearing accessibility defects on population chosen for defect density |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-15-003-size-the-only-class-a-deterministic-acce/events.jsonl
```
