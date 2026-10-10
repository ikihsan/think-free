#!/usr/bin/env python3
"""
E091 — Harvest import-error reports from Stack Overflow, GitHub issues, and library trackers.
"""

import json
import os
import time
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
RAW = HERE / "raw" / "api"
RAW.mkdir(parents=True, exist_ok=True)

# Stack Overflow queries — fixed before first fetch
SE_QUERIES = [
    ("stackoverflow", 'python "ImportError" "No module named"', "core"),
    ("stackoverflow", 'python "ModuleNotFoundError" "No module named"', "core"),
    ("stackoverflow", 'python "ImportError" "what package"', "explicit"),
    ("stackoverflow", 'python "ModuleNotFoundError" "what to install"', "explicit"),
    ("stackoverflow", 'python "pip install" "ImportError"', "pip_then_import"),
    ("stackoverflow", 'python "import" "failed" "what package"', "generic"),
    ("stackoverflow", 'python "cannot import" "pip install"', "inverse"),
    ("stackoverflow", 'python "No module named" "pip"', "module_plus_pip"),
]

# GitHub Issues queries — fixed before first fetch
GH_QUERIES = [
    ('"ImportError" "No module named" language:python type:issue', "core"),
    ('"ModuleNotFoundError" "No module named" language:python type:issue', "core"),
    ('"import error" "what package" language:python type:issue', "explicit"),
    ('"pip install" "import failed" language:python type:issue', "pip_then_import"),
    ('"cannot import" "pip install" language:python type:issue', "inverse"),
]

# Library tracker repos
LIBRARY_REPOS = [
    "python/cpython",
    "numpy/numpy",
    "pandas-dev/pandas",
    "psf/requests",
    "django/django",
    "pallets/flask",
    "sqlalchemy/sqlalchemy",
    "pytest-dev/pytest",
]


def get(url, pause):
    """Fetch URL with rate-limit pause."""
    time.sleep(pause)
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "E091-import-error-population/1.0"}
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def stackexchange(site, query, pages=2):
    """Fetch all items for one Stack Overflow query."""
    items = []
    for page in range(1, pages + 1):
        params = urllib.parse.urlencode({
            "q": query,
            "site": site,
            "pagesize": 25,
            "page": page,
            "filter": "withbody",
            "tagged": "python",
        })
        url = "https://api.stackexchange.com/2.3/search/advanced?" + params
        try:
            d = get(url, 7.0)  # 7s pause = ~8 req/min, well under 300/day unauthenticated
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print(f"  Rate limited, backing off...")
                time.sleep(60)
                d = get(url, 7.0)
            else:
                raise
        items.extend(d.get("items", []))
        if d.get("backoff"):
            time.sleep(int(d["backoff"]) + 1)
        if not d.get("has_more"):
            break
    return items


def github_search(query, pages=2):
    """Fetch all items for one GitHub search query."""
    items = []
    for page in range(1, pages + 1):
        params = urllib.parse.urlencode({
            "q": query,
            "per_page": 25,
            "page": page,
        })
        url = "https://api.github.com/search/issues?" + params
        try:
            d = get(url, 7.0)  # 7s pause = ~8 req/min, under 10/min unauthenticated
        except urllib.error.HTTPError as e:
            if e.code == 403:
                # Check rate limit
                print(f"  GitHub rate limited (403), backing off...")
                time.sleep(60)
                d = get(url, 7.0)
            else:
                raise
        items.extend(d.get("items", []))
        if len(d.get("items", [])) < 25:
            break
    return items


def github_repo_issues(repo, pages=2):
    """Fetch issues from a specific repo mentioning ImportError/ModuleNotFoundError."""
    items = []
    for page in range(1, pages + 1):
        params = urllib.parse.urlencode({
            "q": 'repo:' + repo + ' ("ImportError" OR "ModuleNotFoundError") type:issue',
            "per_page": 25,
            "page": page,
        })
        url = "https://api.github.com/search/issues?" + params
        try:
            d = get(url, 7.0)
        except urllib.error.HTTPError as e:
            if e.code == 403:
                print(f"  GitHub rate limited on {repo}, backing off...")
                time.sleep(60)
                d = get(url, 7.0)
            else:
                raise
        items.extend(d.get("items", []))
        if len(d.get("items", [])) < 25:
            break
    return items


def main():
    manifest = []

    # Stack Overflow
    print("\n=== Stack Overflow Harvest ===")
    for site, query, klass in SE_QUERIES:
        print(f"  Query: {query[:60]}...")
        items = stackexchange(site, query, pages=2)  # 2 pages * 25 = 50 per query
        slug = "se-" + "".join(c if c.isalnum() else "-" for c in query).strip("-")[:80]
        path = RAW / f"{slug}.json"
        with open(path, "w") as f:
            json.dump({"site": site, "query": query, "class": klass, "items": items}, f, indent=1)
        manifest.append({
            "venue": "stackexchange",
            "site": site,
            "query": query,
            "class": klass,
            "n": len(items),
            "file": path.name,
        })
        print(f"    -> {len(items)} items")

    # GitHub Issues (general search)
    print("\n=== GitHub Issues Harvest ===")
    for query, klass in GH_QUERIES:
        print(f"  Query: {query[:60]}...")
        items = github_search(query, pages=2)
        slug = "gh-" + "".join(c if c.isalnum() else "-" for c in query).strip("-")[:80]
        path = RAW / f"{slug}.json"
        with open(path, "w") as f:
            json.dump({"query": query, "class": klass, "items": items}, f, indent=1)
        manifest.append({
            "venue": "github",
            "query": query,
            "class": klass,
            "n": len(items),
            "file": path.name,
        })
        print(f"    -> {len(items)} items")

    # Library trackers
    print("\n=== Library Tracker Harvest ===")
    for repo in LIBRARY_REPOS:
        print(f"  Repo: {repo}...")
        items = github_repo_issues(repo, pages=2)
        slug = "repo-" + repo.replace("/", "-")
        path = RAW / f"{slug}.json"
        with open(path, "w") as f:
            json.dump({"repo": repo, "items": items}, f, indent=1)
        manifest.append({
            "venue": "github",
            "repo": repo,
            "query": '("ImportError" OR "ModuleNotFoundError") type:issue',
            "class": "library_tracker",
            "n": len(items),
            "file": path.name,
        })
        print(f"    -> {len(items)} items")

    # Write manifest
    manifest_path = RAW / "manifest.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=1)
    print(f"\nWrote manifest: {manifest_path}")
    print(f"Total queries: {len(manifest)}")
    print(f"Total items fetched: {sum(m['n'] for m in manifest)}")


if __name__ == "__main__":
    main()