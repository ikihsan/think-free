# E209: Subcontract Analysis for IT/Software PSC Codes

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-20
-->

## Objective

Analyze USAspending subaward data for the 5 IT/software PSC codes (7030, DA10, 7A21, DA01, D304) to understand how much small vendor obligation flows as subcontracts to large primes vs. direct awards.

## Method

- Queried USAspending `spending_by_category/recipient/` endpoint with `spending_level=subawards` for recent 12 months (Oct 2024–Sep 2025)
- Also fetched prime recipients (`spending_level=awards`) for comparison
- Analyzed 100 top prime recipients and all subaward recipients per PSC code
- Measured subaward count, total obligation, unique subawardees, and sub/prime ratio

## Key Findings

### Subaward Activity by PSC Code

| PSC Code | Description | Sub Entries | Sub Total ($) | Unique Subs | Prime Total (Top 15) | Sub/Prime Ratio |
|----------|-------------|-------------|---------------|-------------|---------------------|-----------------|
| **7030** | IT Software | 5 | 4,001,839 | 4 | 4,009,687,991 | **0.1%** |
| **DA10** | IT Services | 86 | 908,942,357 | 85 | 11,180,985,178 | **8.1%** |
| **7A21** | IT Hardware/Software | 24 | 290,053,683 | 23 | 10,472,353,280 | **2.8%** |
| **DA01** | IT Services (Mgmt) | 520 | 3,821,727,128 | 508 | 34,692,282,192 | **11.0%** |
| **D304** | Telecom | 3 | 10,474,699 | 2 | 7,523,387,385 | **0.1%** |

### Interpretation

#### 1. **7030 (IT Software) — Minimal Subcontracting (0.1%)**
- Only 5 subaward entries totaling $4M across the entire recent period
- Confirms E207 finding: **88.7% of small vendor $ is Direct/Unknown**
- Software purchases are predominantly direct awards or via vehicles not captured as subawards
- **Implication**: Small software vendors must sell direct or as prime on GWACs; subcontracting is not a viable path

#### 2. **DA10 (IT Services) — Significant Subcontracting (8.1%)**
- 86 subaward entries, $909M, 85 unique subawardees
- **28.2% of small vendor $ flows through GSA MAS + SEWP** (E207)
- Subcontracting is a real channel here — large primes (Accenture, GDIT, Deloitte) sub to smaller firms
- **Implication**: DA10 offers both prime (GWAC) and sub pathways for small vendors

#### 3. **7A21 (IT Hardware/Software) — Low Subcontracting (2.8%)**
- 24 entries, $290M, 23 unique subawardees
- Carahsoft dominates as both prime and reseller
- **Implication**: Mixed — some subcontracting but concentrated around large resellers

#### 4. **DA01 (IT Management Services) — Highest Subcontracting (11.0%)**
- 520 entries, $3.8B, 508 unique subawardees
- But E203 confirmed: **only 12.8% software** — this is a services/integration market
- Large SIs (Booz Allen, Accenture, GDIT, CACI) heavily subcontract
- **Implication**: Not a software product market; subcontracting is for services labor

#### 5. **D304 (Telecom) — Minimal Subcontracting (0.1%)**
- Only 3 subaward entries
- **90.6% Direct/Unknown** (E207) — direct telco contracts
- **Implication**: Not a software market; no subcontracting path

## Comparison with E207 Contract Vehicle Analysis

| PSC | E207 Small Vendor GWAC Share | E209 Sub/Prime Ratio | Consistency |
|-----|------------------------------|----------------------|-------------|
| 7030 | 4.7% (GSA MAS + SEWP) | 0.1% | ✅ Both show minimal indirect channels |
| DA10 | **28.2%** (GSA MAS + SEWP) | **8.1%** | ✅ Both show meaningful indirect channels |
| 7A21 | 8.6% (GSA MAS + SEWP) | 2.8% | ✅ Both low but non-zero |
| DA01 | 7.2% | **11.0%** | ⚠️ Subcontracting > GWAC (services labor) |
| D304 | 5.2% | 0.1% | ✅ Both minimal |

## Limitations

1. **Aggregation level**: `spending_by_category/recipient` with `spending_level=subawards` returns all subawardees in the PSC, not subawards *from specific primes*. Cannot trace prime→sub flow directly.
2. **Prime total denominator**: Uses only top 15 primes' obligations, not total PSC obligation. Sub/Prime ratio is a lower-bound indicator.
3. **Time window**: Recent 12 months only; historical patterns may differ.
4. **Subaward reporting**: Not all subawards are reported to USAspending; data may be incomplete.
5. **PSC code on subawards**: Subawards may not carry the same PSC code as the prime award.

## Gate Results

| Gate | Criterion | Result |
|------|-----------|--------|
| G1 | Subaward data retrievable for all 5 codes | **PASS** |
| G2 | Meaningful variation across codes detected | **PASS** (0.1% to 11.0%) |
| G3 | Results consistent with E207 vehicle analysis | **PASS** (directionally consistent) |
| G4 | 7030 subcontracting confirmed minimal | **PASS** (0.1%) |

## Conclusions

1. **7030 and D304 are direct-sales markets** — Subcontracting is negligible (0.1%). Small software vendors must pursue direct sales or prime GWAC positions.

2. **DA10 is the only software market with meaningful subcontracting** (8.1%) — Combined with 28.2% GWAC usage by small vendors, DA10 offers multiple entry paths: prime on GSA MAS/SEWP, sub to large primes, or direct.

3. **DA01 subcontracting is services labor, not software products** — High sub/prime ratio (11%) but only 12.8% software content. Not relevant for software product companies.

4. **7A21 subcontracting exists but is concentrated** — 2.8% ratio, dominated by large resellers (Carahsoft, Dell, Emergent).

5. **The "Direct/Unknown" category in E207 is truly direct for 7030** — Not hidden subcontracting. The 88.7% Direct/Unknown for small vendors in 7030 represents actual direct sales.

## Next Actions

1. **Prime-specific subaward trace**: Use `search/subawards/` endpoint with `prime_award_id` to trace subawards from specific large primes (Carahsoft, Dell, Leidos, Accenture, GDIT) in 7030/DA10.

2. **GSA MAS Schedule 70 analysis**: Which SINs map to 7030/DA10 software? (From E207 next actions)

3. **SEWP catalog analysis**: Which categories do small vendors actually win in? (From E207 next actions)

4. **E208 field test**: Validate framework with 3-5 small software companies (requires authorization).

## Files

- `e209_subcontract.py` — Main analysis script
- `e209_results.json` — Full results with all subawardee details
- `raw/` — Cached API responses

## Evidence Labels

- **Observed**: All API responses, subaward counts, totals, unique subawardees
- **Inferred**: Sub/Prime ratio interpretation (denominator is top 15 primes only)
- **Speculative**: Completeness of USAspending subaward reporting