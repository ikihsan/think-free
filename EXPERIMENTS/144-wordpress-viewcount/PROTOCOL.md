<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-15
-->

# E144: View-count principle on WordPress plugins

## Objective

Test whether the view-count principle generalizes to wordpress.org plugins:
- Need-related plugins (those with keywords indicating caching, security, SEO,
  performance optimization, backup, contact forms, and similar practical needs)
  have systematically higher active installation activity than random plugins.

## Conclusion

**Negative result: The view-count principle does not generalize to WordPress plugins.**

Need-related plugins have a **13.8 percentage point LOWER** active installation rate
than random plugins (82.5% vs 96.3%, z = -3.29, p = 0.05). This is the opposite
direction of the view-count principle's prediction.

## Experiment History

This experiment (E144) tested the view-count principle on wordpress.org plugins,
a package registry ecosystem with "active installations" metadata analogous to
download counts on other platforms. This was a fresh domain — the mission had
not previously conducted a focused view-count experiment on WordPress plugins.

Previous view-count principle tests:

- PyPI (E071): **SUPPORTED** — need-related 82.93% active vs random 57.50%
- NPM (E072): **SUPPORTED** — 100% need-related active vs 0% random
- Maven Central (E090): **NOT SUPPORTED**
- crates.io (E095): **NOT SUPPORTED** — all crates 100% active, no discrimination
- CPAN (0xx-cpan-viewcount): **ALL GATES PASS** — need-related 94.6% vs random 86.1%
- WordPress plugins (E144): **NOT SUPPORTED** — need-related LOWER activity

## Key Findings

1. **Sample**: 103 need-related plugins and 109 random plugins classified from 7 need-related keywords and 10 random keywords

2. **Active installation rates**:
   - Need-related: 85/103 = 82.5%
   - Random: 105/109 = 96.3%
   - Difference: -13.8 pp (need-related LESS active)

3. **Gate evaluation**:
   - G1 (sample size ≥ 100 each): PASS
   - G2 (significance p < 0.05): FAIL — need-related significantly LOWER (p = 0.05, z = -3.29)
   - G3 (Wilson LB > 0.60): PASS — Wilson LB = 0.74 (but this just means the rate is reasonably high, not that it's higher than random)
   - G4 (arrival field rate ≥ 95%): FAIL — need 82.5%, random 96.3%

4. **Interpretation**: The "active signal" for need-related plugins is not elevated on wordpress.org. In fact, the reverse is observed. This suggests that need-related keywords on WordPress plugins may be more common on niche/smaller plugins rather than widely-adopted ones, or that the "active installations" metric doesn't correlate with "need" in the expected way on this platform.

## Files

- `EXPERIMENTS/144-wordpress-viewcount/PROTOCOL.md` — Experiment protocol
- `EXPERIMENTS/144-wordpress-viewcount/collect.py` — Data collection script
- `EXPERIMENTS/144-wordpress-viewcount/results.json` — Gate evaluations and statistics