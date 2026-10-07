"""E048 — the review-defect reading: can the user see the disagreement?

Split out of harness.py at the 300-line cap, by invariant: this is the one
place that answers what the user can observe after the commit (or the blocked
commit), while harness.py owns the E047 arm-running oracle.
"""

import os
import tempfile

from gitenv import ROOT, git, node_bin, sh


def prettier_check_blob(blob):
    """True when `blob` passes prettier --check as a .js file, False when it
    does not, None when there is no blob to check."""
    if blob is None:
        return None
    fd, path = tempfile.mkstemp(suffix=".js", dir="/tmp/opencode")
    try:
        with os.fdopen(fd, "w") as fh:
            fh.write(blob)
        cmd = "%s %s --check %s" % (
            node_bin(),
            os.path.join(ROOT, "npm", "node_modules", "prettier", "bin",
                         "prettier.cjs"),
            path)
        code, _ = sh(cmd, "/tmp/opencode")
        return code == 0
    finally:
        os.unlink(path)


def review_defect(repo, result):
    """E048's question: is the formatter's rewrite being rejected visible?

    Three observations on bytes after the run:
    - head_formatted: the committed app.js passes prettier --check
    - worktree_formatted: the worktree file passes prettier --check
    - status_porcelain: what `git status` prints for the user
    The disagreement (defect) shape: head_formatted is False while
    worktree_formatted is True -- the user sees a formatted file and
    `git status` dirty, but HEAD silently fails the format check CI runs.
    """
    commit_blob = result.get("committed_blob") or None
    if commit_blob is None:
        try:
            commit_blob = git(repo, "show", "HEAD:app.js")
        except RuntimeError:
            commit_blob = None
    worktree = result.get("worktree_after", "")
    try:
        status = git(repo, "status", "--porcelain").strip()
    except RuntimeError:
        status = "<git status failed>"
    head_formatted = prettier_check_blob(commit_blob)
    worktree_formatted = prettier_check_blob(worktree)
    return {
        "head_formatted": head_formatted,
        "worktree_formatted": worktree_formatted,
        "status_porcelain": status,
        "disagreement": (head_formatted is False
                         and worktree_formatted is True),
    }
