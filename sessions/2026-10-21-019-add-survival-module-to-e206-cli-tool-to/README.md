# Session 2026-10-21-019-add-survival-module-to-e206-cli-tool-to

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-21
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-21T12:52:22+00:00
- **Duration:** 1658.4s
- **Host:** `instance-20260717-0947`
- **Branch:** `HEAD`

## Goal

Add survival module to E206 CLI tool to reproduce E211 entry survival metrics from raw data offline, completing the two-axis assessment framework

## Summary

Added survival module to E206 CLI tool. The survival module (e206_survival.py) now reproduces E211 entry survival metrics from raw data offline. Verified against all 3 PSC codes with E211 data (7030, DA10, DA01) - all metrics match E211 baselines exactly. The E206 integrated CLI tool (run.py) now includes 'survival' module option and produces JSON output with survival data. Two-axis recommendation framework is complete with both accessibility and sustainability metrics.

## Next

Run comprehensive E206 validation across all 5 PSC codes with survival module enabled; update STATE.md with results

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 441 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | .fedmarket_cache.db |
|   undeclared | ENHANCEMENT-PLAN.md |
|   undeclared | EXPERIMENTS/091-import-error-population/__pycache__/constants.cpython-38.pyc |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/e206_output.py |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/e206_subaward.py |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/e206_survival.py |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/A_7030.json |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/A_7A21.json |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/A_D304.json |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/A_DA01.json |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 12:52:22 | session_start | Add survival module to E206 CLI tool to reproduce E211 entry survival metrics from raw data offline, completing the two-axis assessment framework |
| 2 | 13:19:50 | unlogged_change | changed but never declared as an artifact: .fedmarket_cache.db |
| 3 | 13:19:50 | unlogged_change | changed but never declared as an artifact: ENHANCEMENT-PLAN.md |
| 4 | 13:19:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/091-import-error-population/__pycache__/constants.cpython-38.pyc |
| 5 | 13:19:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/e206_output.py |
| 6 | 13:19:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/e206_subaward.py |
| 7 | 13:19:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/e206_survival.py |
| 8 | 13:19:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/A_7030.json |
| 9 | 13:19:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/A_7A21.json |
| 10 | 13:19:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/A_D304.json |
| 11 | 13:19:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/A_DA01.json |
| 12 | 13:19:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/A_DA10.json |
| 13 | 13:19:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/B_6810.json |
| 14 | 13:19:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/B_7030.json |
| 15 | 13:19:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/B_7A21.json |
| 16 | 13:19:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/B_D304.json |
| 17 | 13:19:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/B_DA01.json |
| 18 | 13:19:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/B_DA10.json |
| 19 | 13:19:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p1.json |
| 20 | 13:19:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p1.meta.json |
| 21 | 13:19:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p10.json |
| 22 | 13:19:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p10.meta.json |
| 23 | 13:19:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p11.json |
| 24 | 13:19:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p11.meta.json |
| 25 | 13:19:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p12.json |
| 26 | 13:19:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p12.meta.json |
| 27 | 13:19:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p13.json |
| 28 | 13:19:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p13.meta.json |
| 29 | 13:19:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p14.json |
| 30 | 13:19:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p14.meta.json |
| 31 | 13:19:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p15.json |
| 32 | 13:19:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p15.meta.json |
| 33 | 13:19:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p16.json |
| 34 | 13:19:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p16.meta.json |
| 35 | 13:19:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p17.json |
| 36 | 13:19:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p17.meta.json |
| 37 | 13:19:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p18.json |
| 38 | 13:19:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p18.meta.json |
| 39 | 13:19:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p19.json |
| 40 | 13:19:50 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p19.meta.json |
| 435 | 13:20:00 | unlogged_change | changed but never declared as an artifact: tests/test_docfiles_index.py |
| 436 | 13:20:00 | unlogged_change | changed but never declared as an artifact: tests/test_fedmarket.py |
| 437 | 13:20:00 | unlogged_change | changed but never declared as an artifact: tests/test_fedmarket_dynamic.py |
| 438 | 13:20:00 | unlogged_change | changed but never declared as an artifact: tests/test_predirty_attribution.py |
| 439 | 13:20:00 | unlogged_change | changed but never declared as an artifact: tools/originlib/predirty.py |
| 440 | 13:20:00 | unlogged_change | changed but never declared as an artifact: usaspending_assess/__init__.py |
| 441 | 13:20:00 | unlogged_change | changed but never declared as an artifact: usaspending_assess/assess.py |
| 442 | 13:20:00 | unlogged_change | changed but never declared as an artifact: usaspending_assess/cli.py |
| 443 | 13:20:01 | doc_update | updated STATE.md |
| 444 | 13:20:01 | session_end | Added survival module to E206 CLI tool. The survival module (e206_survival.py) now reproduces E211 entry survival metrics from raw data offline. Verif |

_394 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-21-019-add-survival-module-to-e206-cli-tool-to/events.jsonl
```
