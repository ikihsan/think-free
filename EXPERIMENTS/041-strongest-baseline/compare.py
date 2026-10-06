#!/usr/bin/env python3
"""Compare stg vs strongest shell baseline on E040 cases."""
import json
import os
import sys
import tempfile
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
STG = os.path.join(HERE, "..", "..", "stage-lines", "stg")
sys.path.insert(0, HERE)
from shell_baseline import ShellBaseline
from test_shell_baseline import make_repo, CASES


def staged_blob(root):
    p = subprocess.run(["git", "show", ":f"], cwd=root, capture_output=True)
    return p.stdout.decode() if p.returncode == 0 else None


def run_stg(repo, path, line):
    result = subprocess.run(
        [sys.executable, STG, "stage", f"{path}:{line}"],
        cwd=repo, capture_output=True
    )
    staged = staged_blob(repo)
    return {
        "route": "stg",
        "exit": result.returncode,
        "stdout": result.stdout.decode(),
        "stderr": result.stderr.decode(),
        "staged": repr(staged) if staged else None
    }


def run_baseline(repo, path, line):
    baseline = ShellBaseline()
    rc, out, err, staged = baseline.stage(repo, path, line)
    return {
        "route": "shell_baseline",
        "exit": rc,
        "stdout": out,
        "stderr": err,
        "staged": repr(staged) if staged else None
    }


def main():
    os.makedirs(os.path.join(HERE, "raw"), exist_ok=True)
    rows = []
    for name, base, work, line, expected in CASES:
        for route_name, route_fn in [("stg", run_stg), ("shell_baseline", run_baseline)]:
            repo = make_repo(base, work)
            result = route_fn(repo, "f", line)
            result["case"] = name
            result["expected"] = repr(expected)
            result["exact"] = (result["staged"] == repr(expected))
            result["honest"] = (result["exit"] == 2 and not result["exact"] and 
                               result["staged"] in (repr(base), "None")) or result["exact"]
            rows.append(result)
            print(json.dumps(result))
    
    with open(os.path.join(HERE, "raw", "comparison.jsonl"), "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    
    # Summary
    print("\n--- Summary ---")
    for route in ["stg", "shell_baseline"]:
        route_rows = [r for r in rows if r["route"] == route]
        exact = sum(1 for r in route_rows if r["exact"])
        honest = sum(1 for r in route_rows if r["honest"])
        print(f"{route}: exact={exact}/5, honest={honest}/5")
    
    # Kill gate
    sb_rows = [r for r in rows if r["route"] == "shell_baseline"]
    if all(r["exact"] and r["honest"] for r in sb_rows):
        print("\nKILL GATE MET: shell baseline matches stg exactly and honestly")
        sys.exit(1)  # Signal kill
    else:
        print("\nKILL GATE NOT MET: stg retains practical advantage")
        sys.exit(0)


if __name__ == "__main__":
    main()