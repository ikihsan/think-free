<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-12
-->

# E128 — GitHub Discussions View-Count Experiment Results

## Summary

Tested whether the view-count principle generalizes to GitHub Discussions (code-hosting platform community discussions). Used matched harvest design with pattern-based classification (declared pre-measurement) across 6 technical repositories.

## Gates

| Gate | Threshold | Result |
|------|-----------|--------|
| G1 | ≥95% have engagement > 0 | **FAIL** (83.0%) |
| G2 | Classifier coverage ≥60% AND need fraction ≥5% | **PASS** (87.7% coverage, 37.2% need fraction) |
| G3 | Cliff's delta > 0.2 AND p < 0.05 | **FAIL** (δ = -0.085, p = 0.0009) |
| G4 | ≥50% of need-related have >10 engagement | **FAIL** (13.0%) |

## Key Metrics

- **Total discussions harvested**: 2,302 (from 6 repositories)
- **Classified (need + random)**: 2,019 (87.7% coverage)
- **Need-related**: 857
- **Random**: 1,162
- **Unclassified**: 283
- **Need median engagement**: 2 (reactions + comments)
- **Random median engagement**: 3 (reactions + comments)
- **Cliff's delta**: -0.0853 (negative!)
- **Mann-Whitney U p-value**: 0.000944
- **Need active rate (>10 engagement)**: 13.0%

## Interpretation

The view-count principle **strongly fails** on GitHub Discussions:

1. **G1 fails**: 17% of discussions have zero engagement (no reactions, no comments). The arrival metric doesn't cover the population.

2. **Effect is in the wrong direction**: Random discussions (announcements, showcases, version updates) have **higher median engagement (3)** than need-related discussions (questions, debugging, help requests) with **median engagement (2)**. Cliff's delta = -0.085.

3. **Statistical significance but wrong sign**: p = 0.0009 confirms the difference is real, but need-related discussions get *less* engagement.

4. **Low active rate**: Only 13% of need-related discussions exceed 10 total engagement.

## Why the Principle Fails Here

GitHub Discussions engagement (reactions + comments) reflects:
- **Community signaling** (👍 for announcements, 🎉 for releases)
- **Entertainment/agreement** (memes, jokes, popular opinions)
- **Project governance** (RFCs, proposals)

Not individual need-seeking behavior. A developer with a debugging question doesn't generate 👍 reactions; they get answers (comments) but low reaction counts. Meanwhile, "Version 2.0 released!" gets hundreds of 👍.

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
| VS Code Marketplace | 0.158 | Fails threshold |
| **GitHub Discussions** | **-0.085** | **Fails (wrong direction)** |
| GitHub repos (E107) | 0.826* | *Harvest artifact (E113) |

## Conclusion

**The view-count principle does not generalize to GitHub Discussions.** The arrival metric (reactions + comments) measures community signaling and entertainment, not need-seeking. Need-related discussions systematically receive *less* engagement than announcements/showcases. This maps a clear boundary: code-hosting platform discussions are a platform type where the principle fails.

## Artifacts

- `raw_data.jsonl` — 2302 discussions with classifications
- `classified_data.jsonl` — 2019 classified discussions
- `results.json` — Full gate results
- `harvest.py` — Harvesting script
- `measure_github_discussions.py` — Measurement script
- `PROTOCOL.md` — Original protocol
- `RESULT.md` — This file

## Evidence Labels

All metrics: **observed** (directly measured from harvested data)
Cliff's delta interpretation: **observed** (negative effect measured)
Domain boundary claim: **observed** (measured on this platform)
