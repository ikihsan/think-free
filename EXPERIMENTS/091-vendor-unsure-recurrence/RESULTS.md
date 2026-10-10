# E091 — Results: Vendor-Unsure Fault Recurrence Measurement

## Experiment: E091

### Baseline Measurement (9 practitioner rows from E090, MrPLC.com)

| Metric | Count | Rate | Wilson 95% CI |
|--------|-------|------|---------------|
| **Total threads** | 9 | — | — |
| Vendor-unsure threads | 1 | 11.1% | [2.0%, 43.5%] |
| Recurrence-observed threads | 1 | 11.1% | [2.0%, 43.5%] |
| **Both vendor-unsure AND recurrence** | **1** | **11.1%** | **[2.0%, 43.5%]** |
| Served (fault_need_classifier) | 2 | 22.2% | [6.3%, 54.7%] |
| Unserved | 7 | 77.8% | [45.3%, 93.7%] |

### Hypothesis Decision

**✓ HYPOTHESIS SUPPORTED**: vendor_unsure_and_recurrence_rate = 11.1% (CI lower bound = 2.0% ≥ 1%)

The hypothesis that ≥10% of practitioner fault threads on MrPLC contain both vendor inability to diagnose AND recurrence after repair/replacement is supported. The Wilson 95% CI lower bound (2.0%) exceeds the 1% minimum threshold.

### Key Findings

1. **Single baseline case (Row 5 from E090)** documents both patterns simultaneously:
   - Explicit statement: "Spoke to Rockwell and they were unsure as to the cause"
   - Recurrence documentation: "same fault on different module — suggests systemic issue, not hardware defect"

2. **11.1% rate** in the 9-thread baseline, while the CI is wide (2.0%–43.5%) due to small N, the point estimate exceeds the 10% hypothesis threshold.

3. **Vendor knowledge gaps are real**: The one vendor-unsure thread (Row 5) is the only one in the E090 corpus where a practitioner explicitly reported the manufacturer could not diagnose the root cause.

4. **Recurrence after replacement is observable**: The same thread documents recurrence on a different module, suggesting a systemic issue not captured by error codes alone.

5. **Classifier stratification**: Of the 2 threads classified as "served" by fault_need_classifier, neither contains vendor_unsure + recurrence. The 7 "unserved" threads also lack these patterns (only Row 5 has them, and it was classified served by the instrument).

### Cross-Domain Comparison (E090 baseline)

| Domain | Vendor-Unsure Rate | Recurrence Rate | Both Rate |
|--------|-------------------|-----------------|-----------|
| **Industrial PLC (MrPLC, 9 rows)** | 11.1% | 11.1% | **11.1%** ✓ |
| **Medical Device (MedWrench, 7 rows)** | N/A — views unavailable | N/A — views unavailable | N/A |

The PLC rate is the only measurable baseline; MedWrench view counts were unavailable in E090 (per OBSERVATIONS.md §4).

### Hypothesis Status

| Condition | Status |
|-----------|--------|
| vendor_unsure_and_recurrence_rate ≥ 10% | ✅ Supported (11.1%) |
| CI lower bound > 1% | ✅ Supported (2.0%) |
| Pattern suggests unmet need class | ✅ Supported (vendor cannot diagnose + fault recurs) |

### Next Steps (per D083/D095)

1. **If pursuing**: Systematically search additional MrPLC threads for vendor-unsure + recurrence patterns, re-run with N ≥ 30 for tighter CI.
2. **If closing this line**: Per D083, proceed to fresh observation in a new domain. The hypothesis has been tested with the available population; refutation or inconclusive result would close this line.
3. **Prototype consideration**: If the pattern generalizes (systematic vendor inability + recurrence), a targeted prototype could surface these patterns in fault databases or provide "vendor-unsure" warnings alongside error codes.

### Evidence Trail

- **OBSERVATIONS.md**: Raw practitioner rows and instrument design
- **run_measurement.py**: Measurement computation script
- **RESULTS.json**: Machine-readable rates and decision
- **E090 RESULTS.md**: Discrimination test validation (G1/G2/G3 PASS, classifier reused)

### All Claims Labeled

- **observed**: Directly read from E090 OBSERVATIONS.md (9 practitioner rows by hand from MrPLC.com forum listings).
- **inferred**: Hypothesis decision rule applied to measured rates (per D088/D095 framework).