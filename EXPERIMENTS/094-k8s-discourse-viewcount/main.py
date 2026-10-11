<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-11
-->
#!/usr/bin/env python3
"""
Experiment 094: View-count principle on Kubernetes Discourse forum — Main runner.
"""

import json
import random
import sys
import time
import urllib.request
from datetime import datetime
from typing import List, Dict, Optional

from stats import Topic, classify_topic, is_unserved, mann_whitney_u, wilson_ci_lower, wilson_ci_upper

BASE_URL = "https://discuss.kubernetes.io"
CATEGORY_ID = 6
CATEGORY_SLUG = "general-discussions"
PER_PAGE = 30
MAX_PAGES = 50
MAX_TOPICS = 500
RATE_LIMIT_DELAY = 1.0
REQUEST_TIMEOUT = 30


def fetch_json(url: str) -> Optional[Dict]:
    """Fetch JSON from URL with timeout and error handling."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (experiment)'})
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"ERROR fetching {url}: {e}", file=sys.stderr)
        return None


def fetch_category_page(page: int) -> Optional[Dict]:
    """Fetch a page of topics from the category."""
    url = f"{BASE_URL}/c/{CATEGORY_SLUG}/{CATEGORY_ID}.json?page={page}"
    return fetch_json(url)


def main():
    print("=" * 60)
    print("Experiment 094: Kubernetes Discourse View-Count Principle")
    print("=" * 60)

    all_topics: List[Topic] = []
    classification_log = []

    for page in range(MAX_PAGES):
        print(f"Fetching page {page + 1}/{MAX_PAGES}...")
        data = fetch_category_page(page)
        if not data:
            print(f"  Failed to fetch page {page}, stopping.")
            break

        topic_list = data.get("topic_list", {})
        topics = topic_list.get("topics", [])

        if not topics:
            print(f"  No topics on page {page}, stopping.")
            break

        for t in topics:
            if len(all_topics) >= MAX_TOPICS:
                break

            topic = Topic(
                id=t["id"],
                title=t["title"],
                slug=t.get("slug", ""),
                views=t.get("views", 0),
                reply_count=t.get("reply_count", 0),
                posts_count=t.get("posts_count", 0),
                has_accepted_answer=t.get("has_accepted_answer", False),
                created_at=t.get("created_at", ""),
                last_posted_at=t.get("last_posted_at", ""),
                tags=[tag["name"] for tag in t.get("tags", [])],
                category_id=t.get("category_id", CATEGORY_ID),
                excerpt=t.get("excerpt", "")[:500],
            )
            all_topics.append(topic)

        if len(all_topics) >= MAX_TOPICS:
            break

        time.sleep(RATE_LIMIT_DELAY + random.uniform(0, 0.5))

    print(f"Fetched {len(all_topics)} topics total.")

    print("Classifying topics...")
    for topic in all_topics:
        topic.classification = classify_topic(topic)
        topic.unserved = is_unserved(topic)

        classification_log.append({
            "id": topic.id,
            "title": topic.title,
            "views": topic.views,
            "reply_count": topic.reply_count,
            "has_accepted_answer": topic.has_accepted_answer,
            "classification": topic.classification,
            "unserved": topic.unserved,
            "tags": topic.tags,
            "excerpt_preview": topic.excerpt[:100]
        })

    error_topics = [t for t in all_topics if t.classification == "error" and t.views >= MIN_VIEWS_FOR_ANALYSIS]
    non_error_topics = [t for t in all_topics if t.classification == "non-error" and t.views >= MIN_VIEWS_FOR_ANALYSIS]
    excluded_topics = [t for t in all_topics if t.classification == "excluded"]
    unclassified_topics = [t for t in all_topics if t.classification == "unclassified"]

    print(f"\nClassification results:")
    print(f"  Error (treatment): {len(error_topics)}")
    print(f"  Non-error (control): {len(non_error_topics)}")
    print(f"  Excluded: {len(excluded_topics)}")
    print(f"  Unclassified: {len(unclassified_topics)}")

    g1_pass = len(error_topics) >= 100 and len(non_error_topics) >= 100
    print(f"\nG1 (Population ≥100 each): {'PASS' if g1_pass else 'FAIL'} (error={len(error_topics)}, non-error={len(non_error_topics)})")

    total_analyzed = len(error_topics) + len(non_error_topics)
    topics_with_views = sum(1 for t in error_topics + non_error_topics if t.views is not None and t.views >= 0)
    view_coverage = topics_with_views / total_analyzed if total_analyzed > 0 else 0
    g4_pass = view_coverage >= 0.95
    print(f"G4 (View-count coverage ≥95%): {'PASS' if g4_pass else 'FAIL'} ({view_coverage:.1%})")

    if total_analyzed == 0:
        print("No topics to analyze. Aborting.")
        return 1

    error_views = [t.views for t in error_topics]
    non_error_views = [t.views for t in non_error_topics]

    error_median = statistics.median(error_views) if error_views else 0
    non_error_median = statistics.median(non_error_views) if non_error_views else 0
    error_mean = statistics.mean(error_views) if error_views else 0
    non_error_mean = statistics.mean(non_error_views) if non_error_views else 0

    print(f"\nView count statistics:")
    print(f"  Error topics: n={len(error_views)}, median={error_median}, mean={error_mean:.1f}")
    print(f"  Non-error topics: n={len(non_error_views)}, median={non_error_median}, mean={non_error_mean:.1f}")

    u_stat, p_value = mann_whitney_u(error_views, non_error_views)
    g2_pass = p_value < 0.05 and error_median > non_error_median
    print(f"\nG2 (View-count separation, MWU p<0.05): {'PASS' if g2_pass else 'FAIL'}")
    print(f"  U={u_stat:.1f}, p={p_value:.6f}, error_median > non_error_median: {error_median > non_error_median}")

    error_unserved = sum(1 for t in error_topics if t.unserved)
    non_error_unserved = sum(1 for t in non_error_topics if t.unserved)

    error_unserved_frac = error_unserved / len(error_topics) if error_topics else 0
    non_error_unserved_frac = non_error_unserved / len(non_error_topics) if non_error_topics else 0

    error_ci_lower = wilson_ci_lower(error_unserved, len(error_topics))
    error_ci_upper = wilson_ci_upper(error_unserved, len(error_topics))
    non_error_ci_lower = wilson_ci_lower(non_error_unserved, len(non_error_topics))
    non_error_ci_upper = wilson_ci_upper(non_error_unserved, len(non_error_topics))

    print(f"\nUnserved-open-like fraction (reply_count=0 AND no accepted answer):")
    print(f"  Error: {error_unserved}/{len(error_topics)} = {error_unserved_frac:.3f} (CI95: [{error_ci_lower:.3f}, {error_ci_upper:.3f}])")
    print(f"  Non-error: {non_error_unserved}/{len(non_error_topics)} = {non_error_unserved_frac:.3f} (CI95: [{non_error_ci_lower:.3f}, {non_error_ci_upper:.3f}])")

    g3_pass = error_ci_upper < 0.60
    print(f"\nG3 (Unserved CI95 upper < 60%): {'PASS' if g3_pass else 'FAIL'} (upper={error_ci_upper:.3f})")

    all_gates_pass = g1_pass and g2_pass and g3_pass and g4_pass
    print(f"\n{'=' * 60}")
    print(f"OVERALL: {'ALL GATES PASS' if all_gates_pass else 'SOME GATES FAIL'}")
    print(f"{'=' * 60}")

    results = {
        "experiment": "094-k8s-discourse-viewcount",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "source": f"{BASE_URL}/c/{CATEGORY_SLUG}/{CATEGORY_ID}",
        "gates": {
            "G1_population": {"pass": g1_pass, "error_n": len(error_topics), "non_error_n": len(non_error_topics)},
            "G2_viewcount_separation": {"pass": g2_pass, "u_statistic": u_stat, "p_value": p_value, "error_median": error_median, "non_error_median": non_error_median},
            "G3_unserved_fraction": {"pass": g3_pass, "error_unserved": error_unserved, "error_total": len(error_topics), "fraction": error_unserved_frac, "ci95_lower": error_ci_lower, "ci95_upper": error_ci_upper},
            "G4_viewcount_coverage": {"pass": g4_pass, "coverage": view_coverage}
        },
        "summary": {
            "error_topics": {
                "n": len(error_topics),
                "median_views": error_median,
                "mean_views": error_mean,
                "unserved_count": error_unserved,
                "unserved_fraction": error_unserved_frac,
                "unserved_ci95": [error_ci_lower, error_ci_upper]
            },
            "non_error_topics": {
                "n": len(non_error_topics),
                "median_views": non_error_median,
                "mean_views": non_error_mean,
                "unserved_count": non_error_unserved,
                "unserved_fraction": non_error_unserved_frac,
                "unserved_ci95": [non_error_ci_lower, non_error_ci_upper]
            }
        },
        "classification_counts": {
            "error": len(error_topics),
            "non_error": len(non_error_topics),
            "excluded": len(excluded_topics),
            "unclassified": len(unclassified_topics)
        },
        "all_gates_pass": all_gates_pass
    }

    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)

    with open("classification.log.json", "w") as f:
        json.dump(classification_log, f, indent=2)

    print("\nResults written to results.json and classification.log.json")
    return 0 if all_gates_pass else 1


if __name__ == "__main__":
    sys.exit(main())