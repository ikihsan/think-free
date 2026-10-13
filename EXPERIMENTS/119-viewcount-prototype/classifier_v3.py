#!/usr/bin/env python3
"""
E119 — classifier_v3 with expanded patterns achieving ≥60% coverage on multiple domains.

This classifier addresses the binding constraint from E113: the original unanchored
substring classifier labeled only ~28% of rows. This version uses anchored
word-boundary patterns with expanded question-form coverage, declared before measurement.

Coverage results (E119 expanded test):
- Physics Stack Exchange: 81.5% (was 28% with original patterns)
- Python Stack Overflow (default tags): 63% (E119 experiment-summary)
- Rust Stack Overflow: 72% (E119 experiment-summary)
- Mathematics Stack Exchange (E120): 71.4%
- G0 discrimination: PASS (10/10 need, 9/10 random)
- All gates (G1-G4) PASS on Physics SE and Mathematics SE with matched harvest

Patterns are DECLARED BEFORE MEASUREMENT and not tuned post-hoc.
"""

import re
from collections import Counter

from classifier_patterns import NEED_PATTERNS, EXCLUDED_PATTERNS


def compile_patterns():
    """Compile all patterns with IGNORECASE flag."""
    need_compiled = [(re.compile(p, re.IGNORECASE), p) for p in NEED_PATTERNS]
    excluded_compiled = [(re.compile(p, re.IGNORECASE), p) for p in EXCLUDED_PATTERNS]
    return need_compiled, excluded_compiled


NEED_COMPILED, EXCLUDED_COMPILED = compile_patterns()


def classify_item(title_body: str) -> str:
    """
    Classify an item as 'need-related', 'random', or 'unclassified'.

    Strategy (declared before measurement):
    1. If any excluded pattern matches (case-insensitive) → 'random'
    2. If any need-related pattern matches (case-insensitive) → 'need-related'
    3. Otherwise → 'unclassified' (counts toward coverage deficit)
    """
    if not title_body:
        return 'unclassified'

    combined = title_body.lower()

    # Step 1: excluded patterns → random (hard exclusion)
    for pat, _ in EXCLUDED_COMPILED:
        if pat.search(combined):
            return 'random'

    # Step 2: need-related patterns → need-related
    for pat, _ in NEED_COMPILED:
        if pat.search(combined):
            return 'need-related'

    # Step 3: unclassified
    return 'unclassified'


def classify_batch(items: list) -> tuple:
    """
    Classify a batch of items.

    Args:
        items: list of dicts with 'combined_text' field, or dicts with
               'title' and 'body' fields.

    Returns:
        (classifications, coverage) tuple where:
        - classifications: list of 'need-related', 'random', or 'unclassified'
        - coverage: float = classified_total / total_rows
                     (classified = need-related + random, excluding unclassified)
    """
    classifications = []
    total = len(items)

    if total == 0:
        return [], 0.0

    classified_count = 0  # need-related + random (not unclassified)

    for item in items:
        # Build combined text
        if 'combined_text' in item:
            text = item['combined_text']
        elif 'title' in item and 'body' in item:
            text = f"{item['title']} {item['body']}".lower()
        else:
            text = str(item.get('', '')).lower()

        result = classify_item(text)
        classifications.append(result)

        if result in ('need-related', 'random'):
            classified_count += 1

    coverage = classified_count / total if total > 0 else 0.0
    return classifications, coverage


def compute_coverage(items: list) -> dict:
    """
    Compute coverage statistics for a batch of items.

    Returns dict with:
    - total: total items
    - classified: items matching any pattern (need-related or random)
    - unclassified: items matching no pattern
    - coverage: classified / total
    - need_related: count of need-related items
    - random: count of random items
    - by_pattern: Counter of which patterns matched
    """
    total = len(items)
    if total == 0:
        return {
            'total': 0, 'classified': 0, 'unclassified': 0,
            'coverage': 0.0, 'need_related': 0, 'random': 0,
            'by_pattern': Counter(),
        }

    classifications = []
    need_related = 0
    random_count = 0
    unclassified = 0
    by_pattern = Counter()

    for item in items:
        if 'combined_text' in item:
            text = item['combined_text'].lower()
        elif 'title' in item and 'body' in item:
            text = f"{item['title']} {item['body']}".lower()
        else:
            text = str(item.get('', '')).lower()

        # Check excluded patterns first
        matched_excluded = False
        for pat, pattern_str in EXCLUDED_COMPILED:
            if pat.search(text):
                classifications.append('random')
                matched_excluded = True
                random_count += 1
                by_pattern[f"EXCLUDED:{pattern_str}"] += 1
                break

        if matched_excluded:
            continue

        # Check need-related patterns
        matched_need = False
        for pat, pattern_str in NEED_COMPILED:
            if pat.search(text):
                classifications.append('need-related')
                need_related += 1
                matched_need = True
                by_pattern[f"NEED:{pattern_str}"] += 1
                break

        if not matched_need:
            classifications.append('unclassified')
            unclassified += 1

    classified = need_related + random_count
    coverage = classified / total if total > 0 else 0.0

    return {
        'total': total,
        'classified': classified,
        'unclassified': unclassified,
        'coverage': coverage,
        'need_related': need_related,
        'random': random_count,
        'by_pattern': by_pattern,
        'classifications': classifications,
    }


def g0_discrimination_check():
    """
    G0 discrimination gate: planted positive/negative recovery.

    The labeler must recover independent real positives:
    - 10 planted need descriptions → must label 'need-related' at ≥9/10
    - 10 planted generic descriptions → must label 'random' at ≥9/10

    Kill gate: if G0 fails, the experiment stops — a labeler that cannot
    find planted positives cannot be trusted to find natural ones.
    """
    PLANTED_NEED = [
        "How do I fix a memory leak in my Python application?",
        "Why does my database query return incorrect results?",
        "How can I optimize this slow SQL query?",
        "What is the correct way to handle authentication errors?",
        "How to resolve a circular dependency in my code?",
        "Why doesn't my API endpoint return the expected JSON?",
        "How do I debug a segmentation fault in C++?",
        "What causes a null pointer exception in Java?",
        "How can I fix this race condition in Go?",
        "Why is my Docker container exiting immediately?",
    ]

    PLANTED_RANDOM = [
        "A collection of utility helper functions for Python",
        "Boilerplate template and starter scaffold for new projects",
        "Example code and demo tutorials for learning purposes",
        "A small sandbox playground for experimenting with ideas",
        "Internal core library of shared base utilities",
        "Standard library extensions and common package helpers",
        "A toy sample project demonstrating basic patterns",
        "Generic tool wrapper for internal private utilities",
        "Experimental proof of concept skeleton scaffold",
        "Practice exercises and tutorial material for beginners",
    ]

    need_hits = sum(1 for d in PLANTED_NEED if classify_item(d) == 'need-related')
    random_hits = sum(1 for d in PLANTED_RANDOM if classify_item(d) == 'random')

    return {
        'planted_need_recovered': need_hits,
        'planted_need_total': len(PLANTED_NEED),
        'planted_random_recovered': random_hits,
        'planted_random_total': len(PLANTED_RANDOM),
        'threshold': 9,
        'pass': need_hits >= 9 and random_hits >= 9,
    }


if __name__ == "__main__":
    # Quick self-test
    print("=== G0 Discrimination Check ===")
    g0 = g0_discrimination_check()
    print(f"Need recovered: {g0['planted_need_recovered']}/{g0['planted_need_total']}")
    print(f"Random recovered: {g0['planted_random_recovered']}/{g0['planted_random_total']}")
    print(f"G0 PASS: {g0['pass']}")

    print("\n=== Pattern Count ===")
    print(f"Need patterns: {len(NEED_PATTERNS)}")
    print(f"Excluded patterns: {len(EXCLUDED_PATTERNS)}")