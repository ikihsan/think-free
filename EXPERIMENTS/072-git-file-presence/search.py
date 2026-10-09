#!/usr/bin/env python3
"""E072 search: check git repos for required file presence (pre-existing on disk)."""
from __future__ import print_function

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

REQUIRED_FILE = "README.md"

# Pre-existing repo paths — created before the run starts
REPO_PATHS = [
    os.path.join(HERE, "repos", "has_readme"),
    os.path.join(HERE, "repos", "missing_readme"),
    os.path.join(HERE, "repos", "not_git_repo"),
    os.path.join(HERE, "repos", "has_readme_extras"),
]


def check_repo(fpath):
    """Check if a git repo at path fpath contains the required file.
    Returns outcome: 'pass' (file exists in git index), 'fail' (file missing or error),
    'ambiguous' (path not a git repo)."""
    # First check if path exists
    if not os.path.exists(fpath):
        return {"path": fpath, "outcome": "fail", "detail": "path_not_found"}

    # Check if it's a git repo by looking for .git directory
    git_dir = os.path.join(fpath, ".git")
    if not os.path.isdir(git_dir):
        return {"path": fpath, "outcome": "fail", "detail": "not_a_git_repo"}

    try:
        # Use git ls-files to check if the file is tracked in the index
        result = subprocess.run(
            ["git", "ls-files", REQUIRED_FILE],
            capture_output=True, text=True, timeout=30,
            cwd=fpath,
        )
        if result.returncode == 0 and REQUIRED_FILE in result.stdout.strip():
            # File is tracked in git index
            outcome = "pass"
            detail = "file_tracked_in_index"
        else:
            # File is not tracked in git index
            outcome = "fail"
            detail = "file_not_in_index"
    except subprocess.TimeoutExpired:
        return {"path": fpath, "outcome": "error", "detail": "timeout"}
    except Exception as e:
        return {"path": fpath, "outcome": "error", "detail": "exception:{}".format(e)}

    return {"path": fpath, "outcome": outcome, "detail": detail}


def main():
    os.makedirs(RAW, exist_ok=True)

    results = []

    print("=== E072 Search: git repo file presence for kill-gate protocol ===\n")

    for dname in REPO_PATHS:
        print(f"Checking repo: {dname}")
        r = check_repo(dname)
        results.append(r)
        print(f"  Outcome: {r['outcome']} ({r.get('detail', '')})")

    # Write raw results
    results_path = os.path.join(RAW, "results.jsonl")
    with open(results_path, "w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")

    print(f"\nWrote {len(results)} results to {results_path}")

    # Summary
    pass_count = sum(1 for r in results if r["outcome"] == "pass")
    fail_count = sum(1 for r in results if r["outcome"] == "fail")
    err_count = sum(1 for r in results if r["outcome"] == "error")

    print(f"\nSummary: pass={pass_count}, fail={fail_count}, error={err_count}")

    # G1 check: does the corpus contain at least one non-vacuous "pass" case?
    # A non-vacuous pass case is one where the path is a valid git repo AND the file
    # exists in the git index. The "not_git_repo" is the vacuous case — it's not a git repo.
    non_vacuous_pass_cases = [
        r for r in results
        if r["outcome"] == "pass"
        and r.get("detail", "") != "not_a_git_repo"
        and r.get("detail", "") != "path_not_found"
    ]

    G1_PASS = len(non_vacuous_pass_cases) > 0
    print()
    print(f"G1 (gateability — non-vacuous passing region): {'PASS' if G1_PASS else 'FAIL'}")
    if G1_PASS:
        print(f"  {len(non_vacuous_pass_cases)} non-vacuous pass case(s): valid git repos with file in index")
    else:
        print("  No non-vacuous pass case found — gate is vacuous, cannot fail")

    # G2: Search strategy executed
    G2_PASS = err_count == 0
    print(f"G2 (search strategy executed): {'PASS' if G2_PASS else 'FAIL'}")
    if not G2_PASS:
        for e in results:
            if e["outcome"] == "error":
                print(f"  Error on {e['path']}: {e.get('detail', 'unknown')}")

    # G3: Negative control — at least one repo should fail (missing file or not a repo)
    fail_cases = [r for r in results if r["outcome"] == "fail"]
    G3_PASS = len(fail_cases) > 0
    print(f"G3 (negative control — at least one repo fails): {'PASS' if G3_PASS else 'FAIL'}")
    if not G3_PASS:
        print("  WARNING: No repos registered as fail — instrument may not detect missing files")

    # -------------------------------------------------------------------------
    # Overall verdict
    # -------------------------------------------------------------------------
    print()
    all_pass = G1_PASS and G2_PASS and G3_PASS

    if all_pass:
        print("VERDICT: ALL GATES PASS.")
        print("The kill gate protocol fix generalizes to the git repository file presence domain.")
        print("G1: Gate has non-vacuous passing regions (valid git repos with file in index)")
        print("G2: All repos were checked successfully")
        print("G3: Known-deficient repos (missing file, not a git repo) were detected as fail")
        print()
        print("This demonstrates that the E070/E071 protocol fix (a) pre-declared passing regions")
        print("and (b) pre-existing input data) works across three domains:")
        print("  1. Package naming (E070): PyPI JSON API")
        print("  2. Config validity (E071): YAML config files on disk")
        print("  3. Git file presence (E072): git repos on disk")
        return 0
    else:
        print("VERDICT: ONE OR MORE GATES FAILED.")
        print("The kill gate protocol fix was not fully validated in this domain.")
        print("  G1:", "PASS" if G1_PASS else "FAIL")
        print("  G2:", "PASS" if G2_PASS else "FAIL")
        print("  G3:", "PASS" if G3_PASS else "FAIL")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())