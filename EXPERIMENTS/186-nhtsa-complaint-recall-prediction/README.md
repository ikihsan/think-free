# Fresh Exploration: NHTSA Complaint-Recall Predictive Relationship

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-18
-->

## Hypothesis

**H0 (null):** Owner complaints submitted to NHTSA do not systematically precede recalls for the same vehicle component/category. The temporal pattern of complaints provides no predictive signal for future recalls.

**H1 (alternative):** Owner complaints on NHTSA contain early signals of issues that later become recalls. Complaints for a specific component category increase significantly before a recall is issued for that component, and this pattern is detectable across multiple vehicle models.

This tests whether a **predictive early-warning** need exists in automotive safety — a completely different need type from the "question answering" and "view-count principle" needs previously explored. The need is: *"Alert me to emerging safety issues for my vehicle before a recall is issued."*

## Domain Selection Rule (Stated Before Fetch)

Select a domain in the "consumer safety regulation" category that:
1. Has a public API requiring no authentication for both incident reports and regulatory actions
2. Has two distinct but related data streams: citizen reports (complaints) and official actions (recalls)
3. Has measurable temporal signals (dates on both streams)
4. Has not been tested by this mission
5. Is not a package registry, Q&A forum, fault code database, developer platform, model hub, encyclopedia, blogging platform, news aggregator, or view-count principle test domain

NHTSA satisfies all five: public APIs for both complaints and recalls (no auth), citizen complaints + manufacturer recalls with dates, temporal ordering measurable, not previously tested, distinct platform type (regulatory safety database).

## Prior Art Check

- NHTSA APIs: https://api.nhtsa.gov/ (public, no auth)
- ~400M+ vehicles in US fleet, ~2M+ complaints, ~50k+ recalls historically
- Academic work: "Predicting Vehicle Recalls from Complaint Data" (SAE papers, 2010-2020), NHTSA's own Early Warning Reporting (EWR) system uses manufacturer-submitted data (not public complaints)
- Commercial: CarFax, AutoCheck use recall data but not complaint trend analysis for prediction
- **Claimed difference:** Tests whether *public* complaint data (not manufacturer EWR data) has predictive signal for recalls, measured across multiple models/components with predeclared gates.

## Protocol

### Data Sources

- NHTSA Recalls API: `https://api.nhtsa.gov/recalls/recallsByVehicle?make={make}&model={model}&modelYear={year}`
- NHTSA Complaints API: `https://api.nhtsa.gov/complaints/complaintsByVehicle?make={make}&model={model}&modelYear={year}`

### Sampling

1. Select 20 vehicle model/year combinations with ≥1 recall in 2018-2024 (to ensure recall population exists)
2. For each, fetch all recalls and all complaints (max 1000 complaints per model/year via pagination)
3. Time range: complaints from 2015-2024, recalls from 2018-2024

### Classification (Pre-declared)

**Component Categories** (from NHTSA's component field taxonomy, mapped to 12 top-level categories):
1. FUEL SYSTEM
2. ELECTRICAL SYSTEM
3. ENGINE
4. TRANSMISSION
5. BRAKES
6. STEERING
7. SUSPENSION
8. AIR BAGS
9. SEAT BELTS
10. STRUCTURE/BODY
11. VISIBILITY (lights, wipers, windows)
12. OTHER

### Temporal Analysis

For each (model, year, component category) with ≥1 recall:
- **Recall date**: `ReportReceivedDate` of first recall in that category
- **Complaint window**: 730 days (2 years) before recall date
- **Baseline window**: 730 days before complaint window (4 years before recall)
- **Signal**: Complaint count in complaint window vs baseline window for same category

### Gates (Pre-declared)

| Gate | Condition | Threshold |
|------|-----------|-----------|
| **G1** (sample adequacy) | ≥ 10 model/year/category triples with ≥1 recall | 10 |
| **G2** (complaint volume) | ≥ 50 total complaints across sampled triples | 50 |
| **G3** (temporal signal) | Median complaint rate ratio (window/baseline) ≥ 2.0 for recalled categories | 2.0 |
| **G4** (specificity) | Non-recalled categories show ratio < 1.5 (no false signal) | 1.5 |
| **G5** (statistical) | Mann-Whitney U test: recalled vs non-recalled category ratios, p < 0.05 | p < 0.05 |

### Kill Conditions

- Any gate FAIL → predictive signal not established in this population
- G3 FAIL with p ≥ 0.05 → no evidence complaints precede recalls systematically
- G4 FAIL → signal not specific to recalled categories (false positives)

### Falsification

Strongest accessible alternative: "No systematic temporal pattern" — complaints occur randomly relative to recalls. Significant signal in opposite direction (complaints *decrease* before recalls) would also falsify.

### Resource Limits

- Max ~20 model/year × 2 API calls (recalls + complaints) × pagination
- Timeout 30 seconds per request
- Stdlib only (urllib, json, statistics, datetime, urllib.parse)
- Rate limit: 1s between requests

### Output

- `results.json`: Raw data + gate results + statistical tests
- `temporal_analysis.json`: Per-triple complaint timelines and ratios
- `RESULT.md`: Human-readable summary with evidence labels

## Expected Outcomes

If H1 supported: Public complaint data contains predictive signal for recalls. A tool that monitors complaint trends by component could provide early warning to owners. This validates a **predictive monitoring** need type — distinct from Q&A serving.

If H0 supported: Public complaints do not systematically precede recalls. Either manufacturers detect issues through other channels (dealer reports, warranty claims, EWR), or complaint volume is too noisy. The predictive monitoring need is not served by this data source.

Either result advances the mission by testing a **new need type (predictive monitoring)** in a **new domain (automotive safety regulation)**.

## Reproduction

```bash
cd EXPERIMENTS/186-nhtsa-complaint-recall-prediction
python3 run.py
cat results.json
```

Environment: Python 3.8.10, stdlib only, network access to api.nhtsa.gov. Runtime ≈ 2-5 minutes.