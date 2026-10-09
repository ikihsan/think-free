<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-09
-->

# E083 — Fresh observation: 3D printer firmware/hardware fault codes on Discourse forums

Session `2026-10-09-025`, VM `instance-20260717-0947`, declared 2026-10-09.

## The question

Every need-harvest experiment this mission has run (HN, GitHub Issues, Stack Exchange, CFPB, Discourse) measures **statements of need on platforms** and finds the same confound: "unanswered on a platform is not unserved in reality" (F096). The need-harvest route is closed at the population level (D083).

This experiment tests a fundamentally different surface: **3D printer firmware/hardware fault codes and their real-world root causes on Discourse forums**. These are not statements of need — they are **standardized fault conditions emitted by 3D printer firmware** (Marlin, Klipper, RepRapFirmware, Creality OS, Bambu Lab firmware) with a structured taxonomy:

- **Marlin standardized errors**: `THERMAL RUNAWAY`, `MINTEMP`, `MAXTEMP`, `HEATING FAILED`, `PROBE FAILED`, `HOMING FAILED`, `ERR: ...` codes
- **Klipper error codes**: `MCU 'mcu' shutdown: ...`, `Temperature sensor error`, `Stepper driver error`, `Homing failed`, `Probe error`
- **Creality/Bambu proprietary codes**: Web UI / touchscreen error codes
- **Hardware fault indicators**: `SD CARD ERROR`, `FILE ERROR`, `LAYER SHIFT`, `CLOGGED NOZZLE`, `BED LEVELING FAILED`

Each fault type on a specific printer model/firmware maps to a set of possible root causes (thermistor failure, heater cartridge failure, wiring break, stepper driver overheating, bed probe failure, nozzle clog, belt tension, frame alignment) and repair procedures.

This is a fresh domain (3D printing hardware/firmware debugging), a fresh surface (standardized firmware fault codes + printer specifications), and a fresh population (3D printer operators diagnosing real machines). It has not been read by this mission.

The `view_count` instrument (validated on Stack Exchange in E071 and Discourse in E077) provides **independent arrivals at a fault** — the critical discriminator the mission was missing (F096).

## Protocol

### Data source

**Discourse forums** for 3D printer brands/communities — these publish `view_count` (validated in E077), are accessible without API keys, and cover the 3D printing domain.

Target forums (pre-declared, tested accessible):
1. `forum.creality.com` — Creality printers (Ender, K1, CR, Halot series), Marlin-based firmware
2. `forum.lulzbot.com` — LulzBot printers (TAZ, Mini), Marlin-based firmware
3. `community.home-assistant.io` — Home Assistant (includes 3D printing integrations, Klipper/Moonraker)
4. `community.openhab.org` — openHAB (includes 3D printing, Klipper)
5. `forum.arduino.cc` — Arduino (includes Marlin firmware development, 3D printer controllers)

Alternates (if any primary fails):
- `discourse.ubuntu.com` — Ubuntu (includes 3D printing software, Klipper)
- `meta.discourse.org` — Discourse meta (control)
- `community.anovaculinary.com` — Cooking (negative control, no 3D printing)

### Population definition

A **case** = one Discourse topic that:
1. Contains at least one firmware/hardware fault indicator in title:
   - Marlin error patterns: `THERMAL RUNAWAY`, `MINTEMP`, `MAXTEMP`, `HEATING FAILED`, `PROBE FAILED`, `HOMING FAILED`, `ERR[: ]`, `Error:`, `Marlin.*error`, `firmware.*error`
   - Klipper error patterns: `Klipper.*error`, `MCU.*shutdown`, `Temperature sensor`, `Stepper driver`, `homing failed`, `probe error`, `klipper.*fault`
   - Hardware fault patterns: `clogged nozzle`, `nozzle clog`, `bed leveling failed`, `layer shift`, `SD card error`, `file error`, `filament runout`, `extruder skip`, `under extrusion`, `over extrusion`, `thermal runaway`
   - Creality/printer-specific: `K1.*error`, `Ender.*error`, `CR.*error`, `Halot.*error`, `TAZ.*error`, `Mini.*error`, `LulzBot.*error`
2. Has `view_count > 0` (arrival evidence)
3. Has at least one reply (`reply_count > 0`) — indicates engagement/diagnosis attempt

A **structured case** = a case where the discussion (replies) explicitly states:
- The root cause (specific component: thermistor, heater cartridge, wiring, stepper driver, bed probe, nozzle, belt, frame, mainboard, SD card)
- The repair procedure or part replacement
- Printer model and firmware type (from title, tags, or body)

### Kill gates (predeclared)

| Gate | Threshold | Measurement |
|------|-----------|-------------|
| **G1 Population** | ≥ 100 structured cases across all forums | Count of structured cases in the sample |
| **G2 Fault concentration** | Top 10 fault types cover ≥ 30% of cases | Frequency distribution of fault types |
| **G3 Printer model coverage** | ≥ 10 distinct printer models in top 10 fault types | Unique printer models per top fault type |
| **G4 Root cause specificity** | ≥ 60% of structured cases name a specific replaceable part/repair (not "check wiring" or "update firmware" without specifics) | Manual classification of 50 random structured cases |
| **G5 Incumbent gap** | No single existing free tool covers ≥ 50% of top 10 fault types with printer-specific root causes | Survey of free tools (Marlin docs, Klipper docs, manufacturer wikis, community guides) |

### Falsification conditions

- If **G1 fails**: The population is too small to support a tool → **KILL**
- If **G2 fails**: Fault types are too dispersed (long tail) → no concentration to exploit → **KILL**
- If **G3 fails**: Top fault types don't appear across enough printer models → no cross-model value → **KILL**
- If **G4 fails**: Discussions don't name specific parts → no actionable computational output → **KILL**
- If **G5 fails**: Incumbents already serve the population → no gap → **KILL**

All gates must pass for the candidate to survive.

### Controls

- **Negative control**: Random sample of topics from `community.anovaculinary.com` (cooking) — should have near-zero fault indicator matches
- **Positive control**: Known high-frequency fault types (`THERMAL RUNAWAY`, `MINTEMP`, `clogged nozzle`, `bed leveling failed`) — should appear in top fault types if population is real

### Analysis method

1. Harvest topics from target Discourse forums via `/latest.json` API (stdlib Python, no external deps)
2. Filter for topics with fault indicators in title
3. Classify each topic's fault type from title patterns
4. For structured case assessment: would need reply bodies (requires additional API calls to `/t/{topic_id}.json`) — but for preliminary analysis, title+metadata only evaluates G2 and G3
5. Aggregate by fault type and printer model (extracted from title/tags)
6. Evaluate gates G2, G3 on title+metadata; G1, G4, G5 require reply data or manual review
7. Survey free incumbent tools for top 10 fault types

### Reproducibility

- Discourse API: no key required, polite polling (1 req/sec)
- Fixed date range: latest topics (implicitly recent)
- Random seed for sampling if needed
- All classification criteria documented in `CLASSIFICATION_RULES.md`
- Stdlib Python 3.8 only

### Resource constraints

- 5 primary forums × ~4 pages (30 topics/page) = ~20 requests per forum = ~100 requests total
- Well within polite polling limits
- No authentication required
- Stdlib Python only, no external dependencies