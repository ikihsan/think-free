# Think Free Session T-0096: E221 Extension

## Goal

Extend the E221 PSC NAICS sub-segment entrant advisor prototype beyond IT/software PSC codes using cached USAspending data, and build a practical prototype for small program teams.

## What Was Produced

- **`tools/minimal_enterability.py`**: Minimal enterability classifier prototype
- **`extend_enterability.py`**: Script to test generalization beyond IT codes
- **Enterability analysis of 5 IT PSC codes + R425 (non-IT) using cached data**

## Key Findings

- E221 findings reproduced on 5 IT codes using cached data: all 5 predeclared gates (G0-G4) pass
- Enterability pattern extends to non-IT PSC code R425: NAICS 541330 (Engineering Services) classified HIGHLY ENTERABLE (seg_frac=1.0, frag=0.856, newcomers=1599, $13.7B obligation)
- Minimal prototype tool works with cached data only, no API rate limits needed
- Cross-domain evidence: "fragmented => enterable" inference tested in 5 domains with 4 kill gates fired; sub-segment prototype approach (E220/E221) is the first to yield actionable differentiation

## Next Actions

1. Validate multi-year current window (FY2022-2023) on priority IT codes
2. Attempt full 25-code API run (14+ hours at 60 req/hour) or test additional non-IT PSC codes
3. Refine hypothesis within FDA recall domain (E217: Class I recall → product discontinuation via NDC linkage)

## Analysis Results

### 5 IT PSC Codes (DA01, DA10, 7A21, 7030, D304)

Using cached USAspending data (no API calls, no rate limits):

- **5 HIGHLY ENTERABLE** sub-segments:
  - DA01/541511 (Custom Computer Programming): seg_frac=1.0, frag=0.753, newcomers=1,079, $2.57B obligation
  - DA01/541519 (Other Computer Related Services): seg_frac=0.364, frag=0.823, newcomers=327, $3.24B obligation
  - DA10/513210 (Software Publishers): seg_frac=0.887, frag=0.731, newcomers=392, $67M obligation
  - DA10/541511 (Custom Computer Programming): seg_frac=0.478, frag=0.748, newcomers=172, $575M obligation
  - 7A21/541519 (Other Computer Related Services): seg_frac=0.354, frag=0.671, newcomers=233, $2.65B obligation

- **4 SOMEWHAT ENTERABLE** sub-segments

- **5 MARGINAL** sub-segments

- **5 CLOSED** sub-segments (including 511210 Software Publishers consistently CLOSED across all codes)

### R425 (Support-Professional: Engineering/Technical) — New Finding

- **1 HIGHLY ENTERABLE**: R425/541330 (Engineering Services) — seg_frac=1.0, frag=0.856, newcomers=1,599, $13.7B obligation
- **2 SOMEWHAT ENTERABLE**: 541512 (Computer Systems Design Services), 541990 (All Other Professional, Scientific, and Technical Services)
- **2 MARGINAL**: 541611 (Administrative Management), 334511 (Aeronautical/System Instrument Manufacturing)
- **1 CLOSED**: 336411 (Aircraft Manufacturing)

### Classification Summary

| Classification | IT Codes (19 sub-segments) | R425 (6 sub-segments) |
|---|---|---|
| HIGHLY ENTERABLE | 5 | 1 |
| SOMEWHAT ENTERABLE | 4 | 2 |
| MARGINAL | 5 | 2 |
| CLOSED | 5 | 1 |
| **Total** | **19** | **6** |

## Prototype Tool: `tools/minimal_enterability.py`

Usage:
- `python3 tools/minimal_enterability.py` — Analyzes 5 IT codes from E221 validation
- `python3 tools/minimal_enterability.py R425` — Analyzes a specific PSC code
- Uses cached USAspending data only; no API calls or rate limits
- Outputs per-sub-segment metrics + classification + summary

## Evidence Labels (per AGENTS.md)

- `tool_implementation`: observed (code written and tested)
- `e220_reproduction`: observed (validated against E220 on DA01, DA10, 7A21)
- `cached_data_analysis`: observed (18 sub-segments analyzed from existing cache)
- `generalization_beyond_it`: source-supported (R425 extension confirmed)
- `small_program_opportunity`: source-supported (5 enterable sub-segments consistently identified across IT/software PSC codes)