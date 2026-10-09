# E080 — Food Recall Purchase Matching Falsification Experiment

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-09
-->

## Hypothesis

**H-01**: A consumer's purchase records (receipts, loyalty exports, manual entry) can be matched against FDA/USDA recall data with sufficient accuracy to warn them of recalled products they own.

**Mechanism**: Match purchase records to recall records using UPC codes, product names, lot numbers, and best-by dates. A match triggers a warning.

**Assumptions**:
1. Purchase records contain sufficient identifiers (UPC, product name, date, store)
2. Recall records contain matchable identifiers (UPC, lot codes, best-by dates, distribution)
3. Matching logic can handle real-world noise (truncated UPCs, store brands, missing lot codes)
4. False alarms (warning on non-recalled products) are more damaging than missed recalls

**Prior Art**: Store loyalty programs (Kroger, Safeway, Costco) notify members of recalls on purchased items. FDA recall API exists. Apps like "Food Recalls" show lists but don't match purchases. The claimed difference: **universal matching across any purchase source**, not store-specific.

**Strongest Objection**: Receipts rarely contain full UPCs or lot codes. Store brands have different UPCs than national brands. Consumers won't manually enter purchases. The matching problem is harder than it appears.

## Kill Gates (predeclared)

All gates must pass for the mechanism to survive. Failure of any gate abandons the direction.

| Gate | Criterion | Rationale |
|------|-----------|-----------|
| **G1 (Precision)** | ≥80% precision on synthetic fixtures: of all matches reported, ≥80% are true recalls | False alarms destroy trust; a tool that cries wolf is worse than none |
| **G2 (Recall)** | ≥60% recall on synthetic fixtures: of all true recalled purchases, ≥60% are detected | Missing recalls defeats the purpose; but some miss is tolerable if precision holds |
| **G3 (Format Coverage)** | ≥2 of 3 purchase formats achieve G1+G2 simultaneously | Must work on real-world formats, not just one ideal format |
| **G4 (Negative Control)** | 0% false matches on purchases with no recall counterpart | Specificity must be perfect on clean negatives; any false positive fails |

## Synthetic Fixtures

Three purchase formats, each with 50 records (25 recalled, 25 not recalled):

1. **Receipt OCR text** — noisy, truncated UPCs, abbreviated names, no lot codes
2. **Loyalty CSV export** — clean UPCs, full names, purchase dates, store IDs
3. **Manual entry** — user-typed names, approximate dates, no UPCs

Recall fixtures: 30 recall records matching FDA schema, covering the 25 recalled purchases across formats.

Ground truth: exact mapping from each purchase to its recall (or none).

## Experiment Design

1. Generate synthetic fixtures with known ground truth
2. Implement matching algorithm (UPC exact → UPC prefix → name fuzzy → lot/date)
3. Run matching on each format independently
4. Compute precision, recall per format and overall
5. Evaluate kill gates
6. Report raw results and verdict

## Reproduction

```bash
cd EXPERIMENTS/080-food-recall-matching
python3 run.py --gate
```

Output: `results.json` with per-format metrics, gate verdicts, and `verdict: PASS|FAIL`.