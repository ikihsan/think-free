# Session 2026-10-20-006-begin-e207-contract-vehicle-analysis-for

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-20
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-20T19:37:12+00:00
- **Duration:** ?s
- **Host:** `instance-20260717-0947`
- **Branch:** `HEAD`

## Goal

Begin E207: contract vehicle analysis for 7030 and DA10 PSC codes to identify which vehicles (SEWP, GSA MAS, CIO-SP4, VA T4NG) small vendors use

## Summary

Completed E207 contract vehicle analysis for all 5 IT/software PSC codes (7030, DA10, 7A21, DA01, D304). Queried USAspending spending_by_award endpoint for 5,000 awards per code (25,000 total). Extracted IDV PIIDs from generated_internal_id field and classified into 11 vehicle categories (SEWP, GSA MAS, CIO-SP, VA T4NG, DoD ESI/DISA, Navy SEAPORT, Army ITES/CHESS, Air Force, DHA, Direct/Unknown, Other/Unknown). Key finding: DA10 is the only code where small vendors meaningfully use GWACs (28.2% of small vendor $ via GSA MAS + SEWP). In 7030, small vendors sell direct (88.7% Direct/Unknown). 7A21 is Army/Navy dominated with Carahsoft concentration. DA01/D304 are services/telecom markets, not software. Results saved to EXPERIMENTS/E207-contract-vehicle-analysis/RESULT.md and e207_comparison.json.

## Next

E208: Field test - recruit 3-5 small software companies to validate assessment framework against real pipeline opportunities

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/E207-contract-vehicle-analysis/RESULT.md | cf932311a89e | 7965 |
| EXPERIMENTS/E207-contract-vehicle-analysis/e207_vehicle.py | 09e629d66b66 | 11401 |
| EXPERIMENTS/E207-contract-vehicle-analysis/e207_compare.py | 3d06bf8faf34 | 6483 |
| EXPERIMENTS/E207-contract-vehicle-analysis/e207_comparison.json | 2039b6d24743 | 10883 |
| EXPERIMENTS/E207-contract-vehicle-analysis/e206_api.py | 1172df5e5c8d | 3576 |
| EXPERIMENTS/E207-contract-vehicle-analysis/e206_keywords.py | 212502333ff9 | 4602 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 4404 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | DECISIONS-NEXT.md |
|   undeclared | EXPERIMENTS/073-viewcount-prototype-v3/RESULT.md |
|   undeclared | EXPERIMENTS/223-award-description-terms/PROTOCOL.md |
|   undeclared | EXPERIMENTS/223-award-description-terms/run.py |
|   undeclared | EXPERIMENTS/225-answer-distribution/RESULT.md |
|   undeclared | EXPERIMENTS/225-answer-distribution/run.py |
|   undeclared | EXPERIMENTS/225-award-description-generalizability/run.py |
|   undeclared | EXPERIMENTS/226-keyword-disambiguation/PROTOCOL.md |
|   undeclared | EXPERIMENTS/226-keyword-disambiguation/RESULTS.md |
|   undeclared | EXPERIMENTS/E172-fresh-observation-pypi/PROTOCOL.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 19:37:12 | session_start | Begin E207: contract vehicle analysis for 7030 and DA10 PSC codes to identify which vehicles (SEWP, GSA MAS, CIO-SP4, VA T4NG) small vendors use |
| 2 | 19:37:29 | milestone | Session started for E207 contract vehicle analysis |
| 3 | 19:53:59 | milestone | Completed contract vehicle analysis for all 5 PSC codes (7030, DA10, 7A21, DA01, D304) |
| 4 | 19:56:07 | artifact | wrote EXPERIMENTS/E207-contract-vehicle-analysis/RESULT.md |
| 5 | 19:56:23 | artifact | wrote EXPERIMENTS/E207-contract-vehicle-analysis/e207_vehicle.py |
| 6 | 19:56:36 | artifact | wrote EXPERIMENTS/E207-contract-vehicle-analysis/e207_compare.py |
| 7 | 19:56:48 | artifact | wrote EXPERIMENTS/E207-contract-vehicle-analysis/e207_comparison.json |
| 8 | 19:57:02 | artifact | wrote EXPERIMENTS/E207-contract-vehicle-analysis/e206_api.py |
| 9 | 19:57:18 | artifact | wrote EXPERIMENTS/E207-contract-vehicle-analysis/e206_keywords.py |
| 10 | 20:07:50 | unlogged_change | changed but never declared as an artifact: DECISIONS-NEXT.md |
| 11 | 20:07:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/073-viewcount-prototype-v3/RESULT.md |
| 12 | 20:07:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/223-award-description-terms/PROTOCOL.md |
| 13 | 20:07:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/223-award-description-terms/run.py |
| 14 | 20:07:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/225-answer-distribution/RESULT.md |
| 15 | 20:07:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/225-answer-distribution/run.py |
| 16 | 20:07:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/225-award-description-generalizability/run.py |
| 17 | 20:07:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/226-keyword-disambiguation/PROTOCOL.md |
| 18 | 20:07:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/226-keyword-disambiguation/RESULTS.md |
| 19 | 20:07:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E172-fresh-observation-pypi/PROTOCOL.md |
| 20 | 20:07:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E172-fresh-observation-pypi/RESULT.md |
| 21 | 20:07:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E172-fresh-observation-pypi/run_experiment.py |
| 22 | 20:07:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E173-fresh-observation-github-issues/PROTOCOL.md |
| 23 | 20:07:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E173-fresh-observation-github-issues/RESULT.md |
| 24 | 20:07:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E199-candidate-screen/PROTOCOL.md |
| 25 | 20:07:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E199-candidate-screen/RESULT.md |
| 26 | 20:07:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E199-candidate-screen/raw/7030.json |
| 27 | 20:07:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E199-candidate-screen/raw/7A21.json |
| 28 | 20:07:51 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E199-candidate-screen/raw/D304.json |
| 29 | 20:07:51 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E199-candidate-screen/raw/DA01.json |
| 30 | 20:07:51 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E199-candidate-screen/raw/DA01_all.json |
| 31 | 20:07:51 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E199-candidate-screen/raw/DA10.json |
| 32 | 20:07:51 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E199-candidate-screen/raw/DA10_all.json |
| 33 | 20:07:51 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E200-prototype-7030-validation/PROTOCOL.md |
| 34 | 20:07:51 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E200-prototype-7030-validation/RESULT.md |
| 35 | 20:07:51 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E201-prototype-7030-mvp/PROTOCOL.md |
| 36 | 20:07:51 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E201-prototype-7030-mvp/raw/analyze_7030_recipients.json |
| 37 | 20:07:51 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E201-prototype-7030-mvp/raw/analyze_7030_summary.json |
| 38 | 20:07:51 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E201-prototype-7030-mvp/raw/recip_7030_p1.json |
| 39 | 20:07:51 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E201-prototype-7030-mvp/raw/recip_7030_p1.meta.json |
| 40 | 20:07:51 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E201-prototype-7030-mvp/raw/recip_7030_p10.json |
| 4405 | 20:21:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E203-award-description-categorization/raw/award_DA10_p48.json |
| 4406 | 20:21:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E203-award-description-categorization/raw/award_DA10_p48.meta.json |
| 4407 | 20:21:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E203-award-description-categorization/raw/award_DA10_p49.json |
| 4408 | 20:21:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E203-award-description-categorization/raw/award_DA10_p49.meta.json |
| 4409 | 20:21:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E203-award-description-categorization/raw/award_DA10_p5.json |
| 4410 | 20:21:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E203-award-description-categorization/raw/award_DA10_p5.meta.json |
| 4411 | 20:21:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E203-award-description-categorization/raw/award_DA10_p50.json |
| 4412 | 20:21:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E203-award-description-categorization/raw/award_DA10_p50.meta.json |
| 4413 | 20:21:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E203-award-description-categorization/raw/award_DA10_p6.json |
| 4414 | 20:25:00 | session_end | Completed E207 contract vehicle analysis for all 5 IT/software PSC codes (7030, DA10, 7A21, DA01, D304). Queried USAspending spending_by_award endpoin |

_4364 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-20-006-begin-e207-contract-vehicle-analysis-for/events.jsonl
```
