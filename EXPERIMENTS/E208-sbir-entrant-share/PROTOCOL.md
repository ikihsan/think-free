<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-21
-->

# E208 protocol: does category fragmentation predict newcomer entry in NIH SBIR?

**Date:** 2026-10-21. **Author:** opencode session 2026-10-21-002.

## The concrete difficulty this tests

`STATE.md` calls NIH SBIR spending category 101 "the most fragmented market
measured in this repository" (147 grants, 134 distinct organizations, top-5
share 11.6%; E204, replicated to the dollar by E207), and reads the pattern as
**"a genuine market at the scale a small program operates at"** (E198's words
for the federal IT codes, same logic). Between "the vendor landscape is
fragmented" and "a small program can actually enter" sits one step nobody has
measured anywhere in this record: **do the winners actually include newcomers?**

A fragmented landscape is equally consistent with three stories:

1. newcomers keep entering (the reading the record assumes);
2. the same mid-size pool of incumbents rotates, and no organization is new;
3. the category is fragmented *because* it is marginal — grants too small or too
   risky for anyone to repeat.

No experiment in this repository has ever computed an entrant rate
(`grep -rli "first-time|new entrant|newcomer" EXPERIMENTS/*/RESULT.md` → none,
2026-10-21). So the accessibility screen measures concentration and stops
exactly where the practical question starts.

## Question (predeclared)

**Across NIH SBIR (R41/R42) spending categories, is a category's fragmentation
(1 − top-5 award-amount share) associated with the fraction of its FY2023
awardees that are newcomers to that segment — organizations with no R41/R42
award in the same category in FY2018–FY2022?**

Secondary, also predeclared: is category 101's newcomer fraction at least 0.30,
and how do newcomers split between *segment* newcomers (no prior award in this
category) and *domain* newcomers (no prior R41/R42 award in any category)?

## Exposure and population, read before this protocol was written

The exposure (concentration) comes from E207's committed census
(`E207-sbir-category101-census/summary.json`), never from the fetch this
protocol declares: **64 categories carry ≥ 10 distinct FY2023 organizations**,
their `top5_share` spans **0.116–0.719** (17 categories ≤ 0.30, 11 ≥ 0.60).
Those 64 categories are the analysis population. The outcome (who is new) is
computed nowhere in the repo and is not known to this session.

## Instrument

- `fetch_prior.py` — fetches every FY2018–FY2023 project with
  `activity_codes:['R41','R42']` from `api.reporter.nih.gov`
  `/v2/projects/search`, stopped by the API's own `meta.total` per year (no row
  cap, no sampling, no seed: no random component). Rows written verbatim to
  `raw/prior_years.json`.
- `analyze.py` — reads only `raw/prior_years.json`; writes `results.json` and
  `per_category.csv`. Organization identity is
  `organization.external_org_id` (present on 368/368 FY2023 rows in E207's
  committed census; `org_ipf_code` is the declared fallback). A grant belongs to
  every category in its `spending_categories` list.

Definitions, fixed here:

- **FY2023 org of category C** = distinct `external_org_id` holding an R41/R42
  FY2023 award whose `spending_categories` contains C.
- **Segment newcomer** = an FY2023 org of C with no R41/R42 award in FY2018–FY2022
  whose `spending_categories` contains C.
- **Domain newcomer** = an FY2023 org of C with no R41/R42 award of any kind in
  FY2018–FY2022.
- **Entrant fraction** of C = segment newcomers ÷ FY2023 orgs of C.
- **Fragmentation** of C = 1 − top-5 award-amount share, recomputed from the new
  FY2023 fetch (not copied from E207).

## Gates (declared before any prior-year fetch)

- **G0 — the instrument reproduces the known census.** The new FY2023 fetch
  returns 368 rows; category 101 has 147 grants (±10%: 132–162) over 134
  distinct organizations (±10%: 121–147) and a top-5 share within ±5
  percentage points of 0.1159. A failure here means the fetch code is wrong or
  the API moved; **no conclusion about entry is drawn either way.**
- **G1 — identity is computable.** ≥ 99% of FY2023 rows and ≥ 99% of FY2018–FY2022
  rows in the analysis population carry `external_org_id` (or `org_ipf_code`).
  Below that, org-name fallback would decide the outcome by string handling, so
  the measurement stops.
- **G2 — the prior window is complete.** For each of FY2018, 2019, 2020, 2021,
  2022 the fetched row count equals that year's API-reported `meta.total` for
  R41/R42. Any year short of its total = incomplete denominator, declared, and
  the entrant fractions of categories touched by the gap are withheld.
- **G3 — the headline association (kill gate).** Over the 64 analysis
  categories, Spearman ρ between fragmentation and entrant fraction is
  **≥ +0.40** *and* an exact-label permutation test (10,000 permutations,
  seed 20261021) gives **p < 0.05**. ρ < 0.40 or p ≥ 0.05 **fires the kill
  gate**: on this population fragmentation does not predict newcomer entry, and
  the accessibility pattern's practical reading ("a small program can enter")
  is recorded as an unsupported inference, not a finding.
- **G4 — the headline category.** Category 101's segment-entrant fraction is
  **≥ 0.30**. Below that, "most fragmented" does not mean "recently enterable"
  even where fragmentation is highest. (0.30 is a pragmatic bar chosen here, not
  a derived threshold; it is stated as such wherever the number is reported.)

## What each outcome decides

- **G3 and G4 pass:** the accessibility pattern gains its first direct evidence
  on the entry step, for this population and window. Still not a product, not
  adoption, not a claim about any other domain.
- **G3 fails (or G4 fails):** the screen measures concentration, not entry; the
  "small program can build and sell" reading is an inference this record has
  not earned. Recorded as a finding with the per-category table, not buried.
- **G0–G2 fail:** instrument defect; the defect is declared and the session
  ends with no conclusion.

## Known biases, declared in advance

- **Newcomers are over-counted if an organization changed its registered name**
  while keeping its `external_org_id`… which the identity key prevents; the
  residual risk is an organization receiving a *new* `external_org_id` (a
  reincorporated firm counts as new — the same thing a buyer would see). A
  name-based sensitivity (normalized `org_name`) is reported beside the
  primary, never substituted for it.
- **A five-year window** can miss a returning incumbent whose last award predates
  FY2018; that counts as new. A nine-year window (FY2014–FY2022) is the declared
  sensitivity analysis and is run whenever the primary runs.
- **Award amount is not an outcome here**, and nothing in this protocol asks
  whether the grants are worth winning.

## Bound

One population (NIH RePORTER R41/R42, FY2018–FY2023), one exposure, one
outcome, one analysis, one declared sensitivity. No re-run on unchanged
parameters, no product claim, no adoption claim, and no extension to the
federal IT codes (their data has no org-stable identity key in this record).
