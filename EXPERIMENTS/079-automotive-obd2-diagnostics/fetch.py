#!/usr/bin/env python3
"""
E079 — Fetch Mechanics Stack Exchange questions with OBD2 codes.
Uses Stack Exchange API v2.3.
"""

import json
import os
import re
import sys
import time
import urllib.request
from typing import Any, Dict, List, Optional, Set

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

API_BASE = "https://api.stackexchange.com/2.3"
SITE = "mechanics"
PAGE_SIZE = 100
MAX_PAGES_PER_QUERY = 50
SLEEP_BETWEEN_REQUESTS = 0.1  # seconds, respect API limits

# Common vehicle make tags on Mechanics.SE (from actual tag list)
MAKE_TAGS = [
    "toyota", "honda", "ford", "chevrolet", "nissan", "hyundai",
    "bmw", "vw", "subaru", "dodge", "jeep", "mazda",
    "kia", "acura", "lexus", "volvo", "porsche", "mini",
    "mitsubishi", "suzuki", "infiniti", "cadillac", "buick", "gmc",
    "ram", "chrysler", "jaguar", "fiat", "tesla"
]

# Also search directly for OBD/DTC tagged questions
OBD_TAGS = ["obd-ii", "dtc"]

# OBD2 code pattern: P0xxx, P1xxx, P2xxx, P3xxx, Bxxxx, Cxxxx, Uxxxx
OBD2_PATTERN = re.compile(r'\b[PBCU][0-9]{4}\b')

# Output directory
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------

def fetch_page(url: str, params: Dict[str, str]) -> Optional[Dict]:
    """Fetch a page from Stack Exchange API."""
    query = "&".join(f"{k}={v}" for k, v in params.items())
    full_url = f"{url}?{query}"
    try:
        req = urllib.request.Request(full_url, headers={"User-Agent": "Think Free E079"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
            # Respect backoff
            if "backoff" in data:
                time.sleep(data["backoff"])
            return data
    except urllib.error.HTTPError as e:
        if e.code == 429:
            print(f"    Rate limited, waiting 60 seconds...")
            time.sleep(60)
            return fetch_page(url, params)
        print(f"    HTTP error {e.code}: {e.reason} for {full_url}")
        return None
    except Exception as e:
        print(f"    Error fetching {full_url}: {e}")
        return None


def search_questions_by_tag(tag: str, pages: int = MAX_PAGES_PER_QUERY) -> List[Dict]:
    """Search questions tagged with a specific tag. No filter - gets title, tags, but not body."""
    all_items = []
    for page in range(1, pages + 1):
        params = {
            "site": SITE,
            "tagged": tag,
            "pagesize": str(PAGE_SIZE),
            "page": str(page),
            "order": "desc",
            "sort": "activity",
        }
        data = fetch_page(f"{API_BASE}/questions", params)
        if not data or "items" not in data:
            break
        items = data["items"]
        if not items:
            break
        all_items.extend(items)
        if not data.get("has_more", False):
            break
        time.sleep(SLEEP_BETWEEN_REQUESTS)
    return all_items


def fetch_questions_by_ids(question_ids: List[int]) -> List[Dict]:
    """Fetch full question details (with body) for a list of question IDs."""
    if not question_ids:
        return []

    all_items = []
    # API allows up to 100 IDs at once
    for i in range(0, len(question_ids), 100):
        batch = question_ids[i:i+100]
        ids_str = ";".join(str(qid) for qid in batch)
        params = {
            "site": SITE,
            # No filter - use default which includes body
        }
        data = fetch_page(f"{API_BASE}/questions/{ids_str}", params)
        if not data or "items" not in data:
            continue
        all_items.extend(data["items"])
        time.sleep(SLEEP_BETWEEN_REQUESTS)
    return all_items


def fetch_answers_for_questions(question_ids: List[int]) -> Dict[int, List[Dict]]:
    """Fetch answers for multiple questions. Returns dict of question_id -> answers."""
    if not question_ids:
        return {}

    all_answers = {}
    for i in range(0, len(question_ids), 100):
        batch = question_ids[i:i+100]
        ids_str = ";".join(str(qid) for qid in batch)
        params = {
            "site": SITE,
            "pagesize": "10",
            "order": "desc",
            "sort": "votes",
        }
        data = fetch_page(f"{API_BASE}/questions/{ids_str}/answers", params)
        if not data or "items" not in data:
            continue
        for ans in data["items"]:
            qid = ans.get("question_id")
            if qid not in all_answers:
                all_answers[qid] = []
            all_answers[qid].append(ans)
        time.sleep(SLEEP_BETWEEN_REQUESTS)
    return all_answers


def extract_codes(text: str) -> List[str]:
    """Extract OBD2 codes from text."""
    return OBD2_PATTERN.findall(text.upper())


def has_obd2_code_in_title(item: Dict) -> bool:
    """Check if a question has any OBD2 code in title."""
    title = item.get("title", "")
    return bool(OBD2_PATTERN.search(title.upper()))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    print("=== E079 Fetch Mechanics.SE Questions with OBD2 Codes ===")
    print(f"Output directory: {OUTPUT_DIR}")
    print()

    all_questions = []
    seen_ids = set()

    # Strategy 1: Search by OBD/DTC tags (most direct)
    print("Fetching questions by OBD/DTC tags...")
    for tag in OBD_TAGS:
        print(f"  Tag: {tag}")
        questions = search_questions_by_tag(tag, pages=MAX_PAGES_PER_QUERY)
        print(f"    Found {len(questions)} questions")
        for q in questions:
            if q["question_id"] not in seen_ids:
                seen_ids.add(q["question_id"])
                all_questions.append(q)
        time.sleep(SLEEP_BETWEEN_REQUESTS)

    # Strategy 2: Search by make tags
    print("\nFetching questions by make tags...")
    for make in MAKE_TAGS:
        print(f"  Tag: {make}")
        questions = search_questions_by_tag(make, pages=10)  # Fewer pages per make
        print(f"    Found {len(questions)} questions")
        for q in questions:
            if q["question_id"] not in seen_ids:
                seen_ids.add(q["question_id"])
                all_questions.append(q)
        time.sleep(SLEEP_BETWEEN_REQUESTS)

    print(f"\nTotal unique questions (title-only): {len(all_questions)}")

    # Filter for OBD2 codes in TITLE
    title_candidates = [q for q in all_questions if has_obd2_code_in_title(q)]
    print(f"Questions with OBD2 codes in title: {len(title_candidates)}")

    # Also include all OBD/DTC tagged questions (they're likely relevant even without code in title)
    obd_tagged_ids = {q["question_id"] for q in all_questions if any(t in OBD_TAGS for t in q.get("tags", []))}
    print(f"Questions tagged with OBD/DTC tags: {len(obd_tagged_ids)}")

    # Combine: title candidates + OBD-tagged questions
    candidate_ids = set(q["question_id"] for q in title_candidates) | obd_tagged_ids
    print(f"Total candidate questions for full fetch: {len(candidate_ids)}")

    # Fetch full question details (with body) for candidates
    print("\nFetching full question details (with body)...")
    candidate_questions = fetch_questions_by_ids(list(candidate_ids))
    print(f"Fetched {len(candidate_questions)} full questions")

    # Extract codes from title + body
    for q in candidate_questions:
        text = f"{q.get('title', '')} {q.get('body', '')}"
        q["obd2_codes"] = extract_codes(text)

    # Filter for questions that actually have OBD2 codes in title or body
    questions_with_codes = [q for q in candidate_questions if q["obd2_codes"]]
    print(f"Questions with OBD2 codes in title/body: {len(questions_with_codes)}")

    # Fetch answers for these questions
    print("\nFetching answers...")
    question_ids = [q["question_id"] for q in questions_with_codes]
    answers_map = fetch_answers_for_questions(question_ids)
    for q in questions_with_codes:
        q["answers"] = answers_map.get(q["question_id"], [])

    # Save raw questions (title-only, all)
    raw_path = os.path.join(OUTPUT_DIR, "questions_raw.json")
    with open(raw_path, "w") as f:
        json.dump(all_questions, f, indent=2)
    print(f"Saved raw questions to {raw_path}")

    # Save questions with codes and answers
    with_answers_path = os.path.join(OUTPUT_DIR, "questions_with_answers.json")
    with open(with_answers_path, "w") as f:
        json.dump(questions_with_codes, f, indent=2)
    print(f"Saved questions with codes and answers to {with_answers_path}")

    # Summary statistics
    code_counts = {}
    for q in questions_with_codes:
        for code in q["obd2_codes"]:
            code_counts[code] = code_counts.get(code, 0) + 1

    print(f"\nTotal OBD2 code mentions: {sum(code_counts.values())}")
    print(f"Unique codes: {len(code_counts)}")
    print("\nTop 20 codes:")
    for code, count in sorted(code_counts.items(), key=lambda x: -x[1])[:20]:
        print(f"  {code}: {count}")

    return 0


if __name__ == "__main__":
    sys.exit(main())