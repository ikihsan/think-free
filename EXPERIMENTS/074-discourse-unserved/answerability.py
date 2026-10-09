#!/usr/bin/env python3
"""Extract top 20 unremedied topics by view_count for answerability sub-test."""
import json
import os

CLASS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "classification.json")

with open(CLASS_PATH) as f:
    results = json.load(f)

# Filter to unserved-open-like
unserved = [r for r in results if r["is_unserved_open_like"]]

# Sort by views (arrival) descending
unserved_sorted = sorted(unserved, key=lambda x: x["views"], reverse=True)

# Top 20
top20 = unserved_sorted[:20]

print("=== Top 20 Unserved-Open-Like Topics by View Count ===\n")
for i, t in enumerate(top20, 1):
    print(f"{i}. [{t['domain']}] {t['title']}")
    print(f"   views={t['views']}, replies={t['reply_count']}, op_likes={t['op_like_count']}")
    print()

# Save for the answerability test
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw", "answerability_top20.json")
with open(output_path, "w") as f:
    json.dump(top20, f, indent=2)
print(f"Saved to {output_path}")
