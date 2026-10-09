#!/usr/bin/env python3
"""
E082 — Fetch electronics.stackexchange.com questions with MCU fault codes.
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
SITE = "electronics.stackexchange.com"
PAGE_SIZE = 100
MAX_PAGES_PER_QUERY = 50
SLEEP_BETWEEN_REQUESTS = 0.1  # seconds, respect API limits

# Common MCU family tags on electronics.SE
MCU_TAGS = [
    "stm32", "stm32f1", "stm32f4", "stm32h7", "stm32g0", "stm32l4", "stm32wb", "stm32wl",
    "arm", "cortex-m", "cortex-m0", "cortex-m3", "cortex-m4", "cortex-m7", "cortex-m33",
    "atmel", "avr", "atmega", "attiny", "arduino",
    "pic", "dspic", "pic16", "pic18", "pic24", "pic32",
    "esp32", "esp8266", "espressif",
    "nrf52", "nrf51", "nordic",
    "msp430", "msp432", "ti-msp",
    "tm4c", "tiva", "stellaris", "lm4f",
    "lpc", "lpc17", "lpc43", "lpc55", "nxp",
    "kinetis", "k20", "k22", "k64", "k66", "k80", "k82",
    "efm32", "gecko", "silabs", "silicon-labs",
    "sam", "samd", "samc", "same", "saml", "samg", "samv", "samrh",
    "rp2040", "rp2350", "raspberry-pi-pico", "pico",
]

# Fault/exception search tags
FAULT_TAGS = ["hardfault", "fault", "exception", "crash", "reset", "watchdog", "brownout"]

# Fault pattern regex (case-insensitive)
FAULT_PATTERN = re.compile(
    r'\b(?:'
    r'HardFault|MemManage|BusFault|UsageFault|SecureFault|'
    r'HFSR|CFSR|DFSR|AFSR|MMFAR|BFAR|UFSR|BFSR|SHCSR|'
    r'EXC_RETURN|FAULTMASK|PRIMASK|BASEPRI|'
    r'stack\s+overflow|watchdog|brownout|brown-out|'
    r'Hard\s+Fault|Bus\s+Fault|Usage\s+Fault|MemManage\s+Fault|Secure\s+Fault|'
    r'DIVBYZERO|UNALIGNED|NOCP|INVSTATE|UNDEFINSTR|INVPC|'
    r'IBUSERR|PRECISERR|IMPRECISERR|UNSTKERR|STKERR|'
    r'null\s+pointer|division\s+by\s+zero|undefined\s+instruction|'
    r'fault|exception|crash|reset|watchdog|brownout'
    r')\b',
    re.IGNORECASE
)

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
        req = urllib.request.Request(full_url, headers={"User-Agent": "Think Free E082"})
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
    """Search questions tagged with a specific tag. Gets title, tags, but not body by default."""
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


def has_fault_indicator_in_title(item: Dict) -> bool:
    """Check if a question has any fault indicator in title."""
    title = item.get("title", "")
    return bool(FAULT_PATTERN.search(title))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    print("=== E082 Fetch electronics.SE Questions with MCU Fault Indicators ===")
    print(f"Output directory: {OUTPUT_DIR}")
    print()

    all_questions = []
    seen_ids = set()

    # Strategy 1: Search by fault tags (most direct)
    print("Fetching questions by fault-related tags...")
    for tag in FAULT_TAGS:
        print(f"  Tag: {tag}")
        questions = search_questions_by_tag(tag, pages=MAX_PAGES_PER_QUERY)
        print(f"    Found {len(questions)} questions")
        for q in questions:
            if q["question_id"] not in seen_ids:
                seen_ids.add(q["question_id"])
                all_questions.append(q)
        time.sleep(SLEEP_BETWEEN_REQUESTS)

    # Strategy 2: Search by MCU tags
    print("\nFetching questions by MCU family tags...")
    for mcu in MCU_TAGS:
        print(f"  Tag: {mcu}")
        questions = search_questions_by_tag(mcu, pages=10)  # Fewer pages per MCU
        print(f"    Found {len(questions)} questions")
        for q in questions:
            if q["question_id"] not in seen_ids:
                seen_ids.add(q["question_id"])
                all_questions.append(q)
        time.sleep(SLEEP_BETWEEN_REQUESTS)

    print(f"\nTotal unique questions (title-only): {len(all_questions)}")

    # Filter for fault indicators in TITLE
    title_candidates = [q for q in all_questions if has_fault_indicator_in_title(q)]
    print(f"Questions with fault indicators in title: {len(title_candidates)}")

    # Also include all fault-tagged questions (likely relevant even without indicator in title)
    fault_tagged_ids = {q["question_id"] for q in all_questions if any(t in FAULT_TAGS for t in q.get("tags", []))}
    print(f"Questions tagged with fault tags: {len(fault_tagged_ids)}")

    # Combine: title candidates + fault-tagged questions
    candidate_ids = set(q["question_id"] for q in title_candidates) | fault_tagged_ids
    print(f"Total candidate questions for full fetch: {len(candidate_ids)}")

    # Fetch full question details (with body) for candidates
    print("\nFetching full question details (with body)...")
    candidate_questions = fetch_questions_by_ids(list(candidate_ids))
    print(f"Fetched {len(candidate_questions)} full questions")

    # Extract fault types from title + body
    for q in candidate_questions:
        text = f"{q.get('title', '')} {q.get('body', '')}"
        q["fault_indicators"] = FAULT_PATTERN.findall(text)

    # Filter for questions that actually have fault indicators in title or body
    questions_with_faults = [q for q in candidate_questions if q["fault_indicators"]]
    print(f"Questions with fault indicators in title/body: {len(questions_with_faults)}")

    # Fetch answers for these questions
    print("\nFetching answers...")
    question_ids = [q["question_id"] for q in questions_with_faults]
    answers_map = fetch_answers_for_questions(question_ids)
    for q in questions_with_faults:
        q["answers"] = answers_map.get(q["question_id"], [])

    # Save raw questions (title-only, all)
    raw_path = os.path.join(OUTPUT_DIR, "questions_raw.json")
    with open(raw_path, "w") as f:
        json.dump(all_questions, f, indent=2)
    print(f"Saved raw questions to {raw_path}")

    # Save questions with faults and answers
    with_answers_path = os.path.join(OUTPUT_DIR, "questions_with_answers.json")
    with open(with_answers_path, "w") as f:
        json.dump(questions_with_faults, f, indent=2)
    print(f"Saved questions with faults and answers to {with_answers_path}")

    # Summary statistics
    fault_counts = {}
    for q in questions_with_faults:
        for fault in q["fault_indicators"]:
            fault_counts[fault] = fault_counts.get(fault, 0) + 1

    print(f"\nTotal fault indicator mentions: {sum(fault_counts.values())}")
    print(f"Unique fault indicators: {len(fault_counts)}")
    print("\nTop 30 fault indicators:")
    for fault, count in sorted(fault_counts.items(), key=lambda x: -x[1])[:30]:
        print(f"  {fault}: {count}")

    return 0


if __name__ == "__main__":
    sys.exit(main())