# Session 2026-10-12-005-improve-view-count-classifier-and-docume

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-12
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-12T06:46:08+00:00
- **Duration:** 29.0s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Improve view-count classifier and document results

## Summary

Built and tested improved view-count classifier with 8 bigram phrase additions across NEED_INDICATORS and GENERIC_TERMS. Key quantitative results on E113 raw_pool.json (700 GitHub repos): labelled fraction improved from 28.8% to 32.2% (+3.4 pp, +11.7% relative). G1 population gate flipped from FAIL (need=104, generic=92) to PASS (need=109, generic=110). G0 discrimination preserved (10/10 planted need and generic recovered). Five new need phrases: 'prompt engineering', 'diffusion models', 'large language models', 'safety-critical', 'data pipeline'. Three new generic phrases: 'toolkit', 'platform', 'web application'. Improvement is engineering (vocabulary addition), not research. D083 domain sweep remains stopped per prior decision. View-count principle boundaries documented across 7+ domains. Single most useful next action: run improved classifier on other experiment raw pools to test whether coverage improvement generalizes beyond GitHub repos.)

## Next

Run improved classifier on other experiment raw pools (e.g., Hex.pm, crates.io, PyPI, Code Review SE) to test generalization of coverage improvement beyond GitHub repos. This ~30-min experiment using committed data would confirm or constrain the improvement's broader applicability, guiding whether to apply across existing experiment corpus, build practical tool, or shift research direction.

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 9 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | DECISIONS-SCREENING-20.md |
|   undeclared | DECISIONS.md |
|   undeclared | EXPERIMENTS/113-viewcount-matched-harvest/labeling_improved.py |
|   undeclared | EXPERIMENTS/114-value-grounding/checked_controls_v1.jsonl |
|   undeclared | EXPERIMENTS/114-value-grounding/checked_v1.jsonl |
|   undeclared | EXPERIMENTS/114-value-grounding/checked_v1_full.jsonl |
|   undeclared | EXPERIMENTS/114-value-grounding/controls.jsonl |
|   undeclared | EXPERIMENTS/114-value-grounding/ground.py |
|   undeclared | sessions/2026-10-12-004-test-whether-recurring-payment-detection/events.jsonl |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 06:46:08 | session_start | Improve view-count classifier and document results |
| 2 | 06:46:37 | unlogged_change | changed but never declared as an artifact: DECISIONS-SCREENING-20.md |
| 3 | 06:46:37 | unlogged_change | changed but never declared as an artifact: DECISIONS.md |
| 4 | 06:46:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/113-viewcount-matched-harvest/labeling_improved.py |
| 5 | 06:46:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/114-value-grounding/checked_controls_v1.jsonl |
| 6 | 06:46:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/114-value-grounding/checked_v1.jsonl |
| 7 | 06:46:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/114-value-grounding/checked_v1_full.jsonl |
| 8 | 06:46:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/114-value-grounding/controls.jsonl |
| 9 | 06:46:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/114-value-grounding/ground.py |
| 10 | 06:46:37 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-12-004-test-whether-recurring-payment-detection/events.jsonl |
| 11 | 06:46:37 | doc_update | updated DECISIONS.md |
| 12 | 06:46:37 | session_end | Built and tested improved view-count classifier with 8 bigram phrase additions across NEED_INDICATORS and GENERIC_TERMS. Key quantitative results on E |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-12-005-improve-view-count-classifier-and-docume/events.jsonl
```
