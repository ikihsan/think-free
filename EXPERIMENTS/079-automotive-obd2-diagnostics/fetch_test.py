#!/usr/bin/env python3
"""
E079 — Quick test fetch for 30 candidates.
"""

import json
import os
import re
import sys
import time
import urllib.request
from typing import Any, Dict, List, Optional

API_BASE = "https://api.stackexchange.com/2.3"
SITE = "mechanics"
SLEEP = 0.5

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")
QUESTIONS_RAW = os.path.join(OUTPUT_DIR, "questions_raw.json")


def fetch(url: str, params: Dict[str, str]) -> Optional[Dict]:
    query = "&".join(f"{k}={v}" for k, v in params.items())
    full_url = f"{url}?{query}"
    try:
        req = urllib.request.Request(full_url, headers={"User-Agent": "Think Free E079"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
            if "backoff" in data:
                time.sleep(data["backoff"])
            return data
    except Exception as e:
        print(f"Error: {e}")
        return None


def main() -> int:
    with open(QUESTIONS_RAW, "r") as f:
        raw = json.load(f)

    # Find title candidates
    OBD2_PATTERN = re.compile(r'\b[PBCU][0-9]{4}\b')
    candidates = [q for q in raw if OBD2_PATTERN.search(q.get("title", "").upper())]
    print(f"Total title candidates: {len(candidates)}")

    # Take first 30
    test_ids = [q["question_id"] for q in candidates[:30]]
    print(f"Test IDs: {test_ids}")

    # Fetch full questions
    print("Fetching questions...")
    ids_str = ";".join(str(qid) for qid in test_ids)
    data = fetch(f"{API_BASE}/questions/{ids_str}", {"site": SITE})
    if not data or "items" not in data:
        print("Failed to fetch questions")
        return 1
    questions = data["items"]
    print(f"Got {len(questions)} questions")

    # Fetch answers
    print("Fetching answers...")
    data = fetch(f"{API_BASE}/questions/{ids_str}/answers", {
        "site": SITE, "pagesize": "10", "order": "desc", "sort": "votes"
    })
    answers_map = {}
    if data and "items" in data:
        for ans in data["items"]:
            qid = ans.get("question_id")
            if qid not in answers_map:
                answers_map[qid] = []
            answers_map[qid].append(ans)
    print(f"Got answers for {len(answers_map)} questions")

    # Merge
    for q in questions:
        q["answers"] = answers_map.get(q["question_id"], [])

    # Save test data
    test_file = os.path.join(OUTPUT_DIR, "test_candidates.json")
    with open(test_file, "w") as f:
        json.dump(questions, f, indent=2)
    print(f"Saved to {test_file}")

    # Print sample
    for q in questions[:5]:
        print(f"\nQ{q['question_id']}: {q['title']}")
        print(f"  Tags: {q['tags']}")
        print(f"  Body preview: {q.get('body', '')[:200]}...")
        print(f"  Answers: {len(q['answers'])}")
        for ans in q['answers'][:1]:
            print(f"  Top answer score: {ans.get('score')}, accepted: {ans.get('is_accepted')}")
            print(f"  Answer preview: {ans.get('body', '')[:300]}...")

    return 0


if __name__ == "__main__":
    sys.exit(main())