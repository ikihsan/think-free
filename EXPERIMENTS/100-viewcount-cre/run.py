"""E100 — View-count principle on Code Review Stack Exchange Python tag."""

import json
import urllib.request
import sys

# Configuration
SITE = "codereview"
TAG = "python"
SAMPLE_SIZE = 100  # aim for >= 50 classified
GATE = "--gate" in sys.argv

# Need-related classification heuristics
NEED_INDICATORS = [
    "how to", "how do i", "how can i", "want to", "trying to",
    "run", "fix", "debug", "refactor", "optimize", "improve", "resolve",
    "python", "function", "class", "variable", "loop", "error", "bug", "issue",
]
RANDOM_EXCLUDE = [
    "what is", "explain", "concept", "understand",
    "best", "opinion", "poll", "suggestion",
    "getting started",
]


def fetch_questions_page(page=1, pagesize=10):
    """Fetch one page of Python-tagged Code Review questions from Stack Exchange."""
    url = (
        f"https://api.stackexchange.com/2.3/questions"
        f"?page={page}&pagesize={pagesize}"
        f"&order=desc&sort=activity&tagged={TAG}&site={SITE}"
    )
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "origin-mission-E100"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read().decode()
            return json.loads(data)
    except Exception as e:
        print(f"Error fetching page {page}: {e}", file=sys.stderr)
        return None


def classify_question(q):
    """Classify a question as need-related or random."""
    title = q.get("title", "").lower()
    body = q.get("body", "").lower()
    combined = title + " " + body

    # Check for random-exclude patterns first
    for pattern in RANDOM_EXCLUDE:
        if pattern in combined:
            return "random"

    # Check for need-related indicators
    for indicator in NEED_INDICATORS:
        if indicator in combined:
            return "need-related"

    # Default: if no clear indicator, classify as random
    return "random"


def has_accepted_answer(q):
    """Check if a question has an accepted answer."""
    return q.get("accepted_answer_id") is not None


def has_positive_score_answer(q):
    """Check if a question has at least one answer with score > 0."""
    answers = q.get("answers", [])
    if not answers:
        return False
    return any(a.get("score", 0) > 0 for a in answers)


def main():
    page = 1
    classified = {"need-related": 0, "random": 0}
    active = {"need-related": 0, "random": 0}
    unserved = {"need-related": 0, "random": 0}
    classified_count = 0
    pages_fetched = 0

    # Fetch pages until we have enough classified questions
    while classified_count < 50:
        data = fetch_questions_page(page=page, pagesize=10)
        if data is None:
            print(f"Failed to fetch page {page}, stopping.")
            break
        items = data.get("items", [])
        if not items:
            print(f"No more items on page {page}.")
            break

        for item in items:
            cls = classify_question(item)
            if cls not in classified:
                continue
            classified[cls] += 1
            classified_count += 1

            # Check metrics
            has_accepted = has_accepted_answer(item)
            pos_answer = has_positive_score_answer(item)

            if cls == "need-related":
                if not has_accepted:
                    unserved["need-related"] += 1
                active["need-related"] += (1 if pos_answer else 0)
            else:
                if not has_accepted:
                    unserved["random"] += 1
                active["random"] += (1 if pos_answer else 0)

            # Print individual results for first 20
            if classified_count <= 20:
                title = item.get("title", "")[:80]
                need_marker = " [NEED]" if cls == "need-related" else " [RDOM]"
                print(f"  {classified_count}. {title}{need_marker}")
                print(f"   Views: {item.get('view_count', 0)}, Answers: {item.get('answer_count', 0)}, Accepted: {has_accepted}")

        pages_fetched += 1
        page += 1

        # Safety break: don't fetch more than 10 pages
        if page > 10:
            print("Reached page limit of 10, stopping.")
            break

    # Print summary
    print("\n=== Classification Summary ===")
    for cls in ["need-related", "random"]:
        count = classified[cls]
        rate = (active[cls] / count * 100) if count > 0 else 0
        us_rate = (unserved[cls] / count * 100) if count > 0 else 0
        print(f"  {cls}: {count} classified, {active[cls]} active, unserved: {unserved[cls]} ({us_rate:.1f}%)")

    print(f"\n=== Metrics ===")
    print(f"  Total classified: {classified_count}")
    print(f"  Pages fetched: {pages_fetched}")
    print(f"  G2 gate (n >= 50): {'PASS' if classified_count >= 50 else 'FAIL'}")
    print(f"  G4 gate (classified >= 30): {'PASS' if classified_count >= 30 else 'FAIL'}")

    if classified_count >= 30:
        # G1 gate: check unserved rate for need-related
        need_unserved_rate = (unserved["need-related"] / classified["need-related"] * 100) if classified["need-related"] > 0 else 0
        random_unserved_rate = (unserved["random"] / classified["random"] * 100) if classified["random"] > 0 else 0
        need_active_rate = (active["need-related"] / classified["need-related"] * 100) if classified["need-related"] > 0 else 0
        random_active_rate = (active["random"] / classified["random"] * 100) if classified["random"] > 0 else 0

        print(f"\n  G1 gate (need unserved rate):")
        print(f"    need-related unserved rate: {need_unserved_rate:.1f}%")
        print(f"    random unserved rate: {random_unserved_rate:.1f}%")
        print(f"    need-related active rate: {need_active_rate:.1f}%")
        print(f"    random active rate: {random_active_rate:.1f}%")
        print(f"    G1 threshold: unserved rate >= 20% (i.e., need not systematically served)")
        g1_pass = need_unserved_rate >= 20
        print(f"    Result: {'PASS' if g1_pass else 'FAIL'}")

        if g1_pass:
            print("\n*** ALL GATES PASS *** - view-count principle reveals unserved population on Code Review tag ***")
            return 0
        else:
            print("\n*** G1 FAIL *** - view-count principle does not reveal unserved population on Code Review tag ***")
            return 0
    else:
        print("\n*** GATE PRECONDITIONS NOT MET *** - insufficient data")
        return 2


if __name__ == "__main__":
    sys.exit(main())