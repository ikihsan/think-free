# Federal Marketplace Assessor Prototype

**File**: `assess.py` (new, untracked)

A runnable Python prototype providing one-command PSC code market assessments for small software teams entering the federal marketplace. Uses pre-cached E206 experiment data for instant results without API calls.

## Usage

```bash
python3 assess.py 7030                    # Assess PSC code 7030
python3 assess.py DA10 --output report.txt  # Save to file
```

## Output Example (7030)

```
FEDERAL MARKETPLACE ASSESSMENT: PSC Code 7030

Screen Score: 2411.1  (Rank: #1 of 5)
Verdict: PROCEED — Best overall for direct sales

SMALL-TEAM ENTRY METRICS
  Recipients: 3,916
  Top-10 concentration: 38.4%
  ≤ $40k: 32.1%  |  ≤ $100k: 46.8%
  Single-award recipients: 100.0%

SOFTWARE MARKET FIT
  Software awards: 63.0% of count
  Software ≤ $40k: 36.5%  |  Software ≤ $100k: 63.0%

ENTRY PATHWAYS
  GSA MAS small vendor share: 5.9% in 511210 (Software); GSA Schedule channel: 2.1% awarding
  Top vehicles: N/A
  GSA MAS small vendor shares: N/A

RECOMMENDED ENTRY STRATEGY
  Direct sales to 3,916 recipients (32% ≤ $40k). Subcontract to Carahsoft/DLT/CDW.
```

## Validated Across PSC Codes

| Code | Verdict | Key Metric |
|------|---------|------------|
| **7030** | PROCEED | Best for direct sales: 3,916 recipients, 32.1% ≤ $40k |
| **DA10** | PROCEED | Best for GSA Schedule/GWAC: 28% small vendor GSA MAS share |
| 7A21 | CAUTION | Carahsoft-dominated, subcontract only |
| DA01 | CAUTION | Largest market but services-dominated |
| D304 | DEPRIORITIZE | Not a software market |

## Data Source

Uses pre-cached E206 experiment data (`test_7030.json`, `test_DA10.json`) from prior experiments E197-E211. No API calls required — instant results.

## What This Prototype Advances

- **Concrete problem**: Small software teams have no easy way to assess federal marketplace opportunities
- **Built on 20+ experiments**: E197-E211 analyzing 5 IT/software PSC codes via USAspending API
- **Accessible format**: Distills complex analysis into a one-page report
- **Prototype, not product**: Evidence-gathering prototype; iterable based on feedback

## Next Actions

1. **Generate complete cached data**: Run `E206 CLI` with all 5 modules to expand assessor coverage
2. **E208 field test**: Recruit 3-5 small software companies to validate assessment framework against real pipeline opportunities