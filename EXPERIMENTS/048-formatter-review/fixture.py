#!/usr/bin/env python3
"""E047 — the fixture: one file, two changed regions, one of them unstaged.

Split out of `harness.py` at the 300-line cap, by invariant: this is the thing
every arm is measured on, and if it changes, every number in
`raw/results.json` changes with it. It lives alone so that a reader can check
the fixture without reading the oracle or the arms.

**Region A** is staged and badly spaced, so `prettier --write` must rewrite it.
That rewrite is what proves the formatter actually ran in a given arm, without
which "no sweep" says nothing about the runner's staging behaviour.

**Region B** is the unstaged marker line, already well formatted so prettier
leaves its bytes alone. The only way it reaches a commit is by being staged, so
its presence in a blob is the finding and its absence is the clean result. No
grading, no model, no judgement call: the claim is that a specific line the user
chose not to stage appears in their commit.

The two regions are six unchanged lines apart, which at git's default three lines
of context makes them two hunks rather than one. Getting that wrong collapses the
experiment: the marker would be inseparable from the region the formatter is
meant to fix, and no arm could distinguish staging from formatting.

Staging is arranged with no interactive command. Region A is written and staged
while region B does not yet exist, so a plain `git add app.js` stages exactly the
hunk region B later modifies. That is `git add -p` with the answer already known,
and it keeps every arm independent of this repository's own tooling.
"""

import os
import tempfile

from gitenv import git

MARKER = "UNSTAGED_SWEEP_MARKER"
REFORMATTED = "const a = 1;"
BADSPACED = "const a   =   1;"

GOOD = """\
// fixture header
const a = 1;
// separator one
// separator two
// separator three
// separator four
// separator five
const b = 2;
// footer one
// footer two
"""

WORKTREE = """\
// fixture header
const a   =   1;
// separator one
// separator two
// separator three
// separator four
// separator five
const %s = "swept";
const b = 2;
// footer one
// footer two
""" % MARKER


def build_repo():
    """A repo with region A staged and region B unstaged, byte for byte."""
    repo = tempfile.mkdtemp(prefix="e047-")
    # `git init -b` needs git 2.28 and this VM runs 2.25.1 on PATH, so the branch
    # name is set the portable way. The name is irrelevant to the oracle; that the
    # first commit is the one `base` is not.
    git(repo, "init", "-q")
    git(repo, "checkout", "-q", "-b", "main")
    git(repo, "config", "user.email", "e047@example.invalid")
    git(repo, "config", "user.name", "E047")
    git(repo, "config", "commit.gpgsign", "false")
    git(repo, "config", "core.autocrlf", "false")
    path = os.path.join(repo, "app.js")
    with open(path, "w") as fh:
        fh.write(GOOD)
    git(repo, "add", "app.js")
    git(repo, "commit", "-q", "-m", "base")
    # Region A only: the marker does not exist yet, so this stages exactly A.
    with open(path, "w") as fh:
        fh.write(GOOD.replace(REFORMATTED, BADSPACED))
    git(repo, "add", "app.js")
    # Now region B appears in the worktree and stays unstaged.
    with open(path, "w") as fh:
        fh.write(WORKTREE)
    return repo


def verify_fixture(repo):
    """Assert the fixture is what the experiment claims, before any arm runs.

    Two properties, both load-bearing: the staged content is exactly region A (no
    marker), and the unstaged content is exactly region A plus region B. If either
    fails, every arm would be measuring a different repository than the one
    described here — which is what happened on the first run of this experiment,
    for the reason recorded at the hunk count below.
    """
    staged = git(repo, "show", ":app.js")
    worktree = open(os.path.join(repo, "app.js")).read()
    unstaged = git(repo, "diff", "--", "app.js")
    problems = []
    if MARKER in staged:
        problems.append("the marker is already staged")
    if BADSPACED not in staged:
        problems.append("region A is not staged")
    if MARKER not in worktree:
        problems.append("the marker is not in the worktree")
    if MARKER not in unstaged:
        problems.append("the marker is not in the unstaged diff")
    # Counted as hunk *headers*, not occurrences of "@@": git writes two per
    # header (`@@ -a,b +c,d @@`) plus optional trailing context, so a substring
    # count reports two for every single hunk. That mistake made a correct
    # fixture look broken on this experiment's first run.
    hunks = sum(1 for line in unstaged.splitlines() if line.startswith("@@"))
    if hunks != 1:
        problems.append("the unstaged diff has %d hunks, expected 1" % hunks)
    return problems