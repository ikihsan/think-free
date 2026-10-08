#!/usr/bin/env python3
"""E055 arms: one function per stager, each returning its own exit and output.

Every arm is handed the same declared intent — "make the index hold this change,
at working-tree line N" — and each translates that into its own documented
syntax. The grader never sees any of this; `run.py` keeps them apart, which is
the whole point: an arm that reports success is not evidence about the index.

An arm returns `{"exit", "out", "err"}` or `{"not_evaluated": reason}`. A tool
that *refuses* is a result and keeps its exit code; a tool that cannot run at
all is `not_evaluated` and is excluded from every count, because an arm that
never started reads as a clean run (F010, F084).

`body_position` is deliberately a second reader rather than a call into
git-hunk's parser: it walks git's own `-U3` output, so agreement with the
position `git-hunk show` prints is evidence about the tool instead of a
tautology about the harness.
"""

import json
import os
import re
import shutil
import sys

from gitenv import GIT_HUNK, FILTERDIFF, DRIVER, STG, git, sh

HUNK_RE = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")


def body_position(repo, want, env=None):
    """The `git-hunk -l` selector for working-tree line `want`, or (None, why).

    git-hunk pins `diff -U3`; its `-l` counts positions in the hunk body with
    context lines included and the `@@ ... @@ trailing-text` context excluded.
    Measured on this host before the run: `-l 4` staged the fourth body line of a
    hunk whose fourth body line was working-tree line 5, and `-l 8` on a 7-line
    body was refused as out of range — so the space is the body, not the file.
    """
    rc, out, _ = git(["diff", "-U3", "--no-color", "--", "f.txt"], repo, env)
    if rc != 0:
        return None, "git diff failed: %s" % out[:120]
    lines = out.split("\n")
    for i, raw in enumerate(lines):
        m = HUNK_RE.match(raw)
        if not m:
            continue
        new_line = int(m.group(3))
        for offset, body in enumerate(lines[i + 1:]):
            if not body or body.startswith("@@") or body.startswith("diff --git"):
                break
            prefix = body[0]
            if prefix == "+":
                if new_line == want:
                    return offset + 1, "changed line"
                new_line += 1
            elif prefix == " ":
                if new_line == want:
                    return None, "line %d is context; nothing to stage" % want
                new_line += 1
    return None, "line %d is not a changed line in any -U3 hunk" % want


def hunk_id(repo, env=None):
    """The unstaged hunk id for f.txt, read from git-hunk's own listing."""
    rc, out, err = sh([GIT_HUNK, "list", "--json"], repo, env)
    if rc != 0:
        return None, "git-hunk list exited %d: %s" % (rc, (err or out)[:160])
    try:
        doc = json.loads(out)
    except ValueError as exc:
        return None, "git-hunk list --json did not parse: %s" % exc
    hunks = [h for h in doc.get("hunks", [])
             if h.get("status") == "unstaged"
             and h.get("file", {}).get("text") == "f.txt"]
    if len(hunks) != 1:
        return None, "%d unstaged hunks for f.txt, expected exactly 1" % len(hunks)
    return hunks[0]["id"], None


def _missing(tool):
    return {"not_evaluated": "%s not on PATH" % tool} if not shutil.which(tool) \
        else None


def _run(args, repo, env=None):
    """Every arm's result is a dict, so no caller has to know which shape it got."""
    rc, out, err = sh(args, repo, env)
    return {"exit": rc, "out": out, "err": err}


def arm_stg(repo, want, env):
    return _run([sys.executable, STG, "stage", "f.txt:%d" % want], repo, env)


def arm_filterdiff(repo, want, env):
    if not shutil.which(FILTERDIFF):
        return _missing(FILTERDIFF)
    return _run(["bash", "-c", "git diff -U0 | %s --lines=%d | "
                "git apply --cached --unidiff-zero" % (FILTERDIFF, want)], repo, env)


def arm_pty(repo, want, env):
    if not os.path.exists(DRIVER):
        return {"not_evaluated": "E037 driver.py not found at %s" % DRIVER}
    return _run([sys.executable, DRIVER, str(want), "f.txt"], repo, env)


def arm_naive(repo, _want, env):
    """The route F083 observed every real agent converging on.

    `git add -p` cannot address a line, so this arm answers every hunk at git's
    default context. It is in the population because six real agents wrote this
    by hand: `git diff`, hand-write a minimal patch, `git apply --cached`.
    """
    return _run(["bash", "-c", "printf 'y\\n' | git add -p f.txt"], repo, env)


def arm_git_hunk_native(repo, want, env):
    """git-hunk's best case: the caller converts the file line to a body position."""
    if not shutil.which(GIT_HUNK):
        return _missing(GIT_HUNK)
    pos, why = body_position(repo, want, env)
    if pos is None:
        return {"not_evaluated": why, "exit": None, "selector": None}
    hid, why = hunk_id(repo, env)
    if hid is None:
        return {"not_evaluated": why, "exit": None, "selector": None}
    res = _run([GIT_HUNK, "stage", hid, "-l", str(pos)], repo, env)
    res["selector"] = {"want_line": want, "passed": pos, "hunk": hid[:7],
                       "space": "hunk body, context counted"}
    return res


def arm_git_hunk_naive(repo, want, env):
    """The realistic porting mistake, declared rather than discovered.

    `-l` counts hunk-body positions with context included; `stg` takes an
    absolute file line. The two spaces differ by the number of leading context
    lines in the hunk, and this arm measures what that costs when a caller ports
    a number between them. It is excluded from KILL-C's K2 on purpose: K2 asks
    about a shipped tool's own best case, and counting a caller's mistake as the
    tool's failure would be the wrong comparison.
    """
    if not shutil.which(GIT_HUNK):
        return _missing(GIT_HUNK)
    hid, why = hunk_id(repo, env)
    if hid is None:
        return {"not_evaluated": why, "exit": None, "selector": None}
    res = _run([GIT_HUNK, "stage", hid, "-l", str(want)], repo, env)
    res["selector"] = {"want_line": want, "passed": want, "hunk": hid[:7],
                       "space": "file line passed as a body position on purpose"}
    return res


def arm_gah(repo, _want, _env):
    """Declared before the fetch, never measured."""
    return {"not_evaluated": "gah 0.3.0: no release binary exists on any channel "
                             "(all five GitHub releases carry zero assets, no "
                             "binstall entry, no container) and building it needs "
                             "a Rust edition-2024 toolchain this host does not have"}


ARMS = [
    ("stg", arm_stg),
    ("filterdiff", arm_filterdiff),
    ("pty_driver", arm_pty),
    ("naive", arm_naive),
    ("git-hunk-native", arm_git_hunk_native),
    ("git-hunk-naive", arm_git_hunk_naive),
    ("gah", arm_gah),
]
