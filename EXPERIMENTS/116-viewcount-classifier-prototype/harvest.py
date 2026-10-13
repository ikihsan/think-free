"""Pool collection for the E116 view-count classifier prototype.

Split out of `classify.py` at the repository's 300-line cap. This module
owns the Hex.pm API harvest: the search queries and the two fetch loops
that build the classified pool.
"""

import json
import urllib.request
import urllib.error


def collect_pool():
    """Collect the classifier pool from the Hex.pm API.

    Returns the deduplicated package list in harvest order, which is the
    order the classifier and every downstream count depend on.
    """
    all_packages = []
    seen_names = set()

    NEED_QUERIES = [
        "web", "auth", "database", "cache", "test", "api", "framework",
        "cli", "migration",
    ]
    RANDOM_QUERIES = ["", "elixir", "erlang"]

    print("  Fetching need-related via search queries...")
    for query in NEED_QUERIES:
        url = f"https://hex.pm/api/packages?search={query}&sort=downloads&page=1"
        req = urllib.request.Request(url, headers={"User-Agent": "E116-Classifier/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read().decode("utf-8")
                parsed = json.loads(data)
                results = parsed if isinstance(parsed, list) else (
                    parsed.get("data") or parsed.get("packages") or []
                )
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
        except Exception as e:
            print(f"  Query '{query}' failed: {e}")
            continue
        if len(all_packages) >= 200:
            break

    print("  Fetching random from default listing...")
    if len(all_packages) < 200:
        url = "https://hex.pm/api/packages?page=1"
        req = urllib.request.Request(url, headers={"User-Agent": "E116-Classifier/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read().decode("utf-8")
                parsed = json.loads(data)
                results = parsed if isinstance(parsed, list) else (
                    parsed.get("data") or parsed.get("packages") or []
                )
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
        except Exception as e:
            print(f"  Random fetch failed: {e}")
    return all_packages
