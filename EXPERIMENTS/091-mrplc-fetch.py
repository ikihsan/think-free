#!/usr/bin/env python3
"""
E091 Discrimination Test — network fetch: URL -> BeautifulSoup.

Split out of `091-discrimination-harness.py` at the 300-line cap. This half is
the only part of the harness that touches the network, which is what lets the
parsers and the instrument be exercised offline against recorded pages.

MrPLC pagination: page 1 carries no page parameter; pages 2+ use ?page=x.
"""

import sys
from typing import Any, List, Optional

import requests
from bs4 import BeautifulSoup


def fetch_mrplc_forum_page(forum_url: str, page_num: int = 1) -> Optional[BeautifulSoup]:
    """Fetch a MrPLC forum page and return BeautifulSoup object.

    Args:
        forum_url: Base URL of the forum (e.g.,
            'https://www.mrplc.com/forums/forum/15-mitsubishi/')
        page_num: Page number (1 = first page)

    Returns:
        BeautifulSoup object if successful, None on failure
    """
    # MrPLC pagination: page 1 has no page parameter, pages 2+ use ?page=x
    if page_num == 1:
        url = forum_url
    else:
        # Handle URL with or trailing slash
        base = forum_url.rstrip('/')
        if '?page=' in base:
            url = f"{base}&page={page_num}"
        else:
            url = f"{base}?page={page_num}"

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        resp = requests.get(url, timeout=15, headers=headers)
        if resp.status_code != 200:
            print(f"  WARN: Got status {resp.status_code} for {url}", file=sys.stderr)
            return None
        return BeautifulSoup(resp.text, "html.parser")
    except Exception as e:
        print(f"  ERROR fetching {url}: {e}", file=sys.stderr)
        return None


def fetch_forum_pages(forum_url: str, max_pages: int = 3) -> List[Any]:
    """Fetch multiple pages of a MrPLC forum listing.

    Args:
        forum_url: Base URL of the forum (e.g.,
            'https://www.mrplc.com/forums/forum/15-mitsubishi/')
        max_pages: Maximum number of pages to fetch (1 = first page only)

    Returns:
        List of BeautifulSoup objects, one per page fetched
    """
    pages = []
    for page_num in range(1, max_pages + 1):
        soup = fetch_mrplc_forum_page(forum_url, page_num=page_num)
        if soup is not None:
            pages.append(soup)
        else:
            # If a page fails, stop fetching further pages
            print(f"  STOPPING: Page {page_num} fetch failed, stopping pagination", file=sys.stderr)
            break
    return pages
