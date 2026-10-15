"""Adapter for modelscope/evalscope run output format.

Reads predictions and reviews directories and produces (key_rows, out_rows)
for preflight.concordance. The join key is 'index' within each task directory.

Format (per E128):
- predictions_dir/{model}/{benchmark}_{subset}.jsonl with 'index' field
- reviews_dir/{model}/{benchmark}_{subset}.jsonl with 'index' field
"""

import json
import os
import glob


def _load_jsonl(path):
    """Load all records from a JSONL file."""
    records = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def adapt_evalscope(predictions_dir, reviews_dir):
    """Adapter for evalscope run output.

    Returns (key_rows, out_rows) where:
    - key_rows: list of {"task": str, "index": int} per prediction row
    - out_rows: list of {"task": str, "index": int, "score": float, "target": str} per review row

    Adapter tax: ~10 lines (schema mapping for two file types, join by index)
    """
    key_rows = []
    out_rows = []

    # Find all prediction files
    pred_pattern = os.path.join(predictions_dir, "**", "*.jsonl")
    for pred_path in sorted(glob.glob(pred_pattern, recursive=True)):
        # Extract task name from path: predictions_dir/{model}/{task}.jsonl
        rel_path = os.path.relpath(pred_path, predictions_dir)
        task = rel_path.replace(".jsonl", "").replace(os.sep, "/")

        # Find corresponding review file
        review_path = os.path.join(reviews_dir, rel_path)
        if not os.path.exists(review_path):
            continue

        predictions = _load_jsonl(pred_path)
        reviews = _load_jsonl(review_path)

        # Build review lookup by index
        review_by_index = {r["index"]: r for r in reviews}

        for pred in predictions:
            idx = pred["index"]
            key_rows.append({"task": task, "index": idx})

            review = review_by_index.get(idx)
            if review:
                out_rows.append({
                    "task": task,
                    "index": idx,
                    "score": review.get("score"),
                    "target": review.get("target"),
                })
            else:
                out_rows.append({"task": task, "index": idx})

    return key_rows, out_rows


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python evalscope_adapter.py <predictions_dir> <reviews_dir>")
        sys.exit(1)

    key_rows, out_rows = adapt_evalscope(sys.argv[1], sys.argv[2])
    print(f"key_rows: {len(key_rows)}")
    print(f"out_rows: {len(out_rows)}")
    for kr in key_rows[:3]:
        print(f"  key: {kr}")
    for or_ in out_rows[:3]:
        print(f"  out: {or_}")