# Session 2026-10-21-008-integrate-e211-entry-survival-analysis-i

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-21
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-21T06:11:30+00:00
- **Duration:** 22.8s
- **Host:** `instance-20260717-0947`
- **Branch:** `HEAD`

## Goal

Integrate E211 entry survival analysis into E206 integrated CLI tool

## Summary

Completed E211 entry survival analysis integration into E206 CLI. All three PSC codes (7030, DA10, DA01) reproduce E211 exact survival figures: 7030 53.3%/13.8% survival/graduation, DA10 72.6%/41.2%, DA01 69.6%/44.9%. Two-axis recommendation (7030=best entry accessibility, DA10=better for sustained business) displays automatically. Survival module (e206_survival.py) computes UEI-matched survival, graduation, name-est I2 robustness from raw/ data. CLI integration in run.py includes automatic survival analysis and two-axis recommendation. JSON output includes survival data (small_uei_count, survival_pct, graduation_pct, survival_name_est_pct, survival_net_positive_pct, mean/median awards, cross_market). Fixed JSON output key check from small_uei_count to n_cohort. Raw data exists for 3 codes (7030, DA10, DA01) matching E211 protocol.

## Next

Review doc standards and verify no document exceeds 300 lines

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 122 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/e206_survival.py |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/A_7030.json |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/A_DA01.json |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/A_DA10.json |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/B_7030.json |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/B_DA01.json |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/B_DA10.json |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p1.json |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p1.meta.json |
|   undeclared | EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p10.json |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 06:11:30 | session_start | Integrate E211 entry survival analysis into E206 integrated CLI tool |
| 2 | 06:11:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/e206_survival.py |
| 3 | 06:11:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/A_7030.json |
| 4 | 06:11:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/A_DA01.json |
| 5 | 06:11:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/A_DA10.json |
| 6 | 06:11:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/B_7030.json |
| 7 | 06:11:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/B_DA01.json |
| 8 | 06:11:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/B_DA10.json |
| 9 | 06:11:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p1.json |
| 10 | 06:11:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p1.meta.json |
| 11 | 06:11:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p10.json |
| 12 | 06:11:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p10.meta.json |
| 13 | 06:11:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p11.json |
| 14 | 06:11:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p11.meta.json |
| 15 | 06:11:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p12.json |
| 16 | 06:11:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p12.meta.json |
| 17 | 06:11:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p13.json |
| 18 | 06:11:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p13.meta.json |
| 19 | 06:11:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p14.json |
| 20 | 06:11:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p14.meta.json |
| 21 | 06:11:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p15.json |
| 22 | 06:11:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p15.meta.json |
| 23 | 06:11:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p16.json |
| 24 | 06:11:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p16.meta.json |
| 25 | 06:11:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p17.json |
| 26 | 06:11:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p17.meta.json |
| 27 | 06:11:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p18.json |
| 28 | 06:11:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p18.meta.json |
| 29 | 06:11:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p19.json |
| 30 | 06:11:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p19.meta.json |
| 31 | 06:11:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p2.json |
| 32 | 06:11:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p2.meta.json |
| 33 | 06:11:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p20.json |
| 34 | 06:11:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p20.meta.json |
| 35 | 06:11:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p21.json |
| 36 | 06:11:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p21.meta.json |
| 37 | 06:11:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p22.json |
| 38 | 06:11:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p22.meta.json |
| 39 | 06:11:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p23.json |
| 40 | 06:11:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E206-integrated-cli-tool/raw/award_7030_p23.meta.json |
| 115 | 06:11:52 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-003-run-e211-entry-survival-experiment-do-sm/commands.log |
| 116 | 06:11:52 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-003-run-e211-entry-survival-experiment-do-sm/events.jsonl |
| 117 | 06:11:52 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-004-log-artifacts-from-fedmarket-prototype-d/events.jsonl |
| 118 | 06:11:52 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-005-finish-federal-marketplace-assessor-prot/events.jsonl |
| 119 | 06:11:52 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-006-summarize-work-done/events.jsonl |
| 120 | 06:11:52 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-007-continue-think-free-project/events.jsonl |
| 121 | 06:11:52 | unlogged_change | changed but never declared as an artifact: tests/test_docfiles_index.py |
| 122 | 06:11:52 | unlogged_change | changed but never declared as an artifact: tests/test_predirty_attribution.py |
| 123 | 06:11:52 | unlogged_change | changed but never declared as an artifact: tools/originlib/predirty.py |
| 124 | 06:11:53 | session_end | Completed E211 entry survival analysis integration into E206 CLI. All three PSC codes (7030, DA10, DA01) reproduce E211 exact survival figures: 7030 5 |

_74 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-21-008-integrate-e211-entry-survival-analysis-i/events.jsonl
```
