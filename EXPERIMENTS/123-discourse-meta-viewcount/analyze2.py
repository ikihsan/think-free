#!/usr/bin/env python3
"""Analyze served need topics and genuine technical questions."""

import json
import sys
from pathlib import Path
from collections import Counter

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

print('=== Served Need Topics (sample) ===')
for r in need_served[:20]:
    print(f'  [{r.get("category", "")}] {r.get("title", "")[:100]} (views: {r.get("view_count", 0)}, replies: {r.get("reply_count", 0)})')

print()
print('=== Unserved GENUINE Technical Questions (dev/bug categories, excluding blog-like) ===')
blog_indicators = ['blog', 'case study', 'guide', 'tutorial', 'walkthrough', 'introduction', 'overview', 'anniversary', 'celebrating', 'yearly review', 'gives back', 'edition', 'strategy for', 'ways to', 'how to monetize', 'build a culture']
genuine_unserved = []
for r in need_unserved:
    title_lower = r.get('title', '').lower()
    is_blog = any(ind in title_lower for ind in blog_indicators)
    if not is_blog and r.get('category') in ('dev', 'bug', 'mods'):
        genuine_unserved.append(r)

print(f'Genuine technical unserved: {len(genuine_unserved)}')
for r in genuine_unserved:
    print(f'  [{r.get("category", "")}] {r.get("title", "")[:100]} (views: {r.get("view_count", 0)}, replies: {r.get("reply_count", 0)})')

print()
print('=== Served GENUINE Technical Questions ===')
genuine_served = []
for r in need_served:
    title_lower = r.get('title', '').lower()
    is_blog = any(ind in title_lower for ind in blog_indicators)
    if not is_blog and r.get('category') in ('dev', 'bug', 'mods'):
        genuine_served.append(r)

print(f'Genuine technical served: {len(genuine_served)}')
for r in genuine_served[:20]:
    print(f'  [{r.get("category", "")}] {r.get("title", "")[:100]} (views: {r.get("view_count", 0)}, replies: {r.get("reply_count", 0)})')

# Overall genuine stats
genuine_total = len(genuine_unserved) + len(genuine_served)
genuine_unserved_frac = len(genuine_unserved) / genuine_total if genuine_total > 0 else 0
print(f'\nGenuine technical unserved fraction: {genuine_unserved_frac:.1%} ({len(genuine_unserved)}/{genuine_total})')