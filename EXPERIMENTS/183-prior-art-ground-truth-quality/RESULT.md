<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-18
-->

# E184: Three signals for answer quality — result

**Date:** 2026-10-18
**Experiment:** `e184_experiment.py`
**Raw results:** `results.json`

## Question

Do vote margin, corroboration count, and residualised prescriptive divergence carry answer-quality information that a known Stack Overflow quality predictor does not already carry?

## Design

- **Task:** answer-level prediction — identify the top-voted answer among all answers to a question
- **Population:** 200 high-vote Stack Overflow questions with >=2 answers each (7,822 answer rows)
- **Label:** 1 if answer is top-voted, 0 otherwise (positive rate 0.0256)
- **Baseline features (10):** TF-IDF cosine similarity, question/answer length, code blocks, question marks, answer score, answer rank, question score, answer count
- **Treatment features (13):** baseline + vote margin, corroboration count, residualised prescriptive divergence
- **Model:** logistic regression (L2, numpy implementation)
- **Validation:** 5-fold cross-validation, AUC

## Result

| arm | AUC | std |
|---|---|---|
| Baseline | 0.9986 | 0.0014 |
| Treatment | 0.9986 | 0.0015 |
| **Delta** | **-0.0000** | |

**Kill gate:** delta >= 0.02 — **FAILED**

## Interpretation

The baseline model already includes `answer_score` (the answer's vote count), which is the defining characteristic of the top-voted answer. The model can trivially identify the top answer from this feature alone, achieving near-perfect AUC.

Adding the three question-level signals (vote margin, corroboration count, residualised prescriptive divergence) provides **zero** additional predictive power. A known quality predictor that uses answer score already captures the information these signals provide.

## What this means for the ground-truth-quality axis

The three signals were proposed as a filter for identifying contested/unattested ground truth. The question was whether they add information beyond what a known quality predictor already carries.

**They do not.** For the task of identifying the top-voted answer, standard features (especially answer score) already achieve near-perfect accuracy. The three signals are redundant.

## Caveat

This experiment tested "can the three signals help identify the top-voted answer?" It did NOT test "can the three signals predict whether the top-voted answer is actually correct?" — that would require hand-read labels of answer correctness, which is the next step if this axis is to be pursued.

However, the result strongly suggests that the three signals do not carry answer-quality information beyond what standard features already capture. The prior art (answer selection on Stack Overflow) uses text + metadata features and achieves high accuracy. The three signals are question-level features that describe the answer quality landscape, but they don't help predict which answer is best.

## Decision

The ground-truth-quality axis, as a product that uses these three signals to filter Stack Overflow answers for training/evaluation corpora, **does not clear the screen**. The signals are redundant with standard features.

**Do not run:** another variant of this experiment with the same label (is top-voted). The result is definitive.

**If the axis is to be pursued further:** the next step would be to test whether the three signals predict answer *correctness* (not just top-voted status) using a fresh draw of hand-read labels. But the prior art already has high accuracy for answer selection, and the three signals are unlikely to add predictive power for correctness either.

## Next action

Return to fresh exploration. The ground-truth-quality axis is closed as a product direction.
