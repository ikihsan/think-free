#!/usr/bin/env python3
"""explain_misses.py — classify misses and false positives for E143.

A miss is an arm where M2 verdict is "clear" but independent check finds
ungrounded values. We classify each miss as:
- value_present: the value is real, in the CFR amendments, but attached
  to the wrong subject (binding error)
- not_extracted: the value is not extracted at all by M2's extractor

A false positive is an arm where M2 verdict is "condemn" but independent
check finds all values grounded.
"""
import json
import os
import sys
import re

HERE = os.path.dirname(os.path.abspath(__file__))
VALUES_DIR = os.path.join(HERE, "..", "140-judge-form-invariance")
GROUND_DIR = os.path.join(HERE, "..", "114-value-grounding")
sys.path.insert(0, VALUES_DIR)
sys.path.insert(0, GROUND_DIR)
import valueset
import ground


def classify_miss(preamble, cfr_amendments):
    """Classify a single miss (preamble cleared by M2 but has ungrounded values)."""
    preamble_vals = ground.extract(preamble)
    ungrounded = []
    for kind, raw in preamble_vals:
        found = False
        for cand in ground.renderings(raw, kind):
            if cand.lower() in cfr_amendments.lower():
                found = True
                break
        if not found:
            ungrounded.append((kind, raw))

    if not ungrounded:
        return "none", []

    # Classify each ungrounded value
    classifications = []
    for kind, raw in ungrounded:
        # Check if the numeric part appears in CFR
        nums = re.findall(r'\d+(?:[.,]\d+)?', raw)
        found_in_cfr = False
        for num in nums:
            if num in cfr_amendments:
                found_in_cfr = True
                break

        if found_in_cfr:
            classifications.append("value_present")
        else:
            classifications.append("not_extracted")

    if "value_present" in classifications:
        return "value_present", classifications
    else:
        return "not_extracted", classifications


def main():
    arms_path = os.path.join(HERE, "arms.jsonl")
    gates_path = os.path.join(HERE, "gates.json")

    if not os.path.exists(arms_path):
        print("ERROR: arms.jsonl not found. Run build_arms.py first.")
        return 1
    if not os.path.exists(gates_path):
        print("ERROR: gates.json not found. Run score.py first.")
        return 1

    arms = {}
    with open(arms_path) as f:
        for line in f:
            arm = json.loads(line)
            arms[arm["document_number"]] = arm

    with open(gates_path) as f:
        gates_data = json.load(f)

    results = gates_data["results"]

    misses = []
    for r in results:
        if r["verdict_m2"] == "clear" and r["preamble_values_count"] > 0:
            doc_num = r["document_number"]
            arm = arms[doc_num]
            classification, details = classify_miss(arm["preamble"], arm["cfr_amendments"])
            misses.append({
                "document_number": doc_num,
                "title": arm["title"],
                "classification": classification,
                "details": details,
            })

    # False positives: M2 says condemn but all values grounded
    false_positives = []
    for r in results:
        if r["verdict_m2"] == "condemn":
            doc_num = r["document_number"]
            arm = arms[doc_num]
            preamble_vals = ground.extract(arm["preamble"])
            all_grounded = True
            for kind, raw in preamble_vals:
                found = False
                for cand in ground.renderings(raw, kind):
                    if cand.lower() in arm["cfr_amendments"].lower():
                        found = True
                        break
                if not found:
                    all_grounded = False
                    break
            if all_grounded:
                false_positives.append({
                    "document_number": doc_num,
                    "title": arm["title"],
                    "extra_values": r["extra_values_m2"],
                })

    output = {
        "misses": misses,
        "false_positives": false_positives,
        "counts": {
            "total_misses": len(misses),
            "value_present": sum(1 for m in misses if m["classification"] == "value_present"),
            "not_extracted": sum(1 for m in misses if m["classification"] == "not_extracted"),
            "false_positives": len(false_positives),
        }
    }

    out_path = os.path.join(HERE, "misses.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Misses: {len(misses)}")
    print(f"  value_present: {output['counts']['value_present']}")
    print(f"  not_extracted: {output['counts']['not_extracted']}")
    print(f"False positives: {len(false_positives)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())