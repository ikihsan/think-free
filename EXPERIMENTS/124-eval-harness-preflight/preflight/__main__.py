#!/usr/bin/env python3
"""preflight CLI -- three checks on the instrument that produces an evaluation rate.

Usage:
    python3 -m preflight <adapter> <harness_dir> [--anyway] [--fp-ceiling FLOAT]

Adapters:
    jsonl      Per-task JSON files (task_XXX.json) with sample_id, model_output, target
    csv        CSV file (harness.csv) with columns: sample_id, model_output, expected, correct
    yaml       YAML file (harness.yaml) with entries: sample_id, model_output, expected, correct
    xml        XML file (harness.xml) with <entry> elements under <harness> root
    ultraeval  UltraEval-Audio format: res/{model}/{dataset}/{timestamp}.jsonl

Options:
    --anyway          Print the rate even when checks fail (says checks failed)
    --fp-ceiling F    False-positive ceiling for C2 (default: 0.02)
    --premise P       Control arm premise for C3 (default: 0.0)
    --help            Show this help and exit

Examples:
    python3 -m preflight csv ./my_harness_dir
    python3 -m preflight jsonl ./eval_output --anyway
    python3 -m preflight yaml ./harness --fp-ceiling 0.05
    python3 -m preflight ultraeval ./ultraeval_output
"""

import json
import os
import sys

# Ensure the preflight package is importable
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

from preflight import concordance, alternate_form_fp, control_arm, render
from preflight.report import EXIT_OK, EXIT_USAGE, EXIT_WITHHELD, headline


def load_jsonl(path):
    """Load a JSONL file as a list of dicts."""
    with open(path) as fh:
        return [json.loads(line) for line in fh if line.strip()]


def load_csv(path):
    """Load a CSV file as a list of dicts."""
    import csv
    with open(path, newline="") as fh:
        reader = csv.DictReader(fh)
        return [row for row in reader]


def load_yaml(path):
    """Load a YAML file as a list of dicts."""
    import yaml
    with open(path) as fh:
        data = yaml.safe_load(fh)
    if data is None:
        return []
    if isinstance(data, dict):
        return [data]
    if isinstance(data, list):
        return data
    return []


def load_xml(path):
    """Load an XML harness file as a list of dicts."""
    import xml.etree.ElementTree as ET
    tree = ET.parse(path)
    root = tree.getroot()
    entries = []
    for child in root:
        if child.tag == "entry":
            entry = {}
            for sub in child:
                entry[sub.tag] = sub.text
            entries.append(entry)
    return entries


def adapter_jsonl(harness_dir):
    """Adapter for per-task JSON files (task_XXX.json) or results.jsonl."""
    entries = []

    # Try results.jsonl first (E130 format)
    results_path = os.path.join(harness_dir, "results.jsonl")
    if os.path.exists(results_path):
        with open(results_path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                data = json.loads(line)
                sid = data.get("sample_id")
                if not sid:
                    continue
                entries.append({
                    "sample_id": sid,
                    "model_output": data.get("model_output", ""),
                    "expected": data.get("expected", ""),
                    "correct": data.get("correct", False),
                })
    else:
        # Fall back to per-task JSON files (task_XXX.json)
        for fn in sorted(os.listdir(harness_dir)):
            if not fn.endswith(".json"):
                continue
            if not fn.startswith("task_"):
                continue
            with open(os.path.join(harness_dir, fn)) as f:
                data = json.load(f)
            sid = data.get("sample_id")
            if not sid:
                continue
            entries.append({
                "sample_id": sid,
                "model_output": data.get("model_output", ""),
                "expected": data.get("target", data.get("expected", "")),
                "correct": data.get("correct", False),
            })

    out_rows = entries[:]
    key_rows = [{"sample_id": e["sample_id"], "expected": e["expected"]} for e in entries]

    items = [{"arm": "default", "value": e["model_output"], "correct": e["correct"]} for e in entries]

    rows = []
    for e in entries:
        is_pos = e["expected"].lower() in e["model_output"].lower() if e["expected"] else False
        rows.append({
            "sample_id": e["sample_id"],
            "id": e["sample_id"],
            "evidence": e["model_output"],
            "is_positive": is_pos,
        })

    return key_rows, out_rows, items, rows


def adapter_csv(harness_dir):
    """Adapter for CSV format (harness.csv)."""
    csv_path = os.path.join(harness_dir, "harness.csv")
    rows = load_csv(csv_path)

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

        items.append({
            "arm": "default",
            "value": model_output,
            "correct": correct,
        })

        is_pos = expected.lower() in model_output.lower() if expected else False
        rows_for_c3.append({
            "sample_id": sid,
            "id": sid,
            "evidence": model_output,
            "is_positive": is_pos,
        })

    key_rows = [{"sample_id": r["sample_id"], "expected": r["expected"]} for r in out_rows]

    return key_rows, out_rows, items, rows_for_c3


def adapter_yaml(harness_dir):
    """Adapter for YAML format (harness.yaml)."""
    yaml_path = os.path.join(harness_dir, "harness.yaml")
    entries = load_yaml(yaml_path)

    out_rows = []
    items = []
    rows_for_c3 = []

    for entry in entries:
        sid = entry.get("sample_id", "")
        model_output = entry.get("model_output", "")
        expected = entry.get("expected", "")
        correct_raw = entry.get("correct", False)
        if isinstance(correct_raw, str):
            correct = correct_raw.lower() == "true"
        else:
            correct = bool(correct_raw)

        out_rows.append({
            "sample_id": sid,
            "model_output": model_output,
            "expected": expected,
            "correct": correct,
        })

        items.append({
            "arm": "default",
            "value": model_output,
            "correct": correct,
        })

        is_pos = expected.lower() in model_output.lower() if expected else False
        rows_for_c3.append({
            "sample_id": sid,
            "id": sid,
            "evidence": model_output,
            "is_positive": is_pos,
        })

    key_rows = [{"sample_id": e["sample_id"], "expected": e["expected"]} for e in entries]

    return key_rows, out_rows, items, rows_for_c3


def adapter_xml(harness_dir):
    """Adapter for XML format (harness.xml)."""
    xml_path = os.path.join(harness_dir, "harness.xml")
    entries = load_xml(xml_path)

    out_rows = []
    items = []
    rows_for_c3 = []

    for entry in entries:
        sid = entry.get("sample_id", "")
        model_output = entry.get("model_output", "")
        expected = entry.get("expected", "")
        correct_raw = entry.get("correct", "")
        correct = correct_raw.lower() == "true" if isinstance(correct_raw, str) else bool(correct_raw)

        out_rows.append({
            "sample_id": sid,
            "model_output": model_output,
            "expected": expected,
            "correct": correct,
        })

        items.append({
            "arm": "default",
            "value": model_output,
            "correct": correct,
        })

        is_pos = expected.lower() in model_output.lower() if expected else False
        rows_for_c3.append({
            "sample_id": sid,
            "id": sid,
            "evidence": model_output,
            "is_positive": is_pos,
        })

    key_rows = [{"sample_id": e["sample_id"], "expected": e["expected"]} for e in entries]

    return key_rows, out_rows, items, rows_for_c3


def adapter_ultraeval(harness_dir):
    """Adapter for UltraEval-Audio format: res/{model}/{dataset}/{timestamp}.jsonl"""
    entries = []

    # Look for res/{model}/{dataset}/*.jsonl files (excluding overview files)
    res_dir = os.path.join(harness_dir, "res")
    if not os.path.isdir(res_dir):
        # Maybe the harness_dir IS the res dir
        res_dir = harness_dir

    for root, dirs, files in os.walk(res_dir):
        for fn in files:
            if fn.endswith(".jsonl") and not fn.endswith("-overview.jsonl"):
                jsonl_path = os.path.join(root, fn)
                with open(jsonl_path) as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        data = json.loads(line)
                        sid = data.get("sample_id")
                        if not sid:
                            continue
                        entries.append({
                            "sample_id": sid,
                            "model_output": data.get("model_output", ""),
                            "expected": data.get("expected", ""),
                            "correct": data.get("correct", False),
                        })

    out_rows = entries[:]
    key_rows = [{"sample_id": e["sample_id"], "expected": e["expected"]} for e in entries]

    items = [{"arm": "default", "value": e["model_output"], "correct": e["correct"]} for e in entries]

    rows = []
    for e in entries:
        is_pos = e["expected"].lower() in e["model_output"].lower() if e["expected"] else False
        rows.append({
            "sample_id": e["sample_id"],
            "id": e["sample_id"],
            "evidence": e["model_output"],
            "is_positive": is_pos,
        })

    return key_rows, out_rows, items, rows


ADAPTERS = {
    "jsonl": adapter_jsonl,
    "csv": adapter_csv,
    "yaml": adapter_yaml,
    "xml": adapter_xml,
    "ultraeval": adapter_ultraeval,
}


def print_help():
    print(__doc__)
    sys.exit(EXIT_USAGE)


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print_help()

    adapter_name = sys.argv[1]

    if adapter_name not in ADAPTERS:
        print(f"Unknown adapter: {adapter_name}", file=sys.stderr)
        print(f"Available adapters: {', '.join(ADAPTERS.keys())}", file=sys.stderr)
        sys.exit(EXIT_USAGE)

    # Parse remaining args
    harness_dir = None
    anyway = False
    fp_ceiling = 0.02
    premise = 0.0

    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--anyway":
            anyway = True
        elif arg == "--fp-ceiling":
            i += 1
            if i >= len(sys.argv):
                print("--fp-ceiling requires a value", file=sys.stderr)
                sys.exit(EXIT_USAGE)
            fp_ceiling = float(sys.argv[i])
        elif arg == "--premise":
            i += 1
            if i >= len(sys.argv):
                print("--premise requires a value", file=sys.stderr)
                sys.exit(EXIT_USAGE)
            premise = float(sys.argv[i])
        elif arg.startswith("-"):
            print(f"Unknown option: {arg}", file=sys.stderr)
            sys.exit(EXIT_USAGE)
        else:
            if harness_dir is None:
                harness_dir = arg
            else:
                print(f"Unexpected argument: {arg}", file=sys.stderr)
                sys.exit(EXIT_USAGE)
        i += 1

    if harness_dir is None:
        print("Missing harness directory", file=sys.stderr)
        print_help()

    if not os.path.isdir(harness_dir):
        print(f"Harness directory not found: {harness_dir}", file=sys.stderr)
        sys.exit(EXIT_USAGE)

    # Run the adapter
    try:
        key_rows, out_rows, items, rows = ADAPTERS[adapter_name](harness_dir)
    except Exception as e:
        print(f"Adapter {adapter_name} failed: {e}", file=sys.stderr)
        sys.exit(EXIT_USAGE)

    # C1: concordance
    c1 = concordance(key_rows, out_rows)

    # C2: alternate-form FP
    def flagger(item):
        if item.get("correct"):
            return None
        else:
            return "ungrounded_value"

    c2 = alternate_form_fp(items, flagger, fp_ceiling=fp_ceiling)

    # C3: control arm
    is_positive = lambda r: r.get("is_positive", False)
    c3 = control_arm(rows, is_positive, premise=premise, name="control")

    checks = [
        {"check": "C1_concordance", "verdict": c1["verdict"], "reason": c1.get("reason", ""), "summary": c1.get("summary", "")},
        {"check": "C2_alternate_form_fp", "verdict": c2["verdict"], "reason": c2.get("reason", ""), "summary": c2.get("summary", "")},
        {"check": "C3_control_arm", "verdict": c3["verdict"], "reason": c3.get("reason", ""), "summary": c3.get("summary", "")},
    ]

    # Compute a headline rate (fraction of correct items)
    if items:
        correct_count = sum(1 for i in items if i.get("correct"))
        rate = f"{correct_count/len(items):.4f}"
    else:
        rate = "0.0000"

    text, code = render(checks, rate=rate, label="preflight", anyway=anyway)

    print(text)
    sys.exit(code)


if __name__ == "__main__":
    main()