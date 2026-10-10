#!/usr/bin/env python3
"""
E091 — Import-error population measurement experiment.
Orchestrates harvest, classification, and gate evaluation.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run_script(script_name, args=None):
    """Run a Python script and return success status."""
    cmd = [sys.executable, script_name]
    if args:
        cmd.extend(args)
    print(f"\n{'='*60}")
    print(f"Running {script_name} {' '.join(args) if args else ''}...")
    print(f"{'='*60}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description="Run E091 import-error population experiment")
    parser.add_argument("--harvest", action="store_true", help="Run harvest step")
    parser.add_argument("--classify", action="store_true", help="Run classification step")
    parser.add_argument("--gate", action="store_true", help="Evaluate kill gates")
    parser.add_argument("--all", action="store_true", help="Run all steps")
    args = parser.parse_args()

    if not any([args.harvest, args.classify, args.gate, args.all]):
        parser.print_help()
        return 1

    print("=== E091 Import-Error Population Experiment ===")

    if args.all or args.harvest:
        if not run_script("harvest.py"):
            print("Harvest failed!")
            return 1

    if args.all or args.classify:
        if not run_script("classify.py"):
            print("Classification failed!")
            return 1

    if args.all or args.gate:
        if not run_script("evaluate_gates.py"):
            print("Gate evaluation failed!")
            return 1

    # Print final summary
    results_file = Path("results.json")
    if results_file.exists():
        with open(results_file) as f:
            results = json.load(f)
        print(f"\n{'='*60}")
        print("FINAL SUMMARY")
        print(f"{'='*60}")
        print(f"Total import-error reports sampled: {results.get('total_sampled', 'N/A')}")
        print(f"Module-no-dist reports: {results.get('module_no_dist_count', 'N/A')}")
        print(f"Rate: {results.get('module_no_dist_rate', 'N/A'):.2%}")
        print(f"G1 (rate >= 1%): {'PASS' if results.get('g1_pass') else 'FAIL'}")
        print(f"G2 (sample >= 200): {'PASS' if results.get('g2_pass') else 'FAIL'}")
        print(f"G3 (venue diversity): {'PASS' if results.get('g3_pass') else 'FAIL'}")

        if all([results.get('g1_pass'), results.get('g2_pass'), results.get('g3_pass')]):
            print("\n>>> POPULATION MEETS THRESHOLD — RESOLVER HAS DEMAND <<<")
        else:
            print("\n>>> POPULATION BELOW THRESHOLD — CLOSE THE LINE <<<")
            failed = []
            if not results.get('g1_pass'): failed.append("G1")
            if not results.get('g2_pass'): failed.append("G2")
            if not results.get('g3_pass'): failed.append("G3")
            print(f"Failed gates: {', '.join(failed)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())