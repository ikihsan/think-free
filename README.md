# fedmarket — Federal Marketplace Assessment Toolkit

> **Evidence-backed PSC code analysis for small software teams entering the US federal market**

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-alpha-orange.svg)]()

---

## What is this?

**fedmarket** helps small software teams (1-10 people) answer a critical question: **"Which federal PSC code should we target, and how do we enter?"**

It's built on **20+ experiments (E196-E213)** analyzing **$203.32B** in federal IT/software spending across 5 PSC codes, using live USAspending.gov data. Every metric carries an evidence label: **[Observed]**, **[Inferred]**, or **[Speculative]**.

## The Core Insight: Two Axes, Different Winners

| Axis | What it measures | Winner | Why |
|------|------------------|--------|-----|
| **Accessibility** (Axis 1) | How easy to win first contract? | **7030** | 32% of awards ≤$40k, 3,916 recipients, direct sales |
| **Sustainability** (Axis 2) | Do recipients return & grow? | **DA10** | 23.7% graduation rate, GSA MAS pathway, VA channel |

**There is no single "best" code** — the right choice depends on your team's profile.

---

## Quick Start

```bash
# Install
pip install fedmarket

# Assess a PSC code
fedmarket assess 7030

# Compare codes
fedmarket compare 7030 DA10 7A21

# Get a recommendation for your team
fedmarket decide --budget leq_40k --gtm direct --focus software

# Or interactively
fedmarket decide --interactive
```

---

## Commands

### `fedmarket assess <CODE> [CODE...]`
Assess one or more PSC codes with full metrics.

```bash
fedmarket assess 7030                    # Single code, detailed view
fedmarket assess 7030 DA10               # Multiple codes, comparison table
fedmarket assess 7030 --refresh          # Fetch live data from USAspending
fedmarket assess 7030 -o results.json    # Save JSON output
```

**Output includes:**
- Screen metrics (recipients, concentration, award size distribution)
- Software market fit (% software awards, median software award)
- Trend analysis (E204: concentrating/diversifying/hardening)
- Sustainability (E211: survival %, graduation %)
- Contract vehicle access (GSA MAS, SEWP, subcontracting)
- Entry strategy recommendation

### `fedmarket compare <CODE> [CODE...]`
Side-by-side comparison table.

```bash
fedmarket compare 7030 DA10 7A21 DA01 D304
```

### `fedmarket decide`
Profile-based recommendation using the two-axis framework.

```bash
# Non-interactive (CI/CD friendly)
fedmarket decide --budget leq_40k --gtm direct --focus software
fedmarket decide --budget leq_100k --gtm gsa_mas --focus saas
fedmarket decide --budget enterprise --gtm subcontract --focus services

# Interactive
fedmarket decide --interactive
```

**Budget options:** `leq_40k` | `leq_100k` | `enterprise`  
**GTM options:** `direct` | `gsa_mas` | `subcontract`  
**Focus options:** `software` | `saas` | `services`

### `fedmarket list-codes`
List all available PSC codes with basic info.

### `fedmarket version`
Show version and data provenance.

---

## The Five PSC Codes Analyzed

| Code | Name | Market Type | Best For | Key Metric |
|------|------|-------------|----------|------------|
| **7030** | IT Software | Software Product | Direct sales entry | 32.1% ≤$40k, 3,916 recipients |
| **DA10** | IT Services | Software Product + GWAC | Sustained business | 23.7% graduation, GSA MAS 37% |
| **7A21** | IT HW/SW | Software Product (Concentrated) | Subcontract only | Carahsoft 27% concentration |
| **DA01** | IT Mgmt | Services Market | Services firms | $94.9B but 12.8% software |
| **D304** | Telecom | Telecom Market | Avoid for software | 8.1% software |

---

## Two-Axis Framework

### Axis 1: Entry Accessibility
- Screen score (recipient count × concentration)
- ≤$40k award fraction
- Software award percentage
- **Higher = easier entry**

### Axis 2: Business Sustainability
- Survival rate (UEI match, 3-year follow-up)
- Graduation rate (> $100k aggregate)
- **Higher = better long-term business**

### The Tradeoff
- **7030**: Maximizes Axis 1 (easy entry), minimizes Axis 2 (median returner $2,000/3yr)
- **DA10**: Balanced Axis 1 + strong Axis 2 (graduation 23.7%)
- **DA01/7A21**: Strong Axis 2 but entry challenges (concentration or services-dominated)

---

## Evidence Provenance

Every number in fedmarket is traceable to a specific experiment:

| Experiment | What it measured | Key finding |
|------------|------------------|-------------|
| **E196** | Federal spend by PSC code | $203.32B in 5 IT/software codes |
| **E197** | Funded award count validation | 98.6% of awards carry money |
| **E198** | Recipient landscape | 9,977 distinct companies |
| **E199** | Candidate screen | 7030 best balance (score 2,411) |
| **E200** | 7030 prototype validation | Confirmed screen prediction |
| **E201** | 7030 MVP | 3,916 recipients, 100% single-award |
| **E202** | CLI tool v1 | Reproduces baselines within 0.1pp |
| **E203** | Award categorization | 7030: 64.5% software, 41.4% ≤$40k |
| **E204** | Time-window trends | 7030 concentrating, DA10 diversifying |
| **E205** | Agency distribution | DA10: VA 19.4%, GSA 7.8% awarding |
| **E206** | Integrated CLI | All 5 modules validated |
| **E207** | Contract vehicles | DA10: 28.2% small vendor GWAC |
| **E209** | Subcontracting | DA10: 8.1% sub/prime |
| **E210** | GSA MAS SIN/SEWP | DA10: 28% in software SINs |
| **E211** | Entry survival | DA10: 23.7% graduation (cleaned) |
| **E213** | SIN validation | E210 heuristic falsified; DA10 confirmed |

**Full evidence:** See `EXPERIMENTS/` directory in the repository.

---

## Evidence Labels

Per [`docs/policy/evidence-labels.md`](docs/policy/evidence-labels.md):

- **[Observed]** — Directly measured from USAspending API responses
- **[Inferred]** — Derived from observed data with stated assumptions
- **[Speculative]** — Not directly measured; based on reasoning or incomplete evidence

*No metric is presented without a label.*

---

## Installation

```bash
# From PyPI (when published)
pip install fedmarket

# From source
git clone https://github.com/think-free/fedmarket
cd fedmarket
pip install -e .

# With development dependencies
pip install -e ".[dev]"
```

**Requirements:** Python 3.10+, httpx, rich, typer

---

## Usage as a Library

```python
from fedmarket import assess_code, compare_codes, decide_code

# Assess a single code
result = assess_code("7030")
print(result["screen_score"])           # 2411
print(result["recommendation"]["entry_axis"])  # "direct_sales"

# Compare multiple codes
comparison = compare_codes(["7030", "DA10", "7A21"])
print(comparison["ranked_by_screen_score"])    # ['7030', 'DA10', '7A21', ...]

# Get profile-based recommendation
rec = decide_code("leq_40k", "direct", "software")
print(rec["recommended_code"])        # "7030"
print(rec["rationale"])
```

---

## Dynamic Mode (Live USAspending Data)

```bash
# Fetch fresh data (respects API rate limits, caches locally)
fedmarket assess 7030 --refresh
```

The dynamic module queries USAspending API endpoints:
- `/spending_by_category/recipient/`
- `/spending_by_award/`
- `/spending_by_category/funding_agency/`
- `/spending_by_category/awarding_agency/`
- `/spending_by_category/federal_account/`
- `/subawards/`

Results are cached in `~/.cache/fedmarket/` with provenance tracking.

---

## Limitations & Caveats

1. **USAspending API ceiling**: 500 pages (5,000 awards) per query
2. **SIN-level metrics are heuristic**: E213 falsified E210's affinity scores for 7030/7A21/DA01
3. **Small vendor definition**: Single-award recipients in sample (may not capture all small businesses)
4. **No GSA eLibrary/SEWP catalog access**: Validated against USAspending ground truth only
5. **Static survival data**: E211 cohort is FY2020-21 entrants tracked through FY2023-25
6. **No field validation yet**: E208 (field test with real companies) is planned but not executed

---

## Project Structure

```
fedmarket/
├── pyproject.toml          # Package config
├── fedmarket/
│   ├── __init__.py         # Public API
│   ├── core.py             # Static lookup data + assessment
│   ├── dynamic.py          # USAspending API client
│   ├── decision.py         # Two-axis recommendation engine
│   ├── cli.py              # Typer CLI commands
│   └── __main__.py         # python -m fedmarket entry
├── tests/                  # Test suite
└── README.md               # This file
```

---

## Contributing

This is an independent invention project. See `AGENTS.md` for the agent contract and `MISSION.md` for the objective.

### Development

```bash
# Run tests
pytest

# Lint
ruff check .

# Type check (if mypy configured)
mypy fedmarket/
```

---

## License

MIT License — see `LICENSE` file.

---

## Disclaimer

**This is a reversible exploratory prototype.** It packages pre-computed analysis from experiments E196-E213 into an importable API without claiming new algorithms or real-world validation. Results are grounded in observed USAspending data with clear provenance.

**Not financial, legal, or contracting advice.** Consult qualified professionals before making business decisions based on this tool.

---

## Acknowledgments

Data sourced from [USAspending.gov](https://www.usaspending.gov/) — the official open data source for federal spending.

Experiments conducted under the Think Free independent invention mission (2026-10-03 onward).