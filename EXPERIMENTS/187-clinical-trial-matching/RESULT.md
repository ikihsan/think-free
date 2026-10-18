# E187 — Clinical Trial Eligibility Matching: RESULT

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-18
-->

## One-line result

**Kill gate fired.** ClinicalTrials.gov structured eligibility fields (age, sex, location, exclusion keywords) are too restrictive for practical patient-trial matching. Only **35% of patients** have ≥1 matching trial after all filters; median final matches = **0.0**. The location filter alone reduces median matches from 16.5 to 1.0; exclusion keywords reduce it to 0.

## What was tested

**Hypothesis:** Structured eligibility fields from ClinicalTrials.gov API (condition, age, sex, location, exclusion keywords) can match patient profiles to recruiting trials with useful yield.

**Domain:** Healthcare/clinical trials — a completely new domain for this mission, testing a **matching/recommendation** need type (distinct from question answering, view-count principle, predictive monitoring, computational planning, pattern detection).

**Population:** 100 synthetic patient profiles across 20 conditions (5 profiles each), 385 condition-matched recruiting trials with complete eligibility data, 93 random trials.

**Method:** Sequential filtering funnel — apply structured filters one at a time (condition → age → sex → location → exclusion keywords) and measure how many trials survive for each patient. No circular ground truth; the measurement is the funnel itself.

## Gate Results

| Gate | Condition | Result | Evidence |
|------|-----------|--------|----------|
| **G1** (sample adequacy) | ≥30 condition-matched trials with complete data | **PASS** | 385 trials |
| **G2** (patient coverage) | ≥80 patients have ≥1 final match | **FAIL** | 35/100 |
| **G3** (median yield) | Median final matches ≥1 | **FAIL** | 0.0 |
| **G4** (mean yield) | Mean final matches ≥3 | **FAIL** | 0.5 |
| **G5** (retention) | Retain ≥10% of condition-matched trials | **FAIL** | 0.0% |

**Overall: KILL GATE FIRED** (G2, G3, G4, G5 all failed)

## Filtering Funnel Analysis

| Filter Stage | Median Trials Remaining | Mean Trials Remaining |
|--------------|------------------------|----------------------|
| Initial (condition-matched) | 16.5 | 15.8 |
| After Age | 16.0 | 15.1 |
| After Sex | 16.0 | 14.9 |
| **After Location** | **1.0** | **2.3** |
| After Exclusion Keywords | **0.0** | **0.5** |

### Key Findings

1. **Location is the dominant filter** — 94% reduction (16.5 → 1.0 median). Most trials only recruit in 1-3 countries; patients outside those countries have zero matches regardless of medical eligibility.

2. **Exclusion keywords eliminate the rest** — The remaining ~1 trial per patient typically contains exclusion keywords (metastatic, pregnant, transplant, HIV, hepatitis) that don't match the patient profile.

3. **Age and sex filters are minimally restrictive** — They reduce the pool by only ~3% combined. Most trials accept broad age ranges and both sexes.

4. **Only 4 of 20 conditions yield any median matches**:
   - Breast cancer: median 1.0
   - Prostate cancer: median 1.0  
   - Multiple sclerosis: median 1.0
   - Atrial fibrillation: median 1.0
   - All other 16 conditions: median 0.0

5. **Patient profiles with matches tend to be in US/Canada/UK** — These countries have the most recruiting sites.

## What This Decides

**The matching/recommendation need — "find clinical trials I'm eligible for" — is not served by ClinicalTrials.gov structured fields alone.**

- Geographic constraints (location filter) make matching infeasible for most patients
- Exclusion criteria in free text are not reliably parseable with simple keywords
- A tool using only structured API fields would return empty results for 65% of patients
- Full NLP on eligibility criteria text + EHR integration would be needed for viable matching

## Ceilings and Limitations

1. **Synthetic patients only** — Real patients have more complex histories; results are optimistic
2. **Keyword-based exclusion parsing** — Real exclusion criteria are nuanced (e.g., "metastatic unless enrolled in Arm B")
3. **Location = country only** — Doesn't account for travel willingness or site-level distance
4. **20 trials per condition** — May miss trials for rarer conditions; but 385 total is adequate
5. **No MeSH/ontology matching** — Used simple string synonyms; real matching needs ontology
6. **Recruiting status only** — Excludes "Not yet recruiting" trials that may open soon

## What This Does NOT Establish

- ❌ That no trial matching tool can work (commercial tools use NLP + EHR + broader data)
- ❌ That ClinicalTrials.gov data is useless (it's the primary registry)
- ❌ That location filtering is "wrong" (trials genuinely have geographic constraints)

## Evidence Labels

- Gate results and funnel statistics: `observed` (computed from fetched data)
- "Matching need not served by structured fields": `inferred` (from gate failures)
- Ceilings: `observed` (visible in data)

## Next Actions

**Do not pursue:** Patient-trial matching tools based solely on ClinicalTrials.gov structured API fields.

**Fresh exploration continues:** This experiment tested a new domain (healthcare/clinical trials) and a new need type (matching/recommendation). Both are now characterized. The mission should test a different domain or need type per STATE.md standing instruction.

## Reproduction

```bash
cd EXPERIMENTS/187-clinical-trial-matching
python3 run.py
cat results.json
```

Environment: Python 3.8.10, stdlib only, network access to clinicaltrials.gov. Runtime ≈ 4 minutes.