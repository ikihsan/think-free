# Fresh Exploration: Clinical Trial Eligibility Matching

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-18
-->

## Hypothesis

**H0 (null):** A structured eligibility matching tool using ClinicalTrials.gov data cannot accurately match patient profiles to recruiting trials at a rate significantly better than random matching. The eligibility criteria are too complex, variable, or incomplete for automated matching.

**H1 (alternative):** A tool that parses structured eligibility fields (condition, age, sex, location, inclusion/exclusion keywords) from ClinicalTrials.gov can match synthetic patient profiles to recruiting trials with precision ≥0.60 and recall ≥0.40 on a held-out test set, significantly outperforming random matching (precision <0.10, recall <0.10).

This tests a **matching/recommendation** need type in the **healthcare/clinical trials** domain — completely distinct from question answering (Stack Overflow), view-count principle (package registries), predictive monitoring (NHTSA), computational planning (knitting), or pattern detection (bank transactions).

## Domain Selection Rule (Stated Before Fetch)

Select a domain in the "healthcare/clinical research" category that:
1. Has a public API requiring no authentication for structured trial data including eligibility criteria
2. Has a clear matching problem: patients ↔ trials with structured eligibility rules
3. Has measurable ground truth: a patient profile either meets or doesn't meet explicit criteria
4. Has not been tested by this mission
5. Is not a package registry, Q&A forum, fault code database, developer platform, model hub, encyclopedia, blogging platform, news aggregator, automotive safety DB, or craft domain

ClinicalTrials.gov satisfies all five: public API v2 (no auth for reading), structured eligibilityModule with criteria/age/sex/location, explicit inclusion/exclusion criteria text, not previously tested, distinct domain (clinical research).

## Prior Art Check

- ClinicalTrials.gov API v2: https://clinicaltrials.gov/api/v2 (public, no auth)
- ~500k+ studies registered, ~50k+ recruiting at any time
- Commercial: Antidote, TrialJectory, Clara Health, MyTrials.ai — proprietary matching, no public benchmarks
- Academic: "Clinical trial eligibility screening using NLP" (multiple papers 2015-2024), but focus on EHR-to-criteria matching, not public API-to-synthetic-patient
- **Claimed difference:** Tests end-to-end matching using *only public API structured fields* (not NLP on full criteria text) against synthetic patient profiles with known ground truth, with predeclared gates.

## Protocol

### Data Source

- ClinicalTrials.gov API v2: `https://clinicaltrials.gov/api/v2/studies`
- Query parameters: `filter.overallStatus=RECRUITING`, `pageSize=1000`, condition filters
- Fields needed: `protocolSection.eligibilityModule`, `conditionsModule`, `contactsLocationsModule`, `identificationModule`

### Synthetic Patient Profiles (Ground Truth)

Generate 100 synthetic patient profiles with known eligibility for sampled trials:

| Profile | Condition | Age | Sex | Location (Country) | Biomarker/History |
|---------|-----------|-----|-----|-------------------|-------------------|
| P1 | Breast Cancer | 52 | FEMALE | United States | ER+, HER2- |
| P2 | Lung Cancer | 65 | MALE | United States | EGFR+ |
| P3 | Type 2 Diabetes | 58 | FEMALE | Canada | HbA1c 8.2% |
| P4 | Melanoma | 45 | MALE | Australia | BRAF V600E |
| P5 | Rheumatoid Arthritis | 40 | FEMALE | United Kingdom | Seropositive |
| ... | ... | ... | ... | ... | ... |

20 conditions × 5 profiles each = 100 profiles. Each profile has a manually verified "eligible" / "ineligible" label for a set of 50 sampled recruiting trials (20 condition-matched, 30 random).

### Matching Algorithm (Pre-declared)

A trial matches a patient profile if ALL structured criteria pass:

1. **Condition match**: Trial condition list overlaps patient condition (exact or synonym via MeSH mapping)
2. **Age match**: Patient age within [minimumAge, maximumAge] (parsed from stdAges/minimumAge)
3. **Sex match**: Trial sex = patient sex OR trial sex = ALL
4. **Location match**: Trial has recruiting site in patient's country (from contactsLocationsModule.locations)
5. **Keyword inclusion**: No exclusion keyword matches patient profile (simple keyword scan of eligibilityCriteria text for: "pregnant", "transplant", "HIV", "hepatitis", "metastatic" unless patient has it)

### Arms

| Arm | Description |
|-----|-------------|
| **A (Structured Matcher)** | Full structured matching (conditions 1-5 above) |
| **B (Condition-only)** | Condition match only (baseline) |
| **C (Random)** | Random trial selection (control) |

### Gates (Pre-declared)

| Gate | Condition | Threshold |
|------|-----------|-----------|
| **G1** (Sample adequacy) | ≥ 30 recruiting trials with complete eligibility data | 30 |
| **G2** (Profile coverage) | ≥ 80 profiles have ≥1 condition-matched trial | 80 |
| **G3** (Precision) | Arm A precision ≥ 0.60 on eligible-labeled pairs | 0.60 |
| **G4** (Recall) | Arm A recall ≥ 0.40 on eligible-labeled pairs | 0.40 |
| **G5** (Baseline separation) | Arm A F1 > Arm B F1 + 0.15 AND Arm A F1 > Arm C F1 + 0.20 | ΔF1 |

### Kill Conditions

- Any gate FAIL → matching not viable with structured fields alone
- G3 or G4 FAIL → precision/recall too low for practical use
- G5 FAIL → structured fields don't add value over condition-only or random

### Falsification

Strongest accessible alternative: "Condition-only matching is sufficient" — most trials are condition-specific, so age/sex/location filters add little. If Arm B (condition-only) achieves similar F1 to Arm A, structured matching adds no value.

### Resource Limits

- Max ~50 API calls (5 condition searches × 1000 trials each, but paging)
- Timeout 30 seconds per request
- Stdlib only (urllib, json, statistics, datetime, re)
- Rate limit: 1s between requests

### Output

- `results.json`: Raw data + gate results + per-profile metrics
- `matching_details.json`: Per-profile trial matches with reasons
- `RESULT.md`: Human-readable summary with evidence labels

## Expected Outcomes

If H1 supported: Structured eligibility fields from public API enable viable patient-trial matching. A tool could help patients find relevant trials. Validates **matching/recommendation** need type in **healthcare** domain.

If H0 supported: Structured fields insufficient; eligibility requires full NLP on criteria text, EHR integration, or human review. The matching need is not served by public API alone.

Either result advances the mission by testing a **new need type (matching/recommendation)** in a **new domain (clinical trials/healthcare)**.

## Reproduction

```bash
cd EXPERIMENTS/187-clinical-trial-matching
python3 run.py
cat results.json
```

Environment: Python 3.8.10, stdlib only, network access to clinicaltrials.gov. Runtime ≈ 3-5 minutes.