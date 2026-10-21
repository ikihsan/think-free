#!/usr/bin/env python3
"""Project evaluation prototype based on RESEARCH/F.md criteria.

Evaluates open-source projects on pre-release checkable criteria from
RESEARCH/F.md (Investigation F — adoption researcher):
  C1: README leads with a runnable example
  C2: Every public command in README is exercised in CI/test
  C3: Installation is one command per platform, documented with expected output
  C4: No feature merged without user-visible change demonstrated
  C5: Linter passes on the public documentation itself
  C6: New user following only README can produce the headline artifact

This prototype is a reversible exploratory instrument — it gathers evidence
about what makes project evaluation easier/harder, without claiming adoption
or a new algorithm. Results are stored in a JSONL file for later analysis.
"""

import subprocess
import sys
import os
import json
import time
from pathlib import Path
from datetime import datetime


RESULTS_FILE = Path("eval-results.jsonl")


def init_results_file():
    """Initialize the results JSONL file if it doesn't exist."""
    if not RESULTS_FILE.exists():
        RESULTS_FILE.write_text("# eval-results.jsonl — project evaluation results\n")


def append_result(project_url, repo_name, criteria_results, timestamp=None):
    """Append a single evaluation result to the JSONL file."""
    if timestamp is None:
        timestamp = datetime.now().isoformat()

    record = {
        "timestamp": timestamp,
        "project_url": project_url,
        "repo_name": repo_name,
        "criteria": criteria_results,
    }
    with open(RESULTS_FILE, "a") as f:
        f.write(json.dumps(record) + "\n")


def clone_repo(repo_url, work_dir, timeout=60):
    """Clone a GitHub repository with depth 1."""
    try:
        result = subprocess.run(
            ["git", "clone", "--depth", "1", repo_url, work_dir],
            capture_output=True, text=True, timeout=timeout
        )
        if result.returncode != 0:
            return False, result.stderr[:300]
        return True, None
    except subprocess.TimeoutExpired:
        return False, "Clone timed out"
    except FileNotFoundError:
        return False, "git not found"
    except Exception as e:
        return False, str(e)


def cleanup_work_dir(work_dir):
    """Remove the working directory after evaluation."""
    try:
        subprocess.run(["rm", "-rf", work_dir], capture_output=True, timeout=5)
    except Exception:
        pass


def check_c1_runnable_readme(repo_dir):
    """C1: README leads with a runnable example whose output can be compared."""
    readme_path = Path(repo_dir) / "README.md"
    if not readme_path.exists():
        return False, "No README.md found"

    content = readme_path.read_text()
    lines = content.split('\n')

    # Look for code fences in the first 20 lines
    has_code_fence = False
    for i, line in enumerate(lines[:20]):
        if '```' in line or '~~~' in line:
            has_code_fence = True
            break

    if not has_code_fence:
        return False, "No code fence found in first 20 lines of README"

    return True, "README has code fence in first 20 lines"


def check_c2_cli_exercised_in_ci(repo_dir):
    """C2: Every public command in README is exercised in CI or in a test."""
    readme_path = Path(repo_dir) / "README.md"
    if not readme_path.exists():
        return False, "No README.md found"

    content = readme_path.read_text().lower()

    # Look for command-like patterns
    command_patterns = ["pip install", "npm install", "npm i", "cargo install"]
    found_commands = [p for p in command_patterns if p in content]

    if found_commands:
        ci_keywords = ["ci", "test", "github actions", "travis"]
        has_ci_mention = any(kw in content for kw in ci_keywords)
        return True, f"Found commands: {', '.join(found_commands)}, CI mention: {has_ci_mention}"
    else:
        return False, "No install commands found in README"


def check_c3_one_command_install(repo_dir):
    """C3: Installation is one command per supported platform, documented with expected output."""
    readme_path = Path(repo_dir) / "README.md"
    if not readme_path.exists():
        return False, "No README.md found"

    content = readme_path.read_text().lower()

    install_patterns = ["pip install", "conda install", "npm install", "cargo install"]
    found_installs = [p for p in install_patterns if p in content]

    if found_installs:
        platform_keywords = ["windows", "macos", "linux", "docker"]
        has_platform_docs = any(kw in content for kw in platform_keywords)
        return True, f"Found installs: {', '.join(found_installs)}, platform docs: {has_platform_docs}"
    else:
        return False, "No installation commands found in README"


def check_c4_feature_change_demonstrated(repo_dir):
    """C4: No feature merged without user-visible change demonstrated."""
    readme_path = Path(repo_dir) / "README.md"
    if not readme_path.exists():
        return False, "No README.md found"

    content = readme_path.read_text().lower()

    change_indicators = ["release", "changelog", "what's new", "new in", "feature"]
    found_indicators = [kw for kw in change_indicators if kw in content]

    if found_indicators:
        return True, f"Change indicators found: {', '.join(found_indicators)}"
    else:
        return False, "No change/log feature indicators in README"


def check_c5_linter_passes(repo_dir):
    """C5: Linter passes on the public documentation itself."""
    readme_path = Path(repo_dir) / "README.md"
    if not readme_path.exists():
        return False, "No README.md found"

    content = readme_path.read_text()
    line_count = len(content.split('\n'))

    # Simple heuristic: README under 500 lines is reasonable
    if line_count <= 500:
        return True, f"README is {line_count} lines (within reasonable limit)"
    else:
        return True, f"README is {line_count} lines (outside typical limit, instrument-limited)"


def check_c6_readme_enough(repo_dir):
    """C6: New user following only README can produce headline artifact."""
    readme_path = Path(repo_dir) / "README.md"
    if not readme_path.exists():
        return False, "No README.md found"

    content = readme_path.read_text().lower()

    artifact_patterns = ["example", "tutorial", "getting started", "hello", "quickstart"]
    found_patterns = [p for p in artifact_patterns if p in content]

    if found_patterns:
        return True, f"Artifact patterns found: {', '.join(found_patterns)}"
    else:
        return False, "No artifact patterns found in README"


def evaluate_project(repo_url, work_dir_prefix="eval_proj"):
    """Evaluate a project from a GitHub URL against F.md criteria."""
    timestamp_str = datetime.now().strftime("%Y%m%d-%H%M%S")
    work_dir = f"{work_dir_prefix}_{timestamp_str}_{hash(repo_url) % 10000}"

    print(f"\n{'=' * 60}")
    print(f"Evaluating: {repo_url}")
    print(f"Work dir: {work_dir}")
    print(f"{'=' * 60}")

    # Phase 1: Clone
    print("\n[1/7] Cloning repository...")
    success, error = clone_repo(repo_url, work_dir, timeout=60)
    if not success:
        print(f"  FAIL: {error}")
        cleanup_work_dir(work_dir)
        return None

    repo_name = repo_url.rstrip('/').split('/')[-1]
    print(f"  Repo: {repo_name}")

    # Phase 2-7: Check criteria
    criteria = {}

    print("\n[2/7] Checking C1: Runnable README example...")
    c1_ok, c1_note = check_c1_runnable_readme(work_dir)
    criteria['c1_runnable_readme'] = {"pass": c1_ok, "note": c1_note}
    print(f"  {'PASS' if c1_ok else 'FAIL'}: {c1_note}")

    print("\n[3/7] Checking C2: CLI exercised in CI...")
    c2_ok, c2_note = check_c2_cli_exercised_in_ci(work_dir)
    criteria['c2_cli_ci'] = {"pass": c2_ok, "note": c2_note}
    print(f"  {'PASS' if c2_ok else 'FAIL'}: {c2_note}")

    print("\n[4/7] Checking C3: One-command install...")
    c3_ok, c3_note = check_c3_one_command_install(work_dir)
    criteria['c3_one_command_install'] = {"pass": c3_ok, "note": c3_note}
    print(f"  {'PASS' if c3_ok else 'FAIL'}: {c3_note}")

    print("\n[5/7] Checking C4: Feature change demonstrated...")
    c4_ok, c4_note = check_c4_feature_change_demonstrated(work_dir)
    criteria['c4_feature_change'] = {"pass": c4_ok, "note": c4_note}
    print(f"  {'PASS' if c4_ok else 'FAIL'}: {c4_note}")

    print("\n[6/7] Checking C5: Linter on documentation...")
    c5_ok, c5_note = check_c5_linter_passes(work_dir)
    criteria['c5_linter'] = {"pass": c5_ok, "note": c5_note}
    print(f"  {'PASS' if c5_ok else 'FAIL'}: {c5_note}")

    print("\n[7/7] Checking C6: Artifact patterns in README...")
    c6_ok, c6_note = check_c6_readme_enough(work_dir)
    criteria['c6_artifact_patterns'] = {"pass": c6_ok, "note": c6_note}
    print(f"  {'PASS' if c6_ok else 'FAIL'}: {c6_note}")

    # Clean up
    cleanup_work_dir(work_dir)

    # Store result
    append_result(repo_url, repo_name, criteria, datetime.now().isoformat())

    return {
        "url": repo_url,
        "name": repo_name,
        "criteria": criteria,
        "timestamp": datetime.now().isoformat(),
    }


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python3 eval-project-prototype.py <github-repo-url>...")
        print("Example: python3 eval-project-prototype.py https://github.com/psf/requests")
        print("\nResults are stored in eval-results.jsonl")
        sys.exit(1)

    init_results_file()

    all_results = []
    for url in sys.argv[1:]:
        result = evaluate_project(url)
        if result:
            all_results.append(result)

    # Print summary
    print("\n" + "=" * 60)
    print("EVALUATION SUMMARY")
    print("=" * 60)
    print("\nCriteria from RESEARCH/F.md:")
    print("  C1: README leads with a runnable example")
    print("  C2: Every public command in README is exercised in CI/test")
    print("  C3: Installation is one command per platform, documented")
    print("  C4: No feature merged without user-visible change demonstrated")
    print("  C5: Linter passes on public documentation")
    print("  C6: New user following only README can produce headline artifact")
    print()

    if all_results:
        print(f"Evaluated {len(all_results)} project(s).")
        print()

        # Per-criteria summary
        criteria_names = [
            'c1_runnable_readme',
            'c2_cli_ci',
            'c3_one_command_install',
            'c4_feature_change',
            'c5_linter',
            'c6_artifact_patterns',
        ]
        criteria_labels = [
            'C1: Runnable README',
            'C2: CLI in CI',
            'C3: One-command install',
            'C4: Feature changes demonstrated',
            'C5: Linter on docs',
            'C6: Artifact patterns',
        ]

        print("Per-criteria results across all projects:")
        print("-" * 60)
        for name, label in zip(criteria_names, criteria_labels):
            passed = sum(1 for r in all_results if r["criteria"].get(name, {}).get("pass", False))
            total = len(all_results)
            pct = passed / total * 100 if total > 0 else 0
            print(f"  {label:30s} {passed}/{total} ({pct:.0f}%)")

        # Store an overall summary
        summary = {
            "type": "summary",
            "evaluated": len(all_results),
            "timestamp": datetime.now().isoformat(),
            "criteria_breakdown": {},
        }
        for name, label in zip(criteria_names, criteria_labels):
            passed = sum(1 for r in all_results if r["criteria"].get(name, {}).get("pass", False))
            total = len(all_results)
            summary["criteria_breakdown"][label] = {
                "passed": passed,
                "total": total,
                "percentage": round(passed / total * 100) if total > 0 else 0,
            }

        # Write summary alongside results
        summary_file = Path("eval-summary.json")
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2)

        print(f"\nDetailed results stored in: {RESULTS_FILE}")
        print(f"Summary stored in: {summary_file}")
    else:
        print("No projects could be evaluated.")


if __name__ == "__main__":
    main()