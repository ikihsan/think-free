"""E095 — View-count principle on GitHub Discussions."""

import json
import urllib.request
import sys

# Configuration
REPO = "github/linguist"
GATE = "--gate" in sys.argv

# Need-related classification heuristics
NEED_INDICATORS = [
    "how to", "how do i", "how can i", "want to", "trying to",
    "run", "build", "create", "fix", "debug", "solve", "resolve",
    "error", "fail", "not working", "cannot", "issue", "bug", "problem",
    "import", "module", "package", "install",
]
RANDOM_EXCLUDE = [
    "announcement", "release", "version", "changelog",
    "hello", "introduce", "showcase", "demo",
    "thank", "thanks", "welcome",
    "discussion", "question",
]


def fetch_discussions_page(page=1, per_page=100):
    """Fetch one page of Discussions from the GitHub API."""
    url = f"https://api.github.com/repos/{REPO}/discussions?page={page}&per_page={per_page}"
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "origin-mission-E095",
            "Accept": "application/vnd.github+json"
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read().decode()
            return json.loads(data)
    except Exception as e:
        print(f"Error fetching discussions page {page}: {e}", file=sys.stderr)
        return None


def classify_discussion(d):
    """Classify a discussion as need-related or random."""
    title = d.get("title", "").lower()
    body = d.get("body", "").lower()
    body = body or ""  # body can be None
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


def main():
    page = 1
    classified = {"need-related": 0, "random": 0}
    has_comments = {"need-related": 0, "random": 0}  # discussions with comments > 0
    no_comments = {"need-related": 0, "random": 0}  # discussions with comments == 0
    classified_count = 0
    pages_fetched = 0

    # Fetch pages until we have enough classified discussions
    while classified_count < 50:
        data = fetch_discussions_page(page=page, per_page=100)
        if data is None:
            print(f"Failed to fetch page {page}, stopping.")
            break
        items = data
        if not items:
            print(f"No more discussions on page {page}.")
            break

        for item in items:
            cls = classify_discussion(item)
            if cls not in classified:
                continue
            classified[cls] += 1
            classified_count += 1

            # Check comment count
            comment_count = item.get("comments", 0) or 0
            if cls == "need-related":
                has_comments["need-related"] += (1 if comment_count > 0 else 0)
                no_comments["need-related"] += (1 if comment_count == 0 else 0)
            else:
                has_comments["random"] += (1 if comment_count > 0 else 0)
                no_comments["random"] += (1 if comment_count == 0 else 0)

            # Print individual results for first 20
            if classified_count <= 20:
                title = item.get("title", "")[:80]
                needs = " [NEED]" if cls == "need-related" else " [RDOM]"
                print(f"  {classified_count}. {title}{needs} (comments={comment_count})")

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
        has_c = has_comments[cls]
        no_c = no_comments[cls]
        has_rate = (has_c / count * 100) if count > 0 else 0
        no_rate = (no_c / count * 100) if count > 0 else 0
        print(f"  {cls}: {count} classified, {has_c} have comments ({has_rate:.1f}%), {no_c} no comments ({no_rate:.1f}%)")

    print(f"\n=== Metrics ===")
    print(f"  Total classified: {classified_count}")
    print(f"  Pages fetched: {pages_fetched}")
    print(f"  G2 gate (n >= 50): {'PASS' if classified_count >= 50 else 'FAIL'}")
    print(f"  G4 gate (classified >= 30): {'PASS' if classified_count >= 30 else 'FAIL'}")

    if classified_count >= 30:
        # G1 gate: check unserved rate for need-related (comments == 0)
        need_no_comment_rate = (no_comments["need-related"] / classified["need-related"] * 100) if classified["need-related"] > 0 else 0
        random_no_comment_rate = (no_comments["random"] / classified["random"] * 100) if classified["random"] > 0 else 0
        need_has_comment_rate = (has_comments["need-related"] / classified["need-related"] * 100) if classified["need-related"] > 0 else 0
        random_has_comment_rate = (has_comments["random"] / classified["random"] * 100) if classified["random"] > 0 else 0

        print(f"\n  G1 gate (need no-comments rate / served rate):")
        print(f"    need-related no-comments rate: {need_no_comment_rate:.1f}%")
        print(f"    random no-comments rate: {random_no_comment_rate:.1f}%")
        print(f"    need-related has-comments rate: {need_has_comment_rate:.1f}%")
        print(f"    G1 threshold: no-comments rate >= 20% (i.e., need not systematically served)")
        g1_pass = need_no_comment_rate >= 20
        print(f"    Result: {'PASS' if g1_pass else 'FAIL'}")

        if g1_pass:
            print("\n*** ALL GATES PASS *** - view-count principle reveals unserved population on GitHub Discussions ***")
            return 0
        else:
            print("\n*** G1 FAIL *** - view-count principle does not reveal unserved population on GitHub Discussions ***")
            return 0
    else:
        print("\n*** GATE PRECONDITIONS NOT MET *** - insufficient data")
        return 2


if __name__ == "__main__":
    sys.exit(main())