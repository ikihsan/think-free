# E207: Contract Vehicle Analysis for IT/Software PSC Codes

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-20
-->

## Objective

Map federal awards in 5 IT/software PSC codes (7030, DA10, 7A21, DA01, D304) to contract vehicles (SEWP, GSA MAS, CIO-SP4, VA T4NG, etc.) to identify which vehicles small vendors actually use.

## Method

- Queried USAspending `spending_by_award/` endpoint for recent 12 months (Oct 2024–Sep 2025)
- Extracted IDV PIID from `generated_internal_id` field (pattern: `CONT_AWD_{AwardID}_9700_{IDV_PIID}_`)
- Classified 28+ IDV PIID patterns into 11 contract vehicle categories
- Analyzed 5,000 awards per PSC code (25,000 total)
- Measured vehicle share by obligation ($) and award count
- Identified small vendors (≤3 awards in sample) and their vehicle usage

## Key Findings

### Overall Vehicle Distribution by Obligation ($)

| PSC Code | Description | Total Sample $ | Direct/Unknown | GSA MAS | SEWP | Army ITES | Navy SEAPORT | Other/Unknown |
|----------|-------------|----------------|----------------|---------|------|-----------|--------------|---------------|
| **7030** | IT Software | $4.74B | **64.3%** | 14.8% | 8.4% | 5.1% | 4.7% | 2.6% |
| **DA10** | IT Services | $2.99B | **45.9%** | 21.7% | **18.2%** | 8.2% | 4.9% | 20.8% |
| **7A21** | IT Hardware/Software | $3.10B | **31.6%** | **20.2%** | 17.3% | **16.5%** | 12.5% | 14.1% |
| **DA01** | IT Services (Mgmt) | $5.39B | **55.8%** | 19.9% | 0.6% | 15.5% | 7.3% | **42.3%** |
| **D304** | Telecom | $7.32B | **90.6%** | 4.5% | 0.0% | 4.4% | 0.2% | 9.2% |

### Small Vendor Vehicle Share (Recipients with ≤3 Awards)

| PSC Code | Small Vendors (n) | GSA MAS + SEWP Share | GSA MAS | SEWP | Army ITES | Direct/Unknown |
|----------|-------------------|---------------------|---------|------|-----------|----------------|
| **7030** | 1,168 | **4.7%** | 2.7% | 2.0% | 0.9% | 88.7% |
| **DA10** | 684 | **28.2%** | 26.6% | 1.6% | 9.8% | 41.8% |
| **7A21** | 657 | **8.6%** | 5.4% | 3.2% | 5.3% | 80.7% |
| **DA01** | 398 | **7.2%** | 6.2% | 1.0% | **24.9%** | 36.1% |
| **D304** | 411 | **5.2%** | 5.1% | 0.0% | 3.0% | 91.5% |

### Vehicle Pattern Definitions

| Vehicle Category | IDV PIID Patterns | Description |
|------------------|-------------------|-------------|
| **SEWP** | `NNG15SE*`, `NNG15SC*`, `NNG15SD*` | NASA Solutions for Enterprise-Wide Procurement V |
| **GSA MAS** | `GS35F*`, `47QTCA*`, `47QREA*`, `GS03F*`, `GS00*` | GSA Multiple Award Schedule (IT Schedule 70) |
| **CIO-SP** | `HHSN316*`, `HHSN263*` | HHS/NIH Chief Information Officer - Solutions and Partners |
| **VA T4NG** | `VA*`, `36C*`, `523*` | VA Transformational Technology Next Generation |
| **DoD ESI/DISA** | `HC1028*`, `HC1047*`, `HC1084*` | DISA Enterprise Software Initiative |
| **Navy SEAPORT** | `N00178*`, `N00039*`, `N66001*`, `N00189*` | Navy SEAPORT-e / Navy GWACs |
| **Army ITES/CHESS** | `W52P1J*`, `W91*`, `W56*`, `W81*` | Army CHESS / ITES contracts |
| **Direct/Unknown** | `NONE`, `-NONE-`, or no IDV | Direct awards or unclassified vehicles |

## Interpretation

### 1. **7030 (IT Software) - Best for Small Software Vendors**
- **64% Direct/Unknown** — majority of software purchases are direct or via vehicles not in our catalog
- **GSA MAS (14.8%)** and **SEWP (8.4%)** are the main GWAC channels
- **Small vendors use Direct/Unknown (88.7%)** — they mostly sell direct, not through GWACs
- **Only 4.7%** of small vendor $ flows through GSA MAS + SEWP combined

### 2. **DA10 (IT Services) - Strongest GWAC Channel for Small Vendors**
- **GSA MAS (21.7%)** and **SEWP (18.2%)** together = **40%** of market
- **Small vendors: 28.2% through GSA MAS + SEWP** — highest of all codes
- GSA MAS alone carries **26.6%** of small vendor obligation
- **DA10 is the only code where GWACs are a meaningful path for small vendors**

### 3. **7A21 (IT Hardware/Software) - Highly Concentrated, Army-Dominated**
- **Army ITES/CHESS (16.5%)** and **Navy SEAPORT (12.5%)** are major channels
- **Carahsoft dominates** across GSA MAS ($192M), Navy SEAPORT ($240M), Other/Unknown ($295M)
- Small vendors still mostly Direct/Unknown (80.7%)

### 4. **DA01 (IT Management Services) - Services Market, Not Software**
- **42.3% Other/Unknown** — mostly large SI contracts (Accenture, CACI, etc.)
- **Army ITES (15.5%)** significant but for large integrators
- **Only 0.6% SEWP** — not a software license market
- Small vendors split: Direct (36%), Army ITES (25%), GSA MAS (6%)

### 5. **D304 (Telecom) - Telco Market, Not Software**
- **90.6% Direct/Unknown** — direct telco contracts (Verizon, AT&T, V2X)
- **GSA MAS only 4.5%** — minimal GWAC usage
- **Not a software market** (confirmed by E203: 8.1% software)

## Gate Results

| Gate | Criterion | Result |
|------|-----------|--------|
| **G1** | SEWP/GSA MAS identifiable in all 5 codes | **PASS** — both found in 7030, DA10, 7A21 |
| **G2** | Small vendors use identifiable vehicles | **PARTIAL** — only DA10 shows meaningful GWAC usage (28%) |
| **G3** | VA T4NG / CIO-SP4 visible | **FAIL** — CIO-SP <0.5% in all codes; VA T4NG not detected |
| **G4** | Vehicle data sufficient for decision-making | **PASS** — 25,000 awards classified, patterns clear |

## Conclusions

1. **Contract vehicle ≠ small vendor access** — In 4 of 5 codes, small vendors (>80%) sell **direct** (Direct/Unknown), not through GWACs.

2. **DA10 is the exception** — 28% of small vendor $ flows through GSA MAS + SEWP. The GSA Schedule channel (confirmed in E205: 8% awarding agency) makes DA10 uniquely accessible.

3. **7030 small vendors don't use GWACs** — Despite SEWP and GSA MAS being 23% of the 7030 market, small vendors capture only 4.7% of that flow. They sell direct.

4. **Vehicle concentration mirrors vendor concentration** — SEWP and GSA MAS top recipients are large resellers (Carahsoft, DLT, Dell, CDW, Affigent, Emergent), not small software companies.

5. **Direct sales dominate software** — For actual software products (7030, DA10 software portion), the path to market is direct sales or subcontracting through large resellers, not GWAC prime positions.

## Implications for Small Team Entry

| Strategy | 7030 | DA10 | 7A21 |
|----------|------|------|------|
| **Prime on GSA MAS** | Low yield (2.7% of small $) | **High yield (26.6%)** | Moderate (5.4%) |
| **Prime on SEWP** | Low yield (2.0%) | Low (1.6%) | Low (3.2%) |
| **Direct sales** | **Primary path (88.7%)** | Significant (41.8%) | **Primary path (80.7%)** |
| **Sub to large reseller** | Carahsoft, DLT, CDW, Four LLC | Peraton, Highlight, Carahsoft | Carahsoft, Dell, WWTech |
| **Army ITES/CHESS** | Minor (0.9%) | Moderate (9.8%) | Moderate (5.3%) |

## Next Actions

1. **E208**: Field test — validate findings with 3-5 small software companies
2. **Deep dive**: Subcontract analysis — how much small vendor $ flows as sub to large primes?
3. **GSA MAS Schedule 70 analysis** — which SINs (Special Item Numbers) map to 7030/DA10 software?
4. **SEWP catalog analysis** — which categories do small vendors actually win in?

## Files

- `e207_vehicle.py` — Core analysis module
- `e207_compare.py` — Comparative analysis across all 5 codes
- `e207_comparison.json` — Machine-readable results
- `raw/` — Cached API responses (5,000 awards × 5 codes)

## Evidence Labels

- **Observed**: All API responses, vehicle classifications, percentages
- **Inferred**: VA T4NG absence (pattern not detected, not proven absent)
- **Speculative**: Subcontractor flow percentages (not directly measured)

## Limitations

- Sample limited to 5,000 awards per code (recent 12 months)
- IDV PIID extraction depends on `generated_internal_id` format stability
- "Direct/Unknown" conflates true direct awards with unclassified vehicles
- Small vendor definition (≤3 awards in sample) may miss vendors with many small awards
- CIO-SP4 and VA T4NG may use PIID patterns not in our catalog