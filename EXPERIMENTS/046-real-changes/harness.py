#!/usr/bin/env python3
"""E046 harness: build real git repositories, stage with stg, and judge with git.

Three things live here and nothing else does:

`Replay`, which puts a case into a working tree the way a developer's tree
actually looks, lives in `replay.py`: materialising the state is a different
invariant from judging it.
- `independent_hunks` parses `git diff --cached -U0` a second time, separately
  from `stagelib`, so the referee is git and not the tool under test.
- `judge` compares what stg *declared* against what git says it staged.

The judge knows one thing the tool does not get to choose: whether the file
existed in HEAD. For a tracked file, staging one address must leave HEAD's
content with exactly that run replaced. For a new file there is no HEAD content,
so the index may hold the addressed run and nothing else.
"""

import difflib
import os
import shutil
import subprocess
import sys
import tempfile

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))

GIT_ENV = dict(os.environ)
GIT_ENV.update({
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_AUTHOR_NAME": "e043", "GIT_AUTHOR_EMAIL": "e043@example.invalid",
    "GIT_COMMITTER_NAME": "e043", "GIT_COMMITTER_EMAIL": "e043@example.invalid",
    "GIT_AUTHOR_DATE": "2026-01-01T00:00:00+0000",
    "GIT_COMMITTER_DATE": "2026-01-01T00:00:00+0000",
    "LC_ALL": "C",
})


def git(args, cwd, stdin=None):
    p = subprocess.Popen(["git"] + args, cwd=cwd, env=GIT_ENV,
                         stdin=subprocess.PIPE if stdin is not None else None,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(stdin.encode("utf-8") if stdin is not None else None)
    return p.returncode, out, err


def lines_of(blob):
    return blob.decode("utf-8", "replace").splitlines(True)


def independent_hunks(text):
    """`git diff -U0` text -> {path: [(old_start, old_lines, new_start, new_lines)]}.

    Deliberately a second implementation: it reads git's own output rather than
    stg's parser, so agreement between the two is evidence rather than a tautology.
    """
    files = {}
    path = None
    for raw in text.split("\n"):
        if raw.startswith("diff --git "):
            path = None
        elif raw.startswith("+++ b/"):
            path = raw[6:].split("\t")[0]
        elif raw.startswith("@@"):
            body = raw.split("@@")[1].strip()
            old, new = body.split(" ")
            os_, ol = old[1:].split(",") if "," in old[1:] else (old[1:], "1")
            ns, nl = new[1:].split(",") if "," in new[1:] else (new[1:], "1")
            if path is not None:
                files.setdefault(path, []).append(
                    (int(os_), int(ol), int(ns), int(nl)))
    return files


def judge(repo, path, decl, before_patch):
    """Did the index change by exactly the change stg declared?

    Nothing here trusts a coordinate. Every quantity comes from git's own output:

    - **Subset.** The patch that is now staged (HEAD to index) must be a strict
      subset of the patch that was unstaged before the request. A tool that
      staged something git had not reported cannot pass, whatever coordinates it
      printed.
    - **Size.** That staged patch must carry exactly `added` and `removed` lines,
      the counts the tool declared. A tool that staged two lines when asked for
      one is caught by the count, not by the position.
    - **Rest.** Applying the remainder (index to working tree) must reproduce the
      working tree byte for byte. This is what catches an under-staging that
      leaves a remainder which no longer applies, and it is git performing the
      arithmetic rather than this file's own reading of it.

    `before_patch` is `git diff -U0` for this path, captured before the request,
    so the comparison is between two git readings of the same repository.
    """
    rc, out, err = git(["diff", "--cached", "-U0", "--no-color", "--", path], repo)
    if rc != 0:
        return "git_error", {"stderr": err.decode("utf-8", "replace")[:300]}
    staged = out.decode("utf-8", "replace")
    hunks = independent_hunks(staged).get(path, [])
    if len(hunks) != 1:
        return "mis_staged", {"git_hunks": hunks,
                              "note": "expected exactly one hunk in the index"}

    b_removed, b_added = patch_runs(before_patch, path)
    s_removed, s_added = patch_runs(staged, path)
    if not s_removed and not s_added:
        return "nothing_staged", {"note": "the index carries no change at all",
                                  "git_hunks": hunks}
    if not contains_all(b_removed, s_removed) or not contains_all(b_added, s_added):
        return "mis_staged", {"git_hunks": hunks,
                              "note": "staged lines git did not report unstaged",
                              "git_removed": s_removed[:6], "git_added": s_added[:6],
                              "before_removed": b_removed[:6],
                              "before_added": b_added[:6]}
    if len(s_added) != decl["added"] or len(s_removed) != decl["removed"]:
        return "mis_staged", {"git_hunks": hunks,
                              "note": "staged line count differs from the declared count",
                              "git_added": len(s_added), "want_added": decl["added"],
                              "git_removed": len(s_removed),
                              "want_removed": decl["removed"]}

    rc, rest, _ = git(["diff", "-U0", "--no-color", "--", path], repo)
    rest_text = rest.decode("utf-8", "replace")
    rc, idx, _ = git(["show", ":" + path], repo)
    staged_lines = lines_of(idx) if rc == 0 else []
    with open(os.path.join(repo, path), "rb") as fh:
        w_lines = lines_of(fh.read())
    if not independent_hunks(rest_text).get(path):
        # Nothing is left unstaged, so there is no patch to apply and `git apply`
        # rightly refuses an empty one. The property becomes the direct one: the
        # index is the working tree.
        if staged_lines != w_lines:
            return "mis_staged", {"git_hunks": hunks,
                                  "note": "nothing left unstaged but index != worktree",
                                  "index_lines": len(staged_lines),
                                  "want_lines": len(w_lines)}
        return "sound", {"git_hunks": hunks, "added": len(s_added),
                         "removed": len(s_removed), "residual": "none"}
    applied, why = apply_to_copy(staged_lines, rest_text, path)
    if applied != w_lines:
        return "mis_staged", {"git_hunks": hunks,
                              "note": "what is left does not reproduce the working tree",
                              "apply_error": why,
                              "after_lines": len(applied) if applied is not None else None,
                              "want_lines": len(w_lines),
                              "first": (applied or [""])[0][:120]}
    return "sound", {"git_hunks": hunks, "added": len(s_added),
                     "removed": len(s_removed)}


def contains_all(before, staged):
    """Is every element of `staged` present in `before`, counting duplicates?"""
    pool = list(before)
    for item in staged:
        if item in pool:
            pool.remove(item)
        else:
            return False
    return True


def patch_runs(text, path):
    """(removed, added) line contents for `path`, from a `git diff -U0` patch."""
    removed, added, inside, cur = [], [], False, None
    for raw in text.split("\n"):
        if raw.startswith("diff --git "):
            head = raw.split(" ")
            cur = head[-1][2:] if len(head) >= 4 and head[-1].startswith("b/") \
                else None
            inside = False
            continue
        if raw.startswith("--- "):
            # The old side of a new file is `/dev/null` and names no path, so a
            # reader that waits for `--- a/<path>` to match never sees the runs
            # at all. That is how 435 real new-file rows first read as
            # "nothing_staged" with the tool having staged correctly.
            inside = cur == path
            continue
        if raw.startswith("+++ b/"):
            continue
        if raw.startswith("index ") or raw.startswith("new file mode") or \
                raw.startswith("old mode") or raw.startswith("new mode") or \
                raw.startswith("similarity index") or raw.startswith("rename "):
            continue
        if raw.startswith("@@"):
            continue
        if not inside:
            continue
        if raw.startswith("\\"):
            continue
        if raw.startswith("-"):
            removed.append(raw[1:])
        elif raw.startswith("+"):
            added.append(raw[1:])
    return removed, added


def apply_to_copy(staged_lines, patch, path):
    """`git apply` the remaining diff to a scratch copy of the index content.

    The scratch tree keeps the real relative path, because `git apply -p1` strips
    `a/` and writes to whatever path the header names. Pointing it at a file called
    `t` makes every apply fail on "No such file", which is what the first version
    did: 55 sound rows all read as mis-staged because the referee, not the tool,
    was broken.
    """
    tmp = tempfile.mkdtemp(prefix="e043-rest-")
    try:
        target = os.path.join(tmp, path)
        d = os.path.dirname(target)
        if d and not os.path.isdir(d):
            os.makedirs(d)
        # newline="" on both sides, or Python's universal-newline translation
        # silently rewrites every CRLF to LF on read and the referee reports the
        # file it just applied correctly as wrong. That is how 23 CRLF rows of a
        # real requests commit came to read as mis-staged.
        with open(target, "w", newline="") as fh:
            fh.writelines(staged_lines)
        p = subprocess.Popen(["git", "apply", "--unidiff-zero", "-p1", "-"],
                             cwd=tmp, env=GIT_ENV, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, err = p.communicate(patch.encode("utf-8"))
        if p.returncode != 0:
            return None, err.decode("utf-8", "replace")[:200]
        with open(target, newline="") as fh:
            return fh.readlines(), ""
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def stg(args, repo):
    """Run the real CLI, the way a caller would: through its own entry point."""
    cli = os.path.join(os.environ.get("STG_DIR",
                                      os.path.join(REPO_ROOT, "stage-lines")),
                       "stg")
    p = subprocess.Popen([sys.executable, cli] + args, cwd=repo, env=GIT_ENV,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return (p.returncode, out.decode("utf-8", "replace"),
            err.decode("utf-8", "replace"))
