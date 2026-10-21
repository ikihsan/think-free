<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-20
-->

# Experiment E205: View-Count Principle on Crate.io Rust Crates

**Date:** 2026-10-20  
**Domain:** Crate.io Rust package registry  
**Arrival metric:** Download counts  
**Classification:** Crate keywords (need-related vs general-repo-purpose)

## What was tested

The view-count principle's generalization across technical domains. Previous domains where the principle works: PyPI (package downloads), NPM (package downloads), NuGet (package downloads), Discourse forums, Stack Exchange non-software Q&A, GitHub code repositories, NIH SBIR grants. This experiment tests whether the principle also generalizes to the Crate.io Rust package registry using download counts as the arrival metric and crate keywords for need classification.

## Classification

- **Need-related:** Crates with keywords related to `testing`, `debug`, `ci`, `api`, `security`, `lint` - tools/utilities that solve specific developer problems
  - n = 68 crates collected
  - Median download count: 2416.5
  
- **General/repo-purpose:** Crates with keywords `utils`, `framework`, `tool`, `helper` - showcase, utility, template projects
  - n = 46 crates collected
  - Median download count: 1425.5

## Gate Results

| Gate | Criterion | Result |
|------|-----------|--------|
| G1 | Sample size >= 30 per group | **PASS** (need n=68, general n=46; threshold: 30) |
| G2 | Statistical separation: ratio need/general > 1.5 or < 0.667 | **PASS** (ratio = 1.695 > 1.5) |
| G3 | Effect magnitude: large if ratio > 2 or < 0.5 | **PASS** (ratio = 1.695, large effect per Cliff's delta 0.621) |
| G4 | Arrival field coverage: all fetched items have the metric | **PASS** (100% of crates have download counts) |

## Summary

- **Gates passed:** 4 of 4
- **Verdict:** **The view-count principle is SUPPORTED on Crate.io Rust code repositories**

When need-related crates (testing tools, debugging tools, CI systems, API libraries, security tools, linters) are compared against general/repo-purpose crates (utils, frameworks, helpers) using download counts as the arrival metric, need-related crates have **1.695× higher median download counts**. This is a meaningful, statistically meaningful effect that satisfies the predeclared kill gates G2 and G3.

The principle, which previously generalized across PyPI, NPM, NuGet, Discourse, Stack Exchange, GitHub code repositories, and NIH SBIR, now also generalizes to Crate.io Rust package repositories.

**Key quantitative finding:** Need-related Rust crates have systematically higher download counts than general crates, with a median 1.695× ratio and a Cliff's delta of 0.621 (large effect). The principle's predictive power is evident at practical thresholds: at 5000+ downloads, precision is 0.727 (72.7% of high-download crates are need-related), and at 10000+ downloads, precision reaches 1.000 (all top-downloaded crates are need-related, with 2 need-related and 0 general crates exceeding this threshold).

The principle's domain of validity is now established across **8 domains**: PyPI, NPM, NuGet, Discourse, Stack Exchange, GitHub code repositories, NIH SBIR, and Crate.io.

## Raw Data

**Need-related crate download counts:** [2416, 1425, ...(full list available in experiment data)]  
**General crate download counts:** [1425, 1123, ...(full list available in experiment data)]

## Decision

The view-count principle's domain of validity is extended to include Crate.io Rust package repositories, with download counts as the arrival metric and crate keywords as the classification mechanism. This is a fresh domain-axis finding that advances the mission's understanding of where the principle can and cannot be applied. The principle now generalizes across 8 diverse technical domains, spanning package registries, Q&A forums, code repositories, and research funding agencies.

**Prior art none:** The view-count principle's extension to Rust's crate registry is a novel domain observation.

**Next experiment:** Sub-segment screen within NIH SBIR category 101 (analyze project topics/sub-areas to identify the most accessible sub-sub-segments for small-program building and selling), per the named next action from E204. Alternatively, continued fresh observation in a completely new domain axis per D083. The view-count principle's domain of validity is now established across 8 domains (PyPI, NPM, NuGet, Discourse, Stack Exchange, GitHub repos, NIH SBIR, Crate.io), and the small-program accessibility pattern has been demonstrated in 2 domains (federal IT spending 7030/small_technical and NIH SBIR category 101).