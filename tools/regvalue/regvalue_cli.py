#!/usr/bin/env python3
"""regvalue_cli — Extract and ground named values from regulatory text.

Reads a document and answer pairs, uses ground.py's canonicalizer
to determine whether each value claim in the answer is supported (grounded)
or not (ungrounded_value / ungrounded_claim) by the document it references.

Usage:
    python3 regvalue_cli.py <document_path> <answers_jsonl> [threshold=0.6]

Where answers_jsonl is a JSONL file with rows like:
    {"document_number": "2023-1", "question": "How much is the penalty?", "answer": "The penalty is \$500,000."}
"""

import json
import sys
import os

# Import ground.py components
sys.path.insert(0, 'EXPERIMENTS/114-value-grounding')
import ground


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 regvalue_cli.py <document_path> <answers_jsonl> [threshold=0.6]",
              file=sys.stderr)
        sys.exit(1)

    doc_path = sys.argv[1]
    answers_path = sys.argv[2]
    threshold = float(sys.argv[3]) if len(sys.argv) > 3 else 0.6

    # Normalize document using ground.py's normalize (tags removed, html unesced, line wraps joined)
    with open(doc_path, "rb") as f:
        raw = f.read().decode("utf-8", "replace")
    doc = ground.normalize(raw)

    rows = [json.loads(l) for l in open(answers_path) if l.strip()]

    for r in rows:
        num = r.get("document_number", "")
        # Use ground.judge() — the canonical implementation
        checked = ground.judge(doc, r["answer"], threshold)
        r["checked"] = checked
        r["n_values"] = len(checked)
        # Print each value verdict
        verdicts = []
        for v in checked:
            verdicts.append(f"[{v['verdict']}] {v['kind']}: {v['value']} (score={v['score']})")
        print(f"Document {num}: {', '.join(verdicts)}")

    # Summary
    total_values = sum(r["n_values"] for r in rows)
    grounded = sum(sum(1 for v in r["checked"] if v["verdict"] == "grounded") for r in rows)
    ungrounded_value = sum(sum(1 for v in r["checked"] if v["verdict"] == "ungrounded_value") for r in rows)
    ungrounded_claim = sum(sum(1 for v in r["checked"] if v["verdict"] == "ungrounded_claim") for r in rows)

    print(f"\nTotal values checked: {total_values}")
    if total_values > 0:
        print(f"Grounded: {grounded} ({grounded/total_values*100:.1f}%)")
        print(f"Ungrounded_value: {ungrounded_value} ({ungrounded_value/total_values*100:.1f}%)")
        print(f"Ungrounded_claim: {ungrounded_claim} ({ungrounded_claim/total_values*100:.1f}%)")


if __name__ == "__main__":
    main()