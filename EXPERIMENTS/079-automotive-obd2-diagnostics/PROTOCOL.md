<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-09
-->

# E079 — Fresh observation: Automotive OBD2 diagnostic codes as a structured problem population

Session `2026-10-09-021`, VM `instance-20260717-0947`, declared 2026-10-09.

## The question

Every need-harvest experiment this mission has run (HN, GitHub Issues, Stack Exchange, CFPB, Discourse, DIY) measures **statements of need on platforms** and finds the same confound: "unanswered on a platform is not unserved in reality" (F096). The need-harvest route is closed at the population level (D083).

This experiment tests a fundamentally different surface: **Automotive OBD2 diagnostic trouble codes (DTCs) and their real-world root causes**. These are not statements of need — they are **standardized fault codes emitted by vehicle ECUs** with a structured taxonomy (P0xxx generic powertrain, P1xxx manufacturer-specific, P2xxx generic powertrain 2, P3xxx generic powertrain 3, Bxxxx body, Cxxxx chassis, Uxxxx network). Each code on a specific vehicle (make/model/year/engine) maps to a set of possible root causes and repair procedures.

This is a fresh domain (automotive repair), a fresh surface (standardized diagnostic codes + vehicle specifications), and a fresh population (technicians diagnosing real vehicles). It has not been read by this mission.

## Protocol

### Data source

**Mechanics Stack Exchange** (mechanics.stackexchange.com) — a Stack Exchange site dedicated to automotive repair questions. Questions are tagged with vehicle make/model, and often include OBD2 codes in the title or body. Answers from professional technicians provide root cause diagnoses and repair procedures.

Alternative/backup: **r/mechanicadvice** Reddit community (via Pushshift/API), but Stack Exchange has better structure (tags, accepted answers, voting).

### Population definition

A **case** = one Mechanics.SE question that:
1. Contains at least one OBD2 code (pattern: `[PBCU][0-9]{4}`) in title or body
2. Has at least one answer from a user with >100 reputation (proxy for technician)
3. Has an accepted answer OR an answer with score ≥ 3

A **structured case** = a case where the accepted/high-scored answer explicitly states:
- The root cause (specific component, wiring, sensor, etc.)
- The repair procedure or part replacement
- Vehicle make, model, year, engine (from tags or body)

### Kill gates (predeclared)

| Gate | Threshold | Measurement |
|------|-----------|-------------|
| **G1 Population** | ≥ 200 structured cases | Count of structured cases in the sample |
| **G2 Code concentration** | Top 10 codes cover ≥ 30% of cases | Frequency distribution of OBD2 codes |
| **G3 Vehicle coverage** | ≥ 15 distinct make/model/year/engine combinations in top 10 codes | Unique vehicle configs per top code |
| **G4 Root cause specificity** | ≥ 60% of structured cases name a specific replaceable part (not "check wiring" or "diagnose further") | Manual classification of 50 random structured cases |
| **G5 Incumbent gap** | No single existing free tool covers ≥ 50% of top 10 codes with vehicle-specific root causes | Survey of free OBD2 code databases (OBD-Codes.com, Engine-Codes.com, AutoCodes.com, etc.) |

### Falsification conditions

- If **G1 fails**: The population is too small to support a tool → **KILL**
- If **G2 fails**: Codes are too dispersed (long tail) → no concentration to exploit → **KILL**
- If **G3 fails**: Top codes don't appear across enough vehicles → no vehicle-specific value → **KILL**
- If **G4 fails**: Answers don't name specific parts → no actionable computational output → **KILL**
- If **G5 fails**: Incumbents already serve the population → no gap → **KILL**

All gates must pass for the candidate to survive.

### Controls

- **Negative control**: Random sample of Mechanics.SE questions WITHOUT OBD2 codes — should have lower structure rate
- **Positive control**: Known high-frequency codes (P0300, P0420, P0171, P0442) — should appear in top codes if population is real

### Analysis method

1. Fetch Mechanics.SE questions via Stack Exchange API (tagged with common makes, or search for OBD2 code patterns)
2. Filter for questions with OBD2 codes
3. Classify each question's answers for root cause specificity
4. Aggregate by OBD2 code and vehicle config
5. Evaluate gates
6. Survey free incumbent tools for top 10 codes

### Reproducibility

- Stack Exchange API key (optional, increases quota)
- Fixed date range for sampling
- Random seed for sampling
- All classification criteria documented in `CLASSIFICATION_RULES.md`