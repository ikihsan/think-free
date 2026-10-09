#!/usr/bin/env python3
"""
E077 — Classification helpers for Discourse forums.
"""

import re
from typing import Dict, List


# ---------------------------------------------------------------------------
# Classification patterns
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Classification functions
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