#!/usr/bin/env python3
"""E040: what does a non-interactive staging caller actually pay per route?

A scripted agent receives a request like "stage only the change on line 2 of
f" and must pick an interface. Three routes, all on real git repositories, no
mocks:

  stg        one call to `stage-lines/stg stage f:L`
  plumbing   the git-plumbing route a caller without stg writes by hand:
             git diff -U0, parse hunks, apply --cached --unidiff-zero, verify
  filterdiff git diff -U0 | filterdiff --lines=L | git apply --cached, verify

Per (case, route) we record: exit code, tool calls, bytes of output the
caller must read, the staged blob, exactness (staged == requested change),
and honesty (did a non-zero exit accompany a correct refusal; did exit 0
hide a wrong staging). Ground truth is a literal expected blob per case, not
a re-derivation of the selector.
"""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
STG = os.path.join(HERE, "..", "..", "stage-lines", "stg")
FILTERDIFF = "/tmp/opencode/pu/x/usr/bin/filterdiff"
RAW = os.path.join(HERE, "raw")

CASES = [
    {
        "name": "adjacent-modifications",
        "head": "a\nb\nc\nd\n",
        "work": "A\nB\nc\nd\n",
        "request_line": 2,
        "expected": "a\nB\nc\nd\n",
        "note": "two adjacent edits; asked for line 2 only",
    },
    {
        "name": "two-line-insertion",
        "head": "a\nd\n",
        "work": "a\nx\ny\nd\n",
        "request_line": 2,
        "expected": "a\nx\nd\n",  # stg stages the one asked-for line; routes that keep whole hunks over-stage
        "note": "multi-line insertion; asked for one of its lines",
    },
    {
        "name": "single-line-insertion",
        "head": "a\nc\n",
        "work": "a\nb\nc\n",
        "request_line": 2,
        "expected": "a\nb\nc\n",
        "note": "one inserted line, asked for it",
    },
    {
        "name": "tail-modification",
        "head": "a\nb\nc\n",
        "work": "a\nb\nC\n",
        "request_line": 3,
        "expected": "a\nb\nC\n",
        "note": "edit on the last line",
    },
    {
        "name": "unchanged-line",
        "head": "a\nb\n",
        "work": "A\nb\n",
        "request_line": 2,
        "expected": "a\nb\n",  # nothing stageable at line 2
        "unstageable": True,
        "note": "asked for a line that did not change",
    },
]


def sh(args, cwd, input_bytes=None, count=None):
    if count is not None:
        count[0] += 1
    p = subprocess.run(
        args, cwd=cwd, input=input_bytes, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out = p.stdout + p.stderr
    return p.returncode, out


def build_repo(case, root):
    env = dict(os.environ)
    env.update({
        "GIT_AUTHOR_NAME": "e040", "GIT_AUTHOR_EMAIL": "e@x",
        "GIT_COMMITTER_NAME": "e040", "GIT_COMMITTER_EMAIL": "e@x",
    })
    subprocess.run(["git", "init", "-q"], cwd=root, check=True, env=env)
    with open(os.path.join(root, "f"), "w") as fh:
        fh.write(case["head"])
    subprocess.run(["git", "add", "f"], cwd=root, check=True, env=env)
    subprocess.run(["git", "commit", "-qm", "init"], cwd=root, check=True, env=env)
    with open(os.path.join(root, "f"), "w") as fh:
        fh.write(case["work"])


def staged_blob(root):
    p = subprocess.run(["git", "show", ":f"], cwd=root,
                       stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return p.stdout.decode() if p.returncode == 0 else None


def hunk_blocks(diff_text):
    """Split a -U0 diff into (header_lines, [(old_start, old_count,
    new_start, new_count, raw_block_lines)]) keeping raw text."""
    header, hunks = [], []
    cur, block = None, None
    for line in diff_text.splitlines(keepends=True):
        if line.startswith("@@"):
            if cur is not None:
                hunks.append((cur[0], cur[1], cur[2], cur[3], block))
            inner = line.split("@@")[1].strip().split(" ")
            a, c = inner[0][1:], inner[1][1:]
            old_start, old_count = (a.split(",") + ["1"])[:2]
            new_start, new_count = (c.split(",") + ["1"])[:2]
            cur = (int(old_start), int(old_count),
                   int(new_start), int(new_count))
            block = [line]
        elif cur is not None:
            block.append(line)
        else:
            header.append(line)
    if cur is not None:
        hunks.append((cur[0], cur[1], cur[2], cur[3], block))
    return header, hunks


def route_stg(root, line, count):
    rc, out = sh([sys.executable, STG, "stage", "f:%d" % line], root, count=count)
    return rc, out


def route_plumbing(root, line, count):
    """The honest hand-written route: diff, select raw hunks, apply, verify."""
    rc, diff = sh(["git", "diff", "-U0", "--", "f"], root, count=count)
    header, hunks = hunk_blocks(diff.decode())
    keep = []
    for old_start, old_count, new_start, new_count, block in hunks:
        if new_count > 0:
            covered = range(new_start, new_start + new_count)
        else:
            covered = [new_start + 1]  # deletion sits at this working line
        if line in covered:
            keep.append(block)
    if not keep:
        return 2, b"no hunk for that line\n"
    patch = "".join(header) + "".join("".join(b) for b in keep)
    rc, out = sh(["git", "apply", "--cached", "--unidiff-zero"], root,
                 input_bytes=patch.encode(), count=count)
    return rc, out or b"(applied)\n"


def route_filterdiff(root, line, count):
    rc, diff = sh(["git", "diff", "-U0", "--", "f"], root, count=count)
    rc2, out2 = sh([FILTERDIFF, "--lines=%d" % line], root,
                   input_bytes=diff, count=count)
    rc3, out3 = sh(["git", "apply", "--cached", "--unidiff-zero"], root,
                   input_bytes=out2, count=count)
    return rc3 if out3 != b"" else rc3, out2 + out3


def main():
    os.makedirs(RAW, exist_ok=True)
    rows = []
    for case in CASES:
        for route_name, route in (("stg", route_stg),
                                  ("plumbing", route_plumbing),
                                  ("filterdiff", route_filterdiff)):
            root = tempfile.mkdtemp(prefix="e040-")
            build_repo(case, root)
            count = [0]
            rc, out = route(root, case["request_line"], count)
            staged = staged_blob(root)
            exact = staged == case["expected"]
            silent_wrong = (rc == 0 or rc == 1) and staged is not None \
                and staged != case["expected"] and not case.get("unstageable")
            silent_overstage = case.get("unstageable") and rc == 0 \
                and staged != case["head"]
            honest = (rc == 2 and not exact and staged in (case["head"], None)) \
                or exact
            rows.append({
                "case": case["name"], "route": route_name, "exit": rc,
                "tool_calls": count[0], "bytes_read": len(out),
                "staged": repr(staged), "expected": repr(case["expected"]),
                "exact": exact, "honest": honest,
                "silent_wrong": bool(silent_wrong),
                "silent_overstage": bool(silent_overstage),
            })
            print(json.dumps(rows[-1]))
    with open(os.path.join(RAW, "results.jsonl"), "w") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")


if __name__ == "__main__":
    main()
