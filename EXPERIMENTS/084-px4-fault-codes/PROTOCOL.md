<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-09
-->

# E084 — Fresh observation: PX4 drone autopilot fault codes as a structured problem population

Session `2026-10-09-026`, VM `instance-20260717-0947`, declared 2026-10-09.

## The question

Every need-harvest experiment this mission has run (HN, GitHub Issues, Stack Exchange, CFPB, Discourse, DIY) measures **statements of need on platforms** and finds the same confound: "unanswered on a platform is not unserved in reality" (F096). The need-harvest route is closed at the population level (D083).

This experiment tests a fundamentally different surface: **PX4 drone autopilot fault conditions and their real-world root causes**. These are not statements of need — they are **standardized fault conditions emitted by PX4 firmware** with a structured taxonomy:
- **EKF (Extended Kalman Filter) failures**: `EKF2 Missing Data`, `EKF2 IMU Mismatch`, `EKF2 GPS Mismatch`, `EKF2 Yaw Mismatch`, `EKF2 Height Mismatch`, `EKF2 Velocity Mismatch`, `EKF2 Acceleration Mismatch`
- **GPS/GNSS issues**: `GPS GLITCH`, `GPS LOST`, `GPS NO FIX`, `GPS HIGH HDOP`, `GPS JAMMING`, `GPS SPOOFING`
- **Sensor failures**: `IMU FAIL`, `MAG FAIL`, `BARO FAIL`, `RANGE FINDER FAIL`, `AIRSPEED FAIL`, `OPTICAL FLOW FAIL`
- **Actuator/Output issues**: `MOTOR FAIL`, `SERVO FAIL`, `ACTUATOR SATURATION`, `OUTPUT OVERLOAD`
- **Preflight/Prearm checks**: `PREFLIGHT CHECK FAILED`, `PREARM CHECK FAILED`, `PREARM GPS CHECK`, `PREARM MAG CHECK`, `PREARM BARO CHECK`
- **Flight mode/failsafe**: `FAILSAFE TRIGGERED`, `LAND MODE TRIGGERED`, `RTL MODE TRIGGERED`, `TERMINATION TRIGGERED`
- **Communication/Link**: `LINK LOST`, `TELEMETRY LOST`, `RC LOST`, `MAVLINK PARSE ERROR`, `HEARTBEAT LOST`
- **Battery/Power**: `BATTERY LOW`, `BATTERY CRITICAL`, `BATTERY FAIL`, `POWER MODULE FAIL`
- **Geofence/Mission**: `GEOFENCE BREACH`, `MISSION FAILED`, `WAYPOINT FAILED`, `TAKEOFF FAILED`, `LANDING FAILED`
- **Flight controller hardware**: `FMU ASSERT`, `FMU RESET`, `FMU OVERHEAT`, `IO FAIL`, `SD CARD ERROR`, `LOG WRITE ERROR`

Each fault type on a specific airframe (multicopter, fixed-wing, VTOL, rover, boat) with specific flight controller hardware (Pixhawk, Cube, Holybro, etc.) maps to a set of possible root causes (sensor failure, wiring, calibration, vibration, interference, software bug, configuration error) and repair/mitigation procedures.

This is a fresh domain (drone autopilot diagnostics), a fresh surface (standardized PX4 fault codes + airframe specifications), and a fresh population (PX4 operators/developers diagnosing real vehicles). It has not been read by this mission.

The `view_count` instrument (validated on Stack Exchange in E071 and Discourse in E077) provides **independent arrivals at a fault** — the critical discriminator the mission was missing (F096).

## Protocol

### Data source

**Discourse forum**: `discuss.px4.io` — the official PX4 community forum. Publishes `view_count` (validated in E077), accessible without API keys via `/latest.json` and `/top.json` endpoints, and covers the PX4 domain comprehensively.

Target forum (pre-declared, tested accessible):
1. `https://discuss.px4.io` — PX4 autopilot community (all categories: Support, Hardware, Software, Simulation, Development, Showcase)

Alternates (if primary fails):
- `https://discuss.ardupilot.org` — ArduPilot community (if Discourse-based)
- `https://forum.dji.com` — DJI forum (if accessible)
- `https://community.uavcan.org` — UAVCAN/DroneCAN community

Negative control (pre-declared):
- `https://meta.discourse.org` — Discourse meta (no PX4 content)

### Population definition

A **case** = one Discourse topic that:
1. Contains at least one PX4 fault indicator in title:
   - EKF patterns: `EKF2`, `EKF.*fail`, `EKF.*mismatch`, `EKF.*error`, `estimator.*fail`, `estimator.*error`
   - GPS patterns: `GPS.*fail`, `GPS.*lost`, `GPS.*glitch`, `GPS.*no fix`, `GPS.*HDOP`, `GNSS.*fail`, `GNSS.*lost`
   - Sensor patterns: `IMU.*fail`, `MAG.*fail`, `BARO.*fail`, `compass.*fail`, `accelerometer.*fail`, `gyro.*fail`, `rangefinder.*fail`, `lidar.*fail`, `optical.flow.*fail`
   - Actuator patterns: `motor.*fail`, `servo.*fail`, `actuator.*fail`, `actuator.*saturat`, `output.*fail`, `ESC.*fail`
   - Preflight patterns: `preflight.*fail`, `prearm.*fail`, `prearm.*check`, `arming.*fail`, `arming.*check`
   - Failsafe patterns: `failsafe`, `land mode.*trigger`, `RTL.*trigger`, `terminat`
   - Communication patterns: `link.*lost`, `telemetry.*lost`, `RC.*lost`, `radio.*lost`, `heartbeat.*lost`, `MAVLink.*error`
   - Battery patterns: `battery.*low`, `battery.*critical`, `battery.*fail`, `power.*fail`, `voltage.*low`
   - Geofence/Mission patterns: `geofence.*breach`, `mission.*fail`, `waypoint.*fail`, `takeoff.*fail`, `landing.*fail`
   - Hardware patterns: `FMU.*assert`, `FMU.*reset`, `FMU.*overheat`, `IO.*fail`, `SD.*card.*error`, `log.*error`, `log.*fail`
   - Generic error patterns: `error:[ ]`, `fault:`, `FAIL:`, `CRITICAL:`, `WARNING:` (when in context of PX4)
2. Has `view_count > 0` (arrival evidence)
3. Has at least one reply (`reply_count > 0`) — indicates engagement/diagnosis attempt

A **structured case** = a case where the discussion (replies) explicitly states:
- The root cause (specific component: GPS module, IMU, magnetometer, barometer, wiring, vibration, calibration, interference, configuration, software bug)
- The repair/mitigation procedure or parameter change
- Airframe type (multicopter, fixed-wing, VTOL, rover, boat) and flight controller hardware (from title, tags, category, or body)
- PX4 version (if mentioned)

### Kill gates (predeclared)

| Gate | Threshold | Measurement |
|------|-----------|-------------|
| **G1 Population** | ≥ 100 structured cases across all categories | Count of structured cases in the sample |
| **G2 Fault concentration** | Top 10 fault types cover ≥ 30% of cases | Frequency distribution of fault types |
| **G3 Airframe coverage** | ≥ 10 distinct airframe/FC combinations in top 10 fault types | Unique airframe/FC per top fault type |
| **G4 Root cause specificity** | ≥ 60% of structured cases name a specific replaceable part/repair/parameter (not "check wiring" or "recalibrate" without specifics) | Manual classification of 50 random structured cases |
| **G5 Incumbent gap** | No single existing free tool covers ≥ 50% of top 10 fault types with airframe-specific root causes | Survey of free tools (PX4 docs, QGroundControl Analyze, MAVLink Inspector, community guides) |

### Falsification conditions

- If **G1 fails**: The population is too small to support a tool → **KILL**
- If **G2 fails**: Fault types are too dispersed (long tail) → no concentration to exploit → **KILL**
- If **G3 fails**: Top fault types don't appear across enough airframes → no cross-airframe value → **KILL**
- If **G4 fails**: Discussions don't name specific parts/parameters → no actionable computational output → **KILL**
- If **G5 fails**: Incumbents already serve the population → no gap → **KILL**

All gates must pass for the candidate to survive.

### Controls

- **Negative control**: Random sample of topics from `meta.discourse.org` — should have near-zero PX4 fault indicator matches
- **Positive control**: Known high-frequency fault types (`EKF2`, `GPS`, `IMU`, `MAG`, `prearm`, `failsafe`, `battery`) — should appear in top fault types if population is real

### Analysis method

1. Harvest topics from `discuss.px4.io` via `/latest.json` and `/top.json` API (stdlib Python, no external deps)
2. Filter for topics with fault indicators in title
3. Classify each topic's fault type from title patterns
4. For structured case assessment: fetch reply bodies via `/t/{topic_id}.json` to evaluate root cause specificity (G4)
5. Aggregate by fault type and airframe/FC (extracted from title, tags, category, or body)
6. Evaluate gates G2, G3 on title+metadata; G1, G4, G5 require reply data or manual review
7. Survey free incumbent tools for top 10 fault types

### Reproducibility

- Discourse API: no key required, polite polling (1 req/sec)
- Fixed date range: latest topics (implicitly recent), plus `/top.json` for historical coverage
- Random seed for sampling if needed
- All classification criteria documented in `CLASSIFICATION_RULES.md`
- Stdlib Python 3.8 only

### Resource constraints

- Discourse API: ~30 topics per page, ~10 pages = ~300 requests
- Well within polite polling limits
- No authentication required
- Stdlib Python only, no external dependencies

### Deliverables

- `raw/topics_page_*.json` — raw topic list pages
- `raw/topic_<id>.json` — raw topic detail for structured cases
- `raw/classified_topics.jsonl` — classified topics with fault type
- `results.json` — aggregated results with gates assessment
- `CLASSIFICATION_RULES.md` — documented classification criteria
- `README.md` — experiment summary and interpretation