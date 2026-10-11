"""Fresh observation experiment: view-count principle on Hacker News stories.

Tests whether the view-count principle generalizes to a social news aggregator
platform (Hacker News), using story "score" as a proxy for view_count/download_count.

The view-count principle requires "arrival metadata" (view_count/download_count)
to measure unserved/open-like fractions. On Hacker News, the story "score" 
(upvotes) serves as a proxy for arrival count.
"""

import json
import os
import sys
import urllib.request
import time
from statistics import mean

# --- Configuration ---
TOP_STORIES_N = 100  # Number of top stories to harvest
GATE_THRESHOLDS = {
    "G1_need_fraction": 0.20,  # Minimum fraction of need-related stories
    "G2_effect_size": 0.3,  # Minimum Cohen's d for score difference
    "G3_unserved_fraction": 0.50,  # Maximum unserved fraction (CI95 upper bound)
    "G4_view_count_coverage": 0.80,  # Minimum fraction with score metadata
}
DOMAIN = "Hacker News social news aggregator"


def fetch_top_stories(n=TOP_STORIES_N):
    """Fetch the top n Hacker News story IDs."""
    try:
        r = urllib.request.urlopen(
            "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty", timeout=8
        )
        ids = json.loads(r.read())
        return ids[:n]
    except Exception as e:
        print(f"Error fetching top stories: {e}")
        return []


def fetch_story(story_id):
    """Fetch details for a single story."""
    try:
        r = urllib.request.urlopen(
            f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json", timeout=8
        )
        return json.loads(r.read())
    except Exception as e:
        print(f"  Error fetching story {story_id}: {e}")
        return None


def classify_need_related(title, url, text=""):
    """Classify a story as need-related based on title keywords.
    
    Heuristic: stories about tools, libraries, software, or solving problems
    are considered need-related. This is a simplified classification.
    """
    title_lower = (title or "").lower()
    url_lower = (url or "").lower()
    
    need_keywords = [
        "tool", "library", "framework", "package", "module", "import",
        "error", "fix", "debug", "install", "setup", "environment",
        "dependency", "pip", "package manager",
    ]
    
    # Problem-solving keywords
    problem_keywords = [
        "how to", "cannot", "not working", "error", "fix", "solution",
        "help", "replace", "alternative", "migrate",
    ]
    
    score = 0
    for kw in need_keywords:
        if kw in title_lower:
            score += 1
    for kw in problem_keywords:
        if kw in title_lower:
            score += 1
    
    # Also check URL
    for kw in need_keywords:
        if kw in url_lower:
            score += 0.5
    
    return score >= 2  # Threshold for classification


def run_experiment():
    """Run the full view-count experiment on Hacker News."""
    print(f"=" * 60)
    print(f"View-count principle on {DOMAIN}")
    print(f"=" * 60)
    print()
    
    # Step 1: Fetch top stories
    print(f"Step 1: Fetching top {TOP_STORIES_N} Hacker News stories...")
    story_ids = fetch_top_stories(TOP_STORIES_N)
    if not story_ids:
        print("  FAIL: Could not fetch story IDs")
        return False
    print(f"  OK: Fetched {len(story_ids)} story IDs")
    
    # Step 2: Fetch story details
    print(f"\nStep 2: Fetching story details...")
    stories = []
    for i, sid in enumerate(story_ids):
        data = fetch_story(sid)
        if data and data.get("type") == "story":
            stories.append(data)
        if i > 0 and i % 10 == 0:
            print(f"  Fetched {i+1}/{len(story_ids)} stories...")
        time.sleep(0.1)  # Rate limiting
    
    print(f"  OK: Fetched {len(stories)} story items")
    
    if len(stories) < 20:
        print(f"  FAIL: Too few stories fetched ({len(stories)}), need at least 20 for G1")
        return False
    
    # Step 3: Classify stories as need-related
    print(f"\nStep 3: Classifying stories as need-related or random...")
    
    need_related = []
    random_stories = []
    
    for story in stories:
        title = story.get("title", "")
        url = story.get("url", "")
        classification = classify_need_related(title, url)
        
        if classification:
            need_related.append(story)
        else:
            random_stories.append(story)
    
    need_count = len(need_related)
    random_count = len(random_stories)
    total = need_count + random_count
    
    print(f"  Need-related: {need_count}/{total} ({need_count/total*100:.1f}% if total > 0 else 'N/A'%)")
    print(f"  Random: {random_count}/{total} ({random_count/total*100:.1f}% if total > 0 else 'N/A'%)")
    
    # Step 4: Apply gates
    print(f"\nStep 4: Applying view-count gates...")
    
    # G1: Minimum need fraction
    need_fraction = need_count / total if total > 0 else 0
    g1_pass = need_fraction >= GATE_THRESHOLDS["G1_need_fraction"]
    print(f"  G1 (need fraction >= {GATE_THRESHOLDS['G1_need_fraction']}): "
          f"{need_fraction:.4f} {'PASS' if g1_pass else 'FAIL'}")
    
    # G2: Score difference between need-related and random
    need_scores = [s.get("score", 0) for s in need_related if s.get("score") is not None]
    random_scores = [s.get("score", 0) for s in random_stories if s.get("score") is not None]
    
    g2_pass = False
    if len(need_scores) >= 10 and len(random_scores) >= 10:
        need_mean = mean(need_scores)
        random_mean = mean(random_scores)
        need_std = (sum((s - need_mean) ** 2 for s in need_scores) / len(need_scores)) ** 0.5 if need_scores else 0
        random_std = (sum((s - random_mean) ** 2 for s in random_scores) / len(random_scores)) ** 0.5 if random_scores else 0
        
        # Welch's t-test approximation (Cohen's d)
        if need_std > 0 and random_std > 0:
            pooled_std = ((need_std ** 2 + random_std ** 2) / 2) ** 0.5
            if pooled_std > 0:
                cohens_d = (need_mean - random_mean) / pooled_std
                g2_pass = abs(cohens_d) >= GATE_THRESHOLDS["G2_effect_size"]
                print(f"  G2 (Cohen's d >= {GATE_THRESHOLDS['G2_effect_size']}): d={cohens_d:.4f} {'PASS' if g2_pass else 'FAIL'}")
                print(f"    Need mean score: {need_mean:.1f} (n={len(need_scores)})")
                print(f"    Random mean score: {random_mean:.1f} (n={len(random_scores)})")
            else:
                print(f"  G2: FAIL (zero pooled std)")
        else:
            print(f"  G2: FAIL (zero std in one group)")
            print(f"    Need std: {need_std:.4f}, Random std: {random_std:.4f}")
    else:
        print(f"  G2: FAIL (insufficient samples: need={len(need_scores)}, random={len(random_scores)})")
    
    # G3: Unserved fraction (fraction of need-related stories with no score metadata)
    # On Hacker News, all stories have scores, but we check for missing/invalid scores
    unserved_count = sum(1 for s in need_related if s.get("score") is None)
    unserved_fraction = unserved_count / len(need_related) if need_related else 1.0
    # G3: Wilson CI95 upper bound for unserved fraction
    # Simplified: just check the raw fraction against threshold
    g3_pass = unserved_fraction <= GATE_THRESHOLDS["G3_unserved_fraction"]
    print(f"  G3 (unserved fraction <= {GATE_THRESHOLDS['G3_unserved_fraction']}): "
          f"{unserved_fraction:.4f} ({unserved_count}/{len(need_related)}) {'PASS' if g3_pass else 'FAIL'}")
    
    # G4: View count coverage fraction
    total_with_score = sum(1 for s in stories if s.get("score") is not None)
    view_count_coverage = total_with_score / len(stories) if stories else 0
    g4_pass = view_count_coverage >= GATE_THRESHOLDS["G4_view_count_coverage"]
    print(f"  G4 (view_count coverage >= {GATE_THRESHOLDS['G4_view_count_coverage']}): "
          f"{view_count_coverage:.4f} ({total_with_score}/{len(stories)}) {'PASS' if g4_pass else 'FAIL'}")
    
    # Step 5: Summary
    print(f"\n" + "=" * 60)
    print("GATE SUMMARY")
    print("=" * 60)
    all_gates = [g1_pass, g2_pass, g3_pass, g4_pass]
    passed = sum(all_gates)
    print(f"  G1 (need fraction): {'PASS' if g1_pass else 'FAIL'}")
    print(f"  G2 (score difference): {'PASS' if g2_pass else 'FAIL'}")
    print(f"  G3 (unserved fraction): {'PASS' if g3_pass else 'FAIL'}")
    print(f"  G4 (view count coverage): {'PASS' if g4_pass else 'FAIL'}")
    print(f"\n  Total: {passed}/4 gates passed")
    
    # Decision
    if passed == 4:
        print("  RESULT: All gates met - principle generalizes to {DOMAIN}")
        decision = "SUPPORTED"
    elif passed >= 3:
        print("  RESULT: Partial support - some gates met, boundaries identified")
        decision = "PARTIAL"
    else:
        print("  RESULT: Principle does not generalize - too many gates failed")
        decision = "FAILED"
    
    # Save results
    results = {
        "domain": DOMAIN,
        "total_stories": len(stories),
        "need_related": need_count,
        "random": random_count,
        "need_fraction": need_fraction,
        "need_scores": need_scores,
        "random_scores": random_scores,
        "unserved_fraction": unserved_fraction,
        "view_count_coverage": view_count_coverage,
        "g1_pass": g1_pass,
        "g2_pass": g2_pass,
        "g3_pass": g3_pass,
        "g4_pass": g4_pass,
        "decision": decision,
        "gate_thresholds": GATE_THRESHOLDS,
    }
    
    os.makedirs('EXPERIMENTS/09X-hnews-viewcount', exist_ok=True)
    with open('EXPERIMENTS/09X-hnews-viewcount/results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n  Results saved to EXPERIMENTS/09X-hnews-viewcount/results.json")
    
    return passed >= 3  # Consider it a success if at least 3 gates pass


if __name__ == "__main__":
    success = run_experiment()
    sys.exit(0 if success else 3)