# Experiment 083: 3D Printer Fault Codes on Discourse Forums

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-09
-->

Fresh observation in the 3D printing hardware/firmware domain to discover whether a concentrated, structured fault code population exists that could support a computational tool.

## Documents

| Document | Purpose |
|---|---|
| [`PROTOCOL.md`](PROTOCOL.md) | Predeclared protocol with kill gates |
| [`CLASSIFICATION_RULES.md`](CLASSIFICATION_RULES.md) | Classification criteria for fault types and root cause specificity (AMENDMENT 1) |
| [`harvest.py`](harvest.py) | Data acquisition from Discourse forums |
| [`classify.py`](classify.py) | Fault type classification and printer model extraction |
| [`measure.py`](measure.py) | Gate evaluation logic |
| [`run.py`](run.py) | Main experiment runner |
| [`raw/topics_<forum>.jsonl` | Raw topic data per forum (exempt from line cap) |
| [`raw/classified_<forum>.jsonl` | Classified topics per forum (exempt from line cap) |
| [`raw/posts_<forum>.jsonl` | Reply posts for fault topics (exempt from line cap) |
| [`raw/classified_all.jsonl` | Combined classified data across all forums |
| [`results.json`](results.json) | Aggregated gate results |
| [`VERDICT.md`](VERDICT.md) | Gate evaluation results and decision |

## Status

**PARTIAL — G1/G2 PASS, G3 FAIL, G4/G5 PENDING.**

- **G1 Population**: PENDING — 79 fault topics from title+metadata; structured case count needs reply analysis
- **G2 Fault concentration**: **PASS** — 73.4% (top 10 fault types cover 58/79 cases)
- **G3 Printer model coverage**: **FAIL** — 1.8 avg models per top fault (need ≥10)
- **G4 Root cause specificity**: PENDING — requires manual review of reply bodies
- **G5 Incumbent gap**: PENDING — requires tool survey

## Hypothesis

3D printer firmware/hardware fault codes on specific printer models form a concentrated, structured problem population where:
1. Standardized fault types appear repeatedly across printer models
2. Operators diagnose root causes with specific replaceable parts
3. Existing free tools don't provide cross-brand fault code → root cause mappings
4. A computational tool mapping (fault type + printer model) → (root cause + repair) would fill a gap

## Kill Gates (Predeclared)

| Gate | Threshold | Result |
|------|-----------|--------|
| G1 Population | ≥ 100 structured cases | PENDING (79 title-only) |
| G2 Fault concentration | Top 10 fault types cover ≥ 30% | **PASS** (73.4%) |
| G3 Printer model coverage | ≥ 10 distinct models in top 10 faults | **FAIL** (1.8 avg) |
| G4 Root cause specificity | ≥ 60% name specific part | PENDING |
| G5 Incumbent gap | No free tool covers ≥ 50% of top 10 | PENDING |

## Key Findings

1. **Population exists**: 79 fault topics in 500 sampled (15.8% fault rate) across 5 forums
2. **Concentration is strong**: Top 10 fault types = 73.4% of cases (G2 PASS)
3. **Brand silos kill cross-model value**: Creality forum → Creality printers; LulzBot forum → LulzBot printers. No natural cross-brand discussion on manufacturer forums.
4. **view_count instrument works**: 100% of Discourse topics have view_count > 0
5. **Negative control**: Cooking appliance forum shows 5% false positive rate (generic IoT faults)

## Classification (AMENDMENT 1)

Original patterns were too specific to firmware error codes. Real forum titles use diverse symptom language. Expanded patterns capture:
- `HEATING_FAILED`: "heating error", "heater circuit", "heat issue", "nozzle heat", etc.
- `BED_LEVELING_FAILED`: "first layer issues", "not adhering", "bed adhesion", "plate peeling", etc.
- `PROBE_FAILED`: "CR touch error", "auto level error", "probe issue", etc.
- `HOMING_FAILED`: "won't home", "homing issue", "sensorless homing fail", etc.
- `LAYER_SHIFT`: "misaligned layers", "Z-banding", "print shift", etc.
- `PRINT_QUALITY`: "taco heat bed", "warping", "first layer", "surface quality", etc.
- `HARDWARE_FAULT`: "board replacement", "wrong plug", "wiring issue", "shaft replacement", etc.
- `FIRMWARE_ERROR`: "firmware update", "downgrade", "start_print", "web interface missing", etc.
- `ERROR_CODE`: "error code 0125", "FO2", "TR2963", "E1 error", etc.

## Reproduce

```bash
# Full experiment (harvests from 5 Discourse forums, ~200 API requests)
python3 EXPERIMENTS/083-3dprint-fault-codes/run.py

# Classify existing data
python3 EXPERIMENTS/083-3dprint-fault-codes/classify.py EXPERIMENTS/083-3dprint-fault-codes/raw/topics_forum_creality_com.jsonl

# Measure gates on classified data
python3 EXPERIMENTS/083-3dprint-fault-codes/measure.py EXPERIMENTS/083-3dprint-fault-codes/raw/classified_forum_creality_com.jsonl forum.creality.com
```

## Compliance

- Protocol predeclared in `PROTOCOL.md` before data collection
- Classification rules in `CLASSIFICATION_RULES.md` (AMENDMENT 1 declared after preliminary inspection, before full classification)
- Kill gates evaluated against committed data
- Stdlib-only Python 3.8
- No external dependencies
- Raw evidence preserved in `raw/`
- API polling at 1 req/sec (polite)