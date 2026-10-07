#!/usr/bin/env python3
"""Score every trial repository against the quarantined hand-written oracle.

Usage: score.py <fixture-root>

The oracle lives in <fixture-root>/oracle/<scenario>.index and is never present
in a trial directory, so a trial that reaches the right answer did so by
staging, not by reading the answer.
"""

import json
import os
import subprocess
import sys


def sh(args, cwd):
    p = subprocess.Popen(args, cwd=cwd, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out, err = p.communicate()
    return p.returncode, out.decode("utf-8", "replace"), err.decode("utf-8", "replace")


def read(path):
    with open(path) as fh:
        return fh.read()


def index_of(repo):
    rc, out, _ = sh(["git", "show", ":app.py"], repo)
    return out if rc == 0 else None


def score_trial(trial, oracle):
    got = index_of(trial)
    expected = read(oracle + ".index")
    head = sh(["git", "show", "HEAD:app.py"], trial)[1]
    if got is None or got == head:
        # `git show :app.py` succeeds with HEAD's content when the index is
        # untouched, so "staged nothing" must be separated from "staged the
        # wrong thing" or an unrun trial scores as a wrong answer.
        verdict = "nothing_staged"
    elif got == expected:
        verdict = "exact"
    else:
        verdict = "wrong"
    rc, unstaged, _ = sh(["git", "diff", "--no-color", "-U0"], trial)
    return {
        "trial": os.path.basename(trial),
        "verdict": verdict,
        "line": int(read(oracle + ".line").strip()),
        "unstaged_changes_remain": bool(unstaged.strip()),
        "extra_files_left_behind": sorted(
            f for f in os.listdir(trial)
            if f not in ("app.py", ".git", ".bin") and not f.startswith(".git")),
    }


def main():
    root = sys.argv[1]
    oracle_dir = os.path.join(root, "oracle")
    rows = []
    for name in sorted(os.listdir(root)):
        if not name.endswith("-trial"):
            continue
        scenario = name.rsplit("-trial", 1)[0]
        scenario = scenario.rsplit("-", 1)[0]
        oracle = os.path.join(oracle_dir, scenario)
        rows.append(score_trial(os.path.join(root, name), oracle))
    exact = sum(1 for r in rows if r["verdict"] == "exact")
    print(json.dumps({"trials": rows,
                      "exact": exact, "of": len(rows)}, indent=2))


if __name__ == "__main__":
    main()