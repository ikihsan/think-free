#!/usr/bin/env python3
"""Does the oracle actually discriminate? Check it against four routes.

Run from a scratch copy of each fixture, BEFORE any agent is dispatched:
a scorer that cannot tell right from wrong cannot report an agent's success.

Routes:
  stage-all      git add app.py                        (expect `wrong`)
  stage-none     do nothing                            (expect `nothing_staged`)
  stg            stage-lines/stg stage app.py:LINE     (expect `exact`)
  nodiff-patch   align HEAD vs worktree with difflib -- NO `git diff` -- then
                 hand-emit a -U0 hunk for the requested line only and
                 `git apply --cached --unidiff-zero`   (expect `exact`)

The fourth route is the one the `nostg` arm's agents are expected to need:
it proves each fixture is solvable from file contents plus a line coordinate,
without diff output, so an agent failure means the agent, not the fixture.

Usage: check_oracle.py <experiment-root>
"""

import difflib
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STG = os.path.join(os.path.dirname(os.path.dirname(HERE)), "stage-lines", "stg")


def sh(args, cwd, stdin=None):
    p = subprocess.Popen(args, cwd=cwd,
                         stdin=subprocess.PIPE if stdin is not None else None,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(stdin.encode() if stdin is not None else None)
    return p.returncode, out.decode("utf-8", "replace"), err.decode("utf-8", "replace")


def read(path):
    with open(path) as fh:
        return fh.read()


def index(repo):
    rc, out, _ = sh(["git", "show", ":app.py"], repo)
    return out if rc == 0 else None


def verdict(repo, expected):
    got = index(repo)
    head = sh(["git", "show", "HEAD:app.py"], repo)[1]
    if got is None or got == head:
        return "nothing_staged"
    return "exact" if got == expected else "wrong"


def nodiff_patch(repo, line):
    """Stage the change on new-file `line` using only file contents."""
    head = sh(["git", "show", "HEAD:app.py"], repo)[1].splitlines(True)
    work = read(os.path.join(repo, "app.py")).splitlines(True)
    sm = difflib.SequenceMatcher(None, head, work, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        lo, hi = j1 + 1, max(j2, j1 + 1)          # new-file span, 1-based
        if not (lo <= line <= hi):
            continue
        if tag == "insert":
            # Stage only the requested line of the insertion run, not the
            # whole run: that is the point of the scenario.
            old_span = "%d,0" % i1
            new_span = str(line)
            body = ["+" + work[line - 1]]
        elif tag == "delete":
            old_span = str(i1 + 1) if i2 - i1 == 1 else "%d,%d" % (i1 + 1, i2 - i1)
            new_span = "%d,0" % j1
            body = ["-" + l for l in head[i1:i2]]
        else:  # replace: stage only the paired line, not the whole run
            k = line - 1 - j1
            old_span = str(i1 + 1 + k)
            new_span = str(line)
            body = ["-" + head[i1 + k], "+" + work[line - 1]]
        patch = ("diff --git a/app.py b/app.py\n"
                 "--- a/app.py\n+++ b/app.py\n"
                 "@@ -%s +%s @@\n" % (old_span, new_span)
                 + "".join(body))
        return sh(["git", "apply", "--cached", "--unidiff-zero", "-"],
                  repo, stdin=patch)
    return 1, "", "no opcode covers line %d" % line


def main():
    root = sys.argv[1]
    fixtures = os.path.join(root, "oracle")
    rows = []
    for name in sorted(os.listdir(fixtures)):
        if not name.endswith(".line"):
            continue
        scenario = name[:-len(".line")]
        line = int(read(os.path.join(fixtures, name)).strip())
        expected = read(os.path.join(fixtures, scenario + ".index"))
        src = os.path.join(root, "fixtures", scenario + "-nostg")
        for route in ("stage-all", "stage-none", "stg", "nodiff-patch"):
            work = src + "-probe-" + route
            if os.path.exists(work):
                shutil.rmtree(work)
            shutil.copytree(src, work)
            rc = 0
            if route == "stage-all":
                rc, _, _ = sh(["git", "add", "app.py"], work)
            elif route == "stg":
                rc, _, _ = sh([sys.executable, STG, "stage",
                               "app.py:%d" % line], work)
            elif route == "nodiff-patch":
                rc = nodiff_patch(work, line)[0]
            rows.append((scenario, route, verdict(work, expected), rc))
            shutil.rmtree(work)
    print("%-26s %-12s %-16s %s" % ("scenario", "route", "verdict", "exit"))
    for scenario, route, v, rc in rows:
        print("%-26s %-12s %-16s %d" % (scenario, route, v, rc))


if __name__ == "__main__":
    main()
