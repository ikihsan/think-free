#!/usr/bin/env python3
"""explain_misses.py — classify every miss by a fact about the row.

A miss is an arm where M2 says 'clear' but the arm is genuinely unsupported
(M2 missed a real error). Each miss is classified as:
  - value_present: the extra value IS in the reference text (binding error —
    the value is real but attached to the wrong subject)
  - not_extracted: the extra value is NOT in the reference text and M2 didn't
    extract it from the submission (extraction failure)

Standard library only, deterministic.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "140-judge-form-invariance"))
sys.path.insert(0, os.path.join(HERE, "..", "114-value-grounding"))
import valueset  # noqa: E402
import ground  # noqa: E402


def classify_miss(arm):
    """Classify a miss: value_present or not_extracted."""
    sub = arm["summary"]
    ref = arm["reference"]
    sub_vals = valueset.canonical(sub)
    ref_vals = valueset.canonical(ref)
    extra = [k for k in sub_vals if k not in ref_vals]

    if not extra:
        return "no_extra"

    # For each extra value, check if it's actually in the reference
    for key in extra:
        kind, val = key
        found = False
        if isinstance(val, (int, float)):
            val_str = str(int(val)) if val == int(val) else str(val)
            val_comma = f"{int(val):,}" if val == int(val) else str(val)
            for raw_val in [val_str, val_comma, f"{val:.1f}", f"{val:.2f}"]:
                if raw_val in ref:
                    found = True
                    break
        else:
            if str(val).lower() in ref.lower():
                found = True
        if found:
            return "value_present"
    return "not_extracted"


def main():
    scored_path = os.path.join(HERE, "scored_arms.jsonl")
    if not os.path.exists(scored_path):
        print("ERROR: scored_arms.jsonl not found. Run score.py first.")
        return 1

    arms = [json.loads(l) for l in open(scored_path) if l.strip()]

    # Find misses: M2 says clear but genuinely unsupported
    misses = [a for a in arms if a["m2_verdict"] == "clear" and a["genuinely_unsupported"]]

    mechanisms = {"value_present": 0, "not_extracted": 0, "no_extra": 0}
    miss_details = []

    for arm in misses:
        mech = classify_miss(arm)
        mechanisms[mech] = mechanisms.get(mech, 0) + 1
        miss_details.append({
            "document_number": arm["document_number"],
            "mechanism": mech,
            "summary_excerpt": arm["summary"][:200],
        })

    n_misses = len(misses)
    result = {
        "n_misses": n_misses,
        "mechanisms": mechanisms,
        "value_present_share": round(mechanisms["value_present"] / n_misses, 4) if n_misses else 0.0,
        "not_extracted_share": round(mechanisms["not_extracted"] / n_misses, 4) if n_misses else 0.0,
    }

    out_path = os.path.join(HERE, "misses.json")
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)

    # Save miss details
    details_path = os.path.join(HERE, "miss_details.jsonl")
    with open(details_path, "w") as f:
        for d in miss_details:
            f.write(json.dumps(d, sort_keys=True) + "\n")

    print(f"Misses: {n_misses}")
    print(f"Mechanisms: {mechanisms}")
    print(f"value_present share: {result['value_present_share']}")
    print(f"not_extracted share: {result['not_extracted_share']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
