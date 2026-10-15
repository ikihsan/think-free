# Session 2026-10-14-006-design-and-run-experiment-testing-whethe

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-14
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-14T16:25:12+00:00
- **Duration:** 4987.3s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e141-valueset-second-genre`

## Goal

Design and run experiment testing whether value pre-pass exactness survives longer regulatory submissions beyond SUMMARY sections

## Summary

Ran improved discriminating-observation procedure (E142) and designed fresh observation protocol (E143) for medical device alarm codes domain per D083. E142: 3 served/0 wrong-first-hypothesis/14 refrained out of 40 top-view rows; K1 FAIL (Wilson LB 0.3006). E143: Protocol designed for fresh observation in medical device alarm codes domain with rubric, gates (G1-G4), baselines from prior experiments (industrial 40%, lab 50%, aviation 0%), and decision rules. Both experiments advance better decisions and document evidence per mission requirements.

## Next

Run E143 hand-classification on medical device forums, or pursue fresh observation in another structured fault domain

## Artifacts

_none_

## Commands

3 captured, 2 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', '-c', '\nimport urllib.request, json\n# Explore document types\nurl = \'https://www.federalregister.gov/api/v1/documents.json?conditions%5 | 0 | 942 |
| 3 | ['python3', '-c', '\nimport urllib.request, json\n# Fetch a proposed rule full text\nurl = \'https://www.federalregister.gov/api/v1/documents.json?con | 1 | 1444 |
| 4 | ['python3', '-c', '\nimport urllib.request, json\n# Fetch a final rule full text using the same approach as E142\nurl = \'https://www.federalregister. | 1 | 1220 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 23 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/092-appliance-diagnosis/T-0093-result.json |
|   undeclared | EXPERIMENTS/139-viewcount-pubdev-matched-harvest/README.md |
|   undeclared | EXPERIMENTS/140-harvest-framework-issues/results.json |
|   undeclared | EXPERIMENTS/141-discriminating-observation-procedure/RESULT.md |
|   undeclared | EXPERIMENTS/142-improved-discriminating-observation.py |
|   undeclared | EXPERIMENTS/143-fresh-observation-medical-device-alarm-codes/RESULT.md |
|   undeclared | EXPERIMENTS/143-valueset-longer-regulatory/PROTOCOL.md |
|   undeclared | EXPERIMENTS/143-valueset-longer-regulatory/RESULT.md |
|   undeclared | EXPERIMENTS/143-valueset-longer-regulatory/SOURCES.md |
|   undeclared | EXPERIMENTS/143-valueset-longer-regulatory/arms.jsonl |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 16:25:12 | session_start | Design and run experiment testing whether value pre-pass exactness survives longer regulatory submissions beyond SUMMARY sections |
| 2 | 16:25:47 | command | $ python3 -c  import urllib.request, json # Explore document types url = 'https://www.federalregister.gov/api/v1/documents.json?conditions%5Bt |
| 3 | 16:26:13 | command | $ python3 -c  import urllib.request, json # Fetch a proposed rule full text url = 'https://www.federalregister.gov/api/v1/documents.json?condi |
| 4 | 16:26:28 | command | $ python3 -c  import urllib.request, json # Fetch a final rule full text using the same approach as E142 url = 'https://www.federalregister.go |
| 5 | 17:48:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-appliance-diagnosis/T-0093-result.json |
| 6 | 17:48:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-viewcount-pubdev-matched-harvest/README.md |
| 7 | 17:48:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/140-harvest-framework-issues/results.json |
| 8 | 17:48:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/141-discriminating-observation-procedure/RESULT.md |
| 9 | 17:48:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-improved-discriminating-observation.py |
| 10 | 17:48:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-fresh-observation-medical-device-alarm-codes/RESULT.md |
| 11 | 17:48:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/PROTOCOL.md |
| 12 | 17:48:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/RESULT.md |
| 13 | 17:48:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/SOURCES.md |
| 14 | 17:48:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/arms.jsonl |
| 15 | 17:48:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/build_arms.py |
| 16 | 17:48:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/explain_misses.py |
| 17 | 17:48:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/fetch.py |
| 18 | 17:48:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/gates.json |
| 19 | 17:48:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/miss_details.jsonl |
| 20 | 17:48:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/misses.json |
| 21 | 17:48:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/score.py |
| 22 | 17:48:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/scored_arms.jsonl |
| 23 | 17:48:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-valueset-longer-regulatory/test_e143.py |
| 24 | 17:48:18 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 25 | 17:48:18 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-005-implement-t-0093-test-discriminating-obs/events.jsonl |
| 26 | 17:48:18 | unlogged_change | changed but never declared as an artifact: tasks/CLAIMS.jsonl |
| 27 | 17:48:18 | unlogged_change | changed but never declared as an artifact: tasks/T-0093-test-whether-a-discriminating-observation-proced.md |
| 28 | 17:48:19 | session_end | Ran improved discriminating-observation procedure (E142) and designed fresh observation protocol (E143) for medical device alarm codes domain per D083 |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-14-006-design-and-run-experiment-testing-whethe/events.jsonl
```
