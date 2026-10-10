# Population Measurement Results

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-10
-->

## Experiment: E090 — Fresh Observation in Structured Fault/Error-Code Domains

### Instrument Validation Status

✅ **Discrimination Test PASSED** (fault_need_classifier_v3)
- G1 (FPR < 0.10): **PASS** (FPR = 0.000, CI95 [0.000, 0.161])
- G2 (TPR > 0.70): **PASS** (TPR = 0.704, CI95 [0.572, 0.809])
- G3 (FNR < 0.30): **PASS** (FNR = 0.296, CI95 [0.191, 0.428])

Per D088/D095: Instrument validated before population measurement.

---

## Population Measurement Results

### Domain 1: Industrial PLC (MrPLC.com) — 9 practitioner rows

| Classification | Count | Rate | Wilson 95% CI |
|----------------|-------|------|---------------|
| Served | 6 | 66.7% | [35.4%, 87.9%] |
| Unserved | 3 | 33.3% | [12.1%, 64.6%] |

**Served rows (community has answers):**
- PLC-2: Timer not counting (204 views, 6 replies)
- PLC-3: Gx Work 2 software error (1,600 views, 3 replies) — **high interest**
- PLC-4: iQ-R communication error codes 1134/C0B2/C709 (688 views, 11 replies)
- PLC-5: HMI TP1200 HMIRTM.EXE crash (472 views, 6 replies)
- PLC-7: Studio 5000 install errors 1606/1722 (123 views, 1 reply)
- PLC-9: NX1P2 HMI timeout errors (1,300 views, 5 replies) — **high interest**

**Unserved rows (no community resolution visible):**
- PLC-1: GuardLogix fault 125/120 — **Rockwell unsure, recurrence after replacement** (0 views, 0 replies on listing)
- PLC-6: Analog input fluctuating (0 views, 0 replies)
- PLC-8: Error -10 No system program (0 views, 0 replies)

**High-interest unserved (views>500, 0 replies, fault language):** 0

---

### Domain 2: Medical Device (MedWrench.com) — 7 practitioner rows

| Classification | Count | Rate | Wilson 95% CI |
|----------------|-------|------|---------------|
| Served | 1 | 14.3% | [2.6%, 51.3%] |
| Unserved | 6 | 85.7% | [48.7%, 97.4%] |

**Served rows:**
- MED-1: Error 10901 on Fuji FCR (8 replies)

**Unserved rows (views not available on MedWrench listings — all 0):**
- MED-2: Service mode access (0 replies)
- MED-3: Patient cable test procedure (3 replies)
- MED-4: Compact flash firmware image (13 replies)
- MED-5: Error E06 + INHIBIT light (0 replies)
- MED-6: Replacement fan part number (2 replies)
- MED-7: Loud screech during processing (1 reply)

**Note**: MedWrench forum listings do not display view counts. All `views=0` in this dataset. The classifier's "high engagement" tier (views>200) cannot trigger. Several threads have substantial replies (MED-4: 13, MED-1: 8, MED-3: 3) but are classified unserved due to missing view data.

---

### Combined Results (16 practitioner rows)

| Classification | Count | Rate |
|----------------|-------|------|
| Served | 7 | 43.8% |
| Unserved | 9 | 56.2% |

---

## Key Findings (Observed)

### 1. Vendor Knowledge Gaps (2 observed)
| Row | Finding |
|-----|---------|
| PLC-1 | **Rockwell unsure of cause** for GuardLogix fault 125/120; same fault recurred after module replacement |
| MED-2 | Practitioner **needs service manual/mode access** — vendor documentation not publicly accessible |

### 2. Recurrence After Fix (1 observed)
| Row | Finding |
|-----|---------|
| PLC-1 | Fault 125/120 **recurred on different module** — suggests systemic issue, not hardware defect |

### 3. Specific Error/Fault Codes Cited (6 of 16 rows = 37.5%)
- PLC-1: 125, 120
- PLC-4: 1134, C0B2, C709 (hex + decimal)
- PLC-7: 1606, 1722 (Windows installer codes)
- PLC-8: -10
- MED-1: 10901
- MED-5: E06, INHIBIT

### 4. High View Counts on Error Threads (2 of 9 PLC rows >1000 views)
- PLC-3: 1,600 views — Gx Work 2 "System stop failed" software error
- PLC-9: 1,300 views — NX1P2 3rd party HMI timeout errors

---

## Instrument Limitations Noted

1. **MedWrench view counts unavailable** — classifier cannot assess "high interest" on medical threads
2. **Conservative default** — threads with views<50 and 0 replies classified unserved (may miss nascent needs)
3. **Forum listing only** — no thread content analysis (vendor acknowledgment, solution quality)

---

## Conclusions

### For Industrial PLC Domain (MrPLC)
- **66.7% of observed fault threads show community engagement** (served)
- **33.3% appear unserved** — including one with **vendor knowledge gap + recurrence**
- Specific error codes are **commonly cited** (4 of 9 rows)
- High view counts on error threads indicate **real practitioner demand**

### For Medical Device Domain (MedWrench)
- **View count instrument not available** — cannot measure independent arrivals
- **Replies present but classifier conservative** due to missing views
- **Service manual/mode access requests** suggest vendor documentation gaps
- **Parts identification needs** (MED-6) are a distinct need class

### Cross-Domain
- **Structured fault/error codes are the norm** in both domains
- **Vendor support gaps exist** and are explicitly stated by practitioners
- **Recurrence after replacement** indicates systemic issues not captured by error codes alone

---

## Next Steps

Per STATE.md D083/D095: This fresh observation is complete. The instrument passed discrimination test and was applied to practitioner rows.

**No candidate emerges from this measurement alone** — the unserved rate (56.2% combined) includes many low-engagement threads. The high-value signals are:
1. PLC-1: Vendor knowledge gap + recurrence (specific, actionable)
2. PLC-3, PLC-9: High view counts on specific errors (demand signal)
3. MED-2, MED-4: Service documentation access needs

**Recommendation**: If pursuing, focus on PLC-1 pattern (vendor-unsure faults with recurrence) as a testable hypothesis with a cheaper experiment: search for "Rockwell unsure" / "vendor unable to diagnose" across MrPLC and measure recurrence rate.

---

## Evidence Trail

- **OBSERVATIONS.md**: Raw practitioner rows collected by hand
- **PROTOCOL.md**: Discrimination test design (pre-declared)
- **run_discrimination_test_v2.py**: Instrument validation (PASSED)
- **measure_population.py**: Population measurement script
- **DISCRIMINATION_TEST.md**: Test probe definitions

All claims labeled **observed** (directly read from public forum listings).