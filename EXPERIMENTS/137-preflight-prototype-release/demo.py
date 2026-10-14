#!/usr/bin/env python3
"""E137 — preflight prototype demo.

Demonstrates the preflight tool with per-harness adapters using the test data
from the existing experiments (E128, E129, E130, E136).

The preflight checks (C1 concordance, C2 alternate-form FP, C3 control arm)
are imported from the installed preflight package at /home/ubuntu/think-free/preflight/.
The per-harness adapter functions are standalone functions defined in this script,
transforming harness output into the row format that preflight expects.
"""

import os
import sys
import json

HERE = "/home/ubuntu/think-free/EXPERIMENTS/137-preflight-prototype-release"

# Ensure the installed preflight package is found first.
# It is at /home/ubuntu/think-free/preflight, add its parent to sys.path.
_PREFLIGHT_PARENT = "/home/ubuntu/think-free/preflight"
if _PREFLIGHT_PARENT not in sys.path:
    sys.path.insert(0, _PREFLIGHT_PARENT)

from preflight import concordance, alternate_form_fp, control_arm, render


# ---- Per-harness adapter functions (standalone, no package needed) ----

def make_third_harness_adapter(directory):
    """E130: read per-task JSON files and yield rows with sample_id, model_output, target."""
    for filename in sorted(os.listdir(directory)):
        if not filename.endswith(".json"):
            continue
        filepath = os.path.join(directory, filename)
        with open(filepath, "r") as f:
            data = json.load(f)
        row = {"sample_id": data["sample_id"],
               "model_output": data["model_output"],
               "target": data["target"]}
        for k, v in data.items():
            if k not in ("sample_id", "model_output", "target"):
                row[k] = v
        yield row


def make_openai_adapter(directory):
    """E129: read event stream, filter for "match" events, extract sample_id/model_output/expected."""
    events = []
    for fn in sorted(os.listdir(directory)):
        if not fn.endswith('.jsonl') and not fn.endswith('.json'):
            continue
        path = os.path.join(directory, fn)
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        events.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    match_events = [e for e in events if e.get("type") == "match"]
    results = []
    for e in match_events:
        data = e.get("data", {})
        results.append({
            "sample_id": e.get("sample_id", ""),
            "model_output": data.get("picked", ""),
            "expected": data.get("expected", ""),
            "correct": data.get("correct", False),
        })
    return results


def make_eighth_harness_adapter(harness_dir):
    """E136: transform results.json + key/ground_truth.json + output/model_results.json format."""
    harness_dir = os.path.abspath(harness_dir)
    results_path = os.path.join(harness_dir, "results.json")
    key_path = os.path.join(harness_dir, "key", "ground_truth.json")

    with open(results_path) as fh:
        harness = json.load(fh)
    with open(key_path) as fh:
        key_data = json.load(fh)

    out_rows = []
    items = []
    rows_for_c3 = []

    for sid, entry in harness.items():
        model_output = entry.get("model_output", "")
        expected = entry.get("expected", "")
        correct = entry.get("correct", False)

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

    key_rows = [{"sample_id": sid, "expected": key_data[sid]["expected"]} for sid in harness.keys()]

    return key_rows, out_rows, items, rows_for_c3


def demo_third_harness():
    """Demo with the E130 third-harness test data."""
    print("=" * 60)
    print("Demo 1: E130 third-harness adapter (per-task JSON)")
    print("=" * 60)

    key_dir = os.path.join(HERE, "test_data", "third", "key")
    out_dir = os.path.join(HERE, "test_data", "third", "output")

    key_rows = list(make_third_harness_adapter(key_dir))
    out_rows = list(make_third_harness_adapter(out_dir))

    print(f"Key rows: {len(key_rows)}")
    print(f"Output rows: {len(out_rows)}")

    result = concordance(key_rows, out_rows)
    print(f"C1 verdict: {result['verdict']}")
    print(f"C1 best_rate: {result['best_rate']}")
    print(f"C1 summary: {result['summary']}")
    print()


def demo_eighth_harness():
    """Demo with the E136 eighth-harness test data."""
    print("=" * 60)
    print("Demo 2: E136 eighth-harness adapter")
    print("=" * 60)

    harness_dir = os.path.join(HERE, "test_data", "eighth")

    key_rows, out_rows, items, rows_for_c3 = make_eighth_harness_adapter(harness_dir)

    # C1: concordance
    c1 = concordance(key_rows, out_rows)
    print("C1 - concordance:")
    print(f"  verdict: {c1['verdict']}")
    print(f"  best_rate: {c1.get('best_rate', 'N/A')}")
    print(f"  reason: {c1.get('reason', '')[:200]}")
    print()

    # C2: alternate-form FP
    def flagger_by_correct(item):
        if item.get("correct"):
            return None
        else:
            return "ungrounded_value"

    c2 = alternate_form_fp(items, flagger_by_correct, fp_ceiling=0.02)
    print("C2 - alternate-form FP:")
    print(f"  verdict: {c2['verdict']}")
    print(f"  worst_fp_wilson_lower: {c2.get('worst_fp_wilson_lower', 'N/A')}")
    print()

    # C3: control arm
    is_positive = lambda r: r.get("is_positive", False)
    c3 = control_arm(rows_for_c3[:5], is_positive, premise=0.0, name="C accounts")
    print("C3 - control arm:")
    print(f"  verdict: {c3['verdict']}")
    print(f"  rate: {c3.get('rate')}")
    print(f"  positives: {c3.get('positives')}")
    print()

    # Headline
    checks = [
        {"check": "C1_concordance", "verdict": c1["verdict"], "reason": c1.get("reason", "")},
        {"check": "C2_alternate_form_fp", "verdict": c2["verdict"], "reason": c2.get("reason", "")},
        {"check": "C3_control_arm", "verdict": c3["verdict"], "reason": c3.get("reason", "")},
    ]
    text, code = render(checks)
    print("Headline:")
    print(text)
    print(f"Exit code: {code}")
    print()


def main():
    demo_third_harness()
    demo_eighth_harness()
    print("All demos complete.")


if __name__ == "__main__":
    main()