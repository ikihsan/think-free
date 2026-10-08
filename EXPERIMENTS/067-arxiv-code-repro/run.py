#!/usr/bin/env python3"
"""
Orchestrator for E067 - ArXiv computational paper reproducibility experiment.
"""

import subprocess
import sys
import os

def run_step(name, script):
    """Run a step and return success."""
    print(f"\n{'='*60}")
    print(f"STEP: {name}")
    print(f"{'='*60}")
    result = subprocess.run([sys.executable, script], cwd=os.path.dirname(__file__))
    if result.returncode != 0:
        print(f"FAILED: {name}")
        return False
    print(f"PASSED: {name}")
    return True

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Create raw directory
    os.makedirs('raw', exist_ok=True)

    steps = [
        ("Fetch ArXiv papers", "fetch.py"),
        ("Assess repositories", "assess.py"),
        ("Run unit tests", "-m unittest test_assess -v"),
        ("Generate report", "report.py"),
    ]

    for name, script in steps:
        if script.startswith('-m'):
            # Module execution
            parts = script.split()
            result = subprocess.run([sys.executable] + parts, cwd=os.path.dirname(__file__))
            if result.returncode != 0:
                print(f"FAILED: {name}")
                return 1
            print(f"PASSED: {name}")
        else:
            if not run_step(name, script):
                return 1

    print("\n" + "="*60)
    print("ALL STEPS COMPLETED")
    print("="*60)
    return 0

if __name__ == '__main__':
    sys.exit(main())