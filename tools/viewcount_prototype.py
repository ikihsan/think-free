

def classify_package_with_keywords(package_info):
    """Classify a package using both description and keyword-level checks.

    Tries keyword-based classification first (on the project name), then falls
    back to description-based classification. Returns ('need-related'/'random',
    used_field) tuple.
    """
    # Try keyword-based classification on the project name
    kw_result = classify_by_keywords(package_info)
    if kw_result is not None:
        return kw_result

    # Fall back to description-based classification
    desc = package_info.get("description", "") or package_info.get("summary", "") or ""
    cls = classify_package(desc)
    return cls, "description"


def run_prototype(keyword, max_results=200, top_n=10):
    """Run the view-count prototype v3 for a given keyword.

    Returns a results dict with classification, gate results, and prioritized
    need-related package listing. Uses word-boundary matching and keyword-
    enhanced classification from this module's vocabulary.
    """
    # Search packages using the stdlib-only PyPI adapter
    packages = search_pypi(keyword, max_results=max_results)

    if not packages:
        return {
            "observed_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "user_date": time.strftime("%Y-%m-%d", time.gmtime()),
            "platform": "unknown",
            "sample_size": 0,
            "classified": {"need-related": 0, "random": 0},
            "active": {"need-related": 0, "random": 0},
            "active_rates": {"need-related": 0, "random": 0},
            "g1_pass": False,
            "g2_pass": False,
            "g3_pass": False,
            "g4_pass": False,
            "conclusion": "no_packages_found",
            "experiment_description": f"View-count prototype v3 search for keyword: {keyword}",
            "note": "No packages found for the given keyword on PyPI.",
        }

    # Classify and evaluate using word-boundary matching
    classified = {"need-related": 0, "random": 0}
    active = {"need-related": 0, "random": 0}
    need_related_pkgs = []

    for pkg in packages:
        # Use word-boundary classification from this module
        desc = pkg.get("description", "") or pkg.get("summary", "") or ""
        cls = classify_package(desc)

        active_flag = is_active(pkg)
        classified[cls] += 1
        if active_flag:
            active[cls] += 1
        if cls == "need-related":
            need_related_pkgs.append(pkg)

    # Print classification summary
    print("=== Classification ===")
    for cls in ["need-related", "random"]:
        count = classified[cls]
        act = active[cls]
        rate = (act / count * 100) if count > 0 else 0
        print(f"  {cls}: {count} packages, {act} active, active rate = {rate:.1f}%")

    # G1 gate: need-related active rate >= 55% of random active rate
    g1_pass = False
    if classified["need-related"] > 0 and classified["random"] > 0:
        need_rate = active["need-related"] / classified["need-related"]
        random_rate = active["random"] / classified["random"]
        ratio = need_rate / random_rate if random_rate > 0 else 0
        g1_pass = ratio >= 0.55
        print(f"\n=== Gate G1 ===")
        print(f"  need-related active rate: {need_rate*100:.1f}%")
        print(f"  random active rate: {random_rate*100:.1f}%")
        print(f"  ratio (need/random): {ratio*100:.1f}%")
        print(f"  G1 pass (>= 55%): {'PASS' if g1_pass else 'FAIL'}")
    else:
        print(f"\n=== Gate G1 ===")
        print(f"  SKIPPED: need at least one package in each category (need-related={classified['need-related']}, random={classified['random']})")

    # G2 gate: minimum classified sample size >= 100
    g2_pass = classified["need-related"] + classified["random"] >= 100
    print(f"\n=== Gate G2 ===")
    print(f"  classified total: {classified['need-related'] + classified['random']}")
    print(f"  G2 pass (>= 100): {'PASS' if g2_pass else 'FAIL'}")

    # G3 gate: both categories represented
    g3_pass = classified["need-related"] > 0 and classified["random"] > 0
    print(f"\n=== Gate G3 ===")
    print(f"  G3 pass (both categories): {'PASS' if g3_pass else 'FAIL'}")

    # G4 gate: minimum 50 classified
    g4_pass = (classified["need-related"] + classified["random"]) >= 50
    print(f"\n=== Gate G4 ===")
    print(f"  classified total: {classified['need-related'] + classified['random']}")
    print(f"  G4 pass (>= 50): {'PASS' if g4_pass else 'FAIL'}")

    all_pass = g1_pass and g2_pass and g3_pass and g4_pass
    print(f"\n=== Overall ===")
    print(f"  All gates pass: {'YES' if all_pass else 'NO'}")

    # Sort need-related packages: active first, then by number of need indicators present (descending), then alphabetically
    def need_indicator_count(p):
        desc = (p.get("description", "") or "").lower()
        return sum(1 for term in NEED_INDICATORS if _matches_word_boundary(desc, term))

    need_related_pkgs.sort(
        key=lambda p: (
            0 if is_active(p) else 1,
            -need_indicator_count(p),
            p.get("name", "").lower(),
        )
    )

    # Display need-related packages ranked by priority
    print(f"\n=== Need-related packages (top {min(top_n, len(need_related_pkgs))}) ===")
    for i, pkg in enumerate(need_related_pkgs[:top_n]):
        name = pkg.get("name", "N/A")
        version = pkg.get("version", "N/A")
        desc = pkg.get("description", "")[:80] if pkg.get("description") else ""
        active_str = "ACTIVE" if is_active(pkg) else "inactive"
        print(
            f"  {i+1}. {name} {version}"
            f" -- {desc}..."
            f" [{active_str}]"
        )

    # Save results JSON for the session record
    results = {
        "observed_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "user_date": time.strftime("%Y-%m-%d", time.gmtime()),
        "platform": os.uname().machine if hasattr(os, "uname") else "unknown",
        "sample_size": len(packages),
        "classified": classified,
        "active": active,
        "active_rates": {
            "need-related": active["need-related"] / classified["need-related"]
            if classified["need-related"] > 0
            else 0,
            "random": active["random"] / classified["random"] if classified["random"] > 0 else 0,
        },
        "g1_pass": (
            (active["need-related"] / classified["need-related"])
            / (active["random"] / classified["random"] >= 0.55)
            if classified["need-related"] > 0 and classified["random"] > 0
            else False
        ),
        "g2_pass": classified["need-related"] + classified["random"] >= 100,
        "g3_pass": classified["need-related"] > 0 and classified["random"] > 0,
        "g4_pass": (classified["need-related"] + classified["random"]) >= 50,
        "conclusion": "pending",
        "experiment_description": f"View-count prototype v3 search for keyword: {keyword}",
    }

    out_dir = "EXPERIMENTS/073-viewcount-prototype-v3"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n=== Results saved to {out_path} ===")

    return results


def _main():
    """Entry point for command-line usage."""
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 tools/viewcount_cli.py <keyword> [--top N] [--registry pypi]")
        print("       python3 tools/viewcount_cli.py --list-keywords")
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description="View-count principle prototype v3: find need-related packages"
    )
    parser.add_argument("keyword", nargs="?", help="Search keyword or need description")
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="Number of top results to display (default: 10)",
    )
    parser.add_argument(
        "--registry",
        choices=["pypi"],
        default="pypi",
        help="Package registry to search (default: pypi)",
    )
    parser.add_argument(
        "--list-keywords",
        action="store_true",
        help="List example search keywords from past experiments",
    )
    args = parser.parse_args()

    if args.list_keywords:
        print("Example keywords from prior experiments:")
        for kw in [
            "database", "cache", "auth", "security", "logging",
            "monitoring", "testing", "benchmark", "performance", "api",
        ]:
            print(f"  - {kw}")
        return

    if not args.keyword:
        parser.print_usage()
        print(
            "\nEnter a keyword/need description to search for relevant packages.\n"
            "The tool classifies packages as 'need-related' (have a need indicator "
            "in their description) or 'random' and reports active/metadata status."
        )
        return

    keyword = args.keyword
    print(f"=== View-count prototype v3: searching '{keyword}' ===\n")

    results = run_prototype(keyword, max_results=200, top_n=args.top)


if __name__ == "__main__":
    _main()