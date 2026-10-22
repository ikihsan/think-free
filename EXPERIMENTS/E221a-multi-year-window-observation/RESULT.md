# E221a Result: Multi-Year Current Window Observation

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-22
-->

## Summary

**STATUS: FRESH OBSERVATION — Multi-year window enterability robustness question**

Anecdotal analysis using cached USAspending data suggests the multi-year current window (FY2022-2023) may produce different enterability classifications compared to the single-year window (FY2023 only), but definitive validation requires FY2022 recipient data not currently in cache.

### Background

E221 extended the E220 sub-segment entrant advisor to all PSC codes. The tool uses a single-year current window (FY2023) with a five-year prior window (FY2018-2022). The multi-year current window option (FY2022-2023) is implemented in the code (`--multi-year` flag) but has not been executed on the full PSC code set.

The question of whether the current window duration affects enterability classifications is important for practical use: if multi-year data makes previously enterable segments appear less so (or vice versa), this would affect go-to-market timing and strategy for small programs.

### Available Cached Data Analysis

Using existing cache (154 entries), partial analysis was performed on PSC DA01 with the following key sub-segments:

| NAICS | 2023 Recipients | 2018 Prior Recipients | Newcomers | SegFrag | Classification (2023-only) |
|-------|----------------|----------------------|-----------|---------|----------------------------|
| 541511 | 1,079 | 0 | 1,079 (100%) | 75.3% | **HIGHLY ENTERABLE** |
| 541519 | 898 | 732 | 327 (36.4%) | 82.3% | **HIGHLY ENTERABLE** |
| 541512 | 1,709 | 1,650 | 156 (9.1%) | 66.9% | CLOSED |

**Key observation**: NAICS 541511 has 0 prior-window recipients in the 2018 data point, meaning all 1,079 current recipients are newcomers — yielding a 100% segment newcomer fraction. If FY2022 data were included in the current window, some of those recipients may have been already active in FY2022, potentially reducing the newcomer fraction.

### Multi-Year Window Framework

The tool supports multi-year current windows (`--multi-year` flag, FY2022-2023), which would:
- Combine FY2022 and FY2023 as the "current" window
- Keep the prior window as FY2018-2022 (5 years)
- Potentially reduce newcomer fractions if FY2022 recipients overlap with the prior window
- Affect enterability classifications per the E220 thresholds:
  - HIGHLY ENTERABLE: seg_frac >= 0.30, frag >= 0.60, newcomers >= 20
  - SOMEWHAT ENTERABLE: seg_frac >= 0.20, frag >= 0.40, newcomers >= 10
  - MARGINAL: seg_frac >= 0.10, frag >= 0.20, newcomers >= 5

### Gap: Missing FY2022 Recipient Data

FY2022 recipient data for the (PSC, NAICS) combinations is not in the existing cache. The cache has `naics_DA01_2022` (NAICS breakdown for DA01 in FY2022) but does not have `recipients_DA01_{NAICS}_2022` for the key IT codes (541511, 541519, 541512). Without this data, the multi-year window analysis cannot be completed.

### Cross-Domain Context

The "fragmented ⇒ enterable" inference has been tested in five domains:
- NIH SBIR (E208): ρ = −0.246, p = 0.975 — kill gate fired
- Federal IT PSC (E209): ρ = +0.667, p = 0.135 — kill gate fired (n=5)
- International trade (E215): ρ = −0.123, p = 0.623 — kill gate fired
- World Bank projects (E219): ρ = −0.100, p = 0.770 — kill gate fired
- OpenAlex research topics (E218): ρ = +0.604, p < 0.0001 — G3 pass, qualified (driven by Arts/Humanities vs STEM clustering, not market-entry dynamics)

E220/E221 sub-segment approach is the first to yield actionable differentiation (5 enterable sub-segments identified with concrete obligation figures).

### Next Action

**Option 1**: Execute `tools/psc_naics_subsegment_analyzer.py --multi-year --psc-codes DA01 DA10 7A21` to fetch FY2022 data and validate the multi-year window framework. Estimated 3-4 hours at 60 req/hour rate limit for 3 codes.

**Option 2**: Fresh observation in a completely new domain axis per D083, applying the sub-segment entrant advisor methodology to a different market (e.g., state procurement, university research funding, or healthcare spending).

**Option 3**: Run the full 25-PSC code analysis (`--max-psc 25`), estimated at 14+ hours at 60 req/hour, pending API rate-limit resolution.

**Decision**: Proceed with **Option 1** (multi-year window validation on 3 IT codes) to concretely determine whether the current window duration affects enterability classifications. This is the smallest adequate intervention that directly addresses the methodological question without the 14+ hour full run commitment. If FY2022 data is insufficient or the results are ambiguous, Option 2 (fresh observation in new domain) will be the fallback.

**Failure condition**: If FY2022 recipient data cannot be retrieved within rate limits, or if the multi-year analysis produces inconclusive results due to data sparsity, close this claim and move to Option 2.

**Success criterion**: Clear enterability classifications under the multi-year window (FY2022-2023 current vs FY2018-2022 prior) for at least 3 sub-segments per code, allowing comparison with the single-year (FY2023-only) results.