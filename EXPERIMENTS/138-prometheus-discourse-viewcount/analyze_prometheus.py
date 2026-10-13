#!/usr/bin/env python3"
"""
Analyze Prometheus Discourse experiment results.
"""

import json
import sys
from collections import Counter


def load_classified(jsonl_path: str):
    topics = []
    with open(jsonl_path, "r") as f:
        for line in f:
            topics.append(json.loads(line))
    return topics


def load_results(json_path: str):
    with open(json_path, "r") as f:
        return json.load(f)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 analyze_prometheus.py <classified.jsonl>")
        sys.exit(1)

    input_path = sys.argv[1]
    topics = load_classified(input_path)

    results_path = input_path.replace("_classified.jsonl", "_results.json")
    results = load_results(results_path)

    print("=" * 60)
    print("E138 - PROMETHEUS DISCOURSE ANALYSIS")
    print("=" * 60)

    # Classification breakdown
    cls_counts = Counter(t.get("classification", "unknown") for t in topics)
    print(f"\nClassification:")
    for cls, count in cls_counts.most_common():
        print(f"  {cls}: {count}")

    # Pattern match analysis for need-related
    need_topics = [t for t in topics if t.get("classification") == "need"]
    pattern_counts = Counter()
    for t in need_topics:
        for p in t.get("matched_patterns", []):
            pattern_counts[p] += 1

    print(f"\nNeed pattern matches (top 20):")
    for pattern, count in pattern_counts.most_common(20):
        print(f"  {pattern}: {count}")

    # Excluded pattern analysis
    excluded_topics = [t for t in topics if t.get("classification") == "excluded"]
    excluded_patterns = Counter()
    for t in excluded_topics:
        for p in t.get("matched_patterns", []):
            excluded_patterns[p] += 1

    print(f"\nExcluded pattern matches:")
    for pattern, count in excluded_patterns.most_common():
        print(f"  {pattern}: {count}")

    # Unserved analysis (zero replies)
    need_zero_replies = [t for t in need_topics if t.get("reply_count", 0) == 0]
    print(f"\nUnserved topics (zero replies): {len(need_zero_replies)}/{len(need_topics)}")

    if need_zero_replies:
        print(f"\nSample unserved topics:")
        for t in need_zero_replies[:10]:
            print(f"  [{t.get('category')}] {t.get('title')} (views: {t.get('view_count')})")

    # Served topics (with replies)
    need_with_replies = [t for t in need_topics if t.get("reply_count", 0) > 0]
    print(f"\nServed topics (≥1 reply): {len(need_with_replies)}/{len(need_topics)}")

    # By category
    print(f"\nBy category:")
    for cat in sorted(set(t.get("category") for t in topics)):
        cat_topics = [t for t in topics if t.get("category") == cat]
        cat_need = [t for t in cat_topics if t.get("classification") == "need"]
        cat_zero = [t for t in cat_need if t.get("reply_count", 0) == 0]
        print(f"  {cat}: {len(cat_topics)} total, {len(cat_need)} need, {len(cat_zero)} zero-reply")

    # View count distribution
    need_views = [t.get("view_count", 0) for t in need_topics]
    random_views = [t for t in topics if t.get("classification") == "random"]
    random_views = [t.get("view_count", 0) for t in random_views]

    if need_views and random_views:
        print(f"\nView count stats:")
        print(f"  Need: median={sorted(need_views)[len(need_views)//2]}, mean={sum(need_views)/len(need_views):.1f}, max={max(need_views)}")
        print(f"  Random: median={sorted(random_views)[len(random_views)//2]}, mean={sum(random_views)/len(random_views):.1f}, max={max(random_views)}")

    # Gate summary
    print(f"\n{'='*60}")
    print("GATE SUMMARY")
    print(f"{'='*60}")
    for gate in ["g1", "g2", "g3", "g4"]:
        g = results.get(gate, {})
        status = "PASS" if g.get("pass") else "FAIL"
        print(f"  {gate.upper()}: {status}")

    print(f"\nOVERALL: {results.get('overall', 'UNKNOWN')}")


if __name__ == "__main__":
    main()