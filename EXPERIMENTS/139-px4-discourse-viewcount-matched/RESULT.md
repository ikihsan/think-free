# E139 — PX4 Discourse View-Count Experiment Results

<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-14
-->

## Summary

Experiment on the PX4 drone autopilot fault codes domain (discuss.px4.io) using a **developer-forum-specific classifier** and **matched harvest design** (per E113/F116). This was the first view-count experiment on PX4 Discourse with the corrected harvest design.

**Key finding: The view-count principle's arrival metric (G1) generalizes to PX4 Discourse (100% have view_count > 0), but the classifier coverage boundary (G2) and zero-reply metric (G3) both fail, and the effect size is negligible.**

This result contributes to the growing evidence that the view-count principle is highly domain-dependent and that methodology corrections (matched harvest, domain-specific classifier) significantly change outcomes.

## Gates

| Gate | Threshold | Result | Details |
|------|-----------|--------|---------|
| **G1** | ≥95% of topics have `view_count > 0` | **PASS** (100%) | 150 of 150 topics have view_count > 0 |
| **G2** | Classifier coverage ≥60% AND need fraction ≥5% | **FAIL** (58.7% coverage, 58.7% need fraction) | Coverage 58.7% < 60% threshold; need fraction 58.7% > 5% minimum |
| **G3** | Unserved fraction (zero replies) Wilson CI95 upper bound < 60% | **FAIL** (70.86%) | 54 of 88 need-related topics have zero replies; Wilson upper bound 70.86% |
| **G4** | ≥30 topics classified total | **PASS** (150) | 150 topics classified |

## Classifier Coverage

- **Need-related**: 88 topics (58.7% of 150)
- **Random**: 62 topics (41.3% of 150)
- **Coverage**: 58.7% (just below the 60% G2 threshold)
- The classifier reliably identifies need-related topics in the PX4 domain but falls 1.3 percentage points short of the 60% coverage floor

## Need-Related Topic Analysis

- **Total need-related topics**: 88
- **Topics with ≥1 reply (served)**: 34 of 88 (38.6%)
- **Topics with zero replies (unserved)**: 54 of 88 (61.4%)
- **Wilson 95% upper bound on unserved fraction**: 70.86%
- The zero-reply rate substantially exceeds the 60% dysfunctional threshold

## Matched Harvest Analysis

The matched harvest design explicitly avoids the harvest artifact by:

1. Pooling all classified topics (need + random)
2. Sorting by `view_count` descending
3. Splitting at median view_count into high/low engagement halves
4. Comparing need fractions and computing effect sizes

| Metric | High Engagement (78 topics) | Low Engagement (72 topics) |
|---|---|---|
| Need fraction | 60.26% (47/78) | 56.94% (41/72) |
| View count median | 76 | — |

- **Cliff's δ (need vs random view_count)**: **0.0411** — very small effect size
- **Mann-Whitney U p-value**: **0.6704** — not statistically significant
- **Effect present (|δ| > 0.1)**: **FAIL** — no detectable difference in view_count distributions
- High-engagement need fraction (60.26%) barely exceeds low-engagement (56.94%)

The matched harvest shows essentially no detectable difference between need-related and random topics in view_count distributions. The need fraction difference (60.26% vs 56.94%) is 3.3 percentage points, well within noise.

## Comparison with Prior Experiments

| Experiment | Coverage | Unserved (zero-reply) | δ (need vs random) | G2 | G3 |
|---|---|---|---|---|---|
| **E139 (PX4 Discourse)** | 58.7% | 70.86% (upper bound) | 0.0411 | FAIL | FAIL |
| **E138 (Prometheus Discourse)** | 96.7% | 89.1% | +0.144 | PASS | FAIL |
| **E082 (3 Discourse forums)** | ~80% | 15.3% (CI95 upper 21.3%) | N/A | PASS | PASS |
| **E124 (GNOME)** | 37.2% | — | — | FAIL | — |
| **E125 (Jupyter)** | 50.4% | 43.1% | — | FAIL | — |

**Key observations:**
- PX4 Discourse (E139) has coverage between E124/E125 (too low) and Prometheus/E077/E082 (adequate)
- PX4 unserved rate (70.86% upper bound) is between E138 (89.1%) and E082 (15.3%)
- The view-count effect size (δ=0.0411) is much smaller than Prometheus (δ=0.144) and essentially zero compared to the thresholds that matter for candidate generation

## What This Experiment Demonstrates

1. **G1 (arrival metric) generalizes**: The view_count field reliably indicates topic arrival across diverse Discourse forums, including PX4.

2. **G2 (coverage boundary) is near but not crossed**: At 58.7% classifier coverage, PX4 Discourse falls 1.3 percentage points short of the 60% floor. A slightly improved classifier (adding ~2 more need-related topics classified out of 150) would pass G2. This confirms the coverage boundary is real but penetrable — it was also observed in E124 (37.2%), E125 (50.4%), and E138 (96.7%).

3. **G3 (zero-reply metric) fails**: The 70.86% unserved fraction (upper bound) substantially exceeds the 60% threshold, consistent with E138 (89.1%) and unlike E082 (15.3%). This suggests the zero-reply metric is domain-dependent: it works for some technical forums (E082's embedded microcontroller fault codes) but not others (PX4, Prometheus).

4. **Effect size is negligible**: The matched harvest Cliff's δ of 0.0411 and Mann-Whitney p=0.6704 indicate no detectable difference in view_count between need-related and random topics. This contrasts with E138 (δ=+0.144, p=0.039, significant) and shows the view-count separation effect is not generalizable to PX4 Discourse.

5. **No candidate population**: With G2 and G3 both failing, no candidate population is generated from this experiment. The view-count signal is too weak (δ≈0) and the forum's zero-reply rate is too high.

## Artifacts

- `results_raw.json` — 150 harvested topics with view_count and reply_count
- `classified.json` — 150 topics classified as need-related (88) or random (62)
- `results.json` — Full gate results with matched harvest analysis
- `fetch_px4.py` — Harvest script for PX4 Discourse category
- `classify_px4.py` — Developer-forum-specific classifier
- `measure_px4.py` — Gate measurement with matched harvest design

## Evidence Labels

All metrics: **observed** (directly measured from harvested data)
Classifier coverage: **observed** (58.7% on PX4 Discourse topics)
View-count principle generalization: **falsified** for candidate generation on PX4 Discourse (G2 and G3 both fail, δ≈0)
Zero-reply metric validity: **inferred** (domain-dependent; works for E082's embedded forums, fails for E138/PX4)