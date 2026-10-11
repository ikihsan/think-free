# Session 2026-10-09-018-fresh-observation-in-a-new-domain-per-d0

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-09
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-09T21:34:36+00:00
- **Duration:** 1010.2s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Fresh observation in a new domain per D083 - explore an unmeasured practical difficulty

## Summary

E080 food recall purchase matching falsification experiment completed. Mechanism passes all predeclared kill gates (G1 precision≥80%, G2 recall≥60%, G3 ≥2 formats, G4 specificity=1.0) on 5/5 random seeds with synthetic fixtures. However, fixtures guarantee identifier linkage (same store→same UPC, same lot/date) that is the core real-world obstacle. Receipts rarely have UPCs/lot codes; store brands use different UPCs; FDA recall data has sparse UPC coverage. Loyalty programs (Kroger, Costco) already solve this for members. Verdict: hold — technical feasibility shown, practical viability untested. No candidate advanced.

## Next

Fresh observation in another new domain per D083; the food recall matching mechanism survives synthetic falsification but the identifier linkage problem is the hard part. Next session should explore a different practical difficulty.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/080-food-recall-matching/PROTOCOL.md | 5443b230da19 | 3302 |
| EXPERIMENTS/080-food-recall-matching/fixtures.py | fda411e764a5 | 16853 |
| EXPERIMENTS/080-food-recall-matching/matcher.py | 23166bcebf5a | 8402 |
| EXPERIMENTS/080-food-recall-matching/run.py | 34334cd6aedf | 6310 |
| EXPERIMENTS/080-food-recall-matching/RESULTS.md | 89bcf1c51e29 | 5209 |
| EXPERIMENTS/080-food-recall-matching/results.json | d58bda2f1b5a | 1344 |
| EXPERIMENTS/080-food-recall-matching/fixtures/ground_truth.json | 9e3e323f62ce | 1892 |
| EXPERIMENTS/080-food-recall-matching/fixtures/purchases_loyalty_csv.json | 87f001cc7d1d | 8628 |
| EXPERIMENTS/080-food-recall-matching/fixtures/purchases_manual_entry.json | 00fde3759fee | 7818 |
| EXPERIMENTS/080-food-recall-matching/fixtures/purchases_receipt.json | 5d99403a6421 | 8089 |
| EXPERIMENTS/080-food-recall-matching/fixtures/recalls.json | 78b3cb524ec6 | 5681 |

## Commands

5 captured, 2 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', 'EXPERIMENTS/080-food-recall-matching/run.py', '--generate-fixtures', 'EXPERIMENTS/080-food-recall-matching/fixtures'] | 1 | 811 |
| 3 | ['python3', 'EXPERIMENTS/080-food-recall-matching/run.py', '--generate-fixtures', 'EXPERIMENTS/080-food-recall-matching/fixtures'] | 0 | 233 |
| 4 | ['python3', 'EXPERIMENTS/080-food-recall-matching/run.py', '--fixtures', 'EXPERIMENTS/080-food-recall-matching/fixtures'] | 1 | 301 |
| 5 | ['python3', 'EXPERIMENTS/080-food-recall-matching/run.py', '--generate-fixtures', 'EXPERIMENTS/080-food-recall-matching/fixtures'] | 0 | 297 |
| 6 | ['python3', 'EXPERIMENTS/080-food-recall-matching/run.py', '--fixtures', 'EXPERIMENTS/080-food-recall-matching/fixtures'] | 0 | 241 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 25 |
| declared artifacts now missing | 0 |
| integrity errors | 3 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/080-food-recall-matching/fixtures_seed_123/ground_truth.json |
|   undeclared | EXPERIMENTS/080-food-recall-matching/fixtures_seed_123/purchases_loyalty_csv.json |
|   undeclared | EXPERIMENTS/080-food-recall-matching/fixtures_seed_123/purchases_manual_entry.json |
|   undeclared | EXPERIMENTS/080-food-recall-matching/fixtures_seed_123/purchases_receipt.json |
|   undeclared | EXPERIMENTS/080-food-recall-matching/fixtures_seed_123/recalls.json |
|   undeclared | EXPERIMENTS/080-food-recall-matching/fixtures_seed_42/ground_truth.json |
|   undeclared | EXPERIMENTS/080-food-recall-matching/fixtures_seed_42/purchases_loyalty_csv.json |
|   undeclared | EXPERIMENTS/080-food-recall-matching/fixtures_seed_42/purchases_manual_entry.json |
|   undeclared | EXPERIMENTS/080-food-recall-matching/fixtures_seed_42/purchases_receipt.json |
|   undeclared | EXPERIMENTS/080-food-recall-matching/fixtures_seed_42/recalls.json |
|   error | DECISIONS.md was not updated although the session recorded decision |
|   error | FAILURES.md was not updated although the session recorded experiment_result |
|   error | HYPOTHESES.md was not updated although the session recorded experiment_result |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 21:34:36 | session_start | Fresh observation in a new domain per D083 - explore an unmeasured practical difficulty |
| 2 | 21:44:36 | command | $ python3 EXPERIMENTS/080-food-recall-matching/run.py --generate-fixtures EXPERIMENTS/080-food-recall-matching/fixtures |
| 3 | 21:47:08 | command | $ python3 EXPERIMENTS/080-food-recall-matching/run.py --generate-fixtures EXPERIMENTS/080-food-recall-matching/fixtures |
| 4 | 21:47:14 | command | $ python3 EXPERIMENTS/080-food-recall-matching/run.py --fixtures EXPERIMENTS/080-food-recall-matching/fixtures |
| 5 | 21:48:28 | command | $ python3 EXPERIMENTS/080-food-recall-matching/run.py --generate-fixtures EXPERIMENTS/080-food-recall-matching/fixtures |
| 6 | 21:48:37 | command | $ python3 EXPERIMENTS/080-food-recall-matching/run.py --fixtures EXPERIMENTS/080-food-recall-matching/fixtures |
| 7 | 21:50:18 | artifact | wrote EXPERIMENTS/080-food-recall-matching/PROTOCOL.md |
| 8 | 21:50:19 | artifact | wrote EXPERIMENTS/080-food-recall-matching/fixtures.py |
| 9 | 21:50:20 | artifact | wrote EXPERIMENTS/080-food-recall-matching/matcher.py |
| 10 | 21:50:21 | artifact | wrote EXPERIMENTS/080-food-recall-matching/run.py |
| 11 | 21:50:22 | artifact | wrote EXPERIMENTS/080-food-recall-matching/RESULTS.md |
| 12 | 21:50:24 | artifact | wrote EXPERIMENTS/080-food-recall-matching/results.json |
| 13 | 21:50:31 | artifact | wrote EXPERIMENTS/080-food-recall-matching/fixtures/ground_truth.json |
| 14 | 21:50:32 | artifact | wrote EXPERIMENTS/080-food-recall-matching/fixtures/purchases_loyalty_csv.json |
| 15 | 21:50:33 | artifact | wrote EXPERIMENTS/080-food-recall-matching/fixtures/purchases_manual_entry.json |
| 16 | 21:50:34 | artifact | wrote EXPERIMENTS/080-food-recall-matching/fixtures/purchases_receipt.json |
| 17 | 21:50:35 | artifact | wrote EXPERIMENTS/080-food-recall-matching/fixtures/recalls.json |
| 18 | 21:50:42 | decision | E080 food recall matching passes synthetic kill gates but real-world identifier linkage is the unaddressed bottleneck; hold as technical feasibility o |
| 19 | 21:51:12 | experiment_result | PASS on synthetic fixtures (5/5 seeds); mechanism works when identifiers align but real-world UPC/lot/date linkage is the open problem |
| 20 | 21:51:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/080-food-recall-matching/fixtures_seed_123/ground_truth.json |
| 21 | 21:51:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/080-food-recall-matching/fixtures_seed_123/purchases_loyalty_csv.json |
| 22 | 21:51:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/080-food-recall-matching/fixtures_seed_123/purchases_manual_entry.json |
| 23 | 21:51:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/080-food-recall-matching/fixtures_seed_123/purchases_receipt.json |
| 24 | 21:51:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/080-food-recall-matching/fixtures_seed_123/recalls.json |
| 25 | 21:51:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/080-food-recall-matching/fixtures_seed_42/ground_truth.json |
| 26 | 21:51:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/080-food-recall-matching/fixtures_seed_42/purchases_loyalty_csv.json |
| 27 | 21:51:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/080-food-recall-matching/fixtures_seed_42/purchases_manual_entry.json |
| 28 | 21:51:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/080-food-recall-matching/fixtures_seed_42/purchases_receipt.json |
| 29 | 21:51:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/080-food-recall-matching/fixtures_seed_42/recalls.json |
| 30 | 21:51:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/080-food-recall-matching/fixtures_seed_456/ground_truth.json |
| 31 | 21:51:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/080-food-recall-matching/fixtures_seed_456/purchases_loyalty_csv.json |
| 32 | 21:51:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/080-food-recall-matching/fixtures_seed_456/purchases_manual_entry.json |
| 33 | 21:51:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/080-food-recall-matching/fixtures_seed_456/purchases_receipt.json |
| 34 | 21:51:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/080-food-recall-matching/fixtures_seed_456/recalls.json |
| 35 | 21:51:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/080-food-recall-matching/fixtures_seed_789/ground_truth.json |
| 36 | 21:51:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/080-food-recall-matching/fixtures_seed_789/purchases_loyalty_csv.json |
| 37 | 21:51:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/080-food-recall-matching/fixtures_seed_789/purchases_manual_entry.json |
| 38 | 21:51:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/080-food-recall-matching/fixtures_seed_789/purchases_receipt.json |
| 39 | 21:51:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/080-food-recall-matching/fixtures_seed_789/recalls.json |
| 40 | 21:51:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/080-food-recall-matching/fixtures_seed_999/ground_truth.json |
| 41 | 21:51:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/080-food-recall-matching/fixtures_seed_999/purchases_loyalty_csv.json |
| 42 | 21:51:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/080-food-recall-matching/fixtures_seed_999/purchases_manual_entry.json |
| 43 | 21:51:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/080-food-recall-matching/fixtures_seed_999/purchases_receipt.json |
| 44 | 21:51:26 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/080-food-recall-matching/fixtures_seed_999/recalls.json |
| 45 | 21:51:26 | integrity_error | DECISIONS.md was not updated although the session recorded decision |
| 46 | 21:51:26 | integrity_error | FAILURES.md was not updated although the session recorded experiment_result |
| 47 | 21:51:26 | integrity_error | HYPOTHESES.md was not updated although the session recorded experiment_result |
| 48 | 21:51:26 | session_end | E080 food recall purchase matching falsification experiment completed. Mechanism passes all predeclared kill gates (G1 precision≥80%, G2 recall≥60%, G |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-09-018-fresh-observation-in-a-new-domain-per-d0/events.jsonl
```
