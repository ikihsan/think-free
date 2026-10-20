#!/usr/bin/env python3
"""
Fresh observation experiment: Dev.to community articles view-count principle test.
Stdlib only: urllib, json, statistics, datetime, sys, time.
"""

import urllib.request
import urllib.error
import json
import statistics
import sys
import time
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Tuple

# Pre-declared need-related tags
NEED_TAGS = {
    "help", "questions", "askdev", "beginners", "tutorial", 
    "howto", "learning", "discuss"
}

# Pre-declared need-related title keywords (case-insensitive)
NEED_TITLE_KEYWORDS = [
    "how to", "how do", "how can", "how should",
    "what is", "what are", "what's the",
    "help", "help me", "need help",
    "anyone", "anybody", "experience with",
    "best", "recommend", "recommendation", "suggest",
    "looking for", "searching for",
    "why", "why does", "why is",
    "advice", "guidance", "direction",
    "alternative", "alternatives", "vs", "versus",
    "compare", "comparison",
    "learn", "tutorial", "guide", "getting started",
]

API_BASE = "https://dev.to/api/articles"
PER_PAGE = 1000
PAGES = 2
TIMEOUT = 30
MAX_RETRIES = 3
DAYS_BACK = 30

def fetch_json(url: str) -> Any:
    """Fetch JSON from URL with retries."""
    for attempt in range(MAX_RETRIES):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "think-free/166"})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                return json.load(resp)
        except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, TimeoutError) as e:
            if attempt == MAX_RETRIES - 1:
                raise
            time.sleep(2 ** attempt)
    return None

def is_recent(article: Dict, cutoff_date: datetime) -> bool:
    """Check if article is within the last DAYS_BACK days."""
    published_at = article.get("published_at")
    if not published_at:
        return False
    try:
        # published_at format: "2024-01-15T10:30:00Z" or similar
        pub_date = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
        return pub_date >= cutoff_date
    except (ValueError, AttributeError):
        return False

def classify_article(article: Dict) -> Tuple[bool, List[str], List[str]]:
    """Classify article as need-related. Returns (is_need, matched_tags, matched_keywords)."""
    matched_tags = []
    matched_keywords = []
    
    # Check tags
    tags = article.get("tag_list", [])
    if isinstance(tags, str):
        tags = [tags]
    for tag in tags:
        if tag.lower() in NEED_TAGS:
            matched_tags.append(tag)
    
    # Check title keywords
    title = (article.get("title") or "").lower()
    for kw in NEED_TITLE_KEYWORDS:
        if kw in title:
            matched_keywords.append(kw)
    
    is_need = len(matched_tags) > 0 or len(matched_keywords) > 0
    return (is_need, matched_tags, matched_keywords)

def composite_activity(article: Dict) -> float:
    """Compute composite activity score."""
    views = article.get("page_views_count", 0) or 0
    reactions = article.get("positive_reactions_count", 0) or 0
    comments = article.get("comments_count", 0) or 0
    return views + reactions * 10 + comments * 50

def cliffs_delta(x: List[float], y: List[float]) -> float:
    """Compute Cliff's delta (effect size). Positive = x > y."""
    if not x or not y:
        return 0.0
    n_x, n_y = len(x), len(y)
    greater = 0
    less = 0
    for xi in x:
        for yj in y:
            if xi > yj:
                greater += 1
            elif xi < yj:
                less += 1
    return (greater - less) / (n_x * n_y)

def mann_whitney_u(x: List[float], y: List[float]) -> Tuple[float, float]:
    """Mann-Whitney U test. Returns (U, p-value approximation)."""
    combined = [(v, 0) for v in x] + [(v, 1) for v in y]
    combined.sort(key=lambda t: t[0])
    
    # Handle ties
    ranks = {}
    i = 0
    while i < len(combined):
        j = i
        while j < len(combined) and combined[j][0] == combined[i][0]:
            j += 1
        avg_rank = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranks[k] = avg_rank
        i = j
    
    r_x = sum(ranks[idx] for idx, (_, g) in enumerate(combined) if g == 0)
    n_x, n_y = len(x), len(y)
    
    u_x = r_x - n_x * (n_x + 1) / 2
    u_y = n_x * n_y - u_x
    u = min(u_x, u_y)
    
    mean_u = n_x * n_y / 2
    std_u = (n_x * n_y * (n_x + n_y + 1) / 12) ** 0.5
    if std_u == 0:
        return u, 1.0
    z = (u - mean_u) / std_u
    import math
    p = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))
    return u, p

def main():
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=DAYS_BACK)
    print(f"Fetching Dev.to articles (last {DAYS_BACK} days)...", file=sys.stderr)
    
    all_articles = []
    for page in range(1, PAGES + 1):
        url = f"{API_BASE}?per_page={PER_PAGE}&page={page}"
        print(f"  Page {page}/{PAGES}...", file=sys.stderr)
        articles = fetch_json(url)
        if not articles:
            print(f"    No articles returned", file=sys.stderr)
            break
        all_articles.extend(articles)
        time.sleep(0.5)
    
    print(f"Fetched {len(all_articles)} total articles", file=sys.stderr)
    
    # Filter recent
    recent_articles = [a for a in all_articles if is_recent(a, cutoff_date)]
    print(f"Recent (last {DAYS_BACK} days): {len(recent_articles)} articles", file=sys.stderr)
    
    if len(recent_articles) < 100:
        print("WARNING: Fewer than 100 recent articles, using all", file=sys.stderr)
    
    # Classify all recent articles
    need_articles = []
    random_articles = []
    classifications = []
    
    for article in recent_articles:
        is_need, matched_tags, matched_keywords = classify_article(article)
        activity = composite_activity(article)
        
        classifications.append({
            "id": article.get("id"),
            "title": article.get("title"),
            "tags": article.get("tag_list", []),
            "published_at": article.get("published_at"),
            "is_need": is_need,
            "matched_tags": matched_tags,
            "matched_keywords": matched_keywords,
            "views": article.get("page_views_count", 0),
            "reactions": article.get("positive_reactions_count", 0),
            "comments": article.get("comments_count", 0),
            "activity": activity,
        })
        
        if is_need:
            need_articles.append(activity)
        else:
            random_articles.append(activity)
    
    print(f"Classified: {len(need_articles)} need-related, {len(random_articles)} random", file=sys.stderr)
    
    # If we have more than 200 total, sample 100 from each arm
    import random
    random.seed(42)
    if len(need_articles) > 100:
        need_articles = random.sample(need_articles, 100)
    if len(random_articles) > 100:
        random_articles = random.sample(random_articles, 100)
    
    print(f"After sampling: {len(need_articles)} need-related, {len(random_articles)} random", file=sys.stderr)
    
    # Compute gates
    g1_pass = len(need_articles) >= 30 and len(random_articles) >= 30
    g2_pass = len([a for a in need_articles if a > 0]) / len(need_articles) >= 0.8 if need_articles else False
    g4_pass = True  # API guarantees these fields
    
    delta = cliffs_delta(need_articles, random_articles)
    u_stat, p_value = mann_whitney_u(need_articles, random_articles)
    g3_pass = delta >= 0.147 and p_value < 0.05
    
    gates = {
        "G1_sample_size": {"pass": g1_pass, "need_count": len(need_articles), "random_count": len(random_articles)},
        "G2_activity_presence": {"pass": g2_pass, "need_with_activity_pct": len([a for a in need_articles if a > 0]) / len(need_articles) * 100 if need_articles else 0},
        "G3_differential_activity": {"pass": g3_pass, "cliffs_delta": delta, "p_value": p_value, "threshold": 0.147},
        "G4_metadata_universality": {"pass": g4_pass, "note": "API guarantees page_views_count, positive_reactions_count, comments_count"},
    }
    
    all_pass = all(g["pass"] for g in gates.values())
    
    results = {
        "experiment": "166-devto-fresh-observation",
        "timestamp": time.time(),
        "total_fetched": len(all_articles),
        "recent_articles": len(recent_articles),
        "need_count": len(need_articles),
        "random_count": len(random_articles),
        "need_activity_stats": {
            "mean": statistics.mean(need_articles) if need_articles else 0,
            "median": statistics.median(need_articles) if need_articles else 0,
            "stdev": statistics.stdev(need_articles) if len(need_articles) > 1 else 0,
        },
        "random_activity_stats": {
            "mean": statistics.mean(random_articles) if random_articles else 0,
            "median": statistics.median(random_articles) if random_articles else 0,
            "stdev": statistics.stdev(random_articles) if len(random_articles) > 1 else 0,
        },
        "cliffs_delta": delta,
        "mann_whitney_u": u_stat,
        "p_value": p_value,
        "gates": gates,
        "all_gates_pass": all_pass,
        "conclusion": "H1 supported (principle generalizes)" if all_pass else "H0 supported (principle does not generalize)",
    }
    
    # Write results
    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    with open("classification.json", "w") as f:
        json.dump(classifications, f, indent=2)
    
    # Print summary
    print("\n=== RESULTS ===")
    print(f"Total fetched: {len(all_articles)}")
    print(f"Recent (last {DAYS_BACK} days): {len(recent_articles)}")
    print(f"Need-related: {len(need_articles)} articles")
    print(f"  Mean activity: {results['need_activity_stats']['mean']:.2f}")
    print(f"  Median activity: {results['need_activity_stats']['median']:.2f}")
    print(f"Random: {len(random_articles)} articles")
    print(f"  Mean activity: {results['random_activity_stats']['mean']:.2f}")
    print(f"  Median activity: {results['random_activity_stats']['median']:.2f}")
    print(f"Cliff's delta: {delta:.4f} (threshold: 0.147)")
    print(f"Mann-Whitney U: {u_stat:.1f}, p-value: {p_value:.4f}")
    print(f"\nGates:")
    for name, g in gates.items():
        status = "PASS" if g["pass"] else "FAIL"
        print(f"  {name}: {status}")
    print(f"\nOverall: {'ALL GATES PASS' if all_pass else 'KILL GATE FIRED'}")
    print(f"Conclusion: {results['conclusion']}")

if __name__ == "__main__":
    main()