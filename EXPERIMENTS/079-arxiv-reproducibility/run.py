#!/usr/bin/env python3
"""
Run E079 ArXiv reproducibility experiment.

Harvests A2+A3 papers, runs spec generation tool, tests install+smoke,
compares with repo2docker baseline.
"""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from experiment import (
    clone_repo, run_tool_on_repo, test_install_and_smoke, run_repo2docker_baseline,
    load_papers, select_a2_a3_papers, evaluate_gates, print_results
)


def main():
    parser = argparse.ArgumentParser(description="Run E079 ArXiv reproducibility experiment")
    parser.add_argument("--sample", type=int, default=20, help="Number of A2+A3 papers to test")
    parser.add_argument("--harvest", default="raw/harvested_papers.jsonl", help="Harvested papers file")
    parser.add_argument("--gate", action="store_true", help="Evaluate kill gates")
    parser.add_argument("--skip-harvest", action="store_true", help="Skip harvesting, use existing file")
    args = parser.parse_args()

    harvest_file = Path(args.harvest)

    if not args.skip_harvest:
        print("=" * 60)
        print("Step 1: Harvesting papers")
        print("=" * 60)
        harvest_file.parent.mkdir(parents=True, exist_ok=True)
        # Run harvest script
        result = subprocess.run([
            sys.executable, "harvest.py",
            "--max", str(args.sample * 5),  # Harvest more to get enough A2+A3
            "--output", str(harvest_file)
        ], capture_output=True, text=True, timeout=600)
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)

    if not harvest_file.exists():
        print(f"Harvest file not found: {harvest_file}", file=sys.stderr)
        return 1

    papers = load_papers(harvest_file)
    test_papers = select_a2_a3_papers(papers, args.sample)

    print(f"\nSelected {len(test_papers)} A2+A3 papers for testing")

    # Results storage
    results = {
        "papers_tested": len(test_papers),
        "tool": {"install_success": 0, "smoke_success": 0, "combined_success": 0, "details": []},
        "baseline": {"install_success": 0, "smoke_success": 0, "combined_success": 0, "details": []},
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)

        for i, paper in enumerate(test_papers):
            print(f"\n[{i+1}/{len(test_papers)}] {paper['arxiv_id']} -> {paper['github_owner']}/{paper['github_repo']}")

            # Clone repo
            repo_dir = tmp / f"repo_{i}"
            if not clone_repo(paper["github_url"], repo_dir):
                print(f"  Clone failed, skipping")
                continue

            # Extract year from published date
            year = 2024
            if paper.get("published"):
                try:
                    year = int(paper["published"][:4])
                except:
                    pass

            # Run tool
            req_file = tmp / f"req_{i}.txt"
            tool_ok, tool_reqs, tool_meta = run_tool_on_repo(repo_dir, year, req_file)

            if tool_ok and tool_reqs:
                print(f"  Tool generated {len(tool_reqs)} requirements")
                # Test install + smoke
                install_ok, msg = test_install_and_smoke(req_file, repo_dir)
                tool_smoke = install_ok
                if install_ok:
                    results["tool"]["install_success"] += 1
                    results["tool"]["combined_success"] += 1
                print(f"  Tool: install={'OK' if install_ok else 'FAIL'}, smoke={'OK' if tool_smoke else 'FAIL'} - {msg}")
                results["tool"]["details"].append({
                    "arxiv_id": paper["arxiv_id"],
                    "repo": f"{paper['github_owner']}/{paper['github_repo']}",
                    "install": install_ok,
                    "smoke": tool_smoke,
                    "requirements": tool_reqs,
                    "message": msg,
                })
            else:
                print(f"  Tool failed to generate spec")
                results["tool"]["details"].append({
                    "arxiv_id": paper["arxiv_id"],
                    "repo": f"{paper['github_owner']}/{paper['github_repo']}",
                    "install": False,
                    "smoke": False,
                    "error": tool_meta.get("error", "Unknown"),
                })

            # Run baseline (repo2docker) - only on subset to save time
            if i < 5:  # Test baseline on first 5 papers
                print(f"  Running repo2docker baseline...")
                base_ok, base_msg = run_repo2docker_baseline(repo_dir)
                if base_ok:
                    results["baseline"]["install_success"] += 1
                    results["baseline"]["combined_success"] += 1
                print(f"  Baseline: {'OK' if base_ok else 'FAIL'} - {base_msg}")
                results["baseline"]["details"].append({
                    "arxiv_id": paper["arxiv_id"],
                    "repo": f"{paper['github_owner']}/{paper['github_repo']}",
                    "success": base_ok,
                    "message": base_msg,
                })

    # Save results
    results_file = Path("results.json")
    with open(results_file, "w") as f:
        json.dump(results, f, indent=2)

    # Evaluate gates
    verdict = evaluate_gates(results)
    with open("verdict.json", "w") as f:
        json.dump(verdict, f, indent=2)

    # Print summary
    all_pass = print_results(results, verdict)
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())