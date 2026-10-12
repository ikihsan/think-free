#!/usr/bin/env python3
"""
E105 — View-Count Principle Synthesis Across Ecosystems

Reads existing experiment results and produces a comparative synthesis
of the view-count principle's generalization boundaries.
"""

import json
import sys
from pathlib import Path


def load_results(experiment_dir):
    """Load results.json from an experiment directory."""
    results_path = experiment_dir / "results.json"
    if not results_path.exists():
        print(f"WARNING: {results_path} not found, skipping", file=sys.stderr)
        return None
    with open(results_path, "r") as f:
        return json.load(f)


def get_repo_root():
    """Get the repository root directory."""
    # When run from the experiment directory, go up two levels
    return Path(__file__).parent.parent


from analysers import (analyze_pypi, analyze_npm, analyze_nuget, analyze_github_repos, analyze_crates_io, analyze_maven_central, analyze_huggingface)  # noqa: E402
def main():
    """Main entry point: run synthesis and produce comparison."""
    print("=" * 70)
    print("VIEW-COUNT PRINCIPLE SYNTHESIS ACROSS ECOSYSTEMS")
    print("=" * 70)
    print()

    analyses = [
        ("PyPI", analyze_pypi()),
        ("NPM", analyze_npm()),
        ("NuGet", analyze_nuget()),
        ("GitHub Repos", analyze_github_repos()),
        ("crates.io", analyze_crates_io()),
        ("Maven Central", analyze_maven_central()),
        ("Hugging Face Hub", analyze_huggingface()),
    ]

    # Print comparison table
    print(f"{'Ecosystem':<20} {'G1':<6} {'G2':<6} {'G3':<6} {'G4':<6} {'Active Rate':<15} {'Key Finding'}")
    print("-" * 120)

    for name, a in analyses:
        if a is None:
            print(f"{name:<20} {'—':<6} {'—':<6} {'—':<6} {'—':<6} {'—':<15} {'N/A'}")
            continue
        g1 = "PASS" if a.get("g1_retrieval") else "FAIL"
        g2 = "PASS" if a.get("g2_significant") else "FAIL"
        g3 = "PASS" if a.get("g3_passes") else "FAIL"
        g4 = "PASS" if a.get("g4_arrival") else "FAIL/—"
        # Format active rate
        arc = a.get("need_active_rate", 0)
        rrc = a.get("random_active_rate", 0)
        if isinstance(arc, float) and isinstance(rrc, float):
            active_fmt = f"{arc*100:.1f}% vs {rrc*100:.1f}%"
        else:
            active_fmt = str(a.get("difference_pp", "N/A"))[:8]
        finding = (a.get("key_finding", "")[:55] + "...") if a and a.get("key_finding") else "N/A"

        print(f"{name:<20} {g1:<6} {g2:<6} {g3:<6} {g4:<6} {active_fmt:<15} {finding}")

    print()
    print("-" * 120)

    # Synthesis analysis
    print("=" * 70)
    print("SYNTHESIS & GENERALIZATION BOUNDARIES")
    print("=" * 70)
    print()

    print("PRINCIPLE WORKS on (3 package repositories):")
    print("  • PyPI: 82.93% need-related active vs 57.50% random, all gates met,")
    print("    t=3.4660 p=0.00157, Wilson CI95 LB=0.6874 > 0.6. Difference: 25.43pp.")
    print("  • NPM: 100% need-related active vs 0% random, all gates met,")
    print("    t=66.0 p≪0.001, Wilson CI95 LB=0.7225 > 0.6. 100% vs 0% separation.")
    print("  • NuGet: need-related median 7.8M downloads vs random 195K (~40×), all gates pass,")
    print("    G1-G4 all pass. Effect size: ~40× download ratio.")
    print()
    print("PRINCIPLE DOES NOT GENERALIZE to (4+ ecosystems):")
    print("  • GitHub Repos: G2 FAIL — both arms 100% active by stars, no systematic")
    print("    difference (Mann-Whitney p=0.79). Stars are a uniform popularity metric,")
    print("    not correlated with need-relatedness. The principle requires a varying activity")
    print("    metric, not a flat popularity one.")
    print("  • crates.io: G1 FAIL (n<30), G2 FAIL, G4 PASS — 100% have recent_downloads > 0,")
    print("    eliminating binary discrimination. All crates are 'active', so need-related vs")
    print("    random cannot be distinguished by download activity.")
    print("  • Maven Central: G3 FAIL (7.8pp diff, CI95 LB −0.41 < 10pp threshold), G4 FAIL")
    print("    (arrival-field rate 53.6% < 95% threshold). POM metadata doesn't carry")
    print("    sufficient activity differentiation.")
    print("  • Hugging Face Hub: G2 FAIL (p=0.089), G3 FAIL (LB=0.089). Both need-related")
    print("    and random models have low active rates (12.4% vs 8.6%), signal too weak.")
    print()
    print("KEY FINDING:")
    print("  The view-count principle generalizes consistently across package repositories")
    print("  (PyPI, NPM, NuGet) where the JSON/API metadata exposes activity indicators")
    print("  (download counts, release metrics, version history, project URLs, keywords).")
    print("  It does NOT generalize to:")
    print("  1. Social/media venues without exposable arrival metrics (GitHub issues API,")
    print("     web search), 2. Registries where all items are uniformly active (crates.io),")
    print("     3. Registries where the activity metric is not significantly differentiated")
    print("     between need-related and random packages (Maven Central, Hugging Face Hub),")
    print("     4. Platforms where the metric is a uniform popularity measure (GitHub stars).")
    print()
    print("SINGLE PLATFORM CHARACTERISTIC:")
    print("  The view-count principle works when and only when the platform is a package")
    print("  repository that exposable metadata about independent arrivals (downloads, views,")
    print("  releases, keywords, URLs). Social media, issue tracking, and registries without")
    print("  such metadata are outside the principle's scope. Within package repositories,")
    print("  the effect size varies: NPM shows near-perfect separation (100% vs 0%), PyPI")
    print("  shows a moderate gap (25.43pp), and NuGet shows a large ratio difference (~40×)")
    print("  but more moderate Wilson LB (0.912 > 0.60).")
    print()
    print("NEXT ACTIONS per D083:")
    print("  The view-count principle's boundaries are now well-mapped across 7+ ecosystems.")
    print("  Fresh observation in a new domain should target a platform category not yet tested.")
    print("  Candidates: Go modules, RubyGems, Packagist (PHP), or a completely different")
    print("  domain category (e.g., scientific publications, conference proceedings).")
    print()
    print("=" * 70)

    # Save results
    output = {
        "experiment": "105-viewcount-synthesis",
        "analyses": [a for a in analyses if a is not None],
        "summary": {
            "principle_works_on": ["PyPI", "NPM", "NuGet"],
            "principle_fails_on": ["GitHub Repos", "crates.io", "Maven Central", "Hugging Face Hub"],
            "key_characteristic": "Package repository with exposable activity metadata",
            "effect_size_range": "NPM: 100% vs 0% (near-perfect) to NuGet: ~40× download ratio",
            "boundary_reasoning": {
                "works": "Package repos expose metadata about independent arrivals (releases, downloads, URLs, keywords)",
                "fails-uniform": "All items uniformly active (crates.io: 100% recent_downloads > 0)",
                "fails-insignificant-diff": "Activity-rate difference below gate threshold (Maven Central: 7.8pp < 10pp)",
                "fails-signal-weak": "Both categories have low similar active rates (Hugging Face: 12.4% vs 8.6%)",
                "fails-uniform-metric": "Uniform popularity metric not correlated with need-relatedness (GitHub stars)",
            },
        },
    }

    output_path = Path("/home/ubuntu/think-free") / "EXPERIMENTS" / "105-viewcount-synthesis" / "results.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nSynthesis results written to {output_path}")
    print("\nDone.")


if __name__ == "__main__":
    main()