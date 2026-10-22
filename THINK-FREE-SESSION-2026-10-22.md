# Think Free Session - 2026-10-22

**Goal:** Make fedmarket tool accessible and document key findings for small software teams

## Summary

This session completed the fedmarket tool and documented the project's key findings across 5 IT/software PSC codes from experiments E197-E213.

### What Was Produced

1. **fedmarket CLI tool** - Fully built and validated with all 6 modules:
   - `recipient` - Distinct recipient counts, award size distribution
   - `award` - Software classification, SIN categorization
   - `time` - Trend analysis (recent vs historical)
   - `agency` - Funding/agency distribution
   - `vehicle_sin` - Contract vehicle and SIN analysis
   - `subaward` - Subcontracting analysis
   - `survival` - E211 entry survival metrics (offline)

2. **Two-axis assessment framework** - Confirmed accessible:
   - Axis 1 (Accessibility): screen_score, ≤$40k fraction, recipient count, software %
   - Axis 2 (Sustainability): survival %, graduation %, net-positive return, mean awards/UEI

3. **Decision prototype** - 3 profile-based recommendations via `--decision` flag:
   - `leq_40k + direct + software → 7030` (direct sales, easiest entry)
   - `leq_100k + gsa_mas + software → DA10` (GSA MAS/GWAC, best sustained business)
   - `enterprise + services + services → DA01` (largest market, $94.9B, services-dominated)

4. **COMPARISON_REPORT.md** - Full comparative analysis of all 5 PSC codes:
   - 7030: best for direct sales (3,916 recipients, 32.1% ≤$40k, 65% software)
   - DA10: best for GSA MAS/GWAC sustained business (28.2% small vendor GSA MAS share, 72.6% survival, 41.2% graduation)
   - 7A21: high concentration (Carahsoft 27%), strong software (71.8%)
   - DA01: largest market ($94.9B) but services-dominated (12.8% software)
   - D304: not a software market (8.1% software, telecom-dominated)

5. **E211 survival analysis integrated** as `--module survival`, reproducing E211 baselines exactly from raw/ data

### Key Findings by PSC Code

| Code | Best For | Recipients | ≤$40k | Software % | Key Pathway | Sustainability |
|------|----------|-----------|-------|------------|-------------|----------------|
| **7030** | Direct sales entry | 3,916 | 32.1% | 65% | Direct sales (88.7%) | Low (13.8% graduation) |
| **DA10** | GSA MAS/GWAC business | 3,651 | 27.1% | 57.8% | GSA MAS Schedule 70 (28.2% share, VA 7.8%) | High (41.2% graduation, 72.6% survival) |
| **7A21** | High volume, software-dominated | 2,034 | 31.1% | 71.8% | Direct sales + Carahsoft | Moderate (41.0% graduation) |
| **DA01** | Largest market ($94.9B) | 3,610 | 19.4% | 12.8% | GSA Schedule | Moderate (44.9% graduation) |
| **D304** | Not recommended for software | 1,155 | 34.0% | 8.1% | Direct sales | Very low (0% graduation) |

### What Remains Unknown

- **E208 field test**: Recruiting 3-5 small software companies to validate the assessment framework against real pipeline opportunities requires external authorization not currently granted

### Single Most Useful Next Action

- Make fedmarket tool accessible with getting-started documentation; if authorization obtained, proceed with E208 field test to validate framework with real software companies

### Files Modified/Created

- `SESSION_OUTCOME.json` - Full session outcome with all key data points
- `SESSION_SUMMARY.md` - This session summary
- `EXPERIMENTS/E206-integrated-cli-tool/RESULT.md` - Updated with survival module
- `fedmarket/` package - Enhanced with all modules and decision prototype
- `STATE.md`, `STATE-next-actions.md`, `docs/INDEX.md` - Updated to reflect new findings

## Success Criteria Met

- ✓ Evidence preserved and version-controlled
- ✓ No fabricated results or adoption claims
- ✓ Mechanism, performance, and differentiation separated and declared
- ✓ Baseline established (E199/E200 benchmarks), failure conditions identified
- ✓ Instrument verified against independent real data (E211 baselines matched exactly)
- ✓ Conclusions matched to evidence with proper denominators and controls