#!/usr/bin/env python3
"""
E084 — Run PX4 fault code fresh observation experiment
Orchestrates harvest, measurement, and detail fetching.
"""

import subprocess
import sys
import json
from pathlib import Path


def run_script(script_name):
    """Run a Python script and return success status."""
    print(f"\n{'='*60}")
    print(f"Running {script_name}...")
    print(f"{'='*60}")
    result = subprocess.run([sys.executable, script_name], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result.returncode == 0


def main():
    print("=== E084 PX4 Fault Code Fresh Observation Experiment ===")
    
    # Step 1: Harvest topics
    if not run_script("harvest.py"):
        print("Harvest failed!")
        sys.exit(1)
    
    # Step 2: Measure automated gates (G1-G3)
    if not run_script("measure.py"):
        print("Measurement failed!")
        sys.exit(1)
    
    # Step 3: Fetch details for G4 assessment
    if not run_script("fetch_details.py"):
        print("Detail fetching failed!")
        sys.exit(1)
    
    # Step 4: Final verdict
    print(f"\n{'='*60}")
    print("FINAL VERDICT")
    print(f"{'='*60}")
    
    # Load results
    with open("results.json") as f:
        results = json.load(f)
    
    with open("g4_assessment.json") as f:
        g4 = json.load(f)
    
    print(f"G1 Population (proxy): {'PASS' if results['g1_population_proxy'] else 'FAIL'}")
    print(f"G2 Fault concentration: {'PASS' if results['g2_fault_concentration'] else 'FAIL'}")
    print(f"G3 Airframe coverage: {'PASS' if results['g3_airframe_coverage'] else 'FAIL'}")
    print(f"G4 Root cause specificity: {'PASS' if g4.get('g4_pass') else 'FAIL' if g4.get('g4_pass') is not None else 'PENDING'}")
    print(f"G5 Incumbent gap: PENDING (manual survey needed)")
    
    all_gates = [
        results['g1_population_proxy'],
        results['g2_fault_concentration'],
        results['g3_airframe_coverage'],
        g4.get('g4_pass'),
    ]
    
    # All automated gates must pass for candidate to survive
    if all(g is True for g in all_gates):
        print("\n>>> CANDIDATE SURVIVES ALL AUTOMATED GATES <<<")
        print("Next: Conduct G5 incumbent survey manually")
    else:
        print("\n>>> CANDIDATE KILLED BY AUTOMATED GATES <<<")
        failed = []
        if not results['g1_population_proxy']: failed.append("G1")
        if not results['g2_fault_concentration']: failed.append("G2")
        if not results['g3_airframe_coverage']: failed.append("G3")
        if g4.get('g4_pass') is False: failed.append("G4")
        print(f"Failed gates: {', '.join(failed)}")


if __name__ == "__main__":
    main()