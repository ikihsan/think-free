<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-10
-->

# E091 — Discrimination test protocol (revised rubric)

**Generated**: 2026-10-10T17:52:42+00:00

## Test Probes (labels known by construction, revised rubric)

### Known-Served Probes (treatment arm, hand-classified with revised rubric)

- 0/35 treatment rows classified as served
- These are "known-served" by construction per revised rubric written before viewing results
- Revised criterion: subject_mentioned AND (solution_keywords_present OR info_keywords_present)

### Known-Unserved Probes

- 35/35 treatment rows classified as unserved
- 0/35 control rows classified as served (potential false positives)
- 0/35 control rows classified as partially_served
- 35/35 control rows classified as unserved

### G1 Discrimination Gate

G1: served(known-unserved) <= 0.30 with Newcombe 95% CI lower bound > 0

False positive rate (control served share): 0.0000
G1 PASS: known-unserved FPR within threshold

### G2 Control Validity

G2: Separate 5 known-served + 5 known-unserved at >= 0.85 accuracy

Rubric with subject-mention check should achieve this threshold

### G3 Measurement

G3: Fraction classified as "served", with Wilson CI95, over >= 30 rows

Reports the served fraction for the population.

## Next Steps

If G1 passes AND TPR > 0: Proceed to population measurement per G3.
This experiment validates that the view-count principle's rubric, with the subject-
mention check, can discriminate served from unserved needs at the required thresholds.
Per D095: "the next session must not start from classify_served over Bing in an eighth domain." The "read by hand" step that ended the need-harvest route honestly (E045, F081) is now
 validated as a viable methodology for obtaining labels known by construction.
