<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-10
-->

# E092 — Results: Module-provider demand measurement

**Date:** 2026-10-10  
**Session:** `2026-10-10-008-measure-the-rate-of-real-importerror-mod`  
**VM:** `instance-20260717-0947`

## Summary

**G1 FAILS:** Harvest yielded only 40 Stack Overflow questions (target ≥200 classifiable). GitHub issues search returned PRs mentioning ImportError, not practitioner error reports — not a valid population for this question.

**G2 PASSES:** Discrimination test on 40 construction-labelled controls achieved 95% accuracy (20/20 positive, 18/20 negative).

**G3 RATE:** On 40 Stack Overflow questions with "No module named" in body:
- 25 excluded as environment issues (virtualenv, DLL load, conda, path, version conflicts)
- 2 excluded as stdlib
- 2 excluded as unclear
- 2 distribution-only (asker names distribution)
- 3 module-and-dist (asker names both module and distribution)
- **2 module-only** (5% of raw harvest, ~28% of classifiable missing-module reports)
- Wilson CI95 on module-only rate: [0.01, 0.18] — spans kill threshold

**G4 FAILS:** Only 1 of 2 module-only reports has view_count > 0.

## Detailed Classification

| Category | Count | Notes |
|---|---|---|
| environment | 25 | Virtualenv, DLL load failed, conda, pip install but fails, path issues, relative imports, version conflicts |
| stdlib | 2 | configparser, dataclasses |
| unclear | 2 | No clear error pattern |
| distribution-only | 2 | Asker names distribution in question |
| module-and-dist | 3 | Asker names both module and distribution |
| module-only | 2 | `java` (invalid), `Adafruit_GPIO` (genuine) |

## Key Findings

1. **The "what package provides X?" question is rare on Stack Overflow.** Most `ImportError`/`ModuleNotFoundError` questions are about:
   - Environment mismatches (venv, conda, Docker, CI)
   - Binary compatibility (DLL load failed, wrong architecture)
   - Installation process failures (pip/conda/network)
   - Path/import structure issues (relative imports, sibling folders)
   - Version conflicts (numpy, torch, etc.)

2. **GitHub Issues are not the right venue.** Practitioners don't ask "what package?" on GitHub issues — they ask on Stack Overflow. GitHub issues mentioning ImportError are almost exclusively PR titles about fixing imports in the project's own code.

3. **The population is smaller than expected.** The Stack Exchange API (unauthenticated) returns only ~40 questions matching "No module named" in body for Python tag. This is far below the 200 threshold for G1.

4. **The two module-only cases:**
   - `import java` — invalid (Java module, not Python)
   - `No module named 'Adafruit_GPIO'` — genuine, but Adafruit-GPIO is the package name (near-miss)

## Gate Results

| Gate | Threshold | Result | Status |
|---|---|---|---|
| G1 Harvest viability | ≥200 classifiable/arm | 40 SO, 0 GH valid | **FAIL** |
| G2 Control validity | ≥80% accuracy | 95% (38/40) | **PASS** |
| G3 Rate (R ≥ 1%) | R < 0.01 = KILL | R ≈ 0.05 raw, ~0.28 classifiable | **INCONCLUSIVE** (sample too small) |
| G4 View_count | ≥50% have views > 0 | 1/2 = 50% (barely) | **MARGINAL PASS** |

## Decision

**The line closes on measured grounds (G1 failure).** The population of practitioners asking "which distribution provides this module?" on observable venues is too small to measure reliably with current API access. The Stack Exchange API limit (300 req/day unauthenticated) and the low incidence of this specific question type make a statistically sound measurement infeasible.

This does not mean the need doesn't exist — it means the *observable demand signal* for this specific question is below detection threshold on the venues we can access. The resolver mechanism (pyprovides) works technically (E085, E090) but lacks a measurable practitioner population asking the question in accessible venues.

**Reopening condition:** A Stack Exchange API key (10k req/day) or data dump access enabling harvest of 500+ questions, OR a different venue where this question is asked at measurable volume.

## Artifacts

- `harvest_so.json` — 40 Stack Overflow questions
- `DISCRIMINATION_TEST_RESULTS.json` — G2 results (95% accuracy)
- `controls.json` — 40 construction-labelled controls
- `classifier.py` — Classification logic
- `test_classify.py` — Test script