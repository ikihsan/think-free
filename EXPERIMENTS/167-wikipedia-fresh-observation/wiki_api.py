#!/usr/bin/env python3
"""Wikipedia API utilities for view-count experiments. Stdlib only."""

import urllib.request
import urllib.error
import urllib.parse
import json
import time
import sys
from typing import Dict, List, Any, Optional


WIKI_API = "https://en.wikipedia.org/w/api.php"
PAGEVIEWS_API = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/all-access/user"
STUB_CATEGORY = "Category:All_stub_articles"
RATE_LIMIT_DELAY = 0.3
TIMEOUT = 30
MAX_RETRIES = 3


def fetch_json(url: str, allow_404: bool = False) -> Any:
    """Fetch JSON from URL with retries and rate limit handling."""
    for attempt in range(MAX_RETRIES):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "think-free/167 (research)"})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                if resp.status == 429:
                    retry_after = int(resp.headers.get("Retry-After", "60"))
                    time.sleep(retry_after)
                    continue
                return json.load(resp)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                retry_after = int(e.headers.get("Retry-After", "60"))
                print(f"  Rate limited, waiting {retry_after}s...", file=sys.stderr)
                time.sleep(retry_after)
                continue
            if e.code == 404 and allow_404:
                return None
            if attempt == MAX_RETRIES - 1:
                raise
            time.sleep(2 ** attempt)
        except (urllib.error.URLError, json.JSONDecodeError, TimeoutError) as e:
            if attempt == MAX_RETRIES - 1:
                raise
            time.sleep(2 ** attempt)
    return None


def get_stub_titles(limit: int) -> List[str]:
    """Fetch stub article titles from Category:All_stub_articles."""
    titles = []
    cmcontinue = None

    while len(titles) < limit:
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": STUB_CATEGORY,
            "cmnamespace": "0",
            "cmlimit": "500",
            "format": "json",
        }
        if cmcontinue:
            params["cmcontinue"] = cmcontinue

        url = WIKI_API + "?" + urllib.parse.urlencode(params)
        data = fetch_json(url)

        if not data or "query" not in data:
            break

        for member in data["query"]["categorymembers"]:
            title = member["title"]
            if not title.startswith(("Category:", "Template:", "Wikipedia:", "Portal:", "Draft:", "File:", "Help:", "Module:")):
                titles.append(title)
                if len(titles) >= limit:
                    break

        cmcontinue = data.get("continue", {}).get("cmcontinue")
        if not cmcontinue:
            break
        time.sleep(RATE_LIMIT_DELAY)

    return titles[:limit]


def get_random_titles(limit: int) -> List[str]:
    """Fetch random main-namespace article titles."""
    titles = []
    while len(titles) < limit:
        rnlimit = min(50, limit - len(titles))
        params = {
            "action": "query",
            "list": "random",
            "rnnamespace": "0",
            "rnlimit": str(rnlimit),
            "format": "json",
        }
        url = WIKI_API + "?" + urllib.parse.urlencode(params)
        data = fetch_json(url)

        if not data or "query" not in data:
            break

        for page in data["query"]["random"]:
            title = page["title"]
            if not title.startswith(("Category:", "Template:", "Wikipedia:", "Portal:", "Draft:", "File:", "Help:", "Module:")):
                titles.append(title)

        time.sleep(RATE_LIMIT_DELAY)

    return titles[:limit]


def get_article_info(titles: List[str]) -> Dict[str, Dict]:
    """Fetch article length (bytes) for titles."""
    info = {}
    for i in range(0, len(titles), 50):
        batch = titles[i:i+50]
        params = {
            "action": "query",
            "titles": "|".join(batch),
            "prop": "info",
            "inprop": "length",
            "format": "json",
        }
        url = WIKI_API + "?" + urllib.parse.urlencode(params)
        data = fetch_json(url)

        if data and "query" in data and "pages" in data["query"]:
            for page in data["query"]["pages"].values():
                if "missing" not in page:
                    info[page["title"]] = {
                        "length": page.get("length", 0),
                        "pageid": page.get("pageid"),
                    }
        time.sleep(RATE_LIMIT_DELAY)

    return info


def get_pageviews(title: str, days_back: int) -> Optional[int]:
    """Fetch total pageviews for last N days. Returns None if not found."""
    from datetime import datetime, timezone, timedelta

    end_date = datetime.now(timezone.utc) - timedelta(days=1)
    start_date = end_date - timedelta(days=days_back - 1)

    start_str = start_date.strftime("%Y%m%d")
    end_str = end_date.strftime("%Y%m%d")

    encoded_title = urllib.parse.quote(title)
    url = f"{PAGEVIEWS_API}/{encoded_title}/daily/{start_str}/{end_str}"

    data = fetch_json(url, allow_404=True)
    if not data or "items" not in data:
        return None

    total = 0
    for item in data["items"]:
        total += item.get("views", 0)
    return total