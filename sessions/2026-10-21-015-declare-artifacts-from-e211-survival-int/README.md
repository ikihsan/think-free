# Session 2026-10-21-015-declare-artifacts-from-e211-survival-int

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-21
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-21T09:36:15+00:00
- **Duration:** 194.7s
- **Host:** `instance-20260717-0947`
- **Branch:** `HEAD`

## Goal

Declare artifacts from E211 survival integration into E206 CLI tool

## Summary

Declared artifacts from E211 survival integration: modified e206_survival.py (cross-market analysis, cleaned cohort metrics), modified run.py (conditional survival module, corrected gate thresholds), and copied 7 raw data files from E211 to E206 (A_7030.json, A_DA10.json, A_DA01.json, B_7030.json, B_DA10.json, B_DA01.json, B_6810.json).

## Next

E208 field test with 3-5 small software companies (requires authorization). Or extend CLI tool with prime-specific subaward trace via /api/v2/subawards/ for Carahsoft/Dell/Leidos/Accenture/GDIT in 7030/DA10.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/E206-integrated-cli-tool/e206_survival.py | 5aead897e281 | 7790 |
| EXPERIMENTS/E206-integrated-cli-tool/run.py | 55e518d9e29f | 12980 |
| EXPERIMENTS/E206-integrated-cli-tool/raw/A_7030.json | 6599518ccae8 | 825362 |
| EXPERIMENTS/E206-integrated-cli-tool/raw/A_DA10.json | 2e15ac79cd2d | 471498 |
| EXPERIMENTS/E206-integrated-cli-tool/raw/A_DA01.json | f936ce604603 | 188594 |
| EXPERIMENTS/E206-integrated-cli-tool/raw/B_7030.json | f0ef3d23aa80 | 122251 |
| EXPERIMENTS/E206-integrated-cli-tool/raw/B_DA10.json | e266fda3437b | 294567 |
| EXPERIMENTS/E206-integrated-cli-tool/raw/B_DA01.json | 9bc0601d82ef | 307412 |
| EXPERIMENTS/E206-integrated-cli-tool/raw/B_6810.json | 7b7f2107199f | 67599 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 137 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | .fedmarket_cache.db |
|   undeclared | ENHANCEMENT-PLAN.md |
|   undeclared | EXPERIMENTS/091-import-error-population/__pycache__/constants.cpython-38.pyc |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p1.json |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p1.meta.json |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p10.json |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p10.meta.json |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p11.json |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p11.meta.json |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p12.json |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 09:36:15 | session_start | Declare artifacts from E211 survival integration into E206 CLI tool |
| 2 | 09:36:39 | artifact | wrote EXPERIMENTS/E206-integrated-cli-tool/e206_survival.py |
| 3 | 09:37:01 | artifact | wrote EXPERIMENTS/E206-integrated-cli-tool/run.py |
| 4 | 09:37:19 | artifact | wrote EXPERIMENTS/E206-integrated-cli-tool/raw/A_7030.json |
| 5 | 09:37:36 | artifact | wrote EXPERIMENTS/E206-integrated-cli-tool/raw/A_DA10.json |
| 6 | 09:37:57 | artifact | wrote EXPERIMENTS/E206-integrated-cli-tool/raw/A_DA01.json |
| 7 | 09:38:17 | artifact | wrote EXPERIMENTS/E206-integrated-cli-tool/raw/B_7030.json |
| 8 | 09:38:33 | artifact | wrote EXPERIMENTS/E206-integrated-cli-tool/raw/B_DA10.json |
| 9 | 09:38:55 | artifact | wrote EXPERIMENTS/E206-integrated-cli-tool/raw/B_DA01.json |
| 10 | 09:39:12 | artifact | wrote EXPERIMENTS/E206-integrated-cli-tool/raw/B_6810.json |
| 11 | 09:39:29 | unlogged_change | changed but never declared as an artifact: .fedmarket_cache.db |
| 12 | 09:39:29 | unlogged_change | changed but never declared as an artifact: ENHANCEMENT-PLAN.md |
| 13 | 09:39:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/091-import-error-population/__pycache__/constants.cpython-38.pyc |
| 14 | 09:39:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p1.json |
| 15 | 09:39:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p1.meta.json |
| 16 | 09:39:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p10.json |
| 17 | 09:39:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p10.meta.json |
| 18 | 09:39:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p11.json |
| 19 | 09:39:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p11.meta.json |
| 20 | 09:39:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p12.json |
| 21 | 09:39:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p12.meta.json |
| 22 | 09:39:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p13.json |
| 23 | 09:39:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p13.meta.json |
| 24 | 09:39:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p14.json |
| 25 | 09:39:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p14.meta.json |
| 26 | 09:39:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p15.json |
| 27 | 09:39:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p15.meta.json |
| 28 | 09:39:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p16.json |
| 29 | 09:39:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p16.meta.json |
| 30 | 09:39:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p17.json |
| 31 | 09:39:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p17.meta.json |
| 32 | 09:39:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p18.json |
| 33 | 09:39:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p18.meta.json |
| 34 | 09:39:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p19.json |
| 35 | 09:39:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p19.meta.json |
| 36 | 09:39:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p2.json |
| 37 | 09:39:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p2.meta.json |
| 38 | 09:39:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p20.json |
| 39 | 09:39:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p20.meta.json |
| 40 | 09:39:29 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p21.json |
| 140 | 09:39:29 | unlogged_change | changed but never declared as an artifact: tests/test_docfiles_index.py |
| 141 | 09:39:29 | unlogged_change | changed but never declared as an artifact: tests/test_fedmarket.py |
| 142 | 09:39:29 | unlogged_change | changed but never declared as an artifact: tests/test_fedmarket_dynamic.py |
| 143 | 09:39:29 | unlogged_change | changed but never declared as an artifact: tests/test_predirty_attribution.py |
| 144 | 09:39:29 | unlogged_change | changed but never declared as an artifact: tools/originlib/predirty.py |
| 145 | 09:39:29 | unlogged_change | changed but never declared as an artifact: usaspending_assess/__init__.py |
| 146 | 09:39:29 | unlogged_change | changed but never declared as an artifact: usaspending_assess/assess.py |
| 147 | 09:39:29 | unlogged_change | changed but never declared as an artifact: usaspending_assess/cli.py |
| 148 | 09:39:30 | doc_update | updated STATE.md |
| 149 | 09:39:30 | session_end | Declared artifacts from E211 survival integration: modified e206_survival.py (cross-market analysis, cleaned cohort metrics), modified run.py (conditi |

_99 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-21-015-declare-artifacts-from-e211-survival-int/events.jsonl
```
