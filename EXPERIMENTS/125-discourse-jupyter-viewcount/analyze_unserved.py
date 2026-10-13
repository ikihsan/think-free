#!/usr/bin/env python3
"""Analyze unserved fraction on Jupyter Discourse (despite G2 failure)."""

import json
import sys
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "124-discourse-gnome-viewcount"))
from classifier_gnome import classify_gnome_item

data_path = Path(__file__).parent / "data_jupyter.jsonl"
with open(data_path) as f:
    rows = [json.loads(l) for l in f]

need_items = []
for r in rows:
    combined = r.get('combined_text', '').lower()
    classification = classify_gnome_item(combined)
    
    if classification != 'need-related':
        continue
    
    reply_count = r.get('reply_count', 0)
    has_accepted = r.get('has_accepted_answer', False)
    unserved = (reply_count == 0) and (not has_accepted)
    need_items.append({'row': r, 'unserved': unserved})

n_actual = len(need_items)
u_count = sum(1 for i in need_items if i['unserved'])
s_count = n_actual - u_count
frac = u_count / n_actual if n_actual > 0 else 0
z = 1.96; n = n_actual; p = frac
denom = 1 + z**2 / n; centre = (p + z**2/(2*n)) / denom
half = (z / denom) * math.sqrt(p*(1-p)/n + z**2/(4*n**2))
ci_low, ci_high = centre - half, centre + half

print(f"Classified need-related: {n_actual}")
print(f"Unserved: {u_count} ({frac*100:.1f}%)")
print(f"Served: {s_count}")
print(f"Wilson CI95: [{ci_low*100:.1f}%, {ci_high*100:.1f}%]")

print("\n=== Sample Unserved Need Topics ===")
for item in need_items:
    if item['unserved']:
        r = item['row']
        print(f"  [{r.get('category', '')}] {r.get('title', '')[:100]} (views: {r.get('view_count', 0)})")

print("\n=== Sample Served Need Topics ===")
served_count = 0
for item in need_items:
    if not item['unserved'] and served_count < 10:
        r = item['row']
        print(f"  [{r.get('category', '')}] {r.get('title', '')[:100]} (views: {r.get('view_count', 0)}, replies: {r.get('reply_count', 0)})")
        served_count += 1