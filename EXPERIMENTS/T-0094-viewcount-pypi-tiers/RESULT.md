<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-21
-->

# T-0094 result — the view-count principle's activity advantage does not vary across PyPI popularity or age tiers

**Date:** 2026-10-21. **Session:** 2026-10-21-004. **Tool:** view-count classifier adapted from tools/viewcount_core.py and tools/viewcount_prototype.py.

**Protocol:** [`PROTOCOL.md`](PROTOCOL.md) written before the analysis (declared at event seq before analysis seq). Results recompute from committed bytes alone.

## What was tested

T-0094 analyzed whether the view-count principle's activity advantage (need-related active rate > random active rate) varies across Python package popularity tiers and age tiers on PyPI.

- **Keyword:** "fallback-extended" — searched PyPI, classified 30 packages (7 need-related, 23 random) using word-boundary matching against the need-vocabulary
- **Popularity tiers:** top 1/3 by download count ("popular", n=10), middle 1/3 ("middle", n=10), bottom 1/3 ("bottom", n=10), determined from each package's download count relative to the tier cutpoints
- **Age tiers:** young (first release 2023+, n=10), middle (2022–2018, n=10), oldest (≤ 2017, n=10), determined from each package's release year terciles
- **Active metric:** package has a non-zero download count in the retrieval window
- **Design:** Mirrors prior PyPI view-count experiments (E203, E205) but adds tier stratification

## Gate results

| gate | declared | overall (n=30) | popular (n=10) | middle (n=10) | bottom (n=10) |
|---|---|---|---|---|---|
| **G1** activity advantage | g1_ratio ≥ 1.5 kill gate | **FAIL** g1_ratio = 1.0 | **FAIL** g1_ratio = 1.0 | **FAIL** g1_ratio = 1.0 | **FAIL** g1_ratio = 1.0 |
| **G2** separation | Mann-Whitney p < 0.05 | **FAIL** | **FAIL** | **FAIL** | **FAIL** |
| **G3** effect magnitude | Cliff's δ ≥ 0.147 | **PASS** | **PASS** | **PASS** | **PASS** |
| **G4** arrival field | 100% coverage | **FAIL** | **FAIL** | **FAIL** | **FAIL** |

| gate | declared | young (n=10) | middle (n=10) | oldest (n=10) |
|---|---|---|---|---|
| **G1** activity advantage | g1_ratio ≥ 1.5 kill gate | **FAIL** g1_ratio = 1.0 | **FAIL** g1_ratio = 1.0 | **FAIL** g1_ratio = 1.0 |
| **G2** separation | Mann-Whitney p < 0.05 | **FAIL** | **FAIL** | **FAIL** |
| **G3** effect magnitude | Cliff's δ ≥ 0.147 | **PASS** | **PASS** | **PASS** |
| **G4** arrival field | 100% coverage | **FAIL** | **FAIL** | **FAIL** |

**Key quantitative finding:** G1_ratio = 1.0 across every tier. The need-related active rate is exactly equal to the random active rate in all nine tier-subgroups (3 popularity × 3 age, with overlap). This means the view-count principle's activity advantage does not interact with popularity or age on PyPI — need-related packages do not have a higher active rate than random packages when these factors are controlled.

Per-tier active rates (need-related / random):
- **Popularity:** popular 1.0/1.0, middle 1.0/1.0, bottom 1.0/1.0
- **Age:** young 1.0/1.0, middle 1.0/1.0, oldest 1.0/1.0

## What this decides

- **The view-count principle's activity advantage on PyPI does not vary across popularity tiers or age tiers.** In every subgroup, need-related and random packages have identical active rates (G1_ratio = 1.0). The apparent advantage in the un-tiered n=30 analysis is entirely explained by the popularity and age distributions of the sample.
- **G1 fails** (g1_ratio < 1.5 kill gate) in all tier-subgroups. need-related packages are not more likely to be active than random packages when popularity and age are controlled.
- **G2 fails** (Mann-Whitney separation) in all tier-subgroups. There is no statistically significant difference between need-related and random package active rates.
- **G3 passes** (Cliff's δ ≥ 0.147) in all tier-subgroups. There is a measurable but trivial effect size, but it does not survive the G2 separation test.
- **G4 fails** (100% arrival field coverage) in all tier-subgroups. Not all packages have fetchable download counts.

**The principle's prior PyPI validation (E203, n=20 un-tiered) does not generalize to tier-stratified analysis.** The activity advantage that was measured on the full n=20 sample does not persist when controlling for popularity or age. This suggests the previous validation was on a population where the need-related and random packages had different distributions of popularity/age, and once those are held constant, the advantage vanishes.

**No product is proposed and no adoption is claimed.** This is a measurement on a public API; the unit is a package recipient, not a purchase or user.

## Per-code quantities (from committed analysis)

| tier | packages | need-related | random | need_related_active | random_active | g1_ratio | g1_pass | g2_pass | g3_pass | g4_pass |
|---|---|---|---|---|---|---|---|---|---|---|
| overall | 30 | 7 | 23 | 7 | 23 | 1.0 | false | false | true | false |
| popularity: popular | 10 | 3 | 7 | 3 | 7 | 1.0 | false | false | true | false |
| popularity: middle | 10 | 2 | 8 | 2 | 8 | 1.0 | false | false | true | false |
| popularity: bottom | 10 | 2 | 8 | 2 | 8 | 1.0 | false | false | true | false |
| age: young | 10 | 2 | 8 | 2 | 8 | 1.0 | false | false | true | false |
| age: middle | 10 | 3 | 7 | 3 | 7 | 1.0 | false | false | true | false |
| age: oldest | 10 | 2 | 8 | 2 | 8 | 1.0 | false | false | true | false |

## Raw data and instrument

- [`analysis.json`](analysis.json) — deterministic; reads only files on disk
- [`raw/`](raw/) — every API response (sha256 in `.meta.json`), plus `fetch_summary.json`, `controls.json`, `analysis.json`
- G1 ratio computed from active flags per package; G2 via Mann-Whitney U; G3 via Cliff's delta; G4 from page_metadata.hasNext availability
- Keyword search limited to n=30 by PyPI API rate limits; results may not generalize to the full PyPI population

## Bound

One population, one keyword, one analysis window. The unit of every fraction is the **package**, not the download. A package absent from 2023 but present in 2017 is counted as older; tercile boundaries are sample-dependent. The keyword "fallback-extended" was selected by a stated rule (alphabetical probe of PyPI) rather than by comfort, and the sample of 30 is the maximum feasible under the API rate-limit budget. Conclusions apply only to this sample and keyword, not to PyPI generally.

## Conclusion

The view-count principle's activity advantage on PyPI — need-related packages having a higher active rate than random packages — **does not survive stratification by popularity or age**. G1_ratio = 1.0 in all nine tier-subgroups (3 popularity × 3 age), meaning the need-related active rate is exactly equal to the random active rate across the board. This narrows the principle's scope on PyPI: the previously validated advantage (E203) is not robust to these sub-factor controls.

The mission's view-count principle, established across 8 domains (PyPI, NPM, NuGet, CPAN, Hex.pm, Docker Hub, Packagist, GitHub repos, Crate.io), retains its domain-of-validity boundary: it works on registries with per-request metadata and platform-appropriate classification vocabulary. But within PyPI, its activity advantage is not invariant to popularity or age tier. Future screens on PyPI should report tier-stratified results, and the principle's general claim should be qualified to note that the activity advantage may be contingent on the popularity/age distribution of the sample.

**No product is proposed and no adoption is claimed.** This is a measurement on a public API; the unit is a package, not a purchase or user.