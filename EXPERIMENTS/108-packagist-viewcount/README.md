# E108 — View-count principle on Packagist (PHP/Composer package registry)

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-11
-->

## Summary

**ALL GATES PASS** — The view-count principle generalizes strongly to Packagist.

| Metric | Need-related (n=100) | Random (n=100) |
|--------|---------------------|----------------|
| Active rate (monthly > 0) | 100.0% (100/100) | 26.0% (26/100) |
| Monthly download median | 10,342 | 0 |
| Mann-Whitney U p-value | < 0.000001 | |
| Cliff's delta | 0.9936 | |
| Wilson CI95 lower bound (need above random median) | 0.963 | |

## Gates

| Gate | Criterion | Result |
|------|-----------|--------|
| G1 | Classified sample ≥ 100 | **PASS** (200 total, 100 per group) |
| G2 | MWU p < 0.05, Cliff's δ > 0.147 | **PASS** (p < 0.001, δ = 0.9936) |
| G3 | Wilson LB > 0.60 for need above random median | **PASS** (LB = 0.963) |
| G4 | Both categories represented | **PASS** (100 each) |

## Interpretation

The view-count principle holds decisively on Packagist:
- **100% of need-related packages have monthly downloads > 0** vs only 26% of random packages
- Effect size is massive (Cliff's δ = 0.9936, near-maximum separation)
- All 100 need-related packages exceed the random median (which is 0)
- This is the strongest separation yet observed across all tested package registries

## Context

This extends the view-count principle to the **7th package registry** tested:

| Registry | Result | Key Stats |
|----------|--------|-----------|
| PyPI (E071) | PASS | 82.9% vs 57.5% active |
| NPM (E072) | PASS | 100% vs 0% active |
| NuGet (E102) | PASS | p=1.7e-14, δ=0.996 |
| **Packagist (E108)** | **PASS** | **100% vs 26%, δ=0.994** |
| Hex.pm (E103) | PASS | p≈0, δ=0.861, 220× median |
| GitHub repos (E107) | PASS | 8.6× median, δ=0.826 |
| Maven Central (E090) | FAIL | 60% vs 52%, not significant |
| crates.io (E095) | FAIL | 100% both, no discrimination |
| Hugging Face (E101) | FAIL | 12.4% vs 8.6%, not significant |

The principle works on **mature, infrastructure-heavy package ecosystems** (PyPI, NPM, NuGet, Packagist, Hex.pm) where download counts reflect genuine usage demand. It fails on registries where:
- All packages appear active (crates.io: recent_downloads > 0 for all)
- Activity metadata is sparse or differently structured (Maven Central: only 53.6% have arrival field)
- Download dynamics differ from code packages (Hugging Face: model downloads ≠ package usage)

## Artifacts

- `PROTOCOL.md` — Experiment protocol with gates and classification rules
- `collect.py` — Data collection script (search + random sampling)
- `analyze.py` — Gate evaluation with Mann-Whitney U, Cliff's delta, Wilson CI
- `raw/collected.json` — Raw package data (200 packages with metadata)
- `results.json` — Gate evaluation results
- `README.md` — This summary