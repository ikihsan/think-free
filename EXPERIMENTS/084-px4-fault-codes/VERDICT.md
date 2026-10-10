<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-09
-->

# E084 — Verdict: PX4 fault code fresh observation

**Session**: `2026-10-09-026`, VM `instance-20260717-0947`
**Date**: 2026-10-09
**Outcome**: **KILLED — G1 (Population) fails**

## Gate Results

| Gate | Threshold | Measured | Status |
|------|-----------|----------|--------|
| **G1 Population** | ≥ 100 structured cases | ~39 estimated (54 fault topics × 48% structured rate) | **FAIL** |
| **G2 Fault concentration** | Top 10 ≥ 30% | 100% (only 8 fault types total) | **PASS** |
| **G3 Airframe coverage** | ≥ 10 distinct airframe/FC combos | 6 from titles; **17 from post bodies** | **PASS*** |
| **G4 Root cause specificity** | ≥ 60% SPECIFIC | 88.9% (32/36) | **PASS** |
| **G5 Incumbent gap** | No single tool covers ≥ 50% | Not surveyed | **PENDING** |

*G3 passes when airframe/FC extracted from post bodies (not just titles).

## Key Findings

### Population (G1) — INSUFFICIENT
- 854 unique topics harvested from `discuss.px4.io` (latest + top/all + top/yearly + top/monthly)
- 54 topics contain PX4 fault indicators in title (6.3%)
- 36 qualified topics (views > 0, replies > 0)
- 26/36 sampled topics are structured cases (explicit root cause + repair + airframe/FC)
- **Estimated total structured cases: ~39** (54 × 26/36)
- **Well below the 100-case threshold**

The PX4 forum simply doesn't generate enough fault-diagnosis discussions to support a tool. Most discussions are about development, hardware selection, simulators, and feature requests — not field fault diagnosis.

### Fault Concentration (G2) — HIGH (but trivial)
- Only 8 distinct fault types found in qualified topics
- Top type: `EKF_FAILURE` (33%), `FAILSAFE_TRIGGER` (17%), `ACTUATOR_FAILURE` (11%), `SENSOR_FAILURE` (11%)
- 100% concentration is an artifact of small population, not true concentration

### Airframe Coverage (G3) — GOOD (with post-body extraction)
- Titles alone: 6 combos (mostly UNKNOWN)
- Post bodies: 17 distinct airframe/FC combinations across structured cases
- Covers MULTICOPTER, FIXED_WING, VTOL, ROVER, BOAT, SUBMARINE
- FC hardware: PIXHAWK, CUBE, HOLYBRO, CUAV, FMU, STM32_GENERIC, MRO
- **Cross-airframe value exists** — same fault types appear on different platforms

### Root Cause Specificity (G4) — EXCELLENT
- 88.9% of discussions name specific replaceable parts/parameters
- Examples: "replace GPS module", "set EKF2_GPS_DELAY", "recalibrate magnetometer", "resolder connector", "update to v1.14.3"
- 0% GENERIC-only ("check wiring", "recalibrate" without specifics)
- Practitioners **do** provide actionable diagnoses

### Incumbent Gap (G5) — UNKNOWN
- Not surveyed due to G1 failure
- Likely gap exists: PX4 docs/QGroundControl Analyze provide generic guidance, not airframe-specific automated diagnosis

## Negative Control
- `meta.discourse.org` (Discourse meta): 2/30 false positives (6.7%)
- Matches were "sensor" in "CSS pseudo-elements" and "assets" — not PX4-related
- Classification precision acceptable with refined patterns

## Conclusion

**The PX4 fault code population is too small to support a tool candidate.** 

Despite excellent root cause specificity (G4) and cross-airframe coverage (G3), the fundamental population size (G1) fails by a factor of ~2.5×. The forum's discussion volume focuses on development and configuration, not field fault diagnosis.

This is consistent with the pattern observed in prior fresh observations:
- E079 (Automotive OBD2): G2 FAIL (29% vs 30% concentration)
- E083 (3D printer fault codes): G2 PASS (73%) but G3 FAIL (1.8 models/fault due to brand silos)
- E084 (PX4 fault codes): G2 PASS, G3 PASS, G4 PASS, but **G1 FAIL**

**No candidate emerges.** The fresh observation seat remains empty.

## Evidence Files

- `raw/harvest_summary.json` — Harvest statistics
- `raw/classified_topics.jsonl` — 36 qualified topics with fault type
- `raw/topic_details/topic_*.json` — Full topic details for 36 sampled topics
- `raw/structured_cases.jsonl` — 26 structured cases with root cause classification
- `results.json` — Automated gate evaluation (title-only)
- `g4_assessment.json` — Detailed G4 assessment with post-body enrichment
- `CLASSIFICATION_RULES.md` — Predeclared classification criteria
- `PROTOCOL.md` — Predeclared experiment protocol