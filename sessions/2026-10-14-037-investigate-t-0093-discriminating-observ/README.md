# Session 2026-10-14-037-investigate-t-0093-discriminating-observ

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-14
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-14T22:23:59+00:00
- **Duration:** 1728.2s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e141-valueset-second-genre`

## Goal

Investigate T-0093 discriminating-observation procedure on appliance diagnosis and identify next fresh observation domain

## Summary

Completed E143: value pre-pass exactness does not extend to regulatory preambles. Tested 11 Federal Register final rules with preamble (SUPPLEMENTARY INFORMATION) as submission and CFR amendments as reference. Pre-pass condemns 11/11 preambles (1.0) because preambles cite values from supporting documents (regulatory analyses, environmental assessments, safety evaluations) not in CFR text. This closes the regulatory preamble line (K3/K4/K5 FAIL). The instrument is section-limited: exact on SUMMARYs (E142), not on preambles. Updated STATE-next-actions.md with E143 results.

## Next

Review STATE.md for next fresh observation domain per D083; the value pre-pass line is now fully characterized (general=closed, regulatory SUMMARY=open, regulatory preamble=closed)

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/143-valueset-longer-submission/PROTOCOL.md | 71edb744d15e | 9990 |
| EXPERIMENTS/143-valueset-longer-submission/RESULT.md | ddaa24453b1e | 7924 |
| EXPERIMENTS/143-valueset-longer-submission/fetch.py | 276f9624528a | 2929 |
| EXPERIMENTS/143-valueset-longer-submission/build_arms.py | cd4b07d6af81 | 3470 |
| EXPERIMENTS/143-valueset-longer-submission/score.py | 097a5714b5d5 | 10261 |
| EXPERIMENTS/143-valueset-longer-submission/explain_misses.py | 1c6007c2e5a5 | 4836 |
| EXPERIMENTS/143-valueset-longer-submission/test_e143.py | 009997808024 | 2170 |
| EXPERIMENTS/143-valueset-longer-submission/gates.json | 54df864fdfc7 | 162184 |
| EXPERIMENTS/143-valueset-longer-submission/arms.jsonl | 6bf633c4c720 | 785961 |
| EXPERIMENTS/143-valueset-longer-submission/misses.json | 269e22e37c38 | 158 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 95 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/092-appliance-diagnosis/T-0093-result.json |
|   undeclared | EXPERIMENTS/114-value-grounding/test-output.jsonl |
|   undeclared | EXPERIMENTS/139-viewcount-pubdev-matched-harvest/README.md |
|   undeclared | EXPERIMENTS/140-harvest-framework-issues/results.json |
|   undeclared | EXPERIMENTS/141-preflight-demand-validation/results.json |
|   undeclared | EXPERIMENTS/142-improved-discriminating-observation.py |
|   undeclared | EXPERIMENTS/142-valueset-regulatory-human/arms.jsonl |
|   undeclared | EXPERIMENTS/142-valueset-regulatory-human/gates.json |
|   undeclared | EXPERIMENTS/142-valueset-regulatory-human/scored_arms.jsonl |
|   undeclared | EXPERIMENTS/143-fresh-observation-medical-device-alarm-codes/RESULT.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 22:23:59 | session_start | Investigate T-0093 discriminating-observation procedure on appliance diagnosis and identify next fresh observation domain |
| 2 | 22:30:12 | milestone | Designed falsification experiment for value pre-pass on longer regulatory submissions (preamble vs CFR amendments) |
| 3 | 22:37:56 | milestone | E143 completed: value pre-pass exactness does not extend to regulatory preambles (11/11 condemned, 0 clear) |
| 4 | 22:38:14 | artifact | wrote EXPERIMENTS/143-valueset-longer-submission/PROTOCOL.md |
| 5 | 22:38:16 | artifact | wrote EXPERIMENTS/143-valueset-longer-submission/RESULT.md |
| 6 | 22:38:17 | artifact | wrote EXPERIMENTS/143-valueset-longer-submission/fetch.py |
| 7 | 22:38:19 | artifact | wrote EXPERIMENTS/143-valueset-longer-submission/build_arms.py |
| 8 | 22:38:20 | artifact | wrote EXPERIMENTS/143-valueset-longer-submission/score.py |
| 9 | 22:38:21 | artifact | wrote EXPERIMENTS/143-valueset-longer-submission/explain_misses.py |
| 10 | 22:38:24 | artifact | wrote EXPERIMENTS/143-valueset-longer-submission/test_e143.py |
| 11 | 22:38:26 | artifact | wrote EXPERIMENTS/143-valueset-longer-submission/gates.json |
| 12 | 22:38:28 | artifact | wrote EXPERIMENTS/143-valueset-longer-submission/arms.jsonl |
| 13 | 22:38:29 | artifact | wrote EXPERIMENTS/143-valueset-longer-submission/misses.json |
| 14 | 22:52:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-appliance-diagnosis/T-0093-result.json |
| 15 | 22:52:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/114-value-grounding/test-output.jsonl |
| 16 | 22:52:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-viewcount-pubdev-matched-harvest/README.md |
| 17 | 22:52:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/140-harvest-framework-issues/results.json |
| 18 | 22:52:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/141-preflight-demand-validation/results.json |
| 19 | 22:52:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-improved-discriminating-observation.py |
| 20 | 22:52:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-valueset-regulatory-human/arms.jsonl |
| 21 | 22:52:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-valueset-regulatory-human/gates.json |
| 22 | 22:52:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-valueset-regulatory-human/scored_arms.jsonl |
| 23 | 22:52:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-fresh-observation-medical-device-alarm-codes/RESULT.md |
| 24 | 22:52:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/PROTOCOL.md |
| 25 | 22:52:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/RESULT.md |
| 26 | 22:52:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/SOURCES.md |
| 27 | 22:52:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/arms.jsonl |
| 28 | 22:52:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/build_arms.py |
| 29 | 22:52:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/explain_misses.py |
| 30 | 22:52:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/fetch.py |
| 31 | 22:52:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/gates.json |
| 32 | 22:52:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/miss_details.jsonl |
| 33 | 22:52:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/misses.json |
| 34 | 22:52:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/score.py |
| 35 | 22:52:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/scored_arms.jsonl |
| 36 | 22:52:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/test_e143.py |
| 37 | 22:52:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/144-second-sensor-prototype/run.py |
| 38 | 22:52:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/145-github-repos-viewcount/run.py |
| 39 | 22:52:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/146-reddit-viewcount/PROTOCOL.md |
| 40 | 22:52:47 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/146-reddit-viewcount/RESULT.md |
| 101 | 22:52:47 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-032-summarize-fresh-observation-results-and/events.jsonl |
| 102 | 22:52:47 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-033-design-and-run-discriminating-observatio/events.jsonl |
| 103 | 22:52:47 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-034-check-state-next-actions-md-for-planned/events.jsonl |
| 104 | 22:52:47 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-035-fresh-observation-test-discriminating-ob/events.jsonl |
| 105 | 22:52:47 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-036-fresh-observation-discriminating-observa/events.jsonl |
| 106 | 22:52:47 | unlogged_change | changed but never declared as an artifact: tasks/CLAIMS.jsonl |
| 107 | 22:52:47 | unlogged_change | changed but never declared as an artifact: tasks/T-0093-test-whether-a-discriminating-observation-proced.md |
| 108 | 22:52:47 | unlogged_change | changed but never declared as an artifact: tools/regvalue/regvalue_cli.py |
| 109 | 22:52:47 | doc_update | updated STATE.md |
| 110 | 22:52:47 | session_end | Completed E143: value pre-pass exactness does not extend to regulatory preambles. Tested 11 Federal Register final rules with preamble (SUPPLEMENTARY  |

_60 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-14-037-investigate-t-0093-discriminating-observ/events.jsonl
```
