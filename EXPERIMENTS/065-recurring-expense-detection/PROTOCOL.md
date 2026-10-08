<!-- origin-meta
owner: docs/INDEX.md
status: complete
last-verified: 2026-10-08
-->

# E065 — Recurring Expense Detection from Bank Transaction CSVs

## Hypothesis

**H0 (null):** A deterministic, stdlib-only algorithm cannot identify recurring expenses (subscriptions, bills, memberships) from raw bank transaction CSV data with sufficient precision and recall to be useful for a person reviewing their spending.

**H1 (alternative):** A deterministic algorithm using only Python stdlib (`csv`, `datetime`, `collections`, `statistics`, `re`) can detect recurring expenses with ≥85% precision and ≥80% recall on a diverse corpus of real and synthetic bank transaction data, while producing ≤5% false positive rate on non-recurring transactions.

## Kill Gate

The experiment is **killed** (do not build) if either:

1. **Precision** < 85% on held-out test set (20 real CSV exports from different banks/people)
2. **Recall** < 80% on held-out test set for known recurring expenses
3. **False positive rate** > 5% on non-recurring transactions in held-out set

If all three gates pass, the mechanism survives and a CLI prototype is the next step.

## Mechanism

Recurring expenses have detectable patterns in transaction streams:
- **Fixed amount** (or amount within small variance, e.g., $9.99 ± $0.01)
- **Regular interval** (monthly, quarterly, annually, weekly, bi-weekly)
- **Consistent merchant/description** (fuzzy match on normalized merchant name)
- **Predictable timing** (same day of month, or same weekday)

Algorithm (deterministic, greedy, no ML):
1. Parse CSV → normalize: date, amount (absolute), merchant (lowercase, strip noise)
2. Group by normalized merchant
3. For each merchant group with ≥3 transactions:
   - Compute interval distribution (days between consecutive transactions)
   - Test for monthly (~28-31 days), quarterly (~89-92), annual (~360-370), weekly (~6-8), bi-weekly (~13-15)
   - Test amount consistency: coefficient of variation < 0.05 (5%)
   - Score = interval_regularity × amount_consistency × transaction_count
4. Threshold: score ≥ 0.7 → recurring candidate
5. Post-filter: remove candidates where interval variance > 5 days (monthly) or amount CV > 0.1
6. Output: merchant, amount, interval, confidence, next expected date

## Corpus

**Development (not for gate):** 10 synthetic CSVs generated from known recurring patterns + noise transactions. 5 real CSV exports from volunteer contributors (with consent, PII redacted).

**Held-out test (gate evaluation):** 20 real CSV exports from different banks (Chase, BoA, Wells Fargo, Citi, credit unions) and different people. Each CSV: 3-12 months, 50-500 transactions. Ground truth: manually labeled recurring vs non-recurring by the account holder.

**Synthetic augmentation:** 100 generated CSVs with known ground truth:
- Clean monthly subscriptions (Netflix, Spotify, gym)
- Variable-amount utilities (electric, gas - same merchant, varying amount)
- Quarterly/annual (insurance, property tax)
- Weekly (grocery delivery, coffee subscription)
- Near-misses: same merchant, irregular intervals; same interval, varying merchants
- False positive traps: recurring Amazon purchases (variable amount/merchant), payroll (same amount, regular, but income)

## Baselines

**Strongest accessible baseline:** Manual human review — a person scrolling through transactions and marking recurring ones. Measured by timing 3 people reviewing the same 5 CSVs and computing their precision/recall against ground truth.

**Naive baseline:** "Same merchant ≥3 times" — no interval or amount checking.

**Rule-based baseline (reference):** `recurring-expenses` npm package logic ported to Python — not run, only cited.

## Experiment Design

### Phase 1: Corpus Acquisition (Day 1)
- Collect 25 real CSV exports with consent (5 dev, 20 test)
- Document each: bank, date range, transaction count, ground truth labels
- Generate 100 synthetic CSVs with known patterns

### Phase 2: Parser & Normalizer (Day 2)
- CSV parser handling: Chase, BoA, Wells Fargo, Citi, generic formats
- Date parsing (multiple formats: MM/DD/YYYY, DD/MM/YYYY, YYYY-MM-DD)
- Amount parsing (handle credits/debits, currency symbols, parentheses for negative)
- Merchant normalization: lowercase, strip trailing numbers/locations, common suffixes (LLC, INC, COM)

### Phase 3: Detection Algorithm (Days 3-4)
- Group by normalized merchant
- Interval analysis: compute gaps, test against target intervals
- Amount consistency: CV, median absolute deviation
- Scoring function with tunable weights
- Threshold tuning on dev set only

### Phase 4: Gate Evaluation (Day 5)
- Run on held-out 20 CSVs
- Measure precision, recall, FPR
- Compare against human baseline on 5 CSVs
- Ablation: test each signal (interval, amount, count) independently

## Acceptance Criteria (Gate Passing)

| Metric | Threshold | Measurement |
|--------|-----------|-------------|
| Precision (held-out) | ≥85% | TP / (TP + FP) on test CSVs |
| Recall (held-out) | ≥80% | TP / (TP + FN) on test CSVs |
| False Positive Rate | ≤5% | FP / (FP + TN) on non-recurring transactions |
| Human baseline precision | Reference | 3 people × 5 CSVs |
| Human baseline recall | Reference | 3 people × 5 CSVs |

## Controls

- **Positive control:** Synthetic CSVs with perfect recurring patterns — must achieve 100% precision/recall
- **Negative control:** Synthetic CSVs with only noise transactions — must produce 0 recurring detections
- **Variable-amount control:** Utility bills (same merchant, varying amount) — should detect as recurring if interval regular, with amount range reported
- **Income control:** Payroll deposits (regular, same amount) — must NOT be flagged as recurring expense (sign filter)
- **Near-duplicate merchant control:** "AMAZON.COM" vs "AMAZON MARKETPLACE" — fuzzy match should group if same entity

## Artifacts to Produce

1. `detect.py` — stdlib-only, <400 lines
2. `normalize.py` — merchant/date/amount normalization
3. `corpus/` — CSVs (gitignored; manifest with SHA256 and source license)
4. `results.json` — per-CSV detection results + gate metrics
5. `human_baseline.json` — human review times and precision/recall
6. `README.md` — reproduction instructions

## Reproduction Command

```bash
cd /home/ubuntu/think-free/EXPERIMENTS/065-recurring-expense-detection
python3 run.py --corpus corpus/manifest.json --gate
```

## Environment

- Python 3.8+
- No external dependencies (stdlib only: csv, datetime, collections, statistics, re, math)
- Corpus CSVs not in git (manifest with hashes only)

## Epistemic Limits

- Corpus diversity limited to volunteered CSVs; may not represent all banks/formats
- Ground truth depends on account holder's memory/labeling
- Synthetic data ≠ real data; gate uses real held-out data
- A passing gate establishes *technical feasibility*, not *product viability* or *adoption*
- Does not handle: split transactions, merged transactions, merchant name changes mid-stream
- Income vs expense distinction relies on sign convention (may vary by bank export)