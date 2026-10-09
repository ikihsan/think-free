<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-09
-->

# E082 — Fresh observation: Microcontroller fault/exception codes as a structured problem population

Session `2026-10-09-024`, VM `instance-20260717-0947`, declared 2026-10-09.

## The question

Every need-harvest experiment this mission has run (HN, GitHub Issues, Stack Exchange, CFPB, Discourse, DIY, Mechanics.SE, Medical Devices) measures **statements of need on platforms** and finds the same confound: "unanswered on a platform is not unserved in reality" (F096). The need-harvest route is closed at the population level (D083).

This experiment tests a fundamentally different surface: **Microcontroller fault/exception codes and their real-world root causes**. These are not statements of need — they are **standardized fault conditions emitted by MCU hardware** with a structured taxonomy:

- **ARM Cortex-M standardized faults**: HardFault, MemManage, BusFault, UsageFault, SecureFault (ARMv8-M)
- **Vendor-specific fault status registers**: STM32 HFSR/CFSR/DFSR/AFSR, NXP LPC fault registers, TI TMS570/CC26xx/CC13xx fault sources, Microchip PIC/SAM fault sources, Espressif ESP32 exception causes
- **Peripheral-specific fault codes**: USB PHY errors, Ethernet MAC errors, CAN bus errors, ADC/DAC errors

Each fault type on a specific MCU family/part maps to a set of possible root causes (stack overflow, null pointer, unaligned access, division by zero, clock failure, power brownout, etc.) and debugging procedures.

This is a fresh domain (embedded systems / microcontroller firmware debugging), a fresh surface (standardized fault codes + MCU specifications), and a fresh population (embedded engineers diagnosing real firmware/hardware issues). It has not been read by this mission.

## Protocol

### Data source

**electronics.stackexchange.com** — a Stack Exchange site dedicated to electrical engineering questions. Questions are tagged with MCU families (stm32, arm, cortex-m, atmel, pic, esp32, nrf52, etc.), and often include fault codes, exception names, or register values in the title or body. Answers from professional embedded engineers provide root cause diagnoses and debugging procedures.

Alternative/backup: **Stack Exchange Data Explorer (SEDE)** for electronics.stackexchange.com — allows SQL queries against the public data dump with different rate limits than the API.

### Population definition

A **case** = one electronics.stackexchange.com question that:
1. Contains at least one fault/exception indicator in title or body:
   - ARM Cortex-M fault names: `HardFault`, `MemManage`, `BusFault`, `UsageFault`, `SecureFault`
   - Fault status register names: `HFSR`, `CFSR`, `DFSR`, `AFSR`, `MMFAR`, `BFAR`, `UFSR`, `BFSR`, `SHCSR`
   - Vendor-specific: `EXC_RETURN`, `FAULTMASK`, `PRIMASK`, `BASEPRI`
   - Generic fault terms: `fault`, `exception`, `crash`, `reset`, `watchdog`, `brownout`, `hard fault`
2. Tagged with at least one MCU family tag: `stm32`, `arm`, `cortex-m`, `atmel`, `avr`, `pic`, `esp32`, `nrf52`, `nrf51`, `msp430`, `tm4c`, `lpc`, `kinetis`, `efm32`, `sam`, `samd`, `rp2040`, `stm32f1`, `stm32f4`, `stm32h7`, etc.
3. Has at least one answer from a user with >100 reputation (proxy for experienced engineer)
4. Has an accepted answer OR an answer with score ≥ 3

A **structured case** = a case where the accepted/high-scored answer explicitly states:
- The root cause (specific fault condition: stack overflow, null pointer dereference, unaligned access, division by zero, clock configuration, power supply, peripheral misconfiguration, etc.)
- The debugging procedure or fix (code change, register setting, hardware modification)
- MCU family/part (from tags or body)

### Kill gates (predeclared)

| Gate | Threshold | Measurement |
|------|-----------|-------------|
| **G1 Population** | ≥ 200 structured cases | Count of structured cases in the sample |
| **G2 Fault concentration** | Top 10 fault types cover ≥ 30% of cases | Frequency distribution of fault types |
| **G3 MCU family coverage** | ≥ 10 distinct MCU families in top 10 fault types | Unique MCU families per top fault type |
| **G4 Root cause specificity** | ≥ 60% of structured cases name a specific root cause (register value, code pattern, hardware fix — not "check your code" or "use a debugger") | Manual classification of 50 random structured cases |
| **G5 Incumbent gap** | No single existing free tool covers ≥ 50% of top 10 fault types with MCU-specific root causes | Survey of free tools (vendor debuggers, fault analyzers, online resources) |

### Falsification conditions

- If **G1 fails**: The population is too small to support a tool → **KILL**
- If **G2 fails**: Fault types are too dispersed (long tail) → no concentration to exploit → **KILL**
- If **G3 fails**: Top fault types don't appear across enough MCU families → no cross-family value → **KILL**
- If **G4 fails**: Answers don't name specific root causes → no actionable computational output → **KILL**
- If **G5 fails**: Incumbents already serve the population → no gap → **KILL**

All gates must pass for the candidate to survive.

### Controls

- **Negative control**: Random sample of electronics.stackexchange.com questions WITHOUT fault terms — should have lower structure rate
- **Positive control**: Known high-frequency fault types (HardFault, stack overflow, watchdog reset, brownout reset) — should appear in top fault types if population is real

### Analysis method

1. Fetch electronics.stackexchange.com questions via Stack Exchange API (tagged with MCU families, or search for fault patterns in titles)
2. Filter for questions with fault/exception indicators
3. Classify each question's answers for root cause specificity
4. Aggregate by fault type and MCU family
5. Evaluate gates
6. Survey free incumbent tools for top 10 fault types

### Reproducibility

- Stack Exchange API key (optional, increases quota from 300 to 10,000 req/day)
- Fixed date range for sampling
- Random seed for sampling
- All classification criteria documented in `CLASSIFICATION_RULES.md`

### API throttle consideration

Stack Exchange API allows 300 requests/day per IP without a key. With a key: 10,000 req/day. The protocol must be executable within this budget or note the blocker explicitly (as E079 did). Preliminary analysis on title+tag data only (no answer fetches) can evaluate G2 and G3 within ~50 requests.