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
from __future__ import annotations

import json
import math
import os
import re
import sys
import time
import urllib.request
from typing import Any

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DEFAULT_TOPICS_PER_INSTANCE = 150
DEFAULT_DOMAIN_PATTERN = "https://{domain}/latest.json"
DEFAULT_SLEEP_BETWEEN_REQUESTS = 0.3  # seconds, polite polling
MAX_PAGES = 6  # 6 pages x 30 topics = 180 max, but we take first N

# Keyword patterns from E074 classification (NEED_PATTERNS / NON_NEED_PATTERNS)
NEED_PATTERNS = [
    r"\bhow (do|can|to|should|would|is|are)\b",
    r"\bwhat (is|are|should|would|could|causes?|makes?)\b",
    r"\bwhy (is|are|do|does|did|can|won|not)\b",
    r"\bhelp\b",
    r"\bissue|problem|error|broken|failure|not working\b",
    r"\brecommend|suggestion|advice\b",
    r"\bwhich (one|should|is best|to buy|to use|get)\b",
    r"\bwhere (can|to|is|are)\b",
    r"\bany (idea|suggestion|tip|advice|recommendation)\b",
    r"\bcan (someone|anybody|anyone)\b",
    r"\bstuck|confused|lost\b",
    r"\btrying to\b",
    r"\bwondering\b",
    r"\bshould I\b",
]

NON_NEED_PATTERNS = [
    r"\bIC\b",
    r"\bshow.*(off|me)\b",
    r"\bmy (new|first|latest) (setup|build|project|purchase)\b",
    r"\blook at (this|my)\b",
    r"\bjust (got|bought|picked up|received)\b",
    r"\bwhat.*(you|getting|ordering|buying)\b",
    r"\bwelcome to\b",
    r"\bthank(s| you)\b",
    r"\bimage(s)?\s*(only|thread)\b",
    r"\bpicture(s)?\s*(only|thread|uno)\b",
    r"\bintroductions?\b",
]


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------

def is_need_topic(title: str) -> bool:
    """Returns True if the topic title suggests a concrete need."""
    title_lower = title.lower()
    # First filter out non-need patterns
    for pattern in NON_NEED_PATTERNS:
        if re.search(pattern, title_lower):
            return False
    # Then check need patterns
    for pattern in NEED_PATTERNS:
        if re.search(pattern, title_lower):
            return True
    # If no pattern matches, it's not a need topic
    return False


def is_resolved(topic: dict) -> bool:
    """Returns True if the topic has a platform-recorded resolution."""
    # Check for accepted answer
    if topic.get("has_accepted_answer", False):
        return True
    # Check for sufficient engagement (reply_count >= 3 and op_like_count >= 1)
    if topic.get("reply_count", 0) >= 3 and topic.get("op_like_count", 0) >= 1:
        return True
    # Check if closed
    if topic.get("closed", False):
        return True
    return False


def is_unserved_open_like(topic: dict) -> tuple:
    """Apply the three-clause E074 rubric for unserved-open-like.

    Returns (is_unserved_open_like, reason).
    """
    # Clause 1: No platform-recorded resolution
    if is_resolved(topic):
        return False, "resolved"

    # Clause 2: States a concrete need
    title = topic.get("title", "")
    if not is_need_topic(title):
        return False, "not_a_need"

    # Clause 3: Not a request for content/service/price/access/human work
    # (already filtered by NON_NEED_PATTERNS in is_need_topic)

    return True, "unserved_open_like"


# ---------------------------------------------------------------------------
# Discourse API helpers
# ---------------------------------------------------------------------------

def fetch_latest_page(domain: str) -> dict | None:
    """Fetch the latest topics page from a Discourse forum."""
    url = DEFAULT_DOMAIN_PATTERN.format(domain=domain)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def harvest_forum_topics(domain: str, max_topics: int = DEFAULT_TOPICS_PER_INSTANCE) -> list[dict]:
    """Harvest topics from a Discourse forum across multiple pages.

    Returns a list of topic dicts, up to max_topics total.
    Each dict contains: id, title, views, reply_count, like_count,
    op_like_count, has_accepted_answer, closed, _domain.
    """
    all_topics: list[dict] = []
    url_template = "https://{domain}/latest.json?page={page}&per_page=30"

    for page in range(1, MAX_PAGES + 1):
        url = url_template.format(domain=domain, page=page)
        data = fetch_latest_page(domain)
        if data is None:
            break

        page_topics = data.get("topic_list", {}).get("topics", [])
        if not page_topics:
            break

        all_topics.extend(page_topics)

        if len(all_topics) >= max_topics:
            break

        time.sleep(DEFAULT_SLEEP_BETWEEN_REQUESTS)

    # Deduplicate by topic id
    seen_ids: set[int] = set()
    deduped: list[dict] = []
    for t in all_topics:
        tid = t.get("id", 0)
        if tid not in seen_ids:
            seen_ids.add(tid)
            deduped.append(t)
        if len(deduped) >= max_topics:
            break

    # Convert to our standardized topic dict format
    topics: list[dict] = []
    for t in deduped[:max_topics]:
        topic = {
            "id": t.get("id"),
            "title": t.get("title", ""),
            "views": t.get("views", 0),
            "reply_count": t.get("reply_count", 0),
            "like_count": t.get("like_count", 0),
            "op_like_count": t.get("op_like_count", 0),
            "has_accepted_answer": t.get("has_accepted_answer", False),
            "closed": t.get("closed", False),
            "_domain": domain,
        }
        topics.append(topic)

    return topics


# ---------------------------------------------------------------------------
# Measurement
# ---------------------------------------------------------------------------

def classify_topics(topics: list[dict]) -> list[dict]:
    """Classify each topic using the E074 rubric.

    Adds/overwrites these keys in each topic dict:
      - is_need: bool
      - is_resolved: bool
      - is_unserved_open_like: bool
      - classification_reason: str
    """
    results: list[dict] = []
    for t in topics:
        title = t.get("title", "")
        resolved = is_resolved(t)
        is_need = is_need_topic(title)
        is_uol, reason = is_unserved_open_like(t) if not resolved and is_need else (False, "resolved")

        t["is_need"] = is_need
        t["is_resolved"] = resolved
        t["is_unserved_open_like"] = is_uol
        t["classification_reason"] = reason
        results.append(t)
    return results


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
    import math  # ensure math is available
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