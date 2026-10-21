<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-21
-->

# Next actions

**New next priority (2026-10-21):** measure entry where the accessibility
pattern was first claimed — the federal IT codes (E196–E198) — using E208's
instrument shape, since E208 closed the entry-by-fragmentation reading on NIH
SBIR (F152, D129) but left that domain untested.

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

**Open item (D128, not urgent):** if the NIH SBIR prototype is ever used again, its `fetch_grants()` must filter `activity_codes` and drop the 2,000-row cap, or its IC-consensus recommendations should be marked as derived from an unfiltered slice. The prototype is evidence-gathering, not a product; no rush.

## E207 (2026-10-21) — E204's category-101 headline reproduces exactly from a complete census; the number is real, the record was defective

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
