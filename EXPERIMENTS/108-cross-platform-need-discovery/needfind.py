#!/usr/bin/env python3
"""needfind — Cross-platform need discovery using the view-count principle.

Usage:
    python3 needfind.py "async HTTP client for Python"
    python3 needfind.py "React state management" --platforms npm,github
    python3 needfind.py "database ORM" --language python --json
"""

import argparse
import json
import sys
from typing import List, Dict, Any

# Add current directory to path for imports
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from classifier import classify_need, detect_language, extract_search_terms, build_platform_query
from ranker import rank_results, format_results
from platforms import pypi, npm, github, nuget, hex


PLATFORM_MODULES = {
    "pypi": pypi,
    "npm": npm,
    "github": github,
    "nuget": nuget,
    "hex": hex,
}

DEFAULT_PLATFORMS = ["pypi", "npm", "github", "nuget", "hex"]

LANGUAGE_TO_PLATFORMS = {
    "python": ["pypi", "github"],
    "javascript": ["npm", "github"],
    "typescript": ["npm", "github"],
    "csharp": ["nuget", "github"],
    "elixir": ["hex", "github"],
    "rust": ["github"],
    "go": ["github"],
    "java": ["github"],
    "ruby": ["github"],
    "php": ["github"],
}


def select_platforms(query: str, explicit_platforms: List[str] = None, language_hint: str = None) -> List[str]:
    """Determine which platforms to search based on query, explicit list, or language hint."""
    if explicit_platforms:
        return [p for p in explicit_platforms if p in PLATFORM_MODULES]
    
    if language_hint and language_hint in LANGUAGE_TO_PLATFORMS:
        return LANGUAGE_TO_PLATFORMS[language_hint]
    
    # Auto-detect from query
    detected = detect_language(query)
    if detected:
        primary_lang = detected[0][0]
        if primary_lang in LANGUAGE_TO_PLATFORMS:
            return LANGUAGE_TO_PLATFORMS[primary_lang]
    
    # Default: search all platforms
    return DEFAULT_PLATFORMS


def search_platform(platform: str, query: str, language: str = None, max_results: int = 20) -> List[Dict[str, Any]]:
    """Search a single platform and return enriched results."""
    module = PLATFORM_MODULES.get(platform)
    if not module:
        print(f"  Unknown platform: {platform}")
        return []
    
    print(f"  Searching {platform}...")
    
    # Build platform-specific query
    platform_query = build_platform_query(query, platform, language)
    
    # Search
    results = module.search_packages(platform_query, max_results=max_results)
    
    if not results:
        print(f"    No results")
        return []
    
    # Enrich with details
    enriched = module.enrich_results(results, max_detail=min(10, len(results)))
    
    print(f"    Found {len(enriched)} packages")
    return enriched


def main():
    parser = argparse.ArgumentParser(
        description="needfind — Cross-platform need discovery using the view-count principle",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 needfind.py "async HTTP client for Python"
  python3 needfind.py "React state management library" --platforms npm,github
  python3 needfind.py "C# JSON serializer" --language csharp
  python3 needfind.py "Elixir web framework" --json
        """
    )
    
    parser.add_argument("query", help="Natural language need description")
    parser.add_argument("--platforms", help="Comma-separated list of platforms (pypi,npm,github,nuget,hex)")
    parser.add_argument("--language", help="Programming language hint (python,javascript,typescript,csharp,elixir,rust,go,java,ruby,php)")
    parser.add_argument("--max-results", type=int, default=20, help="Max results per platform (default: 20)")
    parser.add_argument("--top", type=int, default=20, help="Number of top results to show (default: 20)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Classify the query
    print(f"Query: {args.query}")
    classification = classify_need(args.query)
    print(f"Classification: {classification['classification']}")
    print(f"Need indicators: {classification['need_indicators_found']}")
    print(f"Categories: {classification['categories']}")
    
    detected_langs = detect_language(args.query)
    if detected_langs:
        print(f"Detected languages: {detected_langs}")
    
    # Select platforms
    explicit_platforms = args.platforms.split(",") if args.platforms else None
    platforms = select_platforms(args.query, explicit_platforms, args.language)
    print(f"Searching platforms: {', '.join(platforms)}")
    print()
    
    # Search each platform
    all_results = []
    for platform in platforms:
        results = search_platform(platform, args.query, args.language, args.max_results)
        all_results.extend(results)
    
    if not all_results:
        print("No results found on any platform.")
        return 1
    
    # Rank results
    print("\nRanking results by view-count signal...")
    ranked = rank_results(all_results, classification)
    
    # Format and output
    output = format_results(ranked, top_n=args.top, json_output=args.json)
    print()
    print(output)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())