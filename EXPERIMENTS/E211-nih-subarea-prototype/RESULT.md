<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-21
-->

# Experiment E211: NIH SBIR Sub-Area Accessibility Prototype

**Date:** 2026-10-21. **Session:** 2026-10-21-011.  
**Tool:** `nih_subarea_prototype.py` (prototype, reads committed E210 raw data)  
**Status:** Complete — all success criteria verified. Prototype reads from disk only; no network dependency for analysis.

## What was tested

E210 measured NIH SBIR spending category 176 sub-areas (Funding Institutes/Centers) and ranked them by accessibility for small programs. The **E211 prototype** builds on this by providing a reusable CLI tool that:

1. Reads the committed E210 analysis data from disk (no API calls needed)
2. Ranks all 17 Funding Institutes/Centers by `access_score` (higher = more accessible)
3. Identifies the top-3 most accessible sub-areas
4. Provides cross-category comparison data (from E210's `cross_category_comparison`)
5. Outputs a formatted summary suitable for small program decision-making

This is an evidence-gathering prototype, not product validation.

## Prototype design

- Reads from `EXPERIMENTS/E210-sbir-category176-subsegment/raw/analysis.json`
- CLI tool: `python3 nih_subarea_prototype.py`
- No network dependency for analysis step (reads only from committed raw data)
- Mirrors E210's reproducibility model

## Per-IC ranking (access_score = higher is better)

| IC | Projects | Distinct Orgs | Top-5% | Access Score | Total Amount |
|---|---|---|---|---|---|
| National Institute of Mental Health | 12 | 9 | 80.1% | 14.97 | $5,180,041 |
| National Cancer Institute | 7 | 7 | 94.4% | 7.41 | $4,079,729 |
| National Institute on Minority Health and Health Disparities | 5 | 2 | 100.0% | 5.00 | $1,908,311 |
| National Institute on Aging | 4 | 4 | 100.0% | 4.00 | $2,838,207 |
| National Institute on Drug Abuse | 4 | 3 | 100.0% | 4.00 | $790,080 |
| National Institute of Allergy and Infectious Diseases | 4 | 4 | 100.0% | 4.00 | $2,921,989 |
| National Heart Lung and Blood Institute | 3 | 3 | 100.0% | 3.00 | $1,721,978 |
| Eunice Kennedy Shriver National Institute of Child Health and Human Development | 3 | 3 | 100.0% | 3.00 | $909,553 |
| National Human Genome Research Institute | 2 | 2 | 100.0% | 2.00 | $454,948 |
| National Center for Advancing Translational Sciences | 2 | 2 | 100.0% | 2.00 | $1,124,234 |
| National Institute of Dental and Craniofacial Research | 1 | 1 | 100.0% | 1.00 | $419,346 |
| National Eye Institute | 1 | 1 | 100.0% | 1.00 | $275,766 |
| National Institute of Diabetes and Digestive and Kidney Diseases | 1 | 1 | 100.0% | 1.00 | $865,222 |
| National Institute on Deafness and Other Communication Disorders | 1 | 1 | 100.0% | 1.00 | $998,469 |
| National Institute of Biomedical Imaging and Bioengineering | 1 | 1 | 100.0% | 1.00 | $250,310 |
| National Institute of General Medical Sciences | 1 | 1 | 100.0% | 1.00 | $831,399 |
| National Institute of Nursing Research | 1 | 1 | 100.0% | 1.00 | $221,912 |

## Top 3 most accessible sub-areas for small programs

1. **National Institute of Mental Health (NIMH)**: 12 projects, 9 distinct organizations, top-5 concentration 80.1%, access score 14.97 — *best entry point*
2. **National Cancer Institute (NCI)**: 7 projects, 7 distinct organizations, top-5 concentration 94.4%, access score 7.41 — *moderate entry point*
3. **National Institute on Minority Health and Health Disparities (NIMHD)**: 5 projects, 2 distinct organizations, top-5 concentration 100.0%, access score 5.00 — *limited but non-concentrated beyond a single organization*

## Cross-category comparison (access_score, higher = more accessible)

| Category | Top IC | Access Score | Top-5% Share | Grants (n) |
|---|---|---|---|---|
| 101 | NCI | 18.55 | 64.7% | 74 |
| 108 | NIAID | 58.73 | 47.7% | 76 |
| 176 | NIMH | 14.97 | 80.1% | 53 |
| 525 | NINDS | 25.54 | 54.8% | 49 |
| 701 | NIAID | 24.33 | 65.8% | 55 |

**Critical observation:** When the SBIR R41/R42 mechanism filter is applied, category 176 becomes the **least accessible** of the five consensus categories (access_score 14.97, top-5 share 80.1%), while category 108 becomes the **most accessible** (access_score 58.73, top-5 share 47.7%). This mechanism-dependent reversal underscores that accessibility is a property of *(instrument, population)*, not a property of the category alone.

## Key finding: mechanism-dependent accessibility

The same spending category can be highly accessible or minimally accessible depending on the NIH funding mechanism selected. When all NIH grants in category 176 are considered (unfiltered), it is the most accessible of the five consensus categories. When restricted to SBIR R41/R42 mechanisms only, it becomes the least accessible. Small programs selecting NIH SBIR topics should be aware that the accessibility profile depends critically on the funding mechanism.

Both the federal IT model (7030/small_technical: 1,130 contractors, 0.6% top-3 concentration, median $16.8K contracts) and the NIH SBIR model (category 176, NIMH: 12 projects, 9 orgs, 80.1% top-5 share, access_score 14.97) support a small program entering the market, but through different models: high-volume small contracts vs. moderate-size grants with broader organizational participation.

## Raw data and instrument

- [`raw/analysis.json`](raw/analysis.json) — deterministic; reads only files on disk
- Prototype script `nih_subarea_prototype.py` — reads only from `raw/analysis.json`
- G0–G4 not applicable (prototype, not a gated experiment); prototype is evidence-gathering

## Bound

One population (NIH SBIR cat 176, FY2023), one exposure (read committed data), one outcome (ranked IC list), one analysis window. The unit of every fraction is the **organization**, not the purchase. A recipient absent from 2018–2022 but present in 2014–2017 is counted a segment newcomer; the nine-year sensitivity is not run here.

## Success Criteria (all met)

- [x] Script runs end-to-end with default data
- [x] Reads from committed E210 raw data (no network needed)
- [x] Ranks all 17 ICs by access_score
- [x] Identifies top-3 most accessible sub-areas
- [x] Output table matches expected format
- [x] All raw data and analysis is reproducible from committed bytes on disk
- [x] No network dependency for the analysis step (reads only from raw/)

## Next experiment

**Fresh observation in a completely new domain axis per D083.** The view-count principle's domain of validity is now established across 8 domains (PyPI, NPM, NuGet, Discourse, Stack Exchange, GitHub repos, NIH SBIR, Crate.io), and the small-program accessibility pattern has been demonstrated in 3 domains (federal IT spending 7030/small_technical, NIH SBIR category 101 sub-segments, and NIH SBIR category 176 sub-segments with mechanism filter). Alternatively, a fresh observation using a different methodology or data source in a domain not yet covered by this repository's experiments.

**Do not run:** a re-run of the same candidate screen on unchanged data; a product build before prototype validation; or a candidate generation step before the measurement methodology is validated on fresh draws in a new domain.