#!/usr/bin/env python3
"""
Harvest ArXiv computational papers with code links for E079.

Uses GitHub API to find papers from E067's population (6 categories, 2024)
and selects A2+A3 papers (partial/docs-only environment info).
"""

import json
import os
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# E067's 6 categories
CATEGORIES = [
    "cs.LG", "cs.CV", "cs.CL", "cs.NE", "stat.ML", "physics.comp-ph"
]

GITHUB_API = "https://api.github.com"
ARXIV_API = "http://export.arxiv.org/api/query"


def github_headers():
    """Get GitHub API headers with token if available."""
    headers = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def fetch_github_repo(owner: str, repo: str):
    """Fetch repository metadata from GitHub API."""
    url = f"{GITHUB_API}/repos/{owner}/{repo}"
    req = Request(url, headers=github_headers())
    try:
        with urlopen(req, timeout=30) as resp:
            return json.load(resp)
    except HTTPError as e:
        if e.code == 404:
            return None
        print(f"  GitHub API error {e.code} for {owner}/{repo}: {e.reason}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  Error fetching {owner}/{repo}: {e}", file=sys.stderr)
        return None


def fetch_repo_contents(owner: str, repo: str, path: str = ""):
    """Fetch repository contents listing."""
    url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}"
    req = Request(url, headers=github_headers())
    try:
        with urlopen(req, timeout=30) as resp:
            return json.load(resp)
    except Exception as e:
        print(f"  Error fetching contents for {owner}/{repo}/{path}: {e}", file=sys.stderr)
        return None


def classify_repo_env(repo_info: dict, contents: list) -> str:
    """
    Classify repository environment specification per E067:
    A1: Machine-runnable spec (Docker/conda/pip with pinned versions)
    A2: Partial spec (lockfiles, some pinning)
    A3: Documentation only (README install instructions)
    A4: No environment info
    """
    if not contents:
        return "A4"

    filenames = {item["name"].lower() for item in contents}

    # Check for A1: fully pinned specs
    has_dockerfile = any(f.startswith("dockerfile") for f in filenames)
    has_conda_env = any(f in filenames for f in ("environment.yml", "environment.yaml"))
    has_req_pinned = False
    if "requirements.txt" in filenames:
        # Would need to fetch content to check pinning
        has_req_pinned = True  # Conservative: assume might be pinned

    if has_dockerfile or has_conda_env or has_req_pinned:
        # Need to verify pinning by fetching content
        return "A1_or_A2"  # Requires content check

    # Check for A2: lockfiles, partial pinning
    lockfiles = {"poetry.lock", "pipfile.lock", "pnpm-lock.yaml", "yarn.lock", "cargo.lock"}
    if filenames & lockfiles:
        return "A2"

    # Check for A3: README with install instructions
    readme_files = [f for f in filenames if f.startswith("readme")]
    if readme_files:
        # Would need to fetch README content
        return "A3"

    return "A4"


def harvest_papers(max_papers: int = 100) -> list:
    """
    Harvest papers from ArXiv categories, find GitHub repos, classify env.
    Returns list of paper dicts with classification.
    """
    papers = []

    for cat in CATEGORIES:
        print(f"Harvesting category: {cat}")
        # Search ArXiv for 2024 papers in category
        query = f"cat:{cat} AND submittedDate:[20240101 TO 20241231]"
        encoded_query = urllib.parse.quote(query)
        url = f"{ARXIV_API}?search_query={encoded_query}&start=0&max_results=50&sortBy=submittedDate&sortOrder=descending"

        try:
            with urlopen(url, timeout=30) as resp:
                xml_content = resp.read().decode('utf-8')
        except Exception as e:
            print(f"  ArXiv API error for {cat}: {e}", file=sys.stderr)
            continue

        # Parse ArXiv XML (simplified - look for arxiv IDs and GitHub links)
        # This is a simplified parser; real implementation would use feedparser
        import re
        entries = re.findall(r'<entry>.*?</entry>', xml_content, re.DOTALL)

        for entry in entries:
            if len(papers) >= max_papers:
                break

            # Extract arxiv ID
            id_match = re.search(r'<id>http://arxiv.org/abs/([^<]+)</id>', entry)
            if not id_match:
                continue
            arxiv_id = id_match.group(1)

            # Extract title
            title_match = re.search(r'<title>([^<]+)</title>', entry)
            title = title_match.group(1).strip() if title_match else ""

            # Extract summary (abstract)
            summary_match = re.search(r'<summary>([^<]+)</summary>', entry, re.DOTALL)
            summary = summary_match.group(1).strip() if summary_match else ""

            # Extract published date
            date_match = re.search(r'<published>([^<]+)</published>', entry)
            published = date_match.group(1) if date_match else ""

            # Look for GitHub links in summary
            github_urls = re.findall(r'https?://github\.com/([\w-]+)/([\w.-]+)', summary)
            github_urls += re.findall(r'github\.com/([\w-]+)/([\w.-]+)', summary)

            for owner, repo in github_urls:
                repo = repo.rstrip('.)\'"')
                print(f"  Found GitHub repo: {owner}/{repo} (arXiv:{arxiv_id})")

                repo_info = fetch_github_repo(owner, repo)
                if not repo_info:
                    continue

                contents = fetch_repo_contents(owner, repo)
                env_class = classify_repo_env(repo_info, contents or [])

                papers.append({
                    "arxiv_id": arxiv_id,
                    "title": title,
                    "published": published,
                    "github_owner": owner,
                    "github_repo": repo,
                    "github_url": f"https://github.com/{owner}/{repo}",
                    "env_classification": env_class,
                    "repo_info": repo_info,
                })

                time.sleep(0.1)  # Rate limiting

        if len(papers) >= max_papers:
            break

    return papers


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Harvest ArXiv papers with GitHub repos")
    parser.add_argument("--max", type=int, default=50, help="Max papers to harvest")
    parser.add_argument("--output", default="raw/harvested_papers.jsonl", help="Output file")
    args = parser.parse_args()

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)

    print(f"Harvesting up to {args.max} papers from {len(CATEGORIES)} categories...")
    papers = harvest_papers(args.max)

    with open(args.output, "w") as f:
        for p in papers:
            f.write(json.dumps(p) + "\n")

    print(f"\nHarvested {len(papers)} papers with GitHub repos")
    for p in papers:
        print(f"  {p['arxiv_id']} -> {p['github_owner']}/{p['github_repo']} [{p['env_classification']}]")

    # Count by classification
    from collections import Counter
    counts = Counter(p["env_classification"] for p in papers)
    print(f"\nClassification counts: {dict(counts)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())