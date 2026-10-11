#!/usr/bin/env python3
"""
Run the complete E100 experiment: harvest and classify lab instrument error code topics.
"""

import subprocess
import sys
import json


def run_harvest():
    """Run the harvest step."""
    print("=== Running harvest ===")
    result = subprocess.run([sys.executable, 'harvest.py'], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result.returncode == 0


def run_classify():
    """Run the classification step."""
    print("=== Running classification ===")
    result = subprocess.run([sys.executable, 'classify.py'], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result.returncode == 0


def main():
    print("E100: Fresh observation in lab instrument error codes domain")
    print("Session: 2026-10-11-007")
    print()
    
    # Step 1: Harvest
    if not run_harvest():
        print("Harvest failed")
        return 1
    
    # Step 2: Classify
    if not run_classify():
        print("Classification failed")
        return 1
    
    # Load and print final results
    try:
        with open('results.json', 'r') as f:
            results = json.load(f)
        
        print("\n=== FINAL RESULTS ===")
        gates = results['gates']
        all_pass = all(gates[g]['pass'] for g in gates if g != 'counts')
        
        for gate_name, gate_result in gates.items():
            if gate_name == 'counts':
                continue
            status = "PASS" if gate_result['pass'] else "FAIL"
            print(f"  {gate_name}: {status}")
            print(f"    {gate_result['detail']}")
        
        print(f"\n=== OVERALL: {'ALL GATES PASS' if all_pass else 'SOME GATES FAIL'} ===")
        
        if all_pass:
            print("\nRESULT: view_count principle generalizes to lab instrument forums")
            print("Unserved-open-like fraction measured with Wilson CI95")
        else:
            print("\nRESULT: view_count principle does NOT fully generalize, or population insufficient")
        
    except FileNotFoundError:
        print("No results.json found")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())