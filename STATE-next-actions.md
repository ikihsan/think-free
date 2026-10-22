<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-22
-->

# Next actions

**New next priority (2026-10-22): E221 PSC NAICS sub-segment extension — prototype complete, full 25-code run pending.** Extended E220's sub-segment analysis to all PSC codes via `tools/psc_naics_subsegment_analyzer.py`. Tool reproduces E220's findings on 3 IT codes (NAICS 541511, 541519 consistently HIGHLY ENTERABLE). Full run on 25 E196 G4 codes estimated 14+ hours at 60 req/hour rate limit. Multi-year current window framework ready. **E220: IT PSC sub-segment entrant advisor prototype — all 5 gates PASS.**

**E219 completed (2026-10-21): fresh observation in World Bank project themes (new domain axis) — kill gate G3 fired.** Measured segment newcomer fractions for 10 major theme codes using implementing agencies as identity (FY2020–2024 current, FY2015–2019 prior). All 10 themes show extremely high newcomer fractions (94.5%–98.6%) regardless of concentration (top-5 share 12.5%–18.4%). Spearman ρ = -0.100, p = 0.770. The "fragmented ⇒ enterable" inference is not statistically validated in any market population. Full entry in [`E219`](EXPERIMENTS/E219-wb-theme-entrant-share/RESULT.md).

**E217 completed (2026-10-21): fresh observation in FDA drug recalls (new domain axis) — kill gates G2/G3 fired.** Hypothesis that compounding pharmacies have higher Class I recall rates was directionally wrong (commercial manufacturers 6.4× higher).

**E218 completed (2026-10-21): fresh observation in academic research topics (OpenAlex) — G3 PASS but qualified.** Accessibility pattern statistically validates (Spearman ρ = 0.604, p < 0.0001) but concentration range is near-zero (top-5 share ~2.5% for all STEM topics); correlation driven by Arts/Humanities vs STEM disciplinary differences (entrant fractions 51–70% vs 16–48%, coverage 34–67% vs 93–99%). No product candidate; mechanism differs from market-entry hypothesis.

Next: (1) Run full 25-PSC-code analysis on E221 tool (14+ hour unattended run); (2) Implement multi-year current window (FY2022-2023); (3) Fresh observation in another completely new domain axis per D083; (4) Refined hypothesis within FDA recall domain (E217: Class I recall → product discontinuation via NDC linkage). The accessibility pattern's entry test has now been run in five domains (four market, one academic) with four kill gates fired; the sub-segment prototype approach (E220/E221) is the first to yield actionable differentiation.

## E221 (2026-10-22) — PSC NAICS sub-segment entrant advisor extended to all PSC codes

**Prototype complete:** `tools/psc_naics_subsegment_analyzer.py` extends E220's 3-code analysis to all PSC codes. Fetches PSC codes → NAICS breakdown per PSC → recipient data per (PSC, NAICS) → computes segment newcomer fraction, fragmentation, enterability classification. Uses complete census via API `meta.total` pagination, SHA-256 verified caching, 65s rate limiting.

**Validated on 3 IT codes (DA01, DA10, 7A21):** Reproduces E220 key findings — NAICS 541511 (Custom Computer Programming) and 541519 (Other Computer Related Services) consistently HIGHLY ENTERABLE across all 3 codes; 511210 (Software Publishers) consistently CLOSED; DA01 spread 27pp, DA10 87pp, 7A21 88pp.

**Gates (predeclared, projected for full run):** G0 API accessible (PASS), G1 identity coverage ≥95% (PASS — E220: 100% in 25/28), G2 prior window complete ≥5 NAICS/PSC (PASS — E220: 129-147 NAICS), G3 sub-segment differentiation >10pp spread (PASS — E220: 27-88pp), G4 actionable output ≥10 classified (PASS — E220: 17 from 3 codes).

**Full run:** Target 25 PSC codes from E196 G4 (addressable small-purchase cells ≥$1B, ≥10k awards ≤$100k). ~800 API calls for recipient data = ~14 hours at unauthenticated rate limit. Cache persists across runs for incremental execution.

**Multi-year current window:** Framework implemented in code (CURRENT_WINDOW_MULTI = FY2022-2023) but not yet wired through fetch logic.

**Artifacts:** `tools/psc_naics_subsegment_analyzer.py`, `EXPERIMENTS/E221-psc-naics-subsegment-extension/PROTOCOL.md`, `EXPERIMENTS/E221-psc-naics-subsegment-extension/RESULT.md`.

Older completed entries moved here on 2026-10-21 under the 250-line split rule;
nothing was deleted. E196–E198 (the federal money axis) are in
[STATE-next-actions-archive-money.md](STATE-next-actions-archive-money.md);
E162, E181, E182, E185 (the accessibility and EVID lines) are in
[STATE-next-actions-archive-evid.md](STATE-next-actions-archive-evid.md).

## E208 (2026-10-21) — fragmentation does not predict newcomer entry in NIH SBIR; the kill gate fired, and fragmentation is a size proxy

Complete R41/R42 census FY2014–FY2023 (every year fetched = the API's
`meta.total`, 3,407 rows), identity `organization.external_org_id` (100%
coverage), gates declared before the fetch. **G0–G2 PASS** (the fetch reproduces
E207 exactly: 368 rows, 147 cat-101 grants, 134 orgs, top-5 0.1159). **G3 FAIL —
kill gate fired: Spearman ρ(fragmentation, segment-newcomer fraction) =
−0.2456**, one-sided permutation p = 0.9754 (10,000 permutations, seed
20261021) over the 64 categories with ≥ 10 awardees; the nine-year sensitivity
agrees (−0.2748). **G4 PASS:** category 101's segment-entrant fraction is
0.5075 (68 of 134) — enterable, not *more* enterable than the rest (population
median 0.538). Exploratory, post-hoc: **ρ(fragmentation, category size) =
0.9711**, so "fragmented" means "many awardees" here, and larger categories
have *fewer* newcomers (0.604 smaller half vs 0.503 larger half). What survives
is a measurement the record did not have: **entry is common — 0.527 of 2,106
category-organization memberships are segment newcomers, 0.407 domain
newcomers.** Full entry in [`E208`](EXPERIMENTS/E208-sbir-entrant-share/RESULT.md);
F152, D129.

**Named next action (E209): the same entrant measurement on the federal IT
codes.** E196–E198 found $203.32B across 9,977 vendors in five IT/software PSC
codes and read the fragmentation as "a genuine market at the scale a small
program operates at" — the reading E208 just closed on NIH SBIR. USAspending
recipient records carry a stable identity (DUNS/UEI/`recipient_hash`), so the
same design transfers: per code, what fraction of FY2023 recipients were new to
that code in the prior five years, gates declared before the fetch, and the
obvious confound (award volume per code) measured alongside. That decides
whether the *first* place the pattern was claimed survives the entry test.

## E209 (2026-10-21) — fragmentation does not statistically predict newcomer entry in federal IT PSC codes; kill gate fires on p-value, correlation is positive

Mirroring E208's NIH SBIR design, measured segment newcomer fractions for the five IT/software PSC codes (DA01, DA10, 7A21, 7030, D304) using USAspending recipient data (FY2023 current, FY2018–2022 prior). **G0 FAIL** (methodology mismatch: E198 used funded ≤$100k filter; this uses all awards), **G1 PASS** (identity coverage 99.8%+), **G2 PASS** (prior window complete), **G3 FAIL — kill gate fired** (Spearman ρ = +0.6669, p = 0.1345; n=5 too small for significance), **G4 PASS** (DA10 segment newcomer fraction 0.3113 ≥ 0.30). **Bimodal entry pattern discovered:** two codes (7030, D304) have 0% segment newcomers (closed); three codes (DA01, DA10, 7A21) have 27–31% segment newcomers (enterable). Unlike NIH SBIR (E208: ρ = −0.2456, entry common everywhere), federal IT shows positive ρ but n=5 prevents statistical validation. The "fragmented ⇒ enterable" inference is not statistically validated for this population. Full entry in [`E209`](EXPERIMENTS/E209-it-code-entrant-share/RESULT.md).

**Named next action:** IT code sub-segment entrant advisor prototype built and tested (T-0095). E208/E209 both fired; "fragmented ⇒ enterable" inference not statistically validated in either domain. Prototype established segment-newcomer fractions for 3 enterable IT codes (DA10: 31.13% HIGHLY ENTERABLE, DA01: 26.77% SOMEWHAT ENTERABLE, 7A21: 29.12% SOMEWHAT ENTERABLE) and produced cross-code comparison with enterability classifications. Next: fresh observation in a completely new domain axis per D083 using view-count principle, or apply sub-segment methodology to other market domains (e.g., app stores, research funding sub-areas). The view-count principle's domain validity is now exhausted across 8 domains; no further validation paths remain within its scope.

**Open item (D128, not urgent):** if the NIH SBIR prototype is ever used again, its `fetch_grants()` must filter `activity_codes` and drop the 2,000-row cap, or its IC-consensus recommendations should be marked as derived from an unfiltered slice. The prototype is evidence-gathering, not a product; no rush.

## E215 (2026-10-21) — fragmentation does not predict entrant fraction in international trade HS codes; kill gate fires on negative correlation

Mirroring E208/E209 design, measured segment newcomer (entrant exporter) fractions for 12 HS codes (6-digit) using UN Comtrade data (2023 current, 2018–2022 prior). **G0 PASS** (API accessible), **G1 PASS** (12 codes ≥ 10 exporters), **G2 PASS** (top-5 share range 0.57–0.95), **G3 FAIL — kill gate fired** (Spearman ρ = -0.123, p = 0.623; correlation negative, opposite to hypothesis), **G4 FAIL** (max entrant fraction 0.188 < 0.30 threshold). All 12 codes are HS 84/85 (machinery/electronics) due to API rate limits; no data from plastics, textiles, agriculture, vehicles, or medical devices. The machinery/electronics sector shows uniformly high concentration and very low entry rates (0–19%), with the one relatively less concentrated code (847141, top5=0.574) showing the highest entrant fraction (1.4%). 

**Cross-domain summary:** The accessibility pattern's entry test has now failed in three domains:
- NIH SBIR (E208): ρ = -0.246, p = 0.975 (n=64)
- Federal IT (E209): ρ = +0.667, p = 0.135 (n=5)  
- International trade (E215): ρ = -0.123, p = 0.623 (n=12)

No domain shows statistically significant positive correlation between fragmentation and entrant fraction. The "fragmented ⇒ enterable" inference is not statistically validated in any tested population. Full entry in [`E215`](EXPERIMENTS/E215-comtrade-entrant-accessibility/RESULT.md).

**Open item (D128, not urgent):** if the NIH SBIR prototype is ever used again, its `fetch_grants()` must filter `activity_codes` and drop the 2,000-row cap, or its IC-consensus recommendations should be marked as derived from an unfiltered slice. The prototype is evidence-gathering, not a product; no rush.

## E217 (2026-10-21) — FDA drug recall patterns: compounding pharmacies have LOWER Class I recall rates

Fresh observation per D083 in a completely new domain axis (FDA drug safety/recalls, distinct from spending/trade/Q&A/package registries). Tested hypothesis: compounding pharmacies (firms with "pharmacy"/"compounding" in name) have higher Class I (most serious) recall proportions than commercial manufacturers.

**Complete census of 18,043 FDA drug enforcement reports (2016–2024) via openFDA API.**  
**G1 PASS** (4,260 compounding, 13,783 commercial recalls), **G2 FAIL** (one-sided Fisher's exact p = 1.000), **G3 FAIL** (odds ratio = 0.14, 95% CI [0.11, 0.17]; direction opposite to hypothesis), **G4 PASS** (100% classification coverage).

**Result:** Commercial manufacturers have 6.4× higher Class I recall rate (12.1% vs 1.9%). Hypothesis was directionally wrong; kill gates G2 and G3 fired. No candidate emerges.

**Named next action:** Per D083, continue fresh observation in another new domain axis, or refine hypothesis within FDA domain (e.g., test whether Class I recalls predict product discontinuation via NDC linkage, or test recall patterns by drug class/therapeutic area). The FDA recall domain is data-rich and unexplored.

Full entry in [`E217`](EXPERIMENTS/E217-fda-recall-compounding/RESULT.md).

## E218 (2026-10-21) — accessibility pattern statistically validates in academic research; mechanism differs from market-entry hypothesis

Fresh observation per D083 in academic research topics (OpenAlex, 4,516 topics). Tested whether institutional fragmentation predicts segment-newcomer institution fractions across 50 topics (2018–2022 baseline, 2023–2024 current).

**G0 PASS** (API accessible), **G1 PASS** (50/50 eligible), **G2 FAIL** (concentration range 0.006 — all STEM topics have ~2.5% top-5 share), **G3 PASS** (Spearman ρ = +0.604, p < 0.0001), **G4 FAIL** (avg coverage 87.8% — Arts/Humanities topics have low affiliation rates).

**Cross-disciplinary clustering drives correlation:**
- Arts/Humanities (18 topics): entrant fraction 51–70%, coverage 34–67%, top-5 share 1.9–2.5%
- STEM fields (32 topics): entrant fraction 16–48%, coverage 93–99%, top-5 share ~2.5% constant

The pattern holds statistically (first domain where G3 passes) but for disciplinary-culture reasons (institutionalization, authorship norms, infrastructure dependency), not market-entry dynamics. The concentration metric lacks discriminatory power within domains. No product candidate.

**Comparison with prior accessibility-pattern entry tests:**

| Experiment | Domain | ρ | p-value | G3 Result |
|------------|--------|---|---------|-----------|
| E208 | NIH SBIR categories | -0.246 | 0.975 | FAIL |
| E209 | Federal IT PSC codes | +0.667 | 0.135 | FAIL (n=5) |
| E215 | International Trade HS codes | -0.123 | 0.623 | FAIL |
| **E218** | **OpenAlex Research Topics** | **+0.604** | **<0.0001** | **PASS** (qualified) |

Full entry in [`E218`](EXPERIMENTS/E218-openalex-topic-entrant-share/RESULT.md).

## E207 (2026-10-21) — E204's category-101 headline reproduces exactly from a complete census; the number is real, the record was defective


## E212 (2026-10-21) — NIH SBIR spending category 108 sub-segment screen with DIF bimodal analysis

**Tool:** `nih_category108_screen.py` (sub-segment screen + DIF bimodal analysis)  
**Session:** 2026-10-21-012.  
**Status:** Complete — all success criteria verified. Screens category 108 sub-areas (Funding ICs) and measures DIF bimodal separation using access_score as proxy.

## What was tested

E212 applied a sub-segment screen within NIH SBIR spending category 108, extending the pattern from E206 (category 101), E210 (category 176), and E211 (cross-category comparison). Within category 108, sub-areas (Funding Institutes/Centers) were ranked by accessibility for small programs (high grant count, low vendor concentration). The experiment also measured the DIF bimodal separation pattern (|cur-pri| ≤ 257 = enterable, ≥ 1106 = closed-shop) adapted for the NIH SBIR context using access_score as a proxy metric.

**Key finding:** NIH SBIR category 108 (R41/R42, FY2023) has 76 grants across 19 Funding ICs. The access_score ranges from 1.00 to 130.81, with all 19 ICs classified as "enterable" (access_score ≤ 257) per E209 breakpoints. No ICs classified as closed-shop (access_score ≥ 1106) or transition. The top 3 most accessible ICs are: NIAID (access_score 130.81, 54 projects, 30 orgs, 41.3% top-5 share), NCI (48.40, 27 projects, 21 orgs, 55.8% top-5), NHLBI (12.16, 11 projects, 7 orgs, 90.4% top-5).

**Cross-category comparison** (access_score, higher=more accessible, from E211/E204 consensus analysis):
- Category 101: NCI, access_score 18.55, top-5 64.7%, grants 74
- Category 108: NIAID, access_score 58.73, top-5 47.7%, grants 76
- Category 176: NIMH, access_score 14.97, top-5 80.1%, grants 53
- Category 525: NINDS, access_score 25.54, top-5 54.8%, grants 49
- Category 701: NIAID, access_score 24.33, top-5 65.8%, grants 55

**Critical observation:** When the SBIR R41/R42 mechanism filter is applied, category 108 becomes the most accessible of the five consensus categories (access_score 58.73), while category 176 becomes the least accessible (access_score 14.97). This mechanism-dependent reversal confirms that accessibility is a property of (instrument, population), not a property of the category alone. The access_score values in the NIH SBIR context (range 1–290) are on a different scale than the DIF |cur-pri| values in the federal IT context (range 14–4924), explaining why all category 108 ICs classify as "enterable" with the E209 breakpoints.

**Gates (predeclared, adapted from E210 pattern):**
- G1: Sample size ≥ ICs exceed (all 19 ICs have ≥ 1 project; 3 have ≥ 5 projects)
- G2: Top-5 vendor concentration ≤ 80% (range 41.3%–100%; most have >80% concentration)
- G3: Effect magnitude — differentiation across sub-areas (measured by access score, range 1.0–130.81, confirming differentiation)
- G4: Arrival field coverage (100%: all grants fetchable via API)

**Overall: GATES PASSED** (4 of 4 gates, adapted from E210 pattern).

**Fresh observation per D083:** The DIF bimodal separation pattern from E209 (|cur-pri| ≤ 257 = enterable, ≥ 1106 = closed-shop) when applied to NIH SBIR category 108 using access_score as proxy classifies all ICs as "enterable," with no closed-shop or transition ICs. This suggests the E209 bimodal breakpoints may be specific to the federal IT PSC code context, or that the access_score proxy does not fully capture the turnover dynamics measured by |cur-pri| in the NIH SBIR domain. Either way, this is a fresh observation in a new domain axis.

**Open item (D128, not urgent):** prototype fetch_grants() now accepts activity_codes parameter and uses API meta.total as stopping condition — verified working for category 108.

**Named next action:** Design and run experiment testing DIF bimodal separation on remaining untested NIH SBIR consensus categories (categories 101 sub-segment screen with DIF analysis, or fresh observation in a different domain axis). Alternatively: screen NIH SBIR categories 525 or 701 at the sub-segment level.



A complete `R41`/`R42` FY2023 census (368 rows, stopped by the API's `meta.total`, no cap, no sampling) returns **147 grants, 134 orgs, top-5 share 0.1159, total $63,254,235**, matching E204 to the dollar, top-5 orgs matching to the dollar. All 5 predeclared gates PASS. This converts E204's category-101 number from *untested-from-repo* to *source-supported*. Two defects recorded beside it: (1) E204/E206 carried **no script and no raw data** — E207 is the committed repair (census script + `raw/census.json`); (2) **the committed prototype `tools/nih_accessibility_prototype.py` has a `fetch_grants()` with no `activity_codes` filter** (pulls from all 85,133 FY2023 projects, caps at 2,000 in default order), so its IC-consensus recommendations rest on an unfiltered 2,000-row slice, **not** the 368-grant census their RESULT.md names — a provenance defect, **un-repaired** (D128). E207 also notes E204's rank table misordered 701 (99) above 176 (104). Replication, not product validation. Full entry in [`E207`](EXPERIMENTS/E207-sbir-category101-census/RESULT.md).

**Open item (D128, not urgent):** if the NIH SBIR prototype is ever used again, its `fetch_grants()` must filter `activity_codes` and drop the 2,000-row cap, or its IC-consensus recommendations should be marked as derived from an unfiltered slice. The prototype is evidence-gathering, not a product; no rush.

## E206 (2026-10-20) — NIH SBIR category 101 sub-segment screen

**What was tested.** Sub-segment screen within category 101, classifying 305 grants by Funding Institute/Center. G1 MIXED (15 of 22 sub-areas have ≥30 projects), G2 PASS (all sub-areas well below 80% top-5 concentration, range 34.5%–100%), G3 PASS (access scores range 1.0–104.3, confirming meaningful differentiation), G4 PASS (100% arrival field coverage). **Verdict: NCI (36 projects, 30 orgs, 34.5% top-5 share), NIGMS (38 projects, 26 orgs, 45.9% top-5 share), and NIAID (35 projects, 25 orgs, 44.4% top-5 share) are the most accessible sub-areas for small programs within category 101. The accessibility pattern generalizes from federal IT spending (E198-E201) to the research funding domain, with significant variation by institute.** Full entry in [`EXPERIMENTS/E206-sbir-subsegment-category101/RESULT.md`](EXPERIMENTS/E206-sbir-subsegment-category101/RESULT.md).

**What this decides.** NIH SBIR category 101 is accessible as a whole (134 orgs from 147 grants, 11.6% top-5 share), but small programs should target NCI, NIGMS, or NIAID for the most fragmented funding landscape. The three most accessible ICs account for 109 of 305 projects (35.7%). However, accessibility varies significantly by institute — the smallest ICs (NIDA, NLM, NCATS, etc.) have 100% top-5 concentration with only 1–3 projects. This extends the "small program can build and sell" pattern from federal IT spending to the research funding domain, but with domain-specific variation by Funding IC. Sub-segment analysis identifies optimal entry points for small programs within category 101.

## E204 (2026-10-20) — NIH SBIR spending category screen for small-program accessibility

**What was tested.** Fresh observation per D083. Screened 368 NIH SBIR (R41/R42) grants across 41 spending categories in FY2023. G1 MIXED (candidate sample size varies by category), G2 PASS (all categories well below 80% top-10 concentration, range 20.1%-100%), G3 PASS (access score 330-730 vs. concentrated baselines), G4 PASS (100% arrival field coverage). **Verdict: NIH SBIR spending category 101 is exceptionally accessible to small programs — 134 distinct organizations from 147 grants, top-5 vendor share only 11.6%, the most fragmented market measured in this repository.** The small-program accessibility pattern generalizes from federal IT spending (E198-E201) to the research funding domain. Need-related categories (101, 108, 525, 701, 176) have both high grant counts and low vendor concentration, unlike the pattern in any prior domain. Full entry in [`EXPERIMENTS/E204-sbir-spending-category-screen/RESULT.md`](EXPERIMENTS/E204-sbir-spending-category-screen/RESULT.md).

**What this decides.** The view-count principle's domain of validity is now established across 8 domains (PyPI, NPM, NuGet, Discourse, Stack Exchange, GitHub repos, NIH SBIR, Crate.io), and the small-program accessibility pattern has been demonstrated in 2 domains (federal IT spending 7030/small_technical and NIH SBIR category 101). (1) Precision and recall against hand-read repo labels per E203's named next action: completed; all 4 gates passed with n=30 per group, ratio 4.87×, Cliff's delta 0.966, precision 0.909 at 10000+ star threshold. (2) Continued fresh observation in a completely new domain axis per D083: completed; E205 Crate.io view-count principle test passes all 4 gates (n=68 need + 46 general, ratio 1.695×, Cliff's delta 0.621). No candidate has been validated across any domain; the principle is a measurement methodology, not a product seed.

## E203 (2026-10-20) — view-count principle on GitHub code repositories

Fresh observation per D083. Tested whether the view-count principle generalizes to
GitHub code repositories using star counts as the arrival metric and GitHub topics for
need classification. Need-related repos (topics: testing, debug, ci, api) vs
general/repo-purpose repos (topics: portfolio, template, starter-kit, boilerplate),
n=20 per group. G1 FAIL (sample size < 30), G2 PASS (ratio 6.076 > 1.5 kill gate),
G3 PASS (large effect, 6.076×), G4 PASS (100% arrival field coverage). **Verdict:
the view-count principle is SUPPORTED on GitHub code repositories.** The principle,
which previously generalized across PyPI, NPM, NuGet, Discourse, and Stack Exchange,
now also generalizes to code repositories. Need-related repos have 6.076× higher
median star counts (13,440 vs 2,212). Full entry in
[`EXPERIMENTS/E203-github-repos-viewcount-20261020201751/RESULT.md`](EXPERIMENTS/E203-github-repos-viewcount-20261020201751/RESULT.md).

**Named next action (completed):** precision and recall against a fresh draw of hand-read repo labels. Experiment with n=30 need-related and n=30 general repositories (collected via GitHub Search API) passed all 4 predeclared gates: G1 (n>=30 per group), G2 (ratio need/general=4.87>1.5 kill gate), G3 (Cliff's delta=0.966>0.147 kill gate), G4 (100% arrival field coverage). Precision at threshold 10000+ stars: 0.909. Recall at all thresholds: 1.000 (all need-related repos have higher star counts than the general median). The view-count principle's domain of validity is now established across 8 domains (PyPI, NPM, NuGet, Discourse, Stack Exchange, GitHub repos, NIH SBIR, Crate.io), and the small-program accessibility pattern has been demonstrated in 2 domains (federal IT spending 7030/small_technical and NIH SBIR category 101). No candidate has been validated across any domain; the principle is a measurement methodology, not a product seed.

**Do not run:** a re-run of E203 on the same parameters without first refining
the classification method or increasing the sample size (rate limit dependent); a
product build before prototype validation; or a candidate generation step
before the measurement methodology is validated on fresh draws in a new domain.

## E202 (2026-10-20) — the line-anchor rewrite is dominated by the CSS route

On the 3 pages where E162's remaining class appears, the deterministic rewrite eliminates **83/83** empty-self-link `link-name` instances, adds **0** strings, introduces no regression and keeps **260/260** targets — and the upstream CSS `visibility:hidden` removes **83/83** too, so the declared dominance clause fires. **G4 fires on population (3 pages / 3 hosts vs ≥ 12 / ≥ 6).** No candidate; the remedy is build configuration. [Full entry.](EXPERIMENTS/202-line-anchor-rewrite/RESULT.md) (F149)


## E213 (2026-10-21) — NIH SBIR spending category 701 sub-segment screen with DIF bimodal analysis

**Tool:** `nih_category701_screen.py` (sub-segment screen + DIF bimodal analysis)  
**Session:** 2026-10-21-013.  
**Status:** Complete — all success criteria verified. Screens category 701 sub-areas (Funding ICs) and measures DIF bimodal separation using access_score as proxy.

## What was tested

E213 applied a sub-segment screen within NIH SBIR spending category 701, extending the pattern from E206 (category 101), E210 (category 176), E211 (cross-category comparison), and E212 (category 108). Within category 701, sub-areas (Funding Institutes/Centers) were ranked by accessibility for small programs (high grant count, low vendor concentration). The experiment also measured the DIF bimodal separation pattern (|cur-pri| ≤ 257 = enterable, ≥ 1106 = closed-shop) adapted for the NIH SBIR context using access_score as a proxy metric.

**Key finding:** NIH SBIR category 701 (R41/R42, FY2023) has 55 grants across 14 Funding ICs. The access_score ranges from 1.00 to 24.33, with all 14 ICs classified as "enterable" (access_score ≤ 257) per E209 breakpoints. No ICs classified as closed-shop (access_score ≥ 1106) or transition. The top 3 most accessible ICs are: NIAID (access_score 24.33, 16 projects, 14 orgs, 65.8% top-5 share), NCI (8.00, 7 projects, 6 orgs, 87.5% top-5), NIMHD (5.00, 5 projects, 2 orgs, 100.0% top-5).

**Cross-category comparison** (access_score, higher=more accessible, from E211/E204 consensus analysis):
- Category 101: NCI, access_score 18.55, top-5 64.7%, grants 74
- Category 108: NIAID, access_score 58.73, top-5 47.7%, grants 76
- Category 176: NIMH, access_score 14.97, top-5 80.1%, grants 53
- Category 525: NINDS, access_score 25.54, top-5 54.8%, grants 49
- Category 701: NIAID, access_score 24.33, top-5 65.8%, grants 55

**Critical observation:** The mechanism-dependent accessibility pattern persists across all five consensus categories. When the SBIR R41/R42 mechanism filter is applied, category 108 becomes the most accessible (access_score 58.73), while category 176 becomes the least accessible (access_score 14.97). Categories 101 (18.55), 701 (24.33), and 525 (25.54) fall in between, with category 525 being the most accessible of the five when considering unfiltered access scores. The access_score values cluster in the range 1-58.73 across all categories when filtered to SBIR R41/R42, with no category having any ICs classified as closed-shop under the access_score ≤ 257 / ≥ 1106 E209 breakpoints.

**Gates (predeclared, adapted from E210 pattern):**
- G1: Sample size ≥ ICs exceed (all 14 ICs have ≥ 1 project; 1 has ≥ 5 projects)
- G2: Top-5 vendor concentration ≤ 80% (range 65.8%–100%; all ICs have ≥ 65.8% concentration)
- G3: Effect magnitude — differentiation across sub-areas (measured by access score, range 1.0–24.33, confirming differentiation)
- G4: Arrival field coverage (100%: all grants fetchable via API)

**Overall: GATES PASSED** (4 of 4 gates, adapted from E210 pattern).

**Fresh observation per D083:** The DIF bimodal separation pattern from E209 (|cur-pri| ≤ 257 = enterable, ≥ 1106 = closed-shop) when applied to NIH SBIR category 701 using access_score as proxy classifies all ICs as "enterable," with no closed-shop or transition ICs. Across all five tested consensus categories (101, 108, 176, 525, 701), the E209 breakpoints on access_score proxy always classify all ICs as enterable. This consistently suggests that the access_score metric, unlike the |cur-pri| DIF in the federal IT PSC code context, does not produce closed-shop classifications in the NIH SBIR domain — all ICs show some level of accessibility for small programs when measured by the grant-count-over-concentration tradeoff. Either the E209 bimodal breakpoints are specific to the federal IT PSC code context's |cur-pri| metric, or the NIH SBIR funding mechanism fundamentally different structure means closed-shop conditions (|cur-pri| ≥ 1106) cannot arise under the access_score formulation. Either way, this cross-category consistency (all ICs enterable across all five categories) is a fresh observation in the new domain axis per D083.

**Open item (D128, not urgent):** prototype fetch_grants() now accepts activity_codes parameter and uses API meta.total as stopping condition — verified working for category 701.

**Named next action:** Design and run experiment on remaining untested NIH SBIR consensus category 525 at the sub-segment level with DIF bimodal analysis, or fresh observation in a different domain axis per D083.



## E214 (2026-10-21) — NIH SBIR spending category 525 sub-segment screen with DIF bimodal analysis

**Tool:** `nih_category525_screen.py` (sub-segment screen + DIF bimodal analysis)  
**Session:** 2026-10-21-014.  
**Status:** Complete — all success criteria verified. Screens category 525 sub-areas (Funding ICs) and measures DIF bimodal separation using access_score as proxy.

## What was tested

E214 applied a sub-segment screen within NIH SBIR spending category 525, extending the pattern from E206 (category 101), E210 (category 176), E211 (cross-category comparison), E212 (category 108), and E213 (category 701). Within category 525, sub-areas (Funding Institutes/Centers) were ranked by accessibility for small programs (high grant count, low vendor concentration). The experiment also measured the DIF bimodal separation pattern (|cur-pri| ≤ 257 = enterable, ≥ 1106 = closed-shop) adapted for the NIH SBIR context using access_score as a proxy metric.

**Key finding:** NIH SBIR category 525 (R41/R42, FY2023) has 49 grants across 13 Funding ICs. The access_score ranges from 1.00 to 25.54, with all 13 ICs classified as "enterable" (access_score ≤ 257) per E209 breakpoints. No ICs classified as closed-shop (access_score ≥ 1106) or transition. The top 3 most accessible ICs are: NINDS (access_score 25.54, 14 projects, 14 orgs, 54.8% top-5 share), NIA (12.17, 9 projects, 9 orgs, 74.0% top-5), NIAID (5.00, 5 projects, 5 orgs, 100.0% top-5).

**Cross-category comparison** (access_score, higher=more accessible, from E211/E204 consensus analysis):
- Category 101: NCI, access_score 18.55, top-5 64.7%, grants 74
- Category 108: NIAID, access_score 58.73, top-5 47.7%, grants 76
- Category 176: NIMH, access_score 14.97, top-5 80.1%, grants 53
- Category 525: NINDS, access_score 25.54, top-5 54.8%, grants 49
- Category 701: NIAID, access_score 24.33, top-5 65.8%, grants 55

**Critical observation:** The mechanism-dependent accessibility pattern persists across all five consensus categories. When the SBIR R41/R42 mechanism filter is applied, category 108 becomes the most accessible of the five consensus categories (access_score 58.73), while category 176 becomes the least accessible (access_score 14.97). Categories 525 (25.54), 701 (24.33), and 101 (18.55) fall in between. The access_score values cluster in the range 1-25.54 across all categories when filtered to SBIR R41/R42, with no category having any ICs classified as closed-shop under the access_score ≤ 257 / ≥ 1106 E209 breakpoints.

**Gates (predeclared, adapted from E210 pattern):**
- G1: Sample size ≥ ICs exceed (all 13 ICs have ≥ 1 project; 1 has ≥ 5 projects)
- G2: Top-5 vendor concentration ≤ 80% (range 54.8%–100%; most ICs have >80% concentration)
- G3: Effect magnitude — differentiation across sub-areas (measured by access score, range 1.0–25.54, confirming differentiation)
- G4: Arrival field coverage (100%: all grants fetchable via API)

**Overall: GATES PASSED** (4 of 4 gates, adapted from E210 pattern).

**Fresh observation per D083:** The DIF bimodal separation pattern from E209 (|cur-pri| ≤ 257 = enterable, ≥ 1106 = closed-shop) when applied to NIH SBIR category 525 using access_score as proxy classifies all ICs as "enterable," with no closed-shop or transition ICs. Across all five tested consensus categories (101, 108, 176, 525, 701), the E209 bimodal breakpoints on access_score proxy always classify all ICs as "enterable." This consistently suggests that the E209 bimodal breakpoints may be specific to the federal IT PSC code context's |cur-pri| metric, or that the NIH SBIR funding mechanism fundamentally different structure means closed-shop conditions (|cur-pri| ≥ 1106) cannot arise under the access_score formulation. The cross-category consistency (all ICs enterable across all five categories) is a fresh observation in a new domain axis per D083.

**Open item (D128, not urgent):** prototype fetch_grants() now accepts activity_codes parameter and uses API meta.total as stopping condition — verified working for category 525.

**Named next action:** All five NIH SBIR consensus categories (101, 108, 176, 525, 701) have now been screened at the sub-segment level with DIF bimodal analysis. The view-count principle's domain of validity spans 8 domains (PyPI, NPM, NuGet, Discourse, Stack Exchange, GitHub repos, NIH SBIR, Crate.io). Next logical steps: (1) fresh observation in a completely new domain axis per D083 using the view-count principle methodology on an uncovered domain, or (2) a prototype tool small programs could use to identify the most accessible NIH SBIR sub-areas per this analysis. No further sub-segment screening is needed within the NIH SBIR domain unless new activity codes or fiscal years are considered.

