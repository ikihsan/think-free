#!/usr/bin/env python3
"""Targeted search for confusion evidence using GitHub global search and Stack Overflow.

Focuses on top pairs by volume with specific confusion queries.
"""
from __future__ import print_function

import json
import os
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
os.makedirs(RAW, exist_ok=True)

# Top 10 pairs by mutation download volume (from E064)
TOP_PAIRS = [
    {"eco": "pypi", "seed": "jinja2", "mutation": "jinja2-cli", "downloads": 11164368},
    {"eco": "pypi", "seed": "click", "mutation": "django-click", "downloads": 1706868},
    {"eco": "pypi", "seed": "typer", "mutation": "django-typer", "downloads": 1638528},
    {"eco": "pypi", "seed": "typer", "mutation": "async-typer", "downloads": 646800},
    {"eco": "pypi", "seed": "typer", "mutation": "typer-cli", "downloads": 485772},
    {"eco": "npm", "seed": "chalk", "mutation": "chalk-cli", "downloads": 430003},
    {"eco": "pypi", "seed": "rich", "mutation": "rich-cli", "downloads": 265656},
    {"eco": "gem", "seed": "redis", "mutation": "async-redis", "downloads": 863051},
    {"eco": "gem", "seed": "rspec", "mutation": "async-rspec", "downloads": 560528},
    {"eco": "pypi", "seed": "sqlalchemy", "mutation": "sqlalchemy-utils", "downloads": None},
]

# Confusion query patterns
CONFUSION_QUERIES = [
    '"accidentally installed {mutation}"',
    '"meant to install {mutation}"',
    '"typo {mutation}"',
    '"wrong package {mutation}"',
    '"confused {seed} with {mutation}"',
    '"{mutation} instead of {seed}"',
    '"{seed} instead of {mutation}"',
    '"installed {mutation} by mistake"',
]

def gh_search_issues(query, max_pages=2):
    """GitHub global issue search."""
    results = []
    for page in range(1, max_pages + 1):
        q = urllib.parse.quote(query)
        url = f"https://api.github.com/search/issues?q={q}&per_page=100&page={page}"
        req = urllib.request.Request(url)
        req.add_header("Accept", "application/vnd.github+json")
        req.add_header("User-Agent", "E069-false-accept-confusion")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                remaining = resp.headers.get("X-RateLimit-Remaining")
                if remaining:
                    print(f"  GH search rate limit: {remaining}")
                body = resp.read().decode("utf-8", "replace")
                data = json.loads(body)
                items = data.get("items", [])
                if not items:
                    break
                results.extend(items)
                if len(items) < 100:
                    break
                time.sleep(6)  # 10 req/min
        except urllib.error.HTTPError as e:
            print(f"  GH search failed: {e.code}")
            if e.code == 403:
                print("  Rate limited, waiting 60s...")
                time.sleep(60)
            break
        except Exception as e:
            print(f"  GH search error: {e}")
            break
    return results


def gh_search_code(query, max_pages=1):
    """GitHub global code search (for config files)."""
    results = []
    for page in range(1, max_pages + 1):
        q = urllib.parse.quote(query)
        url = f"https://api.github.com/search/code?q={q}&per_page=100&page={page}"
        req = urllib.request.Request(url)
        req.add_header("Accept", "application/vnd.github+json")
        req.add_header("User-Agent", "E069-false-accept-confusion")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                remaining = resp.headers.get("X-RateLimit-Remaining")
                if remaining:
                    print(f"  GH code search rate limit: {remaining}")
                body = resp.read().decode("utf-8", "replace")
                data = json.loads(body)
                items = data.get("items", [])
                if not items:
                    break
                results.extend(items)
                if len(items) < 100:
                    break
                time.sleep(6)
        except Exception as e:
            print(f"  GH code search error: {e}")
            break
    return results


def se_search(tagged, query, pagesize=50):
    """Stack Exchange search."""
    url = (
        f"https://api.stackexchange.com/2.3/search/advanced?"
        f"order=desc&sort=relevance&site=stackoverflow"
        f"&tagged={urllib.parse.quote(tagged)}&q={urllib.parse.quote(query)}"
        f"&pagesize={pagesize}"
    )
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            body = resp.read().decode("utf-8", "replace")
            return json.loads(body).get("items", [])
    except Exception as e:
        print(f"  SE search error: {e}")
        return []


def main():
    all_results = []

    for i, pair in enumerate(TOP_PAIRS):
        print(f"\n[{i+1}/{len(TOP_PAIRS)}] {pair['eco']}: {pair['seed']} -> {pair['mutation']} ({pair['downloads']} downloads/yr)")
        pair_results = {"pair": pair, "issue_hits": [], "code_hits": [], "so_hits": []}

        # Map ecosystem to SO tag
        tag_map = {"pypi": "python", "npm": "javascript", "crates": "rust", "gem": "ruby"}
        so_tag = tag_map.get(pair["eco"], "")

        # 1. GitHub issue search with confusion queries
        for q_template in CONFUSION_QUERIES:
            query = q_template.format(seed=pair["seed"], mutation=pair["mutation"])
            print(f"  GH issues: {query}")
            hits = gh_search_issues(query, max_pages=1)
            for h in hits:
                pair_results["issue_hits"].append({
                    "query": query,
                    "title": h.get("title", ""),
                    "body": (h.get("body") or "")[:500],
                    "url": h.get("html_url", ""),
                    "repo": h.get("repository_url", "").replace("https://api.github.com/repos/", ""),
                    "number": h.get("number"),
                })
            print(f"    Found {len(hits)} issues")
            if len(hits) > 0:
                break  # Found something, no need more queries for this pair
            time.sleep(6)

        # 2. GitHub code search for config files with mutation name
        # Look for mutation in requirements.txt, package.json, Cargo.toml, Gemfile
        config_patterns = [
            f'"{pair["mutation"]}" filename:requirements.txt',
            f'"{pair["mutation"]}" filename:package.json',
            f'"{pair["mutation"]}" filename:Cargo.toml',
            f'"{pair["mutation"]}" filename:Gemfile',
            f'"{pair["mutation"]}" filename:pyproject.toml',
            f'"{pair["mutation"]}" filename:setup.py',
        ]
        for pattern in config_patterns:
            print(f"  GH code: {pattern}")
            hits = gh_search_code(pattern, max_pages=1)
            for h in hits:
                pair_results["code_hits"].append({
                    "pattern": pattern,
                    "repo": h.get("repository", {}).get("full_name", ""),
                    "path": h.get("path", ""),
                    "url": h.get("html_url", ""),
                })
            print(f"    Found {len(hits)} files")
            if len(hits) > 0:
                break
            time.sleep(6)

        # 3. Stack Overflow search
        if so_tag:
            # Search for both names together
            query = f"{pair['seed']} {pair['mutation']}"
            print(f"  SO [{so_tag}]: {query}")
            hits = se_search(so_tag, query)
            for h in hits:
                pair_results["so_hits"].append({
                    "query": query,
                    "title": h.get("title", ""),
                    "body": (h.get("body") or "")[:500] if "body" in h else "",
                    "url": h.get("link", ""),
                    "question_id": h.get("question_id"),
                    "tags": h.get("tags", []),
                })
            print(f"    Found {len(hits)} questions")
            time.sleep(1)

            # Search for confusion phrases
            for phrase in ["accidentally installed", "meant to install", "typo", "wrong package"]:
                query2 = f"{pair['mutation']} {phrase}"
                hits2 = se_search(so_tag, query2)
                for h in hits2:
                    pair_results["so_hits"].append({
                        "query": query2,
                        "title": h.get("title", ""),
                        "body": (h.get("body") or "")[:500],
                        "url": h.get("link", ""),
                        "question_id": h.get("question_id"),
                        "tags": h.get("tags", []),
                    })
                time.sleep(1)

        all_results.append(pair_results)

    # Negative controls
    print("\n--- Negative controls ---")
    NEG_CONTROLS = [
        {"seed": "requests", "other": "urllib3", "tag": "python"},
        {"seed": "click", "other": "argparse", "tag": "python"},
        {"seed": "chalk", "other": "colors", "tag": "javascript"},
    ]
    for ctrl in NEG_CONTROLS:
        print(f"  {ctrl['seed']} vs {ctrl['other']}")
        ctrl_results = {"pair": ctrl, "issue_hits": [], "so_hits": []}
        # GH issues
        for q_template in CONFUSION_QUERIES[:3]:
            query = q_template.format(seed=ctrl["seed"], mutation=ctrl["other"])
            hits = gh_search_issues(query, max_pages=1)
            for h in hits:
                ctrl_results["issue_hits"].append({
                    "query": query,
                    "title": h.get("title", ""),
                    "body": (h.get("body") or "")[:500],
                    "url": h.get("html_url", ""),
                })
            print(f"    GH issues '{query}': {len(hits)}")
            time.sleep(6)
            if hits:
                break
        # SO
        query = f"{ctrl['seed']} {ctrl['other']}"
        hits = se_search(ctrl["tag"], query)
        for h in hits:
            ctrl_results["so_hits"].append({
                "query": query,
                "title": h.get("title", ""),
                "body": (h.get("body") or "")[:500] if "body" in h else "",
                "url": h.get("link", ""),
            })
        print(f"    SO: {len(hits)}")
        time.sleep(1)
        all_results.append({"negative_control": True, **ctrl_results})

    # Save
    out_path = os.path.join(RAW, "search-results.jsonl")
    with open(out_path, "w") as f:
        for r in all_results:
            f.write(json.dumps(r) + "\n")
    print(f"\nSaved to {out_path}")


if __name__ == "__main__":
    main()