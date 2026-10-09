<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-09
-->

# E079 Classification Rules

## Structured Case Definition

A question is a **structured case** if ALL of the following are true:

1. **Has OBD2 code**: At least one code matching `[PBCU][0-9]{4}` in title or body
2. **Has qualified answer**: At least one answer from user with reputation > 100
3. **Has accepted or high-scored answer**: Accepted answer exists OR answer with score ≥ 3
4. **Answer names root cause**: The accepted/high-scored answer explicitly identifies a specific component, sensor, wiring issue, or subsystem as the root cause
5. **Answer names repair**: The answer describes a repair procedure or part replacement
6. **Vehicle identifiable**: Make, model, year, and engine can be determined from tags or question body

## Root Cause Specificity Levels

| Level | Description | Example | Counts as "Specific Part" (G4) |
|-------|-------------|---------|-------------------------------|
| 0 | No root cause stated | "Check the code definition" | No |
| 1 | Generic diagnostic step | "Check wiring and connectors" | No |
| 2 | System/subsystem | "EVAP system leak" | No |
| 3 | Component category | "O2 sensor" | Borderline |
| 4 | Specific part | "Bank 1 Sensor 1 O2 sensor (part # 234-4622)" | **Yes** |
| 5 | Specific part + procedure | "Replace Bank 1 Sensor 1 O2 sensor, torque to 44 Nm" | **Yes** |

**G4 threshold**: Levels 4-5 count as "names a specific replaceable part". Level 3 is borderline — count as Yes only if part number or exact location (bank/sensor) is given.

## Vehicle Configuration Extraction

From tags (preferred) or question body:
- **Make**: e.g., "toyota", "honda", "ford"
- **Model**: e.g., "camry", "civic", "f-150"
- **Year**: e.g., "2010", "2015-2018"
- **Engine**: e.g., "2.5l", "3.5l v6", "2.0l turbo"

A vehicle config = (make, model, year_range, engine). Year ranges normalized to start year.

## Code Classification

- **Generic (P0xxx, P2xxx, P3xxx)**: Standardized across manufacturers
- **Manufacturer-specific (P1xxx)**: Meanings vary by make
- **Body (Bxxxx)**: Body control module
- **Chassis (Cxxxx)**: ABS, stability control, etc.
- **Network (Uxxxx)**: Communication bus

For G2/G3, we analyze at the full code level (e.g., P0420, not just "P0xxx").

## Incumbent Tool Survey Criteria

For each top-10 code, check these free resources:
1. **OBD-Codes.com** - generic definitions + some vehicle-specific
2. **Engine-Codes.com** - similar
3. **AutoCodes.com** - mobile app + website
4. **Manufacturer TSB databases** (if free access)
5. **YouTube/forums** - not counted as "tools"

A tool "covers" a code if it provides:
- Vehicle-specific root causes (not just generic definition)
- At least 3 distinct vehicle configs with different root causes
- Accessible without paid subscription

## Sampling for Manual Classification (G4)

1. Take all structured cases
2. Group by OBD2 code
3. From top 10 codes, sample 5 cases each (or all if <5)
4. Total sample = 50 cases (or fewer if not enough)
5. Two independent classifiers apply root cause specificity levels
6. Cohen's κ ≥ 0.7 required for reliability
7. G4 passes if ≥ 60% of sampled cases are Level 4-5