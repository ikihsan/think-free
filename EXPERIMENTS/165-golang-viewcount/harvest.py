#!/usr/bin/env python3
"""
Harvest Go packages from pkg.go.dev search results.
Extracts: package path, synopsis, imported_by count.
"""

import json
import re
import time
import sys
from urllib.parse import quote_plus
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

SEARCH_QUERIES = [
    "framework",
    "client",
    "wrapper",
    "middleware",
    "plugin",
    "driver",
    "adapter",
    "library",
    "tool",
    "util",
    "sdk",
    "api",
    "",  # random/empty query
    "standard library",
]

BASE_URL = "https://pkg.go.dev/search"
LIMIT = 20
DELAY = 1.0  # seconds between requests


def fetch_search_page(query, limit=LIMIT):
    # type: (str, int) -> str
    """Fetch a single search results page."""
    q = quote_plus(query) if query else ""
    url = f"{BASE_URL}?q={q}&limit={limit}&m=package"
    req = Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; GoViewCountBot/1.0; +https://github.com/ikihsan/think-free)",
        "Accept": "text/html",
    })
    try:
        with urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8")
    except (URLError, HTTPError) as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return ""


def parse_search_results(html, query):
    # type: (str, str) -> list
    """Parse package info from search results HTML."""
    packages = []

    # Split by SearchSnippet divs - each contains one package result
    snippet_pattern = r'<div class="SearchSnippet"[^>]*>(.*?)</div>\s*(?=<div class="SearchSnippet"|$)'
    snippets = re.findall(snippet_pattern, html, re.DOTALL)

    for snippet in snippets:
        # Extract package path from the search result anchor
        path_match = re.search(
            r'<a href="(/[^"]+)" data-gtmc="search result" data-gtmv="\d+"',
            snippet
        )
        if not path_match:
            continue
        path = path_match.group(1).lstrip("/")

        # Extract synopsis
        synopsis_match = re.search(
            r'<p class="SearchSnippet-synopsis" data-test-id="snippet-synopsis">\s*([^<]+)\s*</p>',
            snippet
        )
        synopsis = synopsis_match.group(1).strip() if synopsis_match else ""

        # Extract imported by count
        imported_match = re.search(
            r'Imported by\s*</span>\s*<strong>([^<]+)</strong>',
            snippet
        )
        imported_by = 0
        if imported_match:
            count_str = imported_match.group(1).strip().replace(",", "")
            try:
                imported_by = int(count_str)
            except ValueError:
                imported_by = 0

        # Also check for "Imported by N" without strong tag
        if imported_by == 0:
            imported_match2 = re.search(
                r'>Imported by\s+([\d,]+)<',
                snippet
            )
            if imported_match2:
                count_str = imported_match2.group(1).replace(",", "")
                try:
                    imported_by = int(count_str)
                except ValueError:
                    pass

        packages.append({
            "path": path,
            "synopsis": synopsis,
            "imported_by": imported_by,
            "query": query,
        })

    return packages


def harvest_all():
    # type: () -> list
    """Harvest packages from all search queries."""
    all_packages = []
    seen_paths = set()

    for query in SEARCH_QUERIES:
        print(f"Fetching query: '{query or '(empty)'}'...")
        html = fetch_search_page(query)
        if not html:
            print(f"  Failed to fetch")
            continue

        packages = parse_search_results(html, query)
        print(f"  Found {len(packages)} packages")

        # Deduplicate by path
        new_packages = []
        for p in packages:
            if p["path"] not in seen_paths:
                seen_paths.add(p["path"])
                p["query"] = query
                new_packages.append(p)

        all_packages.extend(new_packages)
        print(f"  Added {len(new_packages)} new packages (total: {len(all_packages)})")

        time.sleep(DELAY)

    return all_packages


def main():
    print("Starting Go package harvest...")
    packages = harvest_all()
    print(f"Total unique packages: {len(packages)}")

    # Save raw harvest
    with open("raw_harvest.json", "w") as f:
        json.dump(packages, f, indent=2)

    # Print summary
    with_imported = [p for p in packages if p["imported_by"] > 0]
    print(f"Packages with imported_by > 0: {len(with_imported)} / {len(packages)}")
    if with_imported:
        imported_vals = [p["imported_by"] for p in with_imported]
        print(f"Imported by range: {min(imported_vals)} - {max(imported_vals)}")
        print(f"Median imported by: {sorted(imported_vals)[len(imported_vals)//2]}")


if __name__ == "__main__":
    main()