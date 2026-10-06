#!/usr/bin/env python3
"""E037: is selecting a change by line number reachable today, and what does it cost?

Three routes are compared on the same concrete cases, each asked for the same
thing: stage the change on a given working-tree line, and no other.

  stg      `stg stage f:N` -- the line number and nothing else.
  pty      `git add -p` driven through a real terminal by a program that reads
           git's own display and decides what to answer. This is the strongest
           version of the incumbent: not a naive key dump, but a driver written
           specifically to overcome everything that makes the interface awkward.
  naive    `git add -p` with keys chosen once, at git's default context, and
           replayed. This is what a script or an agent writes on the first try.

`driver.py` holds the pty driver on its own so its size can be counted: the
practical difference between the routes is not whether the incumbent can be
driven at all, it is how much machinery the caller has to write first.

One JSON object per line goes to stdout. Nothing here decides whether the
candidate is any good; it only records what each route did.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
STG = os.path.join(ROOT, "stage-lines", "stg")
DRIVER = os.path.join(HERE, "driver.py")

# name, base, edited, the working-tree line to stage, human description
CASES = [
    ("modify-one-of-three", "one\ntwo\nthree\nfour\nfive\nsix\nseven\n",
     "ONE\ntwo\nthree\nFOUR\nfive\nSIX\nseven\n", 4, "edit line 4 of three edits"),
    ("deletion-among-edits", "a\nb\nc\nd\ne\nf\ng\nh\n",
     "a\nb\nd\ne\nF\ng\nh\n", 3, "delete line 3, keep the edit that follows it"),
    ("insertion-among-edits", "a\nb\nc\nd\ne\nf\ng\nh\n",
     "a\nb\nc\nd\nNEW\ne\nf\ng\nh\n", 5, "insert line 5 of two edits"),
    ("adjacent-edits", "a\nb\nc\nd\ne\n",
     "A\nB\nc\nD\ne\n", 2, "take the second of two adjacent edits"),
    ("append-at-eof", "a\nb\nc\n", "a\nb\nc\nd\ne\n", 4, "append two lines at eof"),
    ("adjacent-inserts", "a\nb\nc\n", "a\nb\nc\nX\nY\n", 4, "take one of two new lines"),
]


def sh(args, cwd):
    return subprocess.run(args, cwd=cwd, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, universal_newlines=True)


def make_repo(base, edited, context=None):
    d = tempfile.mkdtemp(prefix="e037-")
    sh(["git", "init", "-q", "."], d)
    sh(["git", "config", "user.email", "t@example.com"], d)
    sh(["git", "config", "user.name", "t"], d)
    if context:
        sh(["git", "config", "diff.context", context], d)
    with open(os.path.join(d, "f"), "w") as fh:
        fh.write(base)
    sh(["git", "add", "f"], d)
    sh(["git", "commit", "-qm", "base"], d)
    with open(os.path.join(d, "f"), "w") as fh:
        fh.write(edited)
    return d


def staged_anchors(d):
    """Working-tree line numbers of the changes now sitting in the index."""
    out = sh(["git", "diff", "--cached", "-U0", "--no-color"], d).stdout
    got = []
    for line in out.split("\n"):
        m = re.match(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", line)
        if not m:
            continue
        start = int(m.group(1))
        count = int(m.group(2) or 1)
        got.append(start if count else start + 1)
    return sorted(got)


def run_stg(base, edited, line, context=None):
    d = make_repo(base, edited, context)
    try:
        p = sh([sys.executable, STG, "stage", "f:%d" % line], d)
        return {"staged": staged_anchors(d), "rc": p.returncode,
                "stderr": p.stderr.strip()}
    finally:
        shutil.rmtree(d, ignore_errors=True)


def run_pty_driver(base, edited, line, context=None):
    d = make_repo(base, edited, context)
    try:
        p = sh([sys.executable, DRIVER, str(line)], d)
        rec = {"staged": staged_anchors(d), "rc": p.returncode}
        if p.returncode != 0:
            rec["stderr"] = p.stderr.strip()[:200]
        try:
            rec["driver"] = json.loads(p.stdout.strip().split("\n")[-1])
        except (ValueError, IndexError):
            rec["driver"] = {"note": "driver printed nothing parseable"}
        return rec
    finally:
        shutil.rmtree(d, ignore_errors=True)


def naive_keys(base, edited, line):
    """What a first-try script writes: count the hunks at U0, then answer them.

    This is not a strawman. It is the obvious reading of git's output, and it is
    what any caller writes before discovering that `git add -p` does not display
    hunks at U0 at all. The keys are derived once, at git's default context, and
    replayed unchanged everywhere else -- which is the only way a script can use
    them.
    """
    d = make_repo(base, edited)
    try:
        out = sh(["git", "diff", "-U0", "--no-color"], d).stdout
        hunks = [l for l in out.split("\n") if l.startswith("@@")]
        wanted = None
        for i, h in enumerate(hunks):
            m = re.match(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", h)
            start = int(m.group(3))
            count = int(m.group(4) or 1)
            anchor = start if count else start + 1
            if anchor == line:
                wanted = i
                break
        keys = "".join(("y" if i == wanted else "n") + "\n"
                       for i in range(len(hunks)))
        return keys, len(hunks), wanted
    finally:
        shutil.rmtree(d, ignore_errors=True)


def run_naive(base, edited, line, context=None):
    keys, n, wanted = naive_keys(base, edited, line)
    d = make_repo(base, edited, context)
    try:
        p = subprocess.run(["git", "add", "-p", "f"], cwd=d, input=keys,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           universal_newlines=True)
        return {"staged": staged_anchors(d),
                "keys": keys.strip().replace("\n", ","),
                "hunks_assumed": n, "wanted_index": wanted,
                "rc": p.returncode}
    finally:
        shutil.rmtree(d, ignore_errors=True)


def driver_size():
    with open(DRIVER) as fh:
        body = [l for l in fh.read().split("\n")
                if l.strip() and not l.strip().startswith("#")]
    return {"driver_code_lines": len(body)}


def main():
    out = dict(driver_size())
    print(json.dumps({"meta": out}, sort_keys=True))
    for name, base, edited, line, desc in CASES:
        rec = {"case": name, "ask": desc, "line": line}
        rec["stg"] = run_stg(base, edited, line)
        rec["pty_driver"] = run_pty_driver(base, edited, line)
        rec["naive_default"] = run_naive(base, edited, line)
        for ctx in ("1", "3"):
            rec["stg_ctx%s" % ctx] = run_stg(base, edited, line, ctx)
            rec["pty_ctx%s" % ctx] = run_pty_driver(base, edited, line, ctx)
            rec["naive_ctx%s" % ctx] = run_naive(base, edited, line, ctx)

        print(json.dumps(rec, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
