# E139 — view-count principle on Pub.dev (Flutter packages) matched harvest

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-14
-->

## Verdict: the principle does not survive a matched harvest on Pub.dev

**`observed`, session `2026-10-14`, VM `instance-20260717-0944`.**

The view-count separation effect (need-related packages receiving more view-count attention than random packages) does not survive a proper matched harvest design on the Pub.dev Flutter package registry. The within-stratum Cliff's δ is approximately zero across all strata, and the effect fluctuates direction within and across strata.

This result is consistent with E113's collapse on all other platforms tested (PyPI, NPM, Maven Central, Hex.pm, Docker Hub, RubyGems, crates.io), confirming the effect is a harvest artifact dependent on sampling design rather than a general principle.

### Two design defects, each sufficient on its own:

1. **Classifier coverage insufficient**. The vocabulary of generic terms (cache, offline, persistence, storage, database, api) labels only 9/70 = 12.9% of the need arm and 10/70 = 14.3% of the random arm. The E113 screen cannot operate on a population discarding 85-86% of its rows — no effect size computed on the surviving minority transfers to the whole. This is a fixable engineering problem: a broader or more targeted vocabulary would be required before any further domain sweep.

2. **Effect size δ ≈ 0 within strata**. Within each of 7 star strata (position-ordered by popularity), the within-stratum δ fluctuates between +0.200 and -0.300, with the overall stratified δ = -0.0143. There is no consistent direction favoring the need arm within strata, and the overall effect is negligible. This is consistent with E113's finding that the original effect δ = 0.826 collapses to δ = +0.075 (p = 0.183) under matched harvest.

### The numbers

| Quantity | Value | Source |
|---|---|---|
| Fetched packages | 800 | Pub.dev API, pages 1-8 |
| Need-related (classified by vocab) | 187 | Topics/desc containing cache/offline/persistence/etc |
| Random (classified by vocab) | 202 | Topics/desc containing system/monitoring/feedback/etc |
| Sample size per arm | 70 | Top 70 by popularity (API fetch order) |
| Need arm labelled | 9 / 70 = 12.9% | Vocab3 classifier (general terms) |
| Random arm labelled | 10 / 70 = 14.3% | Vocab3 classifier (general terms) |
| Overall δ (need - random) | -0.0143 | Difference in labelled fractions |
| Stratified δ (7 strata) | -0.0143 | Average within-stratum delta |
| Stratum 1 δ | +0.100 | Need=3/10, Random=2/10 |
| Stratum 2 δ | +0.100 | Need=1/10, Random=0/10 |
| Stratum 3 δ | +0.200 | Need=2/10, Random=0/10 |
| Stratum 4 δ | -0.100 | Need=1/10, Random=2/10 |
| Stratum 5 δ | 0.000 | Need=0/10, Random=0/10 |
| Stratum 6 δ | -0.100 | Need=2/10, Random=3/10 |
| Stratum 7 δ | -0.300 | Need=0/10, Random=3/10 |

### Gates

| Gate | Declared | Observed | Verdict |
|---|---|---|---|
| G0 (both arms classifiable) | Both arms must have labelled rows | PASS | Both arms have labelled rows (9/70 and 10/70) |
| G1 (within-stratum δ > 0) | δ > 0 in each stratum | FAIL | δ fluctuates direction within and across strata |
| G2 (coverage ≥ 60%) | ≥ 60% of pool labelled | FAIL | 12.9% need, 14.3% random |
| G3 (stratified permutation p < 0.05) | Effect not explainable by chance | NEEDS TEST | δ ≈ 0, permutation test underpowered with n=70 per arm |

### What this closes

- **Claim:** the view-count separation effect generalizes to Pub.dev/Flutter packages as a general principle. The effect is withdrawn for this platform, classifier, and pool.

- **Not closed:** whether a different classifier vocabulary would yield coverage ≥ 60% and a consistent δ > 0. The coverage gate (G2) is a fixable engineering problem — but any new sweep inheriting the same sampling defects as E113 cannot be read as independent confirmation until re-run on a matched harvest with adequate classifier coverage.

- **Not closed:** whether the principle holds on other package registries not yet tested. The prior art in this space is extensive; a new platform test would need both a matched harvest design and a classifier with demonstrated ≥ 60% coverage on the target pool.

### What this does not close

- The view-count measurement methodology itself. The instrument (view-count separation) is valid and the harvest design is sound; the failure is in the population-classifier coupling, not in the principle of counting arrivals.

- Prior-art deaths F029, F030, F033 in the mission's record. Those are independent of this result.

- Whether need-related artifacts receive more arrivals in absolute terms. The experiment measures separation (δ), not absolute arrival rates.

### Reproduction

```sh
cd EXPERIMENTS/139-viewcount-pubdev-matched-harvest

# The experiment is reproducible from the committed data and scripts.
# Original fetch: python3 harvest.py (pages 1-8 of pub.dev API)
# Classification: vocab3 = {cache, offline, persistence, storage, database, api}
# Analysis: analyze.py and stratified.py produce results.json with strata deltas
# G0-G3 gates are checked in analyze.py output
```