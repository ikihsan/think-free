<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-14
-->

# E150 RESULT — SQL injection technique root cause classification

**Date:** 2026-10-14 · **Status:** Claim falsified

---

## Summary

The claim that a structural classifier beats a keyword baseline by ≥15pp on SQL injection technique classification is **falsified**. The keyword-only baseline achieves 81.2% accuracy, the structural classifier achieves 93.8% (Δ=12.5pp, short of the 15pp threshold). G1 also fails as the structural classifier misses 1 of 16 fixtures.

---

## Gate Results

| Gate | Criterion | Result | Evidence |
|------|-----------|--------|----------|
| **G1** (Fixture validity) | Structural classifier 100% on synthetic fixtures | **FAIL** | 93.8% (15/16) |
| **G2** (Beats keyword baseline) | Structural accuracy ≥ Keyword accuracy + 15pp | **FAIL** | Δ = 12.5pp (93.8% - 81.2%) |
| **G3** (Min absolute accuracy) | Structural accuracy ≥ 80% | **PASS** | 93.8% |
| **G4** (Info-sufficiency witness) | G4 pair distinguishable | **PASS** | Structural distinguishes overlapping cases |
| **G5** (Abstention honesty) | Abstention rate ≤ 20% | **PASS** | 0% abstention |

---

## Key Findings

### 1. Structural classifier outperforms keyword baseline but not by enough

| Classifier | Accuracy |
|------------|----------|
| Random | ~25% |
| Majority | 25% |
| Keyword-only | 81.2% |
| Structural | 93.8% |

The structural classifier **does** add value (12.5pp improvement) by correctly handling fixtures where keywords overlap across categories (e.g., `FROM` appears in both union_based and other queries). However, the 15pp kill gate threshold is not met.

### 2. Keyword baseline is strong due to fixture design

The keyword signals per category have significant overlap:
- `error_based`: `extractvalue`, `updatexml` (unique)
- `blind_time_based`: `sleep`, `benchmark`, `waitfor`, `delay`, `pg_sleep` (unique)
- `boolean_blind`: `and 1=1`, `or 1=1`, `if`, `case when` (unique)
- `union_based`: `union select`, `union all`, `from`, `table`, `password` — **`from` and `table` appear in other queries too**

The keyword baseline fails on 3 fixtures where `FROM`/`table` keywords mislead it toward `union_based`.

### 3. Structural classifier has one clear miss (G1 failure)

Fixture 11: `IF(1=1, 1, 0) FROM dual` — categorized as `boolean_blind` but structural classifier returns `union_based` because it checks `has_union` first (finds no UNION), then `has_delay` (no), then `has_and_1`/`has_or_1` (no — it has `IF` not `AND 1=1`), then `has_extract` (no), then falls back to keyword-only which sees `FROM` and picks `union_based`.

The structural decision logic order doesn't handle `IF(condition, true, false)` pattern.

### 4. Information-sufficiency pair analysis

The protocol declared Fixture A (`extractvalue`) and Fixture B (`SLEEP`) as sharing keywords `SELECT`, `FROM`, function call. They are correctly distinguished by both classifiers — but primarily by the unique function names (`extractvalue` vs `SLEEP`), not deeper structural reasoning.

---

## Interpretation

**The claim is falsified.** While the structural classifier outperforms keyword-only (93.8% vs 81.2%), the 12.5pp gap falls short of the predeclared 15pp threshold. G1 also fails due to one misclassification.

This reinforces the E147 lesson: **synthetic fixture design critically determines whether structural classification can demonstrate advantage**. Here, the keyword overlap was partial (mainly `FROM`/`table`), giving the structural classifier a modest edge but not a decisive one.

---

## What this does not establish

- Whether structural classification would help on **real** SQL injection queries with more variation
- Whether a better structural classifier (with improved decision logic) could beat keyword baseline by ≥15pp
- Whether SQL injection classification is a viable product opportunity

The experiment only tests the claim on the declared synthetic fixtures.

---

## Lessons for future fresh observation

1. **Fixture keyword overlap must be substantial and systematic.** The 12.5pp gap here came from only 3 fixtures where `FROM`/`table` caused keyword confusion. To get ≥15pp, fixtures need more pervasive ambiguity.

2. **Structural decision logic must be robust.** The `IF()` pattern miss shows the structural classifier's logic order matters. A more complete structural parser (e.g., actual SQL parsing) would be needed for real advantage.

3. **The 15pp threshold is demanding.** With 16 fixtures, 15pp = 2.4 fixtures. The structural classifier would need to correct at least 3 more keyword errors than it introduces.

4. **Domain may not need structural classification.** If real SQL injection queries also have mostly clean keyword separation, keyword matching may be sufficient.

---

## Artifacts

- `PROTOCOL.md` — Predeclared protocol with all kill gates
- `fixtures.jsonl` — 16 synthetic fixtures (4 per category)
- `classifier.py` — Structural and keyword-only classifiers
- `results.json` — Raw gate results
- `RESULT.md` — This file

---

## Compliance

- Protocol predeclared in `PROTOCOL.md` before any implementation
- Kill gates evaluated against committed fixtures
- stdlib-only Python 3.8
- No external dependencies
- Raw evidence preserved
- All gates declared before measurement