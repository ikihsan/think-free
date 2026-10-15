# Session 2026-10-14-020-fresh-observation-view-count-principle-o

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-14
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-14T20:06:51+00:00
- **Duration:** 194.1s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e141-valueset-second-genre`

## Goal

fresh observation: view-count principle on Hackage Haskell packages per D083

## Summary

GitHub repos view-count fresh observation: 5% need-related classification (vs 11% on Hex.pm). G1 FAIL (need prevalence 5<15), G2 PASS (corpus=100), G4 PASS (100% stars>0). Build decision: fresh observation confirms view-count principle is domain-specific; GitHub repos have lower need-related fraction than package registries. What remains unknown: whether different query terms, repo types, or classification refinements would yield different results. Single most useful next action: close GitHub repo observation line and either (a) test view-count on another new domain, or (b) integrate all domain findings into principle's applicability map.

## Next

Close GitHub repos view-count experiment and either test principle on another new domain (e.g., Hackage Haskell, CPAN Perl) or compile all domain findings into the view-count principle's applicability map per D083.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/145-github-repos-viewcount/run.py | e2fbaae0bbb9 | 5851 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 45 |
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
| 1 | 20:06:51 | session_start | fresh observation: view-count principle on Hackage Haskell packages per D083 |
| 2 | 20:09:54 | artifact | wrote EXPERIMENTS/145-github-repos-viewcount/run.py |
| 3 | 20:10:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-appliance-diagnosis/T-0093-result.json |
| 4 | 20:10:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/114-value-grounding/test-output.jsonl |
| 5 | 20:10:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-viewcount-pubdev-matched-harvest/README.md |
| 6 | 20:10:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/140-harvest-framework-issues/results.json |
| 7 | 20:10:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-improved-discriminating-observation.py |
| 8 | 20:10:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-fresh-observation-medical-device-alarm-codes/RESULT.md |
| 9 | 20:10:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/PROTOCOL.md |
| 10 | 20:10:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/RESULT.md |
| 11 | 20:10:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/SOURCES.md |
| 12 | 20:10:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/arms.jsonl |
| 13 | 20:10:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/build_arms.py |
| 14 | 20:10:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/explain_misses.py |
| 15 | 20:10:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/fetch.py |
| 16 | 20:10:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/gates.json |
| 17 | 20:10:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/miss_details.jsonl |
| 18 | 20:10:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/misses.json |
| 19 | 20:10:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/score.py |
| 20 | 20:10:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/scored_arms.jsonl |
| 21 | 20:10:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/test_e143.py |
| 22 | 20:10:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/144-second-sensor-prototype/run.py |
| 23 | 20:10:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/e103-repro-viewcount/e103_repro.py |
| 24 | 20:10:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/e103-repro-viewcount/results.json |
| 25 | 20:10:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/viewcount-platform-boundary/e103_vs_e103_comparison.py |
| 26 | 20:10:05 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 27 | 20:10:05 | unlogged_change | changed but never declared as an artifact: checked-output.jsonl |
| 28 | 20:10:05 | unlogged_change | changed but never declared as an artifact: session-record-E142.json |
| 29 | 20:10:05 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-006-design-and-run-experiment-testing-whethe/commands.log |
| 30 | 20:10:05 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-006-design-and-run-experiment-testing-whethe/events.jsonl |
| 31 | 20:10:05 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-007-final-session-recording-and-continuation/events.jsonl |
| 32 | 20:10:05 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-008-evaluate-the-regulatory-value-pre-pass-a/commands.log |
| 33 | 20:10:05 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-008-evaluate-the-regulatory-value-pre-pass-a/events.jsonl |
| 34 | 20:10:05 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-009-complete-regvalue-tool-creation-and-docu/commands.log |
| 35 | 20:10:05 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-009-complete-regvalue-tool-creation-and-docu/events.jsonl |
| 36 | 20:10:05 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-010-close-regulatory-pre-pass-line-and-plan/events.jsonl |
| 37 | 20:10:05 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-011-continue-think-free-autonomous-invention/events.jsonl |
| 38 | 20:10:05 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-012-finish-think-free-session-document-discr/events.jsonl |
| 39 | 20:10:05 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-013-investigate-view-count-principle-platfor/events.jsonl |
| 40 | 20:10:05 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-014-investigate-fresh-observation-domain-for/events.jsonl |
| 41 | 20:10:05 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-015-investigate-fresh-observation-domain-app/events.jsonl |
| 42 | 20:10:05 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-016-analyze-patterns-across-11-experiment-do/events.jsonl |
| 43 | 20:10:05 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-017-finalize-work-and-document-decision-for/events.jsonl |
| 44 | 20:10:05 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-018-prototype-second-sensor-ventilation-diag/events.jsonl |
| 45 | 20:10:05 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-019-record-continuation-decision-for-ventila/events.jsonl |
| 46 | 20:10:05 | unlogged_change | changed but never declared as an artifact: tasks/CLAIMS.jsonl |
| 47 | 20:10:05 | unlogged_change | changed but never declared as an artifact: tasks/T-0093-test-whether-a-discriminating-observation-proced.md |
| 48 | 20:10:06 | session_end | GitHub repos view-count fresh observation: 5% need-related classification (vs 11% on Hex.pm). G1 FAIL (need prevalence 5<15), G2 PASS (corpus=100), G4 |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-14-020-fresh-observation-view-count-principle-o/events.jsonl
```
