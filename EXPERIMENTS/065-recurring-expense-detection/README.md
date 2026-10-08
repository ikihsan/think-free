<!-- origin-meta
owner: docs/INDEX.md
status: complete
last-verified: 2026-10-08
-->

# E065 — Recurring Expense Detection from Bank Transaction CSVs

## Experiment Summary

**Experiment ID:** 065-recurring-expense-detection  
**Date:** 2026-10-08  
**Status:** Kill gate PASSED on synthetic corpus

## Hypothesis Tested

**H0 (null):** A deterministic, stdlib-only algorithm cannot identify recurring expenses (subscriptions, bills, memberships) from raw bank transaction CSV data with sufficient precision and recall to be useful for a person reviewing their spending.

**H1 (alternative):** A deterministic algorithm using only Python stdlib (`csv`, `datetime`, `collections`, `statistics`, `re`) can detect recurring expenses with ≥85% precision and ≥80% recall on a diverse corpus of real and synthetic bank transaction data, while producing ≤5% false positive rate on non-recurring transactions.

**Result:** H0 REJECTED. The algorithm passes all kill gates on synthetic data.

## Kill Gate Results

| Metric | Threshold | Actual | Pass/Fail |
|--------|-----------|--------|-----------|
| Precision | ≥85% | 100.00% | ✅ PASS |
| Recall | ≥80% | 83.86% | ✅ PASS |
| False Positive Rate | ≤5% | 0.00% | ✅ PASS |

**Overall: ✅ ALL GATES PASSED**

## Baseline Comparison

Compared against naive baseline (merchant appears ≥3 times):

| Metric | Our Algorithm | Naive Baseline | Improvement |
|--------|---------------|----------------|-------------|
| Precision | 100.00% | 61.75% | +38.25% |
| Recall | 83.86% | 87.71% | -3.85% |
| F1 | 91.22% | 72.47% | **+18.75%** |
| FPR | 0.00% | 99.00% | -99.00% |

Our algorithm dramatically reduces false positives (99% → 0%) while maintaining competitive recall.

## Algorithm Design

**Core approach:** Deterministic multi-factor scoring:

1. **Merchant grouping** — Normalize merchant names (strip store IDs, business suffixes, domain suffixes)
2. **Interval detection** — Test gaps against weekly (7±2), biweekly (14±2), monthly (30±3), quarterly (91±5), semiannual (182±7), annual (365±10)
3. **Amount consistency** — Coefficient of variation (CV) and median absolute deviation
4. **Scoring** — Combined score = interval_regularity × amount_factor × count_factor × interval_bonus
5. **Variable merchant handling** — Utilities (electric, gas, water) get relaxed amount thresholds
6. **Threshold** — Score ≥ 0.5 → recurring candidate

**Optimizations:**
- O(n) single-pass transaction processing
- Amount indexing for candidate retrieval
- Early exit on insufficient transaction count (<3)
- Token-based merchant normalization (no external deps)

**No external dependencies:** Pure Python standard library.

## Corpus

**Synthetic corpus:** 100 CSV files across 4 bank formats (Chase, Bank of America, Wells Fargo, Generic)
- 3-12 months of transactions per file
- 50-500 transactions per file
- 19 recurring merchants with known patterns:
  - Monthly: Netflix, Spotify, Planet Fitness, Adobe, GitHub, Amazon Prime, Disney+, Hulu, Apple, YouTube Premium
  - Quarterly: State Farm, GEICO
  - Annual: Amazon Prime Annual, Costco
  - Weekly: HelloFresh, Blue Apron
  - Variable monthly: PG&E, SCE, City Water Dept
- Income transactions (payroll, freelance) — correctly NOT flagged
- Noise transactions (groceries, gas, restaurants, retail) — correctly NOT flagged

**Ground truth:** Known recurring merchants per file from generation manifest.

## Reproduction

```bash
cd /home/ubuntu/think-free/EXPERIMENTS/065-recurring-expense-detection
python3 run.py --corpus corpus/synthetic --gate --baseline
```

## Artifacts

- `normalize.py` — CSV parsing & merchant/date/amount normalization (4 formats)
- `detect.py` — Recurring expense detection algorithm
- `generate_corpus.py` — Synthetic corpus generator with manifest
- `run.py` — Experiment runner with gate evaluation & baseline comparison
- `corpus/synthetic/` — 100 synthetic CSV files + manifest.json (gitignored)
- `results.json` — Full experiment results

## Environment

- Python 3.8+
- No external dependencies (stdlib only)
- Corpus CSVs not in git (manifest with hashes only)

## Epistemic Limits

- **Synthetic data only:** Gate evaluation uses generated data with known patterns. Real bank CSVs have additional complexities: merchant name variations, split/merged transactions, format inconsistencies, missing fields.
- **No real-world validation:** Has not been tested on actual bank exports from volunteers.
- **Format coverage:** Only 4 common CSV formats tested. Other banks (credit unions, international) may differ.
- **Variable merchant detection:** Keyword-based; may miss utilities with unusual names.
- **Quarterly/annual detection:** Requires ≥3 transactions; short time windows (<9 months) may miss these.
- **Income vs expense:** Relies on sign convention (negative = expense). Some banks export differently.
- **A passing gate establishes technical feasibility, not product viability or adoption.**