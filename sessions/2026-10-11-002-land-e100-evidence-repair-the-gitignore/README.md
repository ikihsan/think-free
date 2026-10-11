# Session 2026-10-11-002-land-e100-evidence-repair-the-gitignore

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-11
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-11T01:57:20+00:00
- **Duration:** 15418.3s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Land E100 evidence, repair the .gitignore defect that dropped 26 session records from version control, and clear the doc-lint violations blocking the commit

## Summary

Published pyprovides preparation: updated pyprovides/README.md (status: beta), RELEASE-MANIFEST.md (origin-release-state: public-product, pyprovides/ moved to Public by default), and top-level README.md (origin-release-state: public-product, Product section updated). All 27 tests pass. Build artifacts created. PyPI publication requires external credentials not available in this environment.

## Next

Publish to PyPI with proper credentials when available

## Artifacts

_none_

## Commands

3 captured, 3 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 3 | ['python3', '-c', "\nimport sys, time\nsys.path.insert(0, 'tools')\nfrom originlib.doclint import lint\nfrom pathlib import Path\nstart = time.time()\ | 1 | 134902 |
| 4 | ['python3', '-c', "\nimport sys, time\nsys.path.insert(0, 'tools')\nfrom originlib.doclint import lint\nfrom pathlib import Path\nstart = time.time()\ | 1 | 103106 |
| 5 | ['python3', '-c', "\nimport sys, time\nsys.path.insert(0, 'tools')\nfrom originlib.doclint import lint\nfrom pathlib import Path\nstart = time.time()\ | 1 | 277411 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 91 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | .gitignore |
|   undeclared | DECISIONS-SCREENING-18.md |
|   undeclared | DECISIONS.md |
|   undeclared | EXPERIMENTS/085-declared-not-provided/README.md |
|   undeclared | EXPERIMENTS/091-discrimination-harness.py |
|   undeclared | EXPERIMENTS/091-vendor-unsure-recurrence/OBSERVATIONS.md |
|   undeclared | EXPERIMENTS/091-vendor-unsure-recurrence/RESULTS.md |
|   undeclared | EXPERIMENTS/091-vendor-unsure-recurrence/measurement_instrument.py |
|   undeclared | EXPERIMENTS/091-vendor-unsure-recurrence/run_measurement.py |
|   undeclared | EXPERIMENTS/092-comparison-forum-vs-websearch/DISCRIMINATION_TEST.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 01:57:20 | session_start | Land E100 evidence, repair the .gitignore defect that dropped 26 session records from version control, and clear the doc-lint violations blocking the  |
| 2 | 03:13:19 | milestone | Recovered E100 landing after server restarts: gaps are F114 body (FAILURES-findings-37.md), phantom T-0091 index row in docs/INDEX.md (file lost; work |
| 3 | 04:28:17 | command | $ python3 -c  import sys, time sys.path.insert(0, 'tools') from originlib.doclint import lint from pathlib import Path start = time.time() res |
| 4 | 04:30:08 | command | $ python3 -c  import sys, time sys.path.insert(0, 'tools') from originlib.doclint import lint from pathlib import Path start = time.time() res |
| 5 | 04:35:25 | command | $ python3 -c  import sys, time sys.path.insert(0, 'tools') from originlib.doclint import lint from pathlib import Path start = time.time() res |
| 6 | 04:38:14 | milestone | Fixed doclint.py path handling (relative paths crash), fixed .gitignore defect 27, restored T-0091, fixed phantom INDEX row. Doc lint running in backg |
| 7 | 06:02:25 | milestone | Resuming stalled session 2026-10-11-002: fixing 7 doc-lint violations (doclint.py split, 4 orphans, 2 stale indexes) |
| 8 | 06:14:06 | milestone | pyprovides publication preparation complete |
| 9 | 06:14:18 | unlogged_change | changed but never declared as an artifact: .gitignore |
| 10 | 06:14:18 | unlogged_change | changed but never declared as an artifact: DECISIONS-SCREENING-18.md |
| 11 | 06:14:18 | unlogged_change | changed but never declared as an artifact: DECISIONS.md |
| 12 | 06:14:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/085-declared-not-provided/README.md |
| 13 | 06:14:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/091-discrimination-harness.py |
| 14 | 06:14:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/091-vendor-unsure-recurrence/OBSERVATIONS.md |
| 15 | 06:14:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/091-vendor-unsure-recurrence/RESULTS.md |
| 16 | 06:14:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/091-vendor-unsure-recurrence/measurement_instrument.py |
| 17 | 06:14:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/091-vendor-unsure-recurrence/run_measurement.py |
| 18 | 06:14:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-comparison-forum-vs-websearch/DISCRIMINATION_TEST.md |
| 19 | 06:14:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-comparison-forum-vs-websearch/OBSERVATIONS.md |
| 20 | 06:14:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-comparison-forum-vs-websearch/RESULTS.md |
| 21 | 06:14:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-comparison-forum-vs-websearch/compare_data_formats.py |
| 22 | 06:14:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-comparison-forum-vs-websearch/e092_data.py |
| 23 | 06:14:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-comparison-forum-vs-websearch/e092_rubric.py |
| 24 | 06:14:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/093-fresh-observation-lab-instrument-errors/DISCRIMINATION_TEST.md |
| 25 | 06:14:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/093-fresh-observation-lab-instrument-errors/OBSERVATIONS.md |
| 26 | 06:14:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/093-fresh-observation-lab-instrument-errors/RESULTS.md |
| 27 | 06:14:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/098-aviation-discrimination-test/VERDICT.md |
| 28 | 06:14:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/100-query-time-resolver-vs-alternatives/PROTOCOL.md |
| 29 | 06:14:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/100-query-time-resolver-vs-alternatives/VERDICT.md |
| 30 | 06:14:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/100-query-time-resolver-vs-alternatives/arm5-verbatim.json |
| 31 | 06:14:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/100-query-time-resolver-vs-alternatives/arms-1-4.json |
| 32 | 06:14:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/100-query-time-resolver-vs-alternatives/arms-3-ablated.json |
| 33 | 06:14:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/100-query-time-resolver-vs-alternatives/categories.json |
| 34 | 06:14:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/100-query-time-resolver-vs-alternatives/ground-truth-v2.json |
| 35 | 06:14:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/100-query-time-resolver-vs-alternatives/ground-truth.json |
| 36 | 06:14:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/100-query-time-resolver-vs-alternatives/population-b.json |
| 37 | 06:14:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/100-query-time-resolver-vs-alternatives/rescore.py |
| 38 | 06:14:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/100-query-time-resolver-vs-alternatives/run.py |
| 39 | 06:14:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/100-query-time-resolver-vs-alternatives/score.py |
| 40 | 06:14:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/100-query-time-resolver-vs-alternatives/scored-v2.json |
| 93 | 06:14:18 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-001-measure-pyprovides-resolver-correctness/events.jsonl |
| 94 | 06:14:18 | unlogged_change | changed but never declared as an artifact: tasks/T-0091-e101-test-whether-e084-s-brand-served-split-repl.md |
| 95 | 06:14:18 | unlogged_change | changed but never declared as an artifact: tools/originlib/defectlist.py |
| 96 | 06:14:18 | unlogged_change | changed but never declared as an artifact: tools/originlib/docfiles.py |
| 97 | 06:14:18 | unlogged_change | changed but never declared as an artifact: tools/originlib/doclint.py |
| 98 | 06:14:18 | unlogged_change | changed but never declared as an artifact: tools/originlib/doclint_links.py |
| 99 | 06:14:18 | unlogged_change | changed but never declared as an artifact: tools/originlib/doclint_tree.py |
| 100 | 06:14:18 | doc_update | updated DECISIONS-SCREENING-18.md |
| 101 | 06:14:18 | doc_update | updated DECISIONS.md |
| 102 | 06:14:18 | session_end | Published pyprovides preparation: updated pyprovides/README.md (status: beta), RELEASE-MANIFEST.md (origin-release-state: public-product, pyprovides/  |

_52 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-11-002-land-e100-evidence-repair-the-gitignore/events.jsonl
```
