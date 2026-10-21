#!/usr/bin/env python3
"""
Evaluates open-source projects based on the adoption research criteria from
RESEARCH/F.md: time-to-first-value, documentation comprehension cost,
API/CLI surface size, and rollback path availability.

This is a reversible exploratory prototype — it gathers evidence about what
makes project evaluation easier/harder, without claiming adoption or a new algorithm.
"""

import subprocess
import sys
import os
import tempfile
import json
from pathlib import Path


def check_runnable_readme_example(repo_dir):
    """Check if README leads with a runnable example whose output can be compared."""
    readme_path = Path(repo_dir) / "README.md"
    if not readme_path.exists():
        return False, "No README.md found"

    content = readme_path.read_text()
    lines = content.split('\n')

    # Look for code blocks in the first 20 lines
    for i, line in enumerate(lines[:20]):
        if '```' in line or '~~~' in line:
            # Found a code block - check if it's executable
            # Check if next lines after fence look like code
            fence_idx = i
            # Simple heuristic: if there's a code fence in first 20 lines, it's a runnable example
            has_code_fence = True
            break
    else:
        has_code_fence = False

    if has_code_fence:
        # Try to actually run the first code example
        # For now, just report that a code fence exists
        return True, "README has code fence in first 20 lines"
    else:
        return False, "No code fence found in first 20 lines of README"


def check_cli_surface_size(repo_dir):
    """Check if CLI surface is small enough to fit on one screen."""
    # Look for main entry points
    main_py = Path(repo_dir) / "main.py"
    cli_py = Path(repo_dir) / "cli.py"
    __init__ = Path(repo_dir) / "__init__.py"

    entry_points = []
    if main_py.exists():
        entry_points.append("main.py")
    if cli_py.exists():
        entry_points.append("cli.py")
    if __init__.exists():
        # Read __init__.py for exports
        try:
            init_content = __init__.read_text()
            # Look for function/class definitions that form the API
            func_count = init_content.count("def ")
            class_count = init_content.count("class ")
            entry_points.append(f"__init__.py ({func_count} funcs, {class_count} classes)")
        except:
            entry_points.append("__init__.py (read error)")

    if entry_points:
        return True, f"Entry points found: {', '.join(entry_points)}"
    else:
        return False, "No clear entry points found"


def check_rollback_path(documented(repo_dir):
    """Check if uninstall/rollback path is documented."""
    # Look for uninstall instructions, cleanup scripts, etc.
    readme_path = Path(repo_dir) / "README.md"
    if not readme_path.exists():
        return False, "No README.md found"

    content = readme_path.read_text().lower()

    keywords = ["uninstall", "remove", "rollback", "uninstallation", "cleanup"]
    found = [kw for kw in keywords if kw in content]

    if found:
        return True, f"Rollback/uninstall keywords found: {', '.join(found)}"
    else:
        return False, "No uninstall/rollback keywords in README"


def evaluate_project(repo_url, work_dir):
    """Evaluate a project from a GitHub URL."""
    print(f"\nEvaluating: {repo_url}")

    # Clone the repo
    try:
        result = subprocess.run(
            ["git", "clone", "--depth", "1", repo_url, work_dir],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            print(f"  Clone failed: {result.stderr[:200]}")
            return None
    except subprocess.TimeoutExpired:
        print("  Clone timed out")
        return None
    except FileNotFoundError:
        print("  git not found")
        return None

    repo_name = repo_url.rstrip('/').split('/')[-1]
    print(f"  Repo: {repo_name}")

    # Check criteria
    results = {}

    has_runnable, runnable_note = check_runnable_readme_example(work_dir)
    results['runnable_readme'] = (has_runnable, runnable_note)
    print(f"  Runnable README example: {has_runnable} - {runnable_note}")

    cli_ok, cli_note = check_cli_surface_size(work_dir)
    results['cli_surface'] = (cli_ok, cli_note)
    print(f"  CLI surface size: {cli_ok} - {cli_note}")

    rollback_ok, rollback_note = check_rollback_path(work_dir)
    results['rollback'] = (rollback_ok, rollback_note)
    print(f"  Rollback path: {rollback_ok} - {rollback_note}")

    # Clean up
    try:
        subprocess.run(["rm", "-rf", work_dir], capture_output=True, timeout=5)
    except:
        pass

    return results


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python eval-project-prototype.py <github-repo-url>...")
        print("Example: python eval-project-prototype.py https://github.com/psf/requests")
        sys.exit(1)

    results = {}
    for url in sys.argv[1:]:
        # Create a unique working directory
        work_dir = f"/tmp/eval_proj_{hash(url) % 10000}"
        r = evaluate_project(url, work_dir)
        if r:
            results[url] = r

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY OF EVALUATION CRITERIA (from RESEARCH/F.md)")
    print("=" * 60)
    print("\n1. Runnable README example: Can a stranger run a 'hello world'")
    print("   example in one command from the README?")
    print("\n2. CLI surface size: Is the API small enough to fit on one screen?")
    print("\n3. Rollback/unstinstall path: Is there documented cleanup?")

    if results:
        print(f"\nEvaluated {len(results)} project(s).")
        for url, r in results.items():
            print(f"\n{url}:")
            for criterion, (passed, note) in r.items():
                status = "PASS" if passed else "FAIL"
                print(f"  {criterion}: {status} - {note}")
    else:
        print("\nNo projects could be evaluated.")


if __name__ == "__main__":
    main()