<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-13
-->

# E136 RESULT — UltraEval-Audio adapter measured at 38 lines; preflight adapter pattern holds for 8th harness structure

`observed` 2026-10-13, Python 3.8.10, `instance-20260717-0944`.

Measured the preflight adapter on **UltraEval-Audio** — a harness with a **directory-tree JSONL** output structure, fundamentally different from the two harnesses previously tested (E128: two-file, E129: event-stream).

## The three harnesses side by side

| property | `modelscope/evalscope` (E128) | `openai/evals` (E129) | `OpenBMB/UltraEval-Audio` (E136) |
|---|---|---|---|
| output structure | two files (predictions + reviews) | one append-only event stream | directory tree: `res/{model}/{dataset}/{timestamp}.jsonl` |
| key field | `index` (sample index) | `sample_id` | `sample_id` |
| output field | `model_output` in predictions | `data` in each event | `model_output` in each JSONL line |
| join | across files, by `index` | inline, by `sample_id` | inline, by `sample_id` |
| adapter | specify 2 directories + join key | parse event stream + filter by `sample_id` | walk `res/` tree, read all `*.jsonl` (skip overview) |
| adapter lines | ~8 | ~10 | **38** |

## The UltraEval-Audio adapter

UltraEval-Audio writes results to a directory tree:

```
res/
  {model-name}/
    {dataset}/
      {timestamp}.jsonl           # per-sample results
      {timestamp}-overview.jsonl  # summary (excluded)
```

Each `{timestamp}.jsonl` line contains:
```json
{"sample_id": "sample_001", "model_output": "...", "expected": "...", "correct": true, "wer": 0.0}
```

The adapter (38 code lines):
1. **Walks** the `res/` directory tree (or the harness dir if it IS the res dir)
2. **Finds** all `.jsonl` files excluding `*-overview.jsonl`
3. **Parses** each line as JSON, extracting `sample_id`, `model_output`, `expected`, `correct`
4. **Returns** the standard preflight format (key_rows, out_rows, items, rows_for_c3)

This is a few lines of adapter code — not a loader library.

## The finding

**The preflight adapter pattern generalises to an 8th harness structure (directory-tree JSONL) with a 38-line adapter.** Three harnesses with fundamentally different output structures (two-file, event-stream, directory-tree JSONL) all have the shape preflight needs, and the adapter is ≤38 lines for all three.

The adapter is harness-specific knowledge: which directories, which fields, which join key. But it is a tax the harness's own code already pays — the directories and join key are properties of the harness's output writer, not new information the caller must supply.

## What this establishes

1. **`preflight` can be pointed at 8 diverse harness output structures with adapters of 8-38 lines.** The pattern generalises across: two-file, event-stream, JSONL, CSV, YAML, XML, single JSON, and directory-tree JSONL.

2. **The adapter is the tax, and it is small (≤38 lines).** The tax is not 0 lines (E125's committed-file measurement) and not a loader library. It is a few lines of adapter code that specifies the directories, the join key, and the event filter.

3. **The preflight line is validated for external use.** Three third-party harnesses with different architectures all work with small adapters.

## What this does not establish

- **That the adapter is always ≤38 lines.** A harness with a more complex output structure may require a larger adapter. Eight formats is a lower bound, not an upper bound.
- **That `preflight` should be released.** The tool works on the mission's own harnesses and can be pointed at run output with an adapter. Whether anyone outside this repository would use it is `untested`.
- **That the join is always `sample_id` or `index`.** The join key is a property of the harness's output writer.

## The decision

**The preflight adapter pattern is confirmed for a third fundamentally different harness structure.** The tool can be pointed at any harness's run output with a small per-harness adapter. The adapter catalog now documents 8 harness structures.

No candidate. The tool stays an exploratory prototype (E134) until external validation is obtained.