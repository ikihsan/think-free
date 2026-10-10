#!/usr/bin/env python3
"""E096 — Harvest aviation maintenance fault code topics from Aviation Stack Exchange."""

import json
import os
import sys
import time
import urllib.request
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

SEARCH_URL = "https://api.stackexchange.com/2.3/search/advanced"

# Comprehensive search queries for aviation maintenance fault codes
SEARCH_QUERIES = [
    'maintenance fault',           # found 3 topics earlier
    'aircraft maintenance error',  # found 1 topic earlier
    'engine fault code',           # found 1 topic earlier
    'landing gear fault',          # found 2 topics earlier
    'aviation maintenance',        # found 1 topic just now
    'aircraft fault',              # found 1 topic just now
    'plane maintenance',           # found 1 topic just now
    'pilot error',                 # found 1 topic just now
    'avionics troubleshooting',    # found 1 topic just now (23487 views!)
    'aircraft system',             # found 1 topic just now
    'flight deck',                 # found 1 topic just now
    'cockpit warning',             # found 1 topic just now
    'aircraft reliability',        # found 1 topic just now
    'maintenance review',          # found 1 topic just now
    'airworthiness',               # found 1 topic just now (4304 views!)
    'technical fault',             # found 1 topic just now
    'aircraft problem',            # found 1 topic just now
    'maintenance issue',           # found 1 topic just now
    'aviation problem',            # found 1 topic just now
    'flight maintenance',          # found 1 topic just now
    'plane maintenance',           # found 1 topic just now
    'engine monitor',              # found 1 topic just now
    'systems failure',             # found 1 topic just now (3354 views!)
    'aircraft incident',           # found 1 topic just now
]

def se_api(url):
    """Fetch data from the Stack Exchange API with polite delays."""
    time.sleep(1.0)  # 1 request per second, well under 300/day unauthenticated
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "E096-aviation-view-count/1.0"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:
        print(f"  API error: {e}")
        return None


def harvest_topics(query, max_pages=1):
    """Harvest topics for one search query."""
    items = []
    for page in range(1, max_pages + 1):
        params = urllib.parse.urlencode({
            "q": query,
            "site": "aviation",
            "pagesize": 100,
            "page": page,
        })
        url = SEARCH_URL + "?" + params
        data = se_api(url)
        if data is None:
            break
        items.extend(data.get("items", []))
        if not data.get("has_more"):
            break
    return items


def load_corpus_from_api():
    """Harvest topics from all search queries and return list of dicts."""
    print("=== E096 Aviation Stack Exchange harvest ===")
    all_topics = []
    
    for i, query in enumerate(SEARCH_QUERIES):
        print(f"  Query {i+1}: {query[:55]}...")
        topics = harvest_topics(query, max_pages=1)  # 1 page per query
        print(f"    -> {len(topics)} topics")
        
        for topic in topics:
            row = {
                "id": topic.get("question_id"),
                "title": topic.get("title", ""),
                "body": topic.get("body", ""),
                "view_count": topic.get("view_count", 0),
                "answer_count": topic.get("answer_count", 0),
                "score": topic.get("score", 0),
                "tags": topic.get("tags", []),
                "accepted_answer_id": topic.get("accepted_answer_id"),
                "last_activity_date": topic.get("last_activity_date"),
                "creation_date": topic.get("creation_date"),
                "question_score": topic.get("score", 0),
                "query": query,
            }
            all_topics.append(row)
    
    # Remove duplicates by question_id
    seen = set()
    unique = []
    for t in all_topics:
        qid = t['id']
        if qid not in seen:
            seen.add(qid)
            unique.append(t)
    
    print(f"\nTotal unique topics harvested: {len(unique)}")
    return unique


def main():
    import argparse
    parser = argparse.ArgumentParser(description="E096 harvest arm")
    parser.add_argument("--arm", type=int, default=1,
                        help="Arm to harvest (1=treatment, 2=control)")
    parser.add_argument("--limit", type=int, default=None,
                        help="Max number of topics to harvest")
    args = parser.parse_args()
    
    topics = load_corpus_from_api()
    
    # Filter to only those with view_count > 0 and some content
    filtered = [t for t in topics if t['view_count'] > 0 and (t['title'] or t['body'])]
    
    print(f"\nFiltered to {len(filtered)} topics with view_count > 0 and content")
    
    if args.arm == 1:
        corpus_path = os.path.join(HERE, "treatment-needs.jsonl")
        output_path = os.path.join(HERE, "treatment-results.jsonl")
    else:
        corpus_path = os.path.join(HERE, "control-needs.jsonl")
        output_path = os.path.join(HERE, "control-results.jsonl")
    
    os.makedirs(os.path.dirname(corpus_path), exist_ok=True)
    with open(corpus_path, "w", encoding="utf-8") as f:
        for row in filtered[:args.limit] if args.limit else filtered:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    
    print(f"Wrote {len(filtered[:args.limit]) if args.limit else len(filtered)} results to {corpus_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
