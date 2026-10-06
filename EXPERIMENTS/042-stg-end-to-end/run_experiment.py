#!/usr/bin/env python3
"""E042 — agent end-to-end evaluation of stg vs alternatives for line-addressable staging.

Measures first-try correctness, silent failure rate, and honest failure signaling.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

# Add shell_baseline to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "041-strongest-baseline"))
from shell_baseline import ShellBaseline

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
STG = os.path.join(ROOT, "stage-lines", "stg")
FILTERDIFF = os.environ.get("FILTERDIFF", "/tmp/opencode/pu/x/usr/bin/filterdiff")

# Test cases: (name, base_text, edited_text, ask_line, oracle_content, description)
CASES = [
    ("modify-one-of-three",
     "line1\nline2\nline3\nline4\nline5\n",
     "line1\nMODIFIED2\nline3\nline4\nline5\n",
     2,
     "line1\nMODIFIED2\nline3\nline4\nline5\n",
     "single modification among unchanged lines"),
    ("deletion-among-edits",
     "a\nb\nc\nd\ne\nf\ng\nh\n",
     "a\nb\nd\ne\nF\ng\nh\n",
     3,
     "a\nb\nd\ne\nf\ng\nh\n",
     "deletion mixed with other changes"),
    ("insertion-among-edits",
     "a\nb\nc\nd\ne\nf\ng\nh\n",
     "a\nb\nc\nd\nNEW\ne\nf\ng\nh\n",
     5,
     "a\nb\nc\nd\nNEW\ne\nf\ng\nh\n",
     "insertion mixed with other changes"),
    ("adjacent-edits",
     "a\nb\nc\nd\ne\n",
     "A\nB\nc\nD\ne\n",
     2,
     "a\nB\nc\nd\ne\n",
     "two adjacent modifications (breaks git add -p)"),
    ("adjacent-inserts",
     "a\nb\nc\n",
     "a\nb\nc\nX\nY\n",
     4,
     "a\nb\nc\nX\n",
     "two adjacent insertions (broke stg in E037)"),
    ("append-at-eof",
     "a\nb\nc\n",
     "a\nb\nc\nd\ne\n",
     4,
     "a\nb\nc\nd\n",
     "insertion at end of file"),
]

CONTEXTS = [None]  # default diff.context only for end-to-end


def sh(args, cwd, stdin=None, env=None):
    e = dict(os.environ)
    if env:
        e.update(env)
    p = subprocess.Popen(args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         stdin=subprocess.PIPE if stdin is not None else None, env=e)
    out, _ = p.communicate(stdin.encode() if stdin else None, timeout=90)
    return p.returncode, out.decode("utf-8", "replace")


def make_repo(base, edited, context=None):
    d = tempfile.mkdtemp(prefix="e042-")
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


def route_shell_baseline(case, d, env):
    baseline = ShellBaseline()
    rc, out, err, staged = baseline.stage(d, "f.txt", case[3])
    return rc, out + err


def route_filterdiff(case, d, env):
    """The incumbent written the way its own man page describes it."""
    return sh(["bash", "-c",
               "git diff -U0 | %s --lines=%d | git apply --cached --unidiff-zero"
               % (FILTERDIFF, case[3])], d, env=env)


def route_naive(case, d, env):
    """Answer every hunk git prints at default context -- the first-try script."""
    return sh(["bash", "-c", "printf 'y\\n' | git add -p f.txt"], d, env=env)


ROUTES = [
    ("stg", route_stg),
    ("shell_baseline", route_shell_baseline),
    ("filterdiff", route_filterdiff),
    ("naive", route_naive),
]


def classify_result(exit_code, staged_content, oracle_content):
    """Classify result into standardized metrics."""
    if staged_content is None:
        staged_content = ""
    
    matches = (staged_content == oracle_content)
    
    if exit_code == 0:
        if matches:
            return "correct"
        else:
            # Exit 0 but wrong content = silent failure
            return "silent_failure"
    elif exit_code == 1:
        # For stg/shell_baseline: exit 1 = success with changes
        if matches:
            return "correct"
        else:
            return "silent_failure"
    elif exit_code == 2:
        # For stg/shell_baseline: exit 2 = honest failure (nothing staged / error)
        if staged_content == "" or staged_content is None:
            return "honest_failure"
        else:
            # Something was staged but exit 2 - ambiguous
            return "ambiguous"
    else:
        return f"exit_{exit_code}"


def measure(case, context):
    name, base, edited, ask_line, oracle, description = case
    rec = {
        "case": name,
        "want_line": ask_line,
        "description": description,
        "diff_context": context,
        "oracle_content": oracle,
    }
    for rname, fn in ROUTES:
        d, env = make_repo(base, edited, context)
        try:
            rc, out = fn(case, d, env)
            got = index_content(d)
            classification = classify_result(rc, got, oracle)
            rec[rname] = {
                "exit": rc,
                "classification": classification,
                "staged_content": got,
                "output": out[:300],
            }
        except Exception as exc:
            rec[rname] = {
                "exit": -1,
                "classification": "error",
                "error": repr(exc)[:200],
            }
        finally:
            shutil.rmtree(d)
    return rec


def main():
    if not os.path.exists(FILTERDIFF):
        sys.exit(f"filterdiff not found at {FILTERDIFF}; set FILTERDIFF=/path/to/filterdiff")
    
    rows = []
    for case in CASES:
        for ctx in CONTEXTS:
            rec = measure(case, ctx)
            rows.append(rec)
            flags = "  ".join(
                "%s=%s" % (n, rec[n].get("classification", "ERROR"))
                for n, _ in ROUTES
            )
            print("%-26s ctx=%-4s %s" % (case[0], ctx if ctx else "default", flags), flush=True)

    # Save raw JSONL
    raw_dir = os.path.join(HERE, "raw")
    if not os.path.isdir(raw_dir):
        os.makedirs(raw_dir)
    with open(os.path.join(raw_dir, "compare.jsonl"), "w") as fh:
        for r in rows:
            fh.write(json.dumps(r, sort_keys=True) + "\n")

    # Summary
    print("\n=== SUMMARY ===")
    print(f"Cases: {len(CASES)}, Contexts: {len(CONTEXTS)}, Total rows: {len(rows)}")
    
    for name, _ in ROUTES:
        correct = sum(1 for r in rows if r[name].get("classification") == "correct")
        silent = sum(1 for r in rows if r[name].get("classification") == "silent_failure")
        honest = sum(1 for r in rows if r[name].get("classification") == "honest_failure")
        ambiguous = sum(1 for r in rows if r[name].get("classification") == "ambiguous")
        other = sum(1 for r in rows if r[name].get("classification", "").startswith("exit_"))
        errors = sum(1 for r in rows if r[name].get("classification") == "error")
        print("  %-12s correct=%d  silent_failure=%d  honest_failure=%d  ambiguous=%d  other=%d  error=%d"
              % (name, correct, silent, honest, ambiguous, other, errors))
    
    # Kill gate evaluation
    print("\n=== KILL GATE ===")
    stg_correct = sum(1 for r in rows if r["stg"].get("classification") == "correct")
    stg_silent = sum(1 for r in rows if r["stg"].get("classification") == "silent_failure")
    
    fd_correct = sum(1 for r in rows if r["filterdiff"].get("classification") == "correct")
    fd_silent = sum(1 for r in rows if r["filterdiff"].get("classification") == "silent_failure")
    
    naive_correct = sum(1 for r in rows if r["naive"].get("classification") == "correct")
    naive_silent = sum(1 for r in rows if r["naive"].get("classification") == "silent_failure")
    
    print(f"stg:           correct={stg_correct}/{len(rows)}  silent_failure={stg_silent}/{len(rows)}")
    print(f"filterdiff:    correct={fd_correct}/{len(rows)}  silent_failure={fd_silent}/{len(rows)}")
    print(f"naive:         correct={naive_correct}/{len(rows)}  silent_failure={naive_silent}/{len(rows)}")
    
    gate1 = (stg_correct > fd_correct or stg_silent < fd_silent) and \
            (stg_correct > naive_correct or stg_silent < naive_silent)
    print(f"\nKill gate 1 (stg better than filterdiff AND naive): {'PASSED' if gate1 else 'FAILED'}")
    
    sb_correct = sum(1 for r in rows if r["shell_baseline"].get("classification") == "correct")
    sb_silent = sum(1 for r in rows if r["shell_baseline"].get("classification") == "silent_failure")
    print(f"shell_baseline: correct={sb_correct}/{len(rows)}  silent_failure={sb_silent}/{len(rows)}")
    gate2 = (sb_correct == stg_correct and sb_silent == stg_silent)
    print(f"Kill gate 2 (shell_baseline matches stg): {'PASSED (mechanism not differentiator)' if gate2 else 'FAILED (mechanism might differ)'}")
    
    # Per-case detail
    print("\n=== PER CASE ===")
    for r in rows:
        bad = [n for n, _ in ROUTES if r[n].get("classification") != "correct"]
        print("  %-26s want line %-2d  %s" % (
            r["case"], r["want_line"],
            "all correct" if not bad else "wrong: " + ", ".join(bad)))


if __name__ == "__main__":
    main()