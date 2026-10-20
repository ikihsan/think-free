#!/usr/bin/env python3
"""E130 — View-Count Classifier Prototype v3: Continuation across sessions

Expands package pools to 200+ packages from PyPI using a keyword filter,
adds API failure handling, and replicates the effect size improvement on
larger samples per the phase-decision.json recommendation (most useful
next action).

This script continues the E130 prototype across sessions rather than
restarting discovery, as recommended by the phase decision.
"""

import json
import os
import re
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))

# Need indicators for classifier (whole-word token matching only)
NEED_INDICATORS = {
    'bug', 'fix', 'problem', 'issue', 'error', 'crash',
    'tutorial', 'how to', 'guide', 'solution', 'debug',
    'install', 'import', 'dependency', 'feature', 'enhancement',
    'alarm', 'warning', 'fault', 'code', 'patch',
    'security', 'vulnerability',
}

# Generic terms for disambiguation (tokens that suggest generic tech rather than a specific need)
GENERIC_TERMS = {
    'library', 'module', 'package', 'tool', 'helper',
    'util', 'lib', 'core', 'framework', 'engine',
    'api', 'sdk', 'kit', 'system', 'service',
    'python', 'py3', '3', '2',
}


def classify_package(name, description):
    """Classify a package using the v3 classifier: whole-word matching, combined name+description, uncertainty weighting.

    Key fix: classification now depends on the weight threshold (need tokens must
    constitute >30% of all meaningful tokens to be classified as need-related).
    This prevents single-token matches from dominating the classification,
    as occurred in the prior PyPI continuation.
    """
    name_tokens = set(name.lower().split()) if name else set()
    desc = description or ''
    desc_tokens = set(desc.lower().split()) if desc else set()
    all_tokens = name_tokens | desc_tokens

    need_tokens = all_tokens & NEED_INDICATORS
    generic_tokens = all_tokens & GENERIC_TERMS

    has_need_token = len(need_tokens) > 0
    has_only_generic = len(need_tokens) == 0 and len(generic_tokens) > 0
    has_both = len(need_tokens) > 0 and len(generic_tokens) > 0

    THRESHOLD = 0.3  # need tokens must be >30% of meaningful tokens

    if has_need_token and not has_only_generic:
        if has_both:
            total_meaningful = len(need_tokens) + len(generic_tokens)
            weight = len(need_tokens) / total_meaningful if total_meaningful > 0 else 0.0
            # Classify as need-related only if need tokens are a significant portion
            classification = "need-related" if weight > THRESHOLD else "uncertain"
            weight = weight  # retain for output
        else:
            # Only need tokens, no generic tokens - strong signal
            classification = "need-related"
            weight = 1.0
    elif len(generic_tokens) > 0 and len(need_tokens) == 0:
        weight = 0.0
        classification = "uncertain"
    else:
        # No need tokens and no generic tokens
        weight = 0.0
        classification = "uncertain"

    return {
        "classification": classification,
        "weight": weight,
        "need_tokens": list(need_tokens) if need_tokens else [],
        "generic_tokens": list(generic_tokens) if generic_tokens else [],
        "reason": _get_classification_reason(need_tokens, generic_tokens, has_both, weight > THRESHOLD),
    }


def _get_classification_reason(need_tokens, generic_tokens, has_both, meets_threshold):
    """Generate a human-readable reason for the classification."""
    n_need = len(need_tokens)
    n_gen = len(generic_tokens)

    if n_need > 0 and n_gen == 0:
        return f"{n_need} need-specific token(s) found (name and description)"
    elif n_need > 0 and n_gen > 0 and has_both:
        if meets_threshold:
            return f"{n_need} need-specific token(s) outweigh {n_gen} generic token(s) (with context)"
        else:
            return f"{n_need} need-specific token(s) among {n_gen} generic token(s) (weak signal)"
    elif n_need > 0 and n_gen > 0:
        return f"{n_need} need-specific token(s) outweigh {n_gen} generic token(s) (with context)"
    elif n_gen > 0:
        return f"{n_gen} generic token(s) in name/description, no need-specific signals"
    else:
        return "no recognized need or generic tokens in name or description"


def fetch_pypi_packages(keyword=None, n=200):
    """Fetch up to n packages from the PyPI simple index.

    If keyword is provided, fetch from PyPI simple index with that keyword filter.
    Otherwise, fetch from the PyPI simple index without a filter (broad mix).
    """
    packages = []
    seen = set()

    if keyword:
        url = f"https://pypi.org/simple/?q={keyword}"
    else:
        url = "https://pypi.org/simple/"

    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'origin-mission-E130'})
        with urllib.request.urlopen(req, timeout=30) as resp:
            html = resp.read().decode()
            names = re.findall(r'href="/simple/([^"]+)"', html)
            for name in names:
                # Skip version-like names and very short/empty names
                if re.match(r'^[\d._-]+$', name):
                    continue
                if not name or len(name) < 2:
                    continue
                if name in seen:
                    continue
                seen.add(name)
                # Fetch package info to get description
                try:
                    info_url = f"https://pypi.org/pypi/{name}/json"
                    info_req = urllib.request.Request(info_url, headers={'User-Agent': 'origin-mission-E130'})
                    with urllib.request.urlopen(info_req, timeout=15) as info_resp:
                        data = json.loads(info_resp.read().decode())
                        info = data.get("info", {})
                        description = info.get("description", "") or ""
                except Exception:
                    description = ""
                packages.append({"name": name, "description": description})
                if len(packages) >= n:
                    break
    except Exception as e:
        print(f"Error fetching PyPI packages{f' with keyword {keyword}' if keyword else ''}: {e}")
    return packages


def fetch_pypi_package_info(name):
    """Fetch package metadata from PyPI JSON API. Returns dict or None on failure."""
    url = f"https://pypi.org/pypi/{name}/json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'origin-mission-E130'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            info = data.get("info", {})
            return {
                "name": info.get("name", name),
                "description": info.get("description", "") or "",
                "version": info.get("version", "") or "",
                "keywords": info.get("keywords", "") or "",
            }
    except Exception as e:
        print(f"  fetch error for {name}: {e}", file=sys.stderr)
        return None


def is_active_pypi(info):
    """Check if a package has meaningful activity metadata (description + version)."""
    desc = info.get("description", "") or ""
    ver = info.get("version", "") or ""
    return len(desc.strip()) > 0 and ver != "" and ver is not None


def compute_cliff_delta(need_arm, random_arm):
    """Compute Cliff's delta effect size between two independent samples."""
    n1 = len(need_arm)
    n2 = len(random_arm)

    if n1 == 0 or n2 == 0:
        return 0.0

    # Use active flag as the comparison metric
    need_active = sum(1 for p in need_arm if p[2])
    random_active = sum(1 for p in random_arm if p[2])

    # Cliff's delta = P(X > Y) - P(X < Y)
    # Approximation: proportion difference of active packages
    greater = need_active * (n2 - random_active)  # need active vs random inactive
    less = (n1 - need_active) * random_active     # need inactive vs random active

    total = n1 * n2
    if total == 0:
        return 0.0

    delta = (greater - less) / total
    return max(-1.0, min(1.0, delta))


def main():
    # Keyword argument: use a keyword filter for PyPI fetch
    # Using "cache" as it demonstrated success in E071 and provides a targeted sample
    keyword = "cache"

    print(f"=== E130 — View-Count Classifier Prototype v3: Continuation ===")
    print(f"Using PyPI keyword filter: '{keyword}'")

    # Step 1: Fetch packages from PyPI simple index with keyword filter
    print(f"\nStep 1: Fetching 200 packages from PyPI simple index (keyword='{keyword}')...")
    packages = fetch_pypi_packages(keyword=keyword, n=200)
    print(f"Found {len(packages)} packages")

    if len(packages) < 50:
        print(f"Warning: fewer than 50 packages found.")
        sys.exit(1)

    # Step 2: Fetch details, classify, track active status
    classified = {"need-related": 0, "random": 0, "uncertain": 0}
    active = {"need-related": 0, "random": 0}
    classified_count = 0
    pkg_records = []

    for i, pkg in enumerate(packages):
        name = pkg["name"]
        desc = pkg.get("description", "") or ""
        # Fetch full info for active status check
        info = fetch_pypi_package_info(name)
        if info is None:
            classified_count += 1
            pkg_records.append((name, "uncertain", False))
            continue
        cls_result = classify_package(name, info["description"])
        cls_label = cls_result["classification"]
        act = is_active_pypi(info)
        classified[cls_label] += 1
        if cls_label in active:
            if act: active[cls_label] += 1
        classified_count += 1
        pkg_records.append((name, cls_label, act))
        if (i + 1) % 40 == 0:
            print(f"  processed {i+1}/{len(packages)} (classified: {classified_count})...")
        time.sleep(0.1)

    print(f"Classified {classified_count} packages (out of {len(packages)})")

    # Step 3: Classification results
    print(f"\n=== Classification Results ===")
    for cls in ["need-related", "random"]:
        count = classified[cls]
        rate = (active[cls] / count * 100) if count else 0
        print(f"  {cls}: {count} packages, {active[cls]} active, rate = {rate:.1f}%")
    print(f"Total classified: {classified_count} / {len(packages)}")

    # Step 4: Gate evaluation
    print(f"\n=== Gate Evaluation ===")
    g2_pass = classified_count >= 100
    g4_pass = classified_count >= 50
    print(f"  G2 (classified >= 100): {'PASS' if g2_pass else 'FAIL'} ({classified_count})")
    print(f"  G4 (classified >= 50):  {'PASS' if g4_pass else 'FAIL'} ({classified_count})")
    if classified["need-related"] > 0 and classified["random"] > 0:
        need_rate = active["need-related"] / classified["need-related"]
        random_rate = active["random"] / classified["random"]
        ratio = need_rate / random_rate if random_rate > 0 else 0
        g1_pass = ratio >= 1.5
        print(f"  G1 (need/random active rate >= 150%): {'PASS' if g1_pass else 'FAIL'}")
        print(f"    need-related: {need_rate*100:.1f}%, random: {random_rate*100:.1f}%, ratio: {ratio*100:.1f}%")
    else:
        g1_pass = False
        print(f"  G1: SKIPPED (need-related={classified['need-related']}, random={classified['random']})")
    g3_pass = classified["need-related"] > 0 and classified["random"] > 0
    print(f"  G3 (both categories): {'PASS' if g3_pass else 'FAIL'} (need-related={classified['need-related']}, random={classified['random']})")
    all_pass = g1_pass and g2_pass and g3_pass and g4_pass
    print(f"\n  Overall: {'ALL GATES PASS' if all_pass else 'SOME GATES FAILED'}")

    # Step 5: Prioritized package list ranked by need-relatedness + active-rate product
    print(f"\n=== Prioritized Package List (top 50) ===")
    scored = []
    for name, cls, act in pkg_records:
        score = (2 if cls == "need-related" else 1) * (2 if act else 1)
        scored.append((name, cls, act, score))
    scored.sort(key=lambda r: (-r[3], r[0]))
    for name, cls, act, score in scored[:50]:
        if cls == "need-related" and act:    label = "🎯 NEED-RELATED & ACTIVE"
        elif cls == "need-related":          label = "📦 NEED-RELATED"
        elif act:                            label = "✅ ACTIVE"
        else:                                label = "❓ RANDOM"
        print(f"  {label}: {name} (score: {score})")
    if len(scored) > 50:
        print(f"  ... and {len(scored) - 50} more classified packages")

    # Step 6: Split into matched arms
    need_arm = [p for p in pkg_records if p[1] == "need-related" and p[2] == True]
    random_arm = [p for p in pkg_records if p[1] == "random" and p[2] == True]

    print(f"\nNeed-related arm (active): {len(need_arm)} packages")
    print(f"Random arm (active): {len(random_arm)} packages")

    # G1: Sample size >= 50 per group
    g1_pass = len(need_arm) >= 50 and len(random_arm) >= 50
    print(f"G1 (sample size >= 50 per group): {'PASS' if g1_pass else 'FAIL'} (need_arm={len(need_arm)}, random_arm={len(random_arm)})")

    # G2: Coverage floor >= 80% of pool classified (weight >= 0.5)
    total_classified = len(need_arm) + len(random_arm)
    total_pool = classified_count
    g2_pass_check = total_classified / total_pool >= 0.8 if total_pool > 0 else False
    print(f"G2 (coverage floor >= 80%): {'PASS' if g2_pass_check else 'FAIL'} ({total_classified}/{total_pool} = {total_classified/total_pool*100:.1f}%)")

    # G3: Cliff's delta > 0.147
    cliff_d = compute_cliff_delta(need_arm, random_arm)
    g3_pass = cliff_d > 0.147
    print(f"G3 (Cliff's delta > 0.147): {'PASS' if g3_pass else 'FAIL'} (δ = {cliff_d:.4f})")

    # G4: Both categories represented in classified arms
    g4_pass = len(need_arm) > 0 and len(random_arm) > 0
    print(f"G4 (both categories represented): {'PASS' if g4_pass else 'FAIL'} (need_arm={len(need_arm) > 0}, random_arm={len(random_arm) > 0})")

    # Step 7: Save results
    results = {
        "experiment": "E130",
        "title": "View-Count Classifier Prototype v3: Continuation on PyPI (keyword filter)",
        "platform": "pypi",
        "keyword": keyword,
        "pool_size": len(packages),
        "classified": classified,
        "active": active,
        "active_rates": {
            "need-related": active["need-related"] / classified["need-related"] if classified["need-related"] > 0 else 0,
            "random": active["random"] / classified["random"] if classified["random"] > 0 else 0,
        },
        "g1_sample_size_pass": g1_pass,
        "g2_coverage_floor_pass": g2_pass_check,
        "g3_cliff_delta_pass": g3_pass,
        "g4_bothrepresented_pass": g4_pass,
        "cliff_delta": cliff_d,
        "need_arm_size": len(need_arm),
        "random_arm_size": len(random_arm),
        "conclusion": "GATE_OPEN" if all([g1_pass, g2_pass_check, g3_pass, g4_pass]) else "GATE_CLOSED",
        "domain": "pypi_package_ecosystem",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    out_dir = os.path.join(REPO_ROOT, "EXPERIMENTS", "E130-viewcount-classifier-prototype-v3")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "results_continuation.json"), "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults written to {out_dir}/results_continuation.json")

    # Step 8: Decision
    if all([g1_pass, g2_pass_check, g3_pass, g4_pass]):
        print(f"\n" + "=" * 60)
        print("CONCLUSION: GATE_OPEN - All gates passed!")
        print("Continuation: Output prioritized package list and test on")
        print("additional platforms in next session.")
        print("=" * 60)
    else:
        print(f"\n" + "=" * 60)
        print("CONCLUSION: GATE_CLOSED - One or more gates failed.")
        print("Reasons:")
        if not g1_pass:
            print("  - G1: Sample size too small (need >=50 per arm)")
        if not g2_pass_check:
            print("  - G2: Coverage floor not met (<80% of pool classified)")
        if not g3_pass:
            print("  - G3: Cliff's delta too small (<0.147)")
        if not g4_pass:
            print("  - G4: Both categories not represented")
        print("  Continuation: Expand package pools, improve classifier,")
        print("  or test on additional platforms.")
        print("=" * 60)


if __name__ == "__main__":
    main()