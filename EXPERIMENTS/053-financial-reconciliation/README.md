# Financial Reconciliation — Falsification Experiment Results

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-07
-->

## Experiment Summary

**Experiment ID:** 053-financial-reconciliation  
**Date:** 2026-10-07  
**Status:** Kill gate PASSED on all three scenarios across 5 seeds

## Hypothesis Tested

**H0 (null):** A simple deterministic matching algorithm (exact amount + date window + fuzzy counterparty) cannot achieve useful accuracy on realistic bank reconciliation scenarios compared to the strongest accessible baseline.

**H1 (alternative):** The same algorithm achieves ≥90% precision and ≥85% recall on clean synthetic data, and ≥70% precision and ≥65% recall on messy synthetic data (with typos, date shifts, partial amounts), making it a viable starting point for a tool that reduces manual reconciliation effort.

**Result:** H0 REJECTED. The algorithm passes all kill gates.

## Kill Gate Results

| Scenario | Precision | Recall | F1 | FPR | Gate Threshold | Pass/Fail |
|----------|-----------|--------|-----|-----|----------------|-----------|
| Clean | 1.000 | 1.000 | 1.000 | 0.000 | P≥0.90, R≥0.85, FPR≤0.05 | ✅ PASS |
| Realistic | 1.000 | 0.889 | 0.941 | 0.000 | P≥0.70, R≥0.65, FPR≤0.10 | ✅ PASS |
| Adversarial | 1.000 | 0.787 | 0.881 | 0.000 | P≥0.50, R≥0.45, FPR≤0.15 | ✅ PASS |

All 5 seeds (42, 123, 456, 789, 999) pass on all three scenarios.

## Baseline Comparison

Compared against naive exact-match baseline (amount + date only):

| Scenario | Our F1 | Naive F1 | Improvement |
|----------|--------|----------|-------------|
| Clean | 1.000 | 1.000 | 0.000 (tie) |
| Realistic | 0.941 | 0.861 | +0.080 |
| Adversarial | 0.881 | 0.729 | +0.152 |

Our algorithm significantly outperforms the naive baseline on realistic and adversarial data by handling date shifts, description variations, and split transactions.

## Performance

- **100 transactions:** ~2ms
- **1000 transactions:** ~20ms
- **Kill gate requirement (<1s for 1000):** ✅ PASSED with 50x margin

## Algorithm Design

**Core approach:** Deterministic greedy matching with multi-factor scoring:
1. Amount matching (exact → close ±$1 → loose ±$10)
2. Date matching (exact → ±1 day → ±3 days → ±5 days)
3. Description matching (token-based Jaccard similarity, fast)
4. Reference matching (strong signal when both present)

**Optimizations:**
- Amount indexing (O(1) candidate retrieval)
- Early exit on amount/date mismatch
- Token-based similarity instead of Levenshtein
- Split detection via amount complement indexing

**No external dependencies:** Pure Python standard library.

## Prior Art Check

### User Vocabulary: "bank reconciliation", "bank statement matching", "transaction matching"
- **settlement-engine** (lordisrael1, 5★, 2026): Full Nigerian fintech reconciliation platform with three-way matching (webhook/settlement/bank), double-entry ledger, trust levels, audit trail. TypeScript/PostgreSQL. Heavy infrastructure.
- **Settly** (moniem2020, 2★, 2025): Bank/payment aggregator reconciliation with CSV/PDF upload, fuzzy matching via RapidFuzz, React dashboard. Python/FastAPI.
- **163 GitHub repositories** tagged "bank-reconciliation-engine" — mostly early-stage/student projects (0-5 stars).

### Academic Vocabulary: "record linkage", "entity resolution", "transaction matching", "financial data matching"
- Classic record linkage (Fellegi-Sunter, 1969) — probabilistic framework
- Database entity resolution surveys (Christophides et al., 2020)
- Financial transaction matching in AML/fraud detection literature
- No standard benchmark dataset for bank statement vs ledger reconciliation

### Infrastructure Vocabulary: "reconciliation engine", "matching algorithm", "fuzzy matching"
- **RapidFuzz** — string similarity library used by Settly
- **Polars** — fast DataFrame library used by Settly
- **OpenRefine** — general data reconciliation against external authorities (Wikidata, etc.), not financial
- **dedupe** (Python) — record linkage library, general-purpose

## Difference Statement

**In one sentence:** A lightweight, zero-dependency, deterministic matching library for bank statement vs ledger reconciliation that can be embedded in any Python application, as opposed to full-platform reconciliation systems requiring databases, web services, and complex deployment.

**Why it matters:** Most existing tools are either (a) full ERP/fintech platforms with heavy infrastructure, or (b) general-purpose record linkage libraries requiring ML expertise. There's a gap for a simple, auditable, deterministic matching component that handles the specific quirks of financial reconciliation (date shifts, fee deductions, split transactions) without requiring a data science team.

## Surviving Risks

1. **Clone risk:** The core matching mechanism (amount + date + description scoring) is a well-known pattern in record linkage. The contribution is packaging it for the specific financial reconciliation use case with deterministic, auditable behavior.
2. **Scope risk:** Real bank statements have complexities not in synthetic data: multi-currency, varying date formats, PDF parsing, bank-specific column layouts, running balances.
3. **Adoption risk:** Accountants/bookkeepers may prefer spreadsheet workflows or ERP-built-in tools over a programmable library.
4. **Validation gap:** Synthetic data ≠ real data. The experiment only validates the mechanism on controlled fixtures.

## Information-Sufficiency Test

**Test:** Can two different underlying realities produce identical inputs but require different outputs?

**Construction:**
- Reality A: Bank charge $100.00 on Jan 5, ledger has $100.00 on Jan 5 for "STARBUCKS" — genuine match
- Reality B: Bank charge $100.00 on Jan 5, ledger has $100.00 on Jan 5 for "STARBUCKS" but it's a different transaction (coincidental same amount/date/merchant)

**Result:** The algorithm cannot distinguish these — it would match both. This is correct behavior for a matching tool (it flags for human review), but a fully automated system would need additional signals (references, running balances, sequence).

**Mitigation:** The algorithm produces confidence scores and leaves ambiguous matches for human review. It does not claim full automation.

## Conclusions

1. **Mechanism validated:** The deterministic matching approach has sufficient signal on synthetic data to be worth building on.
2. **Not novel:** The algorithmic approach is standard record linkage adapted to financial domain. The novelty would be in the specific financial heuristics (split detection, fee handling, date windows) and the zero-dependency embeddable design.
3. **Next step for productization:** Test on real bank statement data (CSV/OFX/QFX), add format parsers, build CLI, validate with actual bookkeepers.
4. **Not a standalone candidate yet:** This is a component, not a product. It could be a library contribution to an existing project (e.g., Settly, beancount, hledger) rather than a new repository.

## Raw Results

All raw results saved in `results_seed{42,123,456,789,999}.json` with full matching details.

## Reproduction

```bash
cd /home/ubuntu/think-free/EXPERIMENTS/053-financial-reconciliation
python3 run.py --scenario all --seed 42
python3 baseline.py
```

## Environment

- Python 3.8.10
- No external dependencies
- Deterministic: seeded random generation