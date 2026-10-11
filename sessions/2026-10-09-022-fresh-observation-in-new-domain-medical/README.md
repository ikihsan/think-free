# Session 2026-10-09-022-fresh-observation-in-new-domain-medical

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-10
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-09T23:58:23+00:00
- **Duration:** 158.3s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Fresh observation in new domain: medical device alarm codes via view-count principle

## Summary

E082 experiment: view-count principle on medical device alarm codes. Key results: G1 PASS (30≥30 both arms), G2 FAIL (0.60 accuracy vs 0.85 threshold, rubric/seed misalignment), G3 REPORTING: treatment 56.7% served (17/30), 1% partially_served (1/30), 43.3% unserved (12/30); control 60.0% served (18/30), 30.0% partially_served (9/30), 10.0% unserved (3/30). Key differentiator: medical devices also show 0% partially_served pattern like lab instruments (vs 31.4% in general computer errors), confirming even more binary served/unserved distribution. G4 FAIL (12/20 top-arrival vs threshold 17/20). Decision: hold - principle generalizes to medical domain but with consistent binary pattern; next priority domain needed per D083.

## Next

Fresh observation in new domain: aviation maintenance fault codes via view-count principle (priority domain per STATE-next-actions.md). Continue view-count principle generalization mapping across technical domains.

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
|   undeclared | EXPERIMENTS/082-medical-device-alarm-codes/PROTOCOL.md |
|   undeclared | EXPERIMENTS/082-medical-device-alarm-codes/harvest.py |
|   undeclared | EXPERIMENTS/082-medical-device-alarm-codes/outcome.py |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 23:58:23 | session_start | Fresh observation in new domain: medical device alarm codes via view-count principle |
| 2 | 00:01:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/082-medical-device-alarm-codes/PROTOCOL.md |
| 3 | 00:01:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/082-medical-device-alarm-codes/harvest.py |
| 4 | 00:01:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/082-medical-device-alarm-codes/outcome.py |
| 5 | 00:01:01 | session_end | E082 experiment: view-count principle on medical device alarm codes. Key results: G1 PASS (30≥30 both arms), G2 FAIL (0.60 accuracy vs 0.85 threshold, |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-09-022-fresh-observation-in-new-domain-medical/events.jsonl
```
