<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-14
-->
# E160 — Fresh observation: Medical diagnosis technique root cause classification

**Date:** 2026-10-14 · **Status:** Protocol declared before any implementation

---
## The claim (one sentence, scoped)

Given only the text of a medical symptom description, a deterministic classifier can assign the correct diagnosis category (bacterial infection, viral infection, chronic condition, acute injury) at accuracy ≥ 80%, beating a keyword-based baseline by ≥ 15 percentage points.

---
## Practical difficulty

When patients present with symptoms, healthcare providers must:
1. Identify the likely diagnosis from symptom descriptions
2. Understand the underlying pattern (bacterial vs viral vs chronic vs acute)
3. Apply the appropriate next steps (prescription, supportive care, referral, emergency intervention)

This is a recurrent clinical task with observable failure patterns that could be systematically classified. The symptom description contains structural features (symptom duration, combination of findings, temporal pattern) that may enable accurate diagnosis without in-person examination.

---
## Strongest baseline

**Keyword-based pattern matching** — a rule-based classifier that searches for canonical phrases per diagnosis category:

| Category | Canonical signals (not exhaustive) |
|----------|-----------------------------------|
| `bacterial_infection` | fever, elevated wbc, positive culture, purulent, acute onset |
| `viral_infection` | fever, cough, runny nose, normal wbc, diffuse symptoms |
| `chronic_condition` | persistent symptoms > 2 weeks, weight loss, lab trends, gradual onset |
| `acute_injury` | severe pain, swelling, clear mechanism, limited range of motion |

This baseline is **runnable, deterministic, and requires no training data**. It represents the strongest accessible approach that uses only the symptom text.

---
## Kill gates (pre-declared, all must pass for the claim to survive)

| Gate | Condition | Threshold |
|------|-----------|-----------|
| **G1** — Synthetic fixture validity | All 16 synthetic fixtures (4 per category) are correctly labelled by construction | 16/16 = 100% (by design) |
| **G2** — Classifier beats keyword baseline | Classifier accuracy ≥ Keyword baseline accuracy + 15pp | Δ ≥ 0.15 |
| **G3** — Minimum absolute accuracy | Classifier accuracy on held-out fixtures ≥ 80% | Acc ≥ 0.80 |
| **G4** — Information-sufficiency witness | Two fixtures with **identical surface keywords** but **different root causes** must be distinguishable by the classifier (or the classifier must abstain on both) | Both correctly classified or both abstained |
| **G5** — Abstention honesty | Classifier abstention rate ≤ 20% on valid fixtures | Abstain ≤ 0.20 |

**If any gate fails, the claim is falsified and the line of work ends.**

---
## Synthetic fixtures (declared before implementation)

16 synthetic medical symptom descriptions, 4 per category, constructed from common clinical presentation patterns. Each fixture is a string describing a patient's symptoms with onset, duration, and associated findings.

### Categories and distinguishing features:

| Category | Canonical symptoms in description |
|----------|----------------------------------|
| **bacterial_infection** | fever (high), elevated wbc, positive culture, purulent discharge, acute onset (> 2 days) |
| **viral_infection** | fever (moderate), cough, runny nose, normal wbc, diffuse symptoms, gradual onset |
| **chronic_condition** | symptoms > 2 weeks duration, weight loss, lab trend changes, gradual onset, fluctuating severity |
| **acute_injury** | severe pain, swelling, clear mechanism/trauma, limited range of motion, acute onset |

### Information-sufficiency pair (G4):

Two fixtures constructed to contain **identical surface keyword sets** but different root causes:

- **Fixture A (bacterial_infection):** `Fever 102°F, elevated WBC 18.5, purulent throat discharge, acute onset 2 days ago`
- **Fixture B (viral_infection):** `Fever 101°F, cough, runny nose, normal WBC 6.5, gradual onset 3 days ago`

Both contain: `fever`, `onset`, `WBC`. Fixture A uses `elevated` + `purulent` → bacterial_infection. Fixture B uses `cough` + `runny nose` → viral_infection. The classifier must use the accompanying symptom context (`purulent` vs `cough`) and structural patterns to distinguish, since a naive keyword-set-equal comparison would map both to the same category (fever-related).

---
## Inputs, oracle, thresholds, resource limits

- **Inputs:** 16 synthetic fixture strings (declared in `fixtures.jsonl`)
- **Oracle:** The category field in each fixture (ground truth by construction)
- **Thresholds:** As defined in kill gates above
- **Resource limits:** Python 3.8+, stdlib only, no network, runtime < 10s
- **Random seed:** Fixed at 42 for any stochastic component

---
## Negative controls (must fail)

1. **Random classifier** — assigns categories uniformly at random (expected accuracy ~25%)
2. **Majority classifier** — always predicts the most frequent category in the fixture set
3. **Keyword-only ablated classifier** — the proposed classifier with structural features disabled

These must perform **worse** than the full classifier on G2/G3. If they perform equally, the experiment cannot distinguish signal from noise.

---
## Synthetic data declaration

All fixtures are **synthetic**, constructed by the experimenter from documented clinical presentation patterns. They are **not** harvested from real patient records. Their origin is recorded in `fixtures.jsonl` with `source: "synthetic"`. They can falsify a universal claim but cannot establish real-world prevalence.

---
## Reproduction

```bash
cd EXPERIMENTS/160-medical-diagnosis-classification
python3 run.py
cat results.json
```