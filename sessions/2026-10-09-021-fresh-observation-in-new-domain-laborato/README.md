# Session 2026-10-09-021-fresh-observation-in-new-domain-laborato

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-09
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-09T23:56:09+00:00
- **Duration:** 18.5s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Fresh observation in new domain: laboratory instrument error codes via view-count principle

## Summary

E081 experiment: view-count principle on laboratory instrument error codes. Key results: G1 PASS (35≥30 both arms), G2 FAIL (0.70 accuracy vs 0.85 threshold, rubric misalignment), G3 REPORTING: treatment 60.0% served (21/35), 0% partially_served; control 57.1% served (20/35), 31.4% partially_served. Key finding: view-count principle generalizes to laboratory instrument error codes with domain-differentiated pattern (binary served/unserved vs mixed partials). Decision: hold - principle not limited to software/Q&A domains, narrows viable candidate space. Fresh observation confirmed in new domain per D083.

## Next

Fresh observation in new domain: medical device alarm codes via view-count principle (priority domain per STATE-next-actions.md). Continue view-count principle generalization mapping across technical domains.

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 6 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/081-lab-instrument-error-codes/PROTOCOL.md |
|   undeclared | EXPERIMENTS/081-lab-instrument-error-codes/harvest.py |
|   undeclared | EXPERIMENTS/081-lab-instrument-error-codes/outcome.py |
|   undeclared | EXPERIMENTS/082-mcu-fault-diagnostics/results.json |
|   undeclared | raw/topics_all.jsonl |
|   undeclared | raw/topics_embedded_forum_placeholder.jsonl |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 23:56:09 | session_start | Fresh observation in new domain: laboratory instrument error codes via view-count principle |
| 2 | 23:56:27 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/081-lab-instrument-error-codes/PROTOCOL.md |
| 3 | 23:56:27 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/081-lab-instrument-error-codes/harvest.py |
| 4 | 23:56:27 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/081-lab-instrument-error-codes/outcome.py |
| 5 | 23:56:27 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/082-mcu-fault-diagnostics/results.json |
| 6 | 23:56:27 | unlogged_change | changed but never declared as an artifact: raw/topics_all.jsonl |
| 7 | 23:56:27 | unlogged_change | changed but never declared as an artifact: raw/topics_embedded_forum_placeholder.jsonl |
| 8 | 23:56:27 | session_end | E081 experiment: view-count principle on laboratory instrument error codes. Key results: G1 PASS (35≥30 both arms), G2 FAIL (0.70 accuracy vs 0.85 thr |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-09-021-fresh-observation-in-new-domain-laborato/events.jsonl
```
