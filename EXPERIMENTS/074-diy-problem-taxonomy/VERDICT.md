<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-09
-->

# Experiment 074 Verdict: DIY Problem Taxonomy

## Result: **FAIL** — Kill gate not met

## Gate Results

| Gate | Criterion | Result | Evidence |
|------|-----------|--------|----------|
| **G1** (Population) | Single problem type ≥ 15% | **PASS** | PROC (Procedure/method) = 27.8% (188/676) |
| **G2** (Structure) | That type ≥ 50% structured input | **FAIL** | PROC structured rate = 1.1% (2/188) |
| **G3** (Gap) | No existing computational tool | Not evaluated | G2 failure makes G3 moot |

## Key Findings

### Problem Type Distribution (676 questions)
| Type | Count | % | Structured % | Notes |
|------|-------|---|--------------|-------|
| PROC (Procedure) | 188 | 27.8% | 1.1% | "How do I...?" — broad, unstructured |
| OTHER | 175 | 25.9% | 2.3% | Conceptual, theoretical, terminology |
| DIAG (Diagnosis) | 164 | 24.3% | 4.9% | Symptoms, error codes — **highest structure** |
| MATL (Material) | 46 | 6.8% | 0% | Product selection |
| CODE (Compliance) | 37 | 5.5% | 8.1% | Code references — **highest structure rate** |
| CALC (Calculation) | 28 | 4.1% | 3.6% | Well-served by existing calculators |
| SAFE (Safety) | 16 | 2.4% | 0% | |
| IDENT (Identification) | 15 | 2.2% | 0% | |
| MAINT (Maintenance) | 6 | 0.9% | 0% | |
| COST (Cost) | 1 | 0.1% | 0% | |

### Structured Input Analysis
- **Overall structured rate**: 2.1% (14/676)
- **DIAG structured examples**: Model numbers (Maytag MVW7230HW0, Panasonic FV-0511VFL1), measurements (30 ft, 24VAC)
- **CODE structured examples**: NEC 408.41, UPC 908.2.4
- **False positives**: "CAT5/6" matched as error_code, "240V" matched as measurement

### Tool Gap Assessment
- **DIAG**: Cross-brand appliance diagnostic gap exists, but population (24.3%) < G1 threshold for DIAG itself, and structure rate (4.9%) << G2
- **CODE**: Free jurisdiction-aware code checker gap exists, but population (5.5%) << G1
- **CALC**: Well-served by existing free calculators
- **PROC**: Too broad for a single computational tool

## Interpretation

The DIY Stack Exchange corpus represents real, high-volume practitioner problems (top question: 713K views for "How can I add a 'C' wire to my thermostat?"). However:

1. **No concentrated structured problem type**: The dominant type (PROC) is inherently unstructured — procedural knowledge doesn't reduce to structured inputs.

2. **Diagnosis has structure but not population**: DIAG has the highest structured-input rate (4.9%) but at 24.3% population it doesn't dominate, and 4.9% << 50% G2 threshold.

3. **Code compliance has structure rate but not population**: CODE has 8.1% structure rate but only 5.5% population.

4. **The "long tail" is the reality**: DIY problems are highly diverse, context-dependent, and rarely reducible to a structured computational input.

## Decision

**No candidate emerges from this domain under the declared protocol.**

The experiment correctly falsifies the hypothesis that DIY Stack Exchange contains a concentrated, structured problem population amenable to a computational tool.

## Lessons for Future Fresh Observation

1. **Structure is rare in physical-world Q&A**: Unlike package repositories (where metadata is structured by design), human problem statements in physical domains are narrative and contextual.

2. **Population concentration ≠ structure concentration**: The most common problem type (procedural) is the least structured.

3. **Kill gate design matters**: The 15%/50% thresholds were appropriate — they caught the real distribution.

4. **Next domain should be pre-screened for structured data**: Look for domains where the problem statement naturally includes codes, IDs, measurements (e.g., automotive OBD2, industrial equipment logs, medical device alarms, laboratory instrument errors).

## Artifacts
- `data/questions.json` — 676 fetched questions
- `data/taxonomy.csv` — classified questions
- `data/distribution.json` — type distribution
- `data/structured_by_type.json` — structure rates per type
- `data/tool_check.md` — existing tool survey
- `data/verdict.json` — gate evaluation
- `analyze.py` — classification logic
- `fetch.py` — data acquisition

## Compliance
- Protocol predeclared in `PROTOCOL.md`
- Kill gates evaluated against committed data
- stdlib-only Python 3.8
- No external dependencies
- Raw evidence preserved