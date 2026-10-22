# E220 Protocol: IT PSC Sub-Segment Entrant Advisor Prototype

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-22
-->


## Objective

Build a runnable prototype tool that identifies the most enterable sub-segments (NAICS codes) within the three enterable federal IT PSC codes (DA01, DA10, 7A21) discovered in E209, for small programs seeking federal contract opportunities.

## Background

E209 measured segment newcomer fractions for 5 IT PSC codes using USAspending recipient data (FY2023 current, FY2018–2022 prior):
- **Enterable cluster** (27–31% segment newcomers): DA01, DA10, 7A21
- **Closed cluster** (0% segment newcomers): 7030, D304

The enterable codes represent service/development categories:
- DA01: Application Development Labour ($60.9B obligation)
- DA10: SaaS ($18.5B obligation)  
- 7A21: Perpetual Licence Software ($13.7B obligation)

## Research Question

Within each enterable PSC code, which NAICS sub-segments are most accessible to small programs? Measured by:
1. Segment newcomer fraction (fraction of current-window recipients new to that NAICS-within-PSC)
2. Fragmentation (1 - top-5 recipient obligation share)
3. Market size (total obligation)
4. Absolute newcomer count

## Data Source

USAspending API v2:
- `POST /api/v2/search/spending_by_category/naics/` — NAICS breakdown within PSC code
- `POST /api/v2/search/spending_by_category/recipient/` — Recipients within (PSC, NAICS) combination

## Windows

| Window | Fiscal Years | USAspending `time_period` |
|--------|--------------|---------------------------|
| **Current** | FY2023 | `[{"start_date": "2023-01-01", "end_date": "2023-12-31"}]` |
| **Prior** | FY2018–2022 | `[{"start_date": "2018-01-01", "end_date": "2022-12-31"}]` |

## Target PSC Codes

Enterable codes from E209: **DA01, DA10, 7A21**

## Gates (Predeclared)

| Gate | Condition | Threshold |
|------|-----------|-----------|
| **G0** | API accessible, returns data for all 3 PSC codes | 3/3 codes return NAICS breakdown |
| **G1** | Identity coverage | ≥ 95% of recipient rows carry `recipient_id` |
| **G2** | Prior window complete | All 3 PSC codes return ≥ 5 NAICS codes in prior window |
| **G3** | Sub-segment differentiation | ≥ 2 NAICS codes per PSC show > 10pp spread in segment newcomer fraction |
| **G4** | Actionable output | Tool produces ranked table with ≥ 3 sub-segments classified as "HIGHLY ENTERABLE", "SOMEWHAT ENTERABLE", or "MARGINAL" |

## Enterability Classification (Predeclared)

Based on E209's observed segment newcomer fractions (0.2677–0.3113 for enterable codes):

| Classification | Segment Newcomer Fraction | Fragmentation (1 - top5) | Minimum Newcomer Count |
|----------------|---------------------------|--------------------------|------------------------|
| **HIGHLY ENTERABLE** | ≥ 0.30 | ≥ 0.60 | ≥ 20 |
| **SOMEWHAT ENTERABLE** | ≥ 0.20 | ≥ 0.40 | ≥ 10 |
| **MARGINAL** | ≥ 0.10 | ≥ 0.20 | ≥ 5 |
| **CLOSED** | < 0.10 | < 0.20 | — |

## Output Artifacts

1. `raw/naics_current_{CODE}.json` — NAICS breakdown for current window
2. `raw/naics_prior_{CODE}.json` — NAICS breakdown for prior window  
3. `raw/recipients_{CODE}_{NAICS}_{WINDOW}.json` — Recipient data per (PSC, NAICS, window)
4. `results/subsegment_metrics.csv` — Per-subsegment metrics
5. `results/ranked_subsegments.csv` — Ranked by enterability score
6. `RESULT.md` — Gate verdicts, interpretation, prototype assessment

## Kill Condition

If **G3 FAILS** (insufficient differentiation across NAICS sub-segments within enterable PSC codes), the sub-segment approach does not add value over PSC-level analysis, and the prototype should not be developed further.

## Implementation Notes

- Rate limit: USAspending unauthenticated ~60 req/hour. Use caching aggressively.
- Fetch NAICS for all 3 codes first (6 API calls: 3 codes × 2 windows)
- Then fetch recipients for top NAICS codes by obligation (prioritize by market size)
- Cache all raw responses with SHA-256 integrity verification
- All gates evaluated on committed raw data only