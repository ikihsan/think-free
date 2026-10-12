# Session 2026-10-12-008-explore-and-improve-view-count-classifie

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-12
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-12T08:41:58+00:00
- **Duration:** 2643.7s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Explore and improve view-count classifier coverage (E113 binding constraint)

## Summary

E117 fresh observation: view-count principle on PyPI with keyword cache. ALL GATES PASS (G1-G4): need-related active rate 99.1% vs random 31.6%, ratio 318.8%, 187/200 classified, 13 failures. Key: 100% active rate for need-related group warrants investigation. Advances mission evidence base on view-count principle generalization across PyPI keywords.

## Next

Investigate E117 classifier bias: re-read 20 classified packages to assess need-indicator word-boundary accuracy, then design E118 with modified classifier vocabulary to test generalizability across keywords (per D083 fresh observation in same domain with different classifier approach).

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/E117-viewcount-cache-keyword/classifications.json | 1760f7ec43b5 | 8745 |
| EXPERIMENTS/E117-viewcount-cache-keyword/results.json | 2e14c6dd3c2e | 750 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 30 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | DECISIONS-SCREENING-20.md |
|   undeclared | DECISIONS.md |
|   undeclared | EXPERIMENTS/049-lockfile-closure/analysis.json |
|   undeclared | EXPERIMENTS/113-viewcount-matched-harvest/labeling_improved.py |
|   undeclared | EXPERIMENTS/114-value-grounding/checked_controls_v1.jsonl |
|   undeclared | EXPERIMENTS/114-value-grounding/checked_v1.jsonl |
|   undeclared | EXPERIMENTS/114-value-grounding/checked_v1_full.jsonl |
|   undeclared | EXPERIMENTS/114-value-grounding/controls.jsonl |
|   undeclared | EXPERIMENTS/114-value-grounding/ground.py |
|   undeclared | EXPERIMENTS/116-viewcount-classifier-prototype/PROTOCOL.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 08:41:58 | session_start | Explore and improve view-count classifier coverage (E113 binding constraint) |
| 2 | 09:24:02 | artifact | wrote EXPERIMENTS/E117-viewcount-cache-keyword/classifications.json |
| 3 | 09:24:04 | artifact | wrote EXPERIMENTS/E117-viewcount-cache-keyword/results.json |
| 4 | 09:26:01 | unlogged_change | changed but never declared as an artifact: DECISIONS-SCREENING-20.md |
| 5 | 09:26:01 | unlogged_change | changed but never declared as an artifact: DECISIONS.md |
| 6 | 09:26:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/analysis.json |
| 7 | 09:26:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/113-viewcount-matched-harvest/labeling_improved.py |
| 8 | 09:26:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/114-value-grounding/checked_controls_v1.jsonl |
| 9 | 09:26:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/114-value-grounding/checked_v1.jsonl |
| 10 | 09:26:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/114-value-grounding/checked_v1_full.jsonl |
| 11 | 09:26:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/114-value-grounding/controls.jsonl |
| 12 | 09:26:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/114-value-grounding/ground.py |
| 13 | 09:26:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/116-viewcount-classifier-prototype/PROTOCOL.md |
| 14 | 09:26:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/116-viewcount-classifier-prototype/analyze.py |
| 15 | 09:26:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/116-viewcount-classifier-prototype/classify.py |
| 16 | 09:26:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/116-viewcount-classifier-prototype/results.json |
| 17 | 09:26:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-pypi-viewcount-classifier-prototype/classify.py |
| 18 | 09:26:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/117-pypi-viewcount-classifier-prototype/results.json |
| 19 | 09:26:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/118-pypi-viewcount-matched-harvest/PROTOCOL.md |
| 20 | 09:26:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/118-pypi-viewcount-matched-harvest/classify.py |
| 21 | 09:26:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/118-pypi-viewcount-matched-harvest/results.json |
| 22 | 09:26:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/119-hexpm-viewcount-matched-harvest/PROTOCOL.md |
| 23 | 09:26:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/119-hexpm-viewcount-matched-harvest/classify.py |
| 24 | 09:26:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/119-hexpm-viewcount-matched-harvest/main.py |
| 25 | 09:26:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/119-hexpm-viewcount-matched-harvest/results.json |
| 26 | 09:26:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/e103-viewcount-prototype/results.json |
| 27 | 09:26:01 | unlogged_change | changed but never declared as an artifact: SESSION_OUTCOMES.json |
| 28 | 09:26:01 | unlogged_change | changed but never declared as an artifact: THINK_FREE_SUMMARY.md |
| 29 | 09:26:01 | unlogged_change | changed but never declared as an artifact: pyprovides/pyprovides/known_aliases.py |
| 30 | 09:26:01 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-12-004-test-whether-recurring-payment-detection/events.jsonl |
| 31 | 09:26:01 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-12-005-improve-view-count-classifier-and-docume/events.jsonl |
| 32 | 09:26:01 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-12-006-finalize-pyprovides-prototype-validation/events.jsonl |
| 33 | 09:26:01 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-12-007-run-e119-hex-pm-matched-harvest-experime/events.jsonl |
| 34 | 09:26:02 | doc_update | updated DECISIONS.md |
| 35 | 09:26:02 | session_end | E117 fresh observation: view-count principle on PyPI with keyword cache. ALL GATES PASS (G1-G4): need-related active rate 99.1% vs random 31.6%, ratio |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-12-008-explore-and-improve-view-count-classifie/events.jsonl
```
