# E210: GSA MAS SIN and SEWP Category Analysis for Small Vendor Entry

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-20
-->

## Objective

Map GSA MAS PIIDs to Schedule 70 SINs (Special Item Numbers) and SEWP PIIDs to SEWP categories to identify which contract vehicle categories small software vendors actually win. Extends E207 contract vehicle analysis with actionable SIN/category-level intelligence.

## Method

- Queried USAspending `spending_by_award/` endpoint for recent 12 months (Oct 2024–Sep 2025)
- 5,000 awards per PSC code (25,000 total) across 5 IT/software codes: 7030, DA10, 7A21, DA01, D304
- Extracted IDV PIID from `generated_internal_id` field
- Classified awards using **description-based inference** (primary) + PIID pattern fallback:
  - **GSA MAS**: Description keywords → Schedule 70 SINs (511210 Software, 518210C Cloud, 54151S Services, etc.)
  - **SEWP**: Description keywords → SEWP Categories (A Hardware, B Software, C Services, D Telecom, E AV)
- Identified small vendors (≤3 awards in sample) and measured their share per SIN/category
- Applied affinity scores from public GSA/SEWP award patterns to estimate small vendor opportunity

## Key Findings

### GSA MAS Schedule 70 SIN Analysis by PSC Code

| PSC | SIN | Name | Market ($) | Small Vendor Share | Affinity | Verdict |
|-----|-----|------|------------|-------------------|----------|---------|
| **7030** | 511210 | Software Publishing | 675M | **5.9%** | 85% | Large market, low small vendor access |
| | 511210S | SaaS | 509M | **4.5%** | 80% | Large market, low small vendor access |
| | 518210C | Cloud Services | 509M | **4.5%** | 75% | Large market, low small vendor access |
| | 54151S | IT Services | 194M | **11.0%** | 60% | Moderate market, moderate access |
| **DA10** | 511210 | Software Publishing | 536M | **28.3%** | 85% | **STRONG** - Large market, high small vendor share |
| | 511210S | SaaS | 516M | **27.2%** | 80% | **STRONG** - Large market, high small vendor share |
| | 518210C | Cloud Services | 516M | **27.2%** | 75% | **STRONG** - Large market, high small vendor share |
| | 54151S | IT Services | 114M | **65.6%** | 60% | **STRONG** - High small vendor share |
| **7A21** | 511210 | Software Publishing | 581M | **4.0%** | 85% | Large market, very low small vendor access |
| | 511210S | SaaS | 555M | **3.2%** | 80% | Large market, very low small vendor access |
| | 518210C | Cloud Services | 555M | **3.2%** | 75% | Large market, very low small vendor access |
| | 54151S | IT Services | 72M | **14.2%** | 60% | Small market, moderate access |
| **DA01** | 511210 | Software Publishing | 1,010M | **5.5%** | 85% | Services market (12.8% software per E203) |
| | 54151S | IT Services | 89M | **85.2%** | 60% | Services market - small vendors do services |
| **D304** | 54151S | IT Services | 317M | **75.5%** | 60% | Telecom market (8.1% software per E203) |
| | 511210 | Software Publishing | 283M | **85.5%** | 85% | Tiny software slice of telecom market |

### SEWP Category Analysis by PSC Code

| PSC | Category | Name | Market ($) | Small Vendor Share | Affinity | Verdict |
|-----|----------|------|------------|-------------------|----------|---------|
| **7030** | B | IT Software | 360M | **6.0%** | 80% | Low small vendor access |
| | C | IT Services | 257M | **12.0%** | 60% | Moderate access |
| | A | IT Hardware | 128M | **14.5%** | 20% | Hardware-dominated |
| **DA10** | E | Audio/Visual | 337M | **2.4%** | 25% | Large AV market (conferencing) |
| | B | IT Software | 245M | **1.6%** | 80% | Very low small vendor access |
| | C | IT Services | 192M | **4.8%** | 60% | Low access |
| **7A21** | B | IT Software | 478M | **3.1%** | 80% | Very low access |
| | C | IT Services | 365M | **2.6%** | 60% | Very low access |
| **DA01** | C | IT Services | 30M | **63.7%** | 60% | Services market |
| | B | IT Software | 9M | **3.5%** | 80% | Tiny software market |
| **D304** | C | IT Services | 1.8M | **100%** | 60% | Negligible SEWP usage |

## Cross-Code Comparison: Small Vendor GSA MAS Share

| SIN / Category | 7030 | DA10 | 7A21 | DA01 | D304 |
|---|---|---|---|---|---|
| **511210 Software Publishing** | 5.9% | **28.3%** | 4.0% | 5.5% | 85.5%* |
| **511210S SaaS** | 4.5% | **27.2%** | 3.2% | 4.2% | 58.0%* |
| **518210C Cloud Services** | 4.5% | **27.2%** | 3.2% | 4.2% | 58.0%* |
| **54151S IT Services** | 11.0% | **65.6%** | 14.2% | 85.2% | 75.5% |
| **SEWP B (Software)** | 6.0% | 1.6% | 3.1% | 3.5% | 100%* |
| **SEWP C (Services)** | 12.0% | 4.8% | 2.6% | 63.7% | 100%* |

*\* D304/DA01 small vendor shares are inflated by tiny sample sizes; not software markets per E203.*

## Interpretation

### 1. **DA10 is the only software market with meaningful GSA MAS access for small vendors**
- 28% small vendor share in Software Publishing (511210) — $536M market
- 27% in SaaS (511210S) — $516M market  
- 27% in Cloud Services (518210C) — $516M market
- 66% in IT Services (54151S) — $114M market
- **Matches E207**: 28.2% of small vendor $ in DA10 flows through GSA MAS + SEWP

### 2. **7030 GSA MAS is dominated by large resellers**
- Carahsoft, DLT, Dell, CDW, Four LLC capture most GSA MAS flow
- Small vendors: 5-6% share in software SINs despite 85% affinity
- 7030 small vendors sell **direct** (88.7% per E207), not through GWACs

### 3. **7A21 GSA MAS similarly concentrated**
- Carahsoft dominates across GSA MAS ($192M), Navy SEAPORT ($240M), Other/Unknown ($295M)
- Small vendor share only 3-4% in software SINs

### 4. **SEWP is not a small vendor channel for software**
- All codes show <6% small vendor share in SEWP Category B (Software)
- SEWP primes are large integrators/resellers; small vendors don't win prime positions
- Exception: DA01/D304 show high shares but tiny markets, not software

### 5. **DA01 and D304 are not software product markets**
- E203 confirmed: DA01 = 12.8% software, D304 = 8.1% software
- High small vendor shares in services SINs/categories reflect services labor, not software products
- DA01: 85% small vendor share in 54151S (IT Services) = services subcontracting

## Small Vendor Entry Strategy by PSC Code

| Strategy | 7030 (Software) | DA10 (Services) | 7A21 (HW/SW) |
|---|---|---|---|
| **GSA MAS 511210 (Software)** | Low yield (5.9%) | **High yield (28.3%)** | Low yield (4.0%) |
| **GSA MAS 511210S (SaaS)** | Low yield (4.5%) | **High yield (27.2%)** | Low yield (3.2%) |
| **GSA MAS 518210C (Cloud)** | Low yield (4.5%) | **High yield (27.2%)** | Low yield (3.2%) |
| **GSA MAS 54151S (Services)** | Moderate (11.0%) | **High yield (65.6%)** | Moderate (14.2%) |
| **SEWP Cat B (Software)** | Low (6.0%) | Very low (1.6%) | Very low (3.1%) |
| **SEWP Cat C (Services)** | Moderate (12.0%) | Low (4.8%) | Very low (2.6%) |
| **Direct Sales** | **Primary (88.7%)** | Significant (41.8%) | **Primary (80.7%)** |
| **Sub to Large Prime** | Carahsoft, DLT, CDW | Peraton, Highlight, Carahsoft | Carahsoft, Dell |

## Gate Results

| Gate | Criterion | Result |
|------|-----------|--------|
| G1 | SIN/category inference works for all 5 codes | **PASS** — Description-based classification successful |
| G2 | Meaningful variation in small vendor share across codes | **PASS** — DA10 28% vs 7030 6% vs 7A21 4% |
| G3 | Results consistent with E207 vehicle analysis | **PASS** — DA10 only code with high GWAC small vendor share |
| G4 | High-affinity SINs identified with market size >$100M | **PASS** — 511210, 511210S, 518210C all >$500M in DA10 |

## Conclusions

1. **DA10 GSA MAS Schedule 70 is the premier vehicle for small software vendors** — 28% small vendor share in $1.5B+ of software/cloud/SaaS market across 511210, 511210S, 518210C

2. **7030 and 7A21 GSA MAS are large reseller channels** — Small vendors should pursue direct sales or subcontracting, not GSA MAS prime positions

3. **SEWP is not a viable prime vehicle for small software vendors** — <6% small vendor share across all software codes; primes are large integrators

4. **SIN-level targeting matters** — A small software vendor should target:
   - DA10: 511210 (Software), 511210S (SaaS), 518210C (Cloud) on GSA MAS
   - 7030: Direct sales to 3,916 recipients (32% ≤$40k) or sub to Carahsoft/DLT/CDW
   - 7A21: Avoid; extreme concentration around Carahsoft

5. **The "Direct/Unknown" 88.7% in 7030 is truly direct** — Confirmed by E209 (0.1% subcontracting) and this analysis (GSA MAS small vendor share only 6%)

## Next Actions

1. **Integrate SIN/SEWP analysis into E206 CLI tool** — Add `--module vehicle_sin` for SIN/category-level assessment
2. **GSA MAS SIN validation** — Cross-reference top PIIDs with GSA eLibrary for actual SIN holdings
3. **SEWP catalog deep dive** — Map specific SEWP holders to their awarded categories using NASA SEWP public data
4. **Prime-specific subaward trace** — Use `/api/v2/subawards/` with `prime_award_piid` to trace Carahsoft/Dell/Leidos sub flows in 7030
5. **E208 field test** — Validate framework with 3-5 small software companies (requires authorization)

## Files

- `e210_sin_sewp.py` — Main analysis module with SIN/category reference tables and inference logic
- `raw/` — Cached API responses (5,000 awards × 5 codes, reused from E207)

## Evidence Labels

- **Observed**: All API responses, computed SIN/category metrics, small vendor shares
- **Inferred**: SIN/category classification from description keywords (primary), PIID patterns (fallback)
- **Speculative**: Affinity scores (based on public pattern knowledge, not measured in this experiment)

## Limitations

1. **Description-based inference** is heuristic; actual SIN holdings require GSA eLibrary/SEWP catalog cross-reference
2. **5,000 award sample** per code (USAspending API 500-page ceiling)
3. **Small vendor definition** (≤3 awards in sample) may not capture all small businesses
4. **Affinity scores** are estimates from public knowledge, not measured in this experiment
5. **DA01/D304** are not software markets (per E203); their high service SIN shares reflect services labor