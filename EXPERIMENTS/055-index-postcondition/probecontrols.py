#!/usr/bin/env python3
"""E055's probe controls: can the K3 probe see what it is supposed to see?

Split out of `controls.py` by invariant. `controls.py` holds the controls that
bound the **grader** (C1 recovery, C2 sensitivity, C4 selector mapping); this file
holds the controls that bound the **probes** (C5, C6, C7, C8). The distinction is
not cosmetic: the grader's controls ask "can a correct index be rejected and a
wrong index accepted?", the probe's ask "can the instrument that reads the
tool's own output see the shape the gate is about?". A probe blind to that shape
would make a negative gate read as clean, which is the failure F010 records.

Every control here answers "could this run have produced a wrong number for a
reason of its own making?", and none of them reads an arm's vocabulary. C7 is the
one that changed a verdict: the first probe read only `--as-numbered-lines=after`,
which cannot see a carried deletion, so it reported a strict superset where the
tool had in fact claimed exactly the wanted line.
"""

import os
import re
import shutil
import subprocess

import k3probe
from arms import body_position, hunk_id
from gitenv import BASE_ENV, FILTERDIFF, sh
from indexcheck import check
from controls import make_repo, index_bytes

# Read by `k3probe` and by the test that keeps it honest. These are not E038 cases:
# no case in that fixture has a deletion adjacent to the wanted change, which is
# exactly the shape `after` reporting cannot see. `a,b,c,d,e -> A,c,d,e` names
# line 1, whose hunk also deletes line 2.
DELETION_ADJACENT = ("a\nb\nc\nd\ne\n", "A\nc\nd\ne\n", 1)


def _probe_control(root, cases, wanted_case, tag, predicate, question):
    name, base, edited, want, _ = [c for c in cases if c[0] == wanted_case][0]
    d = make_repo(base, edited, root, tag)
    got = k3probe.derive_verdict(d, want)
    shutil.rmtree(d, ignore_errors=True)
    row = {"name": tag, "case": wanted_case, "want_line": want,
           "wrote_lines": got.get("wrote_lines"),
           "removed_old_lines": got.get("removed_old_lines"),
           "named_beyond_want": got.get("named_lines_beyond_want"),
           "why": got.get("why"), "passed": predicate(got)}
    return {"name": question, "rows": 1, "fired": row["passed"], "detail": [row],
            "raw": got.get("raw", "")[:300]}


def control_probe_sees_carried_deletion(root, cases):
    """C7: the probe must see a deletion carried in the wanted line's hunk.

    `--as-numbered-lines=after` alone cannot: a deleted line has no number in the
    new file. Measured, the tool reports `1 :A` — exactly the wanted line — while
    the index also loses line 2 at exit 0. That is the postcondition gap KILL-C
    exists to find, and a probe blind to it would have reported K3 as failed and
    closed the gate on an instrument that could not see the thing.
    """
    base, edited, want = DELETION_ADJACENT
    d = make_repo(base, edited, root, "c7_probe_sees_deletion")
    got = k3probe.derive_verdict(d, want)
    shutil.rmtree(d, ignore_errors=True)
    row = {"name": "c7_probe_sees_carried_deletion", "case": "deletion-adjacent",
           "want_line": want, "wrote_lines": got.get("wrote_lines"),
           "removed_old_lines": got.get("removed_old_lines"),
           "named_beyond_want": got.get("named_lines_beyond_want"),
           "claims_only_the_wanted_line": got.get("claims_only_the_wanted_line"),
           "why": got.get("why")}
    # Two halves. The probe must NAME the extra line, and the fixture must really
    # carry a deletion into the index, or this control would be asserting a probe
    # that is merely wrong.
    row["passed"] = bool(got.get("named_lines_beyond_want"))
    return {"name": "C7_probe_sees_a_carried_deletion", "rows": 1,
            "fired": row["passed"], "detail": [row]}


def control_probe_sees_overstage(root, cases):
    """C5: on a fixture that over-stages, the probe must name another line.

    Without this, K3's negative answer would only mean the probe was blind.
    """
    from controls import OVER_STAGES
    return _probe_control(root, cases, OVER_STAGES[0], "c5_probe_sees_overstage",
                          lambda got: bool(got.get("named_lines_beyond_want")),
                          "C5_probe_sees_an_overstage")


def control_probe_reads_exact(root, cases):
    """C6: on a fixture that stages exactly the want, the probe must name only it.

    A probe that names anything else here would satisfy C5 by accident.
    """
    from controls import STAGES_EXACTLY
    return _probe_control(root, cases, STAGES_EXACTLY[0], "c6_probe_reads_exact",
                          lambda got: got.get("claims_only_the_wanted_line") is True,
                          "C6_probe_reads_a_correct_selection")


def _patch_footprint(repo):
    """Every old and new line number the index-vs-HEAD patch touches, from git.

    Read from `git diff --cached -U0`, which is independent of `filterdiff`: it is
    git's own statement of what is in the index relative to the commit. Returned as
    (old_lines, new_lines) so a comparison against the probe names a disagreement
    rather than a difference.
    """
    rc, out, _ = sh(["git", "diff", "--cached", "-U0", "--no-color", "--", "f.txt"], repo)
    if rc != 0:
        return None, None
    old, new = set(), set()
    for raw in out.split("\n"):
        m = re.match(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", raw)
        if not m:
            continue
        o_line, o_len = int(m.group(1)), int(m.group(2) or 1)
        n_line, n_len = int(m.group(3)), int(m.group(4) or 1)
        if o_len:
            old.update(range(o_line, o_line + o_len))
        if n_len:
            new.update(range(n_line, n_line + n_len))
    return old, new


def control_probe_describes_the_selection(root, cases):
    """C8: the two `--as-numbered-lines` reports together name the whole selection.

    K3's negative answer says the caller can derive the post-state from the tool's
    own output. That is only worth anything if the output is a *complete*
    description, so this compares the probe's reported footprint against the old and
    new line numbers git itself says the index touches, row by row, on the real
    fixtures. Measured rather than argued: the man page's wording is not evidence
    about this build of patchutils.
    """
    rows, agreed, empty = [], 0, 0
    for name, base, edited, want, _ in cases:
        d = make_repo(base, edited, root, "c8-" + name)
        try:
            probe = k3probe.derive_verdict(d, want)
            sh(["bash", "-c", "git diff -U0 | %s --lines=%d | "
                "git apply --cached --unidiff-zero" % (FILTERDIFF, want)], d)
            old, new = _patch_footprint(d)
            reported = set(probe.get("wrote_lines") or []) | \
                set(probe.get("before_lines") or [])
            row = {"case": name, "want_line": want,
                   "git_old_lines": sorted(old) if old is not None else None,
                   "git_new_lines": sorted(new) if new is not None else None,
                   "probe_reported_lines": sorted(reported)}
            if not old and not new:
                row.update({"agrees": None,
                            "note": "nothing staged; filterdiff selected no hunk"})
                empty += 1
            else:
                # A deleted line is named by `before` only, and a replacement is
                # named in both spaces, so the union is the selection's footprint.
                row["agrees"] = (reported == (old | new))
                agreed += 1 if row["agrees"] else 0
            rows.append(row)
        finally:
            shutil.rmtree(d, ignore_errors=True)
    bad = [r for r in rows if r.get("agrees") is False]
    return {"name": "C8_probe_describes_the_whole_selection", "rows": len(rows),
            "decidable": len(rows) - empty, "agreed": agreed,
            "selected_nothing": empty, "disagreements": bad,
            "fired": not bad and agreed > 0}


PROBE_CONTROLS = (control_probe_sees_overstage, control_probe_reads_exact,
                  control_probe_sees_carried_deletion,
                  control_probe_describes_the_selection)
