# E186 — NHTSA Complaint-Recall Predictive Relationship: RESULT

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-18
-->

## One-line result

**Kill gate fired.** Public NHTSA complaint data does not show a statistically significant predictive signal for recalls at the predeclared thresholds. Median complaint rate ratio for recalled categories was **1.78×** (threshold ≥2.0), and Mann-Whitney U test comparing recalled vs non-recalled categories gave **p = 0.187** (threshold <0.05). The predictive early-warning need is not served by this data source at this measurement resolution.

## What was tested

**Hypothesis:** Owner complaints submitted to NHTSA contain early signals of issues that later become recalls. Complaints for a specific component category increase significantly before a recall is issued for that component.

**Domain:** Automotive safety regulation (NHTSA) — a completely new domain for this mission, testing a **predictive monitoring** need type (not question answering, not view-count principle).

**Population:** 20 popular vehicle model/year combinations (2019-2020), 12 with ≥1 recall, 46 total recalls, 42,015 total complaints.

**Method:** For each (model, year, component category) with a recall, compare complaint rate in 2-year window before recall vs 2-year baseline window before that. Compare recalled categories against non-recalled categories using median ratio and Mann-Whitney U test.

## Gate Results

| Gate | Condition | Result | Evidence |
|------|-----------|--------|----------|
| **G1** (sample adequacy) | ≥10 model/year/category triples with recalls | **PASS** | 12 triples |
| **G2** (complaint volume) | ≥50 total complaints | **PASS** | 42,015 complaints |
| **G3** (temporal signal) | Median recalled ratio ≥2.0 | **FAIL** | 1.78× |
| **G4** (specificity) | Median non-recalled ratio <1.5 | **PASS** | 1.25× |
| **G5** (statistical) | Mann-Whitney p < 0.05 | **FAIL** | p = 0.187 |

**Overall: KILL GATE FIRED** (G3 and G5 failed)

## Key Findings

### 1. Complaint elevation exists but is weak
The median complaint rate ratio for recalled categories was 1.78× — complaints do increase before recalls, but not at the predeclared 2.0× threshold. Several individual category/model combinations showed strong signals (ratio >3.0 for Ford Escape STRUCTURE/BODY at 13.1×, Ram 1500 ENGINE at 7.0×), but these were offset by categories with no elevation (ratio 1.0 or <1.0).

### 2. Signal is not specific to recalled categories
Non-recalled categories also showed elevated ratios (median 1.25×), with several exceeding 2.0× (e.g., Ford Escape ELECTRICAL SYSTEM 7.0×, STEERING 8.0×, VISIBILITY 2.3×, OTHER 4.0×). This means complaint trends alone cannot distinguish which component issues will become recalls.

### 3. No statistical separation
Mann-Whitney U test (recalled n=46, non-recalled n=214) gave p=0.187. The distributions overlap substantially — complaint elevation is a general property of aging vehicles, not specific to recall-bound issues.

### 4. Many recalls have zero pre-recall complaints
Of 46 recalls, 18 (39%) had zero complaints in the 2-year window for the recalled category. This includes safety-critical recalls (brakes, air bags, fuel system) where manufacturer detection (dealer reports, warranty claims, Early Warning Reporting) clearly operates through channels other than public complaints.

### 5. Baseline window often empty
For newer model years (2019-2020), the 4-year baseline window often falls before the model existed, yielding zero baseline complaints and infinite ratios. This inflates both recalled and non-recalled ratios, reducing discriminative power.

## What This Decides

**The predictive monitoring need — "alert me to emerging safety issues before a recall" — is not served by public NHTSA complaint data at this measurement resolution.**

- Public complaints are too noisy and non-specific
- Manufacturer detection channels (dealer reports, warranty, EWR) are primary for recalls
- Complaint trends reflect general vehicle aging, not recall-bound issues specifically
- A tool monitoring public complaint trends would generate excessive false alarms

## Ceilings and Limitations

1. **Model year restriction**: 2019-2020 models limit baseline window (many baselines are pre-production)
2. **Component mapping**: NHTSA component taxonomy mapped to 12 categories loses granularity
3. **Complaint pagination**: Limited to 5 pages (500 complaints) per model/year; Ford Escape had 7,695 total
4. **Single country**: US market only; recall timing differs globally
5. **No manufacturer EWR data**: The actual early-warning system uses manufacturer-submitted data (not public)
6. **One measurement resolution**: 2-year windows; shorter/longer windows not tested

## What This Does NOT Establish

- ❌ That no predictive signal exists at any resolution
- ❌ That manufacturer EWR data lacks predictive signal (not tested)
- ❌ That complaint data is useless for all safety purposes
- ❌ That a different classification or time window wouldn't work

## Evidence Labels

- Gate results: `observed` (computed from fetched data)
- Ratios and p-values: `observed`
- "Predictive need not served": `inferred` (from gate failures)
- Ceilings: `observed` (visible in data)

## Next Actions

**Do not pursue:** Predictive monitoring tools based on public NHTSA complaint trends.

**Fresh exploration continues:** This experiment tested one new domain (automotive safety) and one new need type (predictive monitoring). Both the domain and need type are now characterized. The mission should continue fresh exploration in a different domain or need type, per STATE-next-actions.md guidance.

## Reproduction

```bash
cd EXPERIMENTS/186-nhtsa-complaint-recall-prediction
python3 run.py
cat results.json
```

Environment: Python 3.8.10, stdlib only, network access to api.nhtsa.gov. Runtime ≈ 3 minutes.