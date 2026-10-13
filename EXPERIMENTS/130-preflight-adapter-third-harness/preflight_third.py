"""E130 — adapter for third-harness output format.

Reads per-task JSON files (sample_id, model_output, target) and yields rows
compatible with preflight.concordance. Stdlib only, no model calls, no domain
knowledge. The adapter tax is ~12 lines of harness-specific Python.

Used as:

    from preflight_third import make_third_harness_adapter

    key_rows = list(make_third_harness_adapter("path/to/key"))   # scorer's key
    out_rows = list(make_third_harness_adapter("path/to/output"))  # model outputs

    from preflight import concordance
    result = concordance(key_rows, out_rows)
    # result["verdict"] ∈ {OK, SILENT_NO_MATCH, PARTIAL_MATCH, NO_DISCRIMINATING_PAIRING}
"""

import json
import os
from typing import Dict, List, Tuple, Iterable


def make_third_harness_adapter(directory: str) -> Iterable[Dict[str, str]]:
    """Read per-task JSON files and yield rows with sample_id, model_output, target.

    Each task_XXX.json is expected to contain at minimum:
        {
            "sample_id": "task_001",
            "model_output": "the model's prediction text",
            "target": "the ground truth / expected answer"
        }

    The yielded dict always contains the three fields above, plus any extra fields
    present in the file.

    Args:
        directory: path to the directory containing task_XXX.json files.

    Yields:
        dict with at least: sample_id, model_output, target
    """
    for filename in sorted(os.listdir(directory)):
        if not filename.endswith(".json"):
            continue
        filepath = os.path.join(directory, filename)
        with open(filepath, "r") as f:
            data = json.load(f)
        row = {"sample_id": data["sample_id"]}
        row["model_output"] = data["model_output"]
        row["target"] = data["target"]
        # Carry any extra fields through so the row is rich enough for pairing
        for k, v in data.items():
            if k not in ("sample_id", "model_output", "target"):
                row[k] = v
        yield row