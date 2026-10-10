<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-09
-->

# E084 — Fresh observation: PX4 drone autopilot fault codes

**Session**: `2026-10-09-026`, VM `instance-20260717-0947`
**Date**: 2026-10-09
**Status**: Complete — **KILLED by G1 (Population)**

## Summary

This experiment tested whether PX4 drone autopilot fault codes discussed on the official community forum (`discuss.px4.io`) form a viable population for a diagnostic tool candidate.

**Result**: The population is too small (~39 estimated structured cases vs. 100 required). **No candidate emerges.**

## Methodology

Following the fresh observation protocol (D083, E065):
1. **Predeclared protocol** (`PROTOCOL.md`) with kill gates G1–G5
2. **Predeclared classification rules** (`CLASSIFICATION_RULES.md`)
3. **Stdlib Python only** — no external dependencies
4. **Discourse API** — polite polling (1 req/sec), no authentication
5. **Negative control** — `meta.discourse.org` (6.7% false positive rate)

## Data Collection

| Source | Pages | Topics |
|--------|-------|--------|
| `/latest.json` | 15 | 450 |
| `/top.json?period=all` | 5 | 250 |
| `/top.json?period=yearly` | 5 | 250 |
| `/top.json?period=monthly` | 1 | 42 |
| **Total unique** | | **854** |

Filtered for fault indicators in title → 54 topics (6.3%)
Qualified (views>0, replies>0) → 36 topics
Structured cases (sample of 36, fetched details) → 26/36 (72%)

## Gate Evaluation

| Gate | Result | Detail |
|------|--------|--------|
| **G1 Population** | **FAIL** | ~39 estimated structured cases (< 100) |
| **G2 Concentration** | PASS | 100% (only 8 fault types) |
| **G3 Airframe coverage** | PASS* | 17 distinct airframe/FC combos (from post bodies) |
| **G4 Root cause specificity** | PASS | 88.9% SPECIFIC (32/36) |
| **G5 Incumbent gap** | PENDING | Not surveyed (G1 killed) |

*G3 fails on title-only (6 combos), passes with post-body extraction.

## Fault Type Distribution (36 qualified topics)

| Fault Type | Count | Percentage |
|------------|-------|------------|
| EKF_FAILURE | 12 | 33.3% |
| FAILSAFE_TRIGGER | 6 | 16.7% |
| ACTUATOR_FAILURE | 4 | 11.1% |
| SENSOR_FAILURE | 4 | 11.1% |
| VIBRATION_ISSUE | 3 | 8.3% |
| PREARM_FAILURE | 3 | 8.3% |
| GPS_ISSUE | 3 | 8.3% |
| HARDWARE_FAILURE | 1 | 2.8% |

## Root Cause Specificity (G4)

| Classification | Count | Percentage |
|----------------|-------|------------|
| SPECIFIC | 32 | 88.9% |
| MIXED | 1 | 2.8% |
| UNCLEAR | 3 | 8.3% |
| GENERIC | 0 | 0.0% |

**G4 threshold (≥60% SPECIFIC): EXCEEDED**

Examples of SPECIFIC root causes:
- "Replace GPS module, set EKF2_GPS_DELAY to 220ms"
- "Recalibrate magnetometer, check for interference from power cables"
- "Resolder IMU connector, vibration damping mount failed"
- "Update to v1.14.3, fixes EKF2 yaw mismatch bug"
- "Replace ESC, motor 3 output saturated"

## Airframe/FC Coverage (from post bodies)

17 distinct combinations in structured cases:
- ROVER + PIXHAWK, ROVER + UNKNOWN, ROVER + FMU, ROVER + STM32_GENERIC
- MULTICOPTER + PIXHAWK, MULTICOPTER + CUBE, MULTICOPTER + CUAV, MULTICOPTER + HOLYBRO, MULTICOPTER + UNKNOWN
- VTOL + PIXHAWK (2)
- FIXED_WING + UNKNOWN
- BOAT + PIXHAWK, BOAT + UNKNOWN
- SUBMARINE + PIXHAWK (2), SUBMARINE + HOLYBRO, SUBMARINE + UNKNOWN

## Why This Matters

This experiment demonstrates that **practitioners do provide specific, actionable diagnoses** when they discuss faults (G4 PASS), and **fault types do cross airframe boundaries** (G3 PASS with post-body data). The failure is purely **population volume** — the PX4 forum doesn't generate enough fault-diagnosis threads.

This is the **third fresh observation** in this mission to fail on population grounds:
1. **E079** (Automotive OBD2 on Mechanics.SE): G2 FAIL (concentration 29% < 30%)
2. **E083** (3D printer faults on Discourse): G3 FAIL (1.8 models/fault, brand silos)
3. **E084** (PX4 faults on Discourse): **G1 FAIL (~39 cases < 100)**

All three domains have standardized fault codes and real practitioners, but none yield a viable population for a tool candidate under the mission's gates.

## Reproducibility

```bash
cd EXPERIMENTS/084-px4-fault-codes
python3 harvest.py      # Harvest topics (5-10 min)
python3 measure.py      # Evaluate G1-G3 (title-only)
python3 fetch_details.py # Fetch details for G4 (2-3 min)
```

All scripts use stdlib Python 3.8+, no external dependencies.

## Next Steps

Per D083: **Fresh observation in a new domain.** The mission has now tested:
- Software need statements (HN, GitHub, Stack Exchange) — retired
- Automotive OBD2 — killed (concentration)
- 3D printer faults — killed (brand silos / cross-model coverage)
- PX4 drone faults — killed (population size)

Remaining priority domains from `STATE-next-actions.md`:
- Industrial equipment fault codes (PLC/SCADA) — forums block access
- Medical device alarm codes — FDA MAUDE accessible but narrative, not standardized codes
- Laboratory instrument error codes — unknown accessibility
- Aviation maintenance fault codes — Aviation Stack Exchange exists but API throttled

The search continues for a domain with: (1) standardized fault codes, (2) accessible practitioner discussions, (3) sufficient volume, (4) cross-model coverage, (5) specific root causes, (6) incumbent gap.