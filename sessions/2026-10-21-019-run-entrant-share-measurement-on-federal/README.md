# Session 2026-10-21-019-run-entrant-share-measurement-on-federal

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-21
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-21T12:27:51+00:00
- **Duration:** 1100.2s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e141-valueset-second-genre`

## Goal

Run entrant share measurement on federal IT PSC codes (E209) to test if fragmentation predicts newcomer entry, mirroring E208's NIH SBIR design

## Summary

Ran E209: entrant share measurement on 5 federal IT PSC codes mirroring E208's NIH SBIR design. Found bimodal entry pattern (2 codes closed at 0%, 3 codes enterable at 27-31%). Kill gate G3 fired (ρ=+0.6669, p=0.1345, n=5 too small). Updated STATE.md and STATE-next-actions.md. All artifacts committed to EXPERIMENTS/E209-it-code-entrant-share/.

## Next

Fresh observation in new domain axis per D083, or prototype tool for enterable IT sub-segments (DA01, DA10, 7A21)

## Artifacts

_none_

## Commands

4 captured, 1 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', 'EXPERIMENTS/E209-it-code-entrant-share/fetch.py'] | 0 | 121 |
| 3 | ['python3', 'EXPERIMENTS/E209-it-code-entrant-share/fetch.py'] | 0 | 2081 |
| 4 | ['python3', 'EXPERIMENTS/E209-it-code-entrant-share/analyze.py'] | 1 | 1592 |
| 5 | ['python3', 'EXPERIMENTS/E209-it-code-entrant-share/recompute.py'] | 0 | 1611 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 52 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/PROTOCOL.md |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/PROTOTYPE_SCREEN_PLAN.md |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/PROTOTYPE_SCREEN_RESULTS.md |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/RESULT.md |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/analyze.py |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/controls.py |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/fetch.py |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/gates.json |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/it_code_entrant_screen.py |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/per_category.csv |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 12:27:51 | session_start | Run entrant share measurement on federal IT PSC codes (E209) to test if fragmentation predicts newcomer entry, mirroring E208's NIH SBIR design |
| 2 | 12:31:38 | command | $ python3 EXPERIMENTS/E209-it-code-entrant-share/fetch.py |
| 3 | 12:32:29 | command | $ python3 EXPERIMENTS/E209-it-code-entrant-share/fetch.py |
| 4 | 12:32:41 | command | $ python3 EXPERIMENTS/E209-it-code-entrant-share/analyze.py |
| 5 | 12:34:43 | command | $ python3 EXPERIMENTS/E209-it-code-entrant-share/recompute.py |
| 6 | 12:46:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/PROTOCOL.md |
| 7 | 12:46:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/PROTOTYPE_SCREEN_PLAN.md |
| 8 | 12:46:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/PROTOTYPE_SCREEN_RESULTS.md |
| 9 | 12:46:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/RESULT.md |
| 10 | 12:46:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/analyze.py |
| 11 | 12:46:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/controls.py |
| 12 | 12:46:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/fetch.py |
| 13 | 12:46:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/gates.json |
| 14 | 12:46:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/it_code_entrant_screen.py |
| 15 | 12:46:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/per_category.csv |
| 16 | 12:46:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/probe.py |
| 17 | 12:46:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/analysis.json |
| 18 | 12:46:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/controls.json |
| 19 | 12:46:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/ctl_notacode.json |
| 20 | 12:46:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/ctl_notacode.meta.json |
| 21 | 12:46:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/ctl_zzzz.json |
| 22 | 12:46:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/ctl_zzzz.meta.json |
| 23 | 12:46:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/fetch_summary.json |
| 24 | 12:46:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw_probe.json |
| 25 | 12:46:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/recompute.py |
| 26 | 12:46:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E211-nih-subarea-prototype/RESULT.md |
| 27 | 12:46:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E211-nih-subarea-prototype/nih_subarea_prototype.py |
| 28 | 12:46:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E211-nih-subarea-prototype/raw/analysis.json |
| 29 | 12:46:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E212-nih-sbir-category108-subsegment/nih_category108_screen.py |
| 30 | 12:46:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E212-nih-sbir-category108-subsegment/raw/analysis.json |
| 31 | 12:46:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E213-nih-sbir-category701-subsegment/nih_category701_screen.py |
| 32 | 12:46:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E213-nih-sbir-category701-subsegment/raw/analysis.json |
| 33 | 12:46:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E214-nih-sbir-category525-subsegment/nih_category525_screen.py |
| 34 | 12:46:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E214-nih-sbir-category525-subsegment/raw/analysis.json |
| 35 | 12:46:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/T-0094-viewcount-pypi-tiers/PROTOCOL.md |
| 36 | 12:46:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/T-0094-viewcount-pypi-tiers/RESULT.md |
| 37 | 12:46:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/T-0094-viewcount-pypi-tiers/analysis.json |
| 38 | 12:46:10 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 39 | 12:46:10 | unlogged_change | changed but never declared as an artifact: STATE.md |
| 40 | 12:46:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-003-measure-whether-the-federal-it-psc-codes/commands.log |
| 50 | 12:46:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-011-record-e211-nih-sbir-sub-area-accessibil/events.jsonl |
| 51 | 12:46:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-012-run-e212-experiment-nih-sbir-category-10/events.jsonl |
| 52 | 12:46:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-013-declare-e212-artifacts-and-verify-sessio/events.jsonl |
| 53 | 12:46:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-014-finalize-mission-documentation-and-evide/events.jsonl |
| 54 | 12:46:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-015-complete-t-0094-view-count-principle-tie/events.jsonl |
| 55 | 12:46:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-016-complete-e209-it-code-entrant-measuremen/events.jsonl |
| 56 | 12:46:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-017-complete-e209-it-code-entrant-measuremen/events.jsonl |
| 57 | 12:46:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-018-final-summary-and-continuation-decision/events.jsonl |
| 58 | 12:46:11 | doc_update | updated STATE.md |
| 59 | 12:46:11 | session_end | Ran E209: entrant share measurement on 5 federal IT PSC codes mirroring E208's NIH SBIR design. Found bimodal entry pattern (2 codes closed at 0%, 3 c |

_9 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-21-019-run-entrant-share-measurement-on-federal/events.jsonl
```
