#!/usr/bin/env python3
"""
Orchestrator for E165 Go module view-count principle test.
"""

import subprocess
import sys
from pathlib import Path


def run_script(script: str, description: str) -> bool:
    """Run a Python script and return success status."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"{'='*60}")
    result = subprocess.run([sys.executable, script], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result.returncode == 0


def main():
    exp_dir = Path(__file__).parent

    # Step 1: Harvest
    if not run_script("harvest.py", "Harvest Go packages from pkg.go.dev"):
        print("Harvest failed!")
        sys.exit(1)

    # Step 2: Classify
    if not run_script("classify.py", "Classify packages"):
        print("Classification failed!")
        sys.exit(1)

    # Step 3: Measure gates
    if not run_script("measure.py", "Measure gate verdicts"):
        print("Measurement failed!")
        sys.exit(1)

    print("\n" + "="*60)
    print("E165 COMPLETE")
    print("="*60)


if __name__ == "__main__":
    main()