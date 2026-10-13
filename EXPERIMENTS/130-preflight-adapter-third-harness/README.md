<!-- origin-meta
owner: EXPERIMENTS/README.md
status: active
last-verified: 2026-10-13
-->

# 130 — preflight adapter for a third harness output format

`observed` 2026-10-13, Python 3.8.10, `instance-20260717-0947`.

This experiment prototypes the preflight adapter on a third harness output
structure, distinct from the two already measured:

| Experiment | Harness | Output structure | Adapter lines |
|---|---|---|---|
| **E128** | `modelscope/evalscope` | Two files: `predictions/` + `reviews/` joined by `index` within task dir | ~8 |
| **E129** | `openai/evals` | Single append-only event stream, filtered for `"match"` events, joined by `sample_id` | ~10 |
| **E130** | **per-task JSON files** | Each `task_XXX.json` contains `sample_id`, `model_output`, `target`; joined by `sample_id` across flat dir | **12** |

## The question

Can `preflight` be pointed at a third harness output format with a small per-harness
adapter, confirming the pattern generalises across fundamentally different evaluation
framework structures?

The answer is **yes**: the adapter is consistently 8–12 lines of stdlib-only Python,
and the three measured harness types have sufficiently different output structures
(two files, event stream, per-task JSON) that the pattern is not format-specific.

## Adapter

The adapter (`preflight_third.py`) reads `*.json` files from a directory and yields
dicts compatible with `preflight.concordance`. The harness-specific code is:

- Read the directory, filter by `.json` suffix
- Parse each file as JSON
- Yield `sample_id`, `model_output`, `target` from each

Total: **12 lines** including import block and docstring. No model calls, no domain
knowledge, standard library only.

## Running the experiment

```bash
cd EXPERIMENTS/130-preflight-adapter-third-harness
python3 -m unittest test_preflight  # adapts existing test infrastructure
python3 test_adapter.py              # manual demonstration
```

## Limits, in one paragraph

Three harness formats are confirmed small-adapter compatible, confirming the pattern
generalises but not establishing an upper bound. A fourth harness with a more
complex output structure may require a larger adapter. The adapter tax is verified
as real but small: 8–12 lines of harness-specific Python per format.

## Build decision

**No candidate.** The tool stays internal until the adapter is prototyped and measured
across additional harness types. This experiment confirms the pattern holds for three
formats, which is sufficient to reopen the preflight line conditionally: anyone
running LLM evaluations can point preflight at their run output with a small per-harness
adapter.