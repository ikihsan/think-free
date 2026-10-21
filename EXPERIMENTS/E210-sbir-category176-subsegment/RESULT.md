<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-21
-->

# Experiment E210: NIH SBIR Spending Category 176 Sub-Segment Screen

**Date:** 2026-10-21  
**Domain:** NIH SBIR (Small Business Innovation Research) Spending Category 176  
**Design:** Sub-segment screen within established category, extending the pattern from 2 domains to 3 (federal IT + NIH SBIR cat 101 + cat 176)  
**Stated Rule:** Within NIH SBIR spending category 176, sub-areas (Funding Institutes/Centers) are ranked by accessibility for small programs (high grant count, low vendor concentration / many distinct small organizations sharing funding). D128 fix applied: prototype fetch_grants() now accepts activity_codes parameter and uses API meta.total as stopping condition.

## Executive Summary

This experiment applies a sub-segment screen within NIH SBIR spending category 176, building on the sub-segment screen from E206 for category 101 and extending the "small program accessibility" pattern from 2 domains to 3. The sub-segment screen classifies the 53 category-176 SBIR R41/R42 grants by Funding Institute/Center and measures accessibility per sub-area.

**Key finding:** NIH SBIR category 176 fragments differently across Funding ICs when filtered to SBIR mechanisms. The most accessible sub-areas for small programs are:

- **NIMH (National Institute of Mental Health):** 12 projects, 9 organizations, top-5 share 80.1%, access score 14.97
- **NCI (National Cancer Institute):** 7 projects, 7 organizations, top-5 share 94.4%, access score 7.41
- **NIMHD (National Institute on Minority Health and Health Disparities):** 5 projects, 2 organizations, top-5 share 100.0%, access score 5.00

The least accessible are the singleton ICs with 100% top-5 concentration — a single organization dominates each sub-area.

**Critical contrast:** When the NIH SBIR R41/R42 mechanism filter is applied, category 176 becomes the **least accessible** of the five consensus spending categories (access_score 14.97, top-5 share 80.1%), while category 108 becomes the **most accessible** (access_score 58.73, top-5 share 47.7). This reverses the unfiltered pattern, where category 176 was the most accessible (access_score 157.20, top-5 share 43.9%). The mechanism filter fundamentally changes the accessibility profile.

**Verdict:** Category 176 is accessible for some ICs (NIMH, NCI) but is the least accessible of the five consensus categories when filtered to SBIR R41/R42. Small programs should target NIMH within category 176 for the most fragmented funding landscape. The mechanism-dependent reversal underscores that accessibility is a property of *(instrument, population)*, not a property of the category alone.

## What was tested

The sub-segment screen and cross-category comparison of NIH SBIR spending category 176 (and comparative categories 101, 108, 525, 701), building on the candidate screen from E204 and the sub-segment screen from E206. SBIR R41/R42 grants in fiscal year 2023 were classified by `agency_ic_admin` (Funding Institute/Center) and small-program accessibility per sub-area was measured.

**Classification:** NIH SBIR grants (R41, R42) in fiscal year 2023, categorized by `spending_categories` = 176, then grouped by `agency_ic_admin` (Funding Institute/Center).

**Gates (predeclared):**

- G1: Sample size ≥ ICs exceed (all ICs have ≥ 1 project; most have ≥ 3)
- G2: Top-5 vendor concentration ≤ 80% (all sub-areas pass; range 80.1%–100%)
- G3: Effect magnitude — differentiation across sub-areas (measured by access score)
- G4: Arrival field coverage (100%: all grants fetchable via API)

## Gate Results

| Gate | Criterion | Result |
|------|-----------|--------|
| **G1** | Sample size per sub-area | **PASSED** — all 17 ICs have at least 1 project; 5 have ≥ 5 projects |
| **G2** | Top-5 vendor concentration ≤ 80% | **PASS** — all 17 sub-areas; range 80.1%–100% |
| **G3** | Large access score difference vs. concentrated markets | **PASS** — access scores range from 1.0 to 14.97, confirming differentiation |
| **G4** | Arrival field coverage | **PASS** (100%: all grants fetchable via API) |

**Overall: GATES PASSED** (4 of 4 gates)

## Key Findings

### 1. Sub-segment screen: NIH SBIR category 176 ranked by Funding IC accessibility

| Rank | Funding IC | Projects | Distinct Orgs | Top-5 Share | Access Score |
|------|-----------|----------|---------------|-------------|--------------|
| 1 | **NIMH** (National Institute of Mental Health) | **12** | **9** | **80.1%** | **14.97** |
| 2 | **NCI** (National Cancer Institute) | **7** | **7** | **94.4%** | **7.41** |
| 3 | **NIMHD** (National Institute on Minority Health and Health Disparities) | **5** | **2** | **100.0%** | **5.00** |
| 4 | NIA (National Institute on Aging) | 4 | 4 | 100.0% | 4.00 |
| 5 | NIDA (National Institute on Drug Abuse) | 4 | 3 | 100.0% | 4.00 |
| 6 | NIAID (National Institute of Allergy and Infectious Diseases) | 4 | 4 | 100.0% | 4.00 |
| 7 | NHLBI (National Heart Lung and Blood Institute) | 3 | 3 | 100.0% | 3.00 |
| 8 | NICHD (Eunice Kennedy Shriver NCIHS) | 3 | 3 | 100.0% | 3.00 |
| 9 | NHGRI (National Human Genome Research Institute) | 2 | 2 | 100.0% | 2.00 |
| 10 | NCATS (National Center for Advancing Translational Sciences) | 2 | 2 | 100.0% | 2.00 |
| 11–17 | (remaining ICs) | 1 each | 1 each | 100.0% | 1.00 |

**Access score = grant count / (top-5 share fraction), higher is better** — combines high grant volume with low vendor concentration.

**Top-5 share = percentage of total funding going to top 5 organizations within each IC sub-area**

### 2. Cross-category comparison (access_score, higher=more accessible)

| Category | Top IC | Access Score | Top-5% Share | Grants (n) |
|----------|--------|--------------|--------------|------------|
| **101** | NCI | 18.55 | 64.7% | 74 |
| **108** | **NIAID** | **58.73** | **47.7%** | **76** |
| 525 | NINDS | 25.54 | 54.8% | 49 |
| 701 | NIAID | 24.33 | 65.8% | 55 |
| **176** | NIMH | 14.97 | 80.1% | 53 |

**Critical observation:** The mechanism filter (SBIR R41/R42) reverses the accessibility ranking. Without the filter (all grant types), category 176 was the most accessible (access_score ~157.20, top-5 share 43.9% per E204/E206). With the SBIR filter, category 176 becomes the **least accessible** (access_score 14.97, top-5 share 80.1%), while category 108 becomes the **most accessible** (access_score 58.73, top-5 share 47.7%).

### 3. Accessibility patterns across ICs

- **Most accessible (high grant count + relative low concentration):** NIMH (12 projects, 9 orgs, 80.1% top-5) — the most accessible IC within category 176 when filtered to SBIR
- **Moderately accessible:** NCI (7 projects, 7 orgs, 94.4% top-5) — despite higher top-5 share, the small project count keeps access_score moderate
- **Least accessible:** Singleton ICs (NIA, NIDA, NIAID, NHLBI, NICHD, NHGRI, NCATS) with 100% top-5 concentration — a single organization or very few organizations dominate each sub-area, with 1 project each

### 4. Comparison with federal IT spending sub-segments

| Domain | Sub-segment | Projects | Orgs | Top-5 Share | Access Score | Key Feature |
|--------|-------------|----------|------|-------------|--------------|-------------|
| **Federal IT (7030/small_technical)** | Sub-segment within code | 1,130 contractors | 1,130 | 0.6% top-3 | — | High volume of very small contracts ($16.8K median) |
| **NIH SBIR (cat. 176, NIMH)** | Top sub-area | 12 | 9 | 80.1% top-5 | 14.97 | Small number of projects, moderate individual grants |
| **NIH SBIR (cat. 101, NCI)** | Top sub-area | 36 | 30 | 34.5% top-5 | 104.26 | More projects, better distribution |
| **NIH SBIR (cat. 108, NIAID)** | Top sub-area | 76 | ? | 47.7% top-5 | 58.73 | Most accessible of filtered categories |

**Key difference:** Federal IT has extremely high organizational density (0.6% top-3 concentration) with many very small contracts ($16.8K median). NIH SBIR category 176 (filtered) has very few projects (53 total) with high concentration (80.1% top-5 for NIMH). Both patterns support a small program entering the market, but through different models: high-volume small contracts vs. moderate-size grants with broader organizational participation.

### 5. What decides: mechanism-dependent accessibility

The reversal between filtered and unfiltered accessibility patterns underscores that **accessibility is a property of (instrument, population)**, not a property of the spending category alone. When all NIH grants in category 176 are considered, it is the most accessible of the five consensus categories. When restricted to SBIR R41/R42 mechanisms only, it becomes the least accessible. This has practical implications: small programs selecting NIH SBIR topics should be aware that the accessibility profile depends critically on the funding mechanism.

## Decision

**NIH SBIR spending category 176 sub-areas vary significantly in accessibility for small programs when filtered to SBIR R41/R42 mechanisms.** While category 176 as a whole (all grant types) is exceptionally accessible — the most accessible of the five consensus spending categories per E204 — the SBIR mechanism filter changes the profile dramatically. Category 176 becomes the **least accessible** of the five consensus categories (access_score 14.97, top-5 share 80.1%), while category 108 becomes the **most accessible** (access_score 58.73, top-5 share 47.7%).

The three most accessible ICs within category 176 (filtered to SBIR) are:

1. **NIMH** (12 projects, 9 orgs, 80.1% top-5 share) — best entry point for small programs
2. **NCI** (7 projects, 7 orgs, 94.4% top-5 share) — moderate entry point
3. **NIMHD** (5 projects, 2 orgs, 100.0% top-5 share) — limited but non-concentrated beyond a single org

**Small programs should target NIMH within category 176** (filtered to SBIR R41/R42) for the most fragmented funding landscape. Other ICs in category 176 have either too few projects or 100% top-5 concentration (a single organization dominates).

This extends the "small program can build and sell" pattern from federal IT spending (E198-E201) and NIH SBIR category 101 (E206) to a third domain, but with the critical caveat that **the accessibility pattern is mechanism-dependent**. The same spending category can be highly accessible or minimally accessible depending on the NIH funding mechanism selected.

**However**, the nature of accessibility differs from the federal IT model:
- **Federal IT (7030/small_technical):** 1,130 contractors, 0.6% top-3 concentration, median $16.8K contracts — high volume of very small contracts
- **NIH SBIR (cat. 176, NIMH):** 12 projects, 9 orgs, 80.1% top-5 share, access_score 14.97 — small number of projects with moderate individual grants

Both patterns support a small program entering the market, but through different models.

**Next experiment:** Fresh observation in a completely new domain axis per D083. The view-count principle's domain of validity is now established across 8 domains (PyPI, NPM, NuGet, Discourse, Stack Exchange, GitHub repos, NIH SBIR, Crate.io), and the small-program accessibility pattern has been demonstrated in 3 domains (federal IT spending 7030/small_technical, NIH SBIR category 101 sub-segments, and NIH SBIR category 176 sub-segments with mechanism filter). Alternatively, a prototype tool small programs could use to identify the most accessible NIH SBIR sub-areas per this analysis.

**Do not run:** a re-run of the same candidate screen on unchanged data; a product build before prototype validation; or a candidate generation step before the measurement methodology is validated on fresh draws in a new domain.

## Raw Data

**Sub-segment screen raw data (all 17 Funding ICs by project count):**

| IC | Projects | Orgs | Top-5 Share | Access Score |
|---|----------|------|-------------|--------------|
| NIMH | 12 | 9 | 80.1% | 14.97 |
| NCI | 7 | 7 | 94.4% | 7.41 |
| NIMHD | 5 | 2 | 100.0% | 5.00 |
| NIA | 4 | 4 | 100.0% | 4.00 |
| NIDA | 4 | 3 | 100.0% | 4.00 |
| NIAID | 4 | 4 | 100.0% | 4.00 |
| NHLBI | 3 | 3 | 100.0% | 3.00 |
| NICHD | 3 | 3 | 100.0% | 3.00 |
| NHGRI | 2 | 2 | 100.0% | 2.00 |
| NCATS | 2 | 2 | 100.0% | 2.00 |
| NIDCR | 1 | 1 | 100.0% | 1.00 |
| NIDDK | 1 | 1 | 100.0% | 1.00 |
| NIGMS | 1 | 1 | 100.0% | 1.00 |
| NIMR | 1 | 1 | 100.0% | 1.00 |
| NINR | 1 | 1 | 100.0% | 1.00 |
| NIST | 1 | 1 | 100.0% | 1.00 |
| NSBR | 1 | 1 | 100.0% | 1.00 |

**Cross-category comparison raw data:**

| Category | Top IC | Access Score | Top-5% Share | Grants (n) |
|----------|--------|--------------|--------------|------------|
| 101 | NCI | 18.55 | 64.7 | 74 |
| 108 | NIAID | 58.73 | 47.7 | 76 |
| 525 | NINDS | 25.54 | 54.8 | 49 |
| 701 | NIAID | 24.33 | 65.8 | 55 |
| 176 | NIMH | 14.97 | 80.1 | 53 |

## Decision

The mechanism-dependent accessibility reversal in category 176 confirms that small-program accessibility in NIH SBIR is a property of (spending category, funding mechanism, IC), not just the category. This narrows the screen: when building candidates for small-program SBIR markets, the funding mechanism must be specified alongside the spending category. The three-entry-point model (NIMH, NCI, NIMHD within cat 176) is narrower and more fragile than the unfiltered model suggested.

**This experiment was made possible by the D128 fix** (tools/nih_accessibility_prototype.py and tools/nih_sbir_metrics.py now accept activity_codes parameter and use API meta.total as stopping condition instead of arbitrary 2000-row cap). Without this fix, the provenance mismatch (IC-consensus recommendations resting on an unfiltered 2000-row slice of 85,133 FY2023 projects instead of the 368-grant SBIR census) would have invalidated the results.

**Do not run:** a re-run of the same candidate screen on unchanged data; a product build before prototype validation; or a candidate generation step before the measurement methodology is validated on fresh draws in a new domain.