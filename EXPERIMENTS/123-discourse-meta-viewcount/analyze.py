#!/usr/bin/env python3
"""Analyze the unserved need topics from meta.discourse.org."""

import json
import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent.parent
e121_path = repo_root / "EXPERIMENTS" / "121-codereview-e119"
sys.path.insert(0, str(e121_path))
import os
old_cwd = Path.cwd()
os.chdir(e121_path)
from classifier_discourse import classify_discourse_item
os.chdir(old_cwd)

data_path = Path(__file__).parent / "data_meta.jsonl"
with open(data_path) as f:
    rows = [json.loads(l) for l in f]

need_unserved = []
need_served = []
for r in rows:
    cls = classify_discourse_item(r.get('combined_text', ''))
    if cls == 'need-related':
        reply_count = r.get('reply_count', 0)
        has_accepted = r.get('has_accepted_answer', False)
        unserved = (reply_count == 0) and (not has_accepted)
        if unserved:
            need_unserved.append(r)
        else:
            need_served.append(r)

print(f'Unserved need topics: {len(need_unserved)}')
print(f'Served need topics: {len(need_served)}')
print()
print('=== Sample Unserved Need Topics ===')
for r in need_unserved[:30]:
    print(f'  [{r.get("category", "")}] {r.get("title", "")[:100]} (views: {r.get("view_count", 0)}, replies: {r.get("reply_count", 0)})')

print()
print('=== By Category ===')
from collections import Counter
cat_unserved = Counter(r.get('category', '') for r in need_unserved)
cat_served = Counter(r.get('category', '') for r in need_served)
for cat in sorted(set(cat_unserved.keys()) | set(cat_served.keys())):
    u = cat_unserved.get(cat, 0)
    s = cat_served.get(cat, 0)
    total = u + s
    rate = u / total * 100 if total > 0 else 0
    print(f'  {cat}: {u}/{total} unserved ({rate:.1f}%)')

print()
print('=== By Tags ===')
tag_unserved = Counter()
for r in need_unserved:
    for tag in r.get('tags', []):
        if isinstance(tag, str):
            tag_unserved[tag] += 1
        elif isinstance(tag, dict) and 'name' in tag:
            tag_unserved[tag['name']] += 1
for tag, count in tag_unserved.most_common(20):
    print(f'  {tag}: {count}')

print()
print('=== High-view Unserved (potential high-impact) ===')
high_view = sorted(need_unserved, key=lambda r: r.get('view_count', 0), reverse=True)[:15]
for r in high_view:
    print(f'  [{r.get("category", "")}] {r.get("title", "")[:100]} (views: {r.get("view_count", 0)})')