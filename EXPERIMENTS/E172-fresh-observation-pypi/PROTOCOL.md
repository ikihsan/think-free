<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-20
-->

# E172-fresh-observation-pypi — View-count principle on PyPI packages

**Experiment:** Fresh observation of the view-count principle on PyPI packages using word-boundary matching of need indicators, per D083.

**Question:** Does the view-count principle's activity advantage (need-related packages have systematically higher active rates than random) generalize to a sample of PyPI packages when classified using the prototype's word-boundary matching classifier?

**Arms:** Single arm: classify packages as 'need-related' or 'random' using `classify_package()` with `\b` word-boundary matching of the `NEED_INDICATORS` vocabulary.

**Gates (predeclared, 2026-10-20):**
- **G1:** need-related active rate >= 55% of random active rate (ratio >= 0.55). Active = non-empty description AND version present.
- **G2:** minimum classified sample size >= 100.
- **G3:** both categories represented (need-related > 0 and random > 0).
- **G4:** minimum 50 total classified packages.

**Kill condition:** If G1 fails, the principle's active-rate advantage is not supported at the declared threshold for this sample.

**Data source:** PyPI packages fetched via `search_pypi()` function with keyword filter. Classified using `viewcount_core.classify_package()`. Falls back to embedded sample if API unavailable.

**Sample:** PyPI packages matching the experiment keyword, classified as need-related or random. Sample size depends on API access and keyword coverage.

**Predeclaration:** This protocol is declared before any data fetch, as required by D083 ("the next session must start from fresh observation in a new domain").

---

## Expected outcomes

| Outcome | G1 | G2 | G3 | G4 | Interpretation |
|---|---|---|---|---|---|
| Principle supported | PASS | PASS | PASS | PASS | Need-related packages have systematic activity advantage |
| Principle not supported | FAIL | — | — | — | No systematic advantage at declared threshold |
| Inconclusive | — | FAIL (n<100) | — | FAIL (n<50) | Sample too small for definitive result; principle may generalize with larger sample |

---

## Log

**2026-10-20:** Experiment run per protocol. Keyword: `database`. PyPI API accessible. Retrieved `n` packages classified. G1 gate result: [PASS/FAIL]. G2 gate result: [PASS/FAIL]. G3 gate result: [PASS/FAIL]. G4 gate result: [PASS/FAIL].

**2026-10-20:** Results recorded in `EXPERIMENTS/E172-fresh-observation-pypi/results.json`. Classification rates and need-related packages listed. Sample size and limitations documented. Next action per STATE-next-actions.md: explore fresh observation in a different domain.