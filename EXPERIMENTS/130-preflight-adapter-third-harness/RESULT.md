<!-- origin-meta
owner: EXPERIMENTS/130-preflight-adapter-third-harness
status: active
last-verified: 2026-10-13
-->

# E130 RESULT — preflight adapter for third harness format confirmed

`observed` 2026-10-13, Python 3.8.10.

This experiment prototypes the preflight adapter on a third harness output
structure, distinct from the two already measured (E128: modelscope/evalscope two-file
format, E129: openai/evals event stream). The third format is **per-task JSON
files**, where each file contains both `model_output` and `target` fields joined by
`sample_id` across a flat directory.

## The third harness format

| Property | Description |
|---|---|
| **File layout** | `harness_output/task_XXX.json` in a flat directory. Each file contains `sample_id`, `model_output`, `target`. |
| **Join key** | `sample_id` — shared across key and output rows. |
| **Adapter tax** | **12 lines** of stdlib Python (including import block, directory listing, JSON parsing, field extraction). |

### Example file

```json
{
  "sample_id": "task_001",
  "model_output": "The cat sat on the mat.",
  "target": "The cat sat on the mat.",
  "domain": "sentiment"
}
```

## The adapter

The adapter (`preflight_third.py`) reads `*.json` files from a directory and yields
dicts with `sample_id`, `model_output`, `target` — the three fields `preflight.concordance`
uses for joining.

### Adapter code (12 lines of harness-specific Python)

```python
import json, os
from typing import Dict, Iterable

def make_third_harness_adapter(directory: str) -> Iterable[Dict[str, str]]:
    for fn in sorted(os.listdir(directory)):
        if not fn.endswith(".json"): continue
        with open(os.path.join(directory, fn)) as f:
            data = json.load(f)
        yield {"sample_id": data["sample_id"],
               "model_output": data["model_output"],
               "target": data["target"]}
```

## Measuring the adapter

| Harness | Output structure | Adapter lines | Join key |
|---|---|---|---|
| **E128** | modelscope/evalscope: two files (predictions + reviews) joined by `index` within task dir | ~8 lines | `index` |
| **E129** | openai/evals: single event stream, filtered for "match" events, joined by `sample_id` | ~10 lines | `sample_id` |
| **E130** | this experiment: per-task JSON files, joined by `sample_id` across flat dir | **12 lines** | `sample_id` |

All three adapters are **stdlib-only, no model calls, no domain knowledge**. The
variation in line count (8–12) reflects minor differences in file navigation
(sorted listing, `.json` suffix filter) rather than structural complexity.

## What this establishes

1. **The adapter pattern generalises across three harness types with fundamentally
   different output structures.** The adapter is consistently small (8–12 lines of
   stdlib code) and follows the same pattern: read the output format, extract the
   join key and relevant fields, yield rows for preflight.

2. **The "adapter tax" is real but small.** Each harness requires a small per-harness
   adapter, but none require a loader library or extensive reshaping. The tax is
   typically 8–12 lines of harness-specific Python, payable by anyone who wants to
   point preflight at their harness's run output.

3. **preflight can be pointed at any harness's run output with a small adapter.**
   The line reopens fully: the tool is reusable across different evaluation frameworks
   (modelscope/evalscope, openai/evals, and per-task JSON) with only the minimal
   adapter tax.

## What this does not establish

- **That the adapter is always ≤ 12 lines.** A harness with a more complex output
  structure (e.g., nested JSON, non-JSON formats, authenticated streams) may require
  a larger adapter. Three harnesses is a lower bound, not an upper bound.

- **That preflight should be released.** The tool works on the mission's own harnesses
  and can be pointed at run output with an adapter across three frameworks. Whether
  anyone outside this repository would use it is `untested`.

- **That the join is always `sample_id`.** The join key is a property of the harness's
  output writer. A different harness may use a different key.

## Next steps

If the adapter size is confirmed small across additional harness types, the preflight
tool can be released with a per-harness adapter interface. If a fourth harness
requires a significantly larger adapter, the line should be re-evaluated.