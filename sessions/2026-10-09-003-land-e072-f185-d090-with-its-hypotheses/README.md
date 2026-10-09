# Session 2026-10-09-003-land-e072-f185-d090-with-its-hypotheses

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-09
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-09T02:58:46+00:00
- **Duration:** 17008.7s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Land E072 (F185/D090) with its HYPOTHESES gap closed, then run E073: does a piecewise-constant price model replace the CV ceiling and recover recall on E072's frozen corpus?

## Summary

E073 complete: piecewise-constant price model is strictly better than CV ceiling on every count (recall 0.455, F1 0.197, precision 0.126) but recovers only 2 of 14 CV-gate misses. G1 (recall >= 0.50) and G2 (F1 margin >= +0.05) both fail. Recurring-expense detector line closed (F186, D091). eval_arms.py split at 300-line cap. All docs updated, doc lint passes, 21 relevant tests pass.

## Next

Candidate seat empty, all derived actions spent. Next session: fresh observation from a surface that publishes arrivals and a population not yet read, or a new domain entirely.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/073-piecewise-price/README.md | 061e00ad0e63 | 6887 |
| EXPERIMENTS/073-piecewise-price/verdict.json | d4201c863819 | 3547 |
| EXPERIMENTS/073-piecewise-price/added_labels.json | aa1ad6ad6f20 | 3747 |
| EXPERIMENTS/073-piecewise-price/results.json | 96ba72f51cb4 | 31727 |
| EXPERIMENTS/073-piecewise-price/added_groups.json | cf098589122e | 6645 |
| EXPERIMENTS/073-piecewise-price/dropped_groups.json | c20e030c295b | 14716 |
| EXPERIMENTS/073-piecewise-price/eval_arms.py | 9e8c9feaba1d | 14406 |
| EXPERIMENTS/073-piecewise-price/detect_pwc.py | ad071bcc31e9 | 5433 |
| EXPERIMENTS/073-piecewise-price/PROTOCOL.md | 161c5099afd5 | 7047 |

## Commands

5 captured, 2 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 3 | ['python3', 'EXPERIMENTS/073-piecewise-price/eval_arms.py'] | 1 | 51517 |
| 5 | ['python3', 'EXPERIMENTS/073-piecewise-price/eval_arms.py'] | 1 | 87803 |
| 7 | ['python3', 'EXPERIMENTS/073-piecewise-price/eval_arms.py'] | 0 | 33289 |
| 8 | ['python3', 'EXPERIMENTS/073-piecewise-price/eval_arms.py'] | 0 | 35796 |
| 19 | ['python3', 'EXPERIMENTS/073-piecewise-price/eval_arms.py'] | 0 | 43082 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 78 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | .gitignore |
|   undeclared | DECISIONS-SCREENING-15.md |
|   undeclared | DECISIONS-SCREENING-16.md |
|   undeclared | DECISIONS.md |
|   undeclared | EXPERIMENTS/067-viewcount-framework/README.md |
|   undeclared | EXPERIMENTS/067-viewcount-framework/classify.py |
|   undeclared | EXPERIMENTS/067-viewcount-framework/outcome.py |
|   undeclared | EXPERIMENTS/067-viewcount-framework/viewcount.py |
|   undeclared | EXPERIMENTS/067b-did-you-mean-test/EXPERIMENT-RESULT.json |
|   undeclared | EXPERIMENTS/067b-did-you-mean-test/README.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 02:58:46 | session_start | Land E072 (F185/D090) with its HYPOTHESES gap closed, then run E073: does a piecewise-constant price model replace the CV ceiling and recover recall o |
| 2 | 06:40:26 | milestone | Resuming interrupted session 2026-10-09-003: E072 landing complete in-tree (uncommitted), E073 harness written (PROTOCOL.md, detect_pwc.py, eval_arms. |
| 3 | 06:42:16 | command | $ python3 EXPERIMENTS/073-piecewise-price/eval_arms.py |
| 4 | 06:44:26 | note | Pre-first-run harness repair (defect-class, no gate/arm/threshold/label change): run_pwc returned detector dicts where the census expects merchant str |
| 5 | 06:46:47 | command | $ python3 EXPERIMENTS/073-piecewise-price/eval_arms.py |
| 6 | 06:55:19 | note | Pre-first-run harness repair 2 (no gate/arm/threshold/label change): describe_group's census view included positive-credit rows the detector's amount< |
| 7 | 07:03:21 | command | $ python3 EXPERIMENTS/073-piecewise-price/eval_arms.py |
| 8 | 07:06:39 | command | $ python3 EXPERIMENTS/073-piecewise-price/eval_arms.py |
| 9 | 07:11:25 | milestone | E073 first full run complete: G0 passes (e065_raw reproduces E072 exactly after fixing a mixed-side filter defect), G1 and G2 fail (recall 0.455 < 0.5 |
| 10 | 07:20:47 | artifact | wrote EXPERIMENTS/073-piecewise-price/README.md |
| 11 | 07:20:48 | artifact | wrote EXPERIMENTS/073-piecewise-price/verdict.json |
| 12 | 07:20:48 | artifact | wrote EXPERIMENTS/073-piecewise-price/added_labels.json |
| 13 | 07:20:49 | artifact | wrote EXPERIMENTS/073-piecewise-price/results.json |
| 14 | 07:20:50 | artifact | wrote EXPERIMENTS/073-piecewise-price/added_groups.json |
| 15 | 07:20:50 | artifact | wrote EXPERIMENTS/073-piecewise-price/dropped_groups.json |
| 16 | 07:20:51 | artifact | wrote EXPERIMENTS/073-piecewise-price/eval_arms.py |
| 17 | 07:20:52 | artifact | wrote EXPERIMENTS/073-piecewise-price/detect_pwc.py |
| 18 | 07:20:52 | artifact | wrote EXPERIMENTS/073-piecewise-price/PROTOCOL.md |
| 19 | 07:29:40 | command | $ python3 EXPERIMENTS/073-piecewise-price/eval_arms.py |
| 20 | 07:42:14 | unlogged_change | changed but never declared as an artifact: .gitignore |
| 21 | 07:42:14 | unlogged_change | changed but never declared as an artifact: DECISIONS-SCREENING-15.md |
| 22 | 07:42:14 | unlogged_change | changed but never declared as an artifact: DECISIONS-SCREENING-16.md |
| 23 | 07:42:14 | unlogged_change | changed but never declared as an artifact: DECISIONS.md |
| 24 | 07:42:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/067-viewcount-framework/README.md |
| 25 | 07:42:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/067-viewcount-framework/classify.py |
| 26 | 07:42:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/067-viewcount-framework/outcome.py |
| 27 | 07:42:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/067-viewcount-framework/viewcount.py |
| 28 | 07:42:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/067b-did-you-mean-test/EXPERIMENT-RESULT.json |
| 29 | 07:42:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/067b-did-you-mean-test/README.md |
| 30 | 07:42:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/067b-did-you-mean-test/results-raw.json |
| 31 | 07:42:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/069-false-accept-confusion/PROTOCOL.md |
| 32 | 07:42:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/069-false-accept-confusion/README.md |
| 33 | 07:42:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/069-false-accept-confusion/outcome.py |
| 34 | 07:42:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/069-false-accept-confusion/search.py |
| 35 | 07:42:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/069-false-accept-confusion/search_v2.py |
| 36 | 07:42:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/069-view-count-nonsoftware/EXPERIMENT-RESULT.json |
| 37 | 07:42:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/069-view-count-nonsoftware/README.md |
| 38 | 07:42:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/069-view-count-nonsoftware/raw/api-responses.json |
| 39 | 07:42:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-discourse-fresh-observation/EXPERIMENT-RESULT.json |
| 40 | 07:42:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-discourse-fresh-observation/PROTOCOL.md |
| 95 | 07:42:15 | unlogged_change | changed but never declared as an artifact: tools/originlib/idalloc.py |
| 96 | 07:42:15 | unlogged_change | changed but never declared as an artifact: tools/originlib/paths.py |
| 97 | 07:42:15 | unlogged_change | changed but never declared as an artifact: tools/originlib/reconcile.py |
| 98 | 07:42:15 | doc_update | updated DECISIONS-SCREENING-15.md |
| 99 | 07:42:15 | doc_update | updated DECISIONS-SCREENING-16.md |
| 100 | 07:42:15 | doc_update | updated DECISIONS.md |
| 101 | 07:42:15 | doc_update | updated FAILURES.md |
| 102 | 07:42:15 | doc_update | updated HYPOTHESES.md |
| 103 | 07:42:15 | doc_update | updated STATE.md |
| 104 | 07:42:15 | session_end | E073 complete: piecewise-constant price model is strictly better than CV ceiling on every count (recall 0.455, F1 0.197, precision 0.126) but recovers |

_54 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-09-003-land-e072-f185-d090-with-its-hypotheses/events.jsonl
```
