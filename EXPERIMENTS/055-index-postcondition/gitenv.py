#!/usr/bin/env python3
"""E055: the git environment every arm and every control shares.

Split out by invariant, the way E046 split `Replay` from its judge: materialising
a repository state and judging it are different questions, and code that does
both is code where a mistake in one reads as a finding about the other.

`BASE_ENV` pins identity and dates so a commit is reproducible, and `require_git`
refuses the whole run on git older than 2.28. That refusal is not caution: the
`git-hunk` arm shells out to `git diff --no-relative`, which 2.25.1 rejects, and
an arm that dies on start reads exactly like an arm that found nothing (F010,
F084). E047 built git from source for the same reason.
"""

import os
import subprocess

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HERE = os.path.dirname(os.path.abspath(__file__))

STG = os.path.join(REPO, "stage-lines", "stg")
DRIVER = os.path.join(REPO, "EXPERIMENTS", "037-line-staging", "driver.py")
GIT_HUNK = os.environ.get("GIT_HUNK", "git-hunk")
FILTERDIFF = os.environ.get("FILTERDIFF", "filterdiff")

BASE_ENV = dict(os.environ)
BASE_ENV.update({
    "GIT_CONFIG_NOSYSTEM": "1", "LC_ALL": "C", "GIT_PAGER": "cat", "PAGER": "cat",
    "GIT_AUTHOR_NAME": "e055", "GIT_AUTHOR_EMAIL": "e055@example.invalid",
    "GIT_COMMITTER_NAME": "e055", "GIT_COMMITTER_EMAIL": "e055@example.invalid",
    "GIT_AUTHOR_DATE": "2026-01-01T00:00:00+0000",
    "GIT_COMMITTER_DATE": "2026-01-01T00:00:00+0000",
})


def sh(args, cwd, env=None, stdin=None, timeout=90):
    """Run a command in a repository. Returns (rc, stdout, stderr), never raises."""
    e = dict(BASE_ENV)
    if env:
        e.update(env)
    try:
        p = subprocess.Popen(
            args, cwd=cwd, env=e,
            stdin=subprocess.PIPE if stdin is not None else None,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate(stdin.encode("utf-8") if stdin else None,
                                 timeout=timeout)
    except (OSError, subprocess.SubprocessError) as exc:
        return 127, "", repr(exc)
    return (p.returncode, out.decode("utf-8", "replace"),
            err.decode("utf-8", "replace"))


def git(args, cwd, env=None):
    return sh(["git"] + args, cwd, env)


def ctx_env(context):
    """git's `diff.context`, which E038 varied because it moves hunk boundaries."""
    if context is None:
        return {}
    return {"GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "diff.context",
            "GIT_CONFIG_VALUE_0": str(context)}


def git_ok(version):
    """True when `git --version` reports 2.28 or later. Pure, so it is testable.

    Split out of `require_git` so the rule can be falsified against a string
    rather than only against the machine it happens to run on, which is what
    D025 asks: a gate that can only be exercised on the host that satisfies it
    is a gate nobody has falsified.
    """
    parts = [int(p) for p in version.split(".")[:2] if p.isdigit()]
    return len(parts) == 2 and tuple(parts) >= (2, 28)


def require_git():
    """(ok, version). Below 2.28 the git-hunk arm cannot start."""
    rc, out, _ = git(["--version"], ".")
    ver = out.strip().split()[-1] if rc == 0 else "none"
    return git_ok(ver), ver
