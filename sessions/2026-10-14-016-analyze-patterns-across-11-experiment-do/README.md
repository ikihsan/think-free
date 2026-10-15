# Session 2026-10-14-016-analyze-patterns-across-11-experiment-do

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-14
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-14T19:45:39+00:00
- **Duration:** 41.2s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e141-valueset-second-genre`

## Goal

Analyze patterns across 11 experiment domains to identify view-count principle applicability limits

## Summary

Analyzed 11-domain pattern: principle works on 5 domains (PyPI, NPM, Discourse forums, Stack Exchange non-software, Hackage), fails on 9 domains; critical boundary condition: arrival_metadata_required (principle works only on platforms with view_count/download_count); RubyGems_threshold_issue (100% active rate for both need-related and random groups prevents discrimination); E078_classification affects need-related count; hnews_need_classification affects G1 gate. Key finding: classification rubric is critical factor (22/200 vs 100/200 need-related packages). 0 candidates validated across 11 domains.

## Next

review-and-continue

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 40 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/092-appliance-diagnosis/T-0093-result.json |
|   undeclared | EXPERIMENTS/114-value-grounding/test-output.jsonl |
|   undeclared | EXPERIMENTS/139-viewcount-pubdev-matched-harvest/README.md |
|   undeclared | EXPERIMENTS/140-harvest-framework-issues/results.json |
|   undeclared | EXPERIMENTS/142-improved-discriminating-observation.py |
|   undeclared | EXPERIMENTS/143-fresh-observation-medical-device-alarm-codes/RESULT.md |
|   undeclared | EXPERIMENTS/143-valueset-longer-regulatory/PROTOCOL.md |
|   undeclared | EXPERIMENTS/143-valueset-longer-regulatory/RESULT.md |
|   undeclared | EXPERIMENTS/143-valueset-longer-regulatory/SOURCES.md |
|   undeclared | EXPERIMENTS/143-valueset-longer-regulatory/arms.jsonl |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 19:45:39 | session_start | Analyze patterns across 11 experiment domains to identify view-count principle applicability limits |
| 2 | 19:46:20 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-appliance-diagnosis/T-0093-result.json |
| 3 | 19:46:20 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/114-value-grounding/test-output.jsonl |
| 4 | 19:46:20 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-viewcount-pubdev-matched-harvest/README.md |
| 5 | 19:46:20 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/140-harvest-framework-issues/results.json |
| 6 | 19:46:20 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-improved-discriminating-observation.py |
| 7 | 19:46:20 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-fresh-observation-medical-device-alarm-codes/RESULT.md |
| 8 | 19:46:20 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/PROTOCOL.md |
| 9 | 19:46:20 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/RESULT.md |
| 10 | 19:46:20 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/SOURCES.md |
| 11 | 19:46:20 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/arms.jsonl |
| 12 | 19:46:20 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/build_arms.py |
| 13 | 19:46:20 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/explain_misses.py |
| 14 | 19:46:20 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/fetch.py |
| 15 | 19:46:20 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/gates.json |
| 16 | 19:46:20 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/miss_details.jsonl |
| 17 | 19:46:20 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/misses.json |
| 18 | 19:46:20 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/score.py |
| 19 | 19:46:20 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/scored_arms.jsonl |
| 20 | 19:46:20 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/test_e143.py |
| 21 | 19:46:20 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/e103-repro-viewcount/e103_repro.py |
| 22 | 19:46:20 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/e103-repro-viewcount/results.json |
| 23 | 19:46:20 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/viewcount-platform-boundary/e103_vs_e103_comparison.py |
| 24 | 19:46:20 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 25 | 19:46:20 | unlogged_change | changed but never declared as an artifact: checked-output.jsonl |
| 26 | 19:46:20 | unlogged_change | changed but never declared as an artifact: session-record-E142.json |
| 27 | 19:46:20 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-006-design-and-run-experiment-testing-whethe/commands.log |
| 28 | 19:46:20 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-006-design-and-run-experiment-testing-whethe/events.jsonl |
| 29 | 19:46:20 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-007-final-session-recording-and-continuation/events.jsonl |
| 30 | 19:46:20 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-008-evaluate-the-regulatory-value-pre-pass-a/commands.log |
| 31 | 19:46:20 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-008-evaluate-the-regulatory-value-pre-pass-a/events.jsonl |
| 32 | 19:46:20 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-009-complete-regvalue-tool-creation-and-docu/commands.log |
| 33 | 19:46:20 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-009-complete-regvalue-tool-creation-and-docu/events.jsonl |
| 34 | 19:46:20 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-010-close-regulatory-pre-pass-line-and-plan/events.jsonl |
| 35 | 19:46:20 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-011-continue-think-free-autonomous-invention/events.jsonl |
| 36 | 19:46:20 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-012-finish-think-free-session-document-discr/events.jsonl |
| 37 | 19:46:20 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-013-investigate-view-count-principle-platfor/events.jsonl |
| 38 | 19:46:20 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-014-investigate-fresh-observation-domain-for/events.jsonl |
| 39 | 19:46:20 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-015-investigate-fresh-observation-domain-app/events.jsonl |
| 40 | 19:46:20 | unlogged_change | changed but never declared as an artifact: tasks/CLAIMS.jsonl |
| 41 | 19:46:20 | unlogged_change | changed but never declared as an artifact: tasks/T-0093-test-whether-a-discriminating-observation-proced.md |
| 42 | 19:46:20 | session_end | Analyzed 11-domain pattern: principle works on 5 domains (PyPI, NPM, Discourse forums, Stack Exchange non-software, Hackage), fails on 9 domains; crit |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-14-016-analyze-patterns-across-11-experiment-do/events.jsonl
```
