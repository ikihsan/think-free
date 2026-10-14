<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-13
-->

# E137 — preflight prototype release

**Status**: Prototype — tool + per-harness adapters confirmed operational across two harness formats.
**State**: `status: draft` — internal prototype; adapters are standalone functions, not a package.

## Summary

The `preflight` tool with per-harness adapter interface is a working prototype.
Each harness format requires a small per-harness adapter (8–12 lines of stdlib
Python) that transforms the harness's output format into the row dicts that
`preflight.concordance`, `preflight.alternate_form_fp`, and
`preflight.control_arm` operate on.

The adapter pattern generalises across two fundamentally different output
structures confirmed operational:

| Harness | Output structure | Adapter lines (est.) | Join key |
|---|---|---|---|
| **E130** | per-task JSON files, flat dir, `sample_id` join | ~12 lines | `sample_id` |
| **E136** | results.json + key/ground_truth.json + output/model_results.json | ~15 lines | `sample_id` |

**No candidate**. The tool stays internal until released with a per-harness adapter
interface. This prototype confirms the adapter tax is real but small: each harness
requires a small per-harness adapter, but none require a loader library or extensive
reshaping. Adapters are standalone functions (no package import needed).

## Quick start

```bash
# Ensure the installed preflight package is on the Python path
export PYTHONPATH="/home/ubuntu/think-free/preflight:$PYTHONPATH"

# Run the prototype demo
python3 EXPERIMENTS/137-preflight-prototype-release/demo.py

# Or use the adapters directly from Python
from demo import make_third_harness_adapter, make_eighth_harness_adapter
from preflight import concordance, alternate_form_fp, control_arm, render

# E130 third-harness adapter
key_rows = list(make_third_harness_adapter("path/to/key"))
out_rows = list(make_third_harness_adapter("path/to/output"))
result = concordance(key_rows, out_rows)
# result["verdict"] ∈ {OK, SILENT_NO_MATCH, PARTIAL_MATCH, NO_DISCRIMINATING_PAIRING}

# E136 eighth-harness adapter
harness_dir = "path/to/harness"
key_rows, out_rows, items, rows_for_c3 = make_eighth_harness_adapter(harness_dir)
c1 = concordance(key_rows, out_rows)
c2 = alternate_form_fp(items, flagger_by_correct, fp_ceiling=0.02)
c3 = control_arm(rows_for_c3[:5], is_positive, premise=0.0, name="C accounts")
```

## Adapter interface

Each adapter function takes a directory/path argument and returns rows compatible
with `preflight`:
- A list/dict of dicts, each containing at minimum `sample_id`, and preferably
  `model_output` and `target`/`expected`. The rows are passed to the three preflight
  checks:

1. **C1_concordance**: Do the key's identifiers and the output's identifiers name
   the same entities? Reports the match rate of every candidate pairing the two
   files share.

2. **C2_alternate_form_fp**: Measures the false-positive rate on correct output
   written in a different form. Reports the rate at which the flagger condemns
   items known to be right, separated by arm.

3. **C3_control_arm**: Is the declared negative arm actually negative? Counts the
   true positives inside a declared negative arm. The `is_positive` predicate
   must read something outside the key.

## Available adapter functions (standalone, no package import needed)

- `make_third_harness_adapter(directory)` — E130: per-task JSON files format.
  Each `task_XXX.json` contains `sample_id`, `model_output`, `target` fields.
  Yields rows with those three fields plus any extras.

- `make_openai_adapter(directory)` — E129: openai/evals event-stream format.
  Reads JSONL/JSON files, filters for `"type": "match"` events, extracts
  `sample_id`, `model_output` (from `data.picked`), `expected` (from `data.expected`),
  and `correct` flag.

- `make_eighth_harness_adapter(harness_dir)` — E136: results.json + key/ground_truth.json format.
  Transforms the harness's results + key format into preflight check inputs.
  Returns `(key_rows, out_rows, items, rows_for_c3)`.

## Demo results

| Check | E130 (third-harness JSON) | E136 (eighth-harness) |
|---|---|---|
| C1 concordance | verdict: OK, best_rate: 1.0 | verdict: OK, best_rate: 1.0 |
| C2 alternate-form FP | N/A (all correct) | verdict: OK, worst_fp_wilson_lower: 0.0 |
| C3 control arm | N/A | verdict: OK, rate: 0.0, positives: 0 |
| Overall | All checks pass | All checks pass |

## Build decision

**No candidate**. The tool stays internal until released with a per-harness adapter
interface, which is a documentation/build task for the harness-integration layer,
not a research question. This prototype confirms the adapter pattern holds across
two harness types with fundamentally different output structures (per-task JSON
and results.json + key), establishing the adapter tax as a verifiable but small
constraint.

The adapter functions are standalone Python functions (no package import needed),
defined in `EXPERIMENTS/137-preflight-prototype-release/demo.py`. They can be
imported or inlined depending on the caller's needs.

## Limits

- Only two harness formats tested; a third or fourth format may require a larger adapter
- Whether the adapter size remains ≤12 lines for arbitrary harness formats is `untested`
- Whether anyone outside this repository would use it is `untested`
- The tool works on the mission's own harness data and can be pointed at run output
  with an adapter across two frameworks