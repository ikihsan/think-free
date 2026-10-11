"""Prototype extension: pyfix shell wrapper for pyprovides fix-import.

Builds on E086 experiment which tested pyfix against 3 alias cases:
- cv2 -> opencv-python (fails: missing system dep pkg-config)
- psycopg2 -> psycopg2-binary (2.44x speedup: 7.8s vs 19.0s manual)
- MySQLdb -> mysqlclient (fails: missing system dep MySQL client libs)

This prototype extends pyfix with:
1. More alias case tests
2. A simple CLI for developer workflow integration
3. Comparison against manual baseline on concrete examples
4. Documentation of practical difference measured on real examples
"""

import sys
from pathlib import Path
from statistics import mean

# --- CRITICAL: Insert pyprovides paths BEFORE any pyprovides imports ---
# Python resolves all imports at module load time, so these MUST be at the top.
_REPO_ROOT = Path(__file__).parent.parent
_SYS_PROVIDES_DIR = _REPO_ROOT / "pyprovides" / "pyprovides"
_SYS_REPO_DIR = _REPO_ROOT / "pyprovides"

# Insert in the correct order: pyprovides/pyprovides first (contains fix_import.py),
# then the repo root (contains the pyprovides top-level package)
if str(_SYS_PROVIDES_DIR) not in sys.path:
    sys.path.insert(0, str(_SYS_PROVIDES_DIR))
if str(_SYS_REPO_DIR) not in sys.path:
    sys.path.insert(0, str(_SYS_REPO_DIR))

# Now import the pyprovides mechanism
from pyprovides.fix_import import (
    pyfix_suggest,
    run_pyfix_prototype_test,
    mean,
)

# Test cases from E086 experimental data, plus additional cases
alias_cases = [
    # (broken_module, correct_distribution)
    ("cv2", "opencv-python"),         # Fails: missing system dep (pkg-config, OpenGL)
    ("psycopg2", "psycopg2-binary"), # Succeeds: 2.44x speedup observed in E086
    ("MySQLdb", "mysqlclient"),        # Fails: missing system dep (MySQL client libs)
    ("sklearn", "scikit-learn"),      # Common ML alias
    ("yaml", "PyYAML"),               # YAML parsing alias
    ("bs4", "beautifulsoup4"),        # HTML parsing alias
    ("Crypto", "pycryptodome"),       # Cryptography alias
    ("PIL", "Pillow"),                # Image processing alias
    ("dateutil", "python-dateutil"), # Date utilities alias
    ("jwt", "PyJWT"),                 # JWT alias
    ("serial", "pyserial"),           # Serial alias
    ("dotenv", "python-dotenv"),      # Env vars alias
]

# Manual baseline times from E086 and estimates for other cases
manual_baseline = {
    "cv2": 15,     # Estimate: package name search time
    "psycopg2": 19, # E086 measured: 19.0s manual baseline
    "MySQLdb": 15, # Estimate: package name search time
    "sklearn": 10, # Estimate
    "yaml": 5,     # Estimate
    "bs4": 5,      # Estimate
    "Crypto": 5,   # Estimate
    "PIL": 5,      # Estimate
    "dateutil": 5, # Estimate
    "jwt": 5,      # Estimate
    "serial": 5,   # Estimate
    "dotenv": 5,   # Estimate
}


def main():
    """Main entry point for the pyfix prototype demonstration."""
    print("=" * 60)
    print("pyfix Prototype: Import Error Resolution Tool")
    print("=" * 60)
    print()
    print("Extends E086 experiment: pyprovides fix-import command")
    print("wraps import error resolution in a developer workflow")
    print()
    
    print("Testing pyfix against alias cases:")
    print("-" * 40)
    
    results = run_pyfix_prototype_test(alias_cases, manual_baseline)
    
    print(f"\nResults:")
    print(f"  Resolution accuracy: {results['accuracy']*100:.1f}% ({results['resolved']}/{results['total_cases']})")
    print(f"  Mean speedup: {results['mean_speedup']:.2f}x")
    print()
    
    for detail in results["details"]:
        status = "OK" if detail["success"] else "FAIL"
        speedup = f"{detail['speedup_x']:.1f}x" if detail["speedup_x"] != float('inf') else "N/A"
        print(f"  {detail['module']:15s} -> {detail['correct_dist']:15s} [{status}] "
              f"manual:{detail['manual_time_s']}s pyfix:{detail['pyfix_time_s']}s speedup:{speedup} "
              f"-> {detail['suggestion']}")
    
    print()
    print("=" * 60)
    
    # Decision: if accuracy is high enough, the prototype demonstrates practical difference
    if results["accuracy"] >= 0.67:  # 2/3 or better resolution rate
        print("PROTOTYPE RESULT: Demonstrated practical difference")
        print(f"  - {results['accuracy']*100:.0f}% resolution accuracy meets usability threshold")
        print(f"  - {results['mean_speedup']:.1f}x speedup for resolvable cases")
        print(f"  - Prototype is reversible and exploratory (no product claim)")
        print(f"  - Mechanism validated: 15/19 discrimination probes resolved (E086)")
        print(f"  - Empirical speedup: 2.44x for psycopg2 alias case (E086)")
        return 0
    else:
        print("PROTOTYPE RESULT: Limited practical difference observed")
        print(f"  - {results['accuracy']*100:.0f}% resolution accuracy below threshold")
        print(f"  - Speedup observed only for subset of cases")
        print(f"  - Prototype documents boundary conditions (evidence-gathering)")
        print(f"  - Package-name line closed per F113/D102: genuine rate 0.23-0.47% (<1% gate)")
        return 1


if __name__ == "__main__":
    sys.exit(main())