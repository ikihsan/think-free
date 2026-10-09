<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-09
-->

# Experiment 074: DIY Problem Taxonomy — Fresh Observation

## Objective
Systematically classify problem types in the DIY Stack Exchange corpus to discover whether a specific, testable computational opportunity exists in the physical home-repair domain.

## Motivation
- Six invention claims tested, none validated (F001, F006, F008, F009, F010, F012, F060, F081, F084, F099, F101)
- View-count principle validated on package repositories (PyPI, NPM) but not on social/Q&A platforms (E071, E072)
- Need-harvest route closed at population level (F098, F100)
- **D083: any successor session starts from fresh observation in a new domain**
- DIY (home improvement) is a new domain not previously explored

## Method
1. **Sample**: Fetch 200 questions from DIY Stack Exchange (mix of high-vote, recent, unanswered)
2. **Classify**: Each question gets one primary problem-type label from a fixed taxonomy
3. **Measure**: Distribution of problem types, and for each type, whether it has:
   - Structured input (error code, model number, measurements, codes)
   - Deterministic answer (calculation, code lookup, diagnosis tree)
   - Existing computational tool (calculator, database, app)
4. **Kill gate**: If no single problem type accounts for ≥ 15% of questions AND has both structured input AND no existing computational tool, the domain yields no testable candidate.

## Taxonomy (primary problem types)
| Code | Label | Description |
|---|---|---|
| DIAG | Appliance/equipment diagnosis | Symptom + error code → root cause (washer, HVAC, water heater, generator) |
| CALC | Engineering calculation | Voltage drop, load bearing, pipe sizing, concrete mix, tree height |
| CODE | Code compliance | Electrical (NEC), plumbing (UPC/IPC), building code — "is this legal/safe?" |
| IDENT | Identification | Pest, material, component, wire, pipe — "what is this?" |
| PROC | Procedure/method | "How do I...?" — technique, sequence, tool usage |
| MATL | Material selection | "What type of X should I use?" — concrete, wire, pipe, fastener |
| COST | Cost estimation | "How much will this cost?" — materials, labor, comparison |
| SAFE | Safety assessment | "Is this dangerous?" — structural, electrical, chemical |
| MAINT | Maintenance schedule | "When/how often should I...?" — filter, fluid, inspection |
| OTHER | Other | Doesn't fit above |

## Structured-input criteria (for a question to count as "structured")
- Contains error code (e.g., "F83", "E1", "blinking 3 times")
- Contains model number (e.g., "Grundfos UPS3", "Vaillant", "AO Smith")
- Contains specific measurements (e.g., "140 volts", "12 AWG", "2x6 joist", "100 ft run")
- References specific code section (e.g., "NEC 300.4", "UPC 908.2.4")
- References specific standard (e.g., "UL listed", "ASTM C33")

## Existing-tool check (per problem type)
For the top problem types by count, check if a free, accessible computational tool exists:
- Calculator (web or app)
- Database (error code lookup, code reference)
- Diagnostic tree (interactive)
- Code reference (searchable)

## Kill gate (predeclared)
**G1 (population)**: ≥ 15% of sampled questions fall into a single problem type.
**G2 (structure)**: Of that type, ≥ 50% have structured input (as defined above).
**G3 (gap)**: For that type, no free computational tool exists that takes the structured input and produces the answer.

**All three must pass for the experiment to yield a candidate direction.**
If any gate fails, the experiment closes the domain with a negative result.

## Fixtures
- Synthetic fixture: 50 manually labelled questions (from the fetched set) to establish inter-rater reliability
- Real fixture: The full fetched question set (titles, tags, bodies)

## Outputs
- `taxonomy.csv` — question_id, title, tags, primary_type, has_structured_input, notes
- `distribution.json` — counts and percentages per type
- `structured_by_type.json` — structured-input rate per type
- `tool_check.md` — existing tool survey for top 3 types
- `verdict.md` — gate results and decision

## Analysis script
`analyze.py` — stdlib only, reads fixtures, produces outputs, evaluates gates.