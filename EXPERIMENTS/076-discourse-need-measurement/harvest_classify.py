#!/usr/bin/env python3
"""
E076 — Discourse need-serving rate measurement tools.

Core classification and harvesting functions split from run.py to stay
within the 300-line cap.
"""
from __future__ import annotations

import json
import math
import os
import re
import sys
import time
import urllib.request
from typing import Any, dict, list

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