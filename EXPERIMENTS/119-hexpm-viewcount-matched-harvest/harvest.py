"""Pool collection for the E119 Hex.pm matched-harvest experiment.

Split out of `classify.py` at the repository's 300-line cap. This module
owns the two Hex.pm API fetchers and the search queries that build the
matched-harvest pool.
"""

import json


def fetch_hexpm_packages(search_query, page=1, sort="downloads"):
    """Fetch packages from Hex.pm API."""
    import urllib.request
    url = f"https://hex.pm/api/packages?search={urllib.parse.quote(search_query)}&sort={sort}&page={page}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "E119-MatchedHarvest/1.0", "Accept": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read().decode("utf-8")
            return json.loads(data)
    except Exception as e:
        print(f"  Hex.pm search '{search_query}' page {page} failed: {e}")
        return None


def fetch_hexpm_random(page=1):
    """Fetch random packages from Hex.pm default listing."""
    import urllib.request
    url = f"https://hex.pm/api/packages?page={page}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "E119-MatchedHarvest/1.0", "Accept": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read().decode("utf-8")
            return json.loads(data)
    except Exception as e:
        print(f"  Hex.pm random page {page} failed: {e}")
        return None


def collect_pool():
    """Collect the matched-harvest pool from the Hex.pm API.

    Returns the deduplicated package list in harvest order, which is the
    order the classifier and every downstream count depend on.
    """
    all_packages = []
    seen_names = set()

    # Define need queries and random queries for Hex.pm
    NEED_QUERIES = [
        "ecto", "phoenix", "auth", "database", "cache", "api", "web",
        "testing", "cli", "migration",
    ]
    RANDOM_QUERIES = [""]  # empty query = most popular/random

    print("  Fetching need-related via search queries...")
    for query in NEED_QUERIES:
        page = 1
        while True:
            data = fetch_hexpm_packages(query, page=page)
            if data is None:
                break
            results = data if isinstance(data, list) else data.get("data", []) or []
            for pkg in results:
                name = pkg.get("name", "")
                if name and name not in seen_names:
                    seen_names.add(name)
                    desc = pkg.get("description", "")
                    recent = pkg.get("downloads", {}).get("recent", 0) or 0
                    all_packages.append({
                        "name": name,
                        "description": desc,
                        "recent_downloads": recent,
                        "_source": "need_query",
                        "_query": query,
                    })
                    if len(all_packages) >= 200:
                        break
            if len(all_packages) >= 200:
                break
            page += 1

        if len(all_packages) >= 200:
            break

    print("  Fetching random from default listing...")
    if len(all_packages) < 200:
        page = 1
        while True:
            data = fetch_hexpm_random(page=page)
            if data is None:
                break
            results = data if isinstance(data, list) else data.get("data", []) or []
            for pkg in results:
                name = pkg.get("name", "")
                if name and name not in seen_names:
                    seen_names.add(name)
                    desc = pkg.get("description", "")
                    recent = pkg.get("downloads", {}).get("recent", 0) or 0
                    all_packages.append({
                        "name": name,
                        "description": desc,
                        "recent_downloads": recent,
                        "_source": "random",
                    })
                    if len(all_packages) >= 200:
                        break
            if len(all_packages) >= 200:
                break
            page += 1
    return all_packages
