#!/usr/bin/env python3
"""Harvest ImportError/ModuleNotFoundError reports from Stack Overflow and GitHub."""

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

# Stack Exchange API
SE_API_BASE = "https://api.stackexchange.com/2.3"
SE_SITE = "stackoverflow"
SE_PAGESIZE = 100

# GitHub Search API
GH_API_BASE = "https://api.github.com"
GH_SEARCH_ISSUES = "/search/issues"

# Cache directory
CACHE_DIR = os.environ.get("MODULE_DEMAND_CACHE", ".module-demand-cache")
os.makedirs(CACHE_DIR, exist_ok=True)

def se_get(endpoint, params):
    """Fetch from Stack Exchange API."""
    url = f"{SE_API_BASE}{endpoint}"
    query = urllib.parse.urlencode(params)
    full_url = f"{url}?{query}"
    
    cache_file = os.path.join(CACHE_DIR, f"se_{hash(full_url)}.json")
    if os.path.exists(cache_file):
        with open(cache_file) as f:
            return json.load(f)
    
    req = urllib.request.Request(full_url, headers={"User-Agent": "module-demand-harvest/0.1"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as e:
        if e.code == 429:
            print("Rate limited by Stack Exchange API", file=sys.stderr)
            time.sleep(60)
            return se_get(endpoint, params)
        raise
    
    with open(cache_file, "w") as f:
        json.dump(data, f)
    return data

def gh_get(endpoint, params, token=None):
    """Fetch from GitHub API."""
    url = f"{GH_API_BASE}{endpoint}"
    query = urllib.parse.urlencode(params)
    full_url = f"{url}?{query}"
    
    cache_file = os.path.join(CACHE_DIR, f"gh_{hash(full_url)}.json")
    if os.path.exists(cache_file):
        with open(cache_file) as f:
            return json.load(f)
    
    headers = {"User-Agent": "module-demand-harvest/0.1", "Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    
    req = urllib.request.Request(full_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as e:
        if e.code == 403:
            print("Rate limited by GitHub API", file=sys.stderr)
            time.sleep(60)
            return gh_get(endpoint, params, token)
        raise
    
    with open(cache_file, "w") as f:
        json.dump(data, f)
    return data

def harvest_stackoverflow(max_questions=500):
    """Harvest Python ImportError/ModuleNotFoundError questions from Stack Overflow."""
    print(f"Harvesting up to {max_questions} questions from Stack Overflow...")
    
    # Search for questions with ImportError or ModuleNotFoundError in title
    # Using tagged=python and intitle search
    all_questions = []
    page = 1
    
    while len(all_questions) < max_questions:
        params = {
            "site": SE_SITE,
            "tagged": "python",
            "intitle": "ImportError ModuleNotFoundError",
            "sort": "activity",
            "order": "desc",
            "pagesize": min(SE_PAGESIZE, max_questions - len(all_questions)),
            "page": page,
            "filter": "withbody"
        }
        
        data = se_get("/questions", params)
        items = data.get("items", [])
        
        if not items:
            break
            
        for q in items:
            # Filter: must have ImportError or ModuleNotFoundError in title or body
            title = q.get("title", "").lower()
            body = q.get("body", "").lower()
            if "importerror" in title or "modulenotfounderror" in title or \
               "importerror" in body or "modulenotfounderror" in body:
                all_questions.append({
                    "id": q["question_id"],
                    "title": q["title"],
                    "body": q["body"],
                    "tags": q.get("tags", []),
                    "view_count": q.get("view_count", 0),
                    "answer_count": q.get("answer_count", 0),
                    "score": q.get("score", 0),
                    "creation_date": q.get("creation_date", 0),
                    "link": q.get("link", ""),
                    "source": "stackoverflow"
                })
        
        if not data.get("has_more", False):
            break
        page += 1
        time.sleep(0.1)  # Be nice to API
        
        if page > 5:  # Safety limit
            break
    
    print(f"Harvested {len(all_questions)} questions from Stack Overflow")
    return all_questions

def harvest_github(max_issues=500, token=None):
    """Harvest Python ImportError/ModuleNotFoundError issues from GitHub."""
    print(f"Harvesting up to {max_issues} issues from GitHub...")
    
    all_issues = []
    page = 1
    per_page = 100
    
    while len(all_issues) < max_issues:
        params = {
            "q": "ImportError OR ModuleNotFoundError language:Python",
            "sort": "updated",
            "order": "desc",
            "per_page": min(per_page, max_issues - len(all_issues)),
            "page": page
        }
        
        data = gh_get(GH_SEARCH_ISSUES, params, token)
        items = data.get("items", [])
        
        if not items:
            break
            
        for issue in items:
            # Filter: must be in a Python repo and have error in title/body
            title = issue.get("title", "").lower()
            body = issue.get("body", "") or ""
            body_lower = body.lower()
            
            if "importerror" in title or "modulenotfounderror" in title or \
               "importerror" in body_lower or "modulenotfounderror" in body_lower:
                # Check if repo is Python (language or file extension)
                repo = issue.get("repository", {})
                repo_lang = repo.get("language", "").lower()
                # Accept if repo language is Python or we can't determine
                if repo_lang in ("python", "", None):
                    all_issues.append({
                        "id": issue["number"],
                        "url": issue["html_url"],
                        "title": issue["title"],
                        "body": body,
                        "repo": repo.get("full_name", ""),
                        "repo_language": repo_lang,
                        "created_at": issue.get("created_at", ""),
                        "updated_at": issue.get("updated_at", ""),
                        "comments": issue.get("comments", 0),
                        "reactions": issue.get("reactions", {}),
                        "source": "github"
                    })
        
        if len(items) < per_page:
            break
        page += 1
        time.sleep(1)  # Be nice to API
        
        if page > 5:  # Safety limit
            break
    
    print(f"Harvested {len(all_issues)} issues from GitHub")
    return all_issues

def deduplicate(reports):
    """Deduplicate by source-specific ID."""
    seen = set()
    unique = []
    for r in reports:
        key = f"{r['source']}:{r['id']}"
        if key not in seen:
            seen.add(key)
            unique.append(r)
    return unique

if __name__ == "__main__":
    import urllib.parse
    
    # Harvest
    so_questions = harvest_stackoverflow(500)
    gh_token = os.environ.get("GITHUB_TOKEN")
    gh_issues = harvest_github(500, gh_token)
    
    all_reports = so_questions + gh_issues
    all_reports = deduplicate(all_reports)
    
    print(f"Total unique reports: {len(all_reports)}")
    
    # Save raw harvest
    with open("harvest_raw.json", "w") as f:
        json.dump(all_reports, f, indent=1)
    
    print("Raw harvest saved to harvest_raw.json")