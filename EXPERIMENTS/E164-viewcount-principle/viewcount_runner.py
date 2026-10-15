        verdict = "passed: G1-G4 all PASS"
    
    # Build results
    results = {
        "experiment": f"E164 — View-count principle {platform.upper()} fresh observation (prototype)",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "source": "prototype_run",
        "target_domain": platform,
        "sample_size": len(all_projects),
        "classified": {"need-related": len(need_related), "random": len(random_repos)},
        "activity": {
            "need_related_active": len(need_nonzero),
            "need_related_inactive": len(need_related) - len(need_nonzero),
            "random_active": len(random_nonzero),
            "random_inactive": len(random_repos) - len(random_nonzero),
        },
        "gates": gates,
        "verdict": verdict,
        "cliff_delta": cliff,
        "key_finding": f"Platform: {platform}; classifier vocabulary: {'GitHub-designed' if platform == 'github' else 'GitLab-adapted'}; sample size: {len(all_projects)}; classification rate: {len(need_related)/len(all_projects)*100 if False else len(need_related)/len(all_projects)*100:.1f}% need-related"
    }
    
    return results, gates, verdict


# ---------------------------------------------------------------------------
# Prototype CLI
# ---------------------------------------------------------------------------

def main():
    """CLI entry point for the E164 prototype."""
    if len(sys.argv) < 2:
        print("Usage: python3 viewcount_prototype.py <github|gitlab> [samples_per_topic]")
        print("  github  - Run experiment on GitHub (requires API integration)")
        print("  gitlab  - Run experiment on GitLab (uses public HTTP API)")
        sys.exit(1)
    
    platform = sys.argv[1].lower()
    samples = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    
    if platform not in ("github", "gitlab"):
        print(f"Error: platform must be 'github' or 'gitlab', got '{platform}'")
        sys.exit(1)
    
    results, gates, verdict = run_experiment(platform=platform, topics_per_topic=samples)
    
    # Save results
    out_dir = f"EXPERIMENTS/E164-viewcount-prototype"
    os.makedirs(out_dir, exist_ok=True)
    results_path = os.path.join(out_dir, "results.json")
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{results['verdict']}")
    print(f"Results saved to {results_path}")
    print(f"\nGates summary:")
    for gate_name, gate_data in gates.items():
        print(f"  {gate_name}: {'PASS' if gate_data['met'] else 'FAIL'} — {gate_data['observed']}")


if __name__ == "__main__":
    main()