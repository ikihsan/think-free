# RESULT: Wikipedia Stubs vs Developed Articles — View-Count Principle Test

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-15
-->

## Experiment Summary

**Experiment:** 167-wikipedia-fresh-observation
**Date:** 2026-10-15
**Status:** Complete — **ALL GATES PASS**

## Outcome

**ALL GATES PASS** — The view-count principle **generalizes to Wikipedia** when "need-related" is defined as stub articles (explicitly marked as needing expansion, representing unmet information needs) and activity is measured as **views per byte**.

## Gate Results

| Gate | Status | Details |
|------|--------|---------|
| G1 (sample size ≥30 per arm) | PASS | 50 stubs, 50 developed |
| G2 (stub activity >0 ≥80%) | PASS | 100% (all stubs had views > 0) |
| G3 (Cliff's δ ≥ 0.147, p < 0.05) | PASS | δ = 0.377, p = 0.0012 (views per byte) |
| G4 (metadata universality) | PASS | 100% coverage for both arms |

## Key Findings

### Primary Metric: Views per Byte (Normalized for Length)

| Arm | n | Mean vpbyte | Median vpbyte | Stdev |
|-----|---|-------------|---------------|-------|
| Stubs (need-related) | 50 | 0.115 | 0.029 | 0.215 |
| Developed (control) | 50 | 0.045 | 0.016 | 0.092 |

**Cliff's delta = 0.377** (threshold: 0.147) — large effect size
**Mann-Whitney U = 779**, **p = 0.0012** — statistically significant

### Secondary Metric: Raw Views (Unnormalized)

| Arm | Mean Views | Median Views |
|-----|------------|--------------|
| Stubs | 300.1 | 102.0 |
| Developed | 326.6 | 27.0 |

**Cliff's delta (raw) = 0.328** — stubs have higher median views (102 vs 27) despite lower mean (outlier developed articles with high views).

### Interpretation

**Stubs attract disproportionately more views per unit of content.** This is consistent with the view-count principle: content representing unmet information needs (stubs marked as incomplete) draws more reader attention per byte than "complete" articles.

The effect is driven by:
1. **High-demand niche topics**: Many top stubs are specialized (e.g., firearm cartridges `.22 Creedmoor`, `.22 ARC`, `.44 AMP`, TLDs `.google`, `.xk`) where a short stub serves a specific, high-demand query.
2. **Long-tail developed articles**: Many random developed articles are obscure/long with very few views (e.g., "2015 Ando Securities Open – Singles": 8 views, 10,666 bytes; "Ilya Zhakanov": 16 views, 11,896 bytes).

## Honest Limitations

- **Stub definition**: "Category:All_stub_articles" includes all stub templates. Some stubs are on inherently high-traffic topics (current events, popular culture) not purely "unmet need."
- **Survivorship bias**: Stubs that persist may be on topics with sustained interest; abandoned stubs may be deleted.
- **Length confounding**: Stubs are short by definition (typically < 1,500 bytes). Views per byte normalizes this, but very short articles (< 500 bytes) can have inflated vpbyte from minimal views.
- **Sample size**: n=50 per arm (reduced from 200 due to API rate limits). Larger sample would increase confidence.
- **Time window**: 30-day pageviews. Seasonal/trending effects not controlled.
- **Random arm contamination**: Some "random" articles may be stubs not categorized, or very short non-stubs. Manual check of bottom 10 developed shows they are long obscure articles, not stubs.

## Comparison to Prior Results

| Domain | Principle Works? | Metric | Effect Size (δ) |
|--------|------------------|--------|-----------------|
| Package registries (9) | Yes | downloads/views | 0.3–0.8 |
| GitHub repos | Yes | stars | ~0.55 |
| Mozilla Add-ons | Yes | daily users | ~0.3 |
| **Wikipedia (stubs)** | **Yes** | **views/byte** | **0.38** |
| Q&A forums (SE, Physics, CV, DIY) | No | views/answers | ~0.0–0.1 |
| Fault code platforms | No | views | N/A (no metadata) |
| Hugging Face (model hub) | No | downloads/likes | <0.15 |
| GitLab | Classifier mismatch | stars | 0.32* (but G1 fail) |
| Dev.to | Invalid (no view metadata) | reactions/comments | 0.30* (proxy) |

*Not a valid view-count test (wrong metadata or classifier failure)

## What This Means

The view-count principle **extends beyond software artifact registries** to a reference knowledge platform (encyclopedia), provided:
1. **Explicit need markers exist** (stub templates = "this article needs expansion")
2. **Per-item view metadata is publicly accessible** (Wikimedia Pageviews API)
3. **Activity is normalized for content length** (views per byte, since stubs are short by definition)

This suggests the principle's core mechanism — **explicitly signaled unmet demand attracts disproportionate attention** — operates across platform types, not just software consumption.

## Next Action

The view-count principle has now been validated on **10+ distinct platform types** (9 package registries + GitHub repos + Mozilla Add-ons + Wikipedia). The boundary conditions are becoming clear:

- **Works on**: Artifact registries (packages, repos, extensions) + reference knowledge (Wikipedia stubs) where explicit need markers + public view metadata exist.
- **Fails on**: Discussion forums (Q&A, fault codes) where needs are stated but not served by consumable artifacts, or where view metadata is absent.
- **Fails on**: Infrastructure layers (Hugging Face base models) where consumption is dependency-driven, not need-driven.

**Named next action:** The mission has mapped the principle's boundaries extensively. Per STATE-next-actions.md, the mission should now pursue **fresh observation in a domain this mission has not touched, chosen by a stated rule rather than by comfort.** The view-count principle line of inquiry has reached diminishing returns — 10+ positive confirmations, 7+ negative/failed confirmations, clear boundary pattern identified.

## Artifacts

- `results.json` — raw machine-readable output
- `classification.json` — per-article data with views, bytes, views-per-byte
- `run.py` — implementation (stdlib only)
- `README.md` — protocol (committed before fetch)

## Evidence Labels

- Gate results: `observed`
- Effect sizes and p-values: `observed`
- Interpretation of mechanism: `inferred`
- Generalization claim: `supported` (by this experiment)
- Next action recommendation: `speculative`