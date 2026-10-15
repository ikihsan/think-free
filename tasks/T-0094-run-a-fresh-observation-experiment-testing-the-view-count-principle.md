<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-15
-->

# T-0094 — Run a fresh observation experiment testing the view-count principle

## Goal

Build and run a prototype view-count classifier analyzing whether the principle's activity advantage varies across Python package popularity tiers and ages on PyPI. The prototype should test the boundary condition: "principle works on platforms with per-request metadata where need-related content has systematic activity advantages, AND the classification vocabulary is platform-appropriate." Report gate results (G1-G4) and effect sizes across tiers.

## Background

The view-count principle states: "On platforms with per-request metadata (view_count/download_count/star_count), need-related content has systematic activity advantages over random content." This mission has validated the principle on PyPI, NPM, NuGet, CPAN, Hex.pm, Docker Hub, Packagist, RubyGems, and GitHub repos. It does NOT generalize to Q&A forums, model hubs, crates.io, GitLab, or platforms without such metadata.

The boundary condition requires BOTH per-request metadata AND platform-appropriate classification vocabulary.

The named next action (STATE-next-actions.md): "fresh observation in a domain this mission has not touched, chosen by a stated rule rather than by comfort."

## Approach

Adapt the existing view-count prototype framework (tools/viewcount_framework.py, tools/viewcount_core.py, tools/viewcount_prototype.py). The framework provides need-indicator classifier vocabulary, gate computation (G1-G4), and PyPI registry adapter.

For this experiment, I will analyze whether the G1 activity advantage (need-related active rate >= 55% of random) varies across:
- **Popularity tiers**: top 1/3, middle 1/3, bottom 1/3 by download count
- **Package age tiers**: first release year terciles

This is fresh because while PyPI as a domain has been tested extensively, the principle's behavior across popularity tiers and across package ages has not been systematically examined.

## Mileposts

1. Fetch packages from PyPI using keyword search and classify each as need-related or random using word-boundary matching
2. Compute G1-G4 gates and report pass/fail status
3. Analyze G1 activity ratio variation across popularity tiers
4. Analyze G1 activity ratio variation across package age tiers
5. Produce results.json with full gate outcomes and analysis

## Verification

`tools/origin doc lint` must exit 0.
