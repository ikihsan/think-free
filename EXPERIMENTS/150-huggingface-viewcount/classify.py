#!/usr/bin/env python3
"""
Classify models as need-related or general using shared classifier_lib.
"""
import json
import sys
sys.path.insert(0, "EXPERIMENTS/150-huggingface-viewcount")
from classifier_lib import classify_model


def main():
    input_path = "EXPERIMENTS/150-huggingface-viewcount/RAW_DATA.jsonl"
    output_path = "EXPERIMENTS/150-huggingface-viewcount/CLASSIFIED.jsonl"

    need_related = []
    general = []
    excluded = []

    with open(input_path) as f:
        for line in f:
            model = json.loads(line)
            classification, reasons = classify_model(model)
            model["_classification"] = classification
            model["_classification_reasons"] = reasons

            if classification == "need-related":
                need_related.append(model)
            elif classification == "general":
                general.append(model)
            else:
                excluded.append(model)

    # Write classified data
    with open(output_path, "w") as f:
        for model in need_related + general + excluded:
            f.write(json.dumps(model) + "\n")

    print(f"Need-related: {len(need_related)}")
    print(f"General: {len(general)}")
    print(f"Excluded: {len(excluded)}")
    print(f"Total: {len(need_related) + len(general) + len(excluded)}")

    # Print examples of each
    print("\n--- Need-related examples ---")
    for m in need_related[:15]:
        print(f"  {m.get('modelId')}: reasons={m['_classification_reasons']}")

    print("\n--- General examples ---")
    for m in general[:15]:
        print(f"  {m.get('modelId')}: reasons={m['_classification_reasons']}")

    print("\n--- Excluded examples ---")
    for m in excluded[:15]:
        print(f"  {m.get('modelId')}: reasons={m['_classification_reasons']}")


if __name__ == "__main__":
    main()