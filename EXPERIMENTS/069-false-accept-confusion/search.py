#!/usr/bin/env python3
"""Search for confusion evidence for the 24 seed-mutation pairs.

Uses public APIs only: GitHub REST (unauthenticated), Stack Exchange API.
Rate limits respected.
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

# The 24 residual pairs from E064
PAIRS = [
    {"eco": "crates", "seed": "clap", "mutation": "clap-utils", "seed_url": "https://github.com/clap-rs/clap", "mut_url": "https://github.com/tyrchen/clap-utils"},
    {"eco": "crates", "seed": "clap", "mutation": "fast-clap", "seed_url": "https://github.com/clap-rs/clap", "mut_url": "https://github.com/frol/clap"},
    {"eco": "crates", "seed": "regex", "mutation": "regex-cli", "seed_url": "https://github.com/rust-lang/regex", "mut_url": "https://github.com/rust-lang/regex"},
    {"eco": "crates", "seed": "regex", "mutation": "regex-rs", "seed_url": "https://github.com/rust-lang/regex", "mut_url": "https://github.com/newsboat/newsboat"},
    {"eco": "crates", "seed": "regex", "mutation": "simple-regex", "seed_url": "https://github.com/rust-lang/regex", "mut_url": "https://github.com/Animemchik/simple-regex"},
    {"eco": "crates", "seed": "tokio", "mutation": "tokio-go", "seed_url": "https://github.com/tokio-rs/tokio", "mut_url": "https://github.com/zhchang/tokio-go"},
    {"eco": "gem", "seed": "redis", "mutation": "async-redis", "seed_url": "https://github.com/redis/redis-rb", "mut_url": "https://github.com/socketry/async-redis"},
    {"eco": "gem", "seed": "rspec", "mutation": "async-rspec", "seed_url": "https://github.com/rspec/rspec", "mut_url": "https://github.com/socketry/async-rspec"},
    {"eco": "npm", "seed": "chalk", "mutation": "chalk-cli", "seed_url": "https://github.com/chalk/chalk", "mut_url": "https://github.com/chalk/chalk-cli"},
    {"eco": "npm", "seed": "winston", "mutation": "winston-cli", "seed_url": "https://github.com/winstonjs/winston", "mut_url": "https://github.com/vhvostenkov/AGENT_G"},
    {"eco": "pypi", "seed": "typer", "mutation": "async-typer", "seed_url": "https://github.com/fastapi/typer", "mut_url": "https://github.com/byunjuneseok/async-typer"},
    {"eco": "pypi", "seed": "boto3", "mutation": "boto3-utils", "seed_url": "https://github.com/boto/boto3", "mut_url": "https://github.com/matthewhanson/boto3-utils"},
    {"eco": "pypi", "seed": "click", "mutation": "django-click", "seed_url": "https://github.com/pallets/click", "mut_url": "https://github.com/django-commons/django-click"},
    {"eco": "pypi", "seed": "rich", "mutation": "django-rich", "seed_url": "https://github.com/Textualize/rich", "mut_url": "https://github.com/adamchainz/django-rich"},
    {"eco": "pypi", "seed": "typer", "mutation": "django-typer", "seed_url": "https://github.com/fastapi/typer", "mut_url": "https://github.com/django-commons/membership"},
    {"eco": "pypi", "seed": "jinja2", "mutation": "jinja2-cli", "seed_url": "https://github.com/pallets/jinja", "mut_url": "https://github.com/mattrobenolt/jinja2-cli"},
    {"eco": "pypi", "seed": "pydantic", "mutation": "pydantic-cli", "seed_url": "https://github.com/pydantic/pydantic", "mut_url": "https://github.com/mpkocher/pydantic-cli"},
    {"eco": "pypi", "seed": "requests", "mutation": "requests-go", "seed_url": "https://github.com/psf/requests", "mut_url": "https://github.com/wangluozhe/requests-go"},
    {"eco": "pypi", "seed": "requests", "mutation": "requests-rs", "seed_url": "https://github.com/psf/requests", "mut_url": "https://github.com/zt1901/requests-rs"},
    {"eco": "pypi", "seed": "requests", "mutation": "requests-utils", "seed_url": "https://github.com/psf/requests", "mut_url": "https://github.com/ilotoki0804/requests-utils"},
    {"eco": "pypi", "seed": "rich", "mutation": "rich-cli", "seed_url": "https://github.com/Textualize/rich", "mut_url": "https://github.com/Textualize/rich-cli"},
    {"eco": "pypi", "seed": "sqlalchemy", "mutation": "sqlalchemy-utils", "seed_url": "https://github.com/sqlalchemy/sqlalchemy", "mut_url": "https://github.com/kvesteri/sqlalchemy-utils"},
    {"eco": "pypi", "seed": "tenacity", "mutation": "tenacity-rs", "seed_url": "https://github.com/jd/tenacity", "mut_url": "https://github.com/wkargul/tenacity-rs"},
    {"eco": "pypi", "seed": "typer", "mutation": "typer-cli", "seed_url": "https://github.com/fastapi/typer", "mut_url": "https://github.com/fastapi/typer"},
]

# Negative control pairs (seed vs unrelated popular package)
NEGATIVE_CONTROLS = [
    {"eco": "pypi", "seed": "requests", "other": "urllib3", "seed_url": "https://github.com/psf/requests", "other_url": "https://github.com/urllib3/urllib3"},
    {"eco": "pypi", "seed": "click", "other": "argparse", "seed_url": "https://github.com/pallets/click", "other_url": "https://docs.python.org/3/library/argparse.html"},
    {"eco": "npm", "seed": "chalk", "other": "colors", "seed_url": "https://github.com/chalk/chalk", "other_url": "https://github.com/marak/colors.js"},
    {"eco": "crates", "seed": "regex", "other": "fancy-regex", "seed_url": "https://github.com/rust-lang/regex", "other_url": "https://github.com/rust-lang/fancy-regex"},
]

def gh_get(url, headers=None):
    """GitHub API GET with rate limit handling."""
    req = urllib.request.Request(url, headers=headers or {})
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "E069-false-accept-confusion")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            # Rate limit headers
            remaining = resp.headers.get("X-RateLimit-Remaining")
            reset = resp.headers.get("X-RateLimit-Reset")
            if remaining is not None:
                print(f"  GH rate limit remaining: {remaining}")
            body = resp.read().decode("utf-8", "replace")
            return resp.status, json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        return e.code, {"error": body}
    except Exception as e:
        return 0, {"error": str(e)}


def se_get(url):
    """Stack Exchange API GET."""
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            body = resp.read().decode("utf-8", "replace")
            return resp.status, json.loads(body)
    except Exception as e:
        return 0, {"error": str(e)}


def search_gh_issues(repo_owner, repo_name, query, max_pages=3):
    """Search GitHub issues in a repo for query."""
    results = []
    for page in range(1, max_pages + 1):
        q = urllib.parse.quote(query)
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues?q={q}&state=all&per_page=100&page={page}"
        status, data = gh_get(url)
        if status != 200:
            print(f"    GH search failed: {status} {data}")
            break
        items = data if isinstance(data, list) else data.get("items", [])
        if not items:
            break
        results.extend(items)
        if len(items) < 100:
            break
        time.sleep(6)  # 10 req/min = 6 sec between requests
    return results


def extract_owner_repo(url):
    """Extract owner/repo from GitHub URL."""
    # https://github.com/owner/repo
    parts = url.replace("https://github.com/", "").split("/")
    if len(parts) >= 2:
        return parts[0], parts[1]
    return None, None


def search_stackoverflow(tagged, intitle, pagesize=50):
    """Search Stack Overflow for questions."""
    url = (
        f"https://api.stackexchange.com/2.3/search/advanced?"
        f"order=desc&sort=relevance&site=stackoverflow"
        f"&tagged={urllib.parse.quote(tagged)}&title={urllib.parse.quote(intitle)}"
        f"&pagesize={pagesize}"
    )
    status, data = se_get(url)
    if status != 200:
        print(f"    SE search failed: {status} {data}")
        return []
    return data.get("items", [])


def search_stackoverflow_body(tagged, body_text, pagesize=50):
    """Search Stack Overflow question bodies."""
    url = (
        f"https://api.stackexchange.com/2.3/search/advanced?"
        f"order=desc&sort=relevance&site=stackoverflow"
        f"&tagged={urllib.parse.quote(tagged)}&body={urllib.parse.quote(body_text)}"
        f"&pagesize={pagesize}"
    )
    status, data = se_get(url)
    if status != 200:
        print(f"    SE body search failed: {status} {data}")
        return []
    return data.get("items", [])


def main():
    all_results = []

    # Search each pair
    for i, pair in enumerate(PAIRS):
        print(f"\n[{i+1}/{len(PAIRS)}] {pair['eco']}: {pair['seed']} -> {pair['mutation']}")
        pair_results = {"pair": pair, "hits": []}

        # Extract repo info
        seed_owner, seed_repo = extract_owner_repo(pair["seed_url"])
        mut_owner, mut_repo = extract_owner_repo(pair["mut_url"])

        # 1. Search seed repo issues for mutation name
        if seed_owner and seed_repo:
            print(f"  Searching {seed_owner}/{seed_repo} issues for '{pair['mutation']}'...")
            hits = search_gh_issues(seed_owner, seed_repo, pair["mutation"])
            for h in hits:
                body = h.get("body") or ""
                pair_results["hits"].append({
                    "source": "github_issues_seed",
                    "title": h.get("title", ""),
                    "body": body[:500],
                    "url": h.get("html_url", ""),
                    "number": h.get("number"),
                    "repo": f"{seed_owner}/{seed_repo}"
                })
            print(f"    Found {len(hits)} issues")
            time.sleep(6)

        # 2. Search mutation repo issues for seed name
        if mut_owner and mut_repo and mut_owner != seed_owner:
            print(f"  Searching {mut_owner}/{mut_repo} issues for '{pair['seed']}'...")
            hits = search_gh_issues(mut_owner, mut_repo, pair["seed"])
            for h in hits:
                body = h.get("body") or ""
                pair_results["hits"].append({
                    "source": "github_issues_mutation",
                    "title": h.get("title", ""),
                    "body": body[:500],
                    "url": h.get("html_url", ""),
                    "number": h.get("number"),
                    "repo": f"{mut_owner}/{mut_repo}"
                })
            print(f"    Found {len(hits)} issues")
            time.sleep(6)

        # 3. Stack Overflow: tag + title search
        # Map ecosystem to SO tags
        tag_map = {
            "pypi": "python",
            "npm": "javascript",
            "crates": "rust",
            "gem": "ruby",
        }
        tag = tag_map.get(pair["eco"], "")
        if tag:
            print(f"  Searching Stack Overflow [{tag}] for '{pair['seed']} {pair['mutation']}'...")
            hits = search_stackoverflow(tag, f"{pair['seed']} {pair['mutation']}")
            for h in hits:
                pair_results["hits"].append({
                    "source": "stackoverflow_title",
                    "title": h.get("title", ""),
                    "body": h.get("body", "")[:500] if "body" in h else "",
                    "url": h.get("link", ""),
                    "question_id": h.get("question_id"),
                    "tags": h.get("tags", [])
                })
            print(f"    Found {len(hits)} questions")
            time.sleep(1)  # SE allows 30/sec

            # Also search for "accidentally installed" or "meant to install"
            for phrase in ["accidentally installed", "meant to install", "typo", "wrong package"]:
                hits2 = search_stackoverflow_body(tag, f"{pair['mutation']} {phrase}")
                for h in hits2:
                    pair_results["hits"].append({
                        "source": "stackoverflow_body",
                        "title": h.get("title", ""),
                        "body": h.get("body", "")[:500],
                        "url": h.get("link", ""),
                        "question_id": h.get("question_id"),
                        "tags": h.get("tags", [])
                    })
                time.sleep(1)

        all_results.append(pair_results)

    # Negative controls
    print("\n--- Negative controls ---")
    for i, ctrl in enumerate(NEGATIVE_CONTROLS):
        print(f"\n[NC{i+1}] {ctrl['eco']}: {ctrl['seed']} vs {ctrl['other']}")
        ctrl_results = {"pair": ctrl, "hits": []}

        seed_owner, seed_repo = extract_owner_repo(ctrl["seed_url"])
        other_owner, other_repo = extract_owner_repo(ctrl["other_url"])

        if seed_owner and seed_repo:
            hits = search_gh_issues(seed_owner, seed_repo, ctrl["other"])
            for h in hits:
                body = h.get("body") or ""
                ctrl_results["hits"].append({
                    "source": "github_issues_seed",
                    "title": h.get("title", ""),
                    "body": body[:500],
                    "url": h.get("html_url", ""),
                    "number": h.get("number"),
                    "repo": f"{seed_owner}/{seed_repo}"
                })
            print(f"    Found {len(hits)} issues")
            time.sleep(6)

        tag = {"pypi": "python", "npm": "javascript", "crates": "rust"}.get(ctrl["eco"], "")
        if tag:
            hits = search_stackoverflow(tag, f"{ctrl['seed']} {ctrl['other']}")
            for h in hits:
                ctrl_results["hits"].append({
                    "source": "stackoverflow_title",
                    "title": h.get("title", ""),
                    "body": h.get("body", "")[:500] if "body" in h else "",
                    "url": h.get("link", ""),
                    "question_id": h.get("question_id"),
                    "tags": h.get("tags", [])
                })
            print(f"    Found {len(hits)} SO questions")
            time.sleep(1)

        all_results.append({"negative_control": True, **ctrl_results})

    # Save raw results
    out_path = os.path.join(RAW, "search-results.jsonl")
    with open(out_path, "w") as f:
        for r in all_results:
            f.write(json.dumps(r) + "\n")
    print(f"\nSaved {len(all_results)} result sets to {out_path}")


if __name__ == "__main__":
    main()