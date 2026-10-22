## Session 2026-10-22-008 — Enhanced Decision Prototype

### What was produced

**`decision.py`** — A standalone Python script implementing the two-axis framework (entry accessibility vs. business sustainability) for federal software marketplace PSC code recommendation.

- 332 lines, standalone script (no package imports required beyond `fedmarket.data`)
- Takes 3 command-line args: `BUDGET GTM FOCUS`
- Returns PSC code recommendation with full metrics, caveats, and two-axis scores
- Integrates E211 entry survival/graduation data from raw experiment results
- Includes E204 time-window concentration trend warnings in caveats
- Provides profile-matched assessment for 3 recognized profiles, fallback assessment for others

### Key recommendations verified (all 3 profile combinations)

| Profile | Recommended Code | Entry Axis | Business Score | Key Metric |
|---|---|---|---|---|
| `leq_40k + direct + software` | **7030** | direct_sales | 25.5 (low sustainability) | 3,916 recipients, 32.1% ≤$40k |
| `leq_100k + gsa_mas + software` | **DA10** | gwac_pathway | 41.4 (good sustainability) | 28.2% GSA MAS share, VA channel 7.8% |
| `enterprise + services + services` | **DA01** | services_market | 41.3 (good sustainability) | $94.9B market, 12.8% software |

### Build decision change

Created new `decision.py` script as a **reversible exploratory prototype** that packages pre-computed analysis from experiments E202-E213 (2026-10-20/21) without claiming new algorithms or real-world validation. Grounded in observed USAspending data with clear provenance. Two-axis mode combines:
- **Axis 1 (accessibility)**: screen score (40%), ≤$40k fraction (30%), software % (30%)
- **Axis 2 (sustainability)**: survival % (40%), graduation % (30%) from E211

### What remains unknown

1. Whether small teams will find the tool usable in practice
2. E211 data path reliability across different deployment environments
3. Real-world user validation (would require E208 field test with 3-5 small software companies — requires authorization)

### Single most useful next action

**Make decision.py more accessible**: Add `--json` flag for machine-readable output, and verify the E211 data path works reliably when the script is deployed outside the current working directory. This lowers the barrier for small teams to use the two-axis framework and enables the assessment framework for E208 field tests.

### Evidence labels (per docs/policy/evidence-labels.md)

- **Observed**: All API responses, computed metrics, JSON outputs from experiment runs
- **Source-supported**: Metrics from E197-E213 experiments, USAspending ground truth
- **Inferred**: Trend stability (limited by 5,000-award sample ceiling), SIN/category classification from description keywords
- **Speculative**: Affinity scores, subcontractor flow percentages, GSA eLibrary validation needs
- **Untested**: Real-world team usability, field-test validation outcomes