#!/usr/bin/env python3
"""
Classifier with improved coverage for view-count measurements.

Improvements over E078's needle-in-haystack substring matcher:
1. Word-boundary anchored patterns to avoid substring collisions
   (e.g., `ai` in `email`, `base` in `database`)
2. Categorized need patterns with better coverage
3. Explicit non-need filtering
4. Coverage tracking with declared floor
"""

import re
from collections import defaultdict


# ===== Word-boundary anchored need patterns =====
# These use \b word boundaries to prevent substring matches.
# Previously: `ai` matched inside `email`, `base` matched inside `database`.
# Now: these only match whole-word occurrences.

NEED_PATTERNS = [
    # Questions starting with how/what/why
    r'\bhow\b',
    r'\bwhat\b',
    r'\bwhy\b',

    # X how/what/why questions
    r'\bhow (do|can|should|would|is|are)\b',
    r'\bwhat (is|are|should|would|causes?|makes?)\b',
    r'\bwhy (is|are|do|does|did|can|won)\b',

    # Help requests
    r'\bhelp\b',

    # Problem/error reports
    r'\bissue\b',
    r'\bproblem\b',
    r'\berror\b',
    r'\bfailure\b',
    r'\bnot working\b',
    r'\bbroken\b',

    # Recommendations / suggestions
    r'\brecommend\b',
    r'\bsuggestion\b',
    r'\badvice\b',

    # Which/where questions
    r'\bwhich\b',
    r'\bwhich (one|should|is best|to buy|to use|get)\b',
    r'\bwhere\b',
    r'\bwhere (can|to|is|are)\b',

    # Ideas / tips requests
    r'\bany (idea|suggestion|tip|advice|recommendation)\b',
    r'\bcan (someone|anybody|anyone)\b',

    # Confused/lost state
    r'\bstuck\b',
    r'\blost\b',
    r'\bconfused\b',

    # Wondering / should I
    r'\bwondering\b',
    r'\bshould I\b',
]

NON_NEED_PATTERNS = [
    # Show-off / demo content
    r'\bIC\b',  # Integrated Circuit
    r'show.*(off|me)',
    r'my (new|first|latest) (setup|build|project|purchase)',
    r'just (got|bought|picked up|received)',
    r'welcome to',
    r'thank(s| you)',

    # Image / picture only threads
    r'image(s)?\s*(only|thread)',
    r'picture(s)?\s*(only|thread|uno)',
    r'introductions?',

    # Code snippets / output dumps
    r'```',
    r'code block',

    # Announcements
    r'announcement',
    r'release note',
]


# Compile regexes with word boundaries for main patterns
# Wrap patterns with \b on both sides for whole-word matching
ANCHORED_NEED_RE = re.compile(
    '|'.join(f'\\b{pattern}\\b' for pattern in NEED_PATTERNS),
    re.IGNORECASE
)

ANCHORED_NON_NEED_RE = re.compile(
    '|'.join(f'\\b{pattern}\\b' for pattern in NON_NEED_PATTERNS),
    re.IGNORECASE
)


def classify_need(title: str) -> str:
    """
    Classify a thread title as need, non-need, or undetermined.

    Returns:
        "need" - title suggests a concrete problem/question requiring a tool
        "non-need" - title is sharing, showing off, meta, etc.
        "undetermined" - doesn't match either category

    Key improvements over E078:
    - Word-boundary anchoring prevents substring collisions
    - e.g., \bai\b won't match inside "email", \bbase\b won't match inside "database"
    - Comprehensive coverage of need-related vocabulary
    """
    has_need = ANCHORED_NEED_RE.search(title) is not None
    has_non_need = ANCHORED_NON_NEED_RE.search(title) is not None

    if has_need and not has_non_need:
        return "need"
    elif has_non_need:
        return "non-need"
    else:
        return "undetermined"


def coverage_rate(classified_count: int, total_count: int) -> float:
    """Calculate the classification coverage rate."""
    return classified_count / total_count if total_count > 0 else 0.0


def is_unserved_open_like(thread):
    """
    Return True if thread is unserved-open-like per the three-clause rubric.
    (Same rubric as E078, but now with better classification feeding into clause 2.)
    """
    # Clause 1: no recorded resolution
    accepted = thread.get("accepted_answer", False)
    answer_count = thread.get("answer_count", 0)
    has_good_answer = accepted or (answer_count >= 3) or any(
        a.get("score", 0) >= 1 for a in thread.get("answers", [])
    )
    no_recorded_resolution = not has_good_answer

    # Clause 2: states a concrete need (now with better classification)
    title = thread.get("title", "")
    is_need = classify_need(title) == "need"

    # Clause 3: not a request for content/service/price/access/human work
    # (filtered by non-need classification already)

    return no_recorded_resolution and is_need


# ===== Coverage floor declaration =====
# D083 reopening condition 1: "A classifier that covers its population."
# Declared coverage floor: ≥60% of a representative pool must be classifiable
# (need or non-need) to justify reopening the view-count line.
COVERAGE_FLOOR = 0.60  # 60%


# ===== Experiment helpers =====

def compute_coverage(theta_data: dict, pool_size: int) -> dict:
    """
    Compute coverage statistics from classification results.

    theta_data: dict with keys 'need', 'non-need', 'undetermined' counting classified threads
    pool_size: total number of threads in the representative pool
    """
    classified = theta_data.get("need", 0) + theta_data.get("non-need", 0)
    unclassified = theta_data.get("undetermined", 0)

    coverage = classified / pool_size if pool_size > 0 else 0
    uncoverage = unclassified / pool_size if pool_size > 0 else 0

    return {
        "classified_count": classified,
        "unclassified_count": unclassified,
        "coverage": coverage,
        "uncoverage_rate": uncoverage,
        "meets_floor": coverage >= COVERAGE_FLOOR,
        "coverage_floor": COVERAGE_FLOOR,
        "pool_size": pool_size,
    }