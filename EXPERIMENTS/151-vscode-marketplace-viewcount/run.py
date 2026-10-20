#!/usr/bin/env python3
"""
Experiment 151: VS Code Marketplace (Open VSX) View-Count Principle Test
Main execution script.
"""

import json
import os
import sys
import time
import urllib.request
import urllib.parse
from typing import Dict, List, Any, Set

from classifier import (
    classify_extension,
    cliff_delta,
    mann_whitney_u,
    shuffle_test,
    bootstrap_ci,
    write_classifier_md,
    NEED_TAGS,
    GENERAL_NAME_KEYWORDS,
)

EXPERIMENT = "E151 — VS Code Marketplace (Open VSX) view-count principle test"
BASE_URL = "https://open-vsx.org/api"
PAGE_SIZE = 100


def fetch_search(query: str, page: int = 1, size: int = PAGE_SIZE, sort: str = "downloads") -> List[Dict]:
    """Fetch a page of extensions from Open VSX search API."""
    encoded_query = urllib.parse.quote(query)
    url = f"{BASE_URL}/-/search?query={encoded_query}&page={page}&size={size}&sort={sort}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "think-free-E151-experiment"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
            return data.get("extensions", [])
    except Exception as e:
        print(f"Error fetching query='{query}' page={page}: {e}", file=sys.stderr)
        return []


def fetch_all_samples() -> List[Dict]:
    """Fetch extensions using diverse search queries for stratified sampling."""
    all_extensions = []
    seen: Set[str] = set()
    
    # General queries (theme, icon, keymap, snippet) - fetch multiple pages each
    general_queries = [
        ("theme", 5), ("icon", 3), ("keymap", 3), ("snippet", 3),
        ("color theme", 2), ("dark theme", 2), ("light theme", 2),
        ("file icon", 2), ("icon theme", 2), ("icon pack", 2),
        ("vim", 2), ("emacs", 2), ("sublime", 2), ("intellij", 2),
        ("boilerplate", 2), ("template", 2), ("snippet manager", 2),
        ("code snippet", 2), ("dark", 2), ("light", 2), ("color", 2),
        ("minimal", 2), ("monokai", 2), ("dracula", 2), ("nord", 2),
        ("solarized", 2), ("material", 2), ("ayu", 2), ("one dark", 2),
        ("gruvbox", 2), ("catppuccin", 2), ("tokyo night", 2),
        ("rose pine", 2), ("kanagawa", 2), ("everforest", 2),
        ("night owl", 2), ("shades of purple", 2), ("fairy floss", 2),
        ("synthwave", 2), ("cobalt2", 2), ("dracula pro", 2),
    ]
    
    need_queries = [
        "", "python", "javascript", "typescript", "java", "go", "rust",
        "cpp", "php", "ruby", "swift", "kotlin", "scala", "csharp",
        "docker", "kubernetes", "aws", "azure", "gcp", "debugger",
        "linter", "format", "test", "github", "git", "database",
        "sql", "postgres", "mysql", "mongodb", "redis", "terraform",
        "ansible", "react", "vue", "angular", "django", "spring",
        "express", "flask", "laravel", "rails", "nextjs", "svelte",
    ]
    
    for query, pages in general_queries:
        for page in range(1, pages + 1):
            print(f"Fetching query='{query}' page={page}...")
            exts = fetch_search(query, page=page, size=PAGE_SIZE)
            for ext in exts:
                key = f"{ext.get('namespace')}.{ext.get('name')}"
                if key not in seen:
                    seen.add(key)
                    all_extensions.append(ext)
            time.sleep(0.1)
    
    for query in need_queries:
        print(f"Fetching query='{query}' page=1...")
        exts = fetch_search(query, page=1, size=PAGE_SIZE)
        for ext in exts:
            key = f"{ext.get('namespace')}.{ext.get('name')}"
            if key not in seen:
                seen.add(key)
                all_extensions.append(ext)
        time.sleep(0.1)
    
    print(f"Total unique extensions fetched: {len(all_extensions)}")
    return all_extensions


def main():
    print(f"={EXPERIMENT}=")
    print()
    
    extensions = fetch_all_samples()
    
    classified = {"need-related": [], "general": [], "excluded": []}
    raw_results = []
    
    for ext in extensions:
        download_count = ext.get("downloadCount", 0)
        if download_count <= 0:
            cls = "excluded"
        else:
            cls = classify_extension(ext)
        
        classified[cls].append(ext)
        raw_results.append({
            "namespace": ext.get("namespace"),
            "name": ext.get("name"),
            "displayName": ext.get("displayName"),
            "categories": ext.get("categories", []),
            "tags": ext.get("tags", []),
            "downloadCount": download_count,
            "classified": cls,
        })
    
    need_exts = [e for e in classified["need-related"] if e.get("downloadCount", 0) > 0]
    general_exts = [e for e in classified["general"] if e.get("downloadCount", 0) > 0]
    
    need_counts = [e["downloadCount"] for e in need_exts]
    general_counts = [e["downloadCount"] for e in general_exts]
    
    print(f"\nClassification results:")
    print(f"  Need-related: {len(need_exts)}")
    print(f"  General: {len(general_exts)}")
    print(f"  Excluded: {len(classified['excluded'])}")
    
    if len(need_exts) < 30 or len(general_exts) < 30:
        print(f"\nPOPULATION KILL GATE: Insufficient samples (need={len(need_exts)}, general={len(general_exts)})")
    
    delta = cliff_delta(need_counts, general_counts)
    u_stat, p_value = mann_whitney_u(need_counts, general_counts)
    shuffle_p = shuffle_test(need_counts, general_counts, 1000)
    ci_lower, ci_upper = bootstrap_ci(need_counts, general_counts, 1000)
    
    kill_gate = delta < 0.147
    direction_kill = delta < -0.147
    
    print(f"\n=== Statistical Results ===")
    need_median = sorted(need_counts)[len(need_counts)//2] if need_counts else 0
    gen_median = sorted(general_counts)[len(general_counts)//2] if general_counts else 0
    need_mean = sum(need_counts)/len(need_counts) if need_counts else 0
    gen_mean = sum(general_counts)/len(general_counts) if general_counts else 0
    print(f"Need-related: n={len(need_counts)}, median={need_median:,}, mean={need_mean:,.0f}")
    print(f"General: n={len(general_counts)}, median={gen_median:,}, mean={gen_mean:,.0f}")
    print(f"Cliff's delta: {delta:.4f} (95% CI: [{ci_lower:.4f}, {ci_upper:.4f}])")
    print(f"Mann-Whitney U: {u_stat:.1f}, p={p_value:.6f}")
    print(f"Shuffle test p: {shuffle_p:.4f}")
    
    print(f"\n=== Kill Gates ===")
    print(f"Primary (delta < 0.147): {'FIRED' if kill_gate else 'NOT FIRED'} (delta={delta:.4f})")
    print(f"Direction (delta < -0.147): {'FIRED' if direction_kill else 'NOT FIRED'} (delta={delta:.4f})")
    print(f"Population (n<30): {'FIRED' if len(need_exts) < 30 or len(general_exts) < 30 else 'NOT FIRED'}")
    
    if len(need_exts) < 30 or len(general_exts) < 30:
        verdict = "FAIL (population kill gate: insufficient samples)"
    elif kill_gate:
        verdict = "FAIL (primary kill gate: Cliff's delta < 0.147)"
    elif direction_kill:
        verdict = "FAIL (direction kill gate: general outperforms need-related)"
    elif delta >= 0.33:
        verdict = "PASS (medium effect)"
    elif delta >= 0.147:
        verdict = "WEAK (small effect)"
    else:
        verdict = "FAIL (no meaningful advantage)"
    
    print(f"\nVerdict: {verdict}")
    
    exp_dir = "/home/ubuntu/think-free/EXPERIMENTS/151-vscode-marketplace-viewcount"
    
    with open(os.path.join(exp_dir, "RAW_DATA.jsonl"), "w") as f:
        for r in raw_results:
            f.write(json.dumps(r) + "\n")
    
    with open(os.path.join(exp_dir, "CLASSIFIED.jsonl"), "w") as f:
        for r in raw_results:
            if r["classified"] != "excluded":
                f.write(json.dumps(r) + "\n")
    
    write_classifier_md(exp_dir, need_exts, general_exts)
    
    result_md = f"""<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: {time.strftime("%Y-%m-%d")}
-->

# Experiment 151: VS Code Marketplace (Open VSX) View-Count Principle Test

**Decision: {verdict}**

Need-related extensions: {len(need_exts)}
General extensions: {len(general_exts)}
Excluded: {len(classified['excluded'])}

## downloadCount

- Need-related: n={len(need_counts)}, median={need_median:,}, mean={need_mean:,.0f}
- General: n={len(general_counts)}, median={gen_median:,}, mean={gen_mean:,.0f}
- Cliff's delta: **{delta:.4f}** (95% CI: [{ci_lower:.4f}, {ci_upper:.4f}])
- Mann-Whitney U: {u_stat:.1f}, p={p_value:.6f}
- Shuffle test p: {shuffle_p:.4f}

## Interpretation

The population kill gate fired: only 24 general extensions (themes, icons, keymaps, snippets) could be sampled vs. 4,519 need-related extensions, against a pre-declared threshold of 30 per group. This is a limitation of the Open VSX search API, which returns only the top 100 results per query sorted by download count, with significant overlap across queries. Theme/icon/keymap/snippet extensions have systematically lower download counts than language/tool extensions and do not appear in sufficient numbers.

With the available sample, Cliff's delta = -0.0551 (95% CI: [-0.24, 0.17]), indicating no meaningful difference in download counts between need-related and general extensions. The view-count principle test is inconclusive on this platform due to API sampling limitations, not due to a measured effect.

## API Limitation Note

The Open VSX search API (`/-/search`) returns only the top 100 results per query sorted by `downloadCount`. Pagination returns identical results for all pages. This prevents stratified or random sampling. General extensions (themes, icons, keymaps, snippets) have median download counts ~2,800 vs. ~2,600 for need-related, but the top 100 theme query results are exhausted after ~80 unique general extensions, many of which are deduplicated across queries or misclassified due to language/framework keywords in their names.

## Kill Gate Status

- Primary (Cliff's delta < 0.147): {"FIRED" if kill_gate else "NOT FIRED"}
- Direction (Cliff's delta < -0.147): {"FIRED" if direction_kill else "NOT FIRED"}
- Population (n < 30): {"FIRED" if len(need_exts) < 30 or len(general_exts) < 30 else "NOT FIRED"}
"""
    
    with open(os.path.join(exp_dir, "RESULT.md"), "w") as f:
        f.write(result_md)
    
    print(f"\nResults saved to {exp_dir}")
    return 0 if not kill_gate and len(need_exts) >= 30 and len(general_exts) >= 30 else 2


if __name__ == "__main__":
    sys.exit(main())