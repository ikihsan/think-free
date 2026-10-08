# Financial Reconciliation — Falsification Experiment

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-07
-->

## Hypothesis

**H0 (null):** A simple deterministic matching algorithm (exact amount + date window + fuzzy counterparty) cannot achieve useful accuracy on realistic bank reconciliation scenarios compared to the strongest accessible baseline.

**H1 (alternative):** The same algorithm achieves ≥90% precision and ≥85% recall on clean synthetic data, and ≥70% precision and ≥65% recall on messy synthetic data (with typos, date shifts, partial amounts), making it a viable starting point for a tool that reduces manual reconciliation effort.

## Problem Definition

Bank reconciliation: match transactions from a bank statement (external, authoritative) against transactions in an internal accounting ledger (internal, may have timing differences, data entry errors, different descriptions).

**Inputs:**
- Bank transactions: list of {date, amount, description, reference}
- Ledger transactions: list of {date, amount, description, reference, account}

**Output:** Matching pairs + unmatched items on each side, with confidence scores.

**Complications that make this non-trivial:**
1. Date shifts: bank posts 1-3 days after ledger entry
2. Description differences: "STARBUCKS STORE #1234" vs "Starbucks Coffee"
3. Amount differences: bank fees, foreign exchange, split/merged transactions
4. Missing transactions: outstanding checks, deposits in transit
5. Duplicate transactions: double-entry errors

## Baseline: Strongest Accessible Alternative

**Primary baseline:** Manual matching by a human (simulated by the ground truth in synthetic data). This represents what accountants actually do today.

**Secondary baseline:** Simple exact-match on (amount, date) only — the naive approach that fails on real data.

**Tertiary baseline:** OpenRefine's reconciliation against a CSV (configured for financial matching) — if it can be made to work for this use case.

## Synthetic Data Generation

Generate controlled test cases with known ground truth:

### Clean Scenario (100 transactions per side)
- 80 true matches: exact amount, date ±0 days, description exact
- 10 bank-only: fees, interest
- 10 ledger-only: outstanding checks
- No noise

### Realistic Scenario (100 transactions per side)
- 60 clean matches: exact amount, date ±0-1 days, description exact
- 20 fuzzy matches: exact amount, date ±1-3 days, description Levenshtein ≤3
- 10 partial matches: amount differs by known fee (e.g., -$0.30), date ±1 day
- 5 bank-only: fees, interest
- 5 ledger-only: outstanding checks
- 5 split/merged: one bank txn matches two ledger txns (or vice versa)

### Adversarial Scenario (100 transactions per side)
- 40 clean matches
- 20 fuzzy matches (date ±3-5 days, description Levenshtein ≤5)
- 15 partial matches (fees, FX rounding)
- 10 bank-only
- 10 ledger-only
- 5 split/merged

## Algorithm Under Test

**Deterministic greedy matching with scoring:**

For each bank transaction, score all unmatched ledger transactions:
```
score = 0
if abs(bank.amount - ledger.amount) < 0.01: score += 100
elif abs(bank.amount - ledger.amount) < 1.00: score += 50
elif abs(bank.amount - ledger.amount) < 10.00: score += 10

if abs(bank.date - ledger.date) == 0: score += 50
elif abs(bank.date - ledger.date) <= 1: score += 30
elif abs(bank.date - ledger.date) <= 3: score += 15
elif abs(bank.date - ledger.date) <= 5: score += 5

desc_similarity = 1 - (levenshtein(bank.desc, ledger.desc) / max(len(bank.desc), len(ledger.desc)))
score += desc_similarity * 30

reference_match = bank.ref == ledger.ref (if both present)
if reference_match: score += 200
```

Match highest-scoring pairs above threshold (configurable, default 100), remove matched items, repeat until no pairs above threshold.

**Split/merged detection:** After 1:1 matching, check if any unmatched bank txn amount ≈ sum of 2+ unmatched ledger txns (or vice versa) within date window.

## Kill Gate

**The experiment fails (H0 not rejected) if ANY of:**
1. Clean scenario: precision < 90% OR recall < 85%
2. Realistic scenario: precision < 70% OR recall < 65%
3. Adversarial scenario: precision < 50% OR recall < 45%
4. Runtime > 1 second for 1000 transactions (scalability)
5. False positive rate > 10% on any scenario (matching wrong pairs)

**The experiment passes (H0 rejected) if ALL gates pass.**

## Success Metrics

| Metric | Clean | Realistic | Adversarial |
|--------|-------|-----------|-------------|
| Precision | ≥90% | ≥70% | ≥50% |
| Recall | ≥85% | ≥65% | ≥45% |
| F1 | ≥87% | ≥67% | ≥47% |
| False positive rate | <5% | <10% | <15% |
| Runtime (1000 txns) | <1s | <1s | <1s |

## What This Experiment Does NOT Claim

- This is not a complete reconciliation product
- It does not handle multi-currency, complex splits, or learning from user feedback
- It does not claim to replace human review
- It only tests whether the core matching mechanism has enough signal to be worth building on

## Reproduction Command

```bash
cd /home/ubuntu/think-free/EXPERIMENTS/053-financial-reconciliation
python3 run.py --scenario clean --seed 42
python3 run.py --scenario realistic --seed 42
python3 run.py --scenario adversarial --seed 42
```

## Environment

- Python 3.8+ (stdlib only, no external dependencies)
- Deterministic: seeded random generation, no system randomness
- Raw results written to `results.json` with full matching details