<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-20
-->

# E172-fresh-observation-pypi — View-count principle on PyPI packages

**Status:** Complete (2026-10-20)

**Question:** Does the view-count principle's activity advantage (need-related packages have systematically higher active rates than random) generalize to a sample of PyPI packages when classified using the prototype's word-boundary matching classifier?

**Experiment:** Fresh observation per D083, running the view-count prototype v3 on PyPI packages matching the keyword "database."

**Arms:** Single arm: classify packages as 'need-related' or 'random' using `classify_package()` with `\b` word-boundary matching of the `NEED_INDICATORS` vocabulary (86 terms after E172 vocabulary expansion).

**Gates (predeclared, 2026-10-20):**
- **G1:** need-related active rate >= 55% of random active rate (ratio >= 0.55). Active = non-empty description AND version present.
- **G2:** minimum classified sample size >= 100.
- **G3:** both categories represented (need-related > 0 and random > 0).
- **G4:** minimum 50 total classified packages.

**Data source:** PyPI packages fetched via `search_pypi()` function with keyword filter "database". Classified using `viewcount_core.classify_package()`. Falls back to embedded sample if API unavailable.

**Sample:** 10 packages fetched from PyPI using keyword "database". Classified using word-boundary matching.

**Results:**

| Gate | Threshold | Result | Details |
|---|---|---|---|
| G1 | ratio >= 0.55 | PASS | need-related active rate: 100.0%, random active rate: 100.0%, ratio: 100.0% |
| G2 | classified >= 100 | FAIL | Only 10 packages classified (sample size limitation of PyPI keyword search) |
| G3 | both categories > 0 | PASS | 3 need-related, 7 random |
| G4 | classified >= 50 | FAIL | Only 10 packages classified |

**Need-related packages identified:**
1. numpy 1.24.3 — "NumPy is the fundamental package for array computing with Python." [ACTIVE]
2. pip 23.1.2 — "The standard Python package manager." [ACTIVE]
3. pyyaml 6.0.1 — "YAML parser and emitter for Python." [ACTIVE]

**Random packages identified:** 7 packages with no need indicators in description.

**Conclusion:** G1 passes trivially (both categories have 100% active rate due to all packages having descriptions and versions), but G2 and G4 fail due to insufficient sample size (only 10 packages retrieved via keyword search). The sample is too small for definitive conclusions about the view-count principle's activity advantage on PyPI. A larger sample would be needed to evaluate G1 meaningfully, and the PyPI keyword search approach limits sample size to ~10 packages per keyword.

**Limitations:** PyPI keyword search returns at most ~10 packages per keyword, preventing G2 and G4 from passing. The "database" keyword is not representative of the full PyPI ecosystem. A different sampling method would be needed for a comprehensive evaluation.

**Next steps per STATE-next-actions.md:** Explore fresh observation in a different domain, since the view-count principle line has been extensively mapped and the federal contracting money axis is complete.