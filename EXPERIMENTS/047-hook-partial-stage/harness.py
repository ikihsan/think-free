#!/usr/bin/env python3
"""E047 — does a shipped git hook runner fold a partially-staged file's
unstaged hunk into the commit?

The oracle is bytes and nothing else. The claim under test is a correctness
claim: a specific line of content that the user chose not to stage reaches their
commit. There is nothing to grade, score, or ask a model about. `git show :app.js`
and `git cat-file blob HEAD:app.js` either contain the marker or they do not.

Why the commit is made by git and not by the harness. Three of these runners
protect the user by manipulating the index and the worktree *around* the hook —
lint-staged calls it stashing, lefthook calls it hiding, pre-commit does it too.
That is the mechanism under test, so the hook must be reached the way a user
reaches it: `git commit`, through the runner's own installed hook. Invoking
`lefthook run pre-commit` by hand and committing with `--no-verify` would skip
the hiding and report a sweep for lefthook that a real user never gets.

Two readings, because a hook may block the commit rather than make it. What the
runner *staged* is read from the index; what the user would *get* is read from
the commit when one exists. The verdict prefers the commit, because the claim is
about the commit. An arm that reformats and blocks is recorded as blocked, with
its index state, rather than being silently turned into a clean result.

The positive control, and why the experiment is void without it. C0 is the naive
hand-written hook: format the file, `git add` the file. That pattern is what the
two issues in the corpus describe, and everyone agrees it sweeps. If C0 does not
report a sweep on these bytes, this harness cannot detect a sweep, and every
other arm's "clean" is a fact about the harness rather than about the runner. C0
runs first and the run exits non-zero if it does not fail. A gate that cannot
fail is F010; this one is required to fail on the arm it was built to fail on.

The fixture. One file, `app.js`, twelve lines, two changed regions six unchanged
lines apart so they cannot collapse into one hunk at git's default context:

  * region A (staged) — badly spaced, so `prettier --write` must rewrite it. An
    arm where the formatter did not run cannot report "clean" meaningfully, so
    `formatter_ran` is checked on every arm and an arm that fails it is
    INCONCLUSIVE rather than clean.
  * region B (unstaged) — a marker line, already well formatted, so prettier
    leaves its bytes alone and the only way it reaches the commit is by being
    staged.

Staging is arranged without any interactive command: region A is written and
staged while region B does not yet exist, so `git add app.js` stages exactly the
hunk region B later modifies. That is `git add -p` with the answer already
known, and it keeps every arm independent of this repository's own tooling.

Run: python3 EXPERIMENTS/047-hook-partial-stage/harness.py
Writes raw/results.json. Exit 0 when the control failed as required, 1 otherwise.
"""

import json
import os
import shutil
import subprocess
import sys
import time

from arms import ARMS
from fixture import (
    BADSPACED,
    GOOD,
    MARKER,
    REFORMATTED,
    WORKTREE,
    build_repo,
    verify_fixture,
)
from gitenv import git, sh
from versions import read_versions

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")


def read(repo, rev, path="app.js"):
    """Read a blob, retrying and then falling back.

    A runner that blocks the commit rewrites `.git/index` on its way out, and a
    read issued in that window failed and was recorded as "neither a commit nor
    a readable index" — an error that says nothing about the runner. The fallback
    goes through `ls-files -s`, which reads the index entry directly, and reads
    the blob by object id from there.
    """
    import time
    last = None
    for _ in range(5):
        try:
            return git(repo, "show", "%s:%s" % (rev, path))
        except RuntimeError as exc:
            last = exc
            time.sleep(0.3)
    try:
        entry = git(repo, "ls-files", "-s", "--", path).split()
        if len(entry) >= 2:
            return git(repo, "cat-file", "blob", entry[1])
    except RuntimeError as exc:
        last = exc
    sys.stderr.write("read(%s:%s) failed: %s\n" % (rev, path, last))
    return None


def head_moved(repo):
    try:
        return git(repo, "log", "-1", "--format=%s").strip() != "base"
    except RuntimeError:
        return False


def judge(repo):
    """Two independent questions about the same bytes.

    `swept` is the hazard under test: did the hunk the user chose not to stage
    reach the commit? `fix_staged` is a different property: did the formatter's
    rewrite reach the commit? An arm can fail the second while passing the
    first — lefthook without `stage_fixed` does exactly that — and calling such
    an arm "inconclusive, the formatter did not run" would be wrong about it,
    because the formatter ran and its output simply was not staged. Conflating
    the two is also how a tool could be credited with fixing a hazard it never
    addressed, so they are counted separately.

    Whether the formatter ran at all is read from the worktree, the only place
    it can be observed independently of what was staged.
    """
    index_blob = read(repo, ":")
    commit_blob = read(repo, "HEAD") if head_moved(repo) else None
    primary, source = ((commit_blob, "commit")
                       if commit_blob is not None
                       else (index_blob, "index"))
    if primary is None:
        return {"error": "neither a commit nor a readable index", "verdict": "ERROR"}
    worktree = open(os.path.join(repo, "app.js")).read() \
        if os.path.exists(os.path.join(repo, "app.js")) else ""
    # Evidence that the formatter executed is its output appearing *somewhere*:
    # the commit, the index, or the worktree. Looking in one place only is what
    # mislabelled the `git stash push --keep-index` arm, whose stash pop restores
    # a worktree holding the original bad spacing while its commit holds the
    # formatter's output. Nothing in this fixture reformats anything except the
    # formatter, and the B0 arm is the control for exactly that.
    reformatted = [REFORMATTED in t and BADSPACED not in t
                   for t in (commit_blob, index_blob, worktree) if t is not None]
    return {
        # the hazard under test
        "swept": MARKER in primary,
        # a separate property, reported separately
        "fix_staged": REFORMATTED in primary and BADSPACED not in primary,
        # did the formatter run at all
        "formatter_ran": any(reformatted),
        "read_from": source,
        "commit_made": commit_blob is not None,
        "commit_blocked": commit_blob is None,
        "marker_left_in_worktree": MARKER in worktree,
        "index_blob": index_blob,
        "committed_blob": commit_blob,
        "worktree_after": worktree,
    }


def verdict(result):
    """The hazard's verdict, with the precondition stated rather than assumed."""
    if "error" in result:
        return "ERROR: " + result["error"]
    if not result.get("formatter_ran"):
        return ("INCONCLUSIVE: the formatter did not change the worktree, so "
                "the runner's staging behaviour was never exercised")
    if result["swept"]:
        tail = "" if result["fix_staged"] else \
            " (and the formatter's own change was not staged either)"
        return "SWEEP: the unstaged hunk's content reached the commit" + tail
    if not result["fix_staged"]:
        return ("no sweep, but the formatter's change did not reach the "
                "commit: formatted worktree, unformatted commit")
    return "no sweep: the unstaged hunk stayed out and the fix was staged"

def run_arm(name, install, note="", expect_sweep=None, keep=False):
    """Build the fixture, let the arm install itself, commit, and judge.

    `install` writes the runner's configuration into the repo and is the only
    thing that differs between arms of the same runner. `expect_sweep` is the
    arm's declared prediction; recording it is what lets a post-hoc reading of
    the results be checked against what was expected beforehand.
    """
    repo = build_repo()
    problems = verify_fixture(repo)
    if problems:
        shutil.rmtree(repo, ignore_errors=True)
        return {"arm": name, "error": "fixture: " + "; ".join(problems),
                "verdict": "ERROR", "expect_sweep": expect_sweep}
    install_log = ""
    try:
        install_log = install(repo)
    except Exception as exc:
        shutil.rmtree(repo, ignore_errors=True)
        return {"arm": name, "error": "install: %s" % exc, "verdict": "ERROR",
                "install_log": install_log, "expect_sweep": expect_sweep}
    code, log = sh("git commit -q -m under-test", repo)
    result = judge(repo)
    result.update({
        "arm": name,
        "note": note,
        "expect_sweep": expect_sweep,
        "commit_exit": code,
        "commit_log": log[-3000:],
        "install_log": str(install_log)[-2000:],
    })
    result["verdict"] = verdict(result)
    result["matched_expectation"] = (
        None if expect_sweep is None
        else (result.get("swept") == expect_sweep
              and result.get("formatter_ran") is True)
    )
    if keep or os.environ.get("E047_KEEP"):
        result["repo"] = repo
    else:
        shutil.rmtree(repo, ignore_errors=True)
    return result

def main():
    os.makedirs(RAW, exist_ok=True)
    results = []
    for name, install, note, expect in ARMS:
        result = run_arm(name, install, note=note, expect_sweep=expect)
        results.append(result)
        print("%-30s %-14s expect_sweep=%-5s %s"
              % (name, result.get("verdict", "?"), expect,
                 (result.get("error") or "")[:80]))
    control = results[0]
    control_failed = control.get("swept") is True
    # The second control, on the fixture rather than on a runner: with no hook at
    # all the marker must stay out of the commit, and the formatter must not have
    # run. If either fails, the fixture is not the repository the experiment
    # describes and every arm is measuring something else.
    blank = next((r for r in results if r["arm"] == "B0-no-hook"), {})
    fixture_ok = (blank.get("swept") is False
                  and blank.get("formatter_ran") is False)
    payload = {
        "fixture": {
            "good": GOOD,
            "worktree_under_test": WORKTREE,
            "marker": MARKER,
            "note": "region A staged and badly spaced; region B the unstaged "
                    "marker line. Six unchanged lines apart, so they are two "
                    "hunks at git's default context.",
        },
        "versions": read_versions(),
        "arms": results,
        "control_swept": control_failed,
        "fixture_control_ok": fixture_ok,
        "verdict": ("the harness detects a sweep, so every 'clean' below is a "
                    "statement about the runner"
                    if control_failed else
                    "THE HARNESS FAILED ITS CONTROL: it cannot detect a sweep, "
                    "so no other arm's result means anything"),
    }
    with open(os.path.join(RAW, "results.json"), "w") as fh:
        json.dump(payload, fh, indent=2, sort_keys=True)
    print()
    print("control C0 swept: %s   (must be True)" % control_failed)
    print("fixture control B0 clean and no formatter: %s   (must be True)" % fixture_ok)
    print("wrote %s" % os.path.join(RAW, "results.json"))
    return 0 if (control_failed and fixture_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
