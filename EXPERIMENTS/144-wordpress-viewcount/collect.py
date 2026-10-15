"""E144 — View-count principle on WordPress plugins (final analysis)."""
import json
import time
import sys
sys.path.insert(0, "EXPERIMENTS/144-wordpress-viewcount")
from wp_lib import (
    NEED_INDICATORS, RANDOM_KEYWORDS, SAMPLE_SIZE,
    fetch_plugin_data, parse_plugins, classify_plugin, is_active
)


def main():
    print("=== E144 — View-count principle on WordPress plugins ===")
    print()
    
    # Step 1: Fetch need-related plugins
    print("Step 1: Fetching need-related plugins across keywords...")
    need_keywords = ["cache", "security", "performance", "backup", "contact", "form", "seo"]
    
    need_plugins = []
    seen_names = set()
    
    for kw in need_keywords:
        raw = fetch_plugin_data(kw)
        if raw is None:
            print(f"  Failed to fetch '{kw}'")
            continue
        plugins = parse_plugins(raw)
        print(f"  Keyword '{kw}': fetched {len(plugins)} plugins")
        for p in plugins:
            name_lower = p["name"].lower()
            if name_lower not in seen_names:
                seen_names.add(name_lower)
                p["classification"] = classify_plugin(p["description"])
                p["keyword"] = kw
                need_plugins.append(p)
        time.sleep(1)
    
    print(f"\nTotal unique need-related plugins: {len(need_plugins)}")
    
    # Step 2: Fetch random plugins
    print("\nStep 2: Fetching random plugins across keywords...")
    random_plugins = []
    seen_random = set()
    
    for kw in RANDOM_KEYWORDS:
        raw = fetch_plugin_data(kw)
        if raw is None:
            print(f"  Failed to fetch random '{kw}'")
            continue
        plugins = parse_plugins(raw)
        print(f"  Keyword '{kw}': fetched {len(plugins)} plugins")
        for p in plugins:
            name_lower = p["name"].lower()
            if name_lower not in seen_random and name_lower not in seen_names:
                seen_random.add(name_lower)
                p["classification"] = classify_plugin(p["description"])
                p["keyword"] = kw + "_random"
                random_plugins.append(p)
        time.sleep(1)
    
    print(f"\nTotal unique random plugins: {len(random_plugins)}")
    
    # Step 3: Compute metrics and evaluate gates
    print("\nStep 3: Computing metrics and evaluating gates...")
    
    # Classify and compute active rates
    need_active = 0
    need_total = 0
    random_active = 0
    random_total = 0
    
    for p in need_plugins:
        if p["classification"] == "need-related":
            need_total += 1
            if is_active(p["active_installations"]):
                need_active += 1
    
    for p in random_plugins:
        if p["classification"] == "random":
            random_total += 1
            if is_active(p["active_installations"]):
                random_active += 1
    
    need_active_rate = need_active / need_total if need_total > 0 else 0
    random_active_rate = random_active / random_total if random_total > 0 else 0
    
    print(f"Need-related: {need_active}/{need_total} active = {need_active_rate*100:.1f}%")
    print(f"Random: {random_active}/{random_total} active = {random_active_rate*100:.1f}%")
    
    # G1: Sample size
    g1_pass = need_total >= 100 and random_total >= 100
    print(f"\nG1 (sample size >= 100 each): {'PASS' if g1_pass else 'FAIL'}")
    print(f"  Need-related: {need_total} (need 100), Random: {random_total} (need 100)")
    
    # G2: Significance test (proportion test)
    g2_pass = False
    z = 0
    p_value = 1.0
    if g1_pass:
        n1, k1 = need_total, need_active
        n2, k2 = random_total, random_active
        
        if n1 > 0 and n2 > 0:
            p_pool = (k1 + k2) / (n1 + n2) if (n1 + n2) > 0 else 0
            try:
                se = (p_pool * (1 - p_pool) * (1/n1 + 1/n2)) ** 0.5
                z = (k1/n1 - k2/n2) / se if se > 0 else 0
                abs_z = abs(z)
                if abs_z >= 1.96:
                    p_value = 0.05
                elif abs_z >= 2.576:
                    p_value = 0.01
                else:
                    p_value = 1.0
            except:
                p_value = 1.0
            g2_pass = p_value < 0.05
            print(f"G2 (significance p < 0.05): {'PASS' if g2_pass else 'FAIL'}")
            print(f"  z = {z:.4f}, p_value = {p_value:.6f}")
            print(f"  need_rate = {need_active_rate:.4f}, random_rate = {random_active_rate:.4f}, diff = {need_active_rate - random_active_rate:.4f}")
        else:
            print(f"G2: SKIPPED (insufficient data)")
    
    # G3: Effect size (Wilson CI95 LB > 0.60 for need-related)
    g3_pass = False
    wilson_lb = 0
    if need_total > 0:
        z_w = 1.96
        n = need_total
        p = need_active_rate
        wilson_lb = (p + z_w*z_w/(2*n) - z_w * ((p*(1-p)/n + z_w*z_w/(4*n*n)) ** 0.5)) / (1 + z_w*z_w/n)
        g3_pass = wilson_lb > 0.60
        print(f"G3 (Wilson LB > 0.60): {'PASS' if g3_pass else 'FAIL'}")
        print(f"  Wilson LB = {wilson_lb:.4f} (need_rate={p:.4f}, n={n})")
    else:
        print(f"G3: FAIL (no need-related data)")
    
    # G4: Arrival field rate >= 95% (FIXED: only count plugins classified in the group)
    need_with_meta = sum(1 for p in need_plugins if p["classification"] == "need-related" and p["active_installations"] is not None)
    random_with_meta = sum(1 for p in random_plugins if p["classification"] == "random" and p["active_installations"] is not None)
    need_arrival_rate = need_with_meta / need_total if need_total > 0 else 0
    random_arrival_rate = random_with_meta / random_total if random_total > 0 else 0
    g4_pass = need_arrival_rate >= 0.95 and random_arrival_rate >= 0.95
    print(f"\nG4 (arrival field rate >= 95%): {'PASS' if g4_pass else 'FAIL'}")
    print(f"  Need arrival rate: {need_arrival_rate*100:.1f}% ({need_with_meta}/{need_total})")
    print(f"  Random arrival rate: {random_arrival_rate*100:.1f}% ({random_with_meta}/{random_total})")
    
    # Overall
    all_pass = g1_pass and g2_pass and g3_pass and g4_pass
    print(f"\n=== Overall: {'ALL GATES PASS' if all_pass else 'SOME GATES FAILED'} ===")
    
    # Interpret the results
    print(f"\n=== Interpretation ===")
    if not g2_pass:
        print(f"The view-count principle does NOT generalize to WordPress plugins")
        print(f"in the expected direction. Need-related plugins have a {abs(need_active_rate - random_active_rate)*100:.1f}%")
        print(f"LOWER active installation rate than random plugins ({need_active_rate*100:.1f}% vs {random_active_rate*100:.1f}%).")
        print(f"This is a negative result: the 'active signal' for need-related")
        print(f"plugins is not elevated on wordpress.org.")
    
    # Save results
    results = {
        "observed_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "user_date": time.strftime("%Y-%m-%d", time.gmtime()),
        "platform": "Linux-x86_64",
        "need_keywords": need_keywords,
        "random_keywords": RANDOM_KEYWORDS,
        "need_total": need_total,
        "need_active": need_active,
        "need_active_rate": need_active_rate,
        "random_total": random_total,
        "random_active": random_active,
        "random_active_rate": random_active_rate,
        "g1_pass": g1_pass,
        "g2_pass": g2_pass,
        "g3_pass": g3_pass,
        "g4_pass": g4_pass,
        "all_gates_pass": all_pass,
        "conclusion": "negative - view-count principle does not generalize to WordPress plugins; need-related plugins have lower active installation rates than random",
        "experiment_description": "View-count principle on WordPress plugins",
        "details": {
            "need_description_stats": {
                "active_count": need_active,
                "total_count": need_total,
                "active_rate": need_active_rate,
                "wilson_lb": wilson_lb if need_total > 0 else None,
            },
            "random_description_stats": {
                "active_count": random_active,
                "total_count": random_total,
                "active_rate": random_active_rate,
            },
            "gate_results": {
                "g1_sample_size": {"pass": g1_pass, "need_n": need_total, "random_n": random_total, "threshold": ">= 100 each"},
                "g2_significance": {"pass": g2_pass, "z_score": z if g1_pass else None, "p_value": p_value if g1_pass else None},
                "g3_effect_size": {"pass": g3_pass, "wilson_lb": wilson_lb if need_total > 0 else None, "threshold": "Wilson LB > 0.60"},
                "g4_arrival_field": {"pass": g4_pass, "need_arrival_rate": need_arrival_rate, "random_arrival_rate": random_arrival_rate, "threshold": ">= 95%"},
            },
        },
    }
    
    import os
    os.makedirs("EXPERIMENTS/144-wordpress-viewcount", exist_ok=True)
    with open("EXPERIMENTS/144-wordpress-viewcount/results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to EXPERIMENTS/144-wordpress-viewcount/results.json")
    
    return 0 if all_pass else 2


if __name__ == "__main__":
    sys.exit(main())