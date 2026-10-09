#!/usr/bin/env python3
"""
E076 — Discourse need-serving rate measurement tool.

A stdlib-only prototype that harvests topics from a Discourse forum and
measures the need-serving rate using the view_count (arrival) instrument.

Protocol:
  1. Connect to a Discourse forum via its /latest.json endpoint
  2. Harvest the latest N topics (default: 150)
  3. For each topic, classify it as a "need" or "non-need" using title patterns
  4. For need topics, apply the unserved-open-like rubric:
       (a) No platform-recorded resolution (no accepted answer, low engagement)
       (b) States a concrete need (title matches need keywords)
       (c) Not a request for content, service, price, access, or human work
  5. Measure view_count for each topic (arrival field)
  6. Compute the unserved-open-like fraction

This generalises the E074 measurement into a reusable instrument.
"""
import json
import math
import os
import sys

from harvest_classify import (
    DEFAULT_TOPICS_PER_INSTANCE,
    DEFAULT_DOMAIN_PATTERN,
    DEFAULT_SLEEP_BETWEEN_REQUESTS,
    MAX_PAGES,
    fetch_latest_page,
    classify_topics,
    harvest_forum_topics,
)


def measure_need_serving_rate(domain: str, max_topics: int = DEFAULT_TOPICS_PER_INSTANCE) -> dict:
    """Full measurement pipeline for a Discourse forum.

    Returns a dict with:
      - total: number of topics harvested
      - view_positive: count with views > 0
      - need_topics: count classified as need topics
      - unserved_open_like: count classified as unserved-open-like
      - unserved_fraction: unserved_open_like / total (float)
      - by_domain_breakdown: dict of domain -> stats
      - wilson_ci95: (low, high) Wilson score interval 95%
    """
    # Harvest topics
    topics = harvest_forum_topics(domain, max_topics=max_topics)
    total = len(topics)

    if total == 0:
        return {
            "total": 0,
            "view_positive": 0,
            "need_topics": 0,
            "unserved_open_like": 0,
            "unserved_fraction": 0.0,
            "by_domain_breakdown": {},
            "wilson_ci95": [0.0, 0.0],
        }

    # Classify
    classified = classify_topics(topics)

    # Count
    view_positive = sum(1 for t in classified if t["views"] > 0)
    need_topics = sum(1 for t in classified if t["is_need"])
    unserved_open_like = sum(1 for t in classified if t["is_unserved_open_like"])

    # Wilson CI95 for the unserved fraction
    n = total
    k = unserved_open_like
    p = k / n if n > 0 else 0.0
    z = 1.96
    denom = 1 + z**2 / n
    centre = (p + z**2 / (2 * n)) / denom
    half = (z / denom) * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2))
    ci_low = centre - half
    ci_high = centre + half

    # By-domain breakdown (each topic already has _domain)
    by_domain: dict[str, dict] = {}
    for t in classified:
        d = t["_domain"]
        if d not in by_domain:
            by_domain[d] = {
                "total": 0,
                "view_positive": 0,
                "need_topics": 0,
                "unserved_open_like": 0,
            }
        by_domain[d]["total"] += 1
        if t["views"] > 0:
            by_domain[d]["view_positive"] += 1
        if t["is_need"]:
            by_domain[d]["need_topics"] += 1
        if t["is_unserved_open_like"]:
            by_domain[d]["unserved_open_like"] += 1

    return {
        "total": total,
        "view_positive": view_positive,
        "need_topics": need_topics,
        "unserved_open_like": unserved_open_like,
        "unserved_fraction": p,
        "wilson_ci95": [ci_low, ci_high],
        "by_domain_breakdown": by_domain,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    """CLI entry point for the E076 Discourse need-serving rate measurement."""

    if len(sys.argv) < 2:
        print("Usage: python3 run.py <forum-domain> [max-topics]")
        print("  e.g.: python3 run.py community.anovaculinary.com 150")
        print("  Measures need-serving rate for the given Discourse forum.")
        return 1

    domain = sys.argv[1]
    max_topics = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_TOPICS_PER_INSTANCE

    print(f"=== E076 Discourse Need-Serving Rate Measurement ===")
    print(f"Forum: {domain}")
    print(f"Max topics: {max_topics}")
    print()

    # Harvest topics
    topics = harvest_forum_topics(domain, max_topics=max_topics)
    total = len(topics)

    print(f"Harvested {total} topics from {domain}")

    if total == 0:
        print("No topics harvested. Check the forum domain and network access.")
        return 0

    # Classify
    classified = classify_topics(topics)

    # Count
    view_positive = sum(1 for t in classified if t["views"] > 0)
    need_topics = sum(1 for t in classified if t["is_need"])
    unserved_open_like = sum(1 for t in classified if t["is_unserved_open_like"])

    # Wilson CI95 for the unserved fraction
    n = total
    k = unserved_open_like
    p = k / n if n > 0 else 0.0
    z = 1.96
    denom = 1 + z**2 / n
    centre = (p + z**2 / (2 * n)) / denom
    half = (z / denom) * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2))
    ci_low = centre - half
    ci_high = centre + half

    # Display results
    print(f"\n=== Results ===")
    print(f"Topics with view_count > 0: {view_positive}/{total} "
          f"({view_positive/total*100:.1f}%)")
    print(f"Need topics: {need_topics}/{total} "
          f"({need_topics/total*100:.1f}%)")
    print(f"Unserved-open-like: {unserved_open_like}/{total} "
          f"({p*100:.2f}%)")
    print(f"Wilson CI95: [{ci_low*100:.2f}%, {ci_high*100:.2f}%]")

    # By-domain breakdown
    by_domain: dict[str, dict] = {}
    for t in classified:
        d = t["_domain"]
        if d not in by_domain:
            by_domain[d] = {
                "total": 0,
                "view_positive": 0,
                "need_topics": 0,
                "unserved_open_like": 0,
            }
        by_domain[d]["total"] += 1
        if t["views"] > 0:
            by_domain[d]["view_positive"] += 1
        if t["is_need"]:
            by_domain[d]["need_topics"] += 1
        if t["is_unserved_open_like"]:
            by_domain[d]["unserved_open_like"] += 1

    print(f"\n=== By Domain ===")
    for d in sorted(by_domain.keys()):
        bd = by_domain[d]
        print(f"  {d}:")
        print(f"    {bd['unserved_open_like']}/{bd['total']} = {bd['unserved_open_like']/bd['total']*100:.2f}% unserved-open-like")
        print(f"    {bd['need_topics']}/{bd['total']} need topics")
        print(f"    {bd['view_positive']}/{bd['total']} with view_count > 0")

    # Save result to file
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "results.json")
    with open(output_path, "w") as fh:
        json.dump({
            "total": total,
            "view_positive": view_positive,
            "need_topics": need_topics,
            "unserved_open_like": unserved_open_like,
            "unserved_fraction": p,
            "wilson_ci95": [ci_low, ci_high],
            "by_domain_breakdown": by_domain,
        }, fh, sort_keys=True, indent=2)
    print(f"\n=== Result saved to {output_path} ===")

    return 0


if __name__ == "__main__":
    sys.exit(main())