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

### The candidate decision this changes

Stated in advance per owner brief §4:

- **If terminated trials show a high fraction of scientific failures (safety/efficacy/futility) with common mechanistic patterns**, then a tool that tracks "failed mechanistic hypotheses" across conditions could help researchers avoid repeating known-failed approaches. This would be a candidate invention in research intelligence.
- **If terminations are predominantly administrative (funding, business, recruitment, regulatory)**, then the failure record is not a scientific signal and there is no candidate here. The route remains deferred per D083.

Either result is a decision; neither is a candidate. This experiment is not expected to produce a product.

## Population and arms

| Arm | Source | Domain | What it carries |
|-----|--------|--------|-----------------|
| **1 (treatment)** | ClinicalTrials.gov terminated trials for 3 conditions: cancer, Alzheimer's, Type 2 diabetes | Medical research | NCT ID, condition, phase, enrollment, whyStopped, start/completion dates, intervention, sponsor |
| **2 (control)** | ClinicalTrials.gov completed trials for same 3 conditions (sampled) | Medical research | Same fields, for baseline comparison of trial characteristics |

**Why ClinicalTrials.gov, and why it is not interchangeable with prior surfaces:**
- Not a forum: no self-selection bias of "people who post." Every registered trial appears.
- Regulatory mandate: trial registration is required by law (FDAAA 2007) for applicable trials.
- Structured outcome: `whyStopped` is a free-text field but with consistent vocabulary (business decision, safety, efficacy, futility, recruitment, funding, administrative).
- Arrivals metric: **enrollment count** = patients who participated in the failed attempt. Independent arrivals at a failed hypothesis.
- Population: **industry and academic sponsors** testing mechanistic hypotheses in humans. Not hobbyists, not developers, not general consumers.

**Confound declared in advance:** Industry sponsors may use "business decision" as a euphemism for scientific failure. Recruitment failure may reflect scientific unviability (patients won't enroll for a doomed approach). The classifier must handle this ambiguity honestly.

## Gates, all declared before any row is fetched or read

| Gate | Condition | If not met |
|------|-----------|------------|
| **G1 retrieval** | ≥ 200 terminated trials across ≥ 3 conditions, each carrying NCT ID, condition, phase, enrollment, whyStopped, intervention; harvest reconciled against API total count | the route is not measurable at this cost. Stop; record the ceiling. |
| **G2 classification validity** | Two readers classify a 50-trial overlapping subsample (stratified by condition) into {scientific_failure, administrative_failure, ambiguous} at κ ≥ 0.80 | the classification rubric is not reliable. Stop. |
| **G3 the measurement** | Scientific failure fraction of arm 1 (terminated trials), with Wilson CI95, over ≥ 200 trials; and the same fraction stratified by condition and phase | this is the result; no gate |
| **G4 enrollment validation** | ≥ 80% of terminated trials report enrollment > 0 (independent arrivals observed) | the arrivals metric is not usable. Record the gap. |

**Positive control, stated as a requirement on the instrument, not on the world:**
The reader must recover seeded positives (G2). A rubric with no positive control is the shape F029 took.

**Denominators:** Every fraction is over rows read. Rows not read are reported as rows not read. Per D082, an arm that produced no observation is a missing observation, never a zero and never a denominator.

## Classification rubric, written before rows are read

A terminated trial is **scientific_failure** when `whyStopped` indicates:
- Safety concerns, adverse events, toxicity
- Lack of efficacy, futility, no benefit
- Mechanistic failure (biomarker not achieved, target not engaged)
- Dose-limiting toxicity
- Unfavorable risk-benefit

A terminated trial is **administrative_failure** when `whyStopped` indicates:
- Business decision, strategic reprioritization, portfolio decision
- Funding withdrawn, sponsor decision, financial
- Recruitment difficulty, slow enrollment, insufficient enrollment
- Regulatory action, FDA hold, protocol amendment not approved
- Sponsor merger/acquisition, company dissolution
- Administrative, operational, logistical

A terminated trial is **ambiguous** when:
- `whyStopped` is missing, empty, or generic ("study terminated", "closed")
- Multiple reasons given spanning both categories
- Reason is unclear or uses non-standard terminology

## Ceiling, stated now

One platform (ClinicalTrials.gov) via public API; three conditions selected for mechanistic diversity (oncology, neurodegeneration, metabolic); one classification rubric with two readers on a subsample; enrollment as arrivals metric. This measures the *shape* of scientific failure in registered clinical trials. It does not measure demand, does not measure adoption, and does not close any candidate.

## Reproduce

```bash
python3 EXPERIMENTS/075-clinical-trial-failures/harvest.py     # arm 1 + control
python3 EXPERIMENTS/075-clinical-trial-failures/classify.py    # classification with two readers
python3 EXPERIMENTS/075-clinical-trial-failures/analyze.py     # every gate above
```

Needs internet access for ClinicalTrials.gov API calls, Python 3.8+ with stdlib only.

## Conditions to harvest (pre-registered)

Selected for: high trial volume, distinct mechanistic domains, public health significance.

1. **Cancer** (neoplasms) — high volume, many mechanistic hypotheses tested
2. **Alzheimer's disease** — high failure rate, distinct mechanisms (amyloid, tau, inflammation)
3. **Type 2 diabetes** — metabolic domain, different mechanism classes

Target: ~100 terminated trials per condition (300 total), plus ~50 completed trials per condition for control.