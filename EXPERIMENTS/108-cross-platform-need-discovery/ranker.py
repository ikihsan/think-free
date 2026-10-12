#!/usr/bin/env python3
"""Cross-platform ranking module for need discovery."""

from typing import List, Dict, Any, Optional
import math


def normalize_scores(results: List[Dict[str, Any]], platform: str) -> List[Dict[str, Any]]:
    """Normalize activity scores within a platform to 0-1 range."""
    if not results:
        return results
    
    # Extract activity scores
    scores = [r.get("activity_score", 0) for r in results]
    max_score = max(scores) if scores else 1
    min_score = min(scores) if scores else 0
    
    if max_score == min_score:
        for r in results:
            r["normalized_score"] = 0.5
        return results
    
    for r in results:
        raw = r.get("activity_score", 0)
        r["normalized_score"] = (raw - min_score) / (max_score - min_score)
    
    return results


def apply_need_bonus(results: List[Dict[str, Any]], query_classification: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Apply bonus to results that match the query's need classification."""
    need_terms = set(query_classification.get("need_indicators_found", []))
    categories = set(query_classification.get("categories", []))
    
    for r in results:
        bonus = 0.0
        
        # Check description/summary for need terms
        text = (r.get("summary", "") + " " + r.get("description", "")).lower()
        
        # Bonus for matching need indicators
        matches = sum(1 for term in need_terms if term in text)
        bonus += matches * 0.05  # 5% per matching term
        
        # Bonus for matching categories (check topics/keywords)
        if "topics" in r and r["topics"]:
            topics = set(t.lower() for t in r.get("topics", []))
            category_matches = len(categories & topics)
            bonus += category_matches * 0.1
        
        keywords = r.get("keywords")
        if keywords:
            if isinstance(keywords, str):
                keyword_set = set(k.strip().lower() for k in keywords.split(",") if k.strip())
            elif isinstance(keywords, list):
                keyword_set = set(str(k).lower() for k in keywords)
            else:
                keyword_set = set()
            category_matches = len(categories & keyword_set)
            bonus += category_matches * 0.1
        
        r["need_bonus"] = min(bonus, 0.5)  # Cap at 50%
        r["final_score"] = r.get("normalized_score", 0) + r["need_bonus"]
    
    return results


def rank_results(results: List[Dict[str, Any]], query_classification: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Rank results by combined normalized score and need relevance."""
    # Group by platform
    by_platform = {}
    for r in results:
        platform = r.get("platform", "unknown")
        if platform not in by_platform:
            by_platform[platform] = []
        by_platform[platform].append(r)
    
    # Normalize within each platform
    for platform, platform_results in by_platform.items():
        by_platform[platform] = normalize_scores(platform_results, platform)
    
    # Flatten and apply need bonus
    all_results = []
    for platform_results in by_platform.values():
        all_results.extend(platform_results)
    
    all_results = apply_need_bonus(all_results, query_classification)
    
    # Sort by final score descending
    all_results.sort(key=lambda r: r.get("final_score", 0), reverse=True)
    
    # Add rank
    for i, r in enumerate(all_results):
        r["rank"] = i + 1
    
    return all_results


def deduplicate_results(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove duplicate packages across platforms (same name, different platform)."""
    seen = set()
    unique = []
    
    for r in results:
        # Create a key based on name and platform
        key = (r.get("name", "").lower(), r.get("platform", ""))
        if key not in seen:
            seen.add(key)
            unique.append(r)
    
    return unique


def format_results(results: List[Dict[str, Any]], top_n: int = 20, json_output: bool = False) -> str:
    """Format results for display."""
    if json_output:
        import json
        output = []
        for r in results[:top_n]:
            output.append({
                "rank": r.get("rank", 0),
                "platform": r.get("platform", ""),
                "name": r.get("name", ""),
                "summary": r.get("summary", "")[:200],
                "version": r.get("version", ""),
                "activity_score": r.get("activity_score", 0),
                "normalized_score": round(r.get("normalized_score", 0), 3),
                "need_bonus": round(r.get("need_bonus", 0), 3),
                "final_score": round(r.get("final_score", 0), 3),
                "url": r.get("url", ""),
                "language": r.get("language", ""),
                "stars": r.get("stars", 0),
                "downloads_last_month": r.get("downloads_last_month", 0),
                "downloads_recent": r.get("downloads_recent", 0),
                "total_downloads": r.get("total_downloads", 0),
            })
        return json.dumps(output, indent=2)
    
    lines = []
    lines.append(f"{'Rank':>4} {'Platform':<8} {'Name':<40} {'Score':>6} {'Activity':>12} {'Summary'}")
    lines.append("-" * 120)
    
    for r in results[:top_n]:
        rank = r.get("rank", 0)
        platform = r.get("platform", "")[:8]
        name = r.get("name", "")[:38]
        score = r.get("final_score", 0)
        
        # Platform-specific activity display
        activity = r.get("activity_score", 0)
        if platform == "github":
            activity_str = f"{activity:,}★"
        elif platform == "pypi":
            activity_str = f"{activity:,} dl/mo"
        elif platform == "npm":
            activity_str = f"act:{activity}"
        elif platform == "nuget":
            activity_str = f"{activity:,} dl"
        elif platform == "hex":
            activity_str = f"{activity:,} dl/30d"
        else:
            activity_str = str(activity)
        
        summary = r.get("summary", "")[:60]
        
        lines.append(f"{rank:>4} {platform:<8} {name:<40} {score:>6.3f} {activity_str:>12} {summary}")
    
    return "\n".join(lines)


if __name__ == "__main__":
    # Test with mock data
    mock_results = [
        {"name": "httpx", "platform": "pypi", "activity_score": 5000000, "summary": "Next generation HTTP client"},
        {"name": "aiohttp", "platform": "pypi", "activity_score": 3000000, "summary": "Async HTTP client/server"},
        {"name": "requests", "platform": "pypi", "activity_score": 10000000, "summary": "Simple HTTP library"},
        {"name": "axios", "platform": "npm", "activity_score": 95, "summary": "Promise based HTTP client"},
        {"name": "fetch", "platform": "npm", "activity_score": 50, "summary": "Window.fetch polyfill"},
        {"name": "HttpClient", "platform": "nuget", "activity_score": 1000000, "summary": "HTTP client for .NET"},
    ]
    
    query_class = {
        "need_indicators_found": ["async", "http", "client"],
        "categories": ["web"],
    }
    
    ranked = rank_results(mock_results, query_class)
    print(format_results(ranked))