#!/usr/bin/env python3
"""
E146 — View-count principle on GitHub repositories (cross-platform classifier test).

Uses the E107 already-harvested GitHub repository data to test whether the
view-count classifier (developed for Reddit technical communities) generalizes
to repo descriptions/titles. This is a "fresh observation in a new domain axis"
per D083: applying an existing measurement methodology to a different platform.
"""

import json
import os
import re
import sys
from math import sqrt, erfc


# Vocabulary from E116/vocab.py — terms suggesting a programming need.
NEED_INDICATORS = {
    "web", "rest", "api", "http", "client", "server", "framework",
    "database", "orm", "sql", "postgres", "mysql", "mariadb", "redis",
    "mongo", "mongodb", "elasticsearch", "couchdb", "storage", "cache",
    "persistent", "state",
    "auth", "oauth", "oidc", "jwt", "session", "cookie", "security",
    "encrypt", "decrypt", "sign", "verify", "validator", "schema",
    "socket", "tcp", "udp", "grpc", "websocket",
    "pubsub", "messaging", "queue", "topic", "broker", "channel",
    "test", "mock", "fixture", "benchmark", "profile", "fuzz",
    "continuous", "integration", "deployment",
    "cli", "command", "argument", "flag", "option",
    "migration", "schema", "seed", "factory",
    "ecto", "phoenix", "plug", "absinthe", "tesla", "finch",
    "httpoison", "jason", "poison",
    "socket", "tcp", "udp",
    "web", "rest", "api",
    "database", "orm", "sql",
    "auth", "security",
    "test", "mock",
    "cli", "command",
}

# Truly generic terms: disqualifying when present (with disambiguation).
GENERIC_TERMS = {
    "base", "minimal", "alpine", "scratch", "distroless", "slim",
    "latest", "stable", "edge", "main", "master", "dev", "test",
    "example", "demo", "sample", "template", "boilerplate",
    "sandbox", "playground", "poc", "prototype", "experiment",
    "tutorial", "learning", "workshop",
    "personal", "private", "internal", "custom",
    "fork", "mirror", "copy", "backup", "archive", "old",
    "deprecated", "legacy", "unmaintained", "abandoned",
    "utils", "common", "core", "library", "package", "tool", "util",
    "helper",
    "ci", "build", "builder", "compile", "runtime", "debug",
    "example", "demo", "tutorial",
}

DISAMBIG_WINDOW = 3


def tokenize(text):
    """Tokenize text into lowercase words, preserving hyphens within words."""
    if not text:
        return []
    tokens = re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)*", text.lower())
    return tokens


def has_need_context(tokens, idx, need_set, generic_set, window=DISAMBIG_WINDOW):
    """Check if NEED_INDICATORS[idx] carries need-specific context."""
    token = tokens[idx]
    if token not in need_set:
        return False
    if token not in generic_set:
        return True
    start = max(0, idx - window)
    end = min(len(tokens), idx + window + 1)
    for j in range(start, end):
        if j == idx:
            continue
        if tokens[j] in need_set:
            return True
    for offset in range(1, window + 1):
        if idx - offset >= 0 and tokens[idx - offset] in need_set:
            return True
        if idx + offset < len(tokens) and tokens[idx + offset] in need_set:
            return True
    return False


def classify_title(title):
    """Classify a title/description as need-related, random, or uncertain.

    Adapted from E116 classify_description for GitHub repo titles/descriptions.
    Returns (classification, reason, weight).
    weight >= 0.5 = classified; 0.0 = uncertain.
    """
    if not title:
        return "uncertain", "no title", 0.0

    tokens = tokenize(title)
    if not tokens:
        return "uncertain", "no tokens after parsing", 0.0

    need_matches = 0
    generic_matches = 0
    need_indices = []
    generic_indices = []

    for i, tok in enumerate(tokens):
        if tok in NEED_INDICATORS:
            if has_need_context(tokens, i, NEED_INDICATORS, GENERIC_TERMS, DISAMBIG_WINDOW):
                need_matches += 1
                need_indices.append(i)
            else:
                need_matches += 0.5
                need_indices.append(i)
        if tok in GENERIC_TERMS:
            generic_matches += 1
            generic_indices.append(i)

    effective_need = sum(
        1.0 for i in need_indices
        if has_need_context(tokens, i, NEED_INDICATORS, GENERIC_TERMS, DISAMBIG_WINDOW)
    )

    # Fallback: check title for question/problem/request/technical patterns
    title_lower = title.lower()

    question_patterns = [
        "how do", "how can", "how to", "why does", "what is",
        "how does", "how is", "how would", "how will", "how could",
        "can you", "could you", "would you", "can anyone",
        "could anyone", "would anyone", "does anyone", "do you",
        "is there", "are there",
    ]
    problem_patterns = [
        "fix", "debug", "error", "issue", "problem", "bug",
        "crash", "fail", "exception", "not working", "cannot",
        "stuck", "help",
    ]
    request_patterns = [
        "help me", "please help", "need help", "advice",
        "suggest", "recommend", "guidance",
    ]
    technical_patterns = [
        "lint", "format", "refactor", "test", "deploy",
        "ci", "cd", "git", "docker", "kubernetes",
        "api", "database", "sql", "nosql",
    ]

    has_question = any(p in title_lower for p in question_patterns)
    has_problem = any(p in title_lower for p in problem_patterns)
    has_request = any(p in title_lower for p in request_patterns)
    has_technical = any(p in title_lower for p in technical_patterns)

    # Classification logic
    if effective_need > 0 and generic_matches > 0:
        if effective_need > generic_matches:
            return "need-related", f"{int(effective_need)} need-specific token(s) outweigh {generic_matches} generic tokens", 1.0
        else:
            return "random", f"{int(effective_need)} need token(s) but {generic_matches} generic dominates", 0.7

    if effective_need == 0 and generic_matches > 0:
        return "random", f"{int(generic_matches)} generic token(s), no need-specific signals", 0.0

    if effective_need == 0 and generic_matches == 0:
        if has_question or has_problem or has_request or has_technical:
            return "need-related", f"title matches question/problem/request/technical patterns", 0.8
        return "uncertain", "no recognized need or generic tokens", 0.0

    if effective_need > 0 and generic_matches == 0:
        return "need-related", f"{int(effective_need)} need-specific token(s) found", 1.0

    return "random", "classified as random", 0.7


def cliff_delta(x, y):
    """Compute Cliff's delta for two independent samples."""
    if not x or not y:
        return 0.0
    nx = len(x)
    ny = len(y)
    greater = 0
    less = 0
    for xi in x:
        for yi in y:
            if xi > yi:
                greater += 1
            elif xi < yi:
                less += 1
    return (greater - less) / (nx * ny)


def mann_whitney_u(x, y):
    """Compute Mann-Whitney U test statistic and two-sided p-value."""
    if not x or not y:
        return 0.0, 1.0
    nx = len(x)
    ny = len(y)
    combined = sorted(x + y)
    n = len(combined)
    rank_map = {}
    i = 0
    while i < n:
        val = combined[i]
        j = i
        while j < n and combined[j] == val:
            j += 1
        avg_rank = (i + j - 1) / 2.0 + 1
        for k in range(i, j):
            rank_map[combined[k]] = avg_rank
        i = j
    rx = sum(rank_map.get(v, 1) for v in x)
    ux = rx - nx * (nx + 1) / 2
    mu_u = nx * ny / 2.0
    sigma_u_sq = nx * ny * (nx + ny + 1) / 12.0
    if sigma_u_sq > 0:
        z = (ux - mu_u) / (sigma_u_sq ** 0.5)
        p = erfc(abs(z) / (2 ** 0.5))
    else:
        z = 0
        p = 1.0
    return ux, p


def wilson_ci_lower(p, n, z=1.96):
    """Wilson score interval lower bound at 95% confidence."""
    if n == 0:
        return 0.0
    denominator = 1 + z**2 / n
    centre = p + z**2 / (2 * n)
    adjustment = z * sqrt(p * (1 - p) / n + z**2 / (4 * n**2))
    return (centre - adjustment) / denominator


def main():
    # Load E107 raw harvest data
    raw_path = "EXPERIMENTS/107-github-repos-viewcount/raw_data.json"
    if not os.path.exists(raw_path):
        print(f"Error: {raw_path} not found.")
        sys.exit(1)

    with open(raw_path) as f:
        all_repos = json.load(f)

    print("=" * 60)
    print("E146 — View-count principle on GitHub repositories")
    print("(cross-platform classifier test using E107 data)")
    print("=" * 60)
    print()

    total = len(all_repos)
    print(f"Total repositories: {total}")

    # Step 1: Classify each repo's description/name
    print("Classifying repos...")
    need_related = []
    random_posts = []
    uncertain = []

    for repo in all_repos:
        name = repo.get("full_name", repo.get("name", ""))
        description = repo.get("description", "")

        if description:
            cls, reason, weight = classify_title(description)
        else:
            cls, reason, weight = classify_title(name)

        if cls == "need-related":
            need_related.append(repo)
        elif cls == "random":
            random_posts.append(repo)
        else:
            uncertain.append(repo)

    need_count = len(need_related)
    random_count = len(random_posts)
    unc_count = len(uncertain)
    classified_count = need_count + random_count

    print(f"  Need-related: {need_count}")
    print(f"  Random: {random_count}")
    print(f"  Uncertain: {unc_count}")
    print(f"  Classified (weight >= 0.5): {classified_count}/{total} = {classified_count/total*100:.1f}%")

    # Step 2: Engagement metric = star count
    print("\nEngagement metric: stargazers_count")

    need_stars = [r.get("stargazers_count", 0) for r in need_related]
    random_stars = [r.get("stargazers_count", 0) for r in random_posts]

    if need_stars:
        need_median_stars = sorted(need_stars)[len(need_stars) // 2]
        print(f"  Need-related median stars: {need_median_stars}")
    else:
        need_median_stars = 0
        print(f"  Need-related: no data")

    if random_stars:
        random_median_stars = sorted(random_stars)[len(random_stars) // 2]
        print(f"  Random median stars: {random_median_stars}")
    else:
        random_median_stars = 0
        print(f"  Random: no data")

    # Step 3: Gate evaluation
    print("\n=== GATE ASSESSMENT ===")

    # G1: Classified sample size >= 100 total (50 per group minimum)
    g1_pass = classified_count >= 100 and need_count >= 50 and random_count >= 50
    print(f"G1 - Classified sample size >= 100 (50 per group): {'PASS' if g1_pass else 'FAIL'}")
    print(f"  Total classified: {classified_count} (need: {need_count}, random: {random_count})")

    # G2: Coverage floor >= 80%
    coverage_rate = classified_count / total if total > 0 else 0
    g2_pass = coverage_rate >= 0.80
    print(f"G2 - Coverage floor >= 80%: {'PASS' if g2_pass else 'FAIL'}")
    print(f"  Coverage rate: {coverage_rate:.1%} ({classified_count}/{total})")

    # G3: Cliff's delta & Mann-Whitney U on star counts
    if need_stars and random_stars:
        delta = cliff_delta(need_stars, random_stars)
        u_stat, p_value = mann_whitney_u(need_stars, random_stars)
        g3_pass = delta > 0.147 and p_value < 0.05
        print(f"G3 - Cliff's delta > 0.147 & Mann-Whitney U p < 0.05: {'PASS' if g3_pass else 'FAIL'}")
        print(f"  Cliff's delta: {delta:.4f}")
        print(f"  p-value: {p_value:.6f}")
    else:
        g3_pass = False
        delta = 0.0
        p_value = 1.0
        print(f"G3 - Cliff's delta & p-value: FAIL (insufficient data)")

    # G4: Both categories represented
    g4_pass = need_count > 0 and random_count > 0
    print(f"G4 - Both categories represented: {'PASS' if g4_pass else 'FAIL'}")
    print(f"  Need-related: {need_count}, Random: {random_count}")

    # Overall
    all_pass = g1_pass and g2_pass and g3_pass and g4_pass
    verdict = "ALL GATES PASS — Principle supported on GitHub repositories (cross-platform)" if all_pass else "SOME GATES FAILED — Principle not supported on GitHub repositories (cross-platform)"
    conclusion = "Classifier generalizes from Reddit to GitHub repos" if all_pass else "Classifier does not generalize from Reddit to GitHub repos"

    print(f"\n=== Overall: {verdict} ===")
    print(f"Conclusion: {conclusion}")

    # Write results.json
    results = {
        "experiment": "E146",
        "platform": "GitHub repositories (cross-platform test)",
        "source_data": "E107 GitHub repos harvest (160 repos)",
        "total_harvested": total,
        "classified": {
            "need_related": need_count,
            "random": random_count,
            "uncertain": unc_count,
            "total_classified": classified_count,
            "coverage_rate": classified_count / total if total > 0 else 0,
        },
        "engagement": {
            "need_median_stars": need_median_stars if need_stars else 0,
            "random_median_stars": random_median_stars if random_stars else 0,
            "need_star_count": len(need_stars),
            "random_star_count": len(random_stars),
        },
        "gate_results": {
            "g1_pass": g1_pass,
            "g2_pass": g2_pass,
            "g3_pass": g3_pass,
            "g4_pass": g4_pass,
            "cliff_delta": delta,
            "p_value": p_value,
        },
        "all_pass": all_pass,
        "verdict": verdict,
        "conclusion": conclusion,
    }

    output_path = "EXPERIMENTS/146-reddit-viewcount/results.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults written to {output_path}")

    sys.exit(0 if all_pass else 2)


if __name__ == "__main__":
    main()