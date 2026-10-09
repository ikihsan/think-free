#!/usr/bin/env python3
"""
E077 — Harvest helpers for Discourse forums.
"""

import json
import time
import urllib.request
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

TOPICS_PER_FORUM = 50
SLEEP_BETWEEN_REQUESTS = 1.0  # seconds, polite polling


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------

def fetch_latest_page(domain: str, page: int) -> Optional[Dict]:
    """Fetch a page of topics from a Discourse forum."""
    url = f"https://{domain}/latest.json?page={page}&per_page=30"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Think Free E077)"})
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


def harvest_forum_topics(domain: str, max_topics: int = TOPICS_PER_FORUM) -> List[Dict]:
    """Harvest topics from a Discourse forum across multiple pages."""
    all_topics: List[Dict] = []

    for page in range(1, 10):  # Safety limit
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

    # Convert to our standardized topic dict format
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
            "_domain": domain,
        }
        topics.append(topic)

    return topics


def save_raw_data(domain: str, topics: List[Dict], classified: List[Dict], output_dir: str):
    """Save raw topic data and classified data to JSONL files."""
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