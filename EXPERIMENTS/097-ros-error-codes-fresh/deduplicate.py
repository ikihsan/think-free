#!/usr/bin/env python3
"""
Deduplicate practitioner rows and create clean dataset.
"""

import json

# Load raw data
rows = []
with open('raw/practitioner_rows.jsonl', 'r') as f:
    for line in f:
        rows.append(json.loads(line))

# Deduplicate by topic_id
seen = set()
unique_rows = []
for row in rows:
    tid = row['topic_id']
    if tid not in seen:
        seen.add(tid)
        unique_rows.append(row)

print(f"Original: {len(rows)} rows, Unique: {len(unique_rows)} rows")

# Save deduplicated
with open('raw/practitioner_rows_dedup.jsonl', 'w') as f:
    for row in unique_rows:
        f.write(json.dumps(row) + '\n')

# Print summary
print("\nUnique Practitioner Rows:")
print(f"{'#':<3} {'Category':<20} {'Views':<6} {'Replies':<7} {'Title'}")
print("-" * 100)
for i, row in enumerate(unique_rows, 1):
    cat = row.get('category_name', 'Unknown')[:18]
    views = row.get('views', 0)
    replies = row.get('reply_count', 0)
    title = row.get('title', '')[:60]
    print(f"{i:<3} {cat:<20} {views:<6} {replies:<7} {title}")