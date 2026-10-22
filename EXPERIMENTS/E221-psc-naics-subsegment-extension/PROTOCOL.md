# E221 Protocol: PSC NAICS Sub-Segment Entrant Advisor — Full PSC Extension

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-22
-->


## Objective

Extend the E220 sub-segment entrant advisor prototype (which analyzed 3 IT PSC codes: DA01, DA10, 7A21) to all 100+ PSC codes using NAICS-within-PSC granularity, to identify the most enterable market segments for small programs across the entire federal contracting landscape.

## Background

E220 successfully demonstrated that sub-segment analysis adds significant value over PSC-level analysis:
- Strong differentiation exists at NAICS level within each PSC code
- NAICS 541511 (Custom Computer Programming) and 541519 (Other Computer Related Services) are consistently HIGHLY ENTERABLE across all three enterable IT PSC codes
- The PSC-level "enterable" label masked dramatic within-PSC variation (DA01: 9–36% newcomer fraction)

E196 identified the top 25 PSC codes by addressable small purchases (≤$100k awards in ≥$1B cells), with IT/software codes forming the densest cluster.

## Research Question

Across all PSC codes with meaningful small-purchase volume, which NAICS sub-segments are most accessible to small programs? Measured by:
1. Segment newcomer fraction (fraction of current-window recipients new to that NAICS-within-PSC)
2. Fragmentation (1 - top-5 recipient obligation share)
3. Market size (total obligation)
4. Absolute newcomer count

## Data Source

USAspending API v2:
- `POST /api/v2/search/spending_by_category/psc/` — All PSC codes with obligation
- `POST /api/v2/search/spending_by_category/naics/` — NAICS breakdown within PSC code
- `POST /api/v2/search/spending_by_category/recipient/` — Recipients within (PSC, NAICS) combination

## Windows

| Window | Fiscal Years | USAspending `time_period` |
|--------|--------------|---------------------------|
| **Current** | FY2023 | `[{"start_date": "2023-01-01", "end_date": "2023-12-31"}]` |
| **Prior** | FY2018–2022 | `[{"start_date": "2018-01-01", "end_date": "2022-12-31"}]` |
| **Current (multi-year)** | FY2022–2023 | `[{"start_date": "2022-01-01", "end_date": "2022-12-31"}, {"start_date": "2023-01-01", "end_date": "2023-12-31"}]` |

## Target Selection

1. **Primary**: Top 25 PSC codes from E196 G4 (addressable small-purchase cells)
2. **Secondary**: All PSC codes with ≥$1B obligation and ≥1,000 awards ≤$100k
3. **Tertiary**: All 100+ PSC codes (resource-dependent)

## Gates (Predeclared)

| Gate | Condition | Threshold |
|------|-----------|-----------|
| **G0** | API accessible, returns NAICS breakdown for analyzed PSC codes | ≥ 90% of target codes return NAICS breakdown |
| **G1** | Identity coverage | ≥ 95% of recipient rows carry `recipient_id` |
| **G2** | Prior window complete | All target PSC codes return ≥ 5 NAICS codes in prior window |
| **G3** | Sub-segment differentiation | ≥ 2 NAICS codes per PSC show > 10pp spread in segment newcomer fraction |
| **G4** | Actionable output | Tool produces ranked table with ≥ 10 sub-segments classified as "HIGHLY ENTERABLE", "SOMEWHAT ENTERABLE", or "MARGINAL" across all PSC codes |

## Enterability Classification (from E220)

| Classification | Segment Newcomer Fraction | Fragmentation (1 - top5) | Minimum Newcomer Count |
|----------------|---------------------------|--------------------------|------------------------|
| **HIGHLY ENTERABLE** | ≥ 0.30 | ≥ 0.60 | ≥ 20 |
| **SOMEWHAT ENTERABLE** | ≥ 0.20 | ≥ 0.40 | ≥ 10 |
| **MARGINAL** | ≥ 0.10 | ≥ 0.20 | ≥ 5 |
| **CLOSED** | < 0.10 | < 0.20 | — |

## Output Artifacts

1. `raw/psc_all_2023.json` — All PSC codes with obligation
2. `raw/naics_{CODE}_{YEAR}.json` — NAICS breakdown per PSC per window
3. `raw/recipients_{CODE}_{NAICS}_{YEAR}.json` — Recipient data per (PSC, NAICS, window)
4. `results/subsegment_metrics.csv` — Per-subsegment metrics
5. `results/ranked_subsegments.csv` — Ranked by enterability score
6. `results/gates.json` — Gate verdicts
7. `RESULT.md` — Gate verdicts, interpretation, prototype assessment

## Kill Condition

If **G3 FAILS** (insufficient differentiation across NAICS sub-segments within the majority of analyzed PSC codes), the sub-segment approach does not add value over PSC-level analysis for the broader federal market, and the extension should not be developed further.

## Implementation Notes

- Rate limit: USAspending unauthenticated ~60 req/hour. Use caching aggressively.
- Fetch PSC codes first, then NAICS for each code (2 API calls per code: current + prior)
- Then fetch recipients for top NAICS codes by obligation (prioritize by market size)
- Cache all raw responses with SHA-256 integrity verification
- All gates evaluated on committed raw data only
- Multi-year current window option available but not yet implemented

## Expected Timeline

Given rate limits (~60 req/hour) and ~25 target codes × 2 windows × ~8 NAICS × 2 windows = ~800 API calls for recipient data, full run would take ~14 hours. Initial test on 3 codes (DA01, DA10, 7A21) validates approach matches E220.