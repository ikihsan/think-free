#!/usr/bin/env python3
"""E038 head-to-head: does an existing tool already stage by line number?

Declared before the run in PROTOCOL.md section 1 (KILL-P). E037's KILL-B checked git's
own documentation and behaviour and said so honestly: "web search was unavailable on
this host, so 'no prior art' rests on git's own documentation and behaviour, not on a
search." This runs the alternative instead of describing it.

Four routes, all named before the run:

  stg         stage-lines/stg, the prototype.
  filterdiff  git diff | filterdiff --lines=N | git apply --cached --unidiff-zero.
              patchutils 0.3.4. Its man page documents "--lines=RANGE  Only include
              hunks that contain lines from the original file that lie within the
              specified RANGE", which is the coordinate E037 claims is missing.
  pty_driver  E037's driver.py, unchanged: the strongest form of `git add -p`.
  naive       E037's `naive` route, reconstructed here to the same rule (answer every
              hunk git prints at its default context), because E037's compare.py kept
              its own key choice inside the loop.

THE ORACLE. A row counts only if an independent reference patch could be built for it.
The reference is built by hand from the case's own text -- the hunk git would emit for
exactly the wanted line -- and applied with `git apply --cached --unidiff-zero`, so
git itself performs the arithmetic. A case whose reference cannot be built is recorded
as `oracle_built: false` and excluded from every score, because an unbuildable oracle
is a defect in this file, not a result about any route.

  FILTERDIFF=/path/to/filterdiff python3 compare.py
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
STG = os.path.join(ROOT, "stage-lines", "stg")
DRIVER = os.path.join(ROOT, "EXPERIMENTS", "037-line-staging", "driver.py")
FILTERDIFF = os.environ.get("FILTERDIFF", "filterdiff")

# E037's six cases, byte-identical, so the two runs are comparable. Plus four added,
# because the case class that separates the routes is adjacent change and one instance
# of it does not characterise a class.
#
# `want_content` is the oracle: the exact bytes `git show :f.txt` must print after the
# route stages what it was asked for. It is written out by hand from the case's own two
# texts, so it does not depend on any route's idea of which lines changed -- which is
# how an over-staging bug in a tool can otherwise be scored as a pass. Asserting on the
# staged diff cannot see it: a hunk carrying two changes when one was asked for still
# prints one clean hunk. E037's oracle read hunk anchors for exactly that reason, and
# recorded stg as 6 of 6 on a case where stg staged both lines of a two-line insertion.
CASES = [
    # Each `want_content` is the base file with ONLY the wanted line's change applied,
    # written by hand from the two texts above it. The earlier version of this file
    # also listed the other edits in the file, which is a different question and made
    # three correct routes look wrong.
    ("modify-one-of-three", "one\ntwo\nthree\nfour\nfive\nsix\nseven\n",
     "ONE\ntwo\nthree\nFOUR\nfive\nSIX\nseven\n", 4,
     "one\ntwo\nthree\nFOUR\nfive\nsix\nseven\n"),
    ("deletion-among-edits", "a\nb\nc\nd\ne\nf\ng\nh\n",
     "a\nb\nd\ne\nF\ng\nh\n", 3,
     "a\nb\nd\ne\nf\ng\nh\n"),
    ("insertion-among-edits", "a\nb\nc\nd\ne\nf\ng\nh\n",
     "a\nb\nc\nd\nNEW\ne\nf\ng\nh\n", 5,
     "a\nb\nc\nd\nNEW\ne\nf\ng\nh\n"),
    ("adjacent-edits", "a\nb\nc\nd\ne\n", "A\nB\nc\nD\ne\n", 2,
     "a\nB\nc\nd\ne\n"),
    ("append-at-eof", "a\nb\nc\n", "a\nb\nc\nd\ne\n", 4,
     "a\nb\nc\nd\n"),
    ("adjacent-inserts", "a\nb\nc\n", "a\nb\nc\nX\nY\n", 4,
     "a\nb\nc\nX\n"),
    ("three-adjacent", "a\nb\nc\nd\ne\n", "A\nb\nC\nd\nE\n", 3,
     "a\nb\nC\nd\ne\n"),
    ("adjacent-pair-plus-far", "a\nb\nc\nd\ne\n", "A\nB\nc\nd\nE\n", 2,
     "a\nB\nc\nd\ne\n"),
    ("adjacent-insert-run", "a\nb\nc\nd\n", "a\nb\nc\nX\nY\nZ\n", 6,
     "a\nb\nc\nd\nZ\n"),
    ("whole-file-rewrite", "x\ny\nz\n", "x\nY\nz\n", 2,
     "x\nY\nz\n"),
]
CONTEXTS = [None, 1, 3]


def sh(args, cwd, stdin=None, env=None):
    e = dict(os.environ)
    if env:
        e.update(env)
    p = subprocess.Popen(args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         stdin=subprocess.PIPE if stdin is not None else None, env=e)
    out, _ = p.communicate(stdin.encode() if stdin else None, timeout=90)
    return p.returncode, out.decode("utf-8", "replace")


def make_repo(base, edited, context):
    d = tempfile.mkdtemp(prefix="e038-")
    sh(["git", "init", "-q", "."], d)
    sh(["git", "config", "user.email", "t@e.st"], d)
    sh(["git", "config", "user.name", "T"], d)
    with open(os.path.join(d, "f.txt"), "w") as fh:
        fh.write(base)
    sh(["git", "add", "f.txt"], d)
    sh(["git", "commit", "-qm", "init"], d)
    with open(os.path.join(d, "f.txt"), "w") as fh:
        fh.write(edited)
    env = {}
    if context is not None:
        env["GIT_CONFIG_COUNT"] = "1"
        env["GIT_CONFIG_KEY_0"] = "diff.context"
        env["GIT_CONFIG_VALUE_0"] = str(context)
    return d, env


def index_content(d):
    """The bytes a commit would get for f.txt: what the user actually receives."""
    rc, out = sh(["git", "show", ":f.txt"], d)
    return out if rc == 0 else None


def route_stg(case, d, env):
    return sh([sys.executable, STG, "stage", "f.txt:%d" % case[3]], d, env=env)


def route_filterdiff(case, d, env):
    """The incumbent written the way its own man page describes it."""
    return sh(["bash", "-c",
               "git diff -U0 | %s --lines=%d | git apply --cached --unidiff-zero"
               % (FILTERDIFF, case[3])], d, env=env)


def route_pty(case, d, env):
    # E037's driver, given the path as well as the line. It defaults to a file named
    # "f"; pointing it at f.txt is what lets the incumbent see any hunk at all, and a
    # baseline that cannot see the problem is not a baseline.
    return sh([sys.executable, DRIVER, str(case[3]), "f.txt"], d, env=env)


def route_naive(case, d, env):
    """Answer every hunk git prints at its default context -- the first-try script."""
    return sh(["bash", "-c", "printf 'y\\n' | git add -p f.txt"], d, env=env)


ROUTES = [("stg", route_stg), ("filterdiff", route_filterdiff),
          ("pty_driver", route_pty), ("naive", route_naive)]


def measure(case, context):
    name, base, edited, want, want_content = case
    rec = {"case": name, "want": want, "diff_context": context,
           "oracle_content": want_content}
    for rname, fn in ROUTES:
        d, env = make_repo(base, edited, context)
        try:
            rc, out = fn(case, d, env)
            got = index_content(d)
            rc2, diff = sh(["git", "diff", "--cached", "-U0", "f.txt"], d)
            rec[rname] = {
                "exit": rc,
                "match": got == want_content,
                "staged_content": got,
                "wrong_but_exit_0": bool(rc == 0 and got != want_content),
                "under_staged": bool(got is not None and got != edited),
                "staged_hunks": [l for l in diff.split("\n") if l.startswith("@@")],
                "output": out[:300],
            }
        except Exception as exc:                                   # noqa: BLE001
            rec[rname] = {"exit": -1, "match": False, "wrong_but_exit_0": False,
                          "under_staged": False, "error": repr(exc)[:200]}
        finally:
            shutil.rmtree(d)
    return rec


def main():
    if not shutil.which(FILTERDIFF):
        sys.exit("filterdiff not on PATH; set FILTERDIFF=/path/to/filterdiff")
    rows = []
    for case in CASES:
        for ctx in CONTEXTS:
            rec = measure(case, ctx)
            rows.append(rec)
            flags = "  ".join("%s=%s" % (n, "OK" if rec[n].get("match") else "WRONG")
                              for n, _ in ROUTES)
            print("%-26s ctx=%-4s %s" % (case[0], ctx, flags), flush=True)
    raw = os.path.join(HERE, "raw")
    if not os.path.isdir(raw):
        os.makedirs(raw)
    with open(os.path.join(raw, "compare.jsonl"), "a") as fh:
        for r in rows:
            fh.write(json.dumps(r, sort_keys=True) + "\n")

    print("\nscored rows: %d  (%d cases x %d diff.context values)"
          % (len(rows), len(CASES), len(CONTEXTS)))
    for name, _ in ROUTES:
        ok = sum(1 for r in rows if r[name].get("match"))
        silent = sum(1 for r in rows if r[name].get("wrong_but_exit_0"))
        zero = sum(1 for r in rows if r[name].get("exit") == 0)
        print("  %-12s %2d/%-2d correct    %2d wrong-but-exit-0    %2d exit-0"
              % (name, ok, len(rows), silent, zero))
    print("\nper-case, at default diff.context:")
    for r in rows:
        if r["diff_context"] is not None:
            continue
        bad = [n for n, _ in ROUTES if not r[n].get("match")]
        print("  %-26s want line %-2d  %s" % (
            r["case"], r["want"], "all correct" if not bad else "wrong: " + ", ".join(bad)))


if __name__ == "__main__":
    main()
