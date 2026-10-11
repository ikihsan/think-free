"""E097 — View-count principle on GitHub pyproject.toml presence."""

import json
import urllib.request
import sys
import os

# Configuration
GATE = "--gate" in sys.argv

# GitHub Search API for Python repositories
SEARCH_URL = "https://api.github.com/search/repositories?q=language:python+fork:false&sort=stars&order=desc&per_page=100"

# Need-related classification heuristics
NEED_INDICATORS = {
    "web", "rest", "mvc", "orm", "sql", "json", "xml", "http",
    "parser", "lexer", "encoder", "decoder", "converter", "transform",
    "framework", "client", "server", "engine", "core", "utility", "helper",
    "gui", "cli", "webapp", "library", "tool",
}
GENERIC_TERMS = {"utils", "common", "core", "library", "framework", "jar", "dependencies"}


def fetch_repositories(n=100):
    """Fetch n Python repositories from GitHub Search API."""
    repos = []
    url = SEARCH_URL
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "origin-mission-E097",
            "Accept": "application/vnd.github+json"
        })
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read().decode()
            parsed = json.loads(data)
            items = parsed.get("items", [])
            for item in items[:n]:
                repos.append({
                    "full_name": item.get("full_name", ""),
                    "description": item.get("description", "") or "",
                    "language": item.get("language", "") or "",
                    "topics": item.get("topics", []) or [],
                    "stars": item.get("stargazers_count", 0),
                    "forks": item.get("forks_count", 0),
                    "url": item.get("html_url", ""),
                })
    except Exception as e:
        print(f"Error fetching repositories: {e}", file=sys.stderr)
        sys.exit(1)
    return repos


def has_pyproject_toml(full_name):
    """Check if a repository has a pyproject.toml file at root."""
    # Use GitHub Contents API to check for pyproject.toml
    url = f"https://api.github.com/repos/{full_name}/contents/pyproject.toml"
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "origin-mission-E097",
            "Accept": "application/vnd.github+json"
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            # 200 = file exists, 404 = file doesn't exist
            return resp.status == 200
    except Exception:
        return False


def classify_repository(repo):
    """Classify a repository as need-related or random."""
    description = repo["description"].lower()
    topics = " ".join(repo["topics"]).lower()

    # Check for generic terms - if description/keywords are only generic, classify as random
    found_generic = False
    for term in GENERIC_TERMS:
        if term in description:
            found_generic = True
            break

    if found_generic:
        return "random"

    # Check for need-related indicators in description
    for indicator in NEED_INDICATORS:
        if indicator in description:
            return "need-related"

    # Also check topics
    for indicator in NEED_INDICATORS:
        if indicator in topics:
            return "need-related"

    # Default: if no clear indicator, classify as random
    return "random"


def main():
    # Fetch repositories
    repos = fetch_repositories(100)
    print(f"Fetched {len(repos)} Python repositories from GitHub")

    # Classify each repository
    classified = {"need-related": 0, "random": 0}
    has_toml = {"need-related": 0, "random": 0}
    no_toml = {"need-related": 0, "random": 0}
    classified_count = 0

    for repo in repos:
        cls = classify_repository(repo)
        if cls not in classified:
            continue
        classified[cls] += 1
        classified_count += 1

        has_toml_flag = has_pyproject_toml(repo["full_name"])

        if cls == "need-related":
            if has_toml_flag:
                has_toml["need-related"] += 1
            else:
                no_toml["need-related"] += 1
        else:
            if has_toml_flag:
                has_toml["random"] += 1
            else:
                no_toml["random"] += 1

        # Print individual results for first 20
        if classified_count <= 20:
            title = repo["full_name"]
            needs = " [NEED]" if cls == "need-related" else " [RDOM]"
            toml_marker = " (has pyproject.toml)" if has_toml_flag else " (no pyproject.toml)"
            print(f"  {classified_count}. {title}{needs}{toml_marker}")

    # Print summary
    print("\n=== Classification Summary ===")
    for cls in ["need-related", "random"]:
        count = classified[cls]
        with_toml = has_toml[cls]
        without_toml = no_toml[cls]
        with_rate = (with_toml / count * 100) if count > 0 else 0
        without_rate = (without_toml / count * 100) if count > 0 else 0
        print(f"  {cls}: {count} classified, {with_toml} have pyproject.toml ({with_rate:.1f}%), {without_toml} no pyproject.toml ({without_rate:.1f}%)")

    print(f"\n=== Metrics ===")
    print(f"  Total classified: {classified_count}")
    print(f"  G2 gate (n >= 50): {'PASS' if classified_count >= 50 else 'FAIL'}")
    print(f"  G4 gate (classified >= 30): {'PASS' if classified_count >= 30 else 'FAIL'}")

    if classified_count >= 30:
        # G1 gate: check if need-related has significantly higher pyproject.toml rate
        need_rate = (has_toml["need-related"] / classified["need-related"] * 100) if classified["need-related"] > 0 else 0
        random_rate = (has_toml["random"] / classified["random"] * 100) if classified["random"] > 0 else 0
        diff = need_rate - random_rate

        print(f"\n  G1 gate (pyproject.toml rate difference):")
        print(f"    need-related pyproject.toml rate: {need_rate:.1f}%")
        print(f"    random pyproject.toml rate: {random_rate:.1f}%")
        print(f"    difference: {diff:.1f} percentage points")
        print(f"    G1 threshold: difference >= 10pp (i.e., need-related systematically adopt modern build system)")
        g1_pass = diff >= 10.0
        print(f"    Result: {'PASS' if g1_pass else 'FAIL'}")

        if g1_pass:
            print("\n*** ALL GATES PASS *** - view-count principle generalizes to pyproject.toml adoption in Python packages ***")
            return 0
        else:
            print("\n*** G1 FAIL *** - view-count principle does not generalize to pyproject.toml adoption in Python packages ***")
            return 0
    else:
        print("\n*** GATE PRECONDITIONS NOT MET *** - insufficient data")
        return 2


if __name__ == "__main__":
    sys.exit(main())