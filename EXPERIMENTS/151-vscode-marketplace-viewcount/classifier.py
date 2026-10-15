#!/usr/bin/env python3
"""
Experiment 151: VS Code Marketplace (Open VSX) View-Count Principle Test
Classification rules and statistical functions.
"""

import math
import os
import random
import time
from typing import Dict, List, Any, Set

# ── Classification Rules (Pre-declared) ────────────────────────────────

NEED_CATEGORIES = {
    "Programming Languages", "Debuggers", "Linters", "Formatters",
    "Language Packs", "Cloud", "Databases", "Testing", "CI/CD",
    "Containers", "Machine Learning", "AI", "Data Science",
    "Mobile Development", "Game Development", "IoT", "Embedded"
}

NEED_TAGS = {
    # Languages
    "python", "javascript", "typescript", "java", "go", "golang", "rust",
    "cpp", "c++", "csharp", "c#", "php", "ruby", "swift", "kotlin",
    "scala", "r", "matlab", "julia", "dart", "lua", "perl", "haskell",
    "clojure", "elixir", "erlang", "fsharp", "f#", "ocaml", "vbnet",
    "vb.net", "powershell", "bash", "shell", "sql",
    # Frameworks
    "react", "vue", "angular", "django", "flask", "spring", "express",
    "nextjs", "next.js", "nuxt", "svelte", "laravel", "rails", "aspnet",
    "asp.net", "dotnet", ".net",
    # Cloud/DevOps
    "aws", "azure", "gcp", "google-cloud", "kubernetes", "k8s", "docker",
    "terraform", "ansible", "helm", "prometheus", "grafana",
    # Databases
    "postgresql", "postgres", "mysql", "mongodb", "mongo", "redis",
    "sqlite", "dynamodb", "cassandra", "mariadb",
    # Tool purposes
    "debugger", "debug", "lint", "linter", "format", "formatter",
    "test", "testing", "ci", "cd", "github", "gitlab", "bitbucket",
    "language server", "intellisense", "completion", "refactor",
    "profiler", "profiling", "language-support"
}

GENERAL_CATEGORIES = {"Themes", "Icon Themes", "Keymaps", "Snippets"}

GENERAL_TAGS = {
    "theme", "color-theme", "dark-theme", "light-theme", "color-scheme",
    "icon-theme", "icons", "file-icons", "folder-icons", "icon-pack",
    "keymap", "keybinding", "vim", "emacs", "sublime-text", "sublime",
    "snippet", "boilerplate", "template"
}

GENERAL_NAME_KEYWORDS = {
    "theme", "dark", "light", "color", "icon", "keymap", "keybinding",
    "vim", "emacs", "sublime", "snippet", "boilerplate", "template"
}


def classify_extension(ext: Dict[str, Any]) -> str:
    """Classify extension as need-related, general, or excluded."""
    categories = set(ext.get("categories", []))
    tags = set(t.lower() for t in ext.get("tags", []))
    name = ext.get("name", "").lower()
    display_name = ext.get("displayName", "").lower()
    description = ext.get("description", "").lower()
    
    # Check need-related categories
    if categories & NEED_CATEGORIES:
        return "need-related"
    
    # Check need-related tags
    if tags & NEED_TAGS:
        return "need-related"
    
    # Check name/description for need-related keywords
    text = f"{name} {display_name} {description}"
    for kw in NEED_TAGS:
        if kw in text:
            return "need-related"
    
    # Check general categories
    if categories & GENERAL_CATEGORIES:
        if not (categories & NEED_CATEGORIES):
            return "general"
    
    # Check general tags
    if tags & GENERAL_TAGS:
        if not (tags & NEED_TAGS):
            return "general"
    
    # Check name for general keywords
    name_text = f"{name} {display_name}"
    if any(kw in name_text for kw in GENERAL_NAME_KEYWORDS):
        if not any(kw in text for kw in NEED_TAGS):
            return "general"
    
    # Default: excluded
    return "excluded"


def cliff_delta(x: List[float], y: List[float]) -> float:
    """Compute Cliff's delta effect size."""
    if not x or not y:
        return 0.0
    n_x, n_y = len(x), len(y)
    greater = sum(1 for xi in x for yj in y if xi > yj)
    less = sum(1 for xi in x for yj in y if xi < yj)
    return (greater - less) / (n_x * n_y)


def mann_whitney_u(x: List[float], y: List[float]) -> tuple:
    """Compute Mann-Whitney U test statistic and p-value (approximate)."""
    if not x or not y:
        return 0.0, 1.0
    
    combined = [(v, 0) for v in x] + [(v, 1) for v in y]
    combined.sort(key=lambda t: t[0])
    
    n_x, n_y = len(x), len(y)
    rank_sum_x = sum(i + 1 for i, (_, g) in enumerate(combined) if g == 0)
    
    u_x = rank_sum_x - n_x * (n_x + 1) / 2
    u_y = n_x * n_y - u_x
    u = min(u_x, u_y)
    
    # Normal approximation for p-value
    mean_u = n_x * n_y / 2
    std_u = math.sqrt(n_x * n_y * (n_x + n_y + 1) / 12)
    if std_u == 0:
        return u, 1.0
    z = (u - mean_u) / std_u
    # Two-tailed p-value
    from math import erf, sqrt
    p = 2 * (1 - 0.5 * (1 + erf(abs(z) / sqrt(2))))
    return u, p


def shuffle_test(x: List[float], y: List[float], n_perm: int = 1000) -> float:
    """Permutation test for Cliff's delta."""
    if not x or not y:
        return 1.0
    combined = x + y
    n_x = len(x)
    observed = cliff_delta(x, y)
    count = 0
    for _ in range(n_perm):
        random.shuffle(combined)
        perm_x = combined[:n_x]
        perm_y = combined[n_x:]
        if cliff_delta(perm_x, perm_y) >= observed:
            count += 1
    return count / n_perm


def bootstrap_ci(x: List[float], y: List[float], n_boot: int = 1000) -> tuple:
    """Bootstrap confidence interval for Cliff's delta."""
    if not x or not y:
        return 0.0, 0.0
    boot_deltas = []
    for _ in range(n_boot):
        boot_need = [random.choice(x) for _ in x]
        boot_gen = [random.choice(y) for _ in y]
        boot_deltas.append(cliff_delta(boot_need, boot_gen))
    boot_deltas.sort()
    ci_lower = boot_deltas[int(0.025 * n_boot)]
    ci_upper = boot_deltas[int(0.975 * n_boot)]
    return ci_lower, ci_upper


def write_classifier_md(exp_dir: str, need_exts: List[Dict], general_exts: List[Dict]):
    """Write CLASSIFIER.md documentation."""
    import time
    classifier_md = f"""<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: {time.strftime("%Y-%m-%d")}
-->

# Classifier Documentation for E151

## Need-Related Categories
{', '.join(sorted(NEED_CATEGORIES))}

## Need-Related Tags ({len(NEED_TAGS)} tags)
{', '.join(sorted(NEED_TAGS))}

## General Categories
{', '.join(sorted(GENERAL_CATEGORIES))}

## General Tags ({len(GENERAL_TAGS)} tags)
{', '.join(sorted(GENERAL_TAGS))}

## General Name Keywords
{', '.join(sorted(GENERAL_NAME_KEYWORDS))}

## Examples

### Need-Related
"""
    for ext in need_exts[:10]:
        tags = ext.get('tags') or []
        classifier_md += f"- `{ext.get('namespace')}.{ext.get('name')}`: {ext.get('displayName')} (categories: {ext.get('categories')}, tags: {tags[:5]})\n"
    
    classifier_md += "\n### General\n"
    for ext in general_exts[:10]:
        tags = ext.get('tags') or []
        classifier_md += f"- `{ext.get('namespace')}.{ext.get('name')}`: {ext.get('displayName')} (categories: {ext.get('categories')}, tags: {tags[:5]})\n"
    
    with open(os.path.join(exp_dir, "CLASSIFIER.md"), "w") as f:
        f.write(classifier_md)