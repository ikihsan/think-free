#!/usr/bin/env python3
"""Test shell baseline against E038's 10 cases × 3 contexts."""
import json
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shell_baseline import ShellBaseline

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
STG = os.path.join(ROOT, "stage-lines", "stg")

# E038's 10 cases
CASES = [
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
    d = tempfile.mkdtemp(prefix="e038-shell-")
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
    rc, out = sh(["git", "show", ":f.txt"], d)
    return out if rc == 0 else None


def route_stg(case, d, env):
    return sh([sys.executable, STG, "stage", "f.txt:%d" % case[3]], d, env=env)


def route_shell_baseline(case, d, env):
    baseline = ShellBaseline()
    rc, out, err, staged = baseline.stage(d, "f.txt", case[3])
    # We need to return the same format as route_stg
    # The staged blob is already in the index, so just return rc and output
    return rc, out + err


ROUTES = [("stg", route_stg), ("shell_baseline", route_shell_baseline)]


def measure(case, context):
    name, base, edited, want, want_content = case
    rec = {"case": name, "want": want, "diff_context": context,
           "oracle_content": want_content}
    for rname, fn in ROUTES:
        d, env = make_repo(base, edited, context)
        try:
            rc, out = fn(case, d, env)
            got = index_content(d)
            rec[rname] = {
                "exit": rc,
                "match": got == want_content,
                "staged_content": got,
                "wrong_but_exit_0": bool(rc == 0 and got != want_content),
                "output": out[:300],
            }
        except Exception as exc:
            rec[rname] = {"exit": -1, "match": False, "wrong_but_exit_0": False,
                          "error": repr(exc)[:200]}
        finally:
            shutil.rmtree(d)
    return rec


def main():
    rows = []
    for case in CASES:
        for ctx in CONTEXTS:
            rec = measure(case, ctx)
            rows.append(rec)
            flags = "  ".join("%s=%s" % (n, "OK" if rec[n].get("match") else "WRONG")
                              for n, _ in ROUTES)
            print("%-26s ctx=%-4s %s" % (case[0], ctx, flags), flush=True)
    
    # Save raw JSONL
    raw_dir = os.path.join(HERE, "raw")
    if not os.path.isdir(raw_dir):
        os.makedirs(raw_dir)
    with open(os.path.join(raw_dir, "e038_comparison.jsonl"), "w") as fh:
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