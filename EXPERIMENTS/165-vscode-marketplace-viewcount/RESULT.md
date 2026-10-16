<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-16
-->

# Experiment 165: VS Code Marketplace View-Count Principle Test

## Objective
Test whether the view-count principle (need-related content has systematically higher activity metrics than general/random content) generalizes to the VS Code Marketplace extension registry.

## Method
- Fetched 1884 unique extensions from 28 categories via the VS Code Marketplace API (v7.1-preview.1)
- Classified extensions using keyword-based approach:
  - **need-related**: Extensions with problem-solving keywords (fix, debug, lint, test, deploy, etc.) - 1706 (90.5%)
  - **general**: Extensions with infrastructure/aesthetic keywords (theme, keymap, snippet, pack, etc.) - 105 (5.6%)
  - **other**: Extensions matching neither keyword list - 73 (3.9%)
- Measured Cliff's delta effect size on install count (primary) and other metrics

## Results

### Install Counts (Primary Metric)
| Group | n | Median | Mean | P25 | P75 |
|-------|---|--------|------|-----|-----|
| need-related | 1706 | 955 | 429,139 | 107 | 13,108 |
| general | 105 | 1,033 | 337,401 | 96 | 46,330 |
| other | 73 | 166 | 21,316 | 17 | 925 |

### Cliff's Delta Effect Sizes
| Comparison | install_count | average_rating | rating_count | trending_monthly | update_count | download_count |
|------------|---------------|----------------|--------------|------------------|--------------|----------------|
| need-related vs general | **-0.0266** | 0.0588 | 0.0059 | -0.0765 | -0.1173 | -0.3324 |
| need-related vs other | 0.3365 | -0.1241 | 0.1582 | 0.1892 | 0.2847 | 0.1023 |
| general vs other | 0.3391 | -0.1352 | 0.1429 | 0.2143 | 0.3124 | 0.1571 |

## Kill Gate Assessment
- **Primary gate (install_count, need-related vs general): Δ = -0.0266**
- Kill gate threshold from STATE.md: **|Δ| < 0.147** → **GATE FIRED**
- The effect size is negligible and slightly negative (general extensions have marginally higher installs)

## Interpretation
The view-count principle **does not generalize** to VS Code Marketplace with this keyword classification.

### Key Issues Identified
1. **Classifier too broad**: 90.5% of extensions classified as "need-related" - the keyword list (fix, debug, lint, test, deploy, tool, utility, helper, etc.) captures nearly all developer tools
2. **"General" category captures popular items**: Themes, keymaps, and snippet packs are genuinely high-install extensions
3. **Different marketplace dynamics**: VS Code Marketplace is an extension/tool marketplace, not a package registry like npm/PyPI where the principle was validated

### Comparison with Mozilla Add-ons (E162)
- E162 used **targeted keywords** (productivity, privacy) - not broad developer tool terms
- E162 measured **average_daily_users** not install count
- E162 had smaller sample (500) but more focused classification
- E162: G1-G4 all PASS; This experiment: Kill gate FIRED

## Conclusion
**Negative result**: The view-count principle does not extend to VS Code Marketplace with broad keyword classification. The principle's domain of validity remains package registries (PyPI, NPM, NuGet, CPAN, Hex.pm, Docker Hub, Packagist, RubyGems, GitHub repos) and Mozilla Add-ons with targeted classification.

## Next Steps
1. Record as negative result in FAILURES.md
2. Consider targeted replication with Mozilla-style keywords (productivity, privacy, security, accessibility) if warranted
3. Return to fresh exploration in a new domain