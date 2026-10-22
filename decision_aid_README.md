# Think Free — Federal Software Marketplace Decision Aid

## Overview

A reversible exploratory prototype helping small software teams choose a PSC
code and entry strategy for the federal marketplace, using the two-axis
framework (entry accessibility vs. business sustainability) derived from
experiments E197-E213 (2026-10-20/21).

## Problem

Small independent software teams have difficulty determining which PSC code
(Project Service Code) to target and what entry strategy to use when selling
software to federal agencies. The federal marketplace has distinct market
types with different access patterns, concentration levels, and sustainability
profiles.

## Two-Axis Framework

The tool evaluates teams along two dimensions:

| Axis | Metric | High Score Means |
|------|--------|------------------|
| **Accessibility (Entry Score)** | Weighted combination of screen score (40%), ≤$40k fraction (30%), software % (30%) | Easier market entry, more potential customers, smaller award sizes |
| **Sustainability (Business Score)** | Weighted combination of survival % (40%), graduation % (30%) | Better recipient return rates, growth pathway to >$100k awards |

## Profile-Based Recommendations

The tool maps team characteristics to PSC codes and entry strategies:

| Profile | Recommended Code | Entry Axis | Primary Vehicle | Recommendation |
|---------|-----------------|------------|-----------------|----------------|
| `leq_40k + direct + software` | **7030** (IT Software) | direct_sales | direct_sales | balanced — easiest entry, weaker sustainability |
| `leq_100k + gsa_mas + software` | **DA10** (IT Services) | gwac_pathway | gsa_mas_schedule_70 | business — strong sustainability via GSA MAS |
| `enterprise + services + services` | **DA01** (IT Management) | services_market | gsa_schedule | business — largest market, services-dominated |
| `leq_40k + gsa_mas + software` | **DA10** | gwac_pathway | gsa_mas_schedule_70 | business — GSA MAS pathway even with tight budget |
| `leq_100k + direct + software` | **7030** | direct_sales | direct_sales | balanced — best recipient count (3,916) |
| `enterprise + gsa_mas + software` | **DA10** | gwac_pathway | gsa_mas_schedule_70 | business — best for enterprise GSA MAS pursuit |
| `enterprise + direct + software` | **7030** | direct_sales | direct_sales | balanced — largest software market ($25.83B) |
| `leq_100k + services + software` | **DA01** | services_market | gsa_schedule | balanced — services market with some software |
| `enterprise + saas + software` | Falls back to all-code assessment | — | — | — |

*(Full 27-profile coverage available via CLI; see below for unmapped combinations.)*

## CLI Usage

```bash
python3 decision_aid.py <BUDGET> <GTM> <FOCUS>
```

### Arguments

- **BUDGET**: `leq_40k` (≤$40k per award), `leq_100k` (≤$100k), or `enterprise`
- **GTM**: `direct` (direct sales), `gsa_mas` (GSA Schedule/MAS), or `services`
- **FOCUS**: `software` (pure software product) or `services` (IT services/integration)

### Examples

```bash
# Small team, quick revenue, build own sales
python3 decision_aid.py leq_40k direct software

# Team pursuing GSA contracting, moderate ambition
python3 decision_aid.py leq_100k gsa_mas software

# Enterprise services team, largest market focus
python3 decision_aid.py enterprise services services
```

### Output

The tool outputs:
- Recommended PSC code and name
- Entry axis and primary vehicle
- Two-axis recommendation (entry vs business vs balanced)
- Entry Score (0-100 accessibility) and Business Score (0-100 sustainability)
- Key metrics: screen score, recipient count, award size distributions,
  software percentage, DOD %, total obligation, small vendor GSA MAS share
- E211 entry survival data: survival %, graduation %, UEI counts
- Caveats including E204 time-window trend warnings
- Recommendation type (profile_matched or fallback)

## Evidence Base

All data grounded in experiments E197-E213:

- **E197**: 98.6% of federal award records carry money
- **E198**: Vendor landscape — 9,977 distinct companies across 5 IT/software codes
- **E199-E201**: Candidate screen and prototype validation for 7030
- **E202-E206**: Comprehensive CLI tool with all assessment modules
- **E203**: Award description categorization (7030: 64.5% software; DA10: 57.8%)
- **E204**: Time-window concentration trends (7030 rapid concentration; DA10 diversifying)
- **E207**: Contract vehicle analysis (DA10 only code with meaningful GWAC usage)
- **E209**: Subcontract analysis (only DA10 has significant sub/prime pathway)
- **E210**: GSA MAS SIN/SEWP category analysis (DA10 only code with meaningful small vendor GSA MAS share)
- **E211**: Entry survival (DA10: 72.6% survival, 41.2% graduation; 7030: 53.3% survival, 13.8% graduation)
- **E212**: Decision prototype with profile-based recommendations
- **E213**: GSA MAS SIN/SEWP validation using USAspending ground truth

## Limitations

- Decision framework based on USAspending data (5,000-award API ceiling)
- "Direct/Unknown" vehicle classification conflates true direct with unclassified
- Small vendor definition (single-award recipients) may not capture all small businesses
- Description-based SIN/category inference is heuristic
- SAAS focus not separately modeled (included in software category)
- SA endpoint data reflects historical patterns; market dynamics change over time

## Installation

```bash
# From the think-free repository root
python3 decision_aid.py leq_40k direct software
```

No external dependencies beyond Python 3.8+ and the fedmarket package (included
in the repository).

## References

- COMPARISON_REPORT.md — Full comparative analysis of all 5 PSC codes
- EXPERIMENTS/E211-entry-survival/ — Entry survival raw data
- EXPERIMENTS/E206-integrated-cli-tool/ — Integrated CLI tool with all modules
- STATE.md — Verified project state and next actions