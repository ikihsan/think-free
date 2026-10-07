#!/usr/bin/env python3
"""Prototype: Demonstrate stg's line-level staging in a non-interactive workflow.

This script uses stg's parsing mechanism (stagelib.py) to identify individual
line-level changes in a file and stage them by line number without requiring
a TTY - the key advantage over `git add -p`.

It is a reversible exploratory prototype: the script itself can be deleted
without affecting the stg repository or its library code. No product claims
are made; this is evidence-gathering about workflow integration.
"""

import os
import sys
import subprocess

# Add the stage-lines directory to the path so we can import stagelib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from stagelib import parse
from stg_git import annotate, apply_patch, misplaced_insertions, line_count, ends_with_newline


def run_git(*args, cwd=None):
    """Run a git command and return its stdout."""
    result = subprocess.run(
        ["git", *args],
        capture_output=True, text=True, cwd=cwd or os.getcwd()
    )
    return result.stdout.strip(), result.returncode


def get_unstaged_changes(repo_path):
    """Get unstaged changes using git diff -U0, parsed by stg."""
    stdout, rc = run_git("diff", "-U0", "--", ".", cwd=repo_path)
    if rc != 0:
        print(f"git diff failed (rc={rc})")
        return {}
    return parse(stdout)


def list_stageable_changes(change_dict):
    """List all stageable changes with their line numbers and previews."""
    rows = []
    for path, fp in sorted(change_dict.items()):
        if fp.binary:
            rows.append((path, "binary", []))
            continue
        anchors = fp.anchors()
        for c in fp.changes:
            a = anchors.get(id(c), c.new_start)
            last = a + max(c.new_lines, 1) - 1
            span = str(a) if last <= a else f"{a}-{last}"
            # Get preview text (strip the leading +/-
            try:
                preview_txt = c.preview().lstrip("+-")
            except Exception:
                preview_txt = ""
            rows.append((path, span, c.kind, preview_txt, c.new_start, c.new_lines))
    return rows


def stage_by_line_numbers(change_dict, line_specs, repo_path):
    """Stage changes matching the given line number specifications.

    line_specs: list of "path:line" or "path:line1-line2" strings
    """
    # First, annotate the file patches with line counts
    annotate(repo_path, change_dict)

    # Build a mapping from path to FilePatch for quick lookup
    fp_by_path = {path: fp for path, fp in change_dict.items()}

    selected = []
    for spec in line_specs:
        # Parse spec: "path:line" or "path:line1-line2"
        if ":" not in spec:
            print(f"  Skipping invalid spec: {spec}")
            continue

        path_part, _, rng = spec.rpartition(":")
        path = path_part.strip()

        # Handle the range
        if "-" in rng:
            parts = rng.split("-")
            if len(parts) == 2:
                lo, hi = int(parts[0]), int(parts[1])
            else:
                lo = hi = int(parts[0])
        else:
            lo = hi = int(rng)

        fp = fp_by_path.get(path)
        if fp is None:
            print(f"  No change in {path}")
            continue

        if fp.binary:
            print(f"  {path} is binary - skipping")
            continue

        if lo is None:
            # Stage the whole file
            picked = list(fp.changes)
        else:
            if hi > max(fp.new_nlines, 1):
                print(f"  {path} has {fp.new_nlines} line(s); you asked for {hi}")
                continue
            picked = fp.select(lo, hi)

        if not picked:
            print(f"  No change matches {spec}")
            continue

        # Check for misplaced insertions
        bad = misplaced_insertions(fp, repo_path, picked)
        if bad:
            print(f"  WARNING: no newline at end of file, line {bad[0].new_start} "
                  f"is inserted past its last line; git would glue the two together")

        selected.append((fp, picked))

    # Apply patches per file - one patch per file as git apply wants
    by_path = {}
    for fp, picked in selected:
        by_path.setdefault(fp.path, (fp, []))[1].extend(picked)

    staged_paths = []
    for path in sorted(by_path):
        fp, picked = by_path[path]
        render_text = fp.render(picked)
        apply_patch(repo_path, render_text)
        for c in picked:
            a = fp.anchor_of(c)
            print(f"  staged {path}:{a}")
        staged_paths.append(path)

    return staged_paths


def main():
    repo_path = os.getcwd()

    # Verify we're in a git repo
    stdout, rc = run_git("rev-parse", "--is-inside-work-tree")
    if rc != 0:
        print("Error: Not inside a git work tree.")
        sys.exit(1)

    print(f"Repository: {repo_path}")
    print("=" * 60)

    # Get unstaged changes
    changes = get_unstaged_changes(repo_path)

    if not changes:
        print("No unstaged changes found. Nothing to stage.")
        sys.exit(0)

    print("Unstaged changes:")
    print("-" * 40)

    rows = list_stageable_changes(changes)
    if not rows:
        print("No stageable changes found.")
        sys.exit(0)

    for path, span, kind, preview_txt, new_start, new_lines in rows:
        kind_marker = "del" if kind == "delete" else kind[0].upper()
        print(f"  {path}:{span} [{kind_marker}] {preview_txt}")

    print()
    print("Example line specs to stage:")
    print("  stg stage file1.txt:42          # stage change on line 42")
    print("  stg stage file1.txt:42-51       # stage lines 42 through 51")
    print("  stg stage file1.txt:42,file2.txt:8  # stage multiple specs")
    print()

    # For demonstration, stage a few specific lines
    demo_specs = []

    if len(rows) > 0:
        # Demo: stage the first change's anchor line of the first file
        first_path = rows[0][0]
        # Extract line number from span (before any dash)
        first_span = rows[0][1]
        if "-" in first_span:
            lo = int(first_span.split("-")[0])
        else:
            lo = int(first_span)
        demo_specs = [f"{first_path}:{lo}"]

    if not demo_specs:
        print("No line specs provided. Exiting.")
        sys.exit(0)

    print(f"Staging with specs: {demo_specs}")
    print("-" * 40)

    try:
        staged_paths = stage_by_line_numbers(changes, demo_specs, repo_path)
        print()
        print("Staging complete.")
        print(f"Staged paths: {staged_paths}")

        # Verify: show what git status says
        stdout, rc = run_git("status", "--porcelain", cwd=repo_path)
        if stdout:
            print(f"\ngit status --porcelain:\n{stdout}")
        else:
            print("\nNo status changes (all clean).")

        # Show the git diff --cached to confirm
        stdout, rc = run_git("diff", "--cached", "--unidiff-zero", cwd=repo_path)
        if stdout:
            print(f"\ngit diff --cached --unidiff-zero:\n{stdout}")

    except Exception as e:
        print(f"\nError during staging: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()