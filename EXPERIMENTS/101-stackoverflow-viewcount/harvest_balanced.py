#!/usr/bin/env python3
"""
Harvest questions from Stack Overflow (all questions, not just unanswered)
sorted by votes, then filter for high view_count. This matches E077/E082 methodology.
"""

import json
import time
import sys
import os
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

# Tags to sample
TAGS = [
    "python",
    "javascript",
    "java",
    "c++",
    "go",
    "rust",
    "typescript",
    "php",
    "ruby",
]

# API parameters
BASE_URL = "https://api.stackexchange.com/2.3"
PAGESIZE = 100
PAGES_PER_TAG = 3  # 3 pages * 100 = 300 questions per tag
MIN_VIEW_COUNT = 1000  # G1 threshold from E078

# Output
OUT_DIR = Path(__file__).parent / "raw"
OUT_DIR.mkdir(exist_ok=True)

def fetch_page(tag: str, page: int) -> dict:
    """Fetch one page of questions for a tag, sorted by votes."""
    url = (
        f"{BASE_URL}/questions"
        f"?order=desc&sort=votes&tagged={tag}&site=stackoverflow"
        f"&pagesize={PAGESIZE}&page={page}"
    )
    req = Request(url, headers={"User-Agent": "think-free/1.0"})
    try:
        with urlopen(req, timeout=30) as resp:
            data = json.load(resp)
            return data
    except HTTPError as e:
        if e.code == 429:
            print(f"Rate limited, waiting 60s...", file=sys.stderr)
            time.sleep(60)
            return fetch_page(tag, page)
        raise
    except URLError as e:
        print(f"Network error for {tag} page {page}: {e}", file=sys.stderr)
        raise

def harvest_tag(tag: str) -> list:
    """Harvest all pages for one tag."""
    questions = []
    for page in range(1, PAGES_PER_TAG + 1):
        print(f"Fetching {tag} page {page}/{PAGES_PER_TAG}...", file=sys.stderr)
        data = fetch_page(tag, page)
        items = data.get("items", [])
        if not items:
            print(f"  No more items, stopping at page {page}", file=sys.stderr)
            break
        # Filter for min view count
        filtered = [
            q for q in items
            if q.get("view_count", 0) >= MIN_VIEW_COUNT
        ]
        questions.extend(filtered)
        print(f"  Got {len(items)} total, {len(filtered)} passing view_count filter", file=sys.stderr)
        time.sleep(0.5)
        if not data.get("has_more", False):
            break
    return questions

def main():
    all_questions = []
    for tag in TAGS:
        print(f"\n=== Harvesting tag: {tag} ===", file=sys.stderr)
        try:
            qs = harvest_tag(tag)
            print(f"Tag {tag}: {len(qs)} questions after filters", file=sys.stderr)
            all_questions.extend(qs)
        except Exception as e:
            print(f"Error harvesting {tag}: {e}", file=sys.stderr)
            continue

    # Deduplicate by question_id
    seen = set()
    unique = []
    for q in all_questions:
        qid = q["question_id"]
        if qid not in seen:
            seen.add(qid)
            unique.append(q)

    # Sort by view_count descending
    unique.sort(key=lambda q: q.get("view_count", 0), reverse=True)

    print(f"\nTotal unique questions: {len(unique)}", file=sys.stderr)

    # Save raw harvest
    out_file = OUT_DIR / "harvest_balanced.jsonl"
    with open(out_file, "w") as f:
        for q in unique:
            f.write(json.dumps(q) + "\n")
    print(f"Saved to {out_file}", file=sys.stderr)

    # Also save summary
    summary = {
        "total_unique": len(unique),
        "tags": TAGS,
        "pages_per_tag": PAGES_PER_TAG,
        "min_view_count": MIN_VIEW_COUNT,
        "questions": [
            {
                "question_id": q["question_id"],
                "title": q["title"],
                "view_count": q["view_count"],
                "answer_count": q["answer_count"],
                "score": q["score"],
                "tags": q["tags"],
                "is_answered": q["is_answered"],
                "creation_date": q["creation_date"],
                "link": q["link"],
            }
            for q in unique
        ],
    }
    summary_file = OUT_DIR / "harvest_balanced_summary.json"
    with open(summary_file, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Summary saved to {summary_file}", file=sys.stderr)

if __name__ == "__main__":
    main()