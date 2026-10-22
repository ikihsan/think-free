# fedmarket — Federal Marketplace Assessment Toolkit

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-22
-->

**Assess IT/software PSC codes in USAspending for small-team entry opportunities.**

Data grounded in experiments E202–E211 (2026-10-20/21); see `EXPERIMENTS/` for raw results.

This is a **REVERSIBLE EXPLORATORY PROTOTYPE**: it packages pre-computed analysis from the E206 integrated CLI tool into an importable CLI without claiming new algorithms or real-world validation. Results are grounded in observed USAspending data with clear provenance. Two-axis mode combines accessibility metrics (screen score, award size distribution) with sustainability metrics (survival, graduation) from E211 entry survival analysis.

Live modes (`recipient`, `award`, `time`, `agency`, `vehicle_sin`, `subaward`) query the USAspending API at run time; the `--survival` mode is fully offline from the `raw/` data bundled with the package.

Decision mode (`fedmarket-decide`): helps small software teams apply the two-axis framework (entry accessibility vs. business sustainability) to choose a PSC code and entry strategy matched to their characteristics. Interactive by default; fully scripted with `--budget/--gtm/--focus [--json]`.

## Installation

This package is **not published to PyPI** and has no public repository yet.
Install from a checkout of this repository:

```bash
cd fedmarket
pip install .
# or, for development:
pip install -e .
```

Build a wheel:

```bash
pip wheel --no-deps -w dist .
```

Run the tests:

```bash
python3 -m pytest tests/
```

## Quick Start

```bash
# Assess a single PSC code (queries the live USAspending API)
fedmarket --code 7030

# Save results to JSON
fedmarket --code DA10 --output da10.json

# Run specific modules only
fedmarket --code 7030 --modules recipient,award

# Offline entry-survival analysis (bundled raw data; no network)
fedmarket --code 7030 --survival
fedmarket --code DA10 --survival --output da10-survival.json

# Decision guide — interactive
fedmarket-decide

# Decision guide — scripted (for tests, scripts, CI)
fedmarket-decide --budget leq_40k --gtm direct --focus software
fedmarket-decide --budget leq_100k --gtm gsa_mas --focus saas --json
```

## PSC Codes Analyzed

| Code | Name | Screen Score | Software % | ≤$40k | Best For |
|------|------|-------------|------------|-------|----------|
| **7030** | IT Software | 2,411 | 64.5% | 32.1% | **Direct sales** — easiest entry, 3,916 recipients |
| **DA10** | IT Services | 2,345 | 57.8% | 27.1% | **GSA MAS pathway** — best sustainability (41.2% graduation) |
| **7A21** | IT HW/SW | 2,034 | 71.8% | 31.1% | Niche only — Carahsoft 27% concentration |
| **DA01** | IT Mgmt | 2,363 | 12.8% | 19.4% | Services firms — not a software product market |
| **D304** | Telecom | 490 | 8.1% | 34.0% | Avoid for software products |

## Two-Axis Framework

The tool evaluates PSC codes on two independent axes:

### Axis 1: Entry Accessibility
- **Screen score**: recipient count × (1 − top-10 concentration)
- **Small-award fraction**: % of awards ≤ $40k / ≤ $100k
- **Recipient count**: distinct organizations receiving awards
- **Software market fit**: % of awards classified as software

**Winner: 7030** — 3,916 recipients, 32.1% ≤ $40k, 64.5% software

### Axis 2: Business Sustainability (E211 Entry Survival)
- **Survival**: % of ≤$100k FY20–21 recipients returning in FY23–25 (UEI match)
- **Graduation**: % of returning recipients exceeding $100k aggregate
- **Net-positive return**: % with >$0 aggregate in return window

| Code | Survival | Graduation (cleaned) | Median Returner Aggregate |
|------|----------|---------------------|---------------------------|
| **DA10** | **72.6%** | **23.7%** | $176,030 |
| DA01 | 69.6% | 24.2% | $361,559 |
| 7A21 | 43.1% | ~24% | — |
| **7030** | 53.3% | **1.2%** | **$2,000** |

**Winner: DA10** — strongest sustained business pathway

### Recommendation Matrix

| Team Profile | Best Code | Primary Vehicle | Key Tradeoff |
|--------------|-----------|-----------------|--------------|
| ≤$40k, Direct, Software | **7030** | Direct Sales | Lowest sustainability (1.2% graduation) |
| ≤$100k, GSA MAS, Software | **DA10** | GSA MAS 511210/511210S/518210C | Best sustained business (23.7% graduation) |
| Enterprise, Services | **DA01** | GSA Schedule 54151S | Not a software product market |
| Subcontract, Any | **DA10** | Sub to Peraton/Highlight | 8.1% sub/prime ratio |

## Modules

| Module | Experiment | Description |
|--------|------------|-------------|
| `recipient` | E202 | Recipient analysis: screen score, award distribution, concentration |
| `award` | E203 | Award categorization: software/service/hardware/telecom split |
| `time` | E204 | Time-window comparison: recent 12mo vs FY20–25 |
| `agency` | E205 | Agency distribution: funding/awarding agencies, federal accounts |
| `vehicle_sin` | E210 | GSA MAS SIN & SEWP category analysis for small vendor entry |
| `subaward` | E209+ | Prime-specific subaward trace (Carahsoft, Dell, Leidos, Accenture) |
| `survival` | E211 | Entry survival & graduation rates from award-level UEI matching |

## Output

JSON output includes all module results with clear provenance:

```json
{
  "experiment": "E206",
  "psc_code": "7030",
  "modules_run": ["recipient", "award", "time", "agency", "vehicle_sin"],
  "recipient": { ... },
  "award_categorization": { ... },
  "full_period": { ... },
  "recent_period": { ... },
  "funding_agencies": [ ... ],
  "awarding_agencies": [ ... ],
  "federal_accounts": [ ... ],
  "recipient_stats": { ... },
  "vehicle_sin": { ... },
  "survival": { ... }
}
```

## Evidence Labels

All results carry evidence labels:
- **Observed**: Directly from USAspending API responses
- **Inferred**: Derived from observed data (e.g., trend stability limited by API ceiling)
- **Speculative**: Heuristic estimates (e.g., SIN/category affinity scores)

## Limitations

1. USAspending API 500-page limit caps award fetches at 5,000 per query
2. Time-window comparison limited by API pagination ceiling
3. "Direct/Unknown" vehicle classification conflates true direct awards with unclassified vehicles
4. Small vendor definition (single-award recipients) may not capture all small businesses
5. Description-based SIN/category inference is heuristic; actual holdings require GSA eLibrary/SEWP catalog cross-reference
6. DA01/D304 are not software markets (per E203); their high service SIN shares reflect services labor

## Validation

All screen metrics reproduce E199/E200 baselines within 0.1 percentage points.
Survival module reproduces E211 baselines exactly (7030: 53.3%/13.8%, DA10: 72.6%/41.2%, DA01: 69.6%/44.9%).

## License

MIT License — see LICENSE file.

## Related Experiments

- `EXPERIMENTS/E206-integrated-cli-tool/` — Integrated CLI tool validation
- `EXPERIMENTS/E207-contract-vehicle-analysis/` — Contract vehicle analysis
- `EXPERIMENTS/E209-subcontract-analysis/` — Subcontract analysis
- `EXPERIMENTS/E210-vehicle-sin-sewp-analysis/` — GSA MAS SIN/SEWP analysis
- `EXPERIMENTS/E211-entry-survival/` — Entry survival analysis
- `EXPERIMENTS/E213-sin-sewp-validation/` — SIN/SEWP validation against USAspending ground truth