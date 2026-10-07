#!/usr/bin/env python3
"""E046: put one real file change into a working tree the way git would see it.

Split out of `harness.py` by invariant. The judge's question is "did the index
change by exactly this"; this module's question is "is the repository in the
state the real commit describes", and getting that wrong makes every verdict
meaningless. A new file is left *untracked* with an intent-to-add entry, a rename
leaves the old path deleted, a mode change sets the mode, and a real mode that
this process could not write to keeps owner-write so the next write does not fail
on a 0444 file from `jqlang/jq`.
"""

import os
import shutil

from harness import GIT_ENV, git

class Replay(object):
    """One case, materialised as a real repository state."""

    def __init__(self, root, case):
        self.case = case
        self.path = case["path"]
        self.repo = os.path.join(root, "repo")
        if os.path.exists(self.repo):
            shutil.rmtree(self.repo)
        os.makedirs(self.repo)
        git(["init", "-q", self.repo], self.repo)
        self.write("seed.txt", b"seed\n")
        git(["add", "seed.txt"], self.repo)
        git(["commit", "-q", "-m", "base"], self.repo)
        if not case["file_is_new"]:
            self.write(self.path, case["pre_blob"], case["old_mode"])
            git(["add", "--", self.path], self.repo)
            git(["commit", "-q", "-m", "pre-image of the real commit"], self.repo)
        # Real commits carry modes this process cannot restore for itself: a
        # 040755 or 0444 file left in the tree makes the next write fail with
        # EACCES, which killed the run at jq's manual.yml. The case's recorded
        # mode is applied to the index entry instead, and the working tree is kept
        # writable, because the mode under test is what git reports, not what this
        # process is allowed to do.
        self.reset()

    def write(self, rel, blob, mode=0o644):
        full = os.path.join(self.repo, rel)
        d = os.path.dirname(full)
        if d and not os.path.isdir(d):
            os.makedirs(d)
        with open(full, "wb") as fh:
            fh.write(blob)
        os.chmod(full, mode)
        if not os.access(full, os.W_OK):
            # git records only the executable bit, so 0444 and 0644 are the same
            # entry to it; restoring owner-write keeps this file's real mode
            # without changing anything git can see. The first version applied the
            # mode literally and died with EACCES on jq's 0444 manual.yml.
            os.chmod(full, mode | 0o200)

    def reset(self):
        """Back to: pre-image committed, post-image in the tree, nothing staged."""
        git(["reset", "-q", "--hard"], self.repo)
        for rel in self.case.get("deleted_paths", []):
            p = os.path.join(self.repo, rel)
            if os.path.exists(p):
                os.remove(p)
        self.write(self.path, self.case["post_blob"], self.case["new_mode"])
        if self.case.get("needs_intent_to_add"):
            rc, _, err = git(["add", "-N", "--", self.path], self.repo)
            return rc, err.decode("utf-8", "replace")
        return 0, ""

    def index_blob(self):
        rc, out, _ = git(["show", ":" + self.path], self.repo)
        return out if rc == 0 else None
