"""Built-in adapters for common harness output formats.

Each adapter exports an `adapt(harness_dir)` function that returns
(key_rows, out_rows, items, rows_for_c3) compatible with preflight's checks.

Adapter interface:
    def adapt(harness_dir: str) -> tuple[list[dict], list[dict], list[dict], list[dict]]:
        '''
        Args:
            harness_dir: path to the harness run output directory

        Returns:
            key_rows: list of dicts with at least 'sample_id' and 'expected'
            out_rows: list of dicts with at least 'sample_id', 'model_output', 'expected'
            items: list of dicts with at least 'arm', 'value', 'correct' (bool)
            rows_for_c3: list of dicts with at least 'id', 'evidence', 'is_positive' (bool)
        '''

The yielded rows may contain additional fields; preflight's checks will use
shared field names for C1 (concordance), the 'value' and 'correct' fields for
C2 (alternate-form FP), and the 'evidence' and 'is_positive' fields for C3
(control arm).
"""

import csv
import json
import os
import xml.etree.ElementTree as ET
from typing import List, Dict, Tuple, Iterable

try:
    import yaml
except ImportError:
    yaml = None


# --------------------------------------------------------------------------- JSONL (per-task files, E130)
def adapt_jsonl(harness_dir: str) -> Tuple[List[Dict], List[Dict], List[Dict], List[Dict]]:
    """Adapter for per-task JSON files (E130 format).

    Expected structure:
        harness_dir/
          task_001.json  {sample_id, model_output, target, correct?}
          task_002.json
          ...

    If "correct" is not present, defaults to True.
    """
    key_rows = []
    out_rows = []
    items = []
    rows_for_c3 = []

    for filename in sorted(os.listdir(harness_dir)):
        if not filename.endswith(".json"):
            continue
        filepath = os.path.join(harness_dir, filename)
        with open(filepath, "r") as f:
            data = json.load(f)
        row = {
            "sample_id": data["sample_id"],
            "model_output": data["model_output"],
            "target": data["target"],
        }
        correct = data.get("correct", True)
        if isinstance(correct, str):
            correct = correct.lower() == "true"
        else:
            correct = bool(correct)

        key_rows.append({"sample_id": row["sample_id"], "expected": row["target"]})
        out_rows.append({**row, "correct": correct})
        items.append({"arm": "default", "value": row["model_output"], "correct": correct})
        rows_for_c3.append({
            "id": row["sample_id"],
            "evidence": row["model_output"],
            "is_positive": row["target"].lower() in row["model_output"].lower(),
        })

    return key_rows, out_rows, items, rows_for_c3


# --------------------------------------------------------------------------- CSV (E131)
def adapt_csv(harness_dir: str) -> Tuple[List[Dict], List[Dict], List[Dict], List[Dict]]:
    """Adapter for CSV harness format (E131).

    Expected structure:
        harness_dir/
          harness.csv  # columns: sample_id, model_output, expected, correct
    """
    csv_path = os.path.join(harness_dir, "harness.csv")
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"harness.csv not found in {harness_dir}")

    rows = []
    with open(csv_path, newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            rows.append(row)

    key_rows = []
    out_rows = []
    items = []
    rows_for_c3 = []

    for row in rows:
        sid = row.get("sample_id", "")
        model_output = row.get("model_output", "")
        expected = row.get("expected", "")
        correct = row.get("correct", "").lower() == "true"

        out_rows.append({
            "sample_id": sid,
            "model_output": model_output,
            "expected": expected,
            "correct": correct,
        })
        key_rows.append({"sample_id": sid, "expected": expected})
        items.append({"arm": "default", "value": model_output, "correct": correct})
        rows_for_c3.append({
            "id": sid,
            "evidence": model_output,
            "is_positive": expected.lower() in model_output.lower() if expected else False,
        })

    return key_rows, out_rows, items, rows_for_c3


# --------------------------------------------------------------------------- YAML (E132)
def adapt_yaml(harness_dir: str) -> Tuple[List[Dict], List[Dict], List[Dict], List[Dict]]:
    """Adapter for YAML harness format (E132).

    Expected structure:
        harness_dir/
          harness.yaml  # list of entries: {sample_id, model_output, expected, correct}
    """
    if yaml is None:
        raise ImportError("PyYAML required for YAML adapter: pip install pyyaml")

    yaml_path = os.path.join(harness_dir, "harness.yaml")
    if not os.path.exists(yaml_path):
        raise FileNotFoundError(f"harness.yaml not found in {harness_dir}")

    with open(yaml_path) as fh:
        data = yaml.safe_load(fh)

    if data is None:
        entries = []
    elif isinstance(data, dict):
        entries = [data]
    elif isinstance(data, list):
        entries = data
    else:
        entries = []

    key_rows = []
    out_rows = []
    items = []
    rows_for_c3 = []

    for entry in entries:
        sid = entry.get("sample_id", "")
        model_output = entry.get("model_output", "")
        expected = entry.get("expected", "")
        correct_val = entry.get("correct", False)
        correct = correct_val.lower() == "true" if isinstance(correct_val, str) else bool(correct_val)

        out_rows.append({
            "sample_id": sid,
            "model_output": model_output,
            "expected": expected,
            "correct": correct,
        })
        key_rows.append({"sample_id": sid, "expected": expected})
        items.append({"arm": "default", "value": model_output, "correct": correct})
        rows_for_c3.append({
            "id": sid,
            "evidence": model_output,
            "is_positive": expected.lower() in model_output.lower() if expected else False,
        })

    return key_rows, out_rows, items, rows_for_c3


# --------------------------------------------------------------------------- XML (E133)
def adapt_xml(harness_dir: str) -> Tuple[List[Dict], List[Dict], List[Dict], List[Dict]]:
    """Adapter for XML harness format (E133).

    Expected structure:
        harness_dir/
          harness.xml  # <harness><entry><sample_id>...</sample_id>...</entry></harness>
    """
    xml_path = os.path.join(harness_dir, "harness.xml")
    if not os.path.exists(xml_path):
        raise FileNotFoundError(f"harness.xml not found in {harness_dir}")

    tree = ET.parse(xml_path)
    root = tree.getroot()

    entries = []
    for child in root:
        if child.tag == "entry":
            entry = {}
            for sub in child:
                entry[sub.tag] = sub.text
            entries.append(entry)

    key_rows = []
    out_rows = []
    items = []
    rows_for_c3 = []

    for entry in entries:
        sid = entry.get("sample_id", "")
        model_output = entry.get("model_output", "")
        expected = entry.get("expected", "")
        correct_str = entry.get("correct", "").lower()
        correct = correct_str == "true" if isinstance(correct_str, str) else bool(correct_str)

        out_rows.append({
            "sample_id": sid,
            "model_output": model_output,
            "expected": expected,
            "correct": correct,
        })
        key_rows.append({"sample_id": sid, "expected": expected})
        items.append({"arm": "default", "value": model_output, "correct": correct})
        rows_for_c3.append({
            "id": sid,
            "evidence": model_output,
            "is_positive": expected.lower() in model_output.lower() if expected else False,
        })

    return key_rows, out_rows, items, rows_for_c3


# --------------------------------------------------------------------------- Registry of built-in adapters
BUILTIN_ADAPTERS = {
    "jsonl": adapt_jsonl,
    "csv": adapt_csv,
    "yaml": adapt_yaml,
    "xml": adapt_xml,
}


def get_builtin_adapter(name: str):
    """Get a built-in adapter by name."""
    if name not in BUILTIN_ADAPTERS:
        raise ValueError(f"Unknown built-in adapter: {name}. Available: {list(BUILTIN_ADAPTERS.keys())}")
    return BUILTIN_ADAPTERS[name]