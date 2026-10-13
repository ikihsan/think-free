#!/usr/bin/env python3
"""Analyze coverage issues on Jupyter Discourse."""

import json
import sys
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(__file__).parent.parent / "124-discourse-gnome-viewcount"))
from classifier_gnome import classify_gnome_item, compute_gnome_coverage

data_path = Path(__file__).parent / "data_jupyter.jsonl"
with open(data_path) as f:
    rows = [json.loads(l) for l in f]

# Classify all
coverage_result = compute_gnome_coverage(rows)
print(f"Total: {coverage_result['total']}")
print(f"Classified: {coverage_result['classified']} ({coverage_result['coverage']*100:.1f}%)")
print(f"Need-related: {coverage_result['need_related']}")
print(f"Random: {coverage_result['random']}")
print(f"Unclassified: {coverage_result['unclassified']}")
print()

# Show which excluded patterns are matching
print("=== Excluded Pattern Matches ===")
for pattern, count in coverage_result['by_pattern'].most_common(30):
    if pattern.startswith("EXCLUDED:"):
        print(f"  {pattern}: {count}")

print()
print("=== Need Pattern Matches ===")
for pattern, count in coverage_result['by_pattern'].most_common(30):
    if pattern.startswith("NEED:"):
        print(f"  {pattern}: {count}")

print()
print("=== Sample Unclassified Topics ===")
unclassified_samples = []
for r in rows:
    cls = classify_gnome_item(r.get('combined_text', ''))
    if cls == 'unclassified':
        unclassified_samples.append(r)
    if len(unclassified_samples) >= 30:
        break

for r in unclassified_samples:
    print(f"  [{r.get('category', '')}] {r.get('title', '')[:100]}")