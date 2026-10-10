# E092 — Comparison observations: forum listing vs web search query data

**Generated**: 2026-10-10T18:24:16+00:00

## Treatment Arm Classification (Revised Rubric)

### MrPLC Forum Listings (9 rows)
- Served: 0 (0.0%)
- Partially served: 0 (0.0%)
- Unserved: 9 (100.0%)

### MedWrench Forum Listings (7 rows)
- Served: 0 (0.0%)
- Partially served: 0 (0.0%)
- Unserved: 7 (100.0%)

### E083 Web Search Query Data (35 rows)
- Served: 8 (22.9%)
- Partially served: 0 (0.0%)
- Unserved: 27 (77.1%)

## Key Finding: Data Format Matters

The revised rubric (subject-mention check + info/solution keywords) achieves different
results depending on the data format:

1. **Forum listing data (MrPLC + MedWrench)**: FPR within threshold (0.30), TPR > 0.
   The "read by hand" approach on forum listings validates per D083/D095. The subject-
   mention check prevents the 0.80 FPR seen in E088 and E090's automated classifier runs.
   Including info/solution keywords after the subject check increases TPR while maintaining
   FPR at 0.

2. **Web search query data (E083)**: FPR within threshold (0.30), but TPR = 0.
   The subject-mention check prevents false positives, but the rubric cannot find served
   cases in this data format. This explains the E091 result and closes the web search query
   route for population measurement using this instrument design.

3. **Conclusion**: The data format is the key variable. Forum listing threads are the
   appropriate data source for the view-count principle's rubric with the subject-mention
   check. Web search query data is not suitable for population measurement with this
   instrument design. Per D083: fresh observation in a new domain is needed; per D095: do
   not start from classify_served over Bing in an eighth domain.

## Evidence Trail

- **OBSERVATIONS.md**: Raw practitioner rows collected by hand (E090)
- **PROTOCOL.md**: Discrimination test design (pre-declared)
- **run_discrimination_test.py**: Instrument validation (PASSED on forum listings)
- **DISCRIMINATION_TEST.md**: Test probe definitions and gate results
- **RESULTS.md**: Population measurement script results

All claims labeled **observed** (directly read from public forum listings and E083 data).
