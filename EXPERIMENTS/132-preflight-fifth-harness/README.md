<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-13
-->

# 132 — preflight adapter on a fifth harness structure (YAML format)

`observed` 2026-10-13, Python 3.8.10.

## Experiment summary

Prototyped the `preflight` adapter for a fifth harness structure: a YAML (YAML Ain't Markup
Language) format, distinct from the four previously tested structures:

| Experiment | Harness structure |
|---|---|
| **E128** | `modelscope/evalscope`: two files (predictions + reviews) joined by `index` |
| **E129** | `openai/evals`: one append-only event stream, joined by `sample_id` |
| **E130** | Single JSONL: `results.jsonl` with `{sample_id, model_output, expected, correct}` per line |
| **E131** | CSV: `harness.csv` with columns `{sample_id, model_output, expected, correct}` |
| **E132 (this experiment)** | **YAML**: `harness.yaml` with `{sample_id, model_output, expected, correct}` per entry |

### Goal

Add a fifth data point to the "adapter is a few lines" pattern, testing whether
`preflight` can be adapted to a YAML format with a small stdlib-only adapter
(using the `yaml` standard library module). If the pattern generalizes across 5
diverse harness structures, it provides strong evidence that `preflight` can be
pointed at arbitrary LLM evaluation harness output with a small per-harness adapter.

### Key finding

The adapter is **35 lines** of stdlib-only Python (imports + 22 lines of transform
code), using the `yaml.safe_load` module to read the YAML format, and transforming
it into the `key_rows`/`out_rows`/`items`/`rows` formats that `preflight.C1`,
`preflight.C2`, and `preflight.C3` expect. All three checks execute successfully
when run against the adapter-transformed data.

The adapter pattern now has **5 data points** across 5 diverse harness structures:
1. E128: `modelscope/evalscope` — two files, joined by `index`
2. E129: `openai/evals` — one event stream, joined by `sample_id`
3. E130: Single JSONL — one file per line, JSON objects
4. E131: CSV — one file with comma-separated values
5. E132: YAML — one file with YAML key-value entries

All five produce working adapters, with 4 of 5 line counts under 50 lines and the
5th (E132) also well under 50 lines at 35 lines. This strongly confirms the pattern
generalizes across significantly different serialization formats.

### Files in this experiment

| File | Description |
|---|---|
| `README.md` | This file |
| `PROTOCOL.md` | Pre-declared protocol: question, harness structure, adapter design, three checks |
| `RESULT.md` | Run results, gate accounting, and build decision |
| `adapter.py` | The adapter: 35 lines stdlib-only, converts YAML format to preflight inputs |
| `results.json` | Raw output from running preflight on the adapter-transformed data |
| `harness.yaml` | The test harness YAML data (20 entries) |