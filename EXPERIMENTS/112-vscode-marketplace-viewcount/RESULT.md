<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-12
-->

# E112 — VS Code Marketplace View-Count Experiment Results

## Summary

Tested whether the view-count principle generalizes to IDE extension marketplaces (VS Code Marketplace). Used matched harvest design with keyword-based classification (declared before measurement).

## Gates

| Gate | Threshold | Result |
|------|-----------|--------|
| G1 | ≥95% have install_count > 0 | **PASS** (100.0%) |
| G2 | Classifier coverage ≥60% AND need fraction ≥5% | **PASS** (71.2% coverage, 33.2% need fraction) |
| G3 | Cliff's delta > 0.2 AND p < 0.05 | **FAIL** (δ = 0.1579, p < 0.000001) |
| G4 | ≥50% of need-related have >100 installs | **PASS** (100.0%) |

## Key Metrics

- **Total extensions harvested**: 2,000
- **Classified (need + random)**: 1,425 (71.2% coverage)
- **Need-related**: 665
- **Random**: 760
- **Unclassified**: 575
- **Need median installs**: 626,540
- **Random median installs**: 379,359
- **Need/Random median ratio**: 1.65×
- **Cliff's delta**: 0.1579
- **Mann-Whitney U p-value**: < 0.000001

## Interpretation

The view-count principle shows a **directional but weak effect** on VS Code Marketplace:
- Need-related extensions have ~1.65× higher median install counts
- The difference is statistically highly significant (p < 0.000001) due to large sample size
- However, the effect size (Cliff's delta = 0.158) falls below the 0.2 threshold for practical significance
- This means a random need-related extension has only ~58% chance of having more installs than a random non-need extension

## Comparison with Other Domains

| Domain | Cliff's delta | Verdict |
|--------|---------------|---------|
| PyPI | ~0.5+ | Strong |
| NPM | ~0.5+ | Strong |
| NuGet | 0.996 | Very strong |
| Hex.pm | 0.861 | Strong |
| Packagist | 0.994 | Very strong |
| RubyGems | 0.214 | Weak but passes |
| Docker Hub | 0.386 | Moderate |
| Discourse (support) | N/A (unserved fraction) | Passes |
| **VS Code Marketplace** | **0.158** | **Fails threshold** |
| GitHub repos (E107) | 0.826* | *Harvest artifact (E113) |

## Why the Effect Is Weak

Possible explanations:
1. **Marketplace dynamics**: Install counts reflect bundling (e.g., language packs), IDE defaults, and enterprise distribution, not just individual need
2. **Keyword coverage**: The need keywords capture many popular utility extensions (linting, formatting, Git, Docker) but miss some problem-solving extensions
3. **Excluded keywords**: May remove popular extensions from random arm that are genuinely non-need (themes, snippets)
4. **Platform structure**: Unlike package registries where downloads = "I need this library", marketplace installs = "this might be useful" + bundling + defaults

## Conclusion

**The view-count principle does not robustly generalize to VS Code Marketplace.** While need-related extensions have statistically significantly higher install counts, the effect size (δ = 0.158) is below the practical significance threshold (δ > 0.2). This maps a boundary condition for the principle: IDE extension marketplaces combine software distribution with curation/bundling, diluting the need signal.

## Artifacts

- `raw_data.jsonl` — 2000 extensions with classifications
- `classified_data.jsonl` — 1425 classified extensions
- `results.json` — Full gate results
- `harvest.py` — Harvesting script
- `measure_vscode.py` — Measurement script
- `PROTOCOL.md` — Original protocol
- `RESULT.md` — This file

## Evidence Labels

All metrics: **observed** (directly measured from harvested data)
Cliff's delta interpretation: **inferred** (effect size threshold is a convention)
Domain boundary claim: **observed** (measured on this platform)
