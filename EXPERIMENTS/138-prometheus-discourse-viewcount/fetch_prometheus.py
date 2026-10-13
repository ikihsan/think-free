#!/usr/bin/env python3
"""
Fetch topics from discuss.prometheus.io Discourse API.
"""

import json
import sys
import time
import urllib.request
import urllib.error
from typing import Any

BASE_URL = "https://discuss.prometheus.io"
CATEGORIES = [
    "general",
    "prometheus",
    "promql",
    "exporters",
]

# Category name to slug mapping (may need adjustment after checking actual slugs)
CATEGORY_SLUGS = {
    "general": "general",
    "prometheus": "prometheus",
    "promql": "promql",
    "exporters": "exporters",
}

TOPICS_PER_CATEGORY = 75
REQUEST_DELAY = 1.0


def fetch_category(slug: str, limit: int = 100):
    """Fetch topics from a category, handling pagination."""
    topics = []
    page = 0

    while len(topics) < limit:
        url = f"{BASE_URL}/c/{slug}.json?page={page}&order=activity"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "think-free/1.0"})
            with urllib.request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            print(f"HTTP error fetching {url}: {e.code}")
            break
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            break

        topic_list = data.get("topic_list", {})
        topics_page = topic_list.get("topics", [])

        if not topics_page:
            break

        for topic in topics_page:
            # Only keep fields we need
            topics.append({
                "id": topic.get("id"),
                "title": topic.get("title"),
                "slug": topic.get("slug"),
                "posts_count": topic.get("posts_count", 0),
                "reply_count": topic.get("reply_count", 0),
                "view_count": topic.get("views", 0),
                "created_at": topic.get("created_at"),
                "last_posted_at": topic.get("last_posted_at"),
                "category_id": topic.get("category_id"),
                "tags": topic.get("tags", []),
                "excerpt": topic.get("excerpt", ""),
            })

        if len(topics) >= limit:
            topics = topics[:limit]
            break

        page += 1
        time.sleep(REQUEST_DELAY)

    return topics


def fetch_topic_details(topic_id: int):
    """Fetch full topic details including first post body."""
    url = f"{BASE_URL}/t/{topic_id}.json"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "think-free/1.0"})
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))

        post_stream = data.get("post_stream", {})
        posts = post_stream.get("posts", [])
        if posts:
            first_post = posts[0]
            return {
                "raw": first_post.get("raw", ""),
                "cooked": first_post.get("cooked", ""),
            }
    except Exception as e:
        print(f"Error fetching topic {topic_id}: {e}")

    return {"raw": "", "cooked": ""}


def main():
    all_topics = []

    for cat_name in CATEGORIES:
        slug = CATEGORY_SLUGS.get(cat_name, cat_name)
        print(f"Fetching category: {cat_name} (slug: {slug})")
        topics = fetch_category(slug, TOPICS_PER_CATEGORY)

        # Enrich with first post body
        for topic in topics:
            topic["category"] = cat_name
            details = fetch_topic_details(topic["id"])
            topic.update(details)
            time.sleep(REQUEST_DELAY)

        all_topics.extend(topics)
        print(f"  Fetched {len(topics)} topics")
        time.sleep(REQUEST_DELAY)

    # Save raw data
    output_path = "data_prometheus.jsonl"
    with open(output_path, "w") as f:
        for topic in all_topics:
            f.write(json.dumps(topic) + "\n")

    print(f"\nTotal topics fetched: {len(all_topics)}")
    print(f"Saved to: {output_path}")

    # Quick stats
    vc_positive = sum(1 for t in all_topics if t.get("view_count", 0) > 0)
    print(f"View count > 0: {vc_positive}/{len(all_topics)} = {vc_positive/len(all_topics)*100:.1f}%")


if __name__ == "__main__":
    main()