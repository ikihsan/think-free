#!/usr/bin/env python3
"""
Fetch unanswered questions from Electrical Engineering Stack Exchange.
Two arms: Arm A (votes), Arm B (creation).
"""

import json
import time
import urllib.request
import urllib.error
from pathlib import Path

API_BASE = "https://api.stackexchange.com/2.3"
SITE = "electronics"
PAGESIZE = 100
FROM_DATE = 1735689600  # 2025-01-01

def fetch_page(url):
    """Fetch a single page from the API."""
    req = urllib.request.Request(url, headers={'User-Agent': 'think-free/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.load(resp)
            return data
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
        if e.code == 429:
            print("Rate limited, waiting 60s...")
            time.sleep(60)
            return fetch_page(url)
        raise
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        raise

def fetch_questions(sort, pages, arm_name):
    """Fetch questions with body included."""
    questions = []
    # Filter to include body: withbody is a predefined filter
    for page in range(1, pages + 1):
        url = f"{API_BASE}/questions?order=desc&sort={sort}&site={SITE}&pagesize={PAGESIZE}&page={page}&fromdate={FROM_DATE}&filter=withbody"
        print(f"Fetching {arm_name} page {page}...")
        data = fetch_page(url)
        questions.extend(data.get('items', []))
        if not data.get('has_more', False):
            break
        time.sleep(0.1)
    return questions

def fetch_arm_a():
    """Arm A: sort=votes, 2 pages of 100."""
    return fetch_questions('votes', 2, 'Arm A')

def fetch_arm_b():
    """Arm B: sort=creation, 10 pages of 100 (1000 questions)."""
    return fetch_questions('creation', 10, 'Arm B')

def main():
    out_dir = Path(__file__).parent
    fetch_log = []

    print("=" * 60)
    print("E144 - Fetching Electrical Engineering SE questions")
    print("=" * 60)

    # Fetch Arm A
    arm_a = fetch_arm_a()
    print(f"Arm A (votes): {len(arm_a)} questions fetched")

    # Fetch Arm B
    arm_b = fetch_arm_b()
    print(f"Arm B (creation): {len(arm_b)} questions fetched")

    # Filter for unanswered (accepted=false)
    arm_a_unanswered = [q for q in arm_a if not q.get('is_answered', False)]
    arm_b_unanswered = [q for q in arm_b if not q.get('is_answered', False)]

    print(f"Arm A unanswered: {len(arm_a_unanswered)}")
    print(f"Arm B unanswered: {len(arm_b_unanswered)}")

    # Save raw data
    with open(out_dir / 'arm_a_raw.json', 'w') as f:
        json.dump(arm_a, f, indent=2)
    with open(out_dir / 'arm_b_raw.json', 'w') as f:
        json.dump(arm_b, f, indent=2)

    # Save filtered data
    with open(out_dir / 'arm_a_unanswered.json', 'w') as f:
        json.dump(arm_a_unanswered, f, indent=2)
    with open(out_dir / 'arm_b_unanswered.json', 'w') as f:
        json.dump(arm_b_unanswered, f, indent=2)

    # Save fetch log
    fetch_log.append({
        'arm': 'A',
        'sort': 'votes',
        'pages_fetched': 2,
        'total_fetched': len(arm_a),
        'unanswered': len(arm_a_unanswered)
    })
    fetch_log.append({
        'arm': 'B',
        'sort': 'creation',
        'pages_fetched': 1,
        'total_fetched': len(arm_b),
        'unanswered': len(arm_b_unanswered)
    })

    with open(out_dir / 'fetch-log.json', 'w') as f:
        json.dump(fetch_log, f, indent=2)

    print("\nDone. Files written:")
    print(f"  {out_dir}/arm_a_raw.json")
    print(f"  {out_dir}/arm_b_raw.json")
    print(f"  {out_dir}/arm_a_unanswered.json")
    print(f"  {out_dir}/arm_b_unanswered.json")
    print(f"  {out_dir}/fetch-log.json")

if __name__ == '__main__':
    main()