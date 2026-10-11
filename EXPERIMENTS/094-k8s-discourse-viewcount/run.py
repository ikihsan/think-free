#!/usr/bin/env python3
"""
Experiment 094: View-count principle on Kubernetes Discourse forum
Tests whether the view-count principle generalizes to Kubernetes error/failure topics.
Optimized: uses excerpts from category list, no per-topic API calls.
"""

import json
import urllib.request
import urllib.parse
import time
import random
import statistics
import sys
import math
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

# Configuration
BASE_URL = "https://discuss.kubernetes.io"
CATEGORY_ID = 6  # General Discussions
CATEGORY_SLUG = "general-discussions"
PER_PAGE = 30
MAX_PAGES = 50
MAX_TOPICS = 500
RATE_LIMIT_DELAY = 1.0  # seconds between requests
REQUEST_TIMEOUT = 30

# Pre-declared classification keywords (written before first fetch)
ERROR_KEYWORDS = [
    "error", "failed", "fail", "crash", "exit code", "error code",
    "rpc error", "timeout", "deadline", "oom", "kill", "panic",
    "exception", "traceback", "stack trace", "500", "502", "503", "504",
    "404", "403", "connection refused", "connection reset", "dial tcp",
    "i/o timeout", "context deadline", "unknown desc", "malformed",
    "unexpected eof", "not ready", "not healthy", "crashloop", "backoff",
    "evicted", "pending", "imagepull", "errimagepull",
    "createcontainerconfigerror", "createcontainererror", "invalid",
    "denied", "forbidden", "unauthorized", "certificate", "tls", "x509"
]

NON_ERROR_KEYWORDS = [
    "how to", "best practice", "recommend", "suggest", "opinion",
    "discussion", "announcement", "release", "version", "upgrade",
    "migration", "strategy", "architecture", "design", "pattern",
    "tutorial", "guide", "tip", "trick", "experience", "story",
    "case study", "comparison", "vs ", "versus", "alternative",
    "tool", "monitoring", "observability", "logging", "metrics",
    "dashboard", "visualization", "cicd", "gitops", "argocd", "flux",
    "helm", "kustomize", "operator", "crd", "custom resource"
]

EXCLUDE_KEYWORDS = [
    "about the", "welcome to", "forum feedback", "bug bounty",
    "exam content", "cheatsheet", "hackerone"
]

MIN_VIEWS_FOR_ANALYSIS = 10


@dataclass
class Topic:
    id: int
    title: str
    slug: str
    views: int
    reply_count: int
    posts_count: int
    has_accepted_answer: bool
    created_at: str
    last_posted_at: str
    tags: List[str]
    category_id: int
    excerpt: str = ""
    classification: str = "unclassified"
    unserved: bool = False


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


def classify_topic(topic: Topic) -> str:
    """Classify topic as 'error', 'non-error', or 'excluded' based on pre-declared rules."""
    text = (topic.title + " " + topic.excerpt).lower()

    # Check exclusion first
    for kw in EXCLUDE_KEYWORDS:
        if kw in text:
            return "excluded"

    # Check error keywords
    for kw in ERROR_KEYWORDS:
        if kw in text:
            return "error"

    # Check non-error keywords
    for kw in NON_ERROR_KEYWORDS:
        if kw in text:
            return "non-error"

    return "unclassified"


def is_unserved(topic: Topic) -> bool:
    """Determine if topic is unserved-open-like: no replies AND no accepted answer."""
    return topic.reply_count == 0 and not topic.has_accepted_answer


def mann_whitney_u(treatment: List[float], control: List[float]) -> Tuple[float, float]:
    """
    Mann-Whitney U test (two-sided).
    Returns (U statistic, p-value approximation using normal distribution).
    """
    n1 = len(treatment)
    n2 = len(control)

    if n1 == 0 or n2 == 0:
        return 0.0, 1.0

    # Combine and rank
    combined = [(v, 0) for v in treatment] + [(v, 1) for v in control]
    combined.sort(key=lambda x: x[0])

    # Assign ranks (average for ties)
    ranks = {}
    i = 0
    while i < len(combined):
        j = i
        while j < len(combined) and combined[j][0] == combined[i][0]:
            j += 1
        avg_rank = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranks[k] = avg_rank
        i = j

    # Sum ranks for treatment group
    r1 = sum(ranks[i] for i, (_, g) in enumerate(combined) if g == 0)

    # U statistic
    u1 = r1 - n1 * (n1 + 1) / 2
    u2 = n1 * n2 - u1
    u = min(u1, u2)

    # Normal approximation for p-value
    mean_u = n1 * n2 / 2
    std_u = (n1 * n2 * (n1 + n2 + 1) / 12) ** 0.5

    if std_u == 0:
        return u, 1.0

    z = (u - mean_u) / std_u
    # Two-tailed p-value using standard normal CDF approximation
    p = 2 * (1 - 0.5 * (1 + math_erf(abs(z) / 2**0.5)))
    return u, p


def math_erf(x: float) -> float:
    """Approximation of error function."""
    # Abramowitz and Stegun approximation
    a1 = 0.254829592
    a2 = -0.284496736
    a3 = 1.421413741
    a4 = -1.453152027
    a5 = 1.061405429
    p = 0.3275911

    sign = 1 if x >= 0 else -1
    x = abs(x)
    t = 1.0 / (1.0 + p * x)
    y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-x * x)
    return sign * y


def wilson_ci_lower(k: int, n: int, z: float = 1.96) -> float:
    """Wilson score interval lower bound."""
    if n == 0:
        return 0.0
    p = k / n
    denominator = 1 + z**2 / n
    centre = p + z**2 / (2 * n)
    half_width = z * (p * (1 - p) / n + z**2 / (4 * n**2))**0.5
    return (centre - half_width) / denominator


def wilson_ci_upper(k: int, n: int, z: float = 1.96) -> float:
    """Wilson score interval upper bound."""
    if n == 0:
        return 0.0
    p = k / n
    denominator = 1 + z**2 / n
    centre = p + z**2 / (2 * n)
    half_width = z * (p * (1 - p) / n + z**2 / (4 * n**2))**0.5
    return (centre + half_width) / denominator


def main():
    print("=" * 60)
    print("Experiment 094: Kubernetes Discourse View-Count Principle")
    print("=" * 60)

    all_topics = []
    classification_log = []

    # Fetch topics from category pages
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
                excerpt=t.get("excerpt", "")[:500],  # Use excerpt from category list
            )
            all_topics.append(topic)

        if len(all_topics) >= MAX_TOPICS:
            break

        # Rate limiting
        time.sleep(RATE_LIMIT_DELAY + random.uniform(0, 0.5))

    print(f"Fetched {len(all_topics)} topics total.")

    # Classify all topics using excerpts from category list
    print("Classifying topics...")
    for i, topic in enumerate(all_topics):
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

    # Filter out excluded and unclassified, and low-view topics
    error_topics = [t for t in all_topics if t.classification == "error" and t.views >= MIN_VIEWS_FOR_ANALYSIS]
    non_error_topics = [t for t in all_topics if t.classification == "non-error" and t.views >= MIN_VIEWS_FOR_ANALYSIS]
    excluded_topics = [t for t in all_topics if t.classification == "excluded"]
    unclassified_topics = [t for t in all_topics if t.classification == "unclassified"]

    print(f"\nClassification results:")
    print(f"  Error (treatment): {len(error_topics)}")
    print(f"  Non-error (control): {len(non_error_topics)}")
    print(f"  Excluded: {len(excluded_topics)}")
    print(f"  Unclassified: {len(unclassified_topics)}")

    # G1: Population gate
    g1_pass = len(error_topics) >= 100 and len(non_error_topics) >= 100
    print(f"\nG1 (Population ≥100 each): {'PASS' if g1_pass else 'FAIL'} (error={len(error_topics)}, non-error={len(non_error_topics)})")

    # G4: View-count coverage
    total_analyzed = len(error_topics) + len(non_error_topics)
    topics_with_views = sum(1 for t in error_topics + non_error_topics if t.views is not None and t.views >= 0)
    view_coverage = topics_with_views / total_analyzed if total_analyzed > 0 else 0
    g4_pass = view_coverage >= 0.95
    print(f"G4 (View-count coverage ≥95%): {'PASS' if g4_pass else 'FAIL'} ({view_coverage:.1%})")

    if total_analyzed == 0:
        print("No topics to analyze. Aborting.")
        return 1

    # View count statistics
    error_views = [t.views for t in error_topics]
    non_error_views = [t.views for t in non_error_topics]

    error_median = statistics.median(error_views) if error_views else 0
    non_error_median = statistics.median(non_error_views) if non_error_views else 0
    error_mean = statistics.mean(error_views) if error_views else 0
    non_error_mean = statistics.mean(non_error_views) if non_error_views else 0

    print(f"\nView count statistics:")
    print(f"  Error topics: n={len(error_views)}, median={error_median}, mean={error_mean:.1f}")
    print(f"  Non-error topics: n={len(non_error_views)}, median={non_error_median}, mean={non_error_mean:.1f}")

    # G2: Mann-Whitney U test
    u_stat, p_value = mann_whitney_u(error_views, non_error_views)
    g2_pass = p_value < 0.05 and error_median > non_error_median
    print(f"\nG2 (View-count separation, MWU p<0.05): {'PASS' if g2_pass else 'FAIL'}")
    print(f"  U={u_stat:.1f}, p={p_value:.6f}, error_median > non_error_median: {error_median > non_error_median}")

    # Unserved fraction analysis
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

    # G3: Unserved fraction bound (upper bound < 60%)
    g3_pass = error_ci_upper < 0.60
    print(f"\nG3 (Unserved CI95 upper < 60%): {'PASS' if g3_pass else 'FAIL'} (upper={error_ci_upper:.3f})")

    # Overall result
    all_gates_pass = g1_pass and g2_pass and g3_pass and g4_pass
    print(f"\n{'=' * 60}")
    print(f"OVERALL: {'ALL GATES PASS' if all_gates_pass else 'SOME GATES FAIL'}")
    print(f"{'=' * 60}")

    # Prepare results
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

    # Write results
    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)

    with open("classification.log.json", "w") as f:
        json.dump(classification_log, f, indent=2)

    print("\nResults written to results.json and classification.log.json")
    return 0 if all_gates_pass else 1


if __name__ == "__main__":
    sys.exit(main())