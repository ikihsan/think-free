<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-14
-->
# E146 — View-count principle on GitHub repositories (cross-platform classifier test)

## Question

Does the E116 view-count classifier (developed for Reddit technical communities) generalize to GitHub repository descriptions? This tests the cross-platform validity of the classifier vocabulary and disambiguation framework, a "fresh observation in a new domain axis" per D083.

## Background

The view-count classifier (E116) was validated on Hex.pm package names/descriptions with an 80%+ coverage floor. GitHub repositories (E107) already demonstrated the view-count principle with star counts (all gates pass, δ = 0.826). However, the E116 classifier has not been tested on GitHub repo data.

This experiment addresses two questions:
1. Can the E116 classifier (whole-word matching + contextual disambiguation) classify GitHub repo descriptions effectively?
2. If so, does the view-count separation effect (need-related vs. random repos by star count) persist under the new classification?

## Platform

GitHub code repositories, using the E107 already-harvested dataset (160 repos, previously tested with original classification, all gates passed).

## Classification

The E116 classifier uses:
- **NEED_INDICATORS**: 60+ terms suggesting a programming need (web, api, database, auth, etc.)
- **GENERIC_TERMS**: 50+ always-disqualifying generic terms (utils, common, core, library, etc.)
- **Contextual disambiguation**: A term appearing in both sets is only counted if it carries need-specific context (nearby NEED_INDICATOR within 3-token window)
- **Fallback patterns**: Question forms, problem statements, direct requests, technical keywords

## Gates (per E071/E103/E116 protocol, adapted)

| Gate | Criterion | Threshold |
|------|-----------|-----------|
| G1 | Classified sample size | ≥ 100 total (50 per group minimum) |
| G2 | Coverage floor | ≥ 80% of representative pool classified |
| G3 | Effect size | Cliff's delta > 0.147 AND Mann-Whitney U p < 0.05 |
| G4 | Both categories represented | need-related > 0 AND random > 0 |

## Method

1. Load E107 raw harvest (160 GitHub repos with descriptions, star counts, classifications)
2. Apply E116 classifier to each repo's description (or name if description empty)
3. Classify as need-related, random, or uncertain based on weight >= 0.5 threshold
4. Compute engagement = stargazers_count
5. Evaluate all four gates

## Deliverables

- `analyze.py` — Gate evaluation script (this file)
- `results.json` — Full results with gate outcomes and coverage metrics
- `PROTOCOL.md` — This file
- `classify.py` — Classifier implementation (reused from E116 prototype)