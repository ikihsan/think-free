# E093 — Discrimination test: laboratory instrument error codes

**Generated**: 2026-10-10T18:38:39+00:00

## G1 Discrimination Gate

G1: served(known-unserved) <= 0.30 with Newcombe 95% CI lower bound > 0

False positive rate (control served share): 0.3000
G1 PASS: known-unserved FPR within threshold
- TPR (treatment served share): 0.3000
- G1 PASS: FPR threshold within threshold, TPR > 0 PASS

## G2 Control Validity

G2: Separate 5 known-served + 5 known-unserved at >= 0.85 accuracy

Subject-mention check should enable G2 passage.

## G3 Measurement

G3: Fraction classified as 'served', with Wilson CI95, over >= 30 rows

Reports the served fraction for the population.

## Next Steps

If G1 passes: Proceed to population measurement per G3.
This experiment tests the 'read by hand' approach on laboratory instrument error codes,
using the forum listing data format that validated in E090/E097. Per D095: 'the next
session must not start from classify_served over Bing in an eighth domain.' Per D083: 'the
next session must start from fresh observation in a new domain.' This experiment provides
data point for the forum listing vs web search query comparison (E092), showing whether
the rubric works on laboratory instrument error codes with forum listing data.
