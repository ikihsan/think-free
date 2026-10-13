<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-13
-->

# 130 — preflight adapter on a third harness structure

`observed` 2026-10-13, Python 3.8.10.

## Experiment summary

Prototyped the `preflight` adapter for a third harness structure: a single
`results.jsonl` file (one JSON object per line), distinct from the two previously
tested structures:

| Harness | Output structure |
|---|---|
| **E124 / mission** | Scorer key + answer files (committed to repo) |
| **E128** | `modelscope/evalscope`: two files (predictions + reviews) joined by `index` |
| **E129** | `openai/evals`: one append-only event stream, joined by `sample_id` |
| **E130 (this experiment)** | **Single JSONL**: `results.jsonl` with `{sample_id, model_output, expected, correct}` per line |

### Goal

Validate the "adapter is a few lines" pattern on a third, structurally different
harness format. If the pattern generalizes across three diverse structures, it
demonstrates that `preflight` can be pointed at arbitrary LLM evaluation harness
outputs with a small per-harness adapter — making it a candidate for broad use.

### Key finding

The adapter is **34 lines** of stdlib-only Python (plus imports), transforming
the single JSONL format into the `key_rows`/`out_rows`/`items`/`rows` formats
that `preflight`'s three checks (C1, C2, C3) expect. All three checks execute
successfully when run against the adapter-transformed data.

The adapter pattern generalizes to a third diverse harness structure, confirming
the pattern is not limited to the two previously tested harnesses.

### Files in this experiment

| File | Description |
|---|---|
| `README.md` | This file |
| `PROTOCOL.md` | Pre-declared protocol: question, harness structure, adapter design, three checks |
| `RESULT.md` | Run results, gate accounting, and build decision |
| `adapter.py` | The adapter: 34 lines stdlib-only, converts JSONL format to preflight inputs |
| `results.json` | Raw output from running preflight on the adapter-transformed data |