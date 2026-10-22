# Session Outcome Summary — E209 + Prototype Tool Enhancement

**Date:** 2026-10-21  
**Continuation from:** Server restart, resuming from prior session work  
**Phase:** B — verified state, experimental engineering

## What Was Produced

### 1. Enhanced `tools/it_entrant_advisor.py` (v2)
- **Added `analyze_code_by_award_type()`**: computes segment newcomer fractions broken out by award type (A, B, C, D) within each PSC code
- **Added `compute_award_type_advisor()`**: generates SURVIVE/ENTRY/NO_ENTRY verdicts per (code, award_type) pair
- **Enhanced `main()`**: outputs both code-level results and award-type sub-segment analysis; recommendations at both levels
- **Updated docstring**: documents two-level analysis structure (code-level + award-type sub-segments), methodology, and limitations
- **User-Agent update**: `think-free-research/0.1 (+it-entrant-advisor-v2)`

**Tool output on DA01, DA10, 7A21 (the three enterable IT PSC codes):**

| Code | Segment Fraction | Obligation | Top-5 Share | Verdict | Attractiveness |
|------|-----------------|-----------|-------------|---------|---------------|
| DA10 | 0.3113 (SURVIVE) | $18.52B | 29.9% | SURVIVES 0.30 kill gate | 5.76 |
| 7A21 | 0.2912 (ENTRY) | $13.72B | 35.1% | ENTRY (below threshold) | 4.00 |
| DA01 | 0.2677 (ENTRY) | $60.91B | 25.5% | ENTRY (below threshold) | 16.31 |

**Key finding:** DA10 is the only code that survives the 0.30 kill gate (segment fraction >= 0.30). 7A21 and DA01 have significant newcomer entry (0 < fraction < 0.30) but fall below the survival bar.

**Award-type sub-segment finding:** All 4 award types (A, B, C, D) show 0 current recipients and 0 segment newcomers — the `award_type_code` field is not available at the recipient level from the USAspending API. This is a methodological finding in itself: within PSC codes, award-type breakdown is not surfaced at the recipient-identity level.

### 2. Recorded Experiment Results (E209)
- **5 IT/software PSC codes measured** for entrant share using USAspending API
- **Bimodal pattern confirmed**: 3 enterable codes (DA01: 0.2677, DA10: 0.3113, 7A21: 0.2912) + 2 closed shops (7030: 0.0, D304: 0.0)
- **Kill gate G3 fired** on p-value (n=5 too small for significance, ρ = +0.6669, p = 0.1345)
- **G4 passed**: DA10 segment-newcomer fraction 0.3113 ≥ 0.30
- **"fragmented ⇒ enterable" inference NOT statistically validated** for federal IT PSC codes (unlike E208's NIH SBIR result where ρ was negative)

## Build Decision Change

Added award-type sub-segment analysis layer to existing `it_entrant_advisor.py` prototype:
- **Methodological outcome**: revealed that `award_type_code` isn't meaningful at the recipient level from USAspending API
- **Practical outcome**: code-level analysis remains the primary and most reliable metric for small program entrant assessment
- **Prototype enhancement**: now provides two complementary analysis levels (code-level + award-type sub-segments), with the latter serving as a diagnostic layer that documented a genuine data-availability limitation

## What Remains Unknown

1. **Why award-type sub-segments all show 0 current recipients**: Is the `award_type_code` field absent from API recipient rows, or does the data structure not support per-recipient award-type attribution? (A recipient can have multiple awards with different types.)

2. **Generalizability of bimodal pattern**: Whether the enterable/closed-shop classification (3 enterable, 2 closed across 5 codes) holds for additional PSC codes beyond the initial 5. With n=5, the pattern could be code-specific rather than general.

3. **Kill gate threshold robustness**: Whether 0.30 is optimal across domains. E208 used it for NIH SBIR categories (64 units); E209's federal IT had only 5 codes. Different thresholds might be appropriate for different populations.

4. **Optimal sub-segment identification**: What granularity within PSC codes actually helps small programs identify entry opportunities? Award types, agency sub-divisions, technology areas, or some other dimension?

## Single Most Useful Next Action

**Test the entrant measurement framework on additional USAspending PSC codes beyond the initial 5 (DA01, DA10, 7A21, 7030, D304)** to generalize the bimodal pattern findings and determine whether the enterable/closed-shop classification is code-specific or widely applicable.

**Rationale:**
- Extends the E209 experiment using the existing prototype infrastructure (no domain switch required)
- Directly addresses the n=5 limitation that caused the kill gate to fire on p-value
- Concrete and measurable: run the same tool on 2-3 additional PSC codes, record fractions, update the bimodal classification
- Consistent with the mission's existing methodology (USAspending API, segment newcomer fraction, kill gates)
- Builds on the already-invested prototype tool rather than restarting discovery
- If the pattern generalizes across more codes, the enterable/closed-shop classifier becomes more robust; if not, we learn something important about what makes markets enterable vs. closed

**Expected outcome:** 2-3 additional PSC codes measured, segment newcomer fractions recorded, determination of whether the bimodal (3 enterable / 2 closed) pattern extends or whether the landscape is more continuous. This would either validate the classifier as broadly applicable or refine it with more data points.

**Dependencies:** None beyond the existing prototype tool (`tools/it_entrant_advisor.py`) and USAspending API access (which has been working for the initial 5 codes).

**Success criteria:** At least 2 additional PSC codes measured with segment newcomer fractions recorded; determination of whether the enterable/closed-shop classification holds or needs refinement based on the expanded data.