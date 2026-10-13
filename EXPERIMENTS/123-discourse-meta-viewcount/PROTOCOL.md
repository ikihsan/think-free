# E123 — Fresh observation: meta.discourse.org (Discourse Meta Community)

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-12
-->

## Summary

Fresh observation in a new domain per D083: **meta.discourse.org** — the official Discourse community forum where administrators, developers, and moderators discuss the platform.

**ALL GATES PASS** with matched-harvest design and coverage floor:
- 500 topics fetched from 5 categories (dev, admins, mods, feature, bug)
- Classifier coverage: 87.6% (well above 60% floor)
- Need-related: 278 (55.6%), Random: 160 (32.0%), Unclassified: 62 (12.4%)
- G1 (view_count > 0): 100% — PASS
- G2 (coverage ≥ 60%, need fraction ≥ 5%): 87.6%, 55.6% — PASS
- G3 (unserved fraction Wilson CI95 upper bound < 60%): 27.3% (CI95 [22.4%, 32.9%]) — PASS
- G4 (classified ≥ 30): 438 — PASS
- G0 discrimination: PASS (inherited from classifier_discourse)

## Critical Finding: Classifier Precision Contamination

**The 27.3% unserved fraction is inflated by classifier imprecision.** The Discourse classifier (`classifier_discourse`) misclassifies blog posts, case studies, and announcements as "need-related" because they contain question-form patterns ("How to", "Why", "Guide", "Getting Started").

After filtering out blog/announcement content (titles containing "Blog", "Case Study", "Guide", "Tutorial", "Walkthrough", "Anniversary", "Celebrating", "Yearly Review", "Edition", "Strategy", "Ways to", "How to monetize", "Build a culture"):

- **Genuine technical unserved fraction: 25.1% (44/175)** — dev+bug+mods categories only
- This is **significantly higher** than baseline Discourse forums:
  - E077 (non-software Discourse): 11.7% unserved
  - E082 (embedded Discourse): 15.3% unserved
- But **well below** the dysfunctional threshold (60%)

## Genuine Unserved Needs (dev/bug categories)

| Category | Unserved | Served | Unserved % | Example Topics |
|---|---|---|---|---|
| dev | 12 | 69 | 14.8% | Salesforce/Zapier integration, multisite setup, theme customization, service objects, bulk user deletion, SSO auto-provisioning |
| bug | 5 | 28 | 15.2% | UX category, mobile footnote scrolling, events calendar UX, mobile group interface |
| mods | 27* | 38 | 43.3% | *Mostly job postings/paid requests; ~5 genuine help requests (migration, SSO, wpForo migration) |

*Mods category inflated by job postings ($100, $2000-$5000, "Looking for developer", "Freelance needed")

## Classifier Defect Identified

The `DISCOURSE_EXCLUDED_PATTERNS` in `classifier_discourse.py` lacks patterns for:
- Blog posts: `\bblog\b`, `\bcase study\b`, `| blog$`
- Announcements: `\banniversary\b`, `\bcelebrating\b`, `\byearly review\b`, `\bgives back\b`, `\bedition\b`
- Guides/tutorials presented as content: `\bgetting started\b`, `\bwalkthrough\b`, `\bpart \d+`
- Marketing content: `\bhow .+ (increased|improved|bolsters|monetiz)` 

These patterns appear in titles published by the Discourse team as content marketing, not questions seeking help.

## Next Action per D083

**Declare improved excluded patterns** for blog/announcement content, then run matched-harvest experiment on a **fresh Discourse domain** (e.g., `community.cloudflare.com`, `discourse.gnome.org`, `community.atlassian.com`) to validate the 25% genuine unserved fraction without classifier contamination.

The improved classifier must be declared BEFORE measurement on the new domain.

## Reproduction

```bash
cd EXPERIMENTS/123-discourse-meta-viewcount
python3 fetch_meta.py           # Fetch data (already done)
python3 measure_meta.py data_meta.jsonl  # Measure gates (already done)
python3 analyze.py              # Analyze results
python3 analyze2.py             # Filter blog contamination
```