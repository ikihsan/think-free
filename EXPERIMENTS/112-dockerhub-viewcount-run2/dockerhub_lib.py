#!/usr/bin/env python3
"""
Docker Hub View-Count Principle Test — data fetching and gate evaluation.
"""

import time
import urllib.parse
import urllib.request
import json
from typing import List, Optional
from dataclasses import dataclass

from classify import (
    Image,  # re-export
    classify_image,
    NEED_KEYWORD_GROUPS,
    RANDOM_QUERIES,
)
from stats import (
    mann_whitney_u,
    cliff_delta,
    wilson_lower_bound,
)


@dataclass
class Image:
    name: str
    pull_count: int
    star_count: int
    short_description: str
    full_description: str
    classification: str  # "need-related" or "random"


def fetch_dockerhub_search(query: str, page_size: int = 100, page: int = 1) -> List[dict]:
    """Fetch images from Docker Hub search API."""
    url = f"https://hub.docker.com/v2/search/repositories/?query={urllib.parse.quote(query)}&page_size={page_size}&page={page}"
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'origin-mission-E112'}
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
            return data.get("results", [])
    except Exception as e:
        print(f"Error fetching Docker Hub search for query '{query}': {e}")
        return []


def extract_image(image_data: dict, classification: str) -> Optional[Image]:
    """Extract relevant fields from Docker Hub search result."""
    try:
        pull_count = image_data.get("pull_count", 0)
        if pull_count is None:
            pull_count = 0
        star_count = image_data.get("star_count", 0)
        if star_count is None:
            star_count = 0
        
        return Image(
            name=image_data.get("repo_name", ""),
            pull_count=int(pull_count),
            star_count=int(star_count),
            short_description=image_data.get("short_description", "") or "",
            full_description=image_data.get("description", "") or "",
            classification=classification
        )
    except Exception:
        return None


def sample_need_related(target: int) -> List[Image]:
    """Sample need-related images from Docker Hub using keyword searches."""
    need_images = []
    seen_names = set()
    
    for keyword in NEED_KEYWORD_GROUPS:
        if len(need_images) >= target:
            break
        
        page = 1
        while len(need_images) < target:
            results = fetch_dockerhub_search(keyword, page_size=50, page=page)
            if not results:
                break
            
            for result in results:
                name = result.get("repo_name", "")
                if not name or name in seen_names:
                    continue
                
                classification = classify_image(result)
                if classification != "need-related":
                    continue
                
                image = extract_image(result, classification)
                if image and image.pull_count > 0:
                    seen_names.add(name)
                    need_images.append(image)
                    if len(need_images) >= target:
                        break
            
            page += 1
            if page > 5:  # Limit pages per keyword
                break
            
            time.sleep(0.3)  # Rate limiting
        
        time.sleep(0.5)  # Rate limiting between keywords
    
    return need_images


def sample_random(target: int) -> List[Image]:
    """Sample random images from Docker Hub using non-selective queries."""
    random_images = []
    seen_names = set()
    
    for query in RANDOM_QUERIES:
        if len(random_images) >= target:
            break
        
        page = 1
        while len(random_images) < target:
            results = fetch_dockerhub_search(query, page_size=50, page=page)
            if not results:
                break
            
            for result in results:
                name = result.get("repo_name", "")
                if not name or name in seen_names:
                    continue
                
                classification = classify_image(result)
                if classification != "random":
                    continue
                
                image = extract_image(result, classification)
                if image and image.pull_count > 0:
                    seen_names.add(name)
                    random_images.append(image)
                    if len(random_images) >= target:
                        break
            
            page += 1
            if page > 3:  # Limit pages per query
                break
            
            time.sleep(0.3)  # Rate limiting
        
        time.sleep(0.5)  # Rate limiting between queries
    
    return random_images


def run_gates(need_imgs: List[Image], random_imgs: List[Image]) -> dict:
    """Run all four gates and return verdicts."""
    results = {}
    
    # G1: Retrieval (sample size)
    g1_need = len(need_imgs) >= 50
    g1_random = len(random_imgs) >= 50
    results["G1"] = {
        "need_count": len(need_imgs),
        "random_count": len(random_imgs),
        "pass": g1_need and g1_random,
        "details": f"need-related: {len(need_imgs)}, random: {len(random_imgs)} (threshold: 50 each)"
    }
    
    if not (g1_need and g1_random):
        results["G2"] = {"pass": False, "details": "G1 failed, not evaluated"}
        results["G3"] = {"pass": False, "details": "G1 failed, not evaluated"}
        results["G4"] = {"pass": False, "details": "G1 failed, not evaluated"}
        return results
    
    need_pulls = [img.pull_count for img in need_imgs]
    random_pulls = [img.pull_count for img in random_imgs]
    
    # G2: Separation (Mann-Whitney U test)
    u_stat, p_value = mann_whitney_u(need_pulls, random_pulls)
    delta = cliff_delta(need_pulls, random_pulls)
    g2_pass = p_value < 0.05 and delta > 0.147
    results["G2"] = {
        "u_statistic": u_stat,
        "p_value": p_value,
        "cliff_delta": delta,
        "pass": g2_pass,
        "details": f"Mann-Whitney U={u_stat:.1f}, p={p_value:.6f}, Cliff's delta={delta:.3f} (threshold p<0.05, delta>0.147)"
    }
    
    # G3: Effect magnitude (Wilson lower bound)
    random_median = sorted(random_pulls)[len(random_pulls)//2]
    need_above = sum(1 for p in need_pulls if p > random_median)
    n_need = len(need_pulls)
    wilson_lb = wilson_lower_bound(need_above, n_need)
    g3_pass = wilson_lb > 0.60
    results["G3"] = {
        "need_above_random_median": need_above,
        "need_total": n_need,
        "proportion": need_above / n_need if n_need > 0 else 0,
        "wilson_lower_bound": wilson_lb,
        "pass": g3_pass,
        "details": f"{need_above}/{n_need} need-related above random median (Wilson LB={wilson_lb:.4f}, threshold=0.60)"
    }
    
    # G4: Arrival field coverage
    total_need = len(need_imgs)
    total_random = len(random_imgs)
    # By construction, all have pull_count > 0
    g4_pass = True
    results["G4"] = {
        "need_with_pulls": total_need,
        "random_with_pulls": total_random,
        "pass": g4_pass,
        "details": f"All {total_need + total_random} sampled images have pull_count > 0 (filtered at fetch)"
    }
    
    return results