# Session 2026-10-21-014-integrate-e211-survival-data-into-e206-c

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-21
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-21T09:18:43+00:00
- **Duration:** 894.8s
- **Host:** `instance-20260717-0947`
- **Branch:** `HEAD`

## Goal

Integrate E211 survival data into E206 CLI tool so it reports both accessibility and sustainability axes from raw data offline

## Summary

Integrated E211 entry survival data into E206 CLI tool. The tool now reports both accessibility and sustainability axes for 7030, DA10, and DA01 from raw/ data offline. Key changes: (1) Copied E211 raw data (A_7030.json, A_DA10.json, A_DA01.json, B_7030.json, B_DA10.json, B_DA01.json, B_6810.json) into E206's raw/ directory. (2) Updated e206_survival.py to load B window data for all codes to enable cross-market analysis (DA10=470, DA01=355, 6810=10 for 7030 cohort). (3) Updated run.py to conditionally run survival analysis only for codes with raw data (7030, DA10, DA01) and display cleaned cohort metrics (survival and graduation for all-small UEIs). (4) Validated outputs: 7030 shows 53.3% survival / 6.5% graduation (cleaned) → easy entry only; DA10 shows 72.6% survival / 32.2% graduation (cleaned) → sustained business pathway; DA01 shows 69.6% survival / 36.6% graduation (cleaned). The two-axis recommendation is now data-driven.

## Next

Run E208 field test with 3-5 small software companies to validate the two-axis framework against real pipeline opportunities (requires authorization). Alternatively, extend the CLI tool with prime-specific subaward trace via /api/v2/subawards/ for Carahsoft/Dell/Leidos/Accenture/GDIT in 7030/DA10.

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 145 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | .fedmarket_cache.db |
|   undeclared | ENHANCEMENT-PLAN.md |
|   undeclared | EXPERIMENTS/091-import-error-population/__pycache__/constants.cpython-38.pyc |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/e206_survival.py |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/A_7030.json |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/A_DA01.json |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/A_DA10.json |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/B_6810.json |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/B_7030.json |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/B_DA01.json |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 09:18:43 | session_start | Integrate E211 survival data into E206 CLI tool so it reports both accessibility and sustainability axes from raw data offline |
| 2 | 09:33:36 | unlogged_change | changed but never declared as an artifact: .fedmarket_cache.db |
| 3 | 09:33:36 | unlogged_change | changed but never declared as an artifact: ENHANCEMENT-PLAN.md |
| 4 | 09:33:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/091-import-error-population/__pycache__/constants.cpython-38.pyc |
| 5 | 09:33:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/e206_survival.py |
| 6 | 09:33:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/A_7030.json |
| 7 | 09:33:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/A_DA01.json |
| 8 | 09:33:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/A_DA10.json |
| 9 | 09:33:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/B_6810.json |
| 10 | 09:33:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/B_7030.json |
| 11 | 09:33:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/B_DA01.json |
| 12 | 09:33:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/B_DA10.json |
| 13 | 09:33:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p1.json |
| 14 | 09:33:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p1.meta.json |
| 15 | 09:33:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p10.json |
| 16 | 09:33:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p10.meta.json |
| 17 | 09:33:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p11.json |
| 18 | 09:33:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p11.meta.json |
| 19 | 09:33:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p12.json |
| 20 | 09:33:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p12.meta.json |
| 21 | 09:33:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p13.json |
| 22 | 09:33:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p13.meta.json |
| 23 | 09:33:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p14.json |
| 24 | 09:33:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p14.meta.json |
| 25 | 09:33:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p15.json |
| 26 | 09:33:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p15.meta.json |
| 27 | 09:33:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p16.json |
| 28 | 09:33:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p16.meta.json |
| 29 | 09:33:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p17.json |
| 30 | 09:33:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p17.meta.json |
| 31 | 09:33:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p18.json |
| 32 | 09:33:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p18.meta.json |
| 33 | 09:33:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p19.json |
| 34 | 09:33:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p19.meta.json |
| 35 | 09:33:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p2.json |
| 36 | 09:33:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p2.meta.json |
| 37 | 09:33:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p20.json |
| 38 | 09:33:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p20.meta.json |
| 39 | 09:33:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p21.json |
| 40 | 09:33:36 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p21.meta.json |
| 139 | 09:33:37 | unlogged_change | changed but never declared as an artifact: tests/test_docfiles_index.py |
| 140 | 09:33:37 | unlogged_change | changed but never declared as an artifact: tests/test_fedmarket.py |
| 141 | 09:33:37 | unlogged_change | changed but never declared as an artifact: tests/test_fedmarket_dynamic.py |
| 142 | 09:33:37 | unlogged_change | changed but never declared as an artifact: tests/test_predirty_attribution.py |
| 143 | 09:33:37 | unlogged_change | changed but never declared as an artifact: tools/originlib/predirty.py |
| 144 | 09:33:37 | unlogged_change | changed but never declared as an artifact: usaspending_assess/__init__.py |
| 145 | 09:33:37 | unlogged_change | changed but never declared as an artifact: usaspending_assess/assess.py |
| 146 | 09:33:37 | unlogged_change | changed but never declared as an artifact: usaspending_assess/cli.py |
| 147 | 09:33:38 | doc_update | updated STATE.md |
| 148 | 09:33:38 | session_end | Integrated E211 entry survival data into E206 CLI tool. The tool now reports both accessibility and sustainability axes for 7030, DA10, and DA01 from  |

_98 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-21-014-integrate-e211-survival-data-into-e206-c/events.jsonl
```
