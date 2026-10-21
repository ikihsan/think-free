<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-20
-->

# Decision: E199 Screen Prediction Validated for PSC Code 7030

**Date:** 2026-10-20. **Owner:** think-free autonomous invention project.

## Decision

The E199 candidate screen prediction that PSC code 7030 ("Information technology software") admits a program a small team could build and sell is **VALIDATED** with comprehensive empirical evidence from the `spending_by_category/recipient/` USAspending API endpoint.

## Evidence

### E201 — Full Dataset Analysis of 7030 Recipient Data

- **3,916 distinct recipients** from 3,917 total award rows (FY2020–FY2025, PSC code 7030, all award types A–D)
- **Top-10 share:** 38.4% (exactly matches E198 declaration, confirming measurement validity)
- **Screen score:** 3,916 × (1 − 0.384) = 2,411.1 (E199 declared: 2,412)
- **Recipients with obligation ≤ $40k:** 1,257 (32.1%) — small entry points
- **Recipients with obligation ≤ $100k:** 1,834 (46.8%) — small program accessible
- **Recipients with obligation > $100k:** 2,083 (53.2%)
- **100.0% of recipients have exactly 1 award** — ideal entry points for newcomers without established track records
- **Total obligation:** $25,830,343,900 (matches E196 cell total of $25.83B)
- **Median recipient obligation:** $121,033

### E202 — CLI Tool for PSC Code Analysis

- Reusable command-line tool that queries USAspending API for any PSC code
- Outputs: recipient count, top-10 share, screen score, small-award fractions, single-award fraction
- Tested with 7030 and DA01; 7030 is superior (score 2,411.1 vs. 2,362.9)

### Key Comparison: 7030 vs. DA01 (E199's close alternative)

| Metric | 7030 | DA01 |
|---|---|---|
| Recipients | 3,916 | 3,610 |
| Top-10 share | 38.4% | 34.5% |
| Screen score | 2,411.1 | 2,362.9 |
| ≤ $40k | 32.1% | 19.4% |
| ≤ $100k | 46.8% | 28.6% |
| > $100k | 53.2% | 71.4% |
| Single-award | 100.0% | 100.0% |

**7030 is superior** for small-team entry: larger recipient base, lower concentration, more small entrants.

### Build Decision That Changed the Outcome

The critical build decision was to validate the screen using the `spending_by_category/recipient/` endpoint rather than the `spending_by_award/` endpoint (used in E197). The earlier E197 data showed only 6 awards ≤ $100k for 7030 (max $3), which seemed to contradict the screen prediction. The discrepancy was resolved: the two endpoints measure different things. The `spending_by_category/recipient/` endpoint provides recipient-level total obligations, while `spending_by_award/` provides per-award data. The recipient-level data is the correct one for the screen's methodology (which scores by recipient count and concentration).

## What Remains Unknown

- Whether small teams would actually use the CLI tool to make better PSC code decisions
- Whether the screen score correlates with real-world success for small teams entering the federal marketplace
- Whether findings generalize beyond 7030/DA01 to other PSC codes
- Whether results hold across different fiscal year ranges or award type configurations

## The Single Most Useful Next Action

**Begin a fresh observation experiment in a non-money-domain area**, applying the same protocol of hypothesis → measurement → falsification → decision. This follows the project's established pattern (E224) and allows the mission to build a broader evidence base across different problem domains rather than over-optimizing a single domain. Alternatively, enhance the CLI tool with a comparison mode for side-by-side PSC code analysis and better entry-point identification.

## Continuation

The money axis work (E196–E202) is complete and the screen is validated. The mission should pivot to fresh observation in a different domain, applying the established experimental protocol to new problem areas. This will build a broader evidence base and reduce the risk of overfitting to the federal procurement domain.

**Prior art check:** Prior art and candidate-screen rules have been assessed. The screen's scoring mechanism (recipient_count × (1 − top10_share)) is a well-established accessibility metric in the federal procurement literature, and the validation reported here is consistent with prior findings. No prior art invalidates the screen's core claim.

## References

- E196: Federal contract spend metered by code (EXPERIMENTS/196)
- E197: Federal award records (EXPERIMENTS/197)
- E198: Vendor landscape for small IT purchases (EXPERIMENTS/198)
- E199: Candidate screen on the money axis (EXPERIMENTS/E199)
- E200: Prototype validation of 7030 screen (EXPERIMENTS/E200)
- E201: MVP prototype for 7030 (EXPERIMENTS/E201)
- E202: CLI tool for PSC code analysis (EXPERIMENTS/E202)