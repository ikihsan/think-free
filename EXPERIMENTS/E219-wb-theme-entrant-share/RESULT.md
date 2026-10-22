# E219 (2026-10-21) — fragmentation does not predict newcomer entry in World Bank project themes; kill gate fires on near-zero correlation

**Fresh observation per D083 in a completely new domain axis:** International development funding (World Bank projects), distinct from research funding (NIH SBIR), government procurement (USAspending), trade (Comtrade), academic publications (OpenAlex), and drug safety (FDA).

## Design
Mirrored E208/E209/E215/E218 accessibility-pattern entry test. Measured segment newcomer fractions for 10 World Bank major theme codes (1-11, excluding compound themes) using implementing agencies as identity.

- **Current window:** FY2020–2024 (1,583 single-theme projects, 1,353 distinct agencies)
- **Prior window:** FY2015–2019 (380 single-theme projects, 367 distinct agencies)  
- **Identity field:** `impagency` (implementing agency name)
- **Fragmentation metric:** top-5 agency share of project count in current window
- **Newcomer metric:** fraction of current-window agencies absent from prior window
- **Gates declared before fetch** (protocol in `run_e219.py`)

## Results

| Theme | Current Projects | Current Agencies | Prior Agencies | Top-5 Share | Newcomer Fraction |
|-------|------------------|------------------|----------------|-------------|-------------------|
| 1     | 46               | 45               | 20             | 0.130       | 0.956             |
| 2     | 201              | 164              | 50             | 0.184       | 0.945             |
| 3     | 52               | 48               | 12             | 0.173       | 0.979             |
| 4     | 256              | 218              | 62             | 0.125       | 0.986             |
| 5     | 83               | 77               | 40             | 0.133       | 0.974             |
| 6     | 133              | 117              | 33             | 0.143       | 0.983             |
| 7     | 96               | 87               | 22             | 0.146       | 0.977             |
| 8     | 177              | 148              | 42             | 0.181       | 0.980             |
| 9     | 105              | 94               | 28             | 0.152       | 0.968             |
| 10    | 248              | 205              | 57             | 0.165       | 0.976             |
| 11    | 327              | 281              | 73             | 0.131       | 0.968             |

**G0 PASS** (API accessible, no auth required)  
**G1 PASS** (10 themes ≥ 5 agencies each; 9 themes ≥ 30 agencies)  
**G2 PASS** (top-5 share range 0.125–0.184, all well below 0.80 kill threshold)  
**G3 FAIL — kill gate fired** (Spearman ρ = -0.1000, p = 0.7699; correlation near-zero, opposite to hypothesis direction)  
**G4 PASS** (newcomer fractions all ≥ 0.94, far exceeding 0.30 threshold)

## Interpretation

The accessibility pattern's entry test has now failed in **four** market domains:

| Experiment | Domain | ρ | p-value | G3 Result |
|------------|--------|---|---------|-----------|
| E208 | NIH SBIR categories | -0.246 | 0.975 | FAIL |
| E209 | Federal IT PSC codes | +0.667 | 0.135 | FAIL (n=5) |
| E215 | International Trade HS codes | -0.123 | 0.623 | FAIL |
| **E219** | **World Bank themes** | **-0.100** | **0.770** | **FAIL** |
| E218 | OpenAlex Research Topics | +0.604 | <0.0001 | PASS (qualified) |

All four market domains show **no statistically significant positive correlation** between fragmentation and entrant fraction. The "fragmented ⇒ enterable" inference is not statistically validated in any tested market population.

In World Bank themes, **entry is nearly universal** (94.5%–98.6% newcomer fractions across all themes) regardless of concentration level. The prior window (2015–2019) captures only 12–73 agencies per theme vs 45–281 in the current window (2020–2024), suggesting either massive turnover, naming inconsistency, or that the implementing-agency field is not a stable identity marker across time.

**No product candidate emerges.** The accessibility pattern as a market-entry predictor closes across market domains.

## Artifacts
- `EXPERIMENTS/E219-wb-theme-entrant-share/run_e219.py` — protocol & analysis script
- `EXPERIMENTS/E219-wb-theme-entrant-share/raw_current.json` — 1,900 current-window projects
- `EXPERIMENTS/E219-wb-theme-entrant-share/raw_prior.json` — 1,100 prior-window projects
- `EXPERIMENTS/E219-wb-theme-entrant-share/results.json` — parsed results

**Named next action:** The accessibility pattern's entry test has now been run in five domains (four market, one academic). Four kill gates fired. Per D083, continue fresh observation in another completely new domain axis, or pivot to the prototype tool for enterable IT sub-segments (DA01, DA10, 7A21) identified in E209, or refine within FDA recall domain (E217: Class I recall → product discontinuation via NDC linkage).