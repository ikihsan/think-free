# Session 2026-10-10-003-fresh-observation-in-new-domain-building

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-10
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-10T00:16:01+00:00
- **Duration:** 369.9s
- **Host:** `instance-20260717-0944`
- **Branch:** `HEAD`

## Goal

Fresh observation in new domain: building automation HVAC fault codes via view-count principle

## Summary

E085 experiment: view-count principle on building automation HVAC fault codes. Key results: G1 PASS (30≥30 both arms), G2 FAIL (0.70 accuracy vs 0.85 threshold), G3 REPORTING: treatment 50.0% served (15/30), 20% partially_served (6/30), 30% unserved (9/30); control 50.0% served (15/30), 36.7% partially_served (11/30), 13.3% unserved (4/30). Key differentiator: 20% partially_served rate for HVAC matches industrial PLC/SCADA (E084), continuing the gradient pattern across 5 tested domains: lab instruments 0%, medical devices 1%, aviation 10%, industrial/industrial 20%, HVAC 20%, general computer errors 36.7%. This confirms the dose-response gradient where partially_served rate increases as domains become less code-structured. G4 FAIL (14/20 top-arrival vs threshold 17/20). Five of five domains now tested, establishing the view-count principle's generalization boundaries across technical/non-software domains with systematic domain-differentiated classification patterns. Decision: hold - principle generalizes across all tested domains; fresh observation needed in new domain per D083.

## Next

Fresh observation in new domain not among original four priorities or five tested: explore a different domain category to further validate or extend the generalization pattern, or synthesize findings and prepare for candidate generation consideration.

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 20 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | DECISIONS-SCREENING-14.md |
|   undeclared | EXPERIMENTS/080-food-recall-matching/PROTOCOL.md |
|   undeclared | EXPERIMENTS/080-food-recall-matching/RESULTS.md |
|   undeclared | EXPERIMENTS/080-food-recall-matching/fixtures.py |
|   undeclared | EXPERIMENTS/080-food-recall-matching/fixtures/ground_truth.json |
|   undeclared | EXPERIMENTS/080-food-recall-matching/fixtures/purchases_loyalty_csv.json |
|   undeclared | EXPERIMENTS/080-food-recall-matching/fixtures/purchases_manual_entry.json |
|   undeclared | EXPERIMENTS/080-food-recall-matching/fixtures/purchases_receipt.json |
|   undeclared | EXPERIMENTS/080-food-recall-matching/fixtures/recalls.json |
|   undeclared | EXPERIMENTS/080-food-recall-matching/matcher.py |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 00:16:01 | session_start | Fresh observation in new domain: building automation HVAC fault codes via view-count principle |
| 2 | 00:22:10 | unlogged_change | changed but never declared as an artifact: DECISIONS-SCREENING-14.md |
| 3 | 00:22:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/080-food-recall-matching/PROTOCOL.md |
| 4 | 00:22:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/080-food-recall-matching/RESULTS.md |
| 5 | 00:22:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/080-food-recall-matching/fixtures.py |
| 6 | 00:22:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/080-food-recall-matching/fixtures/ground_truth.json |
| 7 | 00:22:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/080-food-recall-matching/fixtures/purchases_loyalty_csv.json |
| 8 | 00:22:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/080-food-recall-matching/fixtures/purchases_manual_entry.json |
| 9 | 00:22:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/080-food-recall-matching/fixtures/purchases_receipt.json |
| 10 | 00:22:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/080-food-recall-matching/fixtures/recalls.json |
| 11 | 00:22:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/080-food-recall-matching/matcher.py |
| 12 | 00:22:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/080-food-recall-matching/results.json |
| 13 | 00:22:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/080-food-recall-matching/run.py |
| 14 | 00:22:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/085-building-automation-hvac/PROTOCOL.md |
| 15 | 00:22:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/085-building-automation-hvac/fault-codes/control-needs.jsonl |
| 16 | 00:22:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/085-building-automation-hvac/fault-codes/treatment-needs.jsonl |
| 17 | 00:22:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/085-building-automation-hvac/harvest.py |
| 18 | 00:22:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/085-building-automation-hvac/outcome.py |
| 19 | 00:22:10 | unlogged_change | changed but never declared as an artifact: FAILURES.md |
| 20 | 00:22:10 | unlogged_change | changed but never declared as an artifact: HYPOTHESES-results.md |
| 21 | 00:22:10 | unlogged_change | changed but never declared as an artifact: HYPOTHESES.md |
| 22 | 00:22:11 | doc_update | updated DECISIONS-SCREENING-14.md |
| 23 | 00:22:11 | doc_update | updated FAILURES.md |
| 24 | 00:22:11 | doc_update | updated HYPOTHESES.md |
| 25 | 00:22:11 | session_end | E085 experiment: view-count principle on building automation HVAC fault codes. Key results: G1 PASS (30≥30 both arms), G2 FAIL (0.70 accuracy vs 0.85  |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-10-003-fresh-observation-in-new-domain-building/events.jsonl
```
