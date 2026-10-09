<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-08
-->

# E067 — view-count measurement framework

**Status:** Prototype. Core measurement engine implemented and verified against E062's non-software Stack Exchange corpus. All key metrics (G1, G4 gate, unremedied arrival statistics) reproduce the original results.

A reusable Python framework for measuring `view_count` — independent arrivals at a need — across need statement corpora. This prototype implements the core measurement engine from E062, structured as a standalone tool that can process need corpora in the standard format and produce the same class of outcome reports.

## The core question

Every population this mission has measured for candidate need comes from one route (software venues: GitHub, PyPI, HN, Stack Overflow). Seven measurements say the candidate seat is empty (F029, F051, F039, F059, F081, F084, F085). The `view_count` instrument (E062) measures what **platforms** record: how many independent people arrive at each need, on every row. This is distinct from counting *statements* of need — it measures actual arrivals, the channel a substitute venue was chosen for.

**If this framework generalises** beyond the E062 population (non-software Stack Exchange), it provides a reusable instrument for future corpus measurements, enabling comparison of view-arrival patterns across domains and helping distinguish served need from stated need.

**If it does not generalise**, it documents the technical gap and the conditions under which `view_count` works (platforms that record an outcome per request).

## Installation

```bash
# From the repository root
PYTHONPATH=EXPERIMENTS python3 -m viewcount --help
```

Or install as a package:

```bash
pip install -e EXPERIMENTS/067-viewcount-framework
```

## Quick start

```bash
# Process the E062 non-software Stack Exchange corpus
python3 -m viewcount process \
    --input EXPERIMENTS/062-nonsw-need-shape/raw/arm1.jsonl \
    --output viewcount-results.json

# Classify a single need title
python3 -m viewcount classify "Is there a tool that fixes blotchy staining?"

# Print a human-readable report from outcome.json
python3 -m viewcount report viewcount-results.json
```

## Motivation

The mission's seven emptiness measurements (F029, F051, F039, F059, F081, F084, F085) all read *statements* of need and concluded "no candidate". But E062 measured a non-software population with `view_count` and found: **17 of 20** top-arrival unremedied needs are answered in full today by a free general assistant. The route was not empty — it was selecting *statements*, not unmet need.

The `view_count` instrument was the mission's missing piece: it asks the question of the **platform** instead of the person, on every row. This prototype makes that instrument reusable.

## Classes

| Class | Meaning |
|---|---|
| `served` | A free general assistant can hand the requester a remedy they could execute today, using only what the requester already holds |
| `unserved-data-absent` | No program can answer because the record was never created |
| `unserved-remedy-is-human` | The need is service, access, price or human work |
| `unserved-open` | Genuinely not served — the only label that can open a candidate |

## Functions

### `process(input_path, output_path)`

Read a need statement corpus in E062 arm1.jsonl format, compute the full `view_count` measurement suite, and write `outcome.json`-compatible results.

**Computes:**

- **G1 reconciliation**: Rows, sites, rows with body, rows with outcome fields
- **G4 age gradient**: Still-open and accepted shares by age cohort, gap in points, monotonicity
- **State distribution**: Counts and view statistics per platform state (accepted, answered, closed, open)
- **Unremedied arrival**: Total views (open rows only), share of all views, median views, top row views, years unanswered, view concentration (top 5%, 10%, 25%)
- **Unremedied shape**: Classification of need types (registry-lookup, diagnose-own-artifact, purchase-source, judgement, technique-or-expertise) among unremedied rows
- **By-site breakdown**: View distribution per site

**Output:** `outcome.json`-compatible dict written to `output_path`.

### `classify(title)`

Classify a need title string into one of five categories:

- `registry-lookup` — needs requiring a published registry entry or spec sheet (serial numbers, VINs, model/year, etc.)
- `diagnose-own-artifact` — needs requiring the requester's own physical artifact to be examined
- `purchase-source` — needs asking where to buy, what brand, what hinge system, etc.
- `judgement` — needs asking for safety/quality reassurance ("is it safe?", "should I?")
- `technique-or-expertise` — all other needs (default catch-all)

### `report(outcome_json)`

Print a human-readable summary of `outcome.json`-computed results, matching the E062 outcome.py print format.

## Data format

The input JSONL format (E062 arm1.jsonl) has one record per row with these fields:

| Field | Meaning |
|---|---|
| `question_id` | Platform-internal question identifier |
| `title` | Need statement title |
| `body` | Full need description (may be empty) |
| `view_count` | Platform-recorded view count for this question |
| `is_answered` | Whether an accepted answer exists |
| `answer_count` | Number of answers recorded |
| `score` | Question score |
| `tags` | Question tags |
| `_site` | Source Stack Exchange site (astronomy, bicycles, cooking, diy, gardening, woodworking) |
| `creation_date` | Unix timestamp of question creation |
| `closed_date` | Unix timestamp of closure (0 if open) |
| `closed_reason` | Why the question was closed (if applicable) |
| `link` | URL to the question |
| `owner` | Question owner info |
| `last_activity_date` | Last activity timestamp |

## Why this framework matters

The `view_count` measurement answers a question the mission's seven emptiness measurements all asked implicitly but could not: **how many independent people arrived at each need, on every row?** Without this measure, the mission was counting *statements* and reading them as *service levels*. With `view_count`, the arrival channel becomes the data, and the distinction between stated need and unmet need can be measured directly.

The framework is designed to be minimally invasive: it requires only the data that a platform already records per question (view counts, answer status, timestamps). No new API calls, no web searches, no model calls. It is the cheapest available discriminator between "tool-solvable unmet need is scarce" (structure) and "the source is the constraint" (platform limitation).

## Roadmap

- [x] Core measurement engine (G1, G4, state distribution, unremedied arrival)
- [x] Need classification by title keyword patterns
- [x] Human-readable report generation (matching E062 outcome.py format)
- [ ] Multi-corpora comparison mode
- [ ] Integration with other platforms' data formats
- [ ] CLI completion and config file support

## License

MIT — see LICENSE in the repository root.