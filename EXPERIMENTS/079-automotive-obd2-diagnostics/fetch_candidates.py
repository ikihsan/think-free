#!/usr/bin/env python3
"""
E079 — Fetch full details for title candidates only.
"""

import json
import os
import sys
import time
import urllib.request
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

API_BASE = "https://api.stackexchange.com/2.3"
SITE = "mechanics"
SLEEP_BETWEEN_REQUESTS = 0.2  # seconds

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")
QUESTIONS_RAW = os.path.join(OUTPUT_DIR, "questions_raw.json")
QUESTIONS_FULL = os.path.join(OUTPUT_DIR, "questions_full.json")
ANSWERS_FILE = os.path.join(OUTPUT_DIR, "answers.json")


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
            if "backoff" in data:
                time.sleep(data["backoff"])
            return data
    except urllib.error.HTTPError as e:
        if e.code == 429:
            print(f"    Rate limited, waiting 60 seconds...")
            time.sleep(60)
            return fetch_page(url, params)
        print(f"    HTTP error {e.code}: {e.reason}")
        return None
    except Exception as e:
        print(f"    Error: {e}")
        return None


def fetch_questions_by_ids(question_ids: List[int]) -> List[Dict]:
    """Fetch full question details (with body) for a list of question IDs."""
    if not question_ids:
        return []

    all_items = []
    for i in range(0, len(question_ids), 100):
        batch = question_ids[i:i+100]
        ids_str = ";".join(str(qid) for qid in batch)
        params = {"site": SITE}
        print(f"  Fetching questions {i+1}-{i+len(batch)}...")
        data = fetch_page(f"{API_BASE}/questions/{ids_str}", params)
        if not data or "items" not in data:
            continue
        all_items.extend(data["items"])
        time.sleep(SLEEP_BETWEEN_REQUESTS)
    return all_items


def fetch_answers_for_questions(question_ids: List[int]) -> Dict[int, List[Dict]]:
    """Fetch answers for multiple questions."""
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
        print(f"  Fetching answers {i+1}-{i+len(batch)}...")
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


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    print("=== E079 Fetch Full Details for Title Candidates ===")

    # Load raw questions
    with open(QUESTIONS_RAW, "r") as f:
        raw_questions = json.load(f)

    # Find title candidates
    import re
    OBD2_PATTERN = re.compile(r'\b[PBCU][0-9]{4}\b')
    candidates = []
    for q in raw_questions:
        title = q.get("title", "")
        if OBD2_PATTERN.search(title.upper()):
            candidates.append(q)

    print(f"Title candidates: {len(candidates)}")
    candidate_ids = [q["question_id"] for q in candidates]

    # Fetch full questions
    print("\nFetching full question details...")
    full_questions = fetch_questions_by_ids(candidate_ids)
    print(f"Fetched {len(full_questions)} full questions")

    # Fetch answers
    print("\nFetching answers...")
    answers_map = fetch_answers_for_questions(candidate_ids)

    # Merge answers into questions
    for q in full_questions:
        q["answers"] = answers_map.get(q["question_id"], [])

    # Save
    with open(QUESTIONS_FULL, "w") as f:
        json.dump(full_questions, f, indent=2)
    print(f"Saved full questions to {QUESTIONS_FULL}")

    with open(ANSWERS_FILE, "w") as f:
        json.dump(answers_map, f, indent=2)
    print(f"Saved answers to {ANSWERS_FILE}")

    # Quick stats
    code_counts = {}
    for q in full_questions:
        text = f"{q.get('title', '')} {q.get('body', '')}"
        codes = re.findall(r'\b[PBCU][0-9]{4}\b', text.upper())
        for code in codes:
            code_counts[code] = code_counts.get(code, 0) + 1

    print(f"\nTotal OBD2 code mentions in title+body: {sum(code_counts.values())}")
    print(f"Unique codes: {len(code_counts)}")
    print("Top 20 codes:")
    for code, count in sorted(code_counts.items(), key=lambda x: -x[1])[:20]:
        print(f"  {code}: {count}")

    return 0


if __name__ == "__main__":
    sys.exit(main())