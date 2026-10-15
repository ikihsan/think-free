#!/usr/bin/env python3
"""E139 — View-Count Fresh Observation on CPAN/Perl Packages

Tests the view-count principle on a new package ecosystem (CPAN/Perl)
using the Metacpan fast API. Fulfills D083 requirement for fresh
observation in a new domain not yet covered by the mission's 15+ experiments.
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
    'perl', 'py3', '3', '2',
}


def classify_package(name, description):
    """Classify a CPAN package using the v3 classifier: whole-word matching, combined name+description, uncertainty weighting."""
    name_tokens = set(name.lower().split()) if name else set()
    desc = description or ''
    desc_tokens = set(desc.lower().split()) if desc else set()
    all_tokens = name_tokens | desc_tokens

    need_tokens = all_tokens & NEED_INDICATORS
    generic_tokens = all_tokens & GENERIC_TERMS

    has_need_token = len(need_tokens) > 0
    has_only_generic = len(need_tokens) == 0 and len(generic_tokens) > 0
    has_both = len(need_tokens) > 0 and len(generic_tokens) > 0

    if has_need_token and not has_only_generic:
        if has_both:
            total_meaningful = len(need_tokens) + len(generic_tokens)
            weight = len(need_tokens) / total_meaningful if total_meaningful > 0 else 0.0
            classification = "need-related"
        else:
            weight = 1.0
            classification = "need-related"
    elif len(generic_tokens) > 0 and len(need_tokens) == 0:
        weight = 0.0
        classification = "uncertain"
    else:
        weight = 0.0
        classification = "uncertain"

    return {
        "classification": classification,
        "weight": weight,
        "need_tokens": list(need_tokens) if need_tokens else [],
        "generic_tokens": list(generic_tokens) if generic_tokens else [],
        "reason": _get_classification_reason(need_tokens, generic_tokens, has_both),
    }


def _get_classification_reason(need_tokens, generic_tokens, has_both):
    if len(need_tokens) > 0 and len(generic_tokens) == 0:
        return f"{len(need_tokens)} need-specific token(s) found (name and description)"
    elif len(need_tokens) > 0 and len(generic_tokens) > 0 and has_both:
        return f"{len(need_tokens)} need-specific token(s) outweigh {len(generic_tokens)} generic token(s) (with context)"
    elif len(need_tokens) > 0 and len(generic_tokens) > 0:
        return f"{len(need_tokens)} need-specific token(s) outweigh {len(generic_tokens)} generic token(s) (with context)"
    elif len(generic_tokens) > 0:
        return f"{len(generic_tokens)} generic token(s) in name/description, no need-specific signals"
    else:
        return "no recognized need or generic tokens in name or description"


def fetch_cpan_releases(keyword, n=200):
    """Fetch up to n Perl releases from Metacpan matching a keyword query."""
    releases = []
    seen = set()
    url = f"https://fastapi.metacpan.org/v1/release/_search?q={keyword}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'origin-mission-E139'})
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read().decode()
            j = json.loads(data)
            hits = j.get('hits', {}).get('hits', [])
            for hit in hits:
                if len(releases) >= n:
                    break
                _source = hit.get('_source', {})
                name = _source.get('name', '')
                abstract = _source.get('abstract', '') or ''
                # Skip if already seen
                if name in seen:
                    continue
                seen.add(name)
                # Skip very short names or names that are just version numbers
                if not name or len(name) < 2:
                    continue
                if re.match(r'^[\d._-]+$', name):
                    continue
                releases.append({"name": name, "description": abstract})
    except Exception as e:
        print(f"Error fetching CPAN releases for keyword '{keyword}': {e}")
    return releases


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 experiment.py <need_keyword>"); sys.exit(2)
    keyword = sys.argv[1]
    print(f"=== E139 — View-Count Fresh Observation on CPAN/Perl Packages ===")
    print(f"Need keyword: {keyword}")

    # Step 1: Fetch packages from Metacpan
    print(f"\nStep 1: Fetching 200 Perl releases from Metacpan via keyword search...")
    releases = fetch_cpan_releases(keyword, n=200)
    print(f"Found {len(releases)} releases")

    if len(releases) < 50:
        print(f"Warning: fewer than 50 releases found with keyword '{keyword}'.")
        print("This may indicate the keyword doesn't match enough CPAN releases.")
        sys.exit(1)

    # Step 2: Classify each release
    classified = {"need-related": 0, "random": 0, "uncertain": 0}
    active = {"need-related": 0, "random": 0}
    classified_count = 0
    pkg_records = []

    for i, rel in enumerate(releases):
        name = rel["name"]
        desc = rel.get("description", "") or ""
        # A package is "active" if it has both a non-empty name and abstract
        act = len(desc.strip()) > 0 and len(name.strip()) > 0
        
        cls_result = classify_package(name, desc)
        cls_label = cls_result["classification"]
        act_flag = act and cls_label in active
        classified[cls_label] += 1
        if cls_label in active and act_flag: active[cls_label] += 1
        classified_count += 1
        pkg_records.append((name, cls_label, act_flag))
        if (i + 1) % 40 == 0:
            print(f"  processed {i+1}/{len(releases)} (classified: {classified_count})...")
        time.sleep(0.1)

    print(f"Classified {classified_count} releases (out of {len(releases)})")

    # Step 3: Classification results
    print(f"\n=== Classification Results ===")
    for cls in ["need-related", "random"]:
        count = classified[cls]
        rate = (active[cls] / count * 100) if count else 0
        print(f"  {cls}: {count} packages, {active[cls]} active, rate = {rate:.1f}%")
    print(f"Total classified: {classified_count} / {len(releases)}")

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
    # Simple proportion-based effect size
    need_with_feature = sum(1 for name, cls, act in need_arm if cls == "need-related" and act)
    random_with_feature = sum(1 for name, cls, act in random_arm if cls == "random" and act)
    n1, n2 = len(need_arm), len(random_arm)

    if need_with_feature > 0 and random_with_feature > 0 and n1 > 0 and n2 > 0:
        prop_diff = abs(need_with_feature/n1 - random_with_feature/n2)
        cliff_d = prop_diff
        g3_pass = cliff_d > 0.147
        print(f"G3 (Cliff's delta > 0.147): {'PASS' if g3_pass else 'FAIL'} (δ = {cliff_d:.4f})")
    else:
        g3_pass = False
        print(f"G3 (Cliff's delta > 0.147): FAIL (insufficient data for effect size)")

    # G4: Both categories represented in classified arms
    g4_pass = len(need_arm) > 0 and len(random_arm) > 0
    print(f"G4 (both categories represented): {'PASS' if g4_pass else 'FAIL'} (need_arm={len(need_arm) > 0}, random_arm={len(random_arm) > 0})")

    # Step 7: Save results
    results = {
        "experiment": "E139",
        "title": "View-Count Fresh Observation on CPAN/Perl Packages",
        "platform": "cpan",
        "keyword": keyword,
        "pool_size": len(releases),
        "classified": classified,
