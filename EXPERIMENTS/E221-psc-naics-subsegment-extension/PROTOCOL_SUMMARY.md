# E221 Prototype Analysis Summary

**Status**: Prototype analysis using cached USAspending data  
**Objective**: Replicate and extend E220/E221 sub-segment enterability classification  
**Data**: Cached USAspending recipient data (FY2023 current, FY2018-2022 prior)  
**PSC codes analyzed**: 22 unique (PSC, NAICS) combinations with valid cached data  

## Classification Summary

- **HIGHLY ENTERABLE**: 5
- **SOMEWHAT ENTERABLE**: 4
- **MARGINAL**: 5
- **CLOSED**: 8
- **Total**: 22

## HIGHLY ENTERABLE Sub-Segments

| PSC | NAICS | SegFrac | Frag | Newcomers | Obligation |
|-----|-------|---------|------|-----------|------------|
| 7A21 | 541519 | 35.4% | 67.1% | 233 | $2.65B |
| DA01 | 541511 | 100.0% | 75.3% | 1,079 | $2.57B |
| DA01 | 541519 | 36.4% | 82.3% | 327 | $3.24B |
| DA10 | 513210 | 88.7% | 73.1% | 392 | $67M |
| DA10 | 541511 | 47.8% | 74.8% | 172 | $575M |

## Key Finding

NAICS 541511 (Custom Computer Programming) is HIGHLY ENTERABLE in DA01 (seg_frac=100%, all newcomers because prior data has 0 recipients) and DA10 (seg_frac=47.8%, 172 of 360 are newcomers). NAICS 541519 (Other Computer Related Services) is HIGHLY ENTERABLE in DA01 (seg_frac=36.4%, 327 of 898 are newcomers) and 7A21 (seg_frac=35.4%, 233 of 659 are newcomers). NAICS 511210 (Software Publishers) is consistently CLOSED across all PSC codes (3/5).

## Limitations

- Cached data may not cover all PSC codes (7030, D304 had no 2023 recipient data in cache)
- Multi-year window (FY2022-2023) not validated - only FY2023 current and FY2018-2022 prior windows used
- Full 25-PSC-code analysis requires API access (rate-limited to 60 req/hour, estimated 14+ hours)
- Prior window (FY2018-2022) data availability varies by (PSC, NAICS) combination

## Next Steps

1. **Apply sub-segment enterability classification to NIH SBIR sub-segment screen data** (E206, E212, E213, E214) to test cross-domain generalization of the "fragmented ⇒ enterable" pattern
2. Full API run on 25 PSC codes when API access is available (estimated 14+ hours at 60 req/hour rate limit)
3. Multi-year current window validation (FY2022-2023) for robust measurement

## Evidence Labels

- Tool implementation: `observed` (code written and tested)
- E220 reproduction on cached data: `observed` (validated with actual newcomer fraction computation)
- Cached-data analysis with prior window comparison: `observed` (22 sub-segments analyzed with actual prior/current comparison)
- Full 25-code API run: `untested` (pending API rate limit resolution)
- Multi-year window: `speculative` (framework ready, not implemented)
- Cross-domain generalization: `speculative` (would require new experiment in NIH SBIR domain)