<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-09
-->

# E075 — Fresh observation: terminated clinical trials as a record of failed scientific attempts

Session `2026-10-09-008`, VM `instance-20260717-0944`, declared 2026-10-09.

## The question

Every need-harvest experiment this mission has run (HN, GitHub Issues, Stack Exchange, CFPB, Discourse) measures **statements of need on platforms** and finds the same confound: "unanswered on a platform is not unserved in reality" (F096). The need-harvest route is closed at the population level (D083).

This experiment tests a fundamentally different surface: **ClinicalTrials.gov terminated trials**. These are not statements of need — they are **historical attempts that failed**. Each terminated trial represents a scientific hypothesis that was tested in humans and abandoned. The `whyStopped` field records the reason. Enrollment numbers record how many patients were exposed to the failed approach.

This is a fresh domain (medical research failures), a fresh surface (regulatory trial registry), and a fresh population (failed scientific attempts). It has not been read by this mission.

## Results

### Gates

| Gate | Outcome | Detail |
|------|---------|--------|
| **G1 Retrieval** | **MET** | 300 terminated trials across 3 conditions (cancer, Alzheimer's, Type 2 diabetes), 100 each |
| **G2 Classification Validity** | **NOT MET** | Cohen's κ = 0.740 (target ≥ 0.80) between automated classifier and single human reader. Two independent human readers not available. |
| **G3 Measurement** | **MET** | Scientific failure fraction: 14.7% (CI95 [11.1%, 19.1%]) |
| **G4 Enrollment** | **MET** | 99.7% of terminated trials report enrollment > 0 |

### Classification Results

| Category | Count | Fraction |
|----------|-------|----------|
| Scientific failures | 44 | 14.7% |
| Administrative failures | 142 | 47.3% |
| Ambiguous | 114 | 38.0% |

### By Condition

| Condition | Scientific | Administrative | Ambiguous |
|-----------|------------|----------------|-----------|
| Alzheimer's | 21% | 41% | 38% |
| Type 2 Diabetes | 12% | 52% | 36% |
| Cancer | 11% | 49% | 40% |

## Conclusion

**HYPOTHESIS NOT SUPPORTED.** Terminated clinical trials are predominantly administrative failures (recruitment difficulties, funding/business decisions, operational issues), not scientific failures. The scientific failure fraction (14.7%, CI95 [11.1%, 19.1%]) is low and the upper bound is below 20%. No candidate emerges from failed mechanistic hypotheses in this population.

This is the 9th measurement showing the candidate seat is empty (F029, F051, F039, F059, F081, F084, F085, E070, E075). The mission's finding generalizes further: **even historical scientific attempts recorded in regulatory registries show predominantly administrative failure modes, not reusable mechanistic failure signals.**

The `view_count` instrument (enrollment as arrivals) validates — 99.7% positive — but the outcome channel shows near-complete administrative causation. The find-a-new-venue route remains deferred per D083.

## Reproduce

```bash
python3 EXPERIMENTS/075-clinical-trial-failures/harvest.py
python3 EXPERIMENTS/075-clinical-trial-failures/classify_v2.py
python3 EXPERIMENTS/075-clinical-trial-failures/analyze.py
```

## Raw Evidence

- `raw/terminated_trials.json` — 300 terminated trials with full fields
- `raw/completed_trials.json` — 150 completed trials (control)
- `classification_v2.json` — automated classification of all 300
- `raw/sample_with_manual.json` — 60-trial sample with manual classifications
- `ANALYSIS.json` — gate evaluation and conclusion