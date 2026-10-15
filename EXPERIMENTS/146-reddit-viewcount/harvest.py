#!/usr/bin/env python3
"""
E146 — Harvest Reddit technical community posts for view-count experiment.
"""

import json
import os
import re
import sys
import time
import urllib.request
import urllib.parse

# Subreddits to sample (technical communities)
SUBREDDITS = [
    "programming", "python", "javascript", "ruby", "go", "rust",
    "cpp", "java", "typescript", "webdev"
]

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


def fetch_reddit_hot(subreddit, limit=100):
    """Fetch hot posts from a subreddit via the public JSON API."""
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())
            posts = []
            for child in data.get("data", {}).get("children", []):
                post = child["data"]
                posts.append({
                    "title": post.get("title", ""),
                    "score": post.get("score", 0),    # upvotes
                    "num_comments": post.get("num_comments", 0),
                    "id": post.get("id", ""),
                    "subreddit": subreddit,
                })
            return posts
    except Exception as e:
        print(f"  Error fetching r/{subreddit}: {e}")
        return []


def main():
    all_posts = []
    for subreddit in SUBREDDITS:
        print(f"Fetching r/{subreddit}...")
        posts = fetch_reddit_hot(subreddit, limit=100)
        for p in posts:
            p["subreddit"] = subreddit
        all_posts.extend(posts)
        print(f"  Got {len(posts)} posts")
        time.sleep(1)  # 60 req/hr unauthenticated budget

    # Write raw harvest
    out_path = "EXPERIMENTS/146-reddit-viewcount/raw_data.jsonl"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        for p in all_posts:
            f.write(json.dumps(p) + "\n")

    print(f"\nWrote {len(all_posts)} posts to {out_path}")
    return len(all_posts)


if __name__ == "__main__":
    n = main()
    print(f"Harvested {n} total posts")