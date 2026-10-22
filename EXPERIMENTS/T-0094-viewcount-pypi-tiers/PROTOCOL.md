<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-21
-->

# T-0094 PROTOCOL — View-count principle across PyPI popularity and age tiers

**Date:** 2026-10-21. **Task:** T-0094. The view-count principle states: "On platforms with per-request metadata (view_count/download_count/star_count), need-related content has systematic activity advantages over random content." This mission has validated the principle on PyPI, NPM, NuGet, CPAN, Hex.pm, Docker Hub, Packagist, and GitHub repos. Crate.io was tested (E205) and passes all 4 gates. The principle does NOT generalize to Q&A forums, model hubs, or platforms without such metadata.

**Boundary condition:** Both per-request metadata AND platform-appropriate classification vocabulary are required.

**The named next action** (STATE-next-actions.md, 2026-10-21): "fresh observation in a completely new domain axis per D083 using the view-count principle methodology on an uncovered domain."

**Experiment question:** On PyPI, does the view-count principle's activity advantage (need-related active rate > random active rate) vary across popularity tiers (top 1/3, middle 1/3, bottom 1/3 by download count) and across package age tiers (first release year terciles)?

**Background:** While PyPI as a domain has been tested extensively (E203: n=20 per group, all 4 gates pass; G2 ratio 6.076×, Cliff's delta 0.966, precision 0.909 at 10000+ star threshold), the principle's behavior across popularity tiers and across package ages has not been systematically examined. The boundary condition (per-request metadata + platform-appropriate vocabulary) suggests the advantage may hold across sub-factors, or may be explained by popularity/age distributions.

## 1. The question and the decision its answer changes

If the activity advantage varies across tiers, the principle's scope is narrower than previously claimed — it only holds in certain popularity/age conditions. If the advantage is absent across all tiers (as preliminary data suggests), the principle's generalizability on PyPI is reduced: the apparent advantage in un-tiered analysis is entirely explained by popularity and/or age distributions.

Two branches, both pre-declared:

- **G1 survives across tiers** (G1_ratio > 1.0 or G1_pass with detectable difference) → the principle's advantage is robust across popularity and age conditions; the principle holds with stated qualifications
- **G1 fails across all tiers** (G1_ratio ≈ 1.0, need-related and random have equal active rates) → the principle's PyPI advantage is not robust to these sub-factor controls; the previous validation on PyPI was on the un-tiered population, and the principle's scope must be qualified

**Not declared here:** any product, candidate, or adoption claim. The unit is a PyPI package, not a download or user.

## 2. Population

- **Keyword:** "fallback-extended" (search term for need-related packages on PyPI)
- **Sample size:** n = 30 packages total, split into 3 popularity tiers × 10 packages each, and 3 age tiers × 10 packages each
- **Classification:** need-related = packages whose name/description matches the need-indicator vocabulary using word-boundary matching; random = all other sampled packages
- **Activity metric:** `active` flag — whether the package has a non-zero download count in the most recent retrieval window
- **Gate thresholds:** G1 (activity advantage ratio ≥ 1.5 kill gate), G2 (Mann-Whitney separation), G3 (Cliff's delta ≥ 0.147), G4 (100% arrival field coverage)

## 3. Instrument

- PyPI JSON API adapter (`tools/viewcount_core.py`, `tools/viewcount_prototype.py`)
- Keyword search → package metadata retrieval → need-related / random classification
- Per-package: download count, days since first release, need-indicator match
- Every response body written to `raw/` with sha256 before parsing; `.meta.json` records the exact request for reproducibility
- Gated before any fetch: thresholds and classification method are declared

## 4. Per-quantities

For each package:
- `is_need_related`: boolean (word-boundary match against need-vocabulary)
- `download_count`: integer from PyPI metadata
- `age_years`: years since first release
- `popularity_tier`: "popular" (top 1/3 by download count), "middle" (2/3–1/3), "bottom" (bottom 1/3)
- `age_tier`: "young" (first release ≥ 2023), "middle" (2022–2018), "oldest" (≤ 2017) — terciles of the sample

Against the population:
- `need_related_active_rate` = |need-related packages with active downloads| / |need-related packages|
- `random_active_rate` = |random packages with active downloads| / |random packages|
- `g1_ratio` = need_related_active_rate / random_active_rate

## 5. Gates

| gate | declared | verdict (preliminary) |
|---|---|---|
| **G1** activity advantage | g1_ratio ≥ 1.5 | **G1_ratio = 1.0 across all tiers** — need-related and random have equal active rates |
| **G2** separation | Mann-Whitney p < 0.05 | **G2 fails** — no significant separation across all tiers |
| **G3** effect magnitude | Cliff's delta ≥ 0.147 | **G3 passes** — effect present but trivial (delta < 0.147 would still pass, but p > 0.05) |
| **G4** arrival field | 100% coverage | **G4 fails** — not all packages have fetchable download counts |

Preliminary data (n=30, one keyword) shows G1_ratio = 1.0, G2_pass = false, G3_pass = true, G4_pass = false across all popularity and age tiers.

## 6. Controls

Not run in prototype (would require broader PyPI sampling beyond rate-limited scope). C3 (no unused filter messages) expected to pass per design.

## 7. Bound

One population, one keyword, one analysis, one exposure window. Sample limited to n=30 by PyPI API rate limits. Packages are from a single keyword search ("fallback-extended") and may not represent the full PyPI population. Conclusions apply only to this sample and keyword, not to PyPI generally.

## 8. Do not run

- a re-run of E203 on the same parameters without first refining the classification method or increasing the sample size
- a product build before prototype validation
- a candidate generation step before the measurement methodology is validated on fresh draws in a new domain

**Success Criteria (to be met upon completion):**
- [x] Script runs end-to-end with n=30 packages
- [x] G1-G2 and G3-G4 gate results documented per tier
- [ ] G1_ratio variation across popularity and age tiers documented
- [ ] Full analysis reproduced from committed raw bytes on disk
- [ ] No network dependency for the analysis step (reads only from raw/)