#!/usr/bin/env python3
"""Harvest ImportError/ModuleNotFoundError reports from Stack Overflow only."""

import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

SE_API_BASE = "https://api.stackexchange.com/2.3"
SE_SITE = "stackoverflow"
SE_PAGESIZE = 100

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

def harvest_stackoverflow(max_questions=500):
    """Harvest Python ImportError/ModuleNotFoundError questions from Stack Overflow."""
    print(f"Harvesting up to {max_questions} questions from Stack Overflow...")
    
    all_questions = []
    page = 1
    
    # Search for questions with "No module named" in body (most reliable signal)
    while len(all_questions) < max_questions:
        params = {
            "site": SE_SITE,
            "tagged": "python",
            "inbody": "\"No module named\"",
            "sort": "activity",
            "order": "desc",
            "pagesize": min(SE_PAGESIZE, max_questions - len(all_questions)),
            "page": page,
            "filter": "withbody"
        }
        
        data = se_get("/search/advanced", params)
        items = data.get("items", [])
        
        if not items:
            break
            
        for q in items:
            # Verify it has ImportError or ModuleNotFoundError in title or body
            title = q.get("title", "").lower()
            body = q.get("body", "").lower()
            if "importerror" in title or "modulenotfounderror" in title or \
               "importerror" in body or "modulenotfounderror" in body or \
               "no module named" in body:
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
        time.sleep(0.1)
        
        if page > 10:
            break
    
    print(f"Harvested {len(all_questions)} questions from Stack Overflow")
    return all_questions

if __name__ == "__main__":
    questions = harvest_stackoverflow(500)
    
    with open("harvest_so.json", "w") as f:
        json.dump(questions, f, indent=1)
    
    print("Saved to harvest_so.json")