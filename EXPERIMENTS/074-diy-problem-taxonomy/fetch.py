#!/usr/bin/env python3
"""
Experiment 074: DIY Problem Taxonomy — Fetch Script
Fetches questions from DIY Stack Exchange API.
stdlib only, Python 3.8+
"""

import json
import time
import urllib.request
import urllib.error
from pathlib import Path

API_BASE = "https://api.stackexchange.com/2.3"
SITE = "diy"
PAGE_SIZE = 100
MAX_PAGES = 3  # ~300 questions total across different sorts

def fetch(url):
    """Fetch URL with rate limiting."""
    req = urllib.request.Request(url, headers={"User-Agent": "think-free/074"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        if e.code == 429:
            # Rate limited - wait and retry
            retry_after = int(e.headers.get("Retry-After", 5))
            print(f"Rate limited, waiting {retry_after}s...")
            time.sleep(retry_after)
            return fetch(url)
        elif e.code == 400:
            # Bad request - might be invalid sort
            print(f"Bad request: {url}")
            return None
        else:
            raise
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def fetch_questions(sort, order="desc", pages=MAX_PAGES):
    """Fetch questions with given sort."""
    all_items = []
    has_more = True
    page = 1

    while has_more and page <= pages:
        url = f"{API_BASE}/questions?order={order}&sort={sort}&site={SITE}&pagesize={PAGE_SIZE}&page={page}&filter=!9Z(-wzftf"
        print(f"Fetching {sort} page {page}...")
        data = fetch(url)
        if not data:
            break
        items = data.get("items", [])
        all_items.extend(items)
        has_more = data.get("has_more", False)
        page += 1
        # Be nice to the API
        time.sleep(0.1)

    return all_items


def fetch_no_answers(pages=MAX_PAGES):
    """Fetch unanswered questions."""
    all_items = []
    has_more = True
    page = 1

    while has_more and page <= pages:
        url = f"{API_BASE}/questions/no-answers?order=desc&sort=activity&site={SITE}&pagesize={PAGE_SIZE}&page={page}&filter=!9Z(-wzftf"
        print(f"Fetching no-answers page {page}...")
        data = fetch(url)
        if not data:
            break
        items = data.get("items", [])
        all_items.extend(items)
        has_more = data.get("has_more", False)
        page += 1
        time.sleep(0.1)

    return all_items


def main():
    exp_dir = Path(__file__).parent
    data_dir = exp_dir / "data"
    data_dir.mkdir(exist_ok=True)

    all_questions = []
    seen_ids = set()

    # Fetch from different sorts to get diverse sample
    for sort in ["votes", "activity", "creation"]:
        items = fetch_questions(sort, pages=2)
        for q in items:
            if q["question_id"] not in seen_ids:
                seen_ids.add(q["question_id"])
                all_questions.append(q)

    # Fetch unanswered
    items = fetch_no_answers(pages=2)
    for q in items:
        if q["question_id"] not in seen_ids:
            seen_ids.add(q["question_id"])
            all_questions.append(q)

    print(f"Total unique questions fetched: {len(all_questions)}")

    # Save raw data
    raw_file = data_dir / "questions_raw.json"
    with open(raw_file, "w") as f:
        json.dump({"items": all_questions}, f, indent=2)
    print(f"Wrote {raw_file}")

    # Also save just the items array for analyze.py
    questions_file = data_dir / "questions.json"
    with open(questions_file, "w") as f:
        json.dump({"items": all_questions}, f, indent=2)
    print(f"Wrote {questions_file}")

    # Print summary
    answered = sum(1 for q in all_questions if q.get("is_answered"))
    unanswered = len(all_questions) - answered
    print(f"Answered: {answered}, Unanswered: {unanswered}")

    # Tag distribution
    tag_counts = {}
    for q in all_questions:
        for t in q.get("tags", []):
            tag_counts[t] = tag_counts.get(t, 0) + 1
    print("\nTop 20 tags:")
    for tag, count in sorted(tag_counts.items(), key=lambda x: -x[1])[:20]:
        print(f"  {tag}: {count}")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())