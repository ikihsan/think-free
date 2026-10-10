<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-10
-->

# Decision & Continuation — Think Free Session Summary

**Date**: 2026-10-10, Asia/Kolkata  
**Phase**: B — fresh observation in new domain (per D083)

---

## 1. What Was Produced/Observed

### E084 — Industrial Equipment Fault Codes (automated outcome)
- **G1 retrieval**: FAIL (20/30 treatment statements harvested; need ≥30)
- **G2 control validity**: FAIL (accuracy 0.60; threshold ≥0.85)
- **G4 answerability**: FAIL (15/20 top-arrival served/partial; need ≥17/20)
- **G3**: Reporting gate only — Treatment: served=15/20 (75.0%), Control: served=17/30 (56.7%)

### E084 — Industrial Equipment Fault Codes (hand-classification of query texts)
- 35 treatment queries classified based on `query_text` alone:
  - **Served**: 14/35 = **40.0%** (1.00 Mitsubishi, 4.00 Allen-Bradley, 3.00 Siemens, 1.00 Omron, 0.00 Rockwell, 0.00 Schneider)
  - **Partial**: 8/35 = **22.9%**
  - **Unserved**: 13/35 = **37.1%**
- **Brand-specific patterns** (based on query text):
  - **Mitsubishi** (7 queries): 7/7 = **100% served**
  - **Allen-Bradley** (4 queries): 4/4 = **100% served**
  - **Siemens** (11 queries): 3/11 = **27.3% served**, 4/11 = **36.4% unserved**, 4/11 = **36.4% partial**
  - **Rockwell** (7 queries): 0/7 = **0% served**, 3/7 = **42.9% unserved**, 4/7 = **57.1% partial**
  - **Omron** (3 queries): 0/3 = **0% served**, 3/3 = **100% unserved**
  - **Schneider** (3 queries): 0/3 = **0% served**, 3/3 = **100% unserved**

### E081 — Lab Instrument Error Codes (hand-classification of query texts)
- 40 treatment queries classified based on `query_text` alone:
  - **Served**: 20/40 = **50.0%**
  - **Partial**: 4/40 = **10.0%**
  - **Unserved**: 16/40 = **40.0%**
- **Critical finding**: The E081 treatment/control distribution is **identical** when classifying by query text. The domain differentiator observed in the automated outcome (lab = 0% partial vs control = 31.4%) is in **search result content** (titles/snippets), NOT query text.

### E086 — Import Error Reports (population measurement, completed)
- **Discrimination test**: PASSED (G1 FPR=0.067, G2 TPR=1.000, G3 Precision=0.909)
- **Population measurement**: 33 total reports (26 Stack Exchange, 7 GitHub Issues)
  - `module_only` (names module, no distribution): **6/31 = 19.35%** (CI95 [9.19%, 36.28%])
  - `distribution_named`: 15/31 = 48.39%
  - `no_module`: 10/31 = 32.26%
- **Kill gate**: module_only rate 19.35% **EXCEEDS** 1% threshold → **BUILD** decision
- **Key finding**: ~19% of real ImportError/ModuleNotFoundError reports ask "which distribution provides this module?" — the pyprovides resolver has a measured use case

---

## 2. Which Build Decision Changed

| Experiment | Previous Decision | Changed Decision | Reason |
|---|---|---|---|
| **E084** (industrial equipment) | Automated gates FAIL → principle does not generalize | **Confirmed FAIL** for automated approach, but **hand-classification reveals brand-specific patterns** (Mitsubishi/Allen-Bradley = 100% served; Rockwell/Omron/Schneider = 0% served) missed by automated harvest | The differentiator is query-text patterns + brand, not just view_count availability |
| **E081** (lab instrument) | Differentiator observed in search result content | **Reclassified**: differentiator is in search result titles/snippets, NOT query text | Treatment and control have identical 50/10/40 distributions when classified by query text alone |
| **E086** (import errors) | STATE-next-actions.md stated "package-name line closed on measured grounds" | **OPEN**: 19.35% module_only rate well above 1% kill gate; resolver has measured use case | E086's measured demand reopens the line; F108's 0.6% rate was about declared dependencies, not import error reports |

---

## 3. What Remains Unknown

1. **Brand-pattern validity in practitioner forums**: Do Mitsubishi/Allen-Bradley forum users actually find solutions at the observed 100% rate? Do Rockwell/Omron/Schneider users face systematic gaps? This requires reading actual forum threads (the "one step this route never took," per STATE-next-actions.md).

2. **Generalization to other fault domains**: Whether the view-count principle's served fraction generalizes to medical device alarm codes or aviation maintenance fault codes when classifying search result content vs. query text.

3. **Served fraction across domains**: The mission has measured served fractions in only some domains:
   - PyPI: 82.93% active (view-count principle)
   - Discourse/Steam: ~11-17% unserved (view-count principle)
   - Lab instrument (query text): 40% served
   - General computer errors (query text): 50% served
   - Industrial equipment (query text): 40% served
   - Import errors (module_only): 19.35%

4. **Whether the "cheap first step" of hand-reading practitioner rows** (per D088/D095) would reveal served fractions different from query-text classification, since the differentiator in E081 was in search result content.

---

## 4. The Single Most Useful Next Action

**Per D083: "the next session must start from fresh observation in a new domain."**  
**Concrete opportunity (per E088, D088, D095)**: Whether structured fault/error-code domains hold needs that are unserved, where the "cheap first step" — reading practitioner rows by hand before any classifier is written — "is the one step this route never took."

### Action: Fresh Observation in Medical Device Alarm Codes Domain

**Protocol** (minimal, reusable):

1. **Harvest**: 30 search queries for common medical device alarm terms from accessible forums/Q&A sites (e.g., MedWrench, biomedical engineering forums):
   - "infusion pump error code"
   - "defibrillator fault"
   - "patient monitor alarm"
   - "ventilator error"
   - "dialysis machine code"
   - Additional terms as available

2. **Hand-classify** each query by the same rubric (based on `query_text`):
   - `served`: query text contains solution/repair keywords indicating a working guide is findable
   - `partial`: query text contains definition/information keywords but no complete guide
   - `unserved`: query text contains no actionable import/module information

3. **Compute served fraction** with Wilson 95% CI and compare to baselines:
   - Industrial equipment (query text): 40.0% served
   - Lab instrument (query text): 50.0% served  
   - Medical device (query text): **to be measured**

4. **Decision rule**: If the medical device served fraction is **significantly different** from both the 40% industrial baseline and the 50% lab baseline (e.g., >60% or <30%), it would indicate the view-count principle's generalization pattern is domain-specific. If it's close to one baseline, the pattern is consistent.

**Why this action**: This is the exact "cheap first step" the mission has not taken for medical device domains. It follows D083 (fresh observation in new domain), D088 (instrument called, not a local copy), and D095 (discrimination test on labels known by construction before population measurement). It also directly answers the E088-open question of whether structured fault domains hold unserved needs, without building a classifier first.

**Expected output**: A small results file (`results.json` or hand-classification table) with served/partial/unserved counts, brand/term patterns, and a recommendation on whether to (a) proceed to population measurement with the view-count instrument, (b) close the domain, or (c) refine the observation protocol.

---
*Evidence preserved in: EXPERIMENTS/084-*, `EXPERIMENTS/081-*, `EXPERIMENTS/086-*  
*This decision links to: STATE.md §D083, D088, D095; STATE-next-actions.md; MISSION.md*