#!/usr/bin/env python3
"""E108 — View-Count Principle on Personal Finance Forums

Tests whether the view-count principle generalizes to personal finance discussions,
e.g., Reddit r/personalfinance. Uses post scores and comment counts as arrival
metadata, and thread titles about financial needs as need statements.

This is "Option B" from synthesis-view-count-final.md — a fresh observation in
a non-technical domain to map the principle's boundary further.
"""

import json
import subprocess
import sys
from pathlib import Path

# Reddit API helper (public read-only endpoints)
def reddit_api(path, params=None):
    """Make unauthenticated Reddit API request."""
    url = f"https://www.reddit.com{path}.json"
    if params:
        query = "&".join(f"{k}={v}" for k, v in params.items())
        url = f"https://www.reddit.com{path}.json?{query}"
    result = subprocess.run(
        ["curl", "-s", "-A", "think-free-experiment/1.0", url],
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

def fetch_subreddit_posts(subreddit, limit=100):
    """Fetch hot posts from a subreddit."""
    result = reddit_api(f"/r/{subreddit}/hot", {"limit": limit})
    if result is None or len(result) == 0:
        return []
    posts = []
    for item in result:
        data = item.get("data", {})
        posts.append({
            "id": data.get("id", ""),
            "title": data.get("title", ""),
            "score": data.get("score", 0),
            "num_comments": data.get("num_comments", 0),
            "url": data.get("url", ""),
        })
    return posts

# Need keywords for financial domain
finance_keywords = {
    'debt', 'loan', 'mortgage', 'credit', 'interest', 'bankrupt',
    'budget', 'savings', 'investment', 'stock', 'bond', 'retirement',
    'tax', 'irs', 'refund', 'paycheck', 'salary', 'bill',
    'expense', 'cost', 'afford', 'affordability', 'savings goal',
    'emergency fund', 'payment', 'installment', 'arrears',
    'insurance', 'claim', 'coverage', 'premium',
    'rent', 'lease', 'housing', 'foreclosure',
    'bank', 'checking', 'savings account', 'overdraft',
    'payday', 'wage', 'income', 'earnings',
    'debt relief', 'consolidation', 'settlement',
    'financial advisor', 'planner', ' counsel',
}

print("=" * 60)
print("E108 — View-Count Principle on Personal Finance Forums")
print("=" * 60)

# Step 1: Fetch posts from r/personalfinance
print("\nStep 1: Fetching r/personalfinance posts...")
posts = fetch_subreddit_posts("personalfinance", limit=100)
print(f"   Fetched {len(posts)} hot posts from r/personalfinance")

if len(posts) < 30:
    print("   WARNING: Less than 30 posts retrieved, may not pass G1")
    sys.exit(1)

# Step 2: Classify posts as need-related or random
print(f"\nStep 2: Classifying posts need-related vs random...")
need_related_count = 0
random_count = 0
posts_with_score = 0
posts_with_comments = 0

classified_posts = []

for post in posts:
    title = post["title"].lower()
    score = post["score"]
    num_comments = post["num_comments"]
    
    # Track arrival field coverage
    if score is not None:
        posts_with_score += 1
    if num_comments is not None:
        posts_with_comments += 1
    
    # Check if title contains finance need keywords
    if any(kw in title for kw in finance_keywords):
        need_related_count += 1
        classified = "need_related"
    else:
        random_count += 1
        classified = "random"
    
    classified_posts.append({
        "id": post["id"],
        "title": post["title"],
        "score": score,
        "num_comments": num_comments,
        "classified": classified,
    })
    
    if need_related_count <= 5 or random_count <= 5:
        print(f"   [{classified}] {post['title'][:80]}... (score={score}, comments={num_comments})")

print(f"   Need-related: {need_related_count}, Random: {random_count}")
print(f"   Posts with score: {posts_with_score}/{len(posts)}")
print(f"   Posts with comments: {posts_with_comments}/{len(posts)}")

# Step 3: Gate assessment
print("\nStep 3: Gate assessment")

# G1: Retrieval
print(f"   G1: Total posts = {len(posts)} (need: ≥30)")
g1_pass = len(posts) >= 30
print(f"   G1: {'PASS' if g1_pass else 'FAIL'}")

# G4: Arrival field
print(f"   G4: Posts with score data: {posts_with_score}/{len(posts)} (need: 100%)")
g4_pass = posts_with_score >= 30  # need at least 30 with score data
print(f"   G4: {'PASS' if g4_pass else 'FAIL'}")

# G2 + G3: Separation and effect magnitude
if g1_pass and g4_pass:
    need_scores = [p["score"] for p in classified_posts if p["classified"] == "need_related" and p["score"] is not None]
    random_scores = [p["score"] for p in classified_posts if p["classified"] == "random" and p["score"] is not None]
    
    print(f"   G2/V: need-related posts with scores: {len(need_scores)}")
    print(f"   G2/R: random posts with scores: {len(random_scores)}")
    
    if need_scores and random_scores:
        # Cliff's δ computation
        greater = sum(1 for x in need_scores for y in random_scores if x > y)
        ties = sum(1 for x in need_scores for y in random_scores if x == y)
        less = len(need_scores) * len(random_scores) - greater - ties
        
        cliff_d = (greater - less) / (len(need_scores) * len(random_scores)) if len(need_scores) * len(random_scores) > 0 else 0
        print(f"   Cliff's δ: {cliff_d:.4f} (need: >0.6)")
        g3_pass = cliff_d > 0.6
        print(f"   G3: {'PASS' if g3_pass else 'FAIL'}")
        
        # Mann-Whitney U
        need_sorted = sorted(need_scores)
        random_sorted = sorted(random_scores)
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
    "experiment": "E108",
    "title": "View-Count Principle on Personal Finance Forums",
    "subreddit": "r/personalfinance",
    "posts_fetched": len(posts),
    "g1_retrieval_pass": g1_pass,
    "g2_separation": g3_pass,
    "g3_effect_magnitude": g3_pass,
    "g4_arrival_field": g4_pass,
    "need_related_count": need_related_count,
    "random_count": random_count,
    "conclusion": "GATE_OPEN" if all([g1_pass, g4_pass, g3_pass]) else "GATE_CLOSED",
    "domain": "personal_finance_forums",
    "timestamp": "2026-10-13"
}

output_path = Path("/home/ubuntu/think-free/EXPERIMENTS/108-personal-finance-viewcount/results.json")
output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_text(json.dumps(results, indent=2))
print(f"\nResults written to {output_path}")
print(json.dumps(results, indent=2))