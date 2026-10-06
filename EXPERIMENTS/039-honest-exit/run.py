#!/usr/bin/env python3
"""E039: does stg's honest-exit claim survive the failure modes an agent workflow produces?

For each boundary case: run stg against a real repository, record its exit code,
stderr, and the resulting `.git/index` content. The claim under test is the README's:
"if it did not stage what you asked for, it says so instead of exiting 0."

The naive comparison route (git diff -U0 | filterdiff --lines=N | git apply
--cached --unidiff-zero) is run on the same cases to contrast exit behaviour.
Every case is a real git repository; nothing is mocked.

  python3 run.py        # rewrites raw/results.jsonl and prints the table
"""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
STG = os.path.join(HERE, "..", "..", "stage-lines", "stg")
FILTERDIFF = os.environ.get("FILTERDIFF", "filterdiff")


def sh(args, cwd, stdin=None):
    p = subprocess.run(args, cwd=cwd, input=stdin, capture_output=True)
    return p.returncode, p.stdout, p.stderr


def git(args, cwd):
    rc, out, err = sh(["git"] + args, cwd)
    if rc != 0:
        raise RuntimeError("git %s failed: %s" % (args, err.decode()))
    return out.decode()


def new_repo(base):
    os.makedirs(base, exist_ok=True)
    git(["init", "-q"], base)
    git(["config", "user.email", "t@t"], base)
    git(["config", "user.name", "t"], base)
    return base


def write(path, text):
    with open(path, "w") as f:
        f.write(text)


def staged_text(d, path):
    rc, out, _ = sh(["git", "show", ":" + path], d)
    return out.decode() if rc == 0 else None


CASES = []


def case(name):
    def deco(fn):
        CASES.append((name, fn))
        return fn
    return deco


@case("binary-file")
def _(d):
    open(os.path.join(d, "b.bin"), "wb").write(b"BIN\x00\x01\x02")
    git(["add", "b.bin"], d)
    git(["commit", "-qm", "init"], d)
    open(os.path.join(d, "b.bin"), "wb").write(b"BIN\x00\x01\x03")
    return ["stage", "b.bin:1"], "b.bin", None


@case("untracked-file")
def _(d):
    write(os.path.join(d, "f"), "a\nb\n")
    git(["add", "f"], d)
    git(["commit", "-qm", "init"], d)
    write(os.path.join(d, "new.txt"), "x\ny\n")
    return ["stage", "new.txt:1"], "new.txt", "x\ny\n"


@case("out-of-range-line")
def _(d):
    write(os.path.join(d, "f"), "a\nb\nc\n")
    git(["add", "f"], d)
    git(["commit", "-qm", "init"], d)
    write(os.path.join(d, "f"), "a\nB\nc\n")
    return ["stage", "f:99"], "f", "a\nb\nc\n"


@case("missing-path")
def _(d):
    write(os.path.join(d, "f"), "a\nb\n")
    git(["add", "f"], d)
    git(["commit", "-qm", "init"], d)
    write(os.path.join(d, "f"), "a\nB\n")
    return ["stage", "nope.txt:1"], "f", "a\nb\n"


@case("conflict-markers-in-file")
def _(d):
    write(os.path.join(d, "f"), "a\nb\nc\n")
    git(["add", "f"], d)
    git(["commit", "-qm", "init"], d)
    write(os.path.join(d, "f"), "a\n<<<<<<< HEAD\nB\n=======\nX\n>>>>>>> br\nc\n")
    return ["stage", "f:2"], "f", "a\nb\nc\n"


@case("rename-mv")
def _(d):
    write(os.path.join(d, "f"), "a\nb\nc\n")
    git(["add", "f"], d)
    git(["commit", "-qm", "init"], d)
    git(["mv", "f", "g"], d)          # staged rename, already in the index
    write(os.path.join(d, "g"), "a\nB\nc\n")
    return ["stage", "g:2"], "g", "a\nb\nc\n"


@case("mode-change-only")
def _(d):
    write(os.path.join(d, "run.sh"), "echo hi\n")
    git(["add", "run.sh"], d)
    git(["commit", "-qm", "init"], d)
    os.chmod(os.path.join(d, "run.sh"), 0o755)
    return ["stage", "run.sh:1"], "run.sh", "echo hi\n"


@case("already-partially-staged")
def _(d):
    write(os.path.join(d, "f"), "1\n2\n3\n4\n5\n")
    git(["add", "f"], d)
    git(["commit", "-qm", "init"], d)
    write(os.path.join(d, "f"), "A\n2\n3\nB\n5\n")
    # stage only line 1 by hand first:
    git(["reset", "-q"], d)
    rc, diff, _ = sh(["git", "diff", "-U0"], d)
    p = subprocess.run([FILTERDIFF, "--lines=1"], input=diff, capture_output=True)
    sh(["git", "apply", "--cached", "--unidiff-zero", "-"], d, stdin=p.stdout)
    return ["stage", "f:4"], "f", "A\n2\n3\n4\n5\n"


def run_case(name, fn):
    with tempfile.TemporaryDirectory() as d:
        new_repo(d)
        args, path, expect = fn(d)
        before = staged_text(d, path)
        rc, out, err = sh([sys.executable, STG] + args, d)
        after = staged_text(d, path)
        moved = (after != before) and (after is not None or before is None)
        # the index changed by the requested sub-change?
        honest = (rc != 0 and after == before) or (rc == 1 and after != before)
        # naive route on the same repo state is not safely runnable after stg
        # touched the index, so it is measured in its own identical repo:
        return {
            "case": name,
            "stg_argv": ["stg"] + args,
            "stg_exit": rc,
            "stg_stderr": err.decode(errors="replace").strip(),
            "index_changed": after != before,
            "index_now": after,
            "exit_matches_outcome": honest,
        }


def run_naive_same(name, fn):
    """filterdiff route on an identically-built repo; exit code is the contrast."""
    with tempfile.TemporaryDirectory() as d:
        new_repo(d)
        args, path, expect = fn(d)
        line = args[1].split(":")[1] if ":" in args[1] else "1"
        rng = line
        rc, diff, _ = sh(["git", "diff", "-U0"], d)
        p = subprocess.run([FILTERDIFF, "--lines=%s" % rng], input=diff, capture_output=True)
        before = staged_text(d, path)
        rc2, _, err2 = sh(["git", "apply", "--cached", "--unidiff-zero", "-"], d, stdin=p.stdout)
        after = staged_text(d, path)
        return {
            "case": name,
            "naive_exit": rc2,
            "naive_stderr": err2.decode(errors="replace").strip(),
            "index_changed": after != before,
            "index_now": after,
        }


def main():
    rows = []
    for name, fn in CASES:
        rows.append(run_case(name, fn))
    naive = []
    for name, fn in CASES:
        naive.append(run_naive_same(name, fn))
    os.makedirs(RAW, exist_ok=True)
    with open(os.path.join(RAW, "results.jsonl"), "w") as f:
        for r in rows:
            f.write(json.dumps(r, sort_keys=True) + "\n")
    with open(os.path.join(RAW, "naive.jsonl"), "w") as f:
        for r in naive:
            f.write(json.dumps(r, sort_keys=True) + "\n")
    print("%-28s %-5s %-4s %-14s %s" % ("case", "exit", "chg", "honest", "stderr"))
    for r in rows:
        print("%-28s %-5s %-4s %-14s %s" % (r["case"], r["stg_exit"],
              r["index_changed"], r["exit_matches_outcome"], r["stg_stderr"][:60]))
    print("\nnaive route (filterdiff | git apply --cached):")
    for r in naive:
        print("%-28s exit=%-4s changed=%-5s %s" % (r["case"], r["naive_exit"], r["index_changed"], r["naive_stderr"][:50]))


if __name__ == "__main__":
    main()
