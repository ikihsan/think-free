<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-13
-->

# 135 — preflight adapter on a seventh harness structure (single JSON format)

`observed` 2026-10-13, Python 3.8.10.

## Experiment summary

Prototyped the `preflight` adapter for a seventh harness structure: a single JSON
file (dict keyed by `sample_id`), distinct from the six previously tested structures:

| Experiment | Harness structure |
|---|---|
| **E128** | `modelscope/evalscope`: two files (predictions + reviews) joined by `index` |
| **E129** | `openai/evals`: one append-only event stream, joined by `sample_id` |
| **E130** | Single JSONL: `results.jsonl` with `{sample_id, model_output, expected, correct}` per line |
| **E131** | CSV: `harness.csv` with `{sample_id, model_output, expected, correct}` per row |
| **E132** | YAML: `harness.yaml` with per-entry `{sample_id, model_output, expected, correct}` |
| **E133** | XML: `harness.xml` with `<entry>` elements containing `{sample_id, model_output, expected, correct}` |
| **E135 (this experiment)** | **Single JSON**: `harness.json` with dict mapping `sample_id` → `{model_output, expected, correct}` |

### Goal

Add a seventh data point to the "adapter is a few lines" pattern, testing whether
`preflight` can be adapted to a single JSON format with a stdlib-only adapter. If
the pattern holds across 7 diverse harness structures, it provides very strong
inductive evidence that `preflight` can be pointed at arbitrary LLM evaluation harness
output with a small per-harness adapter.

### Key finding

The adapter is **33 lines** of stdlib-only Python (including imports), transforming
the single JSON harness format into the `key_rows`/`out_rows`/`items`/`rows` formats
that `preflight.C1`, `preflight.C2`, and `preflight.C3` expect. All three checks
execute successfully when run against the adapter-transformed data.

The adapter pattern now has 7 data points across 7 diverse structures:
1. E128: `modelscope/evalscope` — two files, joined by `index`
2. E129: `openai/evals` — one event stream, joined by `sample_id`
3. E130: Single JSONL — one file per line, JSON objects
4. E131: CSV — one file with comma-separated values
5. E132: YAML — one file with YAML mapping/list
6. E133: XML — one file with XML entry elements
7. E135: Single JSON — one file with dict keyed by sample_id

All seven produce working adapters under 50 lines, confirming the pattern generalizes
across significantly different file formats and structures.

### Files in this experiment

| File | Description |
|---|---|
| `README.md` | This file |
| `PROTOCOL.md` | Pre-declared protocol: question, harness structure, adapter design, three checks |
| `RESULT.md` | Run results, gate accounting, and build decision |
| `adapter.py` | The adapter: 33 lines stdlib-only, converts JSON format to preflight inputs |
| `harness.json` | The test harness JSON data (20 entries) |
| `key/ground_truth.json` | Key file: 20 entries with sample_id and expected fields |
| `output/model_results.json` | Output file: 20 entries with model_output and expected fields |