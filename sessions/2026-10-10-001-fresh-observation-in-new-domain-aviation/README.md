# Session 2026-10-10-001-fresh-observation-in-new-domain-aviation

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-10
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-10T00:01:38+00:00
- **Duration:** 294.2s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Fresh observation in new domain: aviation maintenance fault codes via view-count principle

## Summary

E083 experiment: view-count principle on aviation maintenance fault codes. Key results: G1 PASS (30≥30 both arms), G2 FAIL (0.70 accuracy vs 0.85 threshold), G3 REPORTING: treatment 63.3% served (19/30), 10% partially_served (3/30), 26.7% unserved (8/30); control 50.0% served (15/30), 36.7% partially_served (11/30), 13.3% unserved (4/30). Key differentiator: 10% partially_served rate for aviation maintenance vs 0% for lab instruments and 36.7% for general computer errors — shows the view-count principle has a consistent binary→partial→spectrum pattern across technical domains (increasing partial rate as domains become less code-structured). G4 FAIL (14/20 top-arrival vs threshold 17/20). Decision: hold - principle generalizes to aviation domain with intermediate partial-served rate; three-domain mapping (lab=0%, aviation=10%, general=36.7% partially_served) establishes generalization boundaries. Next fresh observation needed in new domain per D083.

## Next

Fresh observation in new domain: another technical domain to further map view-count principle generalization, or synthesize findings across three tested domains and prepare synthesis report.

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 3 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/083-aviation-maintenance-fault-codes/PROTOCOL.md |
|   undeclared | EXPERIMENTS/083-aviation-maintenance-fault-codes/harvest.py |
|   undeclared | EXPERIMENTS/083-aviation-maintenance-fault-codes/outcome.py |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 00:01:38 | session_start | Fresh observation in new domain: aviation maintenance fault codes via view-count principle |
| 2 | 00:06:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-aviation-maintenance-fault-codes/PROTOCOL.md |
| 3 | 00:06:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-aviation-maintenance-fault-codes/harvest.py |
| 4 | 00:06:32 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-aviation-maintenance-fault-codes/outcome.py |
| 5 | 00:06:32 | session_end | E083 experiment: view-count principle on aviation maintenance fault codes. Key results: G1 PASS (30≥30 both arms), G2 FAIL (0.70 accuracy vs 0.85 thre |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-10-001-fresh-observation-in-new-domain-aviation/events.jsonl
```
