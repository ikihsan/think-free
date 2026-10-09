#!/usr/bin/env python3
"""
E083 — Harvest helpers for 3D printer Discourse forums.
"""

import json
import time
import urllib.request
import urllib.error
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

TOPICS_PER_FORUM = 100
SLEEP_BETWEEN_REQUESTS = 1.0  # seconds, polite polling
MAX_PAGES = 10  # Safety limit


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------

def fetch_latest_page(domain: str, page: int) -> Optional[Dict]:
    """Fetch a page of topics from a Discourse forum."""
    url = f"https://{domain}/latest.json?page={page}&per_page=30"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Think Free E083)"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        if e.code == 429:
            print(f"    Rate limited on {domain} page {page}, waiting 30 seconds...")
            time.sleep(30)
            return fetch_latest_page(domain, page)
        print(f"    Error fetching {url}: {e}")
        return None
    except Exception as e:
        print(f"    Error fetching {url}: {e}")
        return None


def fetch_topic_details(domain: str, topic_id: int) -> Optional[Dict]:
    """Fetch full topic details including posts."""
    url = f"https://{domain}/t/{topic_id}.json"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Think Free E083)"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        if e.code == 429:
            print(f"    Rate limited on {domain} topic {topic_id}, waiting 30 seconds...")
            time.sleep(30)
            return fetch_topic_details(domain, topic_id)
        print(f"    Error fetching {url}: {e}")
        return None
    except Exception as e:
        print(f"    Error fetching {url}: {e}")
        return None


def harvest_forum_topics(domain: str, max_topics: int = TOPICS_PER_FORUM) -> List[Dict]:
    """Harvest topics from a Discourse forum across multiple pages."""
    all_topics: List[Dict] = []

    for page in range(1, MAX_PAGES + 1):
        data = fetch_latest_page(domain, page)
        if data is None:
            break

        page_topics = data.get("topic_list", {}).get("topics", [])
        if not page_topics:
            break

        all_topics.extend(page_topics)

        if len(all_topics) >= max_topics:
            break

        time.sleep(SLEEP_BETWEEN_REQUESTS)

    # Deduplicate by topic id
    seen_ids: set = set()
    deduped: List[Dict] = []
    for t in all_topics:
        tid = t.get("id", 0)
        if tid not in seen_ids:
            seen_ids.add(tid)
            deduped.append(t)
        if len(deduped) >= max_topics:
            break

    # Convert to standardized topic dict format
    topics: List[Dict] = []
    for t in deduped[:max_topics]:
        topic = {
            "id": t.get("id"),
            "title": t.get("title", ""),
            "views": t.get("views", 0),
            "reply_count": t.get("reply_count", 0),
            "like_count": t.get("like_count", 0),
            "op_like_count": t.get("op_like_count", 0),
            "has_accepted_answer": t.get("has_accepted_answer", False),
            "closed": t.get("closed", False),
            "tags": t.get("tags", []),
            "created_at": t.get("created_at", ""),
            "last_posted_at": t.get("last_posted_at", ""),
            "_domain": domain,
        }
        topics.append(topic)

    return topics


def harvest_topic_posts(domain: str, topic_ids: List[int]) -> Dict[int, List[Dict]]:
    """Fetch posts for a list of topic IDs. Returns dict topic_id -> list of posts."""
    posts_by_topic: Dict[int, List[Dict]] = {}

    for tid in topic_ids:
        data = fetch_topic_details(domain, tid)
        if data is None:
            posts_by_topic[tid] = []
            continue

        post_stream = data.get("post_stream", {})
        posts = post_stream.get("posts", [])
        # Skip first post (OP), keep replies
        replies = posts[1:] if len(posts) > 1 else []
        posts_by_topic[tid] = [
            {
                "post_number": p.get("post_number"),
                "username": p.get("username"),
                "created_at": p.get("created_at"),
                "cooked": p.get("cooked", ""),  # HTML content
                "raw": p.get("raw", ""),       # Markdown content
            }
            for p in replies
        ]
        time.sleep(SLEEP_BETWEEN_REQUESTS)

    return posts_by_topic


def save_raw_data(domain: str, topics: List[Dict], classified: List[Dict], posts_by_topic: Dict[int, List[Dict]], output_dir: str):
    """Save raw topic data, classified data, and posts to JSONL files."""
    import os
    os.makedirs(output_dir, exist_ok=True)

    # Sanitize domain for filename
    safe_domain = domain.replace(".", "_")

    # Save raw topics
    with open(os.path.join(output_dir, f"topics_{safe_domain}.jsonl"), "w") as f:
        for t in topics:
            f.write(json.dumps(t) + "\n")

    # Save classified topics
    with open(os.path.join(output_dir, f"classified_{safe_domain}.jsonl"), "w") as f:
        for t in classified:
            f.write(json.dumps(t) + "\n")

    # Save posts
    with open(os.path.join(output_dir, f"posts_{safe_domain}.jsonl"), "w") as f:
        for tid, posts in posts_by_topic.items():
            for p in posts:
                p_copy = p.copy()
                p_copy["topic_id"] = tid
                f.write(json.dumps(p_copy) + "\n")


def load_raw_topics(domain: str, input_dir: str) -> List[Dict]:
    """Load raw topics from JSONL file."""
    safe_domain = domain.replace(".", "_")
    path = os.path.join(input_dir, f"topics_{safe_domain}.jsonl")
    topics = []
    if os.path.exists(path):
        with open(path, "r") as f:
            for line in f:
                topics.append(json.loads(line))
    return topics


def load_classified_topics(domain: str, input_dir: str) -> List[Dict]:
    """Load classified topics from JSONL file."""
    safe_domain = domain.replace(".", "_")
    path = os.path.join(input_dir, f"classified_{safe_domain}.jsonl")
    topics = []
    if os.path.exists(path):
        with open(path, "r") as f:
            for line in f:
                topics.append(json.loads(line))
    return topics


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 harvest.py <domain>")
        sys.exit(1)
    domain = sys.argv[1]
    topics = harvest_forum_topics(domain)
    print(f"Harvested {len(topics)} topics from {domain}")
    for t in topics[:5]:
        print(f"  [{t['views']} views, {t['reply_count']} replies] {t['title'][:80]}")