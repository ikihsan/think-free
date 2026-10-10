<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-09
-->

# E084 — Classification rules for PX4 fault codes

Session `2026-10-09-026`, VM `instance-20260717-0947`, declared 2026-10-09.

## Fault type classification (from title)

Each topic title is matched against patterns in order. First match wins.

### 1. EKF (Extended Kalman Filter) failures
Patterns (case-insensitive):
- `EKF2`
- `EKF.*fail`
- `EKF.*mismatch`
- `EKF.*error`
- `estimator.*fail`
- `estimator.*error`
- `EKF.*reset`
- `EKF.*diverg`

Label: `EKF_FAILURE`

### 2. GPS/GNSS issues
Patterns:
- `GPS.*fail`
- `GPS.*lost`
- `GPS.*glitch`
- `GPS.*no.fix`
- `GPS.*HDOP`
- `GNSS.*fail`
- `GNSS.*lost`
- `GPS.*jam`
- `GPS.*spoof`
- `GPS.*drift`
- `GPS.*accuracy`

Label: `GPS_ISSUE`

### 3. Sensor failures (IMU, MAG, BARO, etc.)
Patterns:
- `IMU.*fail`
- `MAG.*fail`
- `compass.*fail`
- `BARO.*fail`
- `barometer.*fail`
- `accelerometer.*fail`
- `gyro.*fail`
- `rangefinder.*fail`
- `lidar.*fail`
- `optical.flow.*fail`
- `flow.*fail`
- `airspeed.*fail`
- `sensor.*fail`
- `sensor.*error`

Label: `SENSOR_FAILURE`

### 4. Actuator/Output issues
Patterns:
- `motor.*fail`
- `servo.*fail`
- `actuator.*fail`
- `actuator.*saturat`
- `output.*fail`
- `ESC.*fail`
- `thrust.*fail`
- `propeller.*fail`

Label: `ACTUATOR_FAILURE`

### 5. Preflight/Prearm checks
Patterns:
- `preflight.*fail`
- `prearm.*fail`
- `prearm.*check`
- `arming.*fail`
- `arming.*check`
- `preflight.*check`
- `can.not.arm`
- `cannot.arm`
- `arming.*denied`

Label: `PREARM_FAILURE`

### 6. Failsafe/Flight mode triggers
Patterns:
- `failsafe`
- `land.mode.*trigger`
- `RTL.*trigger`
- `return.to.launch.*trigger`
- `terminat`
- `emergency.*land`
- `failsafe.*trigger`

Label: `FAILSAFE_TRIGGER`

### 7. Communication/Link loss
Patterns:
- `link.*lost`
- `telemetry.*lost`
- `RC.*lost`
- `radio.*lost`
- `heartbeat.*lost`
- `MAVLink.*error`
- `MAVLink.*fail`
- `connection.*lost`
- `mavlink.*parse`

Label: `LINK_LOSS`

### 8. Battery/Power issues
Patterns:
- `battery.*low`
- `battery.*critical`
- `battery.*fail`
- `power.*fail`
- `power.*module.*fail`
- `voltage.*low`
- `cell.*low`
- `battery.*warning`

Label: `BATTERY_ISSUE`

### 9. Geofence/Mission failures
Patterns:
- `geofence.*breach`
- `geofence.*fail`
- `mission.*fail`
- `waypoint.*fail`
- `takeoff.*fail`
- `landing.*fail`
- `mission.*error`

Label: `MISSION_FAILURE`

### 10. Flight controller hardware issues
Patterns:
- `FMU.*assert`
- `FMU.*reset`
- `FMU.*overheat`
- `IO.*fail`
- `SD.*card.*error`
- `SD.*card.*fail`
- `log.*error`
- `log.*fail`
- `logging.*fail`
- `flash.*error`
- `boot.*fail`

Label: `HARDWARE_FAILURE`

### 11. Vibration/Mechanical
Patterns:
- `vibration`
- `vibe.*fail`
- `vibe.*high`
- `mechanical.*fail`
- `frame.*fail`
- `mount.*fail`

Label: `VIBRATION_ISSUE`

### 12. Configuration/Parameter issues
Patterns:
- `parameter.*error`
- `config.*error`
- `param.*wrong`
- `parameter.*mismatch`
- `tuning.*fail`
- `PID.*fail`
- `tune.*fail`

Label: `CONFIG_ISSUE`

### 13. Generic/Other
Patterns:
- `error:`
- `fault:`
- `FAIL:`
- `CRITICAL:`
- `WARNING:` (when clearly PX4-related)

Label: `GENERIC_ERROR`

---

## Airframe type extraction (from title, tags, category, body)

Keywords → Airframe type:
- `multicopter`, `quad`, `quadcopter`, `hexacopter`, `octocopter`, `coaxial` → `MULTICOPTER`
- `fixed.wing`, `fixedwing`, `plane`, `airplane`, `VTOL.quad`, `VTOL.fixed`, `tailsitter`, `quadplane` → `FIXED_WING` or `VTOL`
- `VTOL`, `tiltrotor`, `tailsitter`, `quadplane` → `VTOL`
- `rover`, `rover`, `ground`, `UGV` → `ROVER`
- `boat`, `usv`, `surface`, `ship` → `BOAT`
- `sub`, `rov`, `uuv`, `underwater` → `SUBMARINE`

If none found: `UNKNOWN`

---

## Flight controller hardware extraction

Keywords → FC type:
- `Pixhawk` → `PIXHAWK`
- `Cube` (Orange, Black, Green, Purple) → `CUBE`
- `Holybro` → `HOLYBRO`
- `CUAV` → `CUAV`
- `mRo` → `MRO`
- `Drotek` → `DROTEK`
- `Holybro` → `HOLYBRO`
- `STM32` (generic) → `STM32_GENERIC`
- `FMUv` (FMUv5, FMUv6, etc.) → `FMU`

If none found: `UNKNOWN`

---

## Root cause specificity classification (for G4)

For structured cases (topics with replies that diagnose the issue), classify the root cause mention as:

**SPECIFIC** (counts toward G4 threshold) — names a specific replaceable part, parameter, or concrete action:
- Specific component: "GPS module", "IMU", "magnetometer", "barometer", "ESC", "motor", "servo", "wiring harness", "connector", "SD card", "flight controller"
- Specific parameter: "EKF2_GPS_DELAY", "GPS_HDOP_MAX", "IMU_GYRO_CUTOFF", "MAG_CAL", "BAT_CRIT_THR"
- Specific action: "replace GPS module", "recalibrate magnetometer", "check IMU vibration damping", "update firmware to v1.14.3", "set EKF2_AID_MASK to 0", "replace ESC", "resolder connector"

**GENERIC** (does NOT count toward G4 threshold) — vague or non-actionable:
- "check wiring"
- "recalibrate"
- "update firmware" (without version)
- "check connections"
- "inspect hardware"
- "debug further"
- "contact manufacturer"
- "it's a known issue"
- "check logs" (without specific log message)

**UNCLEAR** — cannot determine from available text

---

## Structured case criteria

A topic is a **structured case** if ALL of:
1. Has at least one reply (`reply_count > 0`)
2. At least one reply explicitly identifies a root cause (matches SPECIFIC or GENERIC above)
3. At least one reply suggests a repair/mitigation/parameter change
4. Airframe type or FC hardware is identifiable (from title, tags, category, or body)

---

## Incumbent tool survey criteria (for G5)

For each top 10 fault type, check if any single free tool provides:
- Airframe-specific root cause mapping
- Parameter-specific remediation
- Automated diagnosis from log (ULog) or error code

Tools to survey:
- PX4 User Guide / Developer Guide (docs.px4.io)
- QGroundControl Analyze / MAVLink Inspector
- PX4 Log Analyzer (pyulog, plotjuggler)
- MAVLink Router / MAVProxy
- Community wikis (PX4, ArduPilot, DIYDrones)
- Manufacturer wikis (Holybro, CUAV, CubePilot, mRo)
- GitHub issues/discussions (PX4-Autopilot/PX4-Autopilot)

A tool "covers" a fault type if it provides a diagnostic flowchart or automated analysis that maps the fault code to root causes for at least 3 distinct airframe/FC combinations.