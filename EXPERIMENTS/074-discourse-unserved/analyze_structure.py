#!/usr/bin/env python3
"""Analyze structure of harvested Discourse topics."""
import json
import os

raw_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw", "discourse_topics.json")
with open(raw_path) as f:
    topics = json.load(f)

print(f"Total topics: {len(topics)}")
print(f"\nFirst topic keys: {list(topics[0].keys())}")
print(f"\nSample topic:")
t = topics[0]
for k, v in sorted(t.items()):
    if k == "_body":
        print(f"  {k}: {v[:100]}...")
    else:
        print(f"  {k}: {v}")

# Check for solved-related fields
solved_fields = [k for k in topics[0].keys() if "solved" in k.lower() or "close" in k.lower() or "resolve" in k.lower()]
print(f"\nSolved/closed/resolved fields: {solved_fields}")

# Check for accepted answer fields
accepted_fields = [k for k in topics[0].keys() if "accept" in k.lower() or "answer" in k.lower()]
print(f"Answer-related fields: {accepted_fields}")

# Check for category/tags
tag_fields = [k for k in topics[0].keys() if "tag" in k.lower() or "categ" in k.lower()]
print(f"Tag/category fields: {tag_fields}")

# Summary stats
print(f"\n=== Summary Stats ===")
for field in ["views", "reply_count", "like_count", "category_id"]:
    vals = [t.get(field, 0) for t in topics]
    nonzero = sum(1 for v in vals if v > 0)
    print(f"  {field}: nonzero={nonzero}/{len(vals)}, mean={sum(vals)/len(vals):.1f}, max={max(vals)}")

# Sample titles from each domain
print(f"\n=== Sample titles by domain ===")
for domain in set(t["_domain"] for t in topics):
    dt = [t for t in topics if t["_domain"] == domain][:10]
    print(f"\n{domain}:")
    for t in dt:
        print(f"  [{t['reply_count']} replies, {t['like_count']} likes, {t['views']} views] {t['title'][:70]}")
