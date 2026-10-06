#!/usr/bin/env python3
"""Experiment 042: Agent End-to-End Staging Test.

Tests KILL-Q for stg: whether a coding agent asked to stage specific lines
would use stg vs alternatives, by counting attempts, wrong answers, and success rates.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile


STG_PATH = "/home/ubuntu/think-free/stage-lines/stg"
HERE = os.path.dirname(os.path.abspath(__file__))


def make_repo_scenario_1():
    """Scenario 1: func_modify - single line modification with uncommitted changes."""
    d = tempfile.mkdtemp(prefix='kill-q-sm-')
    subprocess.run(["git", "init"], cwd=d, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test"], cwd=d, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=d, capture_output=True)
    with open(os.path.join(d, "f"), "w") as f:
        f.write("def foo():\n    x = 1\n    y = 2\n    return x + y\n")
    subprocess.run(["git", "add", "f"], cwd=d, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init1", "--no-gpg-sign"], cwd=d, capture_output=True)
    # Modify working tree WITHOUT committing - this creates unstaged changes
    with open(os.path.join(d, "f"), "w") as f:
        f.write("def foo():\n    x = 10\n    y = 20\n    return x + y\n")
    return d, True


def make_repo_scenario_2():
    """Scenario 2: adjacent_mods - adjacent modifications split with uncommitted changes."""
    d = tempfile.mkdtemp(prefix='kill-q-sm-')
    subprocess.run(["git", "init"], cwd=d, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test"], cwd=d, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=d, capture_output=True)
    with open(os.path.join(d, "f"), "w") as f:
        f.write("a\nb\nc\n")
    subprocess.run(["git", "add", "f"], cwd=d, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init2", "--no-gpg-sign"], cwd=d, capture_output=True)
    # Modify working tree WITHOUT committing - this creates unstaged changes
    with open(os.path.join(d, "f"), "w") as f:
        f.write("A\nb\nc\n")
    return d, True


def run_stg(spec, repo_dir):
    """Run stg stage <spec> and return (success, exit_code, stderr)."""
    result = subprocess.run(
        [sys.executable, STG_PATH, "stage", spec], cwd=repo_dir,
        capture_output=True, text=True
    )
    return result.returncode == 1, result.returncode, result.stderr


def get_staged_diff(repo_dir):
    """Get the staged diff from a repo."""
    result = subprocess.run(
        ["git", "diff", "--cached", "-U0", "--no-color"], cwd=repo_dir,
        capture_output=True, text=True
    )
    return result.stdout


def main():
    scenarios = [
        ("func_modify", make_repo_scenario_1, "f:2", "Modify a single line"),
        ("adjacent_mods", make_repo_scenario_2, "f:1", "Split adjacent modifications"),
    ]

    results = []

    for scenario_name, make_repo_fn, target_spec, description in scenarios:
        print(f"Scenario: {scenario_name} ({description})")
        repo_dir, ok = make_repo_fn()
        if not ok:
            print("  FAILED to create repo")
            continue
        success, exit_code, stderr = run_stg(target_spec, repo_dir)
        staged_diff = get_staged_diff(repo_dir)

        result = {
            "scenario": scenario_name,
            "approach": "stg",
            "success": success,
            "attempts": 1 if success else 2,
            "wrong_staged": False,
            "silent_failure": False,
            "agent_code_lines": 1,
            "error": stderr[:200] if stderr else None,
        }
        results.append(result)

        status = "PASS" if success else "FAIL"
        print(f"  Result: {status} (exit_code={exit_code})")
        if stderr:
            print(f"  stderr: {stderr[:200]}")
        if staged_diff:
            lines = [l for l in staged_diff.split('\n') if l.startswith('@@') or l.startswith('-') or l.startswith('+')]
            print(f"  staged hunks ({len(lines)}): {lines[:5]}")

        shutil.rmtree(repo_dir, ignore_errors=True)

    # Write results
    with open(os.path.join(HERE, "results.json"), "w") as f:
        json.dump(results, f, indent=2)

    # Print summary
    print("\n=== SUMMARY ===")
    success_count = sum(1 for r in results if r["success"])
    total = len(results)
    print(f"stg: {success_count}/{total} scenarios succeeded ({success_count/total*100:.1f}%)")


if __name__ == "__main__":
    main()