        "active": active,
        "active_rates": {
            "need-related": active["need-related"] / classified["need-related"] if classified["need-related"] > 0 else 0,
            "random": active["random"] / classified["random"] if classified["random"] > 0 else 0,
        },
        "g1_sample_size_pass": g1_pass,
        "g2_coverage_floor_pass": g2_pass_check,
        "g3_cliff_delta_pass": g3_pass,
        "g4_bothrepresented_pass": g4_pass,
        "cliff_delta": cliff_d if 'cliff_d' in dir() else 0,
        "need_arm_size": len(need_arm),
        "random_arm_size": len(random_arm),
        "conclusion": "GATE_OPEN" if all([g1_pass, g2_pass_check, g3_pass, g4_pass]) else "GATE_CLOSED",
        "domain": "cpan_perl_package_ecosystem",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    out_dir = os.path.join(REPO_ROOT, "EXPERIMENTS", "e139-cpan-experiment")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "results_continuation.json"), "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults written to {out_dir}/results_continuation.json")

    # Step 8: Decision
    if all([g1_pass, g2_pass_check, g3_pass, g4_pass]):
        print(f"\n" + "=" * 60)
        print("CONCLUSION: GATE_OPEN - All gates passed!")
        print("Fresh observation: The view-count principle extends to the CPAN")
        print("Perl package ecosystem. This adds a new domain to the principle's")
        print("validated boundary map, alongside PyPI, NPM, NuGet, Discourse,")
        print("and Stack Exchange non-software.")
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
        print("  This narrows the principle's domain: it does not generalize to")
        print("  CPAN/Perl packages with the current classifier design.")
        print("  Alternative designs or domains should be explored.")
        print("=" * 60)


if __name__ == "__main__":
    main()