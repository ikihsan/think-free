<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-21
-->

# E208 result: fragmentation does not predict newcomer entry in NIH SBIR — the kill gate fired, and entry turned out to be common everywhere

**Date:** 2026-10-21. **Session:** 2026-10-21-002.
Protocol written and recorded before any fetch: [`PROTOCOL.md`](PROTOCOL.md)
(declared at event seq 2; the fetch command is seq 5).

## What was tested

`STATE.md` reads NIH SBIR category 101's fragmentation (147 grants, 134 orgs,
top-5 share 11.6%, E204, replicated to the dollar by E207) as "a genuine market
at the scale a small program operates at". Between *fragmented* and *enterable*
sits one unmeasured step: **do the winners include newcomers?** No experiment in
this record had ever computed an entrant rate.

## Instrument and population

`fetch_prior.py` fetched every NIH RePORTER R41/R42 project for FY2014–FY2023,
each year stopped by the API's own `meta.total` (no cap, no sampling).
`analyze.py` computed, per spending category: top-5 award-amount share
(fragmentation = 1 − share), the share of FY2023 awardee organizations with **no
award in that category in FY2018–FY2022** (segment newcomer), and the share with
**no R41/R42 award of any kind** in that window (domain newcomer). Identity is
`organization.external_org_id`. Analysis population: the 64 categories with ≥ 10
distinct FY2023 organizations (exposure read from E207's committed census before
this protocol existed; the outcome is computed nowhere else in the repo).

| fiscal year | API reported | fetched |
|---|---|---|
| 2014 | 290 | 290 |
| 2015 | 284 | 284 |
| 2016 | 329 | 329 |
| 2017 | 321 | 321 |
| 2018 | 371 | 371 |
| 2019 | 356 | 356 |
| 2020 | 354 | 354 |
| 2021 | 356 | 356 |
| 2022 | 369 | 369 |
| 2023 | 368 | 368 |

## The result — G0–G2 and G4 pass, G3 fires the kill gate

| gate | declared | result | verdict |
|---|---|---|---|
| G0 reproduce E207 | FY2023 = 368 rows; cat 101 = 132–162 grants, 121–147 orgs, top-5 within 6.6%–16.6% | 368 rows; **147 grants, 134 orgs, top-5 0.1159** (identical by org id and by name) | **PASS** |
| G1 identity coverage | ≥ 99% of rows carry `external_org_id` | **100%** in FY2023 and in the prior window | **PASS** |
| G2 prior window complete | fetched = reported for each of FY2018–FY2022 | 5 of 5 years exact | **PASS** |
| G3 fragmentation → entry | Spearman ρ ≥ +0.40 **and** permutation p < 0.05 over 64 categories | **ρ = −0.2456**, one-sided p = **0.9754** (10,000 permutations, seed 20261021) | **FAIL — kill gate fired** |
| G4 category 101 | segment-entrant fraction ≥ 0.30 | **0.5075** (68 of 134) | **PASS** |

The declared sensitivity window (FY2014–FY2022, nine prior years) agrees in
sign: **ρ = −0.2748**. Entry is not missing because the window was short.

## What the numbers say

**Entry is common in every category, fragmented or not.** Across the 64
analysis categories, FY2023 holds **1,110 of 2,106 = 0.527** category-organization
memberships for segment newcomers, and **856 of 2,106 = 0.407** for domain
newcomers. The median category's segment-entrant fraction is **0.538**, the
range **0.308–1.0**, and three categories (5546, 5599, 5680) have **every**
FY2023 awardee new to the segment.

**Category 101, the "most fragmented market measured in this repository", is
unremarkable on entry: 0.5075 segment / 0.4627 domain, against a population
median of 0.538.** "Most fragmented" does not distinguish it where the
practical question is asked.

## Exploratory (post-hoc, not gated, labeled as such)

The negative ρ has a visible cause, and it is not about entry behaviour:

- **ρ(fragmentation, category size) = 0.9711** — in this population,
  "fragmented" is almost perfectly redundant with "many awardees". The
  accessibility screen's fragmentation axis measures *how many* organizations
  hold awards, not concentration independent of size.
- **ρ(category size, entrant fraction) = −0.2583**: the smaller half of the
  analysis categories has a **0.604** segment-newcomer rate, the larger half
  **0.503**. If anything, the small concentrated segments are *more* dominated
  by newcomers.

None of this was declared; it is reported because it explains the sign and
because it changes what the screen measures.

## What this decides

- **The accessibility pattern's practical reading is not supported for this
  population.** "Fragmented ⇒ a small program can enter" was an inference, and
  on NIH SBIR segments the association runs slightly the other way (G3 kill
  gate fired, both windows). This closes the *entry-by-fragmentation* claim for
  R41/R42 FY2014–FY2023 only — not the federal IT codes (untested here), not
  entry itself.
- **What survives is a measurement, and a correction.** NIH SBIR segments turn
  over fast regardless of concentration (0.527 segment / 0.407 domain), and the
  screen's "fragmentation" metric is a size proxy in this data (exploratory,
  ρ = 0.9711). A screen that reports fragmentation as an *entry* signal would be
  reporting size.
- **No product is proposed and no adoption is claimed.** E204/E207's
  concentration numbers stand; what falls is the inference drawn from them.

## Raw data and instrument

- [`fetch_prior.py`](fetch_prior.py), [`analyze.py`](analyze.py) — both
  committed, deterministic (the permutation test is seeded).
- [`raw/prior_years.json`](raw/prior_years.json) — every fetched row for
  FY2014–FY2023 (37.6 MB) with per-year `reported_total`, so G0–G2 recompute
  from the file alone.
- `gates.json`, `per_category.csv` — gates, per-category table, sensitivity.

## Bound

One population, one exposure, one outcome, one analysis, one declared
sensitivity, no re-run on unchanged parameters. The unit of the headline rate
is the *category-organization membership* (an organization holding awards in
three categories is counted three times); the 64 categories cover 303 distinct
FY2023 organizations. Org reincorporation under a new `external_org_id` counts
as new, as a buyer would see it.
