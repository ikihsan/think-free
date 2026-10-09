# Experiment 079: Automotive OBD2 Diagnostic Codes Fresh Observation

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-09
-->

Fresh observation in the automotive OBD2 diagnostic codes domain to discover whether a concentrated, structured problem population exists that could support a computational tool.

## Documents

| Document | Purpose |
|---|---|
| [`PROTOCOL.md`](PROTOCOL.md) | Predeclared protocol with kill gates |
| [`CLASSIFICATION_RULES.md`](CLASSIFICATION_RULES.md) | Classification criteria for root cause specificity |
| [`fetch.py`](fetch.py) | Data acquisition from Mechanics Stack Exchange API (full version) |
| [`fetch_test.py`](fetch_test.py) | Small test fetch (blocked by API throttle) |
| [`fetch_candidates.py`](fetch_candidates.py) | Candidate-only fetch (blocked by API throttle) |
| [`analyze_preliminary.py`](analyze_preliminary.py) | Analysis on title+tag data only |
| [`raw/questions_raw.json`](raw/questions_raw.json) | 10,251 questions with titles/tags (exempt from line cap) |
| [`analysis/preliminary_gate_results.json`](analysis/preliminary_gate_results.json) | Machine-readable gate results |
| [`analysis/title_candidates.json`](analysis/title_candidates.json) | 210 title candidates (exempt from line cap) |
| [`VERDICT.md`](VERDICT.md) | Gate evaluation results and decision |

## Status

**PARTIAL — G2 FAIL (29% vs 30%), G3 PASS (30 vehicle configs), G1/G4 blocked by API throttle, G5 pending.**

## Hypothesis

Automotive OBD2 diagnostic trouble codes (DTCs) on specific vehicles form a concentrated, structured problem population where:
1. Standardized codes (P0xxx, P1xxx, etc.) appear repeatedly across vehicles
2. Professional technicians diagnose root causes with specific replaceable parts
3. Existing free tools don't provide vehicle-specific root cause mappings
4. A computational tool mapping (code + vehicle) → (root cause + repair) would fill a gap

## Kill Gates (Predeclared)

| Gate | Threshold | Result |
|------|-----------|--------|
| G1 Population | ≥ 200 structured cases | PENDING (blocked) |
| G2 Code concentration | Top 10 codes cover ≥ 30% of cases | **FAIL** (29.0%) |
| G3 Vehicle coverage | ≥ 15 distinct vehicle configs in top 10 codes | **PASS** (30) |
| G4 Root cause specificity | ≥ 60% name specific replaceable part | PENDING (blocked) |
| G5 Incumbent gap | No free tool covers ≥ 50% of top 10 codes | PENDING (manual) |

## Key Blocker

**Stack Exchange API throttle (300 req/day per IP)** prevented fetching question bodies and answers for the 210 title candidates. Without answer data, G1 (structured case count) and G4 (root cause specificity) cannot be evaluated.

## Preliminary Findings

- **210 questions** with OBD2 codes in title (from 10,251 Mechanics.SE questions)
- **262 code mentions** across **159 unique codes** — high dispersion
- **Top 10 codes**: P0420 (18), P0171 (15), P0300 (12), P0302/P0430/P0304 (5 each)
- **25 makes represented**, 30 vehicle configs for top 10 codes
- **128/210 candidates** marked as answered (from metadata)

## Conclusion

Candidate does not survive on current evidence. G2 failed by 1 percentage point; G1/G4 blocked; long-tail distribution (159 codes/262 mentions) suggests fundamental dispersion. Path forward would require API key or data dump, but concentration is marginal.

## Reproduce

```bash
# Preliminary analysis (title+tags only, no API calls)
python3 analyze_preliminary.py

# Full fetch (requires API key or waiting for throttle reset)
python3 fetch_candidates.py
python3 analyze.py
```