<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-14
-->

# E147 RESULT — PostgreSQL deadlock report root cause classification

**Date:** 2026-10-14 · **Status:** Claim falsified

---

## Summary

The claim that a structural classifier beats a keyword baseline by ≥15pp on PostgreSQL deadlock report classification is **falsified**. The keyword-only baseline achieves 100% accuracy on the 27 synthetic fixtures, while the structural classifier achieves 74.1%. All kill gates evaluating the structural advantage fail.

---

## Gate Results

| Gate | Criterion | Result | Evidence |
|------|-----------|--------|----------|
| **G1** (Fixture validity) | All 25 fixtures correctly labelled by construction | **PASS** | 27 fixtures, all labelled by construction |
| **G2** (Beats keyword baseline) | Structural accuracy ≥ Keyword accuracy + 15pp | **FAIL** | Structural: 74.1%, Keyword: 100.0%, Δ = -25.9pp |
| **G3** (Min absolute accuracy) | Structural accuracy ≥ 80% | **FAIL** | 74.1% < 80% |
| **G4** (Info-sufficiency witness) | G4 pair distinguishable | **PASS** | Both G4 fixtures correctly classified |
| **G5** (Abstention honesty) | Abstention rate ≤ 20% | **FAIL** | 22.2% (6/27) abstained |

---

## Key Findings

### 1. Keyword baseline is perfect on synthetic fixtures

The keyword-only classifier achieves **100% accuracy** on all 27 synthetic fixtures. This is because the fixture categories have non-overlapping keyword signatures by construction:

- `fk_lock_contention`: Unique `ShareLock` keyword
- `index_lock_contention`: Unique `duplicate key` / `unique constraint` keywords  
- `tuple_lock_contention`: Unique `tuple` / `ctid` keywords
- `advisory_lock_contention`: Unique `advisory` / `pg_advisory` keywords
- `explicit_lock_contention`: Unique `LOCK TABLE` / `AccessExclusiveLock` keywords

The synthetic fixtures were too clean — each category's canonical signals are mutually exclusive in the fixture text.

### 2. Structural classifier underperforms due to parsing conservatism

The structural classifier achieves only 74.1% accuracy:
- `fk_lock_contention`: 16.7% (1/6) — parser fails to extract `wait_relation`/`hold_relation` for FK pattern
- `index_lock_contention`: 60.0% (3/5) — similar parsing issues
- `tuple_lock_contention`: 100% (6/6) — tuple location parsing works
- `advisory_lock_contention`: 100% (5/5) — advisory lock ID parsing works
- `explicit_lock_contention`: 100% (5/5) — LOCK TABLE parsing works

The classifier's structural patterns are too strict and fail to match valid variations in the synthetic fixtures.

### 3. Information-sufficiency pair (G4) passes but for the wrong reason

The G4 pair (fk_lock_contention vs tuple_lock_contention with overlapping keywords) is correctly distinguished — but only because they still have distinguishing keywords (`ShareLock` vs `tuple`), not because the structural classifier uses deeper reasoning.

### 4. Negative controls confirm the problem

| Classifier | Accuracy |
|------------|----------|
| Random | 14.8% |
| Majority (fk_lock_contention) | 22.2% |
| Keyword-only | **100.0%** |
| Structural | 74.1% |

The keyword-only baseline **beats** the structural classifier, violating the negative control requirement.

---

## Interpretation

**The claim is falsified.** The experiment correctly demonstrates that:

1. On clean synthetic fixtures with non-overlapping keyword signatures, keyword matching is sufficient and optimal.
2. The proposed structural classifier adds no value and actually performs worse due to over-engineering.
3. The kill gates correctly catch this: G2 fails (structural doesn't beat keyword), G3 fails (structural < 80%), G5 fails (abstention > 20%).

This is consistent with the mission's methodological principle: **runnable kill gates produce actionable results** (METHODOLOGY-SUMMARY.md). The experiment was run, gates evaluated, and the claim falsified.

---

## What this does not establish

- Whether structural classification would help on **real** (messy) deadlock reports where keywords overlap
- Whether a better structural classifier could beat keyword baseline on real data
- Whether deadlock classification is a viable product opportunity

The experiment only tests the claim on the declared synthetic fixtures. Real-world generalization is untested.

---

## Lessons for future fresh observation

1. **Synthetic fixture design matters critically.** If fixtures have non-overlapping keyword signatures, keyword baseline will win. Fixtures must be designed to force structural reasoning (e.g., overlapping keywords, ambiguous cases).

2. **Information-sufficiency pairs must truly share keyword sets.** My G4 pair shared some keywords but not all — the distinguishing keywords (`ShareLock` vs `tuple`) were still present.

3. **Parser robustness is the bottleneck.** The structural classifier's parsing logic failed on 5/6 FK fixtures and 2/5 index fixtures. A more robust parser (or a different structural approach) would be needed.

4. **The domain may not need structural classification.** If real deadlock reports also have clean keyword separation, a simple keyword classifier is the correct tool — not a complex structural one.

---

## Artifacts

- `PROTOCOL.md` — Predeclared protocol with all kill gates
- `fixtures.jsonl` — 27 synthetic fixtures (5 per category + 2 G4 pair)
- `classifier.py` — Structural and keyword-only classifiers
- `run.py` — Experiment runner with gate evaluation
- `results.json` — Raw gate results

---

## Compliance

- Protocol predeclared in `PROTOCOL.md` before any implementation
- Kill gates evaluated against committed fixtures
- stdlib-only Python 3.8
- No external dependencies
- Raw evidence preserved
- All gates declared before measurement