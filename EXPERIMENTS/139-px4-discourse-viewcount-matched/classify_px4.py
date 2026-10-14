#!/usr/bin/env python3
"""classify_px4.py - Classify PX4 Discourse topics as need-related or random"""

import json
import re
import sys
import os


# Need patterns for developer forums (anchored word-boundary where applicable)
NEED_PATTERNS = [
    # Standard Q&A
    r"\bhow to\b", r"\bhow do i\b", r"\bhow can i\b", r"\bwhy does\b", r"\bwhat is\b", r"\bhow does\b",
    # Task verbs
    r"\brun\b", r"\bcreate\b", r"\bset up\b", r"\bconfigure\b", r"\bdeploy\b", r"\bdebug\b", r"\bfix\b", r"\btroubleshoot\b",
    # Problem statements
    r"\berror\b", r"\bfail\b", r"\bnot working\b", r"\bcannot\b", r"\bissue\b", r"\bproblem\b", r"\bstuck\b", r"\bhelp\b",
    # Evidence-seeking
    r"\btrouble \w+ing\b", r"problem with", r"issue with", r"difficulty \w+ing",
    # Error messages as titles (common patterns)
    r".*object has no attribute .*", r"context deadline exceeded",
    # Noun-phrase questions ending with ?
    r"[A-Z][a-z]+\s+[A-Z][a-z]+\?",
    # X not working / failing / broken
    r"\b\w+\s+not\s+working\b", r"\b\w+\s+failing\b", r"\b\w+\s+broken\b",
    # X isn't working
    r"\b\w+'?n't\s+working\b",
    # Something up with / weird behavior
    r"something up with", r"weird behavior", r"strange behavior",
    # PX4-specific terms
    r"\bpx4\b", r"\bpixhawk\b", r"\bautopilot\b", r"\bflight\b", r"\bfirmware\b",
    r"\bmission\b", r"\bparameter\b", r"\bcalibration\b", r"\bpreflight\b",
]


EXCLUSION_PATTERNS = [
    r"\bblog\b", r"\bcase study\b", r"\banniversary\b", r"\bcelebrating\b",
    r"\bearly review\b", r"\bgives back\b", r"\bgetting started\b", r"\bwalkthrough\b",
    r"\bhow .+ (increased|improved|bolsters|monetiz)\b", r"\bhiring\b", r"\bjob\b",
    r"\bcareer\b", r"\bfreelance\b", r"\bcontract\b", r"\$\d+", r"\bann\b",
    r"\bmeta\b", r"\bmoderator\b", r"\brules\b", r"\bFAQ\b", r"\bwiki\b",
    r"\bshowcase\b", r"\bportfolio\b", r"\bproject\b", r"\bcreated\b", r"\bmade\b",
    r"\bdemo\b", r"\btutorial\b", r"\bguide\b", r"\bexample\b", r"\blearning\b",
    r"\bpractice\b", r"\bexercise\b", r"\bmeme\b", r"\bjoke\b", r"\bfun\b",
    r"\boff topic\b", r"\brandom\b",
]


def is_need_related(title, body=""):
    """Classify a topic as need-related if it matches need patterns and no exclusion patterns."""
    text = (title + " " + body).lower()

    # Check exclusion patterns first
    for pattern in EXCLUSION_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return "random"

    # Check need patterns
    for pattern in NEED_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return "need-related"

    return "random"


def classify_topic(topic):
    """Classify a single topic dict."""
    title = topic.get("title", "")
    body = topic.get("body", "")  # Discourse API may not always include body
    return is_need_related(title, body)


def classify_topics(input_path, output_path):
    """Classify all topics from the harvest results."""
    with open(input_path, "r") as f:
        data = json.load(f)

    topics = data.get("topics", [])
    results = []

    for topic in topics:
        classification = classify_topic(topic)
        results.append({
            "id": topic.get("id"),
            "title": topic.get("title"),
            "view_count": topic.get("view_count"),
            "reply_count": topic.get("reply_count"),
            "classification": classification,
        })

    # Save classified results
    with open(output_path, "w") as f:
        json.dump({"topics": results, "total": len(results)}, f, indent=2)

    # Count classifications
    counts = {"need-related": 0, "random": 0}
    for r in results:
        counts[r["classification"]] += 1

    coverage = round(counts["need-related"] / len(results) * 100, 1) if results else 0
    print("Classifications: {}".format(counts))
    print("Coverage: {}%".format(coverage))

    return 0


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Path to harvest results JSON (results_raw.json)")
    parser.add_argument("output", help="Path to save classified results")
    args = parser.parse_args()
    sys.exit(classify_topics(args.input, args.output))


if __name__ == "__main__":
    main()