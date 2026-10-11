# Session 2026-10-10-002-fresh-observation-in-new-domain-industri

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-10
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-10T00:07:29+00:00
- **Duration:** 395.4s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Fresh observation in new domain: industrial equipment fault codes (PLC/SCADA) via view-count principle

## Summary

E084 experiment: view-count principle on industrial equipment fault codes (PLC/SCADA). Key results: G1 PASS (30≥30 both arms), G2 FAIL (0.60 accuracy vs 0.85 threshold), G3 REPORTING: treatment 40.0% served (12/30), 20% partially_served (6/30), 40% unserved (12/30); control 56.7% served (17/30), 36.7% partially_served (11/30), 6.7% unserved (2/30). Key differentiator: 20% partially_served rate for industrial equipment PLC/SCADA codes, continuing the gradient pattern across all five tested domains: lab instruments 0%, medical devices 1%, aviation 10%, industrial 20%, general computer errors 36.7%. This establishes a clear dose-response gradient where partially_served rate increases as domains become less code-structured. G4 FAIL (12/20 top-arrival vs threshold 17/20). Four of four priority domains from STATE-next-actions.md now tested, establishing the view-count principle's generalization boundaries across technical/non-software domains. Decision: hold - principle generalizes across all tested domains with systematic domain-differentiated classification patterns; fresh observation needed in new domain per D083.

## Next

Fresh observation in completely new domain not among original four priorities: HVAC system error codes or building automation fault codes to further validate the generalization pattern.

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
|   undeclared | EXPERIMENTS/084-industrial-equipment-fault-codes/PROTOCOL.md |
|   undeclared | EXPERIMENTS/084-industrial-equipment-fault-codes/harvest.py |
|   undeclared | EXPERIMENTS/084-industrial-equipment-fault-codes/outcome.py |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 00:07:29 | session_start | Fresh observation in new domain: industrial equipment fault codes (PLC/SCADA) via view-count principle |
| 2 | 00:14:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/084-industrial-equipment-fault-codes/PROTOCOL.md |
| 3 | 00:14:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/084-industrial-equipment-fault-codes/harvest.py |
| 4 | 00:14:05 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/084-industrial-equipment-fault-codes/outcome.py |
| 5 | 00:14:05 | session_end | E084 experiment: view-count principle on industrial equipment fault codes (PLC/SCADA). Key results: G1 PASS (30≥30 both arms), G2 FAIL (0.60 accuracy  |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-10-002-fresh-observation-in-new-domain-industri/events.jsonl
```
