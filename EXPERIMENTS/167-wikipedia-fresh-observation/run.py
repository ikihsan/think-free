#!/usr/bin/env python3
"""
Fresh observation experiment: Wikipedia stubs vs developed articles view-count principle test.
Stdlib only: urllib, json, statistics, datetime, sys, time, random.
"""

import urllib.request
import urllib.error
import urllib.parse
import json
import statistics
import sys
import time
import random
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Tuple, Optional

# Constants
WIKI_API = "https://en.wikipedia.org/w/api.php"
PAGEVIEWS_API = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/all-access/user"
STUB_CATEGORY = "Category:All_stub_articles"
SAMPLE_SIZE = 50
DAYS_BACK = 30
TIMEOUT = 30
MAX_RETRIES = 3
RATE_LIMIT_DELAY = 0.3

def fetch_json(url: str, allow_404: bool = False) -> Any:
    """Fetch JSON from URL with retries and rate limit handling."""
    for attempt in range(MAX_RETRIES):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "think-free/167 (research)"})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                # Check for rate limit headers
                if resp.status == 429:
                    retry_after = int(resp.headers.get("Retry-After", "60"))
                    time.sleep(retry_after)
                    continue
                return json.load(resp)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                retry_after = int(e.headers.get("Retry-After", "60"))
                print(f"  Rate limited, waiting {retry_after}s...", file=sys.stderr)
                time.sleep(retry_after)
                continue
            if e.code == 404 and allow_404:
                return None  # Not found, but not an error for pageviews
            if attempt == MAX_RETRIES - 1:
                raise
            time.sleep(2 ** attempt)
        except (urllib.error.URLError, json.JSONDecodeError, TimeoutError) as e:
            if attempt == MAX_RETRIES - 1:
                raise
            time.sleep(2 ** attempt)
    return None

def get_stub_titles(limit: int) -> List[str]:
    """Fetch stub article titles from Category:All_stub_articles."""
    titles = []
    cmcontinue = None
    
    while len(titles) < limit:
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": STUB_CATEGORY,
            "cmnamespace": "0",  # Main namespace only
            "cmlimit": "500",
            "format": "json",
        }
        if cmcontinue:
            params["cmcontinue"] = cmcontinue
        
        url = WIKI_API + "?" + urllib.parse.urlencode(params)
        data = fetch_json(url)
        
        if not data or "query" not in data:
            break
        
        for member in data["query"]["categorymembers"]:
            title = member["title"]
            # Skip non-article pages (categories, templates, etc. in main namespace)
            if not title.startswith(("Category:", "Template:", "Wikipedia:", "Portal:", "Draft:", "File:", "Help:", "Module:")):
                titles.append(title)
                if len(titles) >= limit:
                    break
        
        cmcontinue = data.get("continue", {}).get("cmcontinue")
        if not cmcontinue:
            break
        time.sleep(RATE_LIMIT_DELAY)
    
    return titles[:limit]

def get_random_titles(limit: int) -> List[str]:
    """Fetch random main-namespace article titles."""
    titles = []
    while len(titles) < limit:
        rnlimit = min(50, limit - len(titles))
        params = {
            "action": "query",
            "list": "random",
            "rnnamespace": "0",
            "rnlimit": str(rnlimit),
            "format": "json",
        }
        url = WIKI_API + "?" + urllib.parse.urlencode(params)
        data = fetch_json(url)
        
        if not data or "query" not in data:
            break
        
        for page in data["query"]["random"]:
            title = page["title"]
            # Skip non-article pages
            if not title.startswith(("Category:", "Template:", "Wikipedia:", "Portal:", "Draft:", "File:", "Help:", "Module:")):
                titles.append(title)
        
        time.sleep(RATE_LIMIT_DELAY)
    
    return titles[:limit]

def get_article_info(titles: List[str]) -> Dict[str, Dict]:
    """Fetch article length (bytes) and other info for titles."""
    info = {}
    # Process in batches of 50 (API limit)
    for i in range(0, len(titles), 50):
        batch = titles[i:i+50]
        params = {
            "action": "query",
            "titles": "|".join(batch),
            "prop": "info",
            "inprop": "length",
            "format": "json",
        }
        url = WIKI_API + "?" + urllib.parse.urlencode(params)
        data = fetch_json(url)
        
        if data and "query" in data and "pages" in data["query"]:
            for page in data["query"]["pages"].values():
                if "missing" not in page:
                    info[page["title"]] = {
                        "length": page.get("length", 0),
                        "pageid": page.get("pageid"),
                    }
        time.sleep(RATE_LIMIT_DELAY)
    
    return info

def get_pageviews(title: str, days_back: int) -> Optional[int]:
    """Fetch total pageviews for last N days. Returns None if not found."""
    end_date = datetime.now(timezone.utc) - timedelta(days=1)  # Yesterday (today's data incomplete)
    start_date = end_date - timedelta(days=days_back - 1)
    
    start_str = start_date.strftime("%Y%m%d")
    end_str = end_date.strftime("%Y%m%d")
    
    # URL encode title
    encoded_title = urllib.parse.quote(title)
    url = f"{PAGEVIEWS_API}/{encoded_title}/daily/{start_str}/{end_str}"
    
    data = fetch_json(url, allow_404=True)
    if not data or "items" not in data:
        return None
    
    total = 0
    for item in data["items"]:
        total += item.get("views", 0)
    return total

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
    print(f"Fetching {SAMPLE_SIZE} stub article titles...", file=sys.stderr)
    stub_titles = get_stub_titles(SAMPLE_SIZE)
    print(f"Got {len(stub_titles)} stub titles", file=sys.stderr)
    
    print(f"Fetching {SAMPLE_SIZE} random article titles...", file=sys.stderr)
    random_titles = get_random_titles(SAMPLE_SIZE)
    print(f"Got {len(random_titles)} random titles", file=sys.stderr)
    
    # Filter random titles to exclude stubs
    all_titles = stub_titles + random_titles
    print(f"Fetching article info for {len(all_titles)} articles...", file=sys.stderr)
    article_info = get_article_info(all_titles)
    
    # Filter to articles with valid length
    valid_stub = [t for t in stub_titles if t in article_info and article_info[t]["length"] > 0]
    valid_random = [t for t in random_titles if t in article_info and article_info[t]["length"] > 0]
    
    print(f"Valid stubs: {len(valid_stub)}, Valid random: {len(valid_random)}", file=sys.stderr)
    
    if len(valid_stub) < 30 or len(valid_random) < 30:
        print("ERROR: Insufficient valid articles", file=sys.stderr)
        sys.exit(1)
    
    # Fetch pageviews
    print("Fetching pageviews...", file=sys.stderr)
    stub_views_per_byte = []
    stub_raw_views = []
    random_views_per_byte = []
    random_raw_views = []
    classifications = []
    
    for i, title in enumerate(valid_stub):
        if i % 20 == 0:
            print(f"  Stubs: {i}/{len(valid_stub)}...", file=sys.stderr)
        views = get_pageviews(title, DAYS_BACK)
        if views is None:
            print(f"    Skipping {title}: no pageviews data", file=sys.stderr)
            continue
        length = article_info[title]["length"]
        vp_byte = views / length if length > 0 else 0
        
        stub_views_per_byte.append(vp_byte)
        stub_raw_views.append(views)
        
        classifications.append({
            "title": title,
            "arm": "stub",
            "views": views,
            "length": length,
            "views_per_byte": vp_byte,
        })
        time.sleep(RATE_LIMIT_DELAY)
    
    for i, title in enumerate(valid_random):
        if i % 20 == 0:
            print(f"  Random: {i}/{len(valid_random)}...", file=sys.stderr)
        views = get_pageviews(title, DAYS_BACK)
        if views is None:
            print(f"    Skipping {title}: no pageviews data", file=sys.stderr)
            continue
        length = article_info[title]["length"]
        vp_byte = views / length if length > 0 else 0
        
        random_views_per_byte.append(vp_byte)
        random_raw_views.append(views)
        
        classifications.append({
            "title": title,
            "arm": "developed",
            "views": views,
            "length": length,
            "views_per_byte": vp_byte,
        })
        time.sleep(RATE_LIMIT_DELAY)
    
    print(f"Got pageviews for {len(stub_views_per_byte)} stubs, {len(random_views_per_byte)} developed", file=sys.stderr)
    
    # Compute gates (primary metric: views per byte)
    g1_pass = len(stub_views_per_byte) >= 30 and len(random_views_per_byte) >= 30
    g2_pass = len([v for v in stub_raw_views if v > 0]) / len(stub_raw_views) >= 0.8 if stub_raw_views else False
    g4_pass = len(stub_views_per_byte) / len(valid_stub) >= 0.8 and len(random_views_per_byte) / len(valid_random) >= 0.8
    
    delta = cliffs_delta(stub_views_per_byte, random_views_per_byte)
    u_stat, p_value = mann_whitney_u(stub_views_per_byte, random_views_per_byte)
    g3_pass = delta >= 0.147 and p_value < 0.05
    
    # Also compute for raw views
    delta_raw = cliffs_delta(stub_raw_views, random_raw_views)
    u_raw, p_raw = mann_whitney_u(stub_raw_views, random_raw_views)
    
    gates = {
        "G1_sample_size": {"pass": g1_pass, "stub_count": len(stub_views_per_byte), "developed_count": len(random_views_per_byte)},
        "G2_activity_presence": {"pass": g2_pass, "stub_with_views_pct": len([v for v in stub_raw_views if v > 0]) / len(stub_raw_views) * 100 if stub_raw_views else 0},
        "G3_differential_activity_vpbyte": {"pass": g3_pass, "cliffs_delta": delta, "p_value": p_value, "threshold": 0.147},
        "G3_differential_activity_raw": {"cliffs_delta": delta_raw, "p_value": p_raw, "note": "Raw views (secondary)"},
        "G4_metadata_universality": {"pass": g4_pass, "stub_coverage": len(stub_views_per_byte) / len(valid_stub) * 100, "developed_coverage": len(random_views_per_byte) / len(valid_random) * 100},
    }
    
    all_pass = all(g["pass"] for g in gates.values() if "pass" in g)
    
    results = {
        "experiment": "167-wikipedia-fresh-observation",
        "timestamp": time.time(),
        "stub_count": len(stub_views_per_byte),
        "developed_count": len(random_views_per_byte),
        "stub_vpbyte_stats": {
            "mean": statistics.mean(stub_views_per_byte) if stub_views_per_byte else 0,
            "median": statistics.median(stub_views_per_byte) if stub_views_per_byte else 0,
            "stdev": statistics.stdev(stub_views_per_byte) if len(stub_views_per_byte) > 1 else 0,
        },
        "developed_vpbyte_stats": {
            "mean": statistics.mean(random_views_per_byte) if random_views_per_byte else 0,
            "median": statistics.median(random_views_per_byte) if random_views_per_byte else 0,
            "stdev": statistics.stdev(random_views_per_byte) if len(random_views_per_byte) > 1 else 0,
        },
        "stub_raw_stats": {
            "mean": statistics.mean(stub_raw_views) if stub_raw_views else 0,
            "median": statistics.median(stub_raw_views) if stub_raw_views else 0,
        },
        "developed_raw_stats": {
            "mean": statistics.mean(random_raw_views) if random_raw_views else 0,
            "median": statistics.median(random_raw_views) if random_raw_views else 0,
        },
        "cliffs_delta_vpbyte": delta,
        "mann_whitney_u_vpbyte": u_stat,
        "p_value_vpbyte": p_value,
        "cliffs_delta_raw": delta_raw,
        "p_value_raw": p_raw,
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
    print("\n=== RESULTS (views per byte) ===")
    print(f"Stubs: {len(stub_views_per_byte)} articles")
    print(f"  Mean vpbyte: {results['stub_vpbyte_stats']['mean']:.6f}")
    print(f"  Median vpbyte: {results['stub_vpbyte_stats']['median']:.6f}")
    print(f"Developed: {len(random_views_per_byte)} articles")
    print(f"  Mean vpbyte: {results['developed_vpbyte_stats']['mean']:.6f}")
    print(f"  Median vpbyte: {results['developed_vpbyte_stats']['median']:.6f}")
    print(f"Cliff's delta: {delta:.4f} (threshold: 0.147)")
    print(f"Mann-Whitney U: {u_stat:.1f}, p-value: {p_value:.4f}")
    print(f"\n=== RESULTS (raw views) ===")
    print(f"Stubs: Mean={results['stub_raw_stats']['mean']:.1f}, Median={results['stub_raw_stats']['median']:.1f}")
    print(f"Developed: Mean={results['developed_raw_stats']['mean']:.1f}, Median={results['developed_raw_stats']['median']:.1f}")
    print(f"Cliff's delta (raw): {delta_raw:.4f}")
    print(f"\nGates:")
    for name, g in gates.items():
        status = "PASS" if g.get("pass", False) else ("FAIL" if "pass" in g else "N/A")
        print(f"  {name}: {status}")
    print(f"\nOverall: {'ALL GATES PASS' if all_pass else 'KILL GATE FIRED'}")
    print(f"Conclusion: {results['conclusion']}")

if __name__ == "__main__":
    main()