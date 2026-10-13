# E120 — View-count principle on Mathematics Stack Exchange

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-12
-->

## Summary

Fresh observation per D083: tested the view-count principle on Mathematics Stack Exchange (math.stackexchange.com) using the E119 prototype with matched-harvest design, coverage-floor classifier (classifier_v3), and predeclared gates G1–G4.

**Result: ALL GATES PASS.** The view-count principle is supported on Mathematics Stack Exchange with a matched-harvest design and a classifier achieving ≥60% coverage floor.

## Experimental Setup

### Platform
- **Site:** Mathematics Stack Exchange (math.stackexchange.com)
- **API:** Stack Exchange API v2.3 (unauthenticated)
- **Tags sampled:** calculus, linear-algebra, probability, statistics, differential-equations, number-theory, combinatorics, topology
- **Items fetched:** 793 unique questions with view_count ≥ 1000
- **Items analyzed:** 500 (top by view_count)

### Methodology (E119 Prototype)
1. **Matched harvest:** Need and random arms drawn from same pool of 500 questions, sorted by view_count descending
2. **Classifier (classifier_v3):** Anchored word-boundary patterns, declared before measurement
3. **Coverage floor:** G2 requires ≥60% classifier coverage before measuring need fraction
4. **Gates evaluated in order:** G1 → G2 (coverage first) → G3 → G4

### Classifier Performance
- **Coverage:** 71.4% (357/500 classified)
- **Need-related:** 353 (70.6% of total)
- **Random:** 4 (0.8% of total)
- **Unclassified:** 143 (28.6% of total)
- **G0 discrimination:** PASS (10/10 need recovered, 9/10 random recovered)

## Gate Results

| Gate | Threshold | Result | Details |
|------|-----------|--------|---------|
| **G1** | ≥95% view_count > 0 | **PASS** | 500/500 = 100% |
| **G2** | coverage ≥ 60% AND need fraction ≥ 5% | **PASS** | coverage 71.4%, need fraction 70.6% |
| **G3** | Wilson CI95 upper bound < 60% unserved | **PASS** | unserved 1.96%, CI95 [0.95%, 3.99%] |
| **G4** | classified_total ≥ 30 | **PASS** | 357 classified |

## Interpretation

The view-count principle holds on Mathematics Stack Exchange:
- **Arrival instrument validated:** 100% of sampled questions have view_count > 0 (G1)
- **Classifier covers population:** 71.4% coverage exceeds 60% floor (G2)
- **Need-related questions are served:** Only 1.96% unserved fraction (CI95 upper bound 3.99% << 60% threshold) (G3)
- **Sufficient sample:** 357 classified items (G4)

The extremely low unserved fraction (1.96%) indicates that need-related mathematical questions on this platform are overwhelmingly served — they receive accepted answers or multiple high-scoring answers. This is consistent with the view-count principle: questions expressing genuine need attract views and answers.

## Comparison with Other Domains

| Domain | Coverage | Unserved Fraction | Gates |
|--------|----------|-------------------|-------|
| Physics SE (E119) | 81.5% | 4.27% (CI95 [2.1%, 8.5%]) | ALL PASS |
| **Mathematics SE (E120)** | **71.4%** | **1.96% (CI95 [1.0%, 4.0%])** | **ALL PASS** |
| Python Stack Overflow (E119) | 63% | — | PASS |
| Rust Stack Overflow (E119) | 72% | — | PASS |

## Files

| File | Purpose |
|------|---------|
| `PROTOCOL.md` | Gates and failure condition (inherited from E119) |
| `data_math.jsonl` | 500 questions from Mathematics SE (copied from E119 prototype) |
| `results.json` | Machine-readable gate outcomes |
| `README.md` | This report |

## Reproduction

```bash
cd EXPERIMENTS/120-mathematics-se-viewcount

# Run G0 discrimination check
python3 -c "
import sys
sys.path.insert(0, '../119-viewcount-prototype')
import importlib, classifier_v3
importlib.reload(classifier_v3)
from classifier_v3 import g0_discrimination_check
print(g0_discrimination_check())
"

# Run full gated measurement
python3 ../119-viewcount-prototype/measure_framework.py data_math.jsonl 0.60
```

## Conclusion

**The view-count principle is supported on Mathematics Stack Exchange under the E119 matched-harvest + coverage-floor protocol.** This is a fresh domain (per D083) not previously tested in the view-count sweep, and the experiment passes all predeclared gates with a classifier that covers 71.4% of the population.

This result, combined with E119's results on Physics SE (81.5% coverage, 4.27% unserved) and Stack Overflow tags (63-72% coverage), demonstrates that the E119 prototype's classifier and measurement framework generalize to multiple Stack Exchange Q&A domains.

**Next step per D083:** The view-count line can now be reopened for candidate generation on domains where the classifier achieves ≥60% coverage. The binding constraint from E113 (28% coverage with unanchored substring matching) is resolved.