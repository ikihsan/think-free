<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-10
-->

# E091 — Vendor-Unsure Fault Recurrence Measurement

## Question

What fraction of practitioner‑reported fault threads on MrPLC.com involve vendor inability to diagnose the root cause, and do those faults exhibit recurrence after module/replacement? This is a focused follow‑up to E090's observation that PLC‑1 documented "Rockwell unsure of cause" with recurrence after module replacement.

## Population

MrPLC.com forum threads that:
- Cite specific error/fault codes (validated by E090 as prevalent)
- Are posted by practitioners (technicians/engineers)
- Are publicly readable without authentication

## Instrument

`fault_need_classifier` — the instrument from E090 that passed its discrimination test (G1 FPR<0.10, G2 TPR>0.70, G3 FNR<0.30). Classifies a thread as:
- `served` — community has answers (high view_count + replies + error codes)
- `unserved` — no community resolution visible

**New classification for E091**: Additionally tags threads with:
- `vendor_unsure` — explicit statement that vendor couldn't diagnose (e.g., "Rockwell unsure," "vendor unable to find cause," "no support from manufacturer")
- `recurrence_observed` — explicit statement that the same fault recurred after repair/replacement

## Hypothesis

A non-trivial fraction (≥ 10%) of fault threads on MrPLC will contain both `vendor_unsure` and `recurrence_observed` statements, indicating a systematic pattern where vendors cannot diagnose and faults recur. This would suggest a class of unmet need that existing tools (even a well‑classified view_count instrument) do not address.

## Gates (predeclared, per D088/D095)

| Gate | Criterion | Kill Condition |
|------|-----------|----------------|
| **G1** | False Positive Rate on known-unserved probes < 0.10 | FAIL → instrument invalid (inherited from E090, already passed) |
| **G2** | True Positive Rate on known-served probes > 0.70 | FAIL → instrument lacks sensitivity (inherited from E090, already passed) |
| **G3** | This experiment has no kill gate on the recurrence measurement itself; the gate is on the classifier (already validated) | — |

**Pass condition**: G1 PASS AND G2 PASS (inherited from E090 discrimination test validation).

## Method

1. **Search MrPLC** for threads matching vendor-unsure + recurrence patterns (or use the 9 practitioner rows already collected by E090 as a baseline)
2. **Extract** for each thread: title, error codes, view_count, reply_count, vendor_unsured flag, recurrence_observed flag
3. **Classify** each thread using `fault_need_classifier`
4. **Compute** rates:
   - `vendor_unsure_rate` = threads with vendor_unsure / total threads
   - `recurrence_rate` = threads with recurrence_observed / total threads
   - `vendor_unsure_and_recurrence_rate` = threads with both / total threads
   - Combined served/unserved rates stratified by vendor_unsure/recurrence
5. **Compare** against the E090 baseline (9 rows, 1 vendor-unsure + recurrence case)

## Success Region (per D088)

- Minimum 30 threads searched (to achieve statistical power for rate measurement)
- FPR < 0.10 and TPR > 0.70 on the classifier (already validated in E090)
- Recurrence rate and vendor-unsure rate computed with Wilson 95% CI
- If vendor_unsure_and_recurrence_rate ≥ 10% with CI lower bound > 0: **evidence of systematic pattern** — next step would be a targeted prototype
- If vendor_unsure_and_recurrence_rate < 1%: **pattern is rare** — closes this hypothesis line

## Evidence Trail

- PROTOCOL.md: Pre‑declared experiment design
- run_measurement.py: Measurement script
- OBSERVATIONS.md: Raw thread observations extracted from MrPLC
- RESULTS.md: Computed rates and conclusions
- run_discrimination_test.py: Instrument validation (from E090, reused)

---

# Run the discrimination test (inherited from E090)

This uses the same test harness as E090 to confirm the classifier still passes before proceeding to population measurement.

```python
#!/usr/bin/env python3
"""Run the E090 discrimination test to validate the classifier before E091 measurement."""
```

## Next Steps

If the classifier passes (G1/G2 from E090): proceed to population measurement on practitioner rows, computing vendor_unsure and recurrence rates.

If the classifier fails: redesign instrument (per D095: "must not start from classify_served over Bing in an eighth domain") and retest.

---

**Per D083/D095**: This experiment extends the fresh observation line started in E090 without revisiting a settled result. It measures a concrete hypothesis (vendor-unsure + recurrence pattern) that was flagged in E090's observations but not quantified.