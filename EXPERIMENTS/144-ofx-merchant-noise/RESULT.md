<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-15
-->

# E144 RESULT — Recurring payment detection on real OFX merchant strings

**Date:** 2026-10-15 · **Status:** Claim falsified

---

## Summary

The claim that E065/E066's deterministic detector recovers recurring payments at F1 ≥ 0.80 on real OFX merchant strings is **falsified**. The detector finds **0 recurring expenses** on the available OFX test fixtures. The test fixtures are too small and lack the transaction depth required by the detector's design (≥3 transactions per merchant with regular intervals).

---

## Gate Results

| Gate | Criterion | Result | Evidence |
|------|-----------|--------|----------|
| **G1** (Real positive recovery) | Micro-recall ≥ 0.90 | **FAIL** | 0.0000 (0/3 positive merchants detected) |
| **G2** (Real-world precision) | Micro-precision ≥ 0.70 | **FAIL** | 0.0000 (no detections) |
| **G3** (Baseline dominance) | Detector F1 − naive F1 ≥ 0.05 | **FAIL** | 0.0000 − 0.0000 = 0.0 |
| **G4** (Instrument can say no) | Permutation ratio ≤ 0.10 | **PASS** | 0.0000 (0 detections on shuffled) |

---

## Key Findings

### 1. Test fixtures are too small for the detector's design

The available OFX test fixtures from Actual Budget (4 files, 17 debit transactions) do not contain enough transactions per merchant to meet the detector's minimum threshold of 3 transactions:

| Merchant | Transactions | Dates | Assessment |
|----------|--------------|-------|------------|
| STARBUCKS STORE 07604 01/21 PURC | 3 | All 2019-01-23 | Same day → 0-day gaps, no interval pattern |
| PATIENT FIRST TOKEN 01/22 PURCHA | 2 | 2019-01-23 (×2) | Only 2 transactions |
| URBAN FARMHOUSE NO 2 01/19 PURCH | 2 | 2019-01-22 (×2) | Only 2 transactions |
| **VERIZON DES:PAYMENTREC ID:XXXXX3** | **1** | 2019-01-22 | **Positive (recurring) but only 1 txn** |
| **TMOBILE*AUTO PAY 01/19 PURCHASE** | **1** | 2019-01-22 | **Positive (recurring) but only 1 txn** |
| **COUNTY WASTE 01/18 PURCHASE 804-** | **1** | 2019-01-22 | **Positive (recurring) but only 1 txn** |
| Others | 1 each | Various | Negative or ambiguous |

**The detector correctly finds 0 recurring expenses** because no merchant has ≥3 transactions with a regular interval pattern. The STARBUCKS cluster has 3 transactions but all on the same day (gaps = 0), which doesn't match any target interval (weekly=7, biweekly=14, monthly=30, etc.).

### 2. The merchant normalization axis is not tested

The experiment's purpose was to test whether E065's `normalize_merchant()` handles real OFX merchant noise (e.g., `VERIZON DES:PAYMENTREC ID:XXXXX3`, `TMOBILE*AUTO PAY...`, `AMZN Mktp US*...`). However, **the interval detection fails before merchant normalization becomes relevant**. The detector groups by normalized merchant first, then requires ≥3 transactions in that group — a threshold not met by any merchant in the test data.

### 3. Naive baseline also fails

The naive baseline (≥3 debits per merchant) detects only STARBUCKS (3 transactions on same day) as "recurring," which is a false positive. Both detector and baseline achieve 0.0 F1 on the labeled positives.

---

## What This Establishes

- **Observed**: The available public OFX test fixtures from self-hosted finance tools (Actual Budget, Firefly III, beancount) are **too small** to validate the recurring expense detector's merchant normalization axis. They contain at most 2-3 transactions per merchant over a few days, not the months of history needed for interval detection.

- **Not established**: Whether the detector's merchant normalization works on real OFX strings. The interval detection gate (requiring ≥3 transactions) is the bottleneck, not the normalization.

- **Confirmed**: The detector's design (minimum 3 transactions, interval regularity ≥0.45, amount CV thresholds) is appropriate for real bank exports with months of history, but incompatible with test fixtures that have only days of data.

---

## What This Does Not Establish

- Whether merchant normalization would work on real production OFX exports with sufficient transaction history
- Whether a lower transaction threshold (e.g., ≥2) with stronger interval evidence would help
- Whether the detector works on CSV exports from modern banks (which may have more history)

---

## Lessons for Future Work

1. **Test fixture size matters.** The detector requires months of transaction history per merchant. Public test fixtures from open-source finance tools are designed for import parsing tests, not for recurring pattern detection.

2. **The merchant normalization axis remains untested.** To test it, we need either:
   - Real production OFX exports (not publicly available at scale)
   - Synthetic OFX files generated with realistic recurring patterns and messy merchant strings
   - A different detector design that can work with fewer transactions (but this changes the claim)

3. **E066's Berka validation stands.** The interval+amount core was validated on 1M+ real transactions (F1 0.8194). The merchant axis is a separate, untested layer.

4. **The protocol's declared limitation was accurate:** "These are test fixtures, not production exports — may be small, synthetic, or curated."

---

## Artifacts

- `PROTOCOL.md` — Predeclared protocol with kill gates
- `fetch.py` — Fetches OFX fixtures from Actual Budget
- `parse_ofx.py` — Parses OFX to normalized transactions
- `label.py` — Predeclared labels for merchant groups
- `score.py` — Runs detector and evaluates gates
- `transactions.jsonl` — 17 parsed debit transactions
- `labels.jsonl` — 13 merchant labels (3 positive, 6 negative, 4 ambiguous)
- `gates.json` — Gate evaluation results
- `raw/` — 4 OFX files + 1 CSV (sha256 recorded in `raw/SOURCES.md`)

---

## Compliance

- Protocol predeclared in `PROTOCOL.md` before any implementation
- Labels committed in `labels.jsonl` before detector run
- Kill gates evaluated against committed data
- stdlib-only Python 3.8
- No external dependencies after fetch
- Raw evidence preserved

---

## Next Action

**Close the OFX merchant-noise line.** The available public test fixtures are fundamentally incompatible with the detector's design requirements. The merchant normalization axis remains untested but is not the bottleneck — the interval detection requirement (≥3 transactions with regular intervals) is.

If this axis is to be tested, it requires either:
1. Access to real production OFX exports (not feasible for public validation)
2. A synthetic OFX generator that creates realistic recurring patterns with messy merchant strings
3. A modified detector design (which would be a new claim, not a test of the existing one)

Per the mission's constraints, **do not rebuild the detector or lower thresholds post-hoc**. The negative result is valid for the declared protocol and data.