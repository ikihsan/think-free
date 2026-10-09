#!/usr/bin/env python3
"""E070 — Package name guard gap measurement (redesigned for speed).

Measures the fraction of plausible near-miss PyPI package names
that pip's `pip install --dry-run` does NOT warn about,
exposing the gap in pip's "did you mean" / typo-protection coverage.

Redesigned: parallel execution with 10s timeouts, focused name set.
"""

import json
import sys
import os
import subprocess
import re
import math
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

# ────────────────────────────────────────────────────────────────────
# Configuration
# ────────────────────────────────────────────────────────────────────

NAMES_PYPI_TSV = "/home/ubuntu/think-free/EXPERIMENTS/064-remedy-existence/raw/names-pypi.tsv"
NAMES_CRATES_TSV = "/home/ubuntu/think-free/EXPERIMENTS/064-remedy-existence/raw/names-crates.tsv"

RESULTS_JSON = "/home/ubuntu/think-free/EXPERIMENTS/070-name-guard-gap/results.json"

WARN_KEYWORDS = ["did you mean", "similar", "ambiguous", "perhaps you meant"]

# ────────────────────────────────────────────────────────────────────
# Helpers
# ────────────────────────────────────────────────────────────────────

def parse_tsv_names(path):
    names = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) >= 3:
                names.append(parts[2])
    return names


def run_pip_dry_run(name):
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--dry-run", name],
            capture_output=True, text=True, timeout=10
        )
        combined = (result.stdout + " " + result.stderr).lower()
        has_warning = any(kw in combined for kw in WARN_KEYWORDS)
        return {"name": name, "exit": result.returncode, "warn": has_warning,
                "stdout": result.stdout.lower(), "stderr": result.stderr.lower()}
    except subprocess.TimeoutExpired:
        return {"name": name, "exit": -1, "warn": False, "stdout": "", "stderr": "timeout"}
    except Exception as e:
        return {"name": name, "exit": -2, "warn": False, "stdout": "", "stderr": str(e)}


def wilson_ci(k, n, z=1.96):
    """Wilson score interval for proportion k/n, returns (lower, upper)."""
    if n == 0:
        return (1.0, 0.0)
    if k == 0:
        return (0.0, z / (1 + z*z/n) * z / n)  # approximate very low
    if k == n:
        return (1 - z / (1 + z*z/n) * z / n, 1.0)
    p_hat = k / n
    center = p_hat + z*z / (2*n)
    margin = z * math.sqrt((p_hat*(1-p_hat) + z*z/(4*n)) / n)
    lower = (center - margin) / (1 + z*z/n)
    upper = (center + margin) / (1 + z*z/n)
    return (max(0.0, min(1.0, lower)), min(1.0, max(0.0, upper)))


# ────────────────────────────────────────────────────────────────────
# Main
# ────────────────────────────────────────────────────────────────────

def main():
    pypi_names = parse_tsv_names(NAMES_PYPI_TSV)
    crates_names = parse_tsv_names(NAMES_CRATES_TSV)

    testable_pypi = [n for n in pypi_names if n.strip()][:50]  # limit to 50 for speed
    testable_crates = [n for n in crates_names if n.strip()][:50]

    print(f"PyPI names to test: {len(testable_pypi)}")
    print(f"Crates.io names to test: {len(testable_crates)}")

    # Parallel pip testing
    pypi_results = []
    with ThreadPoolExecutor(max_workers=8) as exec:
        futures = {exec.submit(run_pip_dry_run, n): n for n in testable_pypi}
        for fut in as_completed(futures):
            pypi_results.append(fut.result())

    crates_results = []
    with ThreadPoolExecutor(max_workers=8) as exec:
        futures = {exec.submit(run_pip_dry_run, n): n for n in testable_crates}
        for fut in as_completed(futures):
            crates_results.append(fut.result())

    # Categorize
    pypi_warned = sum(1 for r in pypi_results if r["warn"])
    pypi_gap = len([r for r in pypi_results if not r["warn"] and r["exit"] in (1, -1, -2)])
    pypi_gap_frac = pypi_gap / len(pypi_results) if pypi_results else 0
    pypi_warn_frac = pypi_warned / len(pypi_results) if pypi_results else 0

    crates_warned = sum(1 for r in crates_results if r["warn"])
    crates_gap = len([r for r in crates_results if not r["warn"] and r["exit"] in (1, -1, -2)])
    crates_gap_frac = crates_gap / len(crates_results) if crates_results else 0
    crates_warn_frac = crates_warned / len(crates_results) if crates_results else 0

    # Wilson CI
    pypi_ci = wilson_ci(pypi_gap, len(pypi_results))
    crates_ci = wilson_ci(crates_gap, len(crates_results))

    # G3 kill gate
    pypi_gate_fail = pypi_ci[0] >= 0.15  # lower CI >= 0.15 → FAIL
    pypi_gate_pass = pypi_ci[1] <= 0.05  # upper CI <= 0.05 → PASS
    pypi_gate_inconclusive = not pypi_gate_fail and not pypi_gate_pass

    crates_gate_fail = crates_ci[0] >= 0.15
    crates_gate_pass = crates_ci[1] <= 0.05
    crates_gate_inconclusive = not crates_gate_fail and not crates_gate_pass

    # Overall verdict
    if pypi_gate_fail and crates_gate_fail:
        verdict = "KILL — pip's name guard gap is too large across ecosystems"
    elif not pypi_gate_fail and not crates_gate_fail:
        verdict = "PASS — pip's name guard gap is small enough across ecosystems"
    elif pypi_gate_fail and not crates_gate_fail:
        verdict = "KILL (PyPI-only)"
    elif not pypi_gate_fail and crates_gate_fail:
        verdict = "KILL (Crates.io-only)"
    else:
        verdict = "INCONCLUSIVE"

    results = {
        "experiment": "E070",
        "question": "pip's 'did you mean' warning fraction for near-miss package names",
        "population": f"PyPI: {len(testable_pypi)} names; Crates.io: {len(testable_crates)} names",
        "pypi": {
            "names_tested": len(pypi_results),
            "warned": pypi_warned,
            "gap_fraction": pypi_gap_frac,
            "gap_wilson_ci95": pypi_ci,
            "gate_G3": {
                "result": "FAIL" if pypi_gate_fail else ("PASS" if pypi_gate_pass else "INCONCLUSIVE"),
                "lower_CI95": pypi_ci[0],
                "upper_CI95": pypi_ci[1],
            },
        },
        "crates": {
            "names_tested": len(crates_results),
            "warned": crates_warned,
            "gap_fraction": crates_gap_frac,
            "gap_wilson_ci95": crates_ci,
            "gate_G3": {
                "result": "FAIL" if crates_gate_fail else ("PASS" if crates_gate_pass else "INCONCLUSIVE"),
                "lower_CI95": crates_ci[0],
                "upper_CI95": crates_ci[1],
            },
        },
        "verdict": verdict,
    }

    with open(RESULTS_JSON, "w") as f:
        json.dump(results, f, indent=2)

    print(json.dumps(results, indent=2))

    # Print summary
    print(f"\n--- Summary ---")
    print(f"PyPI: {pypi_warned}/{len(pypi_results)} warned ({pypi_warn_frac:.1%}), gap: {pypi_gap}/{len(pypi_results)} ({pypi_gap_frac:.1%})")
    print(f"PyPI Wilson CI95: [{pypi_ci[0]:.3f}, {pypi_ci[1]:.3f}], gate G3: {'FAIL' if pypi_gate_fail else ('PASS' if pypi_gate_pass else 'INCONCLUSIVE')}")
    print(f"Crates.io: {crates_warned}/{len(crates_results)} warned ({crates_warn_frac:.1%}), gap: {crates_gap}/{len(crates_results)} ({crates_gap_frac:.1%})")
    print(f"Crates.io Wilson CI95: [{crates_ci[0]:.3f}, {crates_ci[1]:.3f}], gate G3: {'FAIL' if crates_gate_fail else ('PASS' if crates_gate_pass else 'INCONCLUSIVE')}")
    print(f"\nOverall verdict: {verdict}")

    # Exit: 2 if kill gate triggered (candidate killed), 0 otherwise
    sys.exit(2 if (pypi_gate_fail or crates_gate_fail) else 0)


if __name__ == "__main__":
    main()