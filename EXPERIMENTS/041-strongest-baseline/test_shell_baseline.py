#!/usr/bin/env python3
"""Test the strongest shell baseline against E040 cases."""
import tempfile
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shell_baseline import ShellBaseline


def make_repo(base, edited):
    d = tempfile.mkdtemp(prefix="test-")
    subprocess.run(["git", "init", "-q", "."], cwd=d, check=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=d, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=d, check=True)
    with open(os.path.join(d, "f"), "w") as fh:
        fh.write(base)
    subprocess.run(["git", "add", "f"], cwd=d, check=True)
    subprocess.run(["git", "commit", "-qm", "base"], cwd=d, check=True)
    with open(os.path.join(d, "f"), "w") as fh:
        fh.write(edited)
    return d


def staged_blob(root):
    p = subprocess.run(["git", "show", ":f"], cwd=root, capture_output=True)
    return p.stdout.decode() if p.returncode == 0 else None


# E040's 5 cases
CASES = [
    ("adjacent-modifications", "a\nb\nc\nd\n", "A\nB\nc\nd\n", 2, "a\nB\nc\nd\n"),
    ("two-line-insertion", "a\nd\n", "a\nx\ny\nd\n", 2, "a\nx\nd\n"),
    ("single-line-insertion", "a\nc\n", "a\nb\nc\n", 2, "a\nb\nc\n"),
    ("tail-modification", "a\nb\nc\n", "a\nb\nC\n", 3, "a\nb\nC\n"),
    ("unchanged-line", "a\nb\n", "A\nb\n", 2, "a\nb\n"),  # unstageable
]


def main():
    baseline = ShellBaseline()
    all_pass = True
    
    for name, base, work, line, expected in CASES:
        repo = make_repo(base, work)
        rc, out, err, staged = baseline.stage(repo, "f", line)
        exact = (staged == expected)
        honest = (rc == 2 and not exact and staged in (base, None)) or exact
        
        status = "PASS" if (exact and honest) else "FAIL"
        if status == "FAIL":
            all_pass = False
        
        print(f"{name}: exact={exact}, honest={honest}, rc={rc}, staged={repr(staged)}")
        print(f"  expected={repr(expected)}")
        if not exact:
            print(f"  DIFF: got {repr(staged)}, expected {repr(expected)}")
    
    print(f"\nAll cases pass: {all_pass}")
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())