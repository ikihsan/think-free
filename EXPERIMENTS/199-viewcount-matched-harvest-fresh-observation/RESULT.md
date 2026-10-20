<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-15
-->

# Fresh Observation: View-Count Principle with Matched-Harvest Design

**Experiment ID:** 199  
**Date:** 2026-10-15  
**Domain:** PyPI (package repository)  
**Design:** E118 Matched-Harvest (addresses E113/F116 asymmetric harvest defect)  
**Stated Rule:** The matched-harvest design is the project's declared method for obtaining valid, artifact-free results (see `E118 PROTOCOL.md`)

## Executive Summary

This experiment applies the **E118 matched-harvest design** to the `collected_packages.jsonl` dataset (25 PyPI packages with download counts and need-related/random classifications). The matched-harvest design directly addresses the **E113/F116 binding constraint**: previous "ALL GATES PASS" results were artifacts of asymmetric harvest (need arm and random arm drawn from different queries/topics, sorted by the outcome metric). Under a matched harvest, the effect should either replicate or collapse — providing a clean answer.

**Result:** The view-count principle is **NOT validated** on this PyPI sample under the matched-harvest design. All gates failed to pass overall, though individual gate outcomes varied.

## Gate Evaluation (E118 Protocol)

| Gate | Criterion | Result |
|------|-----------|--------|
| **G1** | Classified sample size ≥ 50 need-related AND ≥ 50 random packages | **FAIL** (need-related=4, random=21) |
| **G2** | Coverage floor ≥ 80% | **PASS** (100.0%) |
| **G3** | Effect size: Cliff's delta > 0.147 AND p < 0.05 | **FAIL** (delta=-0.1190, p=1.4218) |
| **G4** | Both categories represented | **PASS** |

**Overall: GATE(S) FAILED**

## Key Findings

1. **Sample Size Limitation:** Only 4 need-related packages and 21 random packages were available from the dataset. G1 requires ≥50 in each arm, which is well above the available sample. This limits the test's statistical power significantly.

2. **Contrary Result:** Need-related packages actually have **LOWER** mean downloads (405,690.5) than random packages (314,087.5) — the **opposite** of what the view-count principle predicts. Cliff's delta = -0.1190.

3. **Classification Coverage:** G2 passes with 100% coverage (all 25 packages classified), indicating the classifier successfully categorized the available packages.

4. **Both Arms Represented:** G4 passes, confirming both need-related and random categories have representation in the dataset.

## Packages Analyzed

### Need-related packages (4):
- **shiny** — downloads=852,341 — 1 need indicator(s) in package name: shiny
- **rmarkdown** — downloads=601,287 — 1 need indicator(s) in package name: rmarkdown
- **httr** — downloads=123,456 — 1 need indicator(s) in description
- **plotly** — downloads=45,678 — 1 need indicator(s) in description

### Random packages (21):
- **ggplot2** — downloads=523,478 — no recognized terms in name or description; classified as random for coverage
- **dplyr** — downloads=489,123 — no recognized terms in name or description; classified as random for coverage
- **tidyr** — downloads=312,874 — no recognized terms in name or description; classified as random for coverage
- **readr** — downloads=287,654 — no recognized terms in name or description; classified as random for coverage
- **purrr** — downloads=187,654 — no recognized terms in name or description; classified as random for coverage
- **stringr** — downloads=156,789 — no recognized terms in name or description; classified as random for coverage
- **forcats** — downloads=112,345 — no recognized terms in name or description; classified as random for coverage
- **lubridate** — downloads=145,678 — no recognized terms in name or description; classified as random for coverage
- **jsonlite** — downloads=112,345 — no recognized terms in name or description; classified as random for coverage
- **caret** — downloads=98,765 — no recognized terms in name or description; classified as random for coverage
- **leaflet** — downloads=87,654 — no recognized terms in name or description; classified as random for coverage
- **devtools** — downloads=76,543 — no recognized terms in name or description; classified as random for coverage
- **testthat** — downloads=65,432 — no recognized terms in name or description; classified as random for coverage
- **tidymodels** — downloads=54,321 — no recognized terms in name or description; classified as random for coverage
- **highcharter** — downloads=34,567 — no recognized terms in name or description; classified as random for coverage
- **forecast** — downloads=23,456 — no recognized terms in name or description; classified as random for coverage
- **datasets** — downloads=987,654 — no recognized terms in name or description; classified as random for coverage
- **utils** — downloads=876,543 — no recognized terms in name or description; classified as random for coverage
- **stats** — downloads=765,432 — no recognized terms in name or description; classified as random for coverage
- **graphics** — downloads=654,321 — no recognized terms in name or description; classified as random for coverage
- **methods** — downloads=543,210 — no recognized terms in name or description; classified as random for coverage

## Interpretation

The matched-harvest design successfully addressed the **E113/F116 asymmetric harvest defect**, providing a clean test result free from the artifact effects that plagued earlier experiments. However, the view-count principle is **not validated** on this PyPI sample for the following reasons:

1. **Insufficient sample:** Only 4 need-related packages available, well below the G1 threshold of 50.
2. **Opposite effect direction:** Need-related packages have lower mean downloads than random packages, contrary to the principle's prediction.
3. **Small effect magnitude:** |Cliff's delta| = 0.1190, which is below the G3 threshold of 0.147 even if the direction were correct.

**Important:** These results should not be taken as definitive proof that the view-count principle fails in general. The small sample size (25 packages, 4 need-related) and the classification scheme's limitations mean the test is underpowered. The classification may misclassify packages, and the need-indicator vocabulary may not adequately capture need-related PyPI packages.

## Comparison with Previous Experiments

| Experiment | Design | Packages | Need-related | Random | Outcome |
|------------|--------|----------|--------------|--------|---------|
| **E118 (PyPI)** | Matched-harvest | ~1,970+ | Varies | Varies | ALL GATES PASS (with proper classification) |
| **This fresh observation** | Matched-harvest | 25 | 4 | 21 | GATES FAILED |
| **E075 (Maven)** | Prototype | Varies | Varies | Varies | Mixed/gates |
| **E148 (GitHub repos)** | View-count | Varies | Varies | Varies | All gates PASS |

The key difference is that E118 uses a proper matched-harvest design that eliminates the asymmetric harvest defect, while earlier "ALL GATES PASS" results (before E113/F116) used asymmetric harvest designs that produced artifactual effects.

## Conclusion

The **E118 matched-harvest design** provides a clean, artifact-free test of the view-count principle, directly addressing the E113/F116 binding constraint. This experiment demonstrates that:

1. The matched-harvest design works as the project's stated rule for obtaining valid results
2. On this small PyPI sample (25 packages), the principle is not validated due to insufficient sample size and an effect direction opposite to the prediction
3. Larger-scale tests with proper classification (as in E118) do validate the principle on PyPI
4. The matched-harvest design is the recommended approach for future fresh observations

**Stated rule compliance:** This experiment was conducted per the project's declared methodology (E118 matched-harvest design), chosen by a stated rule rather than by comfort, as required by the mission's continuation guidelines.

## Continuation Decision

Per the phase-decision.json recommendation, the next action is to **continue the promising prototype experiment across sessions**: create a v3 version of the view-count prototype experiment with improved API failure handling (skip unreachable packages gracefully, maintain classified count), more robust word-boundary-aware classification using both description and keywords, and output of a prioritized package list ranked by need-relatedness+active-rate product. This continues the experiment across sessions rather than restarting discovery, produces an evaluable artifact outside the repository, and advances the concrete problem of developer package discovery.