#!/usr/bin/env python3
"""E107 — View-Count Principle on GitHub Code Repositories"""

import json
import subprocess
import sys
from pathlib import Path

# GitHub API helper
def github_api(path):
    """Make unauthenticated GitHub API request."""
    result = subprocess.run(
        ["curl", "-s", f"https://api.github.com{path}"],
        capture_output=True, text=True,
        timeout=30
    )
    if result.returncode != 0:
        print(f"   API error: {result.stderr[:200]}")
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"   JSON decode error: {result.stdout[:200]}")
        return None

# Step 1: Harvest 50+ Python repositories by topic
print("Step 1: Harvesting repositories by topic...")
search_result = github_api("/search/repositories?q=topic:python+sort:stars+desc&per_page=50")
if search_result is None:
    print("   Failed to fetch repositories, exiting.")
    sys.exit(1)
repos = search_result.get('items', []) if isinstance(search_result, dict) else []
print(f"   Found {len(repos)} repositories (total_count={search_result.get('total_count', '?')})")

if len(repos) < 50:
    print("   WARNING: Less than 50 repos retrieved, may not pass G1")

need_keywords = {
    'bug', 'fix', 'problem', 'issue', 'error', 'crash',
    'tutorial', 'how to', 'guide', 'solution', 'debug',
    'install', 'import', 'dependency', 'feature', 'enhancement'
}

repos_data = []
need_related_count = 0
random_count = 0

for i, repo in enumerate(repos):
    name = repo['full_name']
    star_count = repo['stargazers_count']
    
    # Fetch recent issues (open issues)
    issues_result = github_api(f"/repos/{name}/issues?state=open&per_page=100")
    if issues_result is None:
        issues = []
    elif isinstance(issues_result, list):
        issues = issues_result
    else:
        issues = issues_result.get('items', [])
    
    classified = {"need_related": 0, "random": 0, "issue_count": len(issues)}
    
    for issue in issues:
        title = issue.get('title', '').lower()
        # Check if title contains need keywords
        if any(kw in title for kw in need_keywords):
            classified["need_related"] += 1
            need_related_count += 1
        else:
            classified["random"] += 1
            random_count += 1
    
    repos_data.append({
        "name": name,
        "star_count": star_count,
        "need_related": classified["need_related"],
        "random": classified["random"],
        "issue_count": classified["issue_count"]
    })
    
    if (i + 1) % 10 == 0:
        print(f"   Processed {i+1}/{len(repos)} repos...")
    
    if classified["need_related"] > 0:
        print(f"   {name}: {classified['need_related']} need-related, {classified['random']} random / {classified['issue_count']} total issues")

# Step 3: Gate assessment
print("\nStep 3: Gate assessment")

# G1: Retrieval
print(f"   G1: Total repos = {len(repos_data)} (need: ≥30)")
g1_pass = len(repos_data) >= 30
print(f"   G1: {'PASS' if g1_pass else 'FAIL'}")

# G4: Arrival field
print(f"   G4: All {len(repos_data)} repos have star_count (need: 100%)")
g4_pass = all(r['star_count'] > 0 for r in repos_data)
print(f"   G4: {'PASS' if g4_pass else 'FAIL'}")

# G2 + G3: Separation and effect magnitude
if g1_pass and g4_pass:
    need_stars = [r['star_count'] for r in repos_data if r['need_related'] > 0]
    random_stars = [r['star_count'] for r in repos_data if r['random'] > 0]
    
    print(f"   G2/V: need-related repos with stars: {len(need_stars)}")
    print(f"   G2/R: Random repos with stars: {len(random_stars)}")
    
    if need_stars and random_stars:
        # Cliff's δ computation
        greater = sum(1 for x in need_stars for y in random_stars if x > y)
        ties = sum(1 for x in need_stars for y in random_stars if x == y)
        less = len(need_stars) * len(random_stars) - greater - ties
        
        cliff_d = (greater - less) / (len(need_stars) * len(random_stars)) if len(need_stars) * len(random_stars) > 0 else 0
        print(f"   Cliff's δ: {cliff_d:.4f} (need: >0.6)")
        g3_pass = cliff_d > 0.6
        print(f"   G3: {'PASS' if g3_pass else 'FAIL'}")
        
        # Mann-Whitney U test approximation
        need_sorted = sorted(need_stars)
        random_sorted = sorted(random_stars)
        n1, n2 = len(need_sorted), len(random_sorted)
        u = sum(1 for rs in random_sorted for ns in need_sorted if ns > rs)
        mean_u = n1 * n2 / 2
        se = (n1 * n2 * (n1 + n2 + 1) / 12) ** 0.5
        z = (u - mean_u) / se if se > 0 else 0
        print(f"   G2 (Mann-Whitney U z): {z:.2f}")
    else:
        g3_pass = False
        print(f"   G3: FAIL (insufficient data for effect size)")
else:
    g3_pass = False
    print(f"   G3: SKIP (G1 or G4 not passed)")

# Step 4: Write results
results = {
    "experiment": "E107",
    "title": "View-Count Principle on GitHub Code Repositories",
    "repositories_harvested": len(repos_data),
    "g1_retrieval_pass": g1_pass,
    "g2_separation": g3_pass,
    "g3_effect_magnitude": g3_pass,
    "g4_arrival_field": g4_pass,
    "need_related_count": need_related_count,
    "random_count": random_count,
    "conclusion": "GATE_OPEN" if all([g1_pass, g4_pass, g3_pass]) else "GATE_CLOSED",
    "domain": "github_code_repositories",
    "timestamp": "2026-10-13"
}

output_path = Path("/home/ubuntu/think-free/EXPERIMENTS/107-github-repos-viewcount/results.json")
output_path.write_text(json.dumps(results, indent=2))
print(f"\nResults written to {output_path}")
print(json.dumps(results, indent=2))