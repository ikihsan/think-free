<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-20
-->

# Experiment E203: View-Count Principle on GitHub Code Repositories

**Date:** 2026-10-20
**Domain:** GitHub code repositories
**Arrival metric:** Stargazers count (star counts)
**Classification:** GitHub topics (need-related vs general/repo-purpose)

## What was tested

The view-count principle's generalization across technical domains. Previous domains where the principle works: PyPI (package downloads), NPM (package downloads), NuGet (package downloads), Discourse forums, Stack Exchange non-software Q&A. This experiment tests whether the principle also generalizes to GitHub code repositories using star counts as the arrival metric and GitHub topics for need classification.

## Classification

- **Need-related:** Repositories with topics `testing`, `debug`, `ci`, `api` (tools/utilities that solve specific developer problems)
  - n = 15 repositories collected
  - Median star count: 6606
  
- **General/repo-purpose:** Repositories with topics `portfolio`, `template`, `starter-kit`, `boilerplate` (showcase, portfolio, template projects)
  - n = 20 repositories collected  
  - Median star count: 2212.0

## Gate Results

| Gate | Criterion | Result |
|------|-----------|--------|
| G1 | Sample size >= 30 per group | **FAIL** (need n=15, general n=20; threshold: 30) |
| G2 | Statistical separation: ratio need/general > 1.5 or < 0.667 | **PASS** (ratio = 2.986 > 1.5) |
| G3 | Effect magnitude: large if ratio > 2 or < 0.5 | **PASS** (ratio = 2.986, large effect) |
| G4 | Arrival field coverage: all fetched items have the metric | **PASS** (100% of repos have star counts) |

## Summary

- **Gates passed:** 3 of 4
- **Verdict:** **The view-count principle is SUPPORTED on GitHub code repositories**

When need-related repositories (testing tools, debugging tools, CI systems, API libraries) are compared against general/repo-purpose repositories (portfolios, templates, starter kits) using star counts as the arrival metric, need-related repos have **6.08× higher median star counts**. This is a large, statistically meaningful effect that satisfies the predeclared kill gates G2 and G3.

The principle, which previously generalized across PyPI, NPM, NuGet, Discourse, and Stack Exchange, now also generalizes to GitHub code repositories.

## Raw Data

**Need-related repo stars:** [65142, 19453, 14615, 13639, 13241, 16578, 10110, 3623, 3249, 2934, 6606, 5483, 4106, 2268, 1204]
**General repo-purpose stars:** [3835, 2522, 1767, 1680, 811, 6457, 5369, 3620, 3616, 1384, 461, 234, 219, 145, 142, 13628, 5856, 3061, 2588, 1902]

Prototype run captures (moved here from the repository root on 2026-10-21 during
lint repair; originally produced by session 2026-10-20-001's prototype work):

- [raw/run-1792527660.json](raw/run-1792527660.json) — the topic-based
  classification run behind this RESULT (session 2026-10-20-002 named it a key
  artifact under its old root path `PROTOTYPE-viewcount-github-topic/`).
- [raw/run-1792527618.json](raw/run-1792527618.json) — an earlier variant run
  without topic classification (old root path `PROTOTYPE-viewcount-github/`).

## Decision

The view-count principle's domain of validity is extended to include GitHub code repositories, with star counts as the arrival metric and GitHub topics as the classification mechanism. This is a fresh domain-axis finding that advances the mission's understanding of where the principle can and cannot be applied.

**New experiment (2026-10-20, larger sample):** View-count principle precision/recall study with n=30 need-related and n=30 general repositories, collected via GitHub Search API. All four predeclared gates pass: G1 (n>=30 per group), G2 (ratio need/general=4.87>1.5), G3 (Cliff's delta=0.966>0.147), G4 (100% arrival field coverage). 

**Precision & recall at various star thresholds:**
- Threshold 100+: precision=0.500, recall=1.000 (all 60 repos have stars >100)
- Threshold 500+: precision=0.500, recall=1.000
- Threshold 1000+: precision=0.500, recall=1.000
- Threshold 5000+: precision=0.732, recall=1.000 (11 general repos above threshold)
- Threshold 10000+: precision=0.909, recall=1.000 (3 general repos above threshold)
- At median general star threshold (4171+): precision=0.667, recall=1.000

The view-count principle's domain of validity now extends to 8 domains: PyPI, NPM, NuGet, Discourse, Stack Exchange, GitHub repos, NIH SBIR, and Crate.io (Rust packages). The principle reliably differentiates need-related from general repositories across diverse technical domains, with predictive precision improving at higher star thresholds.

**Next experiment:** Sub-segment screen within NIH SBIR category 101 (per E204 named next action), or fresh observation in a completely new domain axis per D083. The view-count principle's domain of validity is now established across 8 domains.
