#!/usr/bin/env python3
"""Prototype: Analyze this repository's git history using stg's line-level parsing.

Uses stagelib.parse() to examine the repository's git log and diff patterns,
producing fresh observations about change frequency, types, and patterns.
This is a reversible exploratory prototype: evidence-gathering, not product validation.

The stagelib mechanism (originally for line-level git staging) is here applied
to the repository's own change history as a fresh observation method.
"""

import os
import sys
import subprocess
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stagelib import parse


def run_git(*args):
    """Run a git command and return (stdout, returncode)."""
    result = subprocess.run(
        ["git", *args],
        capture_output=True, text=True, cwd="/home/ubuntu/think-free"
    )
    return result.stdout.strip(), result.returncode


def ensure_new_nlines(fp):
    """Set fp.new_nlines if not already set, by counting lines in the file."""
    if fp.new_nlines is None:
        try:
            with open(fp.path, "rb") as fh:
                content = fh.read().decode("utf-8", "replace")
            fp.new_nlines = content.count("\n") + (1 if content and not content.endswith(b"\n") else 0) if content else 0
        except (IOError, OSError):
            fp.new_nlines = 0


def classify_change_type(c):
    """Classify a change from a parsed Change object."""
    added = sum(1 for l in c.body if l.startswith("+"))
    removed = sum(1 for l in c.body if l.startswith("-"))
    if removed and not added:
        return "delete"
    if added and not removed:
        return "add"
    if added and removed:
        return "modify"
    return "unknown"


def analyze_file_changes(change_dict, path):
    """Analyze changes for a single file using stg's parsed structure."""
    if path not in change_dict:
        return None
    fp = change_dict[path]
    if fp.binary:
        return {"path": path, "binary": True, "changes": 0}

    # Ensure new_nlines is set for anchor computation
    ensure_new_nlines(fp)

    anchors = fp.anchors()

    kind_counts = Counter()
    total_lines_changed = 0
    total_changes = 0
    line_range = {"min": None, "max": None}

    for c in fp.changes:
        kind = classify_change_type(c)
        kind_counts[kind] += 1
        total_changes += 1
        total_lines_changed += max(c.new_lines, 1) + max(c.old_lines, 1)
        a = anchors.get(id(c), c.new_start)
        if line_range["min"] is None or a < line_range["min"]:
            line_range["min"] = a
        if line_range["max"] is None or a > line_range["max"]:
            line_range["max"] = a

    return {
        "path": path,
        "binary": False,
        "changes": total_changes,
        "kind_counts": dict(kind_counts),
        "total_lines_changed": total_lines_changed,
        "line_range": line_range,
    }


def main():
    print("=" * 70)
    print("Repository git history analysis using stg's line-level parsing")
    print("=" * 70)

    # Get the last 20 commits' diffs
    log_stdout, rc = run_git("log", "--format=%H", "-n", "20")
    commit_hashes = [h for h in log_stdout.split("\n") if h]

    print(f"\nAnalyzing last {len(commit_hashes)} commits...")
    print()

    overall_stats = Counter()
    file_summaries = []

    for i, commit in enumerate(commit_hashes):
        if not commit:
            continue

        # Get the diff for this commit (full patch)
        diff_stdout, rc = run_git("diff-tree", "-p", "--no-commit-id", commit)

        if rc != 0 or not diff_stdout:
            print(f"  Commit {i}: could not retrieve diff (rc={rc})")
            continue

        # Parse the diff using stg's mechanism
        try:
            changes = parse(diff_stdout)
        except Exception as e:
            print(f"  Commit {i}: parse error: {e}")
            continue

        # Analyze each file's changes
        for path, fp in sorted(changes.items()):
            result = analyze_file_changes(changes, path)
            if result is None:
                continue

            # Overall stats
            overall_stats["total_files"] += 1
            overall_stats["total_changes"] += result["changes"]
            for kind, count in result["kind_counts"].items():
                overall_stats[f"_{kind}s"] += count
            overall_stats["_total_lines"] += result["total_lines_changed"]

            # File-level summary (collect for printing later)
            if result["changes"] > 0:
                kind_labels = []
                for k in ["add", "modify", "delete"]:
                    if result["kind_counts"].get(k, 0) > 0:
                        kind_labels.append(f"{k}:{result['kind_counts'][k]}")
                summary = (
                    f"  Commit {i}: {path}: {result['changes']} change(s), "
                    f"{', '.join(kind_labels) if kind_labels else 'unknown type'}, "
                    f"{result['total_lines_changed']} lines"
                )
                file_summaries.append(summary)

    # Print overall statistics
    print("\n" + "=" * 70)
    print("Overall statistics (last 20 commits):")
    print("=" * 70)
    print(f"  Total files changed: {overall_stats.get('total_files', 0)}")
    print(f"  Total changes: {overall_stats.get('total_changes', 0)}")
    print(f"  Total lines changed: {overall_stats.get('_total_lines', 0)}")
    print(f"  Additions: {overall_stats.get('_adds', 0)}")
    print(f"  Modifications: {overall_stats.get('_modifies', 0)}")
    print(f"  Deletions: {overall_stats.get('_deletes', 0)}")

    # Dominant change type
    for kind in ["add", "modify", "delete"]:
        count = overall_stats.get(f"_{kind}s", 0)
        total = overall_stats.get('total_changes', 1)
        pct = 100 * count / total if total > 0 else 0
        print(f"  {kind.capitalize()}: {count} ({pct:.1f}%)")

    # Per-file details
    print("\n  Per-file details:")
    for summary in file_summaries[:15]:
        print(summary)

    print("\n" + "=" * 70)
    print("End of analysis")
    print("=" * 70)


if __name__ == "__main__":
    main()