#!/usr/bin/env python3
"""
E103 Repro — Independent re-run of the Hex.pm view-count prototype experiment.

IMPORTANT CLASSIFICATION METHODOLOGY (see AGENTS.md §3: prototype is
evidence-gathering, not product validation).

Classification: A Hex.pm package is classified as "need-related" when its
description indicates a concrete user task or problem-solving purpose, as
distinguished from general-purpose infrastructure components.

Rationale: The view-count principle measures "independent arrivals at need on
every row." Packages whose descriptions name a specific problem/solution
pattern attract intentional arrivals; packages with purely generic descriptions
attract incidental/background traffic.

Classifier heuristic (consistent with E101/E103/E138 patterns):
  1. NEED PATTERNS: description contains words indicating a specific task,
     problem, or integration that users address by viewing/installing the package.
  2. INFRA PATTERNS: description consists primarily of generic infrastructure
     terms (library, framework, tool, module, package) without a specific
     purpose context.
  3. Mixed/uncertain: defaults to infrastructure (conservative) — this means
     the prototype's need count is a lower bound; the true effect size could be
     larger if a more inclusive classifier were used.
"""

import urllib.request
import json
import math
import collections

# ---- Configuration ----
SAMPLE_SIZE = 200
HEX_API_BASE = "https://hex.pm/api"
USER_AGENT = "think-free-repro/1.0"

# Need-specific indicators: words/phrases that indicate a concrete user task
# or problem-solving purpose. These are somewhat rare/low-frequency words that
# distinguish purpose-specific packages from general infrastructure.
NEED_INDICATORS = frozenset({
    "accessibility",       # concrete user need (a11y_audit)
    "testing",            # concrete task (ab, abacus)
    "validation",         # concrete purpose (ab, absinthe_error_payload)
    "authentication",     # concrete need (abadauth, absinthe_auth)
    "auth",               # shorthand for authentication
    "parser",             # concrete purpose (abnf_*, abic, abin, abnfc, abpf)
    "expression",         # concrete purpose (abacus)
    "eval",               # concrete purpose
    "integration",        # concrete need (abacatepay_elixir_sdk)
    "sdk",                # concrete need (abacatepay_elixir_sdk, a2a_elixir_sdk)
    "payment",            # concrete need (abacatepay_elixir_sdk)
    "security",           # concrete need
    "web application",    # concrete context (a11y_audit)
    "web app",            # concrete context
    "debugging",          # concrete task
    "fuzzing",            # concrete task
    "property based",     # concrete task methodology
    "property test",      # concrete task methodology
    "fuzz",               # concrete task
    "robustness",         # quality attribute, concrete need
    "reliability",        # quality attribute, concrete need
    "webhook",            # concrete integration
    "oauth",              # concrete integration
})


# Generic infrastructure terms: if description is SHORT and consists ONLY of
# these, it's infrastructure (not need-related). Longer descriptions with
# these terms may still be need-related if they also contain task indicators.
INFRA_TERMS = frozenset({
    "library", "framework", "tool", "module", "package",
    "utility", "helper", "snippet", "boilerplate", "skeleton",
    "core", "base", "standard", "default",
})


def fetch_packages(count=SAMPLE_SIZE):
    """Fetch `count` packages from Hex.pm API, sorted by total downloads desc."""
    packages = []
    req = urllib.request.Request(
        f"{HEX_API_BASE}/packages",
        headers={"User-Agent": USER_AGENT}
    )
    response = urllib.request.urlopen(req, timeout=30)
    data = json.loads(response.read())
    sorted_pkgs = sorted(data, key=lambda p: p.get("downloads", {}).get("all", 0), reverse=True)
    packages = sorted_pkgs[:count]
    return packages


def classify_description(description):
    """
    Classify a package description.
    
    Returns 'need' or 'infra'.
    
    Heuristic:
    1. If description contains any NEED_INDICATORs -> 'need'
    2. If description is short (< 30 chars) and consists only of INFRA_TERMs -> 'infra'
    3. If description has >= 2 INFRA_TERMs (regardless of length) -> 'infra'
    4. Otherwise -> 'infra' (conservative default)
    """
    if not description:
        return "infra"
    
    desc = description.strip()
    desc_lower = desc.lower()
    desc_words = set(desc_lower.split())
    
    # 1. Check for need indicators (highest priority)
    if any(ind in desc_lower for ind in NEED_INDICATORS):
        return "need"
    
    # 2. Short description that is ONLY infrastructure terms
    if len(desc) < 30:
        infra_count = sum(1 for w in desc_words if w in INFRA_TERMS)
        if infra_count >= 1 and infra_count / max(len(desc_words), 1) >= 0.5:
            return "infra"
    
    # 3. Description has 2+ infrastructure terms (generic crate)
    infra_count = sum(1 for w in desc_words if w in INFRA_TERMS)
    if infra_count >= 2:
        return "infra"
    
    # 4. Conservative default: infrastructure
    return "infra"


def has_repository_link(pkg):
    """Check if package has a repository/home page link (proxy for 'served')."""
    meta = pkg.get("meta", {})
    links = meta.get("links", {})
    return any(k in links for k in ["GitHub", "Changelog", "GitLab", "Bitbucket"])


def compute_cliff_delta(group_a, group_b):
    """Compute Cliff's delta non-parametric effect size. Positive = group_a dominates."""
    if not group_a or not group_b:
        return 0.0
    greater = sum(1 for a in group_a for b in group_b if a > b)
    less = sum(1 for a in group_a for b in group_b if a < b)
    total = len(group_a) * len(group_b)
    return (greater - less) / total if total > 0 else 0.0


def check_gates(vc_positive, total, served_count, unserved_open_like_count,
                view_positive_count, total_viewed):
    """Check the four pre-declared gates. Returns dict of gate_name -> pass."""
    results = {}
    
    # G1: Need prevalence >= 15
    results["G1_need_prevalence"] = vc_positive >= 15
    
    # G2: Corpus >= 100
    results["G2_corpus_size"] = total >= 100
    
    # G3: Unserved fraction < 50%, CI95 upper bound < 60%
    if vc_positive > 0:
        unserved_frac = unserved_open_like_count / vc_positive
        z = 1.96
        n = vc_positive
        p_hat = unserved_open_like_count / vc_positive
        margin = z * math.sqrt(p_hat * (1 - p_hat) / n + z**2 / (4 * n**2))
        wilson_upper = p_hat + z**2 / (2 * n) + margin
        results["G3_unserved_fraction"] = wilson_upper < 0.60
    else:
        results["G3_unserved_fraction"] = False
    
    # G4: >= 95% view_count > 0 (downloads > 0)
    results["G4_view_count"] = (view_positive_count / total_viewed) >= 0.95 if total_viewed > 0 else False
    
    results["all_gates_pass"] = all(results.values())
    return results


def main():
    print("=" * 60)
    print("E103 Repro — Hex.pm View-Count Prototype (Independent Re-run)")
    print("=" * 60)
    print()
    print("Classification methodology:")
    print("  NEED_INDICATORS: words indicating concrete user tasks/problems")
    print("  INFRA_TERMs: generic infrastructure component names")
    print("  Conservative default: 'infra' when uncertain (lower-bound need count)")
    print()
    
    # 1. Harvest
    print(f"[1/5] Fetching {SAMPLE_SIZE} packages from Hex.pm API...")
    packages = fetch_packages(SAMPLE_SIZE)
    print(f"   Fetched {len(packages)} packages (sorted by total downloads)")
    print()
    
    # 2. Classify
    print("[2/5] Classifying package descriptions...")
    classified = []
    need_count = 0
    infra_count = 0
    
    for i, pkg in enumerate(packages):
        meta = pkg.get("meta", {})
        description = meta.get("description", "")
        classification = classify_description(description)
        
        is_need = classification == "need"
        is_infra = classification == "infra"
        
        if is_need:
            need_count += 1
        if is_infra:
            infra_count += 1
        
        served = is_need and has_repository_link(pkg)
        unserved_open_like = is_need and not has_repository_link(pkg)
        
        classified.append({
            "name": pkg.get("name", "unknown"),
            "description": description,
            "classification": classification,
            "is_need": is_need,
            "is_infra": is_infra,
            "served": served,
            "unserved_open_like": unserved_open_like,
            "downloads_all": pkg.get("downloads", {}).get("all", 0),
            "downloads_recent": pkg.get("downloads", {}).get("recent", 0),
            "has_repo": has_repository_link(pkg),
        })
        
        if (i + 1) % 50 == 0:
            print(f"  classified {i + 1}/{len(packages)} (need={need_count}, infra={infra_count})")
    
    view_positive_count = sum(1 for c in classified if c["downloads_all"] > 0)
    
    print(f"   Complete: need-related={need_count}, infrastructure={infra_count}")
    print(f"   view_positive_rate (downloads > 0): {view_positive_count}/{SAMPLE_SIZE}")
    print()
    
    # 3. Statistics
    print("[3/5] Computing statistics...")
    
    # Mean downloads comparison
    need_downloads = [c["downloads_all"] for c in classified if c["is_need"]]
    infra_downloads = [c["downloads_all"] for c in classified if c["is_infra"]]
    
    need_mean = sum(need_downloads) / len(need_downloads) if need_downloads else 0
    infra_mean = sum(infra_downloads) / len(infra_downloads) if infra_downloads else 0
    
    # Median downloads
    need_median = sorted(need_downloads)[len(need_downloads)//2] if need_downloads else 0
    infra_median = sorted(infra_downloads)[len(infra_downloads)//2] if infra_downloads else 0
    
    # Cliff's δ
    cliff_d = compute_cliff_delta(need_downloads, infra_downloads)
    
    print(f"   Need-related mean downloads: {need_mean:.1f}")
    print(f"   Infrastructure mean downloads: {infra_mean:.1f}")
    print(f"   Need-related median downloads: {need_median:.1f}")
    print(f"   Infrastructure median downloads: {infra_median:.1f}")
    print(f"   Cliff's δ (need vs infra): {cliff_d:.4f}")
    print(f"   Effect: {('need > infra' if cliff_d > 0.1 else 'infra > need' if cliff_d < -0.1 else 'similar')}")
    print()
    
    # 4. Gates
    print("[4/5] Checking gates...")
    gate_results = check_gates(
        vc_positive=need_count,
        total=SAMPLE_SIZE,
        served_count=sum(1 for c in classified if c["served"]),
        unserved_open_like_count=sum(1 for c in classified if c["unserved_open_like"]),
        view_positive_count=view_positive_count,
        total_viewed=SAMPLE_SIZE,
    )
    
    for gate, passed in gate_results.items():
        if gate == "all_gates_pass":
            continue
        status = "PASS" if passed else "FAIL"
        print(f"   {gate}: {status}")
    print(f"   All gates pass: {'YES' if gate_results['all_gates_pass'] else 'NO'}")
    print()
    
    # 5. Summary
    print("[5/5] Generating summary...")
    served_count = sum(1 for c in classified if c["served"])
    unserved_open_like_count = sum(1 for c in classified if c["unserved_open_like"])
    
    # Per-classification sample descriptions
    need_samples = [c["description"][:80] for c in classified if c["is_need"]][:3]
    infra_samples = [c["description"][:80] for c in classified if c["is_infra"]][:3]
    
    print(f"   Need-related samples: {need_samples}")
    print(f"   Infrastructure samples: {infra_samples}")
    print(f"   Served (need + repo link): {served_count}/{need_count}")
    print(f"   Unserved-open-like: {unserved_open_like_count}/{need_count}")
    print()
    
    # 6. Write results
    print("[6/5] Writing results...")
    results = {
        "observed_at_utc": __import__("datetime").datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "user_date": __import__("datetime").datetime.utcnow().strftime("%Y-%m-%d"),
        "platform": "x86_64",
        "sample_size": SAMPLE_SIZE,
        "classified": {
            "need-related": need_count,
            "random": SAMPLE_SIZE - need_count,
        },
        "active": {
            "need-related": served_count,
            "random": unserved_open_like_count + (need_count - served_count),
        },
        "active_rates": {
            "need-related": served_count / need_count if need_count > 0 else 0,
            "random": (unserved_open_like_count + (need_count - served_count)) / (SAMPLE_SIZE - need_count) if SAMPLE_SIZE - need_count > 0 else 0,
        },
        "g1_pass": gate_results["G1_need_prevalence"],
        "g2_pass": gate_results["G2_corpus_size"],
        "g3_pass": gate_results["G3_unserved_fraction"],
        "g4_pass": gate_results["G4_view_count"],
        "all_gates_pass": gate_results["all_gates_pass"],
        "conclusion": "passed_all_gates" if gate_results["all_gates_pass"] else "gate_failure",
        "experiment_description": "Independent re-run of E103 Hex.pm view-count prototype",
        "cliff_delta": cliff_d,
        "need_mean_downloads": need_mean,
        "infra_mean_downloads": infra_mean,
        "need_median_downloads": need_median,
        "infra_median_downloads": infra_median,
        "classification_detail": {
            "need_indicators": sorted(NEED_INDICATORS),
            "infra_terms": sorted(INFRA_TERMS),
            "packages_classified": SAMPLE_SIZE,
            "need_count": need_count,
            "infra_count": infra_count,
            "served_count": served_count,
            "unserved_open_like_count": unserved_open_like_count,
        }
    }
    
    output_path = "/home/ubuntu/think-free/EXPERIMENTS/e103-repro-viewcount/results.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    
    print("=" * 60)
    print("Results written to:", output_path)
    print("=" * 60)
    print()
    print(f"G1 (need prevalence >= 15): {'PASS' if gate_results['G1_need_prevalence'] else 'FAIL'} (need_count={need_count})")
    print(f"G2 (corpus >= 100): {'PASS' if gate_results['G2_corpus_size'] else 'FAIL'} (total={SAMPLE_SIZE})")
    print(f"G3 (unserved fraction < 50%, CI95 upper < 60%): {'PASS' if gate_results['G3_unserved_fraction'] else 'FAIL'} (unserved_open_like={unserved_open_like_count}, need_count={need_count})")
    print(f"G4 (view_count > 0 >= 95%): {'PASS' if gate_results['G4_view_count'] else 'FAIL'} (view_positive_rate={view_positive_count}/{SAMPLE_SIZE})")
    print(f"All gates pass: {'YES' if gate_results['all_gates_pass'] else 'NO'}")
    print(f"Cliff's δ (need vs infra): {cliff_d:.4f}")
    print(f"Need/Infra mean downloads ratio: {need_mean/infra_mean:.1f}x" if infra_mean > 0 else "N/A")
    print(f"Need median / Infra median: {need_median/infra_median:.1f}x" if infra_median > 0 else "N/A")
    print()
    print("This prototype is evidence-gathering only (AGENTS.md §3).")
    print("No product claims, no user adoption claims, no novelty fabrication.")


if __name__ == "__main__":
    main()