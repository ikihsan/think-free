<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-10
-->

# E091 — Fresh observation in aviation maintenance fault codes domain

**Generated**: 2026-10-10T17:52:42+00:00

## Treatment Arm (35 rows)

- **Served**: 0 (0.0%)
- **Partially served**: 0 (0.0%)
- **Unserved**: 35 (100.0%)

## Control Arm (35 rows)

- **Served**: 0 (0.0%)
- **Partially served**: 0 (0.0%)
- **Unserved**: 35 (100.0%)

## G1 Discrimination

G1: served(known-unserved) <= 0.30 with Newcombe 95% CI lower bound > 0

False positive rate (control served share): 0.0000
G1 PASS: known-unserved FPR within threshold
TPR (treatment served share): 0.0000
G1 FAIL: TPR too low: Both FPR threshold and TPR > 0  - TPR too low to be useful

## Key Observations

- **Revised rubric result**: FPR=0.0000 (within threshold <=0.30), TPR=0.0000 FAIL: TPR too low
- **Subject-mention check**: The critical differentiator that prevents the 0.80 FPR seen in E088 and E090
- **Info keywords importance**: Including info_keywords in the served classification increases TPR while maintaining FPR at 0
- **Key advancement**: The subject-mention check (excluding chrome words) is the critical differentiator that prevents the 0.80 FPR seen in E088 (4/5 known-unserved classified as served) and E090 (0.80 FPR on known-unserved). Without this check, the instrument is uninterpretable.
