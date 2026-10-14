# Session 2026-10-14-004-run-e142-valueset-py-unchanged-on-regula

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-14
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-14T14:06:01+00:00
- **Duration:** 4490.0s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e141-valueset-second-genre`

## Goal

Run E142: valueset.py unchanged on regulatory answers a person wrote (Federal Register final rules and their public comments), measuring conditional coverage, false-positive rate, and the value_present share of misses

## Summary

E139 PX4 Discourse view-count matched-harvest experiment: 150 topics harvested from discuss.px4.io, classified with developer-forum-specific classifier. Results: G1 PASS (100% have view_count > 0), G2 FAIL (58.7% coverage < 60% threshold), G3 FAIL (70.86% unserved fraction upper bound > 60%), G4 PASS (150 topics). Cliff's delta 0.0411 (negligible effect, Mann-Whitney p=0.6704). No candidate generated. Experiment contributes evidence on view-count principle domain-dependence: arrival metric generalizes but coverage boundary and zero-reply metric are domain-specific. Key files produced in EXPERIMENTS/139-px4-discourse-viewcount-matched/: PROTOCOL.md, RESULT.md, fetch_px4.py, classify_px4.py, measure_px4.py, gates.json, results_raw.json, classified.json. Next: evaluate whether to improve classifier coverage, investigate forum differences, or move to new opportunity.

## Next

Decide on continuation direction

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 24 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/139-px4-discourse-viewcount-matched/PROTOCOL.md |
|   undeclared | EXPERIMENTS/139-px4-discourse-viewcount-matched/RESULT.md |
|   undeclared | EXPERIMENTS/139-px4-discourse-viewcount-matched/classified.json |
|   undeclared | EXPERIMENTS/139-px4-discourse-viewcount-matched/classify_px4.py |
|   undeclared | EXPERIMENTS/139-px4-discourse-viewcount-matched/fetch_px4.py |
|   undeclared | EXPERIMENTS/139-px4-discourse-viewcount-matched/gates.json |
|   undeclared | EXPERIMENTS/139-px4-discourse-viewcount-matched/measure_px4.py |
|   undeclared | EXPERIMENTS/139-px4-discourse-viewcount-matched/results_raw.json |
|   undeclared | EXPERIMENTS/142-valueset-regulatory-human/PROTOCOL.md |
|   undeclared | EXPERIMENTS/142-valueset-regulatory-human/RESULT.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 14:06:01 | session_start | Run E142: valueset.py unchanged on regulatory answers a person wrote (Federal Register final rules and their public comments), measuring conditional c |
| 2 | 14:35:56 | milestone | E142 pipeline complete: 20 arms, 0 misses, all gates pass |
| 3 | 15:20:51 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-px4-discourse-viewcount-matched/PROTOCOL.md |
| 4 | 15:20:51 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-px4-discourse-viewcount-matched/RESULT.md |
| 5 | 15:20:51 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-px4-discourse-viewcount-matched/classified.json |
| 6 | 15:20:51 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-px4-discourse-viewcount-matched/classify_px4.py |
| 7 | 15:20:51 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-px4-discourse-viewcount-matched/fetch_px4.py |
| 8 | 15:20:51 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-px4-discourse-viewcount-matched/gates.json |
| 9 | 15:20:51 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-px4-discourse-viewcount-matched/measure_px4.py |
| 10 | 15:20:51 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/139-px4-discourse-viewcount-matched/results_raw.json |
| 11 | 15:20:51 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-valueset-regulatory-human/PROTOCOL.md |
| 12 | 15:20:51 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-valueset-regulatory-human/RESULT.md |
| 13 | 15:20:51 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-valueset-regulatory-human/SOURCES.md |
| 14 | 15:20:51 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-valueset-regulatory-human/arms.jsonl |
| 15 | 15:20:51 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-valueset-regulatory-human/build_arms.py |
| 16 | 15:20:51 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-valueset-regulatory-human/explain_misses.py |
| 17 | 15:20:51 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-valueset-regulatory-human/fetch.py |
| 18 | 15:20:51 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-valueset-regulatory-human/gates.json |
| 19 | 15:20:51 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-valueset-regulatory-human/miss_details.jsonl |
| 20 | 15:20:51 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-valueset-regulatory-human/misses.json |
| 21 | 15:20:51 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-valueset-regulatory-human/score.py |
| 22 | 15:20:51 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-valueset-regulatory-human/scored_arms.jsonl |
| 23 | 15:20:51 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/142-valueset-regulatory-human/test_e142.py |
| 24 | 15:20:51 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 25 | 15:20:51 | unlogged_change | changed but never declared as an artifact: STATE.md |
| 26 | 15:20:51 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-003-land-the-f127-repair-left-uncommitted-by/events.jsonl |
| 27 | 15:20:51 | doc_update | updated STATE.md |
| 28 | 15:20:51 | session_end | E139 PX4 Discourse view-count matched-harvest experiment: 150 topics harvested from discuss.px4.io, classified with developer-forum-specific classifie |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-14-004-run-e142-valueset-py-unchanged-on-regula/events.jsonl
```
