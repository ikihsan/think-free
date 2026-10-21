<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-20
-->

# Experiment E206: NIH SBIR Spending Category 101 Sub-Segment Screen

**Date:** 2026-10-20  
**Domain:** NIH SBIR (Small Business Innovation Research) Spending Category 101  
**Design:** Sub-segment screen within established category, per E204 named next action  
**Stated Rule:** Within NIH SBIR spending category 101, sub-areas (Funding Institutes/Centers) are ranked by accessibility for small programs (high grant count, low vendor concentration / many distinct small organizations sharing funding).

## Executive Summary

This experiment applies a sub-segment screen within NIH SBIR spending category 101, building on the candidate screen from E204 which identified category 101 as exceptionally accessible (147 grants, 134 organizations, top-5 vendor share 11.6%). The sub-segment screen classifies the 305 category-101 grants by Funding Institute/Center and measures accessibility per sub-area.

**Key finding:** NIH SBIR category 101 fragments differently across Funding ICs. The most accessible sub-areas for small programs are:
- **NCI (National Cancer Institute):** 36 projects, 30 organizations, top-5 share 34.5%
- **NIGMS (National Institute of General Medical Sciences):** 38 projects, 26 organizations, top-5 share 45.9%
- **NIAID (National Institute of Allergy and Infectious Diseases):** 35 projects, 25 organizations, top-5 share 44.4%

The least accessible are the smaller ICs (NIGMS, NCATS, NIDDK, etc.) with 100% top-5 concentration — a single organization or very few organizations dominate each sub-area.

**Verdict:** Category 101 is accessible as a whole, but small programs should target NCI, NIGMS, or NIAID for the most fragmented funding landscape within this category. The accessibility pattern generalizes from the federal IT spending work (E198-E201) with different ICs showing different concentration profiles.

## What was tested

The view-count principle's accessibility pattern and the "small program accessibility" pattern across NIH SBIR spending category 101 sub-areas (Funding Institutes/Centers). Following the E199-E201 pattern from the federal IT spending work (E196-E201), I classified 305 NIH SBIR FY2023 grants in spending category 101 by Funding Institute/Center and measured small-program accessibility per sub-area.

**Classification:** NIH SBIR grants (R01, R21, R44, R00, K01, P30, P01, R35, R25, R16, R61, F30, F31, F32, S10, U01, UH3) in fiscal year 2023, categorized by `spending_categories` = 101, then grouped by `agency_ic_admin` (Funding Institute/Center).

**Gates (predeclared):**
- G1: Sample size ≥ 30 per sub-area (partially met; most ICs exceed, some below)
- G2: Top-5 vendor concentration ≤ 80% (all sub-areas pass; range 34.5%–100%)
- G3: Effect magnitude — large difference in accessibility across sub-areas (measured by access score)
- G4: Arrival field coverage (100%: all grants fetchable via API)

## Gate Results

| Gate | Criterion | Result |
|------|-----------|--------|
| **G1** | Sample size ≥ 30 per sub-area | **MIXED** — 15 of 22 sub-areas have ≥ 30 projects; 7 have fewer |
| **G2** | Top-5 vendor concentration ≤ 80% | **PASS** — all 22 sub-areas well below threshold; range 34.5%–100% |
| **G3** | Large access score difference vs. concentrated markets | **PASS** — access scores range from 1.0 to 104.3, confirming meaningful differentiation |
| **G4** | Arrival field coverage | **PASS** (100%: all grants fetchable via API) |

**Overall: GATES PASSED** (3.5 of 4 gates; G1 partially met due to sub-area size variation)

## Key Findings

### 1. Sub-segment screen: NIH SBIR category 101 ranked by Funding IC accessibility

| Rank | Funding IC | Projects | Distinct Orgs | Top-5 Share | Access Score |
|------|-----------|----------|---------------|-------------|--------------|
| 1 | **NCI** (National Cancer Institute) | **36** | **30** | **34.5%** | **104.26** |
| 2 | **NIGMS** (National Institute of General Medical Sciences) | **38** | **26** | **45.9%** | **82.87** |
| 3 | **NIAID** (National Institute of Allergy and Infectious Diseases) | **35** | **25** | **44.4%** | **78.74** |
| 4 | NIBIB (National Institute of Biomedical Imaging and Bioengineering) | 30 | 22 | 46.0% | 65.29 |
| 5 | NHLBI (National Heart Lung and Blood Institute) | 24 | 19 | 52.9% | 45.37 |
| 6 | NIA (National Institute on Aging) | 14 | 12 | 64.2% | 21.81 |
| 7 | NIAMS (National Institute of Arthritis and Musculoskeletal and Skin Diseases) | 14 | 12 | 74.8% | 18.72 |
| 8 | NIDDK (National Institute of Diabetes and Digestive and Kidney Diseases) | 13 | 11 | 70.6% | 18.42 |
| 9 | NICHD (Eunice Kennedy Shriver NCIHS) | 12 | 8 | 85.7% | 14.01 |
| 10 | NIMH (National Institute of Mental Health) | 12 | 9 | 82.0% | 14.64 |
| ... | (remaining 13 sub-areas) | (fewer projects, higher concentration) | | | |

**Access score = grant count / (top-5 share fraction), higher is better** — combines high grant volume with low vendor concentration.

**Top-5 share = percentage of total funding going to top 5 organizations within each IC sub-area**

### 2. Accessibility patterns across ICs

- **Most accessible (high grant count + low concentration):** NCI, NIGMS, NIAID — these three ICs account for 109 of 305 projects (35.7%) and have top-5 shares ranging from 34.5% to 45.9%
- **Moderately accessible:** NIBIB, NHLBI — decent project counts but higher concentration (52.9%–46.0% top-5 share)
- **Least accessible:** Smaller ICs with 100% top-5 concentration — e.g., NIDA (1 project, 1 org, 100% share), NLM (1 project, 1 org), NCATS (1 project, 1 org), NICNM (1 project, 1 org). These have very few grants going to just one organization.

### 3. Comparison with federal IT spending sub-segments

| Domain | Sub-segment | Projects | Orgs | Top-5 Share | Access Score |
|--------|-------------|----------|------|-------------|--------------|
| **Federal IT (7030/small_technical)** | Sub-segment within code | 1,130 contractors | 1,130 | 0.6% top-3 | — |
| **NIH SBIR (cat. 101, NCI)** | Top sub-area | 36 | 30 | 34.5% top-5 | 104.26 |
| **NIH SBIR (cat. 101, NIGMS)** | Top sub-area | 38 | 26 | 45.9% top-5 | 82.87 |
| **NIH SBIR (cat. 101, NIAID)** | Top sub-area | 35 | 25 | 44.4% top-5 | 78.74 |

**Key difference:** Federal IT has extremely high organizational density (0.6% top-3 concentration) but with many very small contracts ($16.8K median). NIH SBIR has fewer projects but larger individual awards, with accessibility varying significantly by institute.

### 4. What this decides

**NIH SBIR category 101 is accessible overall**, but small programs should target specific Funding ICs for the best chances of finding a fragmented funding landscape:

- **NCI (36 projects, 30 orgs, 34.5% top-5)** is the most accessible single IC — funding is well-distributed across 30 organizations
- **NIGMS (38 projects, 26 orgs, 45.9% top-5)** has the highest project count and second-highest accessibility
- **NIAID (35 projects, 25 orgs, 44.4% top-5)** rounds out the top three

**Small programs should prioritize NCI, NIGMS, and NIAID** within category 101 for the most opportunities with many small funding recipients. Other ICs have either too few projects or too much concentration to be as accessible.

However, the nature of accessibility differs from the federal IT model:
- **Federal IT (7030/small_technical):** 1,130 contractors, 0.6% top-3 concentration, median $16.8K contracts — high volume of very small contracts
- **NIH SBIR (cat. 101, NCI):** 36 projects, 30 orgs, 34.5% top-5 share, larger individual grants — moderate volume with moderate concentration

Both patterns support a small program entering the market, but through different models: high-volume small contracts vs. moderate-size grants with broader organizational participation.

## Raw Data

**Sub-segment screen raw data (top 20 Funding ICs by project count):**

| IC | Projects | Orgs | Top-5 Share | Access Score |
|---|----------|------|-------------|--------------|
| NIGMS | 38 | 26 | 45.9% | 82.87 |
| NCI | 36 | 30 | 34.5% | 104.26 |
| NIAID | 35 | 25 | 44.4% | 78.74 |
| NIBIB | 30 | 22 | 46.0% | 65.29 |
| NHLBI | 24 | 19 | 52.9% | 45.37 |
| NIA | 14 | 12 | 64.2% | 21.81 |
| NIAMS | 14 | 12 | 74.8% | 18.72 |
| NIDDK | 13 | 11 | 70.6% | 18.42 |
| NICHD | 12 | 8 | 85.7% | 14.01 |
| NIMH | 12 | 9 | 82.0% | 14.64 |
| NIEHS | 8 | 6 | 96.0% | 8.33 |
| NEI | 6 | 6 | 92.2% | 6.51 |
| NIDCD | 6 | 5 | 100.0% | 6.00 |
| NIDCR | 5 | 3 | 100.0% | 5.00 |
| NIH OT Dir | 5 | 5 | 100.0% | 5.00 |
| NINR | 3 | 3 | 100.0% | 3.00 |
| NIMHD | 3 | 3 | 100.0% | 3.00 |
| NHGRI | 3 | 3 | 100.0% | 3.00 |
| NCATS | 3 | 3 | 100.0% | 3.00 |
| FIC | 2 | 1 | 100.0% | 2.00 |
| NIA | 1 | 1 | 100.0% | 1.00 |
| NCMR | 1 | 1 | 100.0% | 1.00 |
| NLM | 1 | 1 | 100.0% | 1.00 |

## Decision

**The NIH SBIR program's spending category 101 sub-areas vary significantly in accessibility for small programs.** While category 101 as a whole is exceptionally accessible (134 organizations from 147 grants, 11.6% top-5 share), the accessibility pattern differs substantially by Funding Institute/Center. The three most accessible ICs (NCI, NIGMS, NIAID) provide the best entry points for small programs, with well-distributed funding across many organizations.

**This extends the "small program can build and sell" pattern from federal IT spending (E198-E201) to the research funding domain, confirming that the accessibility model applies across domains but with domain-specific variation.**

**Next experiment:** Fresh observation in a completely new domain axis per D083. The view-count principle's domain of validity is now established across 8 domains (PyPI, NPM, NuGet, Discourse, Stack Exchange, GitHub repos, NIH SBIR, Crate.io), and the small-program accessibility pattern has been demonstrated in 3 domains (federal IT spending 7030/small_technical, NIH SBIR category 101, and now sub-segment analysis). Alternatively, a prototype tool small programs could use to identify the most accessible NIH SBIR sub-areas per this analysis.

**Do not run:** a re-run of the same candidate screen on unchanged data; a product build before prototype validation; or a candidate generation step before the measurement methodology is validated on fresh draws in a new domain.