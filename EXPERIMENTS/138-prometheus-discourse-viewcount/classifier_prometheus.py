#!/usr/bin/env python3
"""
Developer-forum-specific classifier for Prometheus Discourse.
Addresses coverage boundary from E124 (GNOME 37.2%) and E125 (Jupyter 50.4%).
"""

import re
import json

# Need patterns (match any to classify as need-related)
NEED_PATTERNS = [
    # Standard Q&A forms
    (r"\bhow to\b", "how_to"),
    (r"\bhow do i\b", "how_do_i"),
    (r"\bhow can i\b", "how_can_i"),
    (r"\bwhy does\b", "why_does"),
    (r"\bwhat is\b", "what_is"),
    (r"\bhow does\b", "how_does"),
    (r"\bhow would\b", "how_would"),
    (r"\bhow will\b", "how_will"),
    (r"\bhow could\b", "how_could"),
    (r"\bcan you\b", "can_you"),
    (r"\bcould you\b", "could_you"),
    (r"\bwould you\b", "would_you"),
    (r"\bcan anyone\b", "can_anyone"),
    (r"\bcould anyone\b", "could_anyone"),
    (r"\bwould anyone\b", "would_anyone"),
    (r"\bdoes anyone\b", "does_anyone"),
    (r"\bdo you\b", "do_you"),
    (r"\bis there\b", "is_there"),
    (r"\bare there\b", "are_there"),

    # Task verbs
    (r"\brun\b", "run"),
    (r"\bcreate\b", "create"),
    (r"\bset up\b", "set_up"),
    (r"\bconfigure\b", "configure"),
    (r"\bdeploy\b", "deploy"),
    (r"\bdebug\b", "debug"),
    (r"\bfix\b", "fix"),
    (r"\btroubleshoot\b", "troubleshoot"),

    # Problem statements
    (r"\berror\b", "error"),
    (r"\bfail\b", "fail"),
    (r"\bnot working\b", "not_working"),
    (r"\bcannot\b", "cannot"),
    (r"\bissue\b", "issue"),
    (r"\bproblem\b", "problem"),
    (r"\bstuck\b", "stuck"),
    (r"\bhelp\b", "help"),

    # Evidence-seeking patterns (developer forum styles)
    (r"\btrouble \w+ing\b", "trouble_verbing"),
    (r"\bproblem with\b", "problem_with"),
    (r"\bissue with\b", "issue_with"),
    (r"\bdifficulty \w+ing\b", "difficulty_verbing"),

    # Error messages as titles (CamelCase + common error phrases)
    (r"[A-Z][a-zA-Z]+(?:[A-Z][a-zA-Z]+)*\s+(?:not found|no attribute|timeout|refused|denied|failed|error|exception)", "error_message_title"),
    (r"'(?:[A-Z][a-zA-Z]+)' object has no attribute '(?:[a-zA-Z_]+)'", "python_attribute_error"),
    (r"context deadline exceeded", "context_deadline"),
    (r"connection refused", "connection_refused"),
    (r"permission denied", "permission_denied"),
    (r"no such file", "no_such_file"),

    # Noun-phrase questions ending with ?
    (r"^[A-Z][a-z]+(?: [A-Z][a-z]+)+\?$", "noun_phrase_question"),

    # X not working / failing / broken patterns
    (r"\b\w+\s+(?:not working|failing|broken|isn't working|doesn't work)\b", "x_not_working"),

    # Something up with / weird behavior
    (r"\bsomething up with\b", "something_up_with"),
    (r"\bweird behavior\b", "weird_behavior"),
    (r"\bstrange behavior\b", "strange_behavior"),

    # Prometheus-specific terms (in title or body)
    (r"\bpromql\b", "promql"),
    (r"\balertmanager\b", "alertmanager"),
    (r"\bscrape\b", "scrape"),
    (r"\brelabel\b", "relabel"),
    (r"\brule\b", "rule"),
    (r"\brecording\b", "recording"),
    (r"\bremote write\b", "remote_write"),
    (r"\bremote read\b", "remote_read"),
    (r"\bthanos\b", "thanos"),
    (r"\bcortex\b", "cortex"),
    (r"\bvictoriametrics\b", "victoriametrics"),
    (r"\bexporter\b", "exporter"),
    (r"\bservicediscovery\b|\bservice discovery\b", "service_discovery"),
    (r"\btsdb\b", "tsdb"),
    (r"\bwal\b", "wal"),
    (r"\bcompaction\b", "compaction"),
    (r"\bretention\b", "retention"),
]

# Exclusion patterns (hard exclusion - if any matches, classify as random)
EXCLUSION_PATTERNS = [
    # Blog/announcement content (E123 finding)
    (r"\bblog\b", "blog"),
    (r"\bcase study\b", "case_study"),
    (r" blog$", "blog_suffix"),
    (r"\banniversary\b", "anniversary"),
    (r"\bcelebrating\b", "celebrating"),
    (r"\byearly review\b", "yearly_review"),
    (r"\bgives back\b", "gives_back"),
    (r"\bedition\b", "edition"),
    (r"\bgetting started\b", "getting_started"),
    (r"\bwalkthrough\b", "walkthrough"),
    (r"\bpart \d+\b", "part_n"),
    (r"\bhow .+ (?:increased|improved|bolsters|monetiz)\b", "marketing_content"),

    # Job postings (E125 contamination)
    (r"\bhiring\b", "hiring"),
    (r"\bjob\b", "job"),
    (r"\bcareer\b", "career"),
    (r"\bfreelance\b", "freelance"),
    (r"\bcontract\b", "contract"),
    (r"\$\d+", "money_amount"),

    # Announcements
    (r"\bann\b", "ann"),
    (r"\[ann\]", "ann_brackets"),
    (r"\[ANN\]", "ANN_brackets"),

    # Meta posts
    (r"\bmeta\b", "meta"),
    (r"\bmoderator\b", "moderator"),
    (r"\bmod post\b", "mod_post"),
    (r"\brules\b", "rules"),
    (r"\bFAQ\b", "faq"),
    (r"\bwiki\b", "wiki"),
    (r"\bguideline\b", "guideline"),
    (r"\bcontributing\b", "contributing"),

    # Showcase/learning
    (r"\bshowcase\b", "showcase"),
    (r"\bportfolio\b", "portfolio"),
    (r"\bproject\b", "project"),
    (r"\bcreated\b", "created"),
    (r"\bmade\b", "made"),
    (r"\bdemo\b", "demo"),
    (r"\bexample\b", "example"),
    (r"\btutorial\b", "tutorial"),
    (r"\bguide\b", "guide"),
    (r"\blearning\b", "learning"),
    (r"\bpractice\b", "practice"),
    (r"\bexercise\b", "exercise"),

    # Off-topic
    (r"\bmeme\b", "meme"),
    (r"\bjoke\b", "joke"),
    (r"\bfun\b", "fun"),
    (r"\boff topic\b", "off_topic"),
    (r"\bwatercooler\b", "watercooler"),
    (r"\brandom\b", "random"),
]

# Compile all patterns
NEED_REGEX = [(re.compile(p, re.IGNORECASE), name) for p, name in NEED_PATTERNS]
EXCLUSION_REGEX = [(re.compile(p, re.IGNORECASE), name) for p, name in EXCLUSION_PATTERNS]


def classify_title(title):
    """Classify a topic title. Returns (classification, matched_pattern_names)."""
    if not title:
        return "random", []

    # Check exclusions first
    excluded_matches = []
    for regex, name in EXCLUSION_REGEX:
        if regex.search(title):
            excluded_matches.append(name)

    if excluded_matches:
        return "excluded", excluded_matches

    # Check need patterns
    need_matches = []
    for regex, name in NEED_REGEX:
        if regex.search(title):
            need_matches.append(name)

    if need_matches:
        return "need", need_matches

    return "random", []


def classify_topic(title, body=""):
    """Classify a topic by title (primary) and body (secondary)."""
    # Primary: title classification
    cls, matches = classify_title(title)
    if cls != "random":
        return cls, matches

    # Secondary: body classification (first 500 chars)
    if body:
        cls, matches = classify_title(body[:500])
        if cls != "random":
            return cls, matches

    return "random", []


def load_topics(jsonl_path):
    """Load topics from JSONL file."""
    topics = []
    with open(jsonl_path, "r") as f:
        for line in f:
            topics.append(json.loads(line))
    return topics


def classify_topics(topics):
    """Add classification to each topic."""
    for topic in topics:
        title = topic.get("title", "")
        body = topic.get("raw", "") or topic.get("excerpt", "") or ""
        cls, matches = classify_topic(title, body)
        topic["classification"] = cls
        topic["matched_patterns"] = matches
    return topics


def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 classifier_prometheus.py <input.jsonl> [output.jsonl]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else input_path.replace(".jsonl", "_classified.jsonl")

    topics = load_topics(input_path)
    classified = classify_topics(topics)

    with open(output_path, "w") as f:
        for topic in classified:
            f.write(json.dumps(topic) + "\n")

    # Print summary
    counts = {"need": 0, "random": 0, "excluded": 0}
    for t in classified:
        counts[t["classification"]] += 1

    total = len(classified)
    coverage = (counts["need"] + counts["random"]) / total if total > 0 else 0
    need_frac = counts["need"] / (counts["need"] + counts["random"]) if (counts["need"] + counts["random"]) > 0 else 0

    print(f"Total: {total}")
    print(f"Need: {counts['need']} ({counts['need']/total*100:.1f}%)")
    print(f"Random: {counts['random']} ({counts['random']/total*100:.1f}%)")
    print(f"Excluded: {counts['excluded']} ({counts['excluded']/total*100:.1f}%)")
    print(f"Coverage: {coverage*100:.1f}% (floor: 60%)")
    print(f"Need fraction: {need_frac*100:.1f}% (floor: 5%)")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()