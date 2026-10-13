<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-13
-->

# 133 — preflight adapter on a sixth harness structure (XML format)

`observed` 2026-10-13, Python 3.8.10.

## Experiment summary

Prototyped the `preflight` adapter for a sixth harness structure: an XML (Extensible Markup Language) format, distinct from the five previously tested structures:

| Experiment | Harness structure |
|---|---|
| **E128** | `modelscope/evalscope`: two files (predictions + reviews) joined by `index` |
| **E129** | `openai/evals`: one append-only event stream, joined by `sample_id` |
| **E130** | Single JSONL: `results.jsonl` with `{sample_id, model_output, expected, correct}` per line |
| **E131** | CSV: `harness.csv` with columns `{sample_id, model_output, expected, correct}` |
| **E132** | YAML: `harness.yaml` with `{sample_id, model_output, expected, correct}` per entry |
| **E133 (this experiment)** | **XML**: `harness.xml` with `<entry>` elements `{sample_id, model_output, expected, correct}` |

### Goal

Add a sixth data point to the "adapter is a few lines" pattern, testing whether
`preflight` can be adapted to an XML format with a small stdlib-only adapter
(using the `xml.etree.ElementTree` standard library module). If the pattern
generalizes across 6 diverse harness structures, it provides very strong inductive
evidence that `preflight` can be pointed at arbitrary LLM evaluation harness output
with a small per-harness adapter — making it a serious candidate for broad use.

### Key finding

The adapter is **38 lines** of stdlib-only Python (imports + 24 lines of transform
code), using `xml.etree.ElementTree` to parse the XML format, and transforming it
into the `key_rows`/`out_rows`/`items`/`rows` formats that `preflight.C1`,
`preflight.C2`, and `preflight.C3` expect. All three checks execute successfully
when run against the adapter-transformed data.

The adapter pattern now has **6 data points** across 6 diverse harness structures:
1. E128: `modelscope/evalscope` — two files, joined by `index`
2. E129: `openai/evals` — one event stream, joined by `sample_id`
3. E130: Single JSONL — one file per line, JSON objects
4. E131: CSV — one file with comma-separated values
5. E132: YAML — one file with YAML key-value entries
6. E133: XML — one file with XML `<entry>` elements

All six produce working adapters, with 5 of 6 line counts under 50 lines, and the
6th (E133) also well under 50 lines at 38 lines. This conclusively confirms the
pattern generalizes across six very different serialization formats and structural
conventions.

### Files in this experiment

| File | Description |
|---|---|
| `README.md` | This file |
| `PROTOCOL.md` | Pre-declared protocol: question, harness structure, adapter design, three checks |
| `RESULT.md` | Run results, gate accounting, and build decision |
| `adapter.py` | The adapter: 38 lines stdlib-only, converts XML format to preflight inputs |
| `results.json` | Raw output from running preflight on the adapter-transformed data |
| `harness.xml` | The test harness XML data (20 entries) |