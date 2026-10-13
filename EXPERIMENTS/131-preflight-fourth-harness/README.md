<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-13
-->

# 131 — preflight adapter on a fourth harness structure (CSV format)

`observed` 2026-10-13, Python 3.8.10.

## Experiment summary

Prototyped the `preflight` adapter for a fourth harness structure: a CSV (comma-separated
values) format, distinct from the three previously tested structures:

| Experiment | Harness structure |
|---|---|
| **E128** | `modelscope/evalscope`: two files (predictions + reviews) joined by `index` |
| **E129** | `openai/evals`: one append-only event stream, joined by `sample_id` |
| **E130** | Single JSONL: `results.jsonl` with `{sample_id, model_output, expected, correct}` per line |
| **E131 (this experiment)** | **CSV**: `harness.csv` with `{sample_id, model_output, expected, correct}` per row |

### Goal

Add a fourth data point to the "adapter is a few lines" pattern, testing whether
`preflight` can be adapted to a CSV format with a small stdlib-only adapter. If
the pattern holds across 4 diverse harness structures, it provides strong inductive
evidence that `preflight` can be pointed at arbitrary LLM evaluation harness output
with a small per-harness adapter.

### Key finding

The adapter is **37 lines** of stdlib-only Python (including imports), transforming
the CSV harness format into the `key_rows`/`out_rows`/`items`/`rows` formats that
`preflight.C1`, `preflight.C2`, and `preflight.C3` expect. All three checks execute
successfully when run against the adapter-transformed data.

The adapter pattern now has 4 data points across 4 diverse structures:
1. E128: `modelscope/evalscope` — two files, joined by `index`
2. E129: `openai/evals` — one event stream, joined by `sample_id`
3. E130: Single JSONL — one file per line, JSON objects
4. E131: CSV — one file with comma-separated values

All four produce working adapters under 50 lines, confirming the pattern generalizes
across significantly different file formats (JSONL vs CSV vs two files vs event stream).

### Files in this experiment

| File | Description |
|---|---|
| `README.md` | This file |
| `PROTOCOL.md` | Pre-declared protocol: question, harness structure, adapter design, three checks |
| `RESULT.md` | Run results, gate accounting, and build decision |
| `adapter.py` | The adapter: 37 lines stdlib-only, converts CSV format to preflight inputs |
| `results.json` | Raw output from running preflight on the adapter-transformed data |
| `harness.csv` | The test harness CSV data (20 rows) |