#!/usr/bin/env python3
"""
Fetch VS Code Marketplace extensions from multiple categories and test the view-count principle.

The view-count principle states that need-related content (extensions that solve
specific problems) should have systematically higher install/view counts than
random/general extensions.
"""

import json
import sys
import time
import urllib.request
import urllib.error
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class Extension:
    extension_id: str
    extension_name: str
    display_name: str
    publisher_name: str
    short_description: str
    install_count: int
    average_rating: float
    rating_count: int
    trending_daily: float
    trending_monthly: float
    trending_weekly: float
    update_count: int
    weighted_rating: float
    download_count: int
    categories: List[str]
    tags: List[str]
    last_updated: str
    published_date: str


# Keywords that indicate an extension solves a specific problem/need
NEED_KEYWORDS = [
    "fix", "debug", "error", "issue", "problem", "solve", "troubleshoot",
    "lint", "format", "beautify", "validate", "check", "analyze", "inspect",
    "test", "coverage", "profile", "benchmark", "optimize", "performance",
    "security", "vulnerability", "audit", "scan", "detect", "find",
    "refactor", "clean", "organize", "structure", "migrate", "convert",
    "transform", "generate", "scaffold", "boilerplate", "template",
    "snippet", "autocomplete", "intellisense", "completion", "hint",
    "documentation", "comment", "docstring", "readme", "changelog",
    "deploy", "build", "compile", "bundle", "package", "publish",
    "docker", "kubernetes", "k8s", "container", "ci", "cd", "pipeline",
    "git", "github", "gitlab", "bitbucket", "version control", "commit",
    "branch", "merge", "rebase", "conflict", "diff", "history",
    "database", "sql", "query", "migration", "schema", "orm",
    "api", "rest", "graphql", "grpc", "websocket", "http", "client",
    "auth", "authentication", "authorization", "oauth", "jwt", "token",
    "env", "environment", "config", "configuration", "settings", "secret",
    "log", "logger", "logging", "trace", "monitor", "observe", "metric",
    "i18n", "internationalization", "localization", "translate", "locale",
    "accessibility", "a11y", "aria", "screen reader", "contrast",
    "theme", "color", "icon", "font", "ui", "ux", "component",
    "react", "vue", "angular", "svelte", "typescript", "javascript",
    "python", "java", "csharp", "go", "rust", "cpp", "php", "ruby",
    "html", "css", "scss", "sass", "less", "postcss", "tailwind",
    "markdown", "mdx", "yaml", "json", "xml", "toml", "ini",
    "regex", "regular expression", "search", "replace", "find",
    "terminal", "shell", "bash", "zsh", "powershell", "command",
    "remote", "ssh", "ftp", "sftp", "sync", "upload", "download",
    "extension", "plugin", "addon", "tool", "utility", "helper",
]

# Keywords that indicate general/infrastructure extensions (not need-specific)
GENERAL_KEYWORDS = [
    "theme", "color theme", "icon theme", "color", "icon", "font",
    "language pack", "localization", "translation",
    "keymap", "keyboard shortcut", "keybinding",
    "snippet", "code snippet", "boilerplate", "template",
    "extension pack", "pack", "bundle",
    "welcome", "start page", "dashboard",
    "settings", "preferences", "configuration",
]


def classify_extension(ext: Extension) -> str:
    """Classify extension as 'need-related', 'general', or 'other'."""
    text = f"{ext.display_name} {ext.short_description} {' '.join(ext.tags)} {' '.join(ext.categories)}".lower()
    
    # Check for need-indicator keywords
    need_score = sum(1 for kw in NEED_KEYWORDS if kw in text)
    
    # Check for general/infrastructure keywords
    general_score = sum(1 for kw in GENERAL_KEYWORDS if kw in text)
    
    if need_score > 0 and need_score > general_score:
        return "need-related"
    elif general_score > 0 and general_score >= need_score:
        return "general"
    else:
        return "other"


def fetch_extensions_from_category(category: str, page_size: int = 50, max_pages: int = 5) -> List[Extension]:
    """Fetch extensions from a specific category."""
    extensions = []
    url = "https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery?api-version=7.1-preview.1"
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Accept": "application/json; api-version=7.1-preview.1",
    }
    
    for page in range(max_pages):
        payload = {
            "filters": [{
                "criteria": [
                    {"filterType": 10, "value": category},  # Category filter
                ],
                "direction": 2,  # Descending (most popular first)
                "pageSize": page_size,
                "pageNumber": page,
            }],
            "flags": 870,  # Include statistics, versions, etc.
        }
        
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers, method='POST')
        
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            print(f"HTTP error on page {page} for category {category}: {e.code} - {e.reason}", file=sys.stderr)
            break
        except Exception as e:
            print(f"Error on page {page} for category {category}: {e}", file=sys.stderr)
            break
        
        if not result.get("results") or not result["results"][0].get("extensions"):
            break
            
        page_extensions = result["results"][0]["extensions"]
        if not page_extensions:
            break
            
        for ext_data in page_extensions:
            try:
                stats = {s["statisticName"]: s["value"] for s in ext_data.get("statistics", [])}
                ext = Extension(
                    extension_id=ext_data["extensionId"],
                    extension_name=ext_data["extensionName"],
                    display_name=ext_data["displayName"],
                    publisher_name=ext_data["publisher"]["displayName"],
                    short_description=ext_data.get("shortDescription", "") or "",
                    install_count=int(stats.get("install", 0)),
                    average_rating=float(stats.get("averagerating", 0)),
                    rating_count=int(stats.get("ratingcount", 0)),
                    trending_daily=float(stats.get("trendingdaily", 0)),
                    trending_monthly=float(stats.get("trendingmonthly", 0)),
                    trending_weekly=float(stats.get("trendingweekly", 0)),
                    update_count=int(stats.get("updateCount", 0)),
                    weighted_rating=float(stats.get("weightedRating", 0)),
                    download_count=int(stats.get("downloadCount", 0)),
                    categories=ext_data.get("categories", []),
                    tags=ext_data.get("tags", []),
                    last_updated=ext_data.get("lastUpdated", ""),
                    published_date=ext_data.get("publishedDate", ""),
                )
                extensions.append(ext)
            except Exception as e:
                print(f"Error parsing extension: {e}", file=sys.stderr)
                continue
        
        print(f"  Category {category}, page {page + 1}: {len(page_extensions)} extensions")
        time.sleep(0.3)  # Be nice to the API
        
    return extensions


def compute_cliffs_delta(group1: List[float], group2: List[float]) -> float:
    """Compute Cliff's delta effect size between two groups."""
    if not group1 or not group2:
        return 0.0
    
    n1, n2 = len(group1), len(group2)
    greater = sum(1 for x in group1 for y in group2 if x > y)
    less = sum(1 for x in group1 for y in group2 if x < y)
    return (greater - less) / (n1 * n2)


def main():
    # Categories to fetch from (based on the marketplace categories seen in earlier queries)
    categories = [
        "Other", "Tools", "Tools/Coding", "Tools/Other", "Programming Languages",
        "Debuggers", "Snippets", "Linters", "Formatters", "Testing",
        "Tools/Performance", "Tools/Web", "Tools/Data", "Tools/Build",
        "Azure", "Azure Pipelines", "Azure Boards", "Azure Repos",
        "Visualization", "Data Science", "AI", "Machine Learning",
        "Extension Packs", "Tools/Extension Packs", "Tools/Source Control",
        "SCM Providers", "Tools/Testing", "Tools/Documentation",
        "Tools/Connected Services", "Tools/Scaffolding", "Tools/Reporting",
    ]
    
    all_extensions = []
    for cat in categories:
        print(f"Fetching category: {cat}")
        exts = fetch_extensions_from_category(cat, page_size=50, max_pages=3)
        all_extensions.extend(exts)
        print(f"  Total so far: {len(all_extensions)}")
    
    # Deduplicate by extension_id
    seen = set()
    unique_extensions = []
    for ext in all_extensions:
        if ext.extension_id not in seen:
            seen.add(ext.extension_id)
            unique_extensions.append(ext)
    
    print(f"\nTotal unique extensions fetched: {len(unique_extensions)}")
    
    if not unique_extensions:
        print("No extensions fetched!")
        return 1
    
    # Classify extensions
    classified = {"need-related": [], "general": [], "other": []}
    for ext in unique_extensions:
        cat = classify_extension(ext)
        classified[cat].append(ext)
    
    print(f"\nClassification:")
    for cat, exts in classified.items():
        print(f"  {cat}: {len(exts)}")
    
    # Need at least 30 per arm for G1 gate (from STATE.md constraints)
    if len(classified["need-related"]) < 30:
        print(f"\nWARNING: need-related group has only {len(classified['need-related'])} extensions (< 30 G1 threshold)")
    if len(classified["general"]) < 30:
        print(f"WARNING: general group has only {len(classified['general'])} extensions (< 30 G1 threshold)")
    
    # Compute statistics for install count (primary activity metric)
    for cat, exts in classified.items():
        if exts:
            installs = [e.install_count for e in exts]
            installs.sort()
            print(f"\n{cat} install counts:")
            print(f"  n={len(installs)}")
            print(f"  median={installs[len(installs)//2]}")
            print(f"  mean={sum(installs)/len(installs):.1f}")
            print(f"  min={installs[0]}, max={installs[-1]}")
            print(f"  p25={installs[len(installs)//4]}, p75={installs[3*len(installs)//4]}")
    
    # Compare need-related vs general (primary comparison)
    if classified["need-related"] and classified["general"]:
        need_installs = [e.install_count for e in classified["need-related"]]
        general_installs = [e.install_count for e in classified["general"]]
        
        delta = compute_cliffs_delta(need_installs, general_installs)
        print(f"\nCliff's delta (need-related vs general): {delta:.4f}")
        
        # Also compute for other metrics
        for metric_name in ["average_rating", "rating_count", "trending_monthly", "update_count", "download_count"]:
            need_vals = [getattr(e, metric_name) for e in classified["need-related"]]
            general_vals = [getattr(e, metric_name) for e in classified["general"]]
            delta_m = compute_cliffs_delta(need_vals, general_vals)
            print(f"  {metric_name}: delta={delta_m:.4f}")
    
    # Compare need-related vs other
    if classified["need-related"] and classified["other"]:
        need_installs = [e.install_count for e in classified["need-related"]]
        other_installs = [e.install_count for e in classified["other"]]
        delta = compute_cliffs_delta(need_installs, other_installs)
        print(f"\nCliff's delta (need-related vs other): {delta:.4f}")
    
    # Compare general vs other
    if classified["general"] and classified["other"]:
        general_installs = [e.install_count for e in classified["general"]]
        other_installs = [e.install_count for e in classified["other"]]
        delta = compute_cliffs_delta(general_installs, other_installs)
        print(f"\nCliff's delta (general vs other): {delta:.4f}")
    
    # Save raw data
    output = {
        "extensions": [asdict(e) for e in unique_extensions],
        "classification": {cat: [asdict(e) for e in exts] for cat, exts in classified.items()},
        "summary": {
            "total": len(unique_extensions),
            "need_related": len(classified["need-related"]),
            "general": len(classified["general"]),
            "other": len(classified["other"]),
        }
    }
    
    with open("/home/ubuntu/think-free/EXPERIMENTS/165-vscode-marketplace-viewcount/raw_data.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print("\nRaw data saved to raw_data.json")
    return 0

if __name__ == "__main__":
    sys.exit(main())
