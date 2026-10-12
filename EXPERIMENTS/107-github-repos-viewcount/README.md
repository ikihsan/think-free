<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-12
-->

# E107 — View-count principle on GitHub code repositories

## Summary

**Result: ALL GATES PASS** — The view-count principle generalizes to GitHub code repositories.

## Experiment Details

- **Platform**: GitHub code repositories
- **Metric**: Star count (stargazers_count)
- **Activity definition**: Stars > 0 AND pushed within 365 days
- **Classification**: Topics + description keywords
- **Sample**: 160 repositories harvested (80 need-related search, 80 random search)
- **Classified**: 77 need-related, 73 random, 10 ambiguous

## Gate Results

| Gate | Criterion | Result |
|------|-----------|--------|
| G1 | Classified sample size ≥ 100 (50 per group) | **PASS** (150 total, 77 need-related, 73 random) |
| G2 | Mann-Whitney U test p<0.05, Cliff's δ>0.147 | **PASS** (p≈0.000, δ=0.826) |
| G3 | Wilson CI95 LB for proportion above random median > 0.60 | **PASS** (LB=0.952) |
| G4 | Both categories represented | **PASS** (77 need-related, 73 random) |

## Key Findings

- **Need-related median stars**: 2,796
- **Random median stars**: 325
- **Ratio**: 8.6× higher for need-related
- **Need-related active rate**: 84.4%
- **Random active rate**: 35.6%
- **All 77 need-related repos** exceed the random median (325 stars)

## Interpretation

The view-count principle strongly generalizes to GitHub code repositories. Repositories addressing common programming needs (web frameworks, databases, auth, caching, etc.) have dramatically higher star counts than repositories with generic utility topics.

This extends the principle's validated domains to include:
- Package registries: PyPI, NPM, NuGet, Hex.pm, CPAN
- Q&A forums: Stack Exchange (non-software), Discourse, Code Review
- **Code hosting: GitHub repositories** ← NEW

The principle fails on: Maven Central, crates.io, Hugging Face Hub, GitHub issues API, web search.

## Files

- `PROTOCOL.md` — Experiment design and gates
- `harvest.py` — Data collection (GitHub Search API only)
- `analyze.py` — Gate evaluation
- `raw_data.json` — Raw harvested repository data
- `results.json` — Gate evaluation results