#!/usr/bin/env python3
"""
E077 — Classification and measurement helpers for Discourse forums.
"""

import json
import math
import re
import time
import urllib.request
from typing import Any, Dict, List, Optional


# Keyword patterns from E074/E076 classification
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

TOPICS_PER_FORUM = 50
SLEEP_BETWEEN_REQUESTS = 1.0  # seconds, polite polling


def fetch_latest_page(domain: str, page: int) -> Optional[Dict]:
    """Fetch a page of topics from a Discourse forum."""
    url = f"https://{domain}/latest.json?page={page}&per_page=30"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Think Free E077)"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        if e.code == 429:
            print(f"    Rate limited on {domain} page {page}, waiting 30 seconds...")
            time.sleep(30)
            return fetch_latest_page(domain, page)
        print(f"    Error fetching {url}: {e}")
        return None
    except Exception as e:
        print(f"    Error fetching {url}: {e}")
        return None


def harvest_forum_topics(domain: str, max_topics: int = TOPICS_PER_FORUM) -> List[Dict]:
    """Harvest topics from a Discourse forum across multiple pages."""
    all_topics: List[Dict] = []

    for page in range(1, 10):  # Safety limit
        data = fetch_latest_page(domain, page)
        if data is None:
            break

        page_topics = data.get("topic_list", {}).get("topics", [])
        if not page_topics:
            break

        all_topics.extend(page_topics)

        if len(all_topics) >= max_topics:
            break

        time.sleep(SLEEP_BETWEEN_REQUESTS)

    # Deduplicate by topic id
    seen_ids: set = set()
    deduped: List[Dict] = []
    for t in all_topics:
        tid = t.get("id", 0)
        if tid not in seen_ids:
            seen_ids.add(tid)
            deduped.append(t)
        if len(deduped) >= max_topics:
            break

    # Convert to our standardized topic dict format
    topics: List[Dict] = []
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
    """Apply the three-clause rubric for unserved-open-like.

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


def wilson_ci95(k: int, n: int) -> tuple:
    """Wilson score interval 95%."""
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    z = 1.96
    denom = 1 + z**2 / n
    centre = (p + z**2 / (2 * n)) / denom
    half = (z / denom) * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2))
    return (centre - half, centre + half)


def classify_topics(topics: List[Dict]) -> List[Dict]:
    """Classify each topic using the rubric."""
    results: List[Dict] = []
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


def save_raw_data(domain: str, topics: List[Dict], classified: List[Dict], output_dir: str):
    """Save raw topic data and classified data to JSONL files."""
    import os
    os.makedirs(output_dir, exist_ok=True)

    # Sanitize domain for filename
    safe_domain = domain.replace(".", "_")

    # Save raw topics
    with open(os.path.join(output_dir, f"topics_{safe_domain}.jsonl"), "w") as f:
        for t in topics:
            f.write(json.dumps(t) + "\n")

    # Save classified topics
    with open(os.path.join(output_dir, f"classified_{safe_domain}.jsonl"), "w") as f:
        for t in classified:
            f.write(json.dumps(t) + "\n")


def measure_forum(topics: List[Dict], domain: str) -> Dict:
    """Full measurement pipeline for a single forum's topics."""
    total = len(topics)

    if total == 0:
        return {
            "domain": domain,
            "total": 0,
            "view_positive": 0,
            "need_topics": 0,
            "unserved_open_like": 0,
            "unserved_fraction": 0.0,
            "wilson_ci95": [0.0, 0.0],
            "view_counts": [],
        }

    # Classify
    classified = classify_topics(topics)

    # Count
    view_positive = sum(1 for t in classified if t.get("views", 0) > 0)
    need_topics = sum(1 for t in classified if t["is_need"])
    unserved_open_like = sum(1 for t in classified if t["is_unserved_open_like"])

    # Wilson CI95
    ci_low, ci_high = wilson_ci95(unserved_open_like, total)

    # View count distribution
    view_counts = [t.get("views", 0) for t in classified]

    print(f"  Total: {total}")
    print(f"  view_count > 0: {view_positive} ({view_positive/total*100:.1f}%)")
    print(f"  Need topics: {need_topics} ({need_topics/total*100:.1f}%)")
    print(f"  Unserved-open-like: {unserved_open_like} ({unserved_open_like/total*100:.2f}%)")
    print(f"  Wilson CI95: [{ci_low*100:.2f}%, {ci_high*100:.2f}%]")

    return {
        "domain": domain,
        "total": total,
        "view_positive": view_positive,
        "need_topics": need_topics,
        "unserved_open_like": unserved_open_like,
        "unserved_fraction": unserved_open_like / total if total > 0 else 0.0,
        "wilson_ci95": [ci_low, ci_high],
        "view_counts": view_counts,
    }


def aggregate_results(all_results: List[Dict]) -> Dict:
    """Aggregate results across all forums."""
    total_all = sum(r["total"] for r in all_results if "error" not in r)
    view_positive_all = sum(r["view_positive"] for r in all_results if "error" not in r)
    need_topics_all = sum(r["need_topics"] for r in all_results if "error" not in r)
    unserved_all = sum(r["unserved_open_like"] for r in all_results if "error" not in r)

    ci_low, ci_high = wilson_ci95(unserved_all, total_all)

    print(f"\n=== AGGREGATE RESULTS ===")
    print(f"Total topics: {total_all}")
    if total_all > 0:
        print(f"view_count > 0: {view_positive_all} ({view_positive_all/total_all*100:.1f}%)")
        print(f"Need topics: {need_topics_all} ({need_topics_all/total_all*100:.1f}%)")
        print(f"Unserved-open-like: {unserved_all} ({unserved_all/total_all*100:.2f}%)")
        print(f"Wilson CI95: [{ci_low*100:.2f}%, {ci_high*100:.2f}%]")
    else:
        print("No data collected")

    # Gate assessments
    print(f"\n=== GATE ASSESSMENTS ===")

    # G1: view_count validation
    vc_rate = view_positive_all / total_all if total_all > 0 else 0
    g1_pass = vc_rate >= 0.95
    print(f"G1 (view_count >= 95%): {'PASS' if g1_pass else 'FAIL'} — {vc_rate*100:.1f}%")

    # G2: need prevalence
    need_rate = need_topics_all / total_all if total_all > 0 else 0
    g2_pass = need_rate >= 0.05
    print(f"G2 (need prevalence >= 5%): {'PASS' if g2_pass else 'FAIL'} — {need_rate*100:.1f}%")

    # G3: unserved fraction measurable
    unserved_rate = unserved_all / total_all if total_all > 0 else 0
    g3_pass = unserved_rate < 0.50 and ci_high < 0.60
    print(f"G3 (unserved < 50%, CI95 upper < 60%): {'PASS' if g3_pass else 'FAIL'} — {unserved_rate*100:.1f}%, CI95=[{ci_low*100:.1f}%, {ci_high*100:.1f}%]")

    # G4: cross-forum variance
    forums_with_unserved = sum(1 for r in all_results if "error" not in r and r["unserved_open_like"] > 0)
    g4_pass = forums_with_unserved >= 3
    print(f"G4 (>= 3 forums with unserved > 0): {'PASS' if g4_pass else 'FAIL'} — {forums_with_unserved} forums")

    all_gates_pass = g1_pass and g2_pass and g3_pass and g4_pass
    print(f"\nALL GATES: {'PASS' if all_gates_pass else 'FAIL'}")

    return {
        "total": total_all,
        "view_positive": view_positive_all,
        "need_topics": need_topics_all,
        "unserved_open_like": unserved_all,
        "unserved_fraction": unserved_rate,
        "wilson_ci95": [ci_low, ci_high],
        "gates": {
            "G1_view_count": {"pass": g1_pass, "value": vc_rate},
            "G2_need_prevalence": {"pass": g2_pass, "value": need_rate},
            "G3_unserved_fraction": {"pass": g3_pass, "value": unserved_rate, "ci95": [ci_low, ci_high]},
            "G4_cross_forum_variance": {"pass": g4_pass, "forums_with_unserved": forums_with_unserved},
        },
        "all_gates_pass": all_gates_pass,
    }