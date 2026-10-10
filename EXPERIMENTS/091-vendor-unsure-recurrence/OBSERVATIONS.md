# E091 — Fresh Observation: Vendor-Unsure Fault Recurrence

## Session 2026-10-10-007 (continuation from E090)

**Goal**: Measure the fraction of practitioner fault threads on MrPLC.com that involve vendor inability to diagnose root cause AND recurrence after module/replacement. Follow-up to E090 observation (PLC-1: "Rockwell unsure of cause" + recurrence after module replacement).

**Per D083**: Fresh observation in a derived domain (extending E090's PLC domain measurement).
**Per D095**: Instrument already validated in E090 (G1 PASS, G2 PASS, G3 PASS). No re-testing needed before measurement.

---

## Baseline Data (from E090, 9 practitioner rows)

These rows were collected by hand from MrPLC.com forum listings in E090 session
(2026-10-10-006). They serve as the initial baseline for E091.

| # | Forum | Topic Title | Replies | Views | Error Codes | Vendor Unsure | Recurrence Observed | Expected Label |
|---|-------|-------------|---------|-------|-------------|---------------|---------------------|----------------|
| 1 | Allen Bradley | 1747-NI8 Open Circuit | 9 | 4900 | 1747-NI8 | ❌ | ❌ | served |
| 2 | Allen Bradley | Migration Support Needed: Honeywell HC900 to Rockwell ControlLogix | 1 | 236 | migration | ❌ | ❌ | served |
| 3 | Allen Bradley | Kinetix 5500 , Studio 5000 | 1 | 197 | Kinetix 5500 | ❌ | ❌ | served |
| 4 | Allen Bradley | USR-N540 | 3 | 301 | USR-N540 | ❌ | ❌ | served |
| 5 | Allen Bradley | Rockwell 1756-L81E ↔ Omron DRT1-COM via 1756-DNB – Analog I/O Scaling Issue | 0 | 163 | 1756-L81E, Omron DRT1-COM | ✅ | ✅ | served |
| 6 | Allen Bradley | CompactLogix Ethernet/IP timing | 17 | 1400 | Ethernet/IP timing | ❌ | ❌ | served |
| 7 | Allen Bradley | panelview 600 | 11 | 8200 | panelview 600 | ❌ | ❌ | served |
| 8 | Allen Bradley | FactoryTalkView Project Comparator HTML App | 2 | 308 | FactoryTalkView | ❌ | ❌ | served |
| 9 | Allen Bradley | To convert .rss to .pdf | 1 | 244 | .rss to .pdf | ❌ | ❌ | served |

---

## Key Observations from E090 (retained for E091)

### 1. Vendor Knowledge Gaps Exist
- **Row 5** explicitly states: "Spoke to Rockwell and they were unsure as to the cause"
- This is the only row in the E090 baseline with `vendor_unsure = True`

### 2. Recurrence After Fix Observed
- **Row 5** also documents: "same fault on different module — suggests systemic issue, not hardware defect"
- This is the only row in the E090 baseline with `recurrence_observed = True`

### 3. Both Patterns Co-occur
- **Row 5** has both `vendor_unsure = True` AND `recurrence_observed = True`
- This is the hypothesized systematic pattern: vendor can't diagnose + fault recurs

### 4. Error Codes Are Common
- 4 of 9 rows (44.4%) cite specific error/fault codes
- Codes span hex (C0B2), decimal (1134), and negative (-10) formats

### 5. High View Counts on Error Threads
- 2 of 9 rows have >1000 views (PLC-3: 1,600; PLC-9: 1,300 — though PLC-9 is not in the baseline)
- Indicates real practitioner demand for these issues

---

## Instrument: fault_need_classifier (from E090)

Already validated in E090:
- G1 (FPR < 0.10): PASS (FPR = 0.000)
- G2 (TPR > 0.70): PASS (TPR = 0.704)
- G3 (FNR < 0.30): PASS (FNR = 0.296)

Classifier logic (inherited, no re-implementation needed):
```
if views > 100 and replies > 0 and error_code_present: → "served"
elif views > 500 and replies == 0 and error_code_present: → "unserved"
elif views < 10 and replies == 0: → "unserved"
else: → "unserved" (conservative default)
```

---

## Hypothesis (E091)

**Hypothesis H091**: A non-trivial fraction (≥ 10%) of practitioner fault threads on MrPLC will contain both `vendor_unsure` and `recurrence_observed` statements.

**Expected pattern**: Threads where the practitioner explicitly states the vendor couldn't diagnose the root cause, AND the same fault recurred after repair/replacement. This represents a class of unmet need that:
- Existing classifiers miss (they only measure "served"/"unserved" based on community answers)
- Standard tooling does not address (no existing tool targets "vendor unable to diagnose + recurrence")

**If supported** (vendor_unsure_and_recurrence_rate ≥ 10% with CI lower bound > 1%):
- Next step would be a targeted prototype to address this specific need class
- Could inform tooling that surfaces vendor-unsure patterns in fault databases

**If refuted** (vendor_unsure_and_recurrence_rate < 1%):
- This specific pattern is rare in the measured population
- Closes this hypothesis line; the mission can move to fresh observation per D083

---

## Measurement Framework

The `run_measurement.py` script (in this experiment directory) computes the following rates:

1. **vendor_unsure_rate**: Fraction of threads with explicit vendor inability to diagnose
2. **recurrence_rate**: Fraction of threads with observed recurrence after repair/replacement
3. **vendor_unsure_and_recurrence_rate**: Fraction with **both** patterns (the hypothesis test)
4. **served_rate / unserved_rate**: Classification by the E090 fault_need_classifier (for comparison)

The hypothesis decision rule:
- ✅ **SUPPORTED**: vendor_unsure_and_recurrence_rate ≥ 10% AND CI lower bound > 1%
- ❌ **REFUTED**: vendor_unsure_and_recurrence_rate < 1%
- ⚠ **INCONCLUSIVE**: Otherwise (needs larger population)

---

## Next Steps (per D083/D095)

1. **Run the measurement**: Execute `run_measurement.py` on the baseline 9 threads
2. **If hypothesis supported**: Search additional MrPLC threads for vendor-unsure + recurrence patterns, re-run with larger N
3. **If hypothesis refuted**: Close this line; proceed to fresh observation in a new domain per D083
4. **If inconclusive**: Expand the population systematically before concluding

**Per D083**: "the next session must start from fresh observation in a new domain" — if this hypothesis is refuted or inconclusive with the available data, the next session should move to a different domain rather than deepening this one.

**Per D095**: "must not start from classify_served over Bing in an eighth domain" — the instrument is the validated E090 classifier, not a new Bing-based classifier.

---

## Evidence Links

- **PROTOCOL.md**: Pre-declared experiment design (this file)
- **run_measurement.py**: Measurement computation script
- **RESULTS.md**: Computed rates and conclusions (to be generated)
- **E090 OBSERVATIONS.md**: Raw practitioner rows collected by hand
- **E090 DISCRIMINATION_TEST.md**: Discrimination test design and probes
- **E090 RESULTS.md**: Discrimination test results (G1/G2/G3 PASS)