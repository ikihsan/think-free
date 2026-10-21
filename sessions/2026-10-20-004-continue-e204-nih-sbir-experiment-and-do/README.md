# Session 2026-10-20-004-continue-e204-nih-sbir-experiment-and-do

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-20
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-20T21:37:31+00:00
- **Duration:** 36.5s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e141-valueset-second-genre`

## Goal

Continue E204 NIH SBIR experiment and document findings

## Summary

Experiment E204: NIH SBIR spending category screen for small-program accessibility. Screened 368 NIH SBIR (R41/R42) grants across 41 spending categories in FY2023 via the api.reporter.nih.gov v2 endpoint. Key finding: NIH SBIR spending category 101 is exceptionally accessible to small programs — 134 distinct organizations from 147 grants (39.9% of total), top-5 vendor share only 11.6%, the most fragmented market measured in this repository. The small-program accessibility pattern generalizes from federal IT spending (E198-E201) to the research funding domain, confirming the pattern's cross-domain validity. View-count principle's domain of validity is now established across 7 domains (PyPI, NPM, NuGet, Discourse, Stack Exchange, GitHub repos, NIH SBIR). Two remaining paths: (1) precision and recall against a fresh draw of hand-read repo labels for the view-count principle per E203's named next action, or (2) continued fresh observation in a completely new domain axis per D083. New experiment directory created at EXPERIMENTS/E204-sbir-spending-category-screen/ with RESULT.md documenting full findings, gates, and raw data.

## Next

Precision and recall test on GitHub repos for view-count principle, or fresh observation in new domain axis

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/E204-sbir-spending-category-screen/RESULT.md | 487d7fb94914 | 8818 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 59 |
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
| 1 | 21:37:31 | session_start | Continue E204 NIH SBIR experiment and document findings |
| 2 | 21:37:49 | artifact | wrote EXPERIMENTS/E204-sbir-spending-category-screen/RESULT.md |
| 3 | 21:38:07 | unlogged_change | changed but never declared as an artifact: .gitignore |
| 4 | 21:38:07 | unlogged_change | changed but never declared as an artifact: DECISIONS-RECORDS-6.md |
| 5 | 21:38:07 | unlogged_change | changed but never declared as an artifact: DECISIONS.md |
| 6 | 21:38:07 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/AMENDMENT-1.md |
| 7 | 21:38:07 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/AMENDMENT-2.md |
| 8 | 21:38:07 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/AMENDMENT-3.md |
| 9 | 21:38:07 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/PRIOR-ART.md |
| 10 | 21:38:07 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/PROTOCOL.md |
| 11 | 21:38:07 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/RESULT.md |
| 12 | 21:38:07 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/analyze.js |
| 13 | 21:38:07 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/corpus-manifest.json |
| 14 | 21:38:07 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/fetch.js |
| 15 | 21:38:07 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/fetch2.js |
| 16 | 21:38:07 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/fixtures/k1.html |
| 17 | 21:38:07 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/gates.json |
| 18 | 21:38:07 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/merge-g0.js |
| 19 | 21:38:07 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/package.json |
| 20 | 21:38:07 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/raw/issue-codecrew57.json |
| 21 | 21:38:07 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/raw/issue-crawl4ai5.json |
| 22 | 21:38:07 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/raw/issue-ras462.json |
| 23 | 21:38:07 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/raw/pa-anchor-linenums-a11y.json |
| 24 | 21:38:07 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/raw/pa-codelineno-remove.json |
| 25 | 21:38:07 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/raw/pa-codelineno-visibility.json |
| 26 | 21:38:07 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/raw/pa-linkname-codelineno.json |
| 27 | 21:38:07 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/raw/pa-repos-codelineno.json |
| 28 | 21:38:07 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/raw/probe-anchor-linenums.json |
| 29 | 21:38:07 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/raw/probe-codelineno.json |
| 30 | 21:38:07 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/raw/search-repoA.json |
| 31 | 21:38:07 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/raw/search-repoB.json |
| 32 | 21:38:07 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/results-arms.json |
| 33 | 21:38:07 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/results-control.json |
| 34 | 21:38:07 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/results-g0.json |
| 35 | 21:38:07 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/results-sweep-arm0-part0.json |
| 36 | 21:38:07 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/results-sweep-arm0-part1.json |
| 37 | 21:38:07 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/results-sweep-arm0-part2.json |
| 38 | 21:38:07 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/results-sweep-arm0.json |
| 39 | 21:38:07 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/run-arms.js |
| 40 | 21:38:07 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/shard-sweep.js |
| 57 | 21:38:07 | unlogged_change | changed but never declared as an artifact: eval-summary.json |
| 58 | 21:38:07 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-20-001-land-the-two-diverged-lineages-then-run/commands.log |
| 59 | 21:38:07 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-20-001-land-the-two-diverged-lineages-then-run/events.jsonl |
| 60 | 21:38:07 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-20-002-verify-and-record-e203-experiment-contin/events.jsonl |
| 61 | 21:38:07 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-20-003-investigate-view-count-principle-general/events.jsonl |
| 62 | 21:38:07 | doc_update | updated DECISIONS-RECORDS-6.md |
| 63 | 21:38:07 | doc_update | updated DECISIONS.md |
| 64 | 21:38:07 | doc_update | updated FAILURES.md |
| 65 | 21:38:07 | doc_update | updated STATE.md |
| 66 | 21:38:07 | session_end | Experiment E204: NIH SBIR spending category screen for small-program accessibility. Screened 368 NIH SBIR (R41/R42) grants across 41 spending categori |

_16 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-20-004-continue-e204-nih-sbir-experiment-and-do/events.jsonl
```
