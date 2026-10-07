#!/usr/bin/env python3
"""Score every trial repository against the quarantined hand-written oracle,
and summarise the shim log: what git calls happened, whether `git diff` was
attempted and refused, and whether the `stg` arm's tool was genuinely
exercised (D074: an arm that did not touch the tool is not a treatment arm).

Usage: score.py <experiment-root>

The oracle lives in <experiment-root>/oracle/<scenario>.index and is never
present in a trial directory, so a trial that reaches the right answer did so
by staging, not by reading the answer.
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


def shim_stats(logfile):
    if not os.path.exists(logfile):
        return {"calls": 0, "diff_refused": 0, "failures": 0,
                "stg_internal_calls": 0}
    calls = refused = failures = internal = 0
    for line in read(logfile).splitlines():
        parts = line.split("\t")
        if len(parts) >= 2 and parts[1] == "REFUSED":
            refused += 1
        elif len(parts) >= 2 and parts[1].startswith("rc="):
            if parts[1] != "rc=0":
                failures += 1
        elif len(parts) >= 4:
            calls += 1
            if parts[2] != "-":
                internal += 1
    return {"calls": calls, "diff_refused": refused, "failures": failures,
            "stg_internal_calls": internal}


def score_trial(trial, oracle, logfile):
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
    name = os.path.basename(trial)
    row = {
        "trial": name,
        "verdict": verdict,
        "line": int(read(oracle + ".line").strip()),
        "unstaged_changes_remain": bool(unstaged.strip()),
        "extra_files_left_behind": sorted(
            f for f in os.listdir(trial) if f not in ("app.py", ".git")),
    }
    row.update(shim_stats(logfile))
    return row


def main():
    root = sys.argv[1]
    trials = os.path.join(root, "trials")
    oracle_dir = os.path.join(root, "oracle")
    rows = []
    for name in sorted(os.listdir(trials)):
        if not name.endswith("-trial"):
            continue
        stem = name[:-len("-trial")]                 # <scenario>-<arm>
        scenario = stem.rsplit("-", 1)[0]
        oracle = os.path.join(oracle_dir, scenario)
        logfile = os.path.join(oracle_dir, "shim-%s.log" % stem)
        rows.append(score_trial(os.path.join(trials, name), oracle, logfile))
    exact = sum(1 for r in rows if r["verdict"] == "exact")
    print(json.dumps({"trials": rows,
                      "exact": exact, "of": len(rows)}, indent=2))


if __name__ == "__main__":
    main()
