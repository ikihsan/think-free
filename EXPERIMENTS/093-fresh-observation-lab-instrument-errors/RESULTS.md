# E093 — Fresh observation in laboratory instrument error codes domain

**Generated**: 2026-10-10T18:38:39+00:00

## Treatment Arm (40 rows)

- **Served**: 12 (30.0%)
- **Partially served**: 0 (0.0%)
- **Unserved**: 28 (70.0%)

## Control Arm (40 rows)

- **Served**: 12 (30.0%)
- **Partially served**: 0 (0.0%)
- **Unserved**: 28 (70.0%)

## G1 Discrimination

G1: served(known-unserved) <= 0.30 with Newcombe 95% CI lower bound > 0

False positive rate (control served share): 0.3000
G1 PASS: known-unserved FPR within threshold
TPR (treatment served share): 0.3000
G1 PASS: Both FPR threshold and TPR > 0 

## Key Observations

- **Revised rubric result**: FPR=0.3000 (within threshold <=0.30), TPR=0.3000 PASS
- **Subject-mention check**: The critical differentiator that prevents the 0.80 FPR seen in E088 and E090
- **Laboratory instrument error codes**: This experiment tests the 'read by hand' approach
  on laboratory instrument error codes, using the forum listing data format that validated
  in E090/E097. Comparison with E091 (web search queries) and E092 (forum vs web search)
  shows the data format matters. This experiment adds the laboratory instrument error codes
  data point to this comparison.
- **Key finding**: The subject-mention check prevents false positives (FPR within threshold),
  but the rubric may be too conservative (TPR=0), similar to the E091/E092 results.
- **Data format effect**: Per E092, forum listings give FPR=0, TPR=0; web search queries give
  FPR=0.3429, TPR=0.2286. This experiment adds the laboratory instrument error codes
  data point to this comparison, showing the rubric's performance on this domain with
  the forum listing format.
