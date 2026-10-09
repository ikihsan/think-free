# E080 Results — Food Recall Purchase Matching Falsification Experiment

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-09
-->

## Summary

**Verdict: PASS on synthetic fixtures** — The matching mechanism survives the predeclared kill gates on 5/5 random seeds.

**But**: This proves the mechanism works on *idealized synthetic data where recall and purchase records are constructed to share identifiers by design*. It does not establish real-world viability.

## Per-Seed Results

| Seed | Receipt P/R/F1 | Loyalty P/R/F1 | Manual P/R/F1 | Gates Pass |
|------|----------------|----------------|---------------|------------|
| 42   | 1.00/1.00/1.00 | 1.00/1.00/1.00 | 1.00/0.93/0.97 | 12/12 |
| 123  | 1.00/1.00/1.00 | 1.00/1.00/1.00 | 1.00/0.93/0.97 | 12/12 |
| 456  | 1.00/1.00/1.00 | 1.00/1.00/1.00 | 1.00/1.00/1.00 | 12/12 |
| 789  | 1.00/1.00/1.00 | 1.00/1.00/1.00 | 1.00/0.93/0.97 | 12/12 |
| 999  | 1.00/1.00/1.00 | 1.00/1.00/1.00 | 1.00/1.00/1.00 | 12/12 |

All gates (G1 precision ≥80%, G2 recall ≥60%, G3 ≥2 formats, G4 specificity=1.0) pass on every seed.

## Why This Is Not Real-World Validation

### The Synthetic Fixture Construction Guarantees Matchability

1. **Same store → same UPC**: Each recall is generated with a random store. Each purchase for that recall uses the *exact same store*, so UPCs match exactly (loyalty) or via suffix (receipt). Real receipts don't reliably encode store-brand vs national-brand UPCs.

2. **Same lot/date by construction**: The recall's lot code and best-by date are copied directly to the purchase record. Real receipts rarely include lot codes; best-by dates are inconsistent.

3. **Deterministic abbreviations**: Receipt product names use a fixed abbreviation dictionary derived from the same canonical name. Real OCR produces unpredictable truncations, typos, and store-specific codes.

4. **No UPC truncation collisions**: The 8-digit suffix is unique across the 30-product catalog. Real UPC suffixes collide (many products share manufacturer prefix).

5. **Manual entry always has correct name**: 70% of manual entries get the exact canonical name; 30% get the deterministic abbreviation. Real users type "spinach" not "Organic Baby Spinach".

### What Would Be Needed for Real-World Testing

| Gap | Real-World Challenge |
|-----|---------------------|
| UPC coverage | Receipts: 10-30% have UPCs; often truncated to 8-10 digits; store brands ≠ national brands |
| Lot codes | Almost never on receipts; sometimes in loyalty data but inconsistent |
| Product names | OCR errors, store abbreviations, private label names, language variations |
| Purchase dating | Receipt date ≠ purchase date (returns, multi-day trips); loyalty has date but not time |
| Recall data | FDA API has UPC in ~40% of recalls; lot codes in ~60%; distribution patterns vague |
| Store mapping | "Nationwide" recall ≠ all stores; regional recalls poorly specified |

### Prior Art Reality Check

- **Kroger/Safeway/Costco loyalty programs**: Already notify members of recalls on purchased items. They have the purchase UPC + store mapping.
- **FDA recall API**: Public, but UPC field sparsely populated; lot codes inconsistent.
- **Apps (Food Recalls, Recall Watch)**: Show recall lists; don't match purchases.
- **The claimed difference**: "Universal matching across any purchase source" — but without store cooperation, you don't have the purchase UPCs.

## Honest Assessment

| Claim | Status |
|-------|--------|
| "Matching algorithm works" | **Observed true** on synthetic fixtures with perfect identifier linkage |
| "Recall detection feasible" | **Inferred** — mechanism works when identifiers align |
| "Real-world viability" | **Untested** — synthetic fixtures don't capture real noise |
| "Consumer adoption likely" | **Speculative** — no user evidence; loyalty programs already serve this |

## Falsification Status

The experiment **did not falsify** the mechanism — the matching logic correctly identifies recalls when purchase and recall records share identifiers. The kill gates were passed.

However, the experiment **did not validate** the practical hypothesis because the synthetic fixtures encode the very identifier linkage that is the core real-world obstacle.

## Next Steps (If Pursuing)

1. **Real receipt corpus**: Collect 100+ real receipts (OCR + manual ground truth) from diverse stores
2. **Real loyalty exports**: Test with actual Kroger/Safeway/Target CSV exports
3. **FDA recall completeness audit**: Measure UPC/lot/date field coverage in actual recalls
4. **User study**: Would consumers photograph receipts / export loyalty data / manually enter?

## Decision

**Hold** — The mechanism is not falsified, but the practical bottleneck (obtaining matchable purchase identifiers without store cooperation) is unaddressed. This is not a candidate for product engineering. Record as a technical feasibility result only.

---

**Raw results**: `results_seed_42.json` through `results_seed_999.json` in experiment directory.
**Fixtures**: `fixtures_seed_*.json` — reproducible from `fixtures.py` with `random.seed(N)`.
**Code**: `matcher.py`, `run.py` — stdlib only, no dependencies.