#!/usr/bin/env python3
"""E055's grader controls: can the referee be wrong in either direction?

Split out of `run.py` by invariant: materialising a repository state and judging
it are different questions. Every control here answers "could this run have
produced a wrong number for a reason of its own making?", and none of them reads
an arm's vocabulary.

| Control | Question it holds shut |
|---|---|
| C1 recovery | Does the grader accept every state E038's hand-written oracle accepts? |
| C2 sensitivity | Does the grader reject every wrong index state injected with `git apply`? |
| C4 selector mapping | Does this file's body-position reader agree with `git-hunk show`? |

C1 and C2 bound the grader from above and below, so a grader that passes both
both accepts correct states and rejects wrong ones. C4 exists because a
`git-hunk-native` miss would otherwise be the harness's arithmetic rather than the
tool's behaviour. The controls on the *probe* — C5, C6, C7, C8 — are in
`probecontrols.py`, because they bound a different instrument: one that reads the
tool's own output rather than the index.

This module also holds the fixture primitives both files share, so a control in
either one builds the same repository state.
"""

import os
import re
import shutil
import subprocess
import sys

from arms import body_position, hunk_id
from gitenv import BASE_ENV, STG, sh
from indexcheck import check

# E038's cases, by name. The probe controls are pinned to named fixtures because
# they assert a specific reading, and a control that silently re-picks its own case
# when the fixture list changes is a control nobody falsified.
OVER_STAGES = ("adjacent-edits",)        # line 2's hunk also carries line 1
STAGES_EXACTLY = ("modify-one-of-three",)  # line 4's hunk carries only line 4


def make_repo(base, edited, root, tag):
    """Pre-image committed, post-image in the tree, nothing staged."""
    d = os.path.join(root, tag)
    os.makedirs(d)
    sh(["git", "init", "-q", "."], d)
    with open(os.path.join(d, "f.txt"), "w") as fh:
        fh.write(base)
    sh(["git", "add", "f.txt"], d)
    sh(["git", "commit", "-qm", "init"], d)
    with open(os.path.join(d, "f.txt"), "w") as fh:
        fh.write(edited)
    return d


def index_bytes(repo):
    rc, out, _ = sh(["git", "cat-file", "blob", ":f.txt"], repo)
    return out.encode("utf-8") if rc == 0 else None


def score(repo, want_content):
    """The grader's verdict, and the bytes, both independent of every arm."""
    rows, ok = check(repo, {"f.txt": want_content})
    return rows[0]["verdict"], index_bytes(repo), ok


# ------------------------------------------------------------------ C1 and C2

def wrong_patches(before, want):
    """Index states that are wrong in a named way, as patches for `git apply`."""
    added = [r[1:] for r in before.split("\n") if r.startswith("+")
             and not r.startswith("+++")]
    out = {"nothing_staged": "", "all_changes": before}
    if added:
        out["invented_line"] = "\n".join(
            ["--- a/f.txt", "+++ b/f.txt",
             "@@ -%d,0 +%d,1 @@" % (want - 1, want), "+" + added[0] + "x"]) + "\n"
        out["doubled_run"] = "\n".join(
            ["--- a/f.txt", "+++ b/f.txt",
             "@@ -%d,0 +%d,2 @@" % (want, want), "+" + added[0],
             "+" + added[0] + "y"]) + "\n"
    return out


def control_recovery(root, cases):
    """C1: the checker accepts every state E038's hand-written oracle accepts.

    Staging is done by `stg`, which E038 scored 30 of 30 against that oracle, so a
    disagreement here is a defect in the checker and voids the run.
    """
    rows = []
    for name, base, edited, want, want_content in cases:
        d = make_repo(base, edited, root, "c1-" + name)
        sh([sys.executable, STG, "stage", "f.txt:%d" % want], d)
        verdict, got, ok = score(d, want_content)
        equal = got == want_content.encode()
        rows.append({"case": name, "want": want, "grader": verdict,
                     "grader_agrees": ok, "bytes_equal": equal,
                     "both_say_holds": ok and equal})
        shutil.rmtree(d, ignore_errors=True)
    bad = [r for r in rows if not r["both_say_holds"]]
    return {"name": "C1_recovery", "rows": len(rows), "passed": len(rows) - len(bad),
            "failed": bad, "fired": not bad}


def control_sensitivity(root, cases):
    """C2: the checker rejects every wrong index state injected with `git apply`.

    E046's four shapes, and the reason for them: that control's first two versions
    asked `stg` for a wrong input, which tests the tool rather than the referee and
    punishes correct behaviour.
    """
    rows, flagged = [], 0
    for name, base, edited, want, want_content in cases[:6]:
        d = make_repo(base, edited, root, "c2-" + name)
        _, before, _ = sh(["git", "diff", "-U0", "--no-color", "--", "f.txt"], d)
        sh([sys.executable, STG, "stage", "f.txt:%d" % want], d)
        correct = index_bytes(d)
        for label, patch in sorted(wrong_patches(before, want).items()):
            sh(["git", "reset", "-q", "--hard"], d)
            with open(os.path.join(d, "f.txt"), "w") as fh:
                fh.write(edited)
            if label != "nothing_staged":
                p = subprocess.Popen(
                    ["git", "apply", "--cached", "--unidiff-zero", "-"],
                    cwd=d, env=BASE_ENV, stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                p.communicate(patch.encode("utf-8"))
            got = index_bytes(d)
            if got == correct:
                rows.append({"case": name, "injected": label, "grader": "not_wrong",
                             "flagged": False,
                             "note": "injection reproduced the correct index"})
                continue
            verdict, _, _ = score(d, want_content)
            hit = verdict != "holds"
            flagged += 1 if hit else 0
            rows.append({"case": name, "injected": label, "grader": verdict,
                         "flagged": hit})
        shutil.rmtree(d, ignore_errors=True)
    real = [r for r in rows if r["grader"] != "not_wrong"]
    missed = [r for r in real if not r["flagged"]]
    return {"name": "C2_sensitivity", "injected": len(real), "flagged": flagged,
            "missed": missed, "injection_was_not_wrong": len(rows) - len(real),
            "fired": not missed}


# ------------------------------------------------------------------------ C4

def control_mapping(root, cases):
    """C4: the harness's body-position mapping agrees with `git-hunk show`.

    `show` prints `<body position> <prefix><line>`; walking those positions and
    counting new-file lines from the hunk header gives the position for a given
    working-tree line, independently of this file's own `-U3` parser. If the two
    disagreed, a `git-hunk-native` miss would be the harness's arithmetic rather
    than the tool's behaviour.
    """
    rows, agreed, decidable = [], 0, 0
    for name, base, edited, want, _ in cases:
        d = make_repo(base, edited, root, "c4-" + name)
        pos, why = body_position(d, want)
        hid, why2 = hunk_id(d)
        row = {"case": name, "want_line": want, "harness_position": pos}
        if pos is None or hid is None:
            row.update({"agree": None, "why": why or why2})
            rows.append(row)
            shutil.rmtree(d, ignore_errors=True)
            continue
        rc, out, _ = sh(["git-hunk", "show", hid], d)
        new_line, shown = None, None
        m = re.search(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@", out)
        if m:
            new_line = int(m.group(1))
            for raw in out.split("\n"):
                b = re.match(r"^\s*(\d+)\s+([+\- ])(.*)$", raw)
                if not b or new_line is None:
                    continue
                position, prefix = int(b.group(1)), b.group(2)
                if prefix in "+ ":
                    if new_line == want and shown is None:
                        shown = position
                    new_line += 1
        row["shown_position"] = shown
        row["agree"] = (shown == pos) if shown is not None else None
        if row["agree"] is not None:
            decidable += 1
            agreed += 1 if row["agree"] else 0
        rows.append(row)
        shutil.rmtree(d, ignore_errors=True)
    return {"name": "C4_selector_mapping", "rows": len(rows), "decidable": decidable,
            "agreed": agreed, "fired": decidable > 0 and agreed == decidable,
            "detail": rows}


GRADER_CONTROLS = (control_recovery, control_sensitivity, control_mapping)
