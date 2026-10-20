        "g2_pass": g2_pass,
        "g3_pass": g3_pass,
        "g4_pass": g4_pass,
        "g1_ratio": ratio,
        "g1_need_rate": need_rate,
        "g1_random_rate": random_rate,
        "classified_total": total_classified,
        "need_related_count": classified["need-related"],
        "random_count": classified["random"],
        "need_related_active": active["need-related"],
        "random_active": active["random"],
    }


# ---------------------------------------------------------------------------
# Main prototype entry point
# ---------------------------------------------------------------------------


def run_vscode_prototype(keyword, max_results=200, min_classified=50):
    """Run the view-count prototype on VS Code Extension Marketplace.

    Adapted from tools/viewcount_prototype.py run_prototype().

    Returns a results dict with classification, gate results, and prioritized
    need-related extension listing.

    Primary challenge: VS Code Marketplace API access barrier (documented in
    fetch_vscode_marketplace()). The experiment either fetches real data or
    falls back to the embedded corpus while documenting the barrier.
    """
    # Fetch extensions from the Marketplace (or fallback)
    extensions = fetch_vscode_marketplace(keyword, max_results=max_results)

    if not extensions:
        return {
            "observed_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "user_date": time.strftime("%Y-%m-%d", time.gmtime()),
            "platform": "vscode-marketplace",
            "sample_size": 0,
            "classified": {"need-related": 0, "random": 0},
            "active": {"need-related": 0, "random": 0},
            "active_rates": {"need-related": 0, "random": 0},
            "g1_pass": False,
            "g2_pass": False,
            "g3_pass": False,
            "g4_pass": False,
            "conclusion": "no_extensions_found",
            "experiment_description": f"View-count prototype on VS Code Marketplace for keyword: {keyword}",
            "note": "No extensions found; API access barrier prevents data collection.",
        }

    # Classify and evaluate
    classified = {"need-related": 0, "random": 0}
    active = {"need-related": 0, "random": 0}
    need_related_exts = []

    for ext in extensions:
        cls = classify_extension_description(ext.get("description", ""))
        active_flag = is_active(ext)

        classified[cls] += 1
        if active_flag:
            active[cls] += 1
        if cls == "need-related":
            need_related_exts.append(ext)

    # Compute gates
    gates = compute_gates(classified, active, sum(classified.values()), min_classified=min_classified)

    # Print classification summary (for human readability)
    print("=== Classification ===")
    for cls in ["need-related", "random"]:
        count = classified[cls]
        act = active[cls]
        rate = (act / count * 100) if count > 0 else 0
        print(f"  {cls}: {count} extensions, {act} active, active rate = {rate:.1f}%")

    print(f"\n=== Gate G1 ===")
    print(f"  need-related active rate: {gates['g1_need_rate']*100:.1f}%")
    print(f"  random active rate: {gates['g1_random_rate']*100:.1f}%")
    print(f"  ratio (need/random): {gates['g1_ratio']*100:.1f}%")
    print(f"  G1 pass (>= 55%): {'PASS' if gates['g1_pass'] else 'FAIL'}")

    print(f"\n=== Gate G2 ===")
    print(f"  classified total: {gates['classified_total']}")
    print(f"  G2 pass (>= 100): {'PASS' if gates['g2_pass'] else 'FAIL'}")

    print(f"\n=== Gate G3 ===")
    print(f"  G3 pass (both categories): {'PASS' if gates['g3_pass'] else 'FAIL'}")

    print(f"\n=== Gate G4 ===")
    print(f"  classified total: {gates['classified_total']}")
    print(f"  G4 pass (>= 50): {'PASS' if gates['g4_pass'] else 'FAIL'}")

    all_pass = gates["g1_pass"] and gates["g2_pass"] and gates["g3_pass"] and gates["g4_pass"]
    print(f"\n=== Overall ===")
    print(f"  All gates pass: {'YES' if all_pass else 'NO'}")

    # Sort need-related extensions: active first, then by number of strong keywords
    def need_indicator_count(ext):
        desc = (ext.get("description", "") or "").lower()
        return sum(1 for term in STRONG_KEYWORDS if _matches_word_boundary(desc, term))

    need_related_exts.sort(
        key=lambda e: (
            0 if is_active(e) else 1,
            -need_indicator_count(e),
            e.get("name", "").lower(),
        )
    )

    # Display need-related extensions ranked by priority
    print(f"\n=== Need-related extensions (top {min(10, len(need_related_exts))}) ===")
    for i, ext in enumerate(need_related_exts[:10]):
        name = ext.get("name", "N/A")
        version = ext.get("version", "N/A")
        desc = ext.get("description", "")[:80] if ext.get("description") else ""
        active_str = "ACTIVE" if is_active(ext) else "inactive"
        print(
            f"  {i+1}. {name} {version}"
            f" -- {desc}..."
            f" [{active_str}]"
        )

    # Build results dict
    results = {
        "observed_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "user_date": time.strftime("%Y-%m-%d", time.gmtime()),
        "platform": "vscode-marketplace",
        "sample_size": len(extensions),
        "classified": classified,
        "active": active,
        "active_rates": {
            "need-related": active["need-related"] / classified["need-related"]
            if classified["need-related"] > 0
            else 0,
            "random": active["random"] / classified["random"] if classified["random"] > 0 else 0,
        },
        "g1_pass": gates["g1_pass"],
        "g2_pass": gates["g2_pass"],
        "g3_pass": gates["g3_pass"],
        "g4_pass": gates["g4_pass"],
        "g1_ratio": gates["g1_ratio"],
        "g1_need_rate": gates["g1_need_rate"],
        "g1_random_rate": gates["g1_random_rate"],
        "conclusion": "pending",
        "experiment_description": f"View-count prototype on VS Code Marketplace for keyword: {keyword}",
        "note": (
            "API access barrier: VS Code Extension Marketplace uses "
            "client-side rendering with no accessible public JSON API. "
            "Fallback corpus used; barrier documented in results."
        ),
    }

    # Save results JSON for the session record
    out_dir = "EXPERIMENTS/E161-vscode-viewcount"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n=== Results saved to {out_path} ===")

    return results


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 tools/vscode_adapter.py <keyword> [--top N]")
        print("  Example: python3 tools/vscode_adapter.py python")
        sys.exit(1)

    keyword = sys.argv[1]
    top_n = 10
    if len(sys.argv) > 3 and sys.argv[3] == "--top":
        top_n = int(sys.argv[4])

    print(f"=== View-count prototype on VS Code Marketplace: searching '{keyword}' ===\n")
    results = run_vscode_prototype(keyword, max_results=200, min_classified=50)