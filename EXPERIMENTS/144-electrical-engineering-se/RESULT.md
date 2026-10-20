<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-15
-->

# E144 result — Electrical Engineering SE: diagnosis population real, answerable class weakly served, program-shaped residue exists

Session `2026-10-15-004`. Protocol `PROTOCOL.md`; screening `screening.json`; G0 gate `g0_probes.py`/`g0_results.json`; attempts `generate_attempts.py` (`attempts.jsonl`, all `attempt_first=true`); threads `fetch_threads.py` (`threads.json`); grades `grade.py` (`grades.jsonl`, `results.json`).

This is the fresh observation E144: the largest untouched non-software technical SE site (~200k questions) where the practitioner is an electrical engineer/technician and resolutions are plausibly self-contained diagnostic procedures.

## 1. Gates

| gate | result |
|---|---|
| **G0 discrimination** | **PASS** — 10/10 answerable probes answered, 10/10 specific probes declined (labels known by construction, independent of thread outcome) |
| **G1 population** | **PASS** — 78 diagnosis-shaped of 1200 fetched (≥ 60 of ≥ 300 required). Arm A (votes): 0/1 diagnosis. Arm B (creation): 78/233 diagnosis (33.5%) |
| **G2 composition** | Reported per arm and pooled with Wilson CI95. See §2. |
| **K1 served share** (answerable diagnosis class) | **FAIL / LINE REOPENS** — 1/8 = 0.125 served, Wilson CI95 [0.0224, 0.4709]. Upper bound 0.4709 < 0.50 threshold. An unserved answerable diagnosis population exists per protocol. **Caveat**: n=8 (protocol target n=20); thread resolution quality poor (0/8 have accepted answers, most have 0 answers). |
| **K2 execution share** | 57/234 = 0.244 pooled execution-shaped. Split: 41 program (0.175), 16 manual (0.068) |
| **K3 program-shaped residue** | **41 rows** — non-zero program-shaped population exists (candidate signal) |

## 2. Population composition

**Arm A (votes, 200 fetched):** 0 diagnosis-shaped. The vote-sorted stratum over-represents engaged/answered questions (E033/E034 lesson), and at high votes the unanswered pool is nearly empty of diagnosis needs.

**Arm B (creation, 1000 fetched, 233 unanswered):** 78 diagnosis-shaped (33.5%, Wilson CI95 [27.6%, 39.8%]). Sub-classes: 31 answerable (39.7%), 47 specific (60.3%). Execution-shaped: 57 (24.5%) — 41 program, 16 manual. Other: 98 (42.1%).

**Pooled (300 fetched per protocol, actually 1200):** 78 diagnosis, 57 execution, 99 other.

The high specific share (60% of diagnosis) is notable: electrical engineering diagnosis often requires the asker's schematic, measurements, or board details — consistent with the domain.

## 3. K1 served share detail

Only 8 answerable diagnosis questions in the top-20-by-view_count sample (deviation: protocol specifies Arm A top 20; Arm A had 0 diagnosis, so Arm B used). Thread resolution quality:

| QID | Title (truncated) | Answers | Accepted | Comments | Grade |
|---|---|---|---|---|---|
| 770754 | Capacitive wave height sensor | 1 | No | 7 | Unserved |
| 769493 | Solder 2 6-layer PCBs | 0 | — | 14 | Unserved (no convergence) |
| 770553 | Interlock pedestrian gate | 2 | No | 3 | Unserved |
| 771406 | USB-RS485 not stable | 0 | — | 26 | Unserved (no convergence) |
| 772062 | FM-like static on speaker | 0 | — | 14 | Unserved (no convergence) |
| 769896 | PMOS gate drive 100V | 1 | No | 1 | **Served** |
| 769368 | Fuzzy logic controller | 2 | No | 7 | Unserved |
| 772015 | Servo spinning | 0 | — | 9 | Unserved (no convergence) |

**Served: 1/8 (Q769896 only).** The one served question had a clear technical answer matching the attempt. The other 7 either had no answers or answers that didn't converge.

**Critical limitation:** 0 of 8 answerable questions have accepted answers. Grading against non-converged threads systematically underestimates served share. The protocol's grading assumption ("threads may still carry converged answers") does not hold here.

## 4. K3 program-shaped residue

41 execution/program questions across the full screened population. Examples:
- "Variable speed, variable rail sine wave driver design" (Q772444)
- "Self Stabilizing Robot Movement Control" (Q771932)
- "Modelling s parameters of a step discontinuity" (Q771850)
- "How antenna spacing affects sidelobes in beamforming" (Q771598)
- "LTspice simulation too slow for 12 phase star rectifier" (Q770729)

These are self-contained script/tool requests (SPICE automation, optimization, calculation, simulation scripting) — the exact artifact class a tool could serve. **Non-zero residue = candidate signal.**

## 5. Instrumentation notes

- **Arm A deviation:** Protocol specified Arm A top 20 for attempt sample; Arm A yielded 0 diagnosis-shaped. Used Arm B instead (pre-declared as deviation). This reduced answerable sample from target n=20 to n=8.
- **Thread resolution quality:** Stack Exchange's `accepted=false` filter does not guarantee answer presence. 12/20 sample questions had 0 answers; only 1 had an accepted answer (none in answerable class). This is worse than E143 (Cross Validated) where threads had better resolution.
- **G0 discrimination passed** but attempt generation initially failed to decline specific questions (fixed in re-run). The model *can* distinguish answerable vs specific when explicitly probed, but the first attempt generation didn't apply this.
- **view_count covariate:** Works — all fetched questions have view_count > 0.

## 6. Decision

**The Electrical Engineering SE line REOPENS on two limbs:**

1. **K1 upper bound < 0.50**: An unserved answerable diagnosis population exists (per protocol, though with caveats: n=8, weak thread resolution).
2. **K3 program-shaped residue = 41 > 0**: A non-zero execution/program population exists — self-contained script/tool needs in SPICE automation, RF design, thermal calculation, motor control, simulation optimization.

**Concrete reason for reopening:** Unlike Cross Validated (E143, program residue 0%), EE SE has a substantial program-shaped need population (17.5% of all questions, 41 rows). These are not "write me a program" requests but domain-specific automation needs (SPICE scripts, antenna array optimization, transformer design calculators, motor control tuning tools) that a general assistant serves poorly without domain-specific tooling.

**What this does not establish:**
- The true served share of answerable class (thread resolution too weak to measure; upper bound 0.47 is an artifact of grading against non-converged threads).
- Whether a tool could serve the program-shaped residue (41 rows is a signal, not validation).
- The answerable class served share in a properly resolved thread population.

**Next action per protocol:** The line reopens. To close it definitively would require: (a) a larger answerable sample with resolved threads (extend sample to 40 per straddle rule, though CI doesn't straddle), (b) better thread resolution (accepted answers or clear convergence), or (c) a different venue with stronger resolution culture. The program-shaped residue (41) is the stronger candidate signal — it survived the E143 closure of statistics-domain program residue and appears specific to engineering diagnosis domains.

## 7. Comparison to prior venues

| Venue | Diagnosis-shaped | Answerable % | Served (answerable) | Program residue |
|---|---|---|---|---|
| Non-software SE (E062) | 17/20 top | 85% | 0.85 | — |
| Anova appliance (E091) | 7/20 top | 35% | 0.25 | 0 |
| Home Improvement (E092) | 66/150 top | 92% | 0.81 | 0 |
| Stack Overflow (E126) | — | — | — | 2% (6/299) |
| Cross Validated (E143) | 143/300 | 47.7% | 1.00 | 0% |
| **Electrical Engineering (E144)** | **78/233 Arm B** | **39.7%** | **0.125 (n=8)** | **17.5% (41/234)** |

The EE SE venue is distinct: high diagnosis density, high specific share (schematic-dependent), low answerable served share (weak thread resolution), and **substantial program-shaped residue**. This is the first venue where K3 > 0 survives.