#!/usr/bin/env python3
"""E046 triage: reproduce one failing row from raw/results.jsonl, in isolation.

    python3 triage.py <case_id substring> [anchor] [--repo LABEL=PATH ...]

Prints the case's two texts around the address, what `stg list --json` declared,
what stg did, what git says the index holds, and what the residual apply produced.
For a class of rows that is the difference between a claim and a guess; the full
run says 40-something rows failed and this file says why each one did.
"""

import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from harness import GIT_ENV, git, stg              # noqa: E402
from replay import Replay                   # noqa: E402
from run import load_manifest                    # noqa: E402


def show(text, lo, hi, label):
    lines = text.decode("utf-8", "replace").splitlines(True)
    print("  %s (%d lines), lines %d..%d:" % (label, len(lines), lo, hi))
    for n in range(max(0, lo), min(len(lines), hi)):
        print("    %4d %s" % (n + 1, lines[n].rstrip("\n")[:96]))


def main(argv):
    repos = {}
    rest = []
    i = 1
    while i < len(argv):
        if argv[i] == "--repo":
            label, _, path = argv[i + 1].partition("=")
            repos[label] = path
            i += 2
            continue
        rest.append(argv[i])
        i += 1
    needle = rest[0]
    want_anchor = int(rest[1]) if len(rest) > 1 else None
    cases = [c for c in load_manifest(repos) if needle in c["case_id"]]
    if not cases:
        raise SystemExit("no case matches %r" % needle)
    case = cases[0]
    print("case %s  (%s, %s, commit %s)"
          % (case["case_id"], case["stratum"], case["status"], case["commit"][:8]))

    root = tempfile.mkdtemp(prefix="e043-triage-")
    replay = Replay(root, case)
    rc, out, err = stg(["list", "--json"], replay.repo)
    rows = json.loads(out) if rc in (0, 1) else []
    changes = [r["change"] for r in rows if r.get("change")]
    target = None
    for c in changes:
        if want_anchor is None or c["anchor"] == want_anchor:
            target = c
            break
    if target is None:
        print("no change at anchor %s; anchors: %s"
              % (want_anchor, [c["anchor"] for c in changes]))
        return 1
    print("declared: %s" % json.dumps(target, sort_keys=True))

    lo = max(0, target["old_start"] - 4)
    hi = target["new_start"] + 4
    show(case["pre_blob"], lo, hi, "pre-image")
    show(case["post_blob"], lo, hi, "post-image")

    anchors = [c["anchor"] for c in changes]
    sharing = [a for a in anchors if a == target["anchor"]]
    print("anchor %d is shared by %d listed change(s)" % (target["anchor"],
                                                          len(sharing)))

    before = git(["diff", "-U0", "--no-color", "--", case["path"]],
                 replay.repo)[1].decode("utf-8", "replace")
    print("\n-- git diff -U0 (unstaged) around the address --")
    print(indent(hunks_near(before, target["new_start"])))
    rc2, out2, err2 = stg(["stage", "%s:%d" % (case["path"], target["anchor"])],
                          replay.repo)
    print("-- stg stage exit=%d --\n%s%s" % (rc2, out2, err2))
    staged = git(["diff", "--cached", "-U0", "--no-color", "--", case["path"]],
                 replay.repo)[1].decode("utf-8", "replace")
    print("-- git diff --cached -U0 --\n%s" % indent(staged))
    rc3, idx, _ = git(["show", ":" + case["path"]], replay.repo)
    print("-- index blob is %d bytes; working tree is %d --"
          % (len(idx) if rc3 == 0 else -1, len(case["post_blob"])))
    return 0


def hunks_near(text, line, window=2):
    out, keep = [], 0
    for raw in text.split("\n"):
        if raw.startswith("@@"):
            parts = raw.split("+")[1].split()[0].split(",")
            keep = abs(int(parts[0]) - line) <= 12
        if keep and raw:
            out.append(raw[:120])
    return "\n".join(out)


def indent(text):
    return "\n".join("    " + l for l in text.split("\n") if l.strip())


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))