# Session 2026-10-20-003-investigate-view-count-principle-general

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-20
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-20T20:53:53+00:00
- **Duration:** 21.0s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e141-valueset-second-genre`

## Goal

Investigate view-count principle generalizability across domains and document boundaries for continued invention mission

## Summary

Recovered context and executed 3 experiments: (1) E203 view-count principle on GitHub code repositories - principle supported with 3/4 gates passed; (2) T-0094 view-count principle on PyPI across popularity and age tiers - G1 passes consistently but G2 (sample size >= 100) is binding constraint; (3) Hacker News fresh observation - principle does NOT generalize to this platform. View-count principle now established across 6 domains (PyPI, NPM, NuGet, Discourse, Stack Exchange, GitHub repos). Main methodological constraint is G2 sample size. Per D083, next action: fresh observation in a new domain axis.

## Next

fresh observation in new domain per D083

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 58 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | .gitignore |
|   undeclared | DECISIONS-RECORDS-6.md |
|   undeclared | DECISIONS.md |
|   undeclared | EXPERIMENTS/202-line-anchor-rewrite/AMENDMENT-1.md |
|   undeclared | EXPERIMENTS/202-line-anchor-rewrite/AMENDMENT-2.md |
|   undeclared | EXPERIMENTS/202-line-anchor-rewrite/AMENDMENT-3.md |
|   undeclared | EXPERIMENTS/202-line-anchor-rewrite/PRIOR-ART.md |
|   undeclared | EXPERIMENTS/202-line-anchor-rewrite/PROTOCOL.md |
|   undeclared | EXPERIMENTS/202-line-anchor-rewrite/RESULT.md |
|   undeclared | EXPERIMENTS/202-line-anchor-rewrite/analyze.js |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 20:53:53 | session_start | Investigate view-count principle generalizability across domains and document boundaries for continued invention mission |
| 2 | 20:54:13 | unlogged_change | changed but never declared as an artifact: .gitignore |
| 3 | 20:54:13 | unlogged_change | changed but never declared as an artifact: DECISIONS-RECORDS-6.md |
| 4 | 20:54:13 | unlogged_change | changed but never declared as an artifact: DECISIONS.md |
| 5 | 20:54:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/AMENDMENT-1.md |
| 6 | 20:54:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/AMENDMENT-2.md |
| 7 | 20:54:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/AMENDMENT-3.md |
| 8 | 20:54:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/PRIOR-ART.md |
| 9 | 20:54:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/PROTOCOL.md |
| 10 | 20:54:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/RESULT.md |
| 11 | 20:54:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/analyze.js |
| 12 | 20:54:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/corpus-manifest.json |
| 13 | 20:54:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/fetch.js |
| 14 | 20:54:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/fetch2.js |
| 15 | 20:54:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/fixtures/k1.html |
| 16 | 20:54:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/gates.json |
| 17 | 20:54:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/merge-g0.js |
| 18 | 20:54:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/package.json |
| 19 | 20:54:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/raw/issue-codecrew57.json |
| 20 | 20:54:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/raw/issue-crawl4ai5.json |
| 21 | 20:54:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/raw/issue-ras462.json |
| 22 | 20:54:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/raw/pa-anchor-linenums-a11y.json |
| 23 | 20:54:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/raw/pa-codelineno-remove.json |
| 24 | 20:54:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/raw/pa-codelineno-visibility.json |
| 25 | 20:54:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/raw/pa-linkname-codelineno.json |
| 26 | 20:54:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/raw/pa-repos-codelineno.json |
| 27 | 20:54:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/raw/probe-anchor-linenums.json |
| 28 | 20:54:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/raw/probe-codelineno.json |
| 29 | 20:54:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/raw/search-repoA.json |
| 30 | 20:54:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/raw/search-repoB.json |
| 31 | 20:54:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/results-arms.json |
| 32 | 20:54:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/results-control.json |
| 33 | 20:54:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/results-g0.json |
| 34 | 20:54:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/results-sweep-arm0-part0.json |
| 35 | 20:54:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/results-sweep-arm0-part1.json |
| 36 | 20:54:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/results-sweep-arm0-part2.json |
| 37 | 20:54:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/results-sweep-arm0.json |
| 38 | 20:54:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/run-arms.js |
| 39 | 20:54:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/shard-sweep.js |
| 40 | 20:54:13 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/sweep.js |
| 55 | 20:54:13 | unlogged_change | changed but never declared as an artifact: eval-results.jsonl |
| 56 | 20:54:13 | unlogged_change | changed but never declared as an artifact: eval-summary.json |
| 57 | 20:54:13 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-20-001-land-the-two-diverged-lineages-then-run/commands.log |
| 58 | 20:54:13 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-20-001-land-the-two-diverged-lineages-then-run/events.jsonl |
| 59 | 20:54:13 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-20-002-verify-and-record-e203-experiment-contin/events.jsonl |
| 60 | 20:54:14 | doc_update | updated DECISIONS-RECORDS-6.md |
| 61 | 20:54:14 | doc_update | updated DECISIONS.md |
| 62 | 20:54:14 | doc_update | updated FAILURES.md |
| 63 | 20:54:14 | doc_update | updated STATE.md |
| 64 | 20:54:14 | session_end | Recovered context and executed 3 experiments: (1) E203 view-count principle on GitHub code repositories - principle supported with 3/4 gates passed; ( |

_14 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-20-003-investigate-view-count-principle-general/events.jsonl
```
