#!/usr/bin/env python3
"""
ground-prototype-cli.py — improved mechanical value grounding checker (CLI).

Extends ground.py (E114) to address its explicit limitations:
  (1) More rendering forms for CFR/U.S.C./FR citations
  (2) Context presence check: whether surrounding words in the answer
      also appear near the value in the document
  (3) Richer verdict types: grounded, ungrounded_value, ungrounded_claim,
      ungrounded_context

This is an exploratory prototype. It is NOT claimed as a finished product
or a new algorithm validated for publication. It gathers evidence about
whether mechanical checks can do better than the v1 baseline.

Usage:
    python3 ground-prototype-cli.py <rawdir> <answers.jsonl> <threshold> <output.jsonl>

Example:
    python3 ground-prototype-cli.py raw answers.jsonl 0.6 checked-output.jsonl
"""

import sys
import os
import json

# Dynamically load the core module by file path to avoid Python's
# module-name restrictions (hyphens in directory names like 114-value-grounding)
core_path = os.path.join(
    os.path.dirname(__file__),
    "ground_prototype_core.py"
)
spec = __import__("importlib").util.spec_from_file_location(
    "ground_prototype_core", core_path
)
_core = __import__("importlib").util.module_from_spec(spec)
spec.loader.exec_module(_core)

# Assign core functions at module level for direct use
normalize = _core.normalize
judge = _core.judge
extract = _core.extract
renderings = _core.renderings
renderings_in_doc = _core.renderings_in_doc
STOP = _core.STOP
MONTHS = _core.MONTHS
ABBR = _core.ABBR
PATTERNS = _core.PATTERNS
BOUND = _core.BOUND
SUFFIX = _core.SUFFIX
content_words = _core.content_words
date_renderings = _core.date_renderings
stem = _core.stem


def main():
    rawdir = sys.argv[1] if len(sys.argv) > 1 else "raw"
    answers = sys.argv[2] if len(sys.argv) > 2 else "answers.jsonl"
    threshold = float(sys.argv[3]) if len(sys.argv) > 3 else 0.6
    out_name = sys.argv[4] if len(sys.argv) > 4 else "checked-prototype.jsonl"

    # Load answers
    rows = [json.loads(l) for l in open(answers) if l.strip()]

    # Cache documents
    cache = {}
    for r in rows:
        num = r["document_number"]
        if num not in cache:
            cache[num] = normalize(
                open(os.path.join(rawdir, "text", num + ".txt"), "rb")
                .read()
                .decode("utf-8", "replace")
            )

    # Run checker on each row
    total = 0
    counts = {}

    for r in rows:
        num = r["document_number"]
        doc = cache[num]
        r["checked"] = judge(doc, r["answer"], threshold)
        r["n_values"] = len(r["checked"])
        total += len(r["checked"])
        for v in r["checked"]:
            verdict = v["verdict"]
            counts[verdict] = counts.get(verdict, 0) + 1

    # Print summary
    verdict_key = lambda v: v["verdict"]
    print(json.dumps({
        "threshold": threshold,
        "rows": len(rows),
        "values_checked": total,
        "counts": counts,
        "per_verdict": {
            "ungrounded_value": counts.get("ungrounded_value", 0),
            "ungrounded_claim": counts.get("ungrounded_claim", 0),
            "ungrounded_context": counts.get("ungrounded_context", 0),
            "grounded": counts.get("grounded", 0),
        }
    }, sort_keys=True))

    # Write output
    out_dir = os.path.dirname(os.path.abspath(out_name))
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)
    with open(out_name, "w") as fh:
        for r in rows:
            fh.write(json.dumps(r, sort_keys=True) + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())