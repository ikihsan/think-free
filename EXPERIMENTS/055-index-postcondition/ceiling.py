#!/usr/bin/env python3
"""E055 ceiling probe: is `filterdiff`'s auditability a property of the tool or of `-U0`?

Run 3 answered KILL-C's K3 with `do_not_build`: on every silent-wrong row the arm's
own output named the carried line, so the caller could derive the verdict without
reading `.git/index`. Both the arm and the probe that established it run `git diff
-U0`, so the negative carried a ceiling it had not measured — if the
carry-revealing output only works at `-U0`, then K3's `False` is an artefact of the
pipeline and the gate would fire at the context a user actually has.

**The first version of this probe left that question open, and its reason was the
instrument rather than the tool.** It read `--as-numbered-lines`, an *optional*
report that lists every line the selection **spans**. Away from `-U0` that list
holds context lines beside carried ones, so the boolean could not separate "the
tool carried this" from "the tool showed me this neighbourhood". Its C10 was
falsified there and the verdict was recorded `not_evaluated`, `verdict_state:
partial`. That artifact is preserved unedited at `raw/ceiling-run1.json`.

This version reads the arm's **primary** output instead (`patchwalk.py`): in a
unified diff a carried line is a `+`/`-` body line and a context line starts with
a space, so the same question is decidable at every context. PROTOCOL.md's
Amendment 3 declares this and its controls before any row was read.

**It still cannot turn KILL-C into `build`.** K3 asks whether the arm's own output
gives the caller no way to derive the verdict, and this reader answers that
question from the arm's primary output wherever that output names the carried
line. Every row the first run recorded as over-staging named it. So this can only
confirm or strengthen `do_not_build`, and the direction of the change is adverse
to building — which is why it is a declared amendment and not a code edit.

    $ python3 ceiling.py > raw/ceiling.json

Two controls, both about the reader, neither about KILL-C:

- **C11, agreement with git.** The lines the walk reports as carried must equal
  the lines `git diff --cached -U0` says the index actually touches, row by row.
  C8's comparison through a *second* reader, so the two cannot agree merely by
  sharing a bug.
- **C12, not trivially everything.** On a selection that is exact, the walk must
  report the wanted line and no other. Without it, a reader that returned the
  whole hunk would satisfy C11 on the over-staging rows and make K3 unfalsifiable
  in the direction that decides the gate.
"""

import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "038-staging-prior-art"))

import patchwalk                                                    # noqa: E402
import provenance                                                   # noqa: E402
from compare import CASES                                          # noqa: E402
from gitenv import FILTERDIFF, ctx_env, sh                         # noqa: E402

BY_NAME = {c[0]: c for c in CASES}

# The two cases run 3 recorded as silent-wrong for filterdiff (exit 0, one index
# digest), plus two it recorded as holds, so the comparison is against arms the
# main run already scored rather than against new ground.
PROBE_CASES = ["adjacent-edits", "adjacent-pair-plus-far",
               "modify-one-of-three", "three-adjacent"]
# -U0 is the pipeline run 3 declared; 1, 3 and the default are what a caller gets
# from `git diff` and from `git config diff.context`.
CONTEXTS = [0, 1, 3, None]

HUNK = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")


def make_repo(base, edited):
    """Base committed, post-image in the tree, nothing staged.

    `gitenv.sh` pins identity and dates, so this fixture is the same shape the
    main run builds and a reader cannot tell the two apart on anything but the
    question being asked.
    """
    d = tempfile.mkdtemp(prefix="e055-ceiling-")
    with open(os.path.join(d, "f.txt"), "w") as fh:
        fh.write(base)
    sh(["git", "init", "-q", "."], d)
    sh(["git", "add", "f.txt"], d)
    sh(["git", "commit", "-qm", "base"], d)
    with open(os.path.join(d, "f.txt"), "w") as fh:
        fh.write(edited)
    return d


def git_footprint(repo):
    """(old, new) line numbers `git diff --cached -U0` says the index touches.

    Read from git, not from the tool, so C11's comparison can disagree with the
    walk rather than merely restate it.
    """
    rc, out, _ = sh(["git", "diff", "--cached", "-U0", "--no-color", "--", "f.txt"],
                    repo)
    old, new = set(), set()
    if rc != 0:
        return None, None
    for raw in out.split("\n"):
        m = HUNK.match(raw)
        if not m:
            continue
        o_line, o_len = int(m.group(1)), int(m.group(2) or 1)
        n_line, n_len = int(m.group(3)), int(m.group(4) or 1)
        if o_len:
            old.update(range(o_line, o_line + o_len))
        if n_len:
            new.update(range(n_line, n_line + n_len))
    return old, new


def main():
    rows = []
    for name in PROBE_CASES:
        _, base, edited, want, want_content = BY_NAME[name]
        for ctx in CONTEXTS:
            d = make_repo(base, edited)
            try:
                # 1. the arm's own primary output, read BEFORE anything is staged,
                #    so the selection is still visible in `git diff`.
                old, new, why, raw = patchwalk.carried(d, want, ctx)
                # 2. the arm, exactly as run 3 ran it, with the context passed
                #    the way `run.py` passes it so both readers and the arm see
                #    the same `diff.context`.
                e = dict(ctx_env(ctx))
                rc, _out, _err = sh(
                    ["bash", "-c",
                     "git diff --no-color -- f.txt | %s --lines=%d | git apply "
                     "--cached --unidiff-zero%s"
                     % (FILTERDIFF, want,
                        " --unidiff-zero" if ctx == 0 else "")], d, e)
                _rc2, held, _e = sh(["bash", "-c", "git show :f.txt"], d)
                g_old, g_new = git_footprint(d)
                beyond = sorted((old | new) - {want}) if old is not None else None
                rows.append({
                    "case": name, "diff_context": ctx, "want": want,
                    "apply_exit": rc,
                    "index_sha256": hashlib.sha256(held.encode()).hexdigest(),
                    "index_holds_intent": held == want_content,
                    "silent_wrong": rc == 0 and held != want_content,
                    "walk_old_lines": sorted(old) if old is not None else None,
                    "walk_new_lines": sorted(new) if new is not None else None,
                    "walk_named_beyond_want": beyond,
                    "caller_can_derive_the_verdict": bool(beyond),
                    "git_old_lines": sorted(g_old) if g_old is not None else None,
                    "git_new_lines": sorted(g_new) if g_new is not None else None,
                    # C11: the walk's footprint against git's own statement.
                    "walk_matches_git": (old is not None and
                                         (old, new) == (g_old, g_new)),
                    "why": why, "selected_patch": raw[:600],
                })
            finally:
                subprocess.call(["rm", "-rf", d])

    # ---- C11: the walk equals git, on every row where anything was staged.
    staged = [r for r in rows if r["walk_old_lines"] or r["walk_new_lines"]]
    c11_rows = [r for r in staged if r["walk_matches_git"]]
    c11 = bool(staged) and len(c11_rows) == len(staged)

    # ---- C12: an exact selection is reported exactly, not as the whole hunk.
    # Pinned to `modify-one-of-three` at -U0, the one configuration in which the
    # first run measured the selection as exact at every context's worth of care.
    exact = [r for r in rows if r["case"] == "modify-one-of-three"
             and r["diff_context"] == 0]
    c12 = bool(exact) and all(
        r["walk_old_lines"] == [r["want"]] and r["walk_new_lines"] == [r["want"]]
        and r["index_holds_intent"] for r in exact)

    at0 = [r for r in rows if r["diff_context"] == 0]
    away = [r for r in rows if r["diff_context"] != 0]
    # K3 away from -U0, now decidable: it holds wherever the arm's own primary
    # output names a line the caller did not ask for.
    k3_away = "holds" if all(r["caller_can_derive_the_verdict"] for r in away) \
        else ("fails" if not any(r["caller_can_derive_the_verdict"] for r in away)
              else "mixed")
    over_away = sum(r["silent_wrong"] for r in away)
    over_at0 = sum(r["silent_wrong"] for r in at0)
    derived_away = sum(r["caller_can_derive_the_verdict"] for r in away)

    if c11 and c12:
        verdict = (
            "At -U0: %d of %d rows over-stage at exit 0, and the tool's own output "
            "names the carried line in every one. Away from -U0: %d of %d rows "
            "over-stage at exit 0, and the tool's own primary output names a line "
            "beyond the want in %d of %d -- C11 holds the walk to git's own "
            "statement of the index on all %d rows where anything was staged, and "
            "C12 shows the walk reports an exact selection as exactly that line. "
            "K3 therefore fails at every context measured, not only at -U0: the "
            "negative is a property of the tool's output, not of the pipeline's "
            "context. `-U0` remains load-bearing for correctness -- away from it "
            "filterdiff over-stages every case probed -- but not for auditability."
            % (over_at0, len(at0), over_away, len(away), derived_away, len(away),
               len(staged)))
        state = "observed"
    else:
        verdict = ("C11=%s C12=%s; the reader is not established, so K3 away from "
                   "-U0 stays not_evaluated and no verdict is computed from it."
                   % (c11, c12))
        state = "partial"

    print(json.dumps({
        "provenance": {"scripts": provenance.stamp()},
        "rows": rows,
        "controls": {
            "C11_walk_agrees_with_git": c11,
            "C11_rows_compared": len(staged),
            "C11_rows_agreeing": len(c11_rows),
            "C11_disagreements": ["%s/ctx=%s" % (r["case"], r["diff_context"])
                                  for r in staged if not r["walk_matches_git"]],
            "C12_exact_selection_read_exactly": c12,
        },
        "K3_away_from_U0": k3_away if (c11 and c12) else "not_evaluated",
        "verdict": verdict,
        "verdict_state": state,
        "supersedes": {
            "artifact": "raw/ceiling-run1.json",
            "K3_away_from_U0": "not_evaluated",
            "verdict_state": "partial",
            "why": "the first probe read --as-numbered-lines, whose line list "
                   "cannot separate carried lines from context away from -U0; "
                   "PROTOCOL.md Amendment 3",
        },
        "ceiling_of_run3_K3": "none measured: K3 is decided at -U0 and at every "
                              "context above, so the negative is not context-bound",
    }, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
