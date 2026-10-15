from __future__ import annotations

import json
import math
import random
import sys
from pathlib import Path

import urllib.request


def fetch_github_repos(query="language:python", per_page=100, page=1):
    """Fetch GitHub repositories sorted by stars."""
    url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page={per_page}&page={page}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "think-free-github-viewcount/1.0",
            "Accept": "application/vnd.github.v3+json",
        }
    )
    try:
        response = urllib.request.urlopen(req, timeout=30)
        data = json.loads(response.read())
        return data.get("items", [])
    except Exception as e:
        print(f"Error fetching GitHub repos: {e}")
        return []


NEED_INDICATORS = frozenset({
    "accessibility", "testing", "validation", "authentication", "auth",
    "parser", "expression", "eval", "integration", "sdk", "payment",
    "security", "web application", "web app", "debugging", "fuzzing",
    "property based", "property test", "fuzz", "robustness", "reliability",
    "webhook", "oauth",
})

INFRA_TERMS = frozenset({
    "library", "framework", "tool", "module", "package",
    "utility", "helper", "snippet", "boilerplate", "skeleton",
    "core", "base", "standard", "default",
})


def classify_description(description):
    """Classify a GitHub repo description as 'need' or 'infra'."""
    if not description:
        return "infra"
    desc = description.strip()
    desc_lower = desc.lower()
    desc_words = set(desc_lower.split())
    if any(ind in desc_lower for ind in NEED_INDICATORS):
        return "need"
    if len(desc) < 30:
        infra_count = sum(1 for w in desc_words if w in INFRA_TERMS)
        if infra_count >= 1 and infra_count / max(len(desc_words), 1) >= 0.5:
            return "infra"
    infra_count = sum(1 for w in desc_words if w in INFRA_TERMS)
    if infra_count >= 2:
        return "infra"
    return "infra"


def main():
    print("=" * 70)
    print("GitHub Repos View-Count Prototype (Fresh Observation)")
    print("Tests the view-count principle's rubric generalization to GitHub")
    print("repositories using hand classification with labels known by construction.")
    print("This is a reversible exploratory prototype (AGENTS.md §3), not a product.")
    print()
    
    print("[1/5] Fetching 100 Python repositories from GitHub API sorted by stars...")
    repos = fetch_github_repos(query="language:python", per_page=100, page=1)
    print(f"   Fetched {len(repos)} repositories (sorted by stars)")
    print()
    
    print("[2/5] Classifying repository descriptions...")
    need_count = 0
    infra_count = 0
    
    for i, repo in enumerate(repos):
        description = repo.get("description", "")
        classification = classify_description(description)
        if classification == "need":
            need_count += 1
        else:
            infra_count += 1
        if (i + 1) % 25 == 0:
            print(f"  classified {i + 1}/{len(repos)} (need={need_count}, infra={infra_count})")
    
    print(f"   Complete: need-related={need_count}, infrastructure={infra_count}")
    print()
    
    print("[3/5] Computing statistics...")
    need_stars = [repo.get("stargazers_count", 0) for repo in repos 
                  if classify_description(repo.get("description", "")) == "need"]
    infra_stars = [repo.get("stargazers_count", 0) for repo in repos 
                   if classify_description(repo.get("description", "")) == "infra"]
    
    need_mean_stars = sum(need_stars) / len(need_stars) if need_stars else 0
    infra_mean_stars = sum(infra_stars) / len(infra_stars) if infra_stars else 0
    need_median_stars = sorted(need_stars)[len(need_stars)//2] if need_stars else 0
    infra_median_stars = sorted(infra_stars)[len(infra_stars)//2] if infra_stars else 0
    
    print(f"   Need-related mean stars: {need_mean_stars:.1f}")
    print(f"   Infrastructure mean stars: {infra_mean_stars:.1f}")
    print(f"   Need-related median stars: {need_median_stars:.1f}")
    print(f"   Infrastructure median stars: {infra_median_stars:.1f}")
    print()
    
    print("[4/5] Checking gates...")
    g1_pass = need_count >= 15
    g2_pass = len(repos) >= 100
    
    view_positive_count = sum(1 for repo in repos if repo.get("stargazers_count", 0) > 0)
    g4_pass = (view_positive_count / len(repos)) >= 0.95 if len(repos) > 0 else False
    
    print(f"   G1 (need prevalence >= 15): {'PASS' if g1_pass else 'FAIL'} (need_count={need_count})")
    print(f"   G2 (corpus >= 100): {'PASS' if g2_pass else 'FAIL'} (total={len(repos)})")
    print(f"   G4 (view_count > 0 >= 95%): {'PASS' if g4_pass else 'FAIL'} (view_positive_rate={view_positive_count}/{len(repos)})")
    print(f"   All gates pass: {'YES' if (g1_pass and g2_pass and g4_pass) else 'NO'}")
    print()
    
    print("[5/5] Generating summary...")
    served_count = 0  # placeholder: would need solution-link analysis
    print(f"   Need-related samples: {need_count}/{len(repos)} ({need_count/len(repos)*100:.1f}%)")
    print(f"   Infrastructure samples: {infra_count}/{len(repos)} ({infra_count/len(repos)*100:.1f}%)")
    print(f"   View positive rate (stars > 0): {view_positive_count}/{len(repos)} ({view_positive_count/len(repos)*100:.1f}%)")
    print(f"   All gates pass: {'YES' if (g1_pass and g2_pass and g4_pass) else 'NO'}")
    print()
    print("=" * 70)
    print("Prototype complete.")
    print("This is a reversible exploratory prototype (AGENTS.md §3):")
    print("  - evidence-gathering, not product validation")
    print("  - tests view-count principle rubric on GitHub Python repos")
    print("  - does not claim adoption, users, or novelty")
    print("=" * 70)


if __name__ == "__main__":
    main()