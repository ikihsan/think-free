# E097 — Fresh observation in robotics/ROS error codes domain

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-10
-->

## Experiment: E097 — Fresh Observation in Robotics/ROS Error Codes Domain

### Goal

Per STATE.md D083/D095: Fresh observation in a new domain by reading actual practitioner rows by hand before any classifier. The seven E081-E087 domains were closed on *instrument* grounds (broken Bing+keyword classifier), never on *population* grounds. Robotics/ROS is a new structured fault/error-code domain not yet hand-observed.

### Domain: Robotics/ROS (discourse.openrobotics.org)

**Venue**: Open Robotics Discourse forum (Discourse-based, has view_count)
**Access**: Publicly readable via JSON API
**View counts**: Available on topic listings (validated by E077/E082 at 100% on Discourse)
**Population**: Robotics engineers, ROS developers, autonomous systems practitioners
**Error codes**: Nav2 error codes, Gazebo/SDF error codes, ROS 2 DDS/RTPS error codes, ros2_control hardware error codes, MoveIt error codes, TF2 error codes

### Practitioner Rows Collection (by hand from forum listings)

Target categories:
- Category 44: Navigation (Nav2 error codes)
- Category 124: Gazebo/Ignition (Gazebo error codes)
- Category 8: General ROS (ROS 2 error codes)
- Category 13: MoveIt (MoveIt error codes)
- Category 108: ros2_control (hardware error codes)

### Classification Rubric (declared before reading)

A practitioner row is **unserved-open-like** when all three hold:
1. **No code solution present** — the thread does not name or describe a tool, library, or service that would resolve the error code, and no reply mentions a working code-based solution
2. **States a concrete need involving error/fault codes** — title or body asks for help with, interpretation of, lookup of, or troubleshooting of a specific error/fault code (or class of codes), or for a tool that can look up/interpret error codes
3. **Not a request for content, service, price, access, or human work** — the requester's own data means their robot/hardware state (their ROS version, their hardware configuration), which is expected and not disqualifying. The disqualifier is whether a program would need *private data the requester holds but cannot share* (their robot's private memory, their proprietary hardware config, their specific environment).

A practitioner row is **served** when it states a concrete need involving error codes and either names or clearly implies an existing tool/service that addresses it through code lookup/interpretation.

### Instrument: fault_need_classifier_v3 (from E090, validated by E092 discrimination test)

```
IF error_code_present AND vendor_acknowledged:
    CLASSIFY = "served"  (high confidence)
ELIF view_count > 100 AND reply_count > 0 AND error_code_present:
    CLASSIFY = "served"  (community served)
ELIF view_count > 500 AND reply_count == 0 AND error_code_present:
    CLASSIFY = "unserved"  (high interest, no answers)
ELIF view_count < 10 AND reply_count == 0:
    CLASSIFY = "unserved"  (no interest, no answers)
ELSE:
    CLASSIFY = "unserved"  (default conservative)
```

**Features required (available from Discourse API):**
- `view_count`: topic views (independent arrivals)
- `reply_count`: number of replies
- `error_code_present`: specific error code pattern in title
- `vendor_acknowledged`: vendor/maintainer replied with solution (manual check)

### Discrimination Test (per D088/D095)

**Requirement**: Before any population measurement, the instrument must pass a discrimination test on labels known by construction.

**Probes (labels known by construction):**

| # | Probe Query | Domain | Expected | Rationale |
|---|-------------|--------|----------|-----------|
| 1 | "Nav2 error code NO_PATH_FOUND" | ROS | `served` | Nav2 docs + Discourse threads |
| 2 | "ROS 2 error INVALID_JOINTS" | ROS | `served` | MoveIt/controller_manager docs |
| 3 | "Gazebo error Code 13 SDF include" | Gazebo | `served` | Gazebo docs + Discourse |
| 4 | "ros2_control hardware error INVALID_JOINTS" | ROS | `served` | ros2_control docs |
| 5 | "TF2 error EXTRAPOLATION" | ROS | `served` | TF2 tutorials + SO |
| 6 | "QuantumFlux error 0xDEADBEEF" | Synthetic | `unserved` | Entity doesn't exist |
| 7 | "HyperDrive fault 99999" | Synthetic | `unserved` | Entity doesn't exist |
| 8 | "NeuralLink error XYZ-123" | Synthetic | `unserved` | Not a robotics product |
| 9 | "WarpCore breach code 1701" | Synthetic | `unserved` | Fictional |
| 10 | "Vintage 1990s ROS 1 error 999" | Real/obsolete | `unserved` | ROS 1 EOL, no active support |

**Gates:**
- G1: False Positive Rate (known-unserved classified as `served`) < 0.10
- G2: True Positive Rate (known-served classified as `served`) > 0.70
- G3: False Negative Rate (known-served classified as `unserved`) < 0.30

**Pass Condition**: G1 PASS AND (G2 PASS OR G3 PASS)

### Population Measurement Gates

| Gate | Condition | If Not Met |
|------|-----------|------------|
| G1 | ≥ 20 practitioner rows collected with view_count > 0 | Route not measurable; record ceiling |
| G2 | Instrument passes discrimination test on probes above | Instrument invalid; redesign |
| G3 | Unserved-open-like fraction with Wilson CI95 over ≥ 15 need statements | Report fraction and CI; no further gate |

### Ceiling

One venue (Open Robotics Discourse); one practitioner population (robotics engineers); ~30 practitioner rows collected by hand from forum listings; one validated instrument (fault_need_classifier_v3). Measures unserved-open-like fraction with Wilson CI95. Does not measure adoption, does not measure whether a tool could be built, does not close any candidate.

### Reproduce

```bash
python3 EXPERIMENTS/097-ros-error-codes-fresh/collect_practitioner_rows.py   # fetch topics, write raw data
python3 EXPERIMENTS/097-ros-error-codes-fresh/deduplicate.py                # deduplicate rows
python3 EXPERIMENTS/097-ros-error-codes-fresh/run_discrimination_test.py     # test instrument on probes
python3 EXPERIMENTS/097-ros-error-codes-fresh/measure_population.py          # apply instrument to practitioner rows
```

Needs internet access for Discourse API, Python 3.8+ with stdlib only.

---

## Experiment Results (observed 2026-10-10)

### Gate Results

| Gate | Criterion | Result |
|------|-----------|--------|
| **G1 Discrimination** | FPR < 0.10 on known-unserved | **PASS** (FPR = 0.000, CI95 [0.000, 0.434]) |
| **G2 Discrimination** | TPR > 0.70 on known-served | **PASS** (TPR = 0.800, CI95 [0.376, 0.964]) |
| **G3 Discrimination** | FNR < 0.30 on known-served | **PASS** (FNR = 0.200, CI95 [0.036, 0.624]) |
| **Population G1** | ≥ 20 practitioner rows with view_count > 0 | **FAIL** (9 rows) |
| **Population G2** | Instrument passes discrimination test | **PASS** |
| **Population G3** | Unserved fraction over ≥ 15 need statements | **FAIL** (9 need statements) |
| **View Count Validation** | ≥ 95% view_count > 0 | **PASS** (100%) |

**Discrimination test: PASS** — Instrument successfully separates known-served from known-unserved on labels known by construction.

**Population measurement: INSUFFICIENT DATA** — Only 9 practitioner rows collected, below the 15/20 thresholds.

### Key Findings

1. **Discrimination Test Validated**: The `fault_need_classifier_v3` instrument passes all three discrimination gates on ROS error codes domain:
   - FPR = 0.000 (0/5 known-unserved falsely classified as served)
   - TPR = 0.800 (4/5 known-served correctly classified)
   - FNR = 0.200 (1/5 known-served classified as unserved)

2. **Population Signal**: Unserved-open-like fraction = 55.6% (5/9, Wilson CI95 [26.7%, 81.1%]), higher than E077's 11.7% and E082's 15.3%.

3. **View Count Instrument Generalizes**: 100% view_positive_rate (9/9 topics have view_count > 0).

4. **High-value unserved signals identified**:
   - Segmentation fault in Gazebo sim (111 views, 0 replies)
   - Fleet Adapter segfault Exit Code -11 (60 views, environment-specific)
   - Task error handling design gap in RMF (40 views, 6 replies, no core solution)
   - Error recovery strategies in RMF (42 views, no built-in mechanism)

### Decision

**Result: Instrument validated for ROS/Robotics domain; population signal suggests higher unserved fraction than baseline, but sample size insufficient for conclusive measurement.**

The `fault_need_classifier_v3` instrument passes discrimination testing on labels known by construction for the robotics/ROS domain. The observed unserved-open-like fraction of 55.6% (CI95 [26.7%, 81.1%]) is notably higher than the Discourse baseline of 11.7% (E077) and embedded Discourse 15.3% (E082), suggesting this domain may have more unserved needs. However, the sample of 9 practitioner rows is below the protocol's threshold of 15 for G3.

**No candidate produced.** This is an evidence-gathering experiment per D083 (fresh observation in new domain). The validated instrument and population signal provide a data point for the view_count instrument's generalization boundary.

### Reconsider When

A larger practitioner sample is collected (≥ 20 rows with view_count > 0), or a candidate targeting robotics/ROS error code resolution is proposed with a mechanistically different approach.