#!/usr/bin/env python3
"""E046 instrument: stage one address, judge it, and prove the judge works.

    python3 controls.py          # prints both control verdicts and exits 3 if either fails

The positive control is E038's own 30-row matrix, which has a hand-written oracle:
the exact bytes the index must hold. The negative control builds wrong index
states with `git apply` and requires the judge to refuse every one. Both are part
of the instrument, not of the result -- without them a number in results.jsonl
means nothing. Three earlier versions of the negative control asked `stg` for a
wrong input, which tests the tool rather than the referee; PROTOCOL.md records
why each was abandoned.
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(EXP, "038-staging-prior-art"))

from harness import GIT_ENV, git, judge, stg
from replay import Replay          # noqa: E402
from compare import CASES as E038_CASES, CONTEXTS             # noqa: E402


def synthetic_case(name, base, edited, context):
    """One of E038's own cases, as a case object the real runner can use."""
    return {"case_id": "e038-" + name, "stratum": "positive_control",
            "repo": "e038", "commit": "", "path": "f.txt",
            "pre_blob": base.encode(), "post_blob": edited.encode(),
            "file_is_new": False, "needs_intent_to_add": False,
            "deleted_paths": [], "old_mode": 0o644, "new_mode": 0o644,
            "diff_context": context}

def controls(root, max_addresses):
    """The oracle must reproduce E038's matrix, and must be able to fail."""
    pos_rows, ok = [], 0
    for name, base, edited, want_line, want_content in E038_CASES:
        for context in CONTEXTS:
            case = synthetic_case(name, base, edited, context)
            replay = Replay(root, case)
            if context is not None:
                git(["config", "diff.context", str(context)], replay.repo)
            rc, out, err = stg(["list", "--json"], replay.repo)
            changes = [r["change"] for r in json.loads(out)
                       if rc in (0, 1) and r.get("change")]
            target = None
            for c in changes:
                if c["anchor"] == want_line:
                    target = c
                    break
            if target is None:
                pos_rows.append({"case_id": case["case_id"], "context": context,
                                 "exact": 0, "why": "address not listed",
                                 "anchors": [c["anchor"] for c in changes]})
                continue
            rc2, detail, got = stage_once(replay, case, target)
            exact = got == want_content.encode()
            pos_rows.append({"case_id": case["case_id"], "context": context,
                             "anchor": want_line, "exact": 1 if exact else 0,
                             "exit": rc2, "verdict": detail.pop("verdict", None),
                             "want_bytes": len(want_content),
                             "got_bytes": len(got) if got is not None else None})
            ok += 1 if exact else 0
    # The negative control must exercise the ORACLE, not the tool. Its first two
    # versions asked stg for a wrong line and called a refusal a failure, which
    # punishes correct behaviour and measures nothing; the second asked for a
    # line no change answers to, and stg refused all twelve, which the oracle
    # never saw. So the wrong index state is built here, with `git apply` directly,
    # and the judge must reject each one. A judge that accepts any of these would
    # make every real-change `sound` below meaningless.
    neg_rows, flagged = [], 0
    for name, base, edited, want_line, want_content in E038_CASES[:6]:
        case = synthetic_case(name, base, edited, None)
        replay = Replay(root, case)
        rc, out, _ = stg(["list", "--json"], replay.repo)
        changes = [r["change"] for r in json.loads(out)
                   if rc in (0, 1) and r.get("change")]
        if not changes:
            continue
        target = changes[0]
        before = git(["diff", "-U0", "--no-color", "--", "f.txt"],
                     replay.repo)[1].decode("utf-8", "replace")
        # The correct answer for this case, so an injection can be checked for
        # being wrong at all: on a single-change file "stage everything" is the
        # right answer, and counting it as a failure would be the third version of
        # this control measuring the wrong thing.
        replay.reset()
        stg(["stage", "f.txt:%d" % target["anchor"]], replay.repo)
        correct = replay.index_blob()
        wrongs = wrong_indexes(replay.repo, "f.txt", before, target)
        for label, patch in sorted(wrongs.items()):
            replay.reset()
            if apply_patch(replay.repo, "f.txt", patch) != 0:
                continue
            if replay.index_blob() == correct:
                neg_rows.append({"case_id": case["case_id"], "injected": label,
                                 "verdict": "not_wrong", "flagged": False,
                                 "note": "injection reproduced the correct index"})
                continue
            verdict, detail = judge(replay.repo, "f.txt", target, before)
            # `flagged` means the oracle refused the wrong state, which is what a
            # working oracle does. The comparison is written as "not sound" rather
            # than "mis_staged" so that a refusal for an unforeseen reason still
            # counts: what has to hold is that no wrong state reads `sound`.
            flagged_it = verdict != "sound"
            flagged += 1 if flagged_it else 0
            neg_rows.append({"case_id": case["case_id"], "injected": label,
                             "verdict": verdict, "note": detail.get("note"),
                             "flagged": flagged_it})
    return pos_rows, ok, neg_rows, flagged

def wrong_indexes(repo, path, before, target):
    """Index states that are wrong in a specific way, as patches for `git apply`."""
    body = parse_runs(before, path)
    out = {}
    # 1. nothing staged at all
    out["nothing_staged"] = ""
    # 2. every change in the file, not just the requested one -- the over-staging
    #    bug E038 found, reproduced against this oracle
    out["all_changes"] = before
    # 3. a line git never reported unstaged, spliced in at the right place
    added = body["added"]
    if added:
        anchor_line = target["new_start"]
        extra = "\n".join(["--- a/" + path, "+++ b/" + path,
                           "@@ -%d,0 +%d,1 @@" % (anchor_line - 1, anchor_line),
                           "+" + added[0] + "x"])
        out["invented_line"] = extra + "\n"
    # 4. the requested run plus one extra line of it
    if body["added"]:
        extra = "\n".join(["--- a/" + path, "+++ b/" + path,
                           "@@ -%d,0 +%d,2 @@" % (target["new_start"],
                                                   target["new_start"]),
                           "+" + added[0], "+" + added[0] + "y"])
        out["doubled_run"] = extra + "\n"
    return out

def parse_runs(text, path):
    removed, added = [], []
    for raw in text.split("\n"):
        if raw.startswith("---") or raw.startswith("+++") or \
                raw.startswith("diff ") or raw.startswith("index ") or \
                raw.startswith("@@"):
            continue
        if raw.startswith("-"):
            removed.append(raw[1:])
        elif raw.startswith("+"):
            added.append(raw[1:])
    return {"removed": removed, "added": added}

def apply_patch(repo, path, patch):
    p = subprocess.Popen(["git", "apply", "--cached", "--unidiff-zero", "-"],
                         cwd=repo, env=GIT_ENV, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.communicate(patch.encode("utf-8"))
    return p.returncode


def stage_once(replay, case, change):
    """Reset, ask for exactly one address, hand the index to the judge.

    `git diff -U0` is captured *after* the reset and *before* the request, because
    the judge compares what was staged against what git reported unstaged, and
    both readings have to be of the same state. The index blob is read here rather
    than by the caller for the same reason: the next call resets it.
    """
    replay.reset()
    before = git(["diff", "-U0", "--no-color", "--", case["path"]],
                 replay.repo)[1].decode("utf-8", "replace")
    rc, out, err = stg(["stage", "%s:%d" % (case["path"], change["anchor"])],
                       replay.repo)
    if rc != 1:
        return rc, {"stage_stdout": out.strip(),
                    "stage_stderr": err.strip()[:300]}, None
    verdict, detail = judge(replay.repo, case["path"], change, before)
    detail["stage_stdout"] = out.strip()
    return rc, dict(detail, verdict=verdict), replay.index_blob()


if __name__ == "__main__":
    import tempfile
    import shutil
    root = tempfile.mkdtemp(prefix="e043-controls-")
    try:
        pos_rows, pos_ok, neg_rows, neg_flagged = controls(root, 60)
    finally:
        shutil.rmtree(root, ignore_errors=True)
    neg_real = [r for r in neg_rows if r["verdict"] != "not_wrong"]
    print("positive control: %d/%d rows exact" % (pos_ok, len(pos_rows)))
    print("negative control: %d/%d wrong index states rejected (%d injections "
          "were not wrong and were skipped)"
          % (neg_flagged, len(neg_real), len(neg_rows) - len(neg_real)))
    sys.exit(0 if pos_ok == len(pos_rows) and neg_flagged == len(neg_real) else 3)
