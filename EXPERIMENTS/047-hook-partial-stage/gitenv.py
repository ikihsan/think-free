#!/usr/bin/env python3
"""E047 — the interpreter and command resolution every arm shares.

Split out of `harness.py` at the 300-line cap, by invariant: this is the one
place that answers "which git, which node, which prettier, and what environment",
and every other module reads those answers from here rather than re-deriving
them. Two of those answers are not what a reader would guess, which is the
reason they live in one file:

- **the git is not the VM's git.** lefthook 2.x requires git >= 2.31 and
  lint-staged 17 requires >= 2.32; this VM has 2.25.1, and both refuse to start
  on it. `setup.sh` builds a current git and every arm uses that one. Staying on
  the system git would have produced "no sweep" for arms that never ran, which
  reads as a result about the runners.
- **paths are absolute, never from `PATH`.** git replaces `PATH` inside a hook
  with its own list, so a hook body that says `node` gets "node: not found" on a
  machine where node is installed and on `PATH`. That cost one run here and it
  produced two arms that did nothing while reporting an error rather than a
  result.
"""

import os
import subprocess

ROOT = os.environ.get("E047_ROOT", "/tmp/opencode/e047")


def git_bin():
    """The git this experiment runs, which is not necessarily the VM's git."""
    built = os.path.join(ROOT, "git", "bin", "git")
    return built if os.path.exists(built) else "git"


def git(repo, *args):
    p = subprocess.run([git_bin(), "-C", repo] + list(args),
                       capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError("git %s -> %s" % (" ".join(args), p.stderr.strip()))
    return p.stdout


def sh(cmd, cwd, timeout=240):
    p = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True,
                       text=True, timeout=timeout, env=env(repo=cwd))
    return p.returncode, p.stdout + p.stderr


def env(repo=None, **extra):
    e = dict(os.environ)
    e["PATH"] = os.path.join(ROOT, "node", "bin") + ":" \
        + os.path.join(ROOT, "git", "bin") + ":" \
        + os.path.join(ROOT, "bin") + ":" + e.get("PATH", "")
    e["E047_ROOT"] = ROOT
    e["npm_config_yes"] = "true"
    if repo:
        e["LEFTHOOK_VERBOSE"] = "1"
    e.update(extra)
    return e


def node_bin():
    """Absolute path to the node this experiment installed. See the module note."""
    return os.path.join(ROOT, "node", "bin", "node")


def prettier_cmd(repo, *args):
    return "%s %s %s" % (node_bin(),
                         os.path.join(ROOT, "npm", "node_modules", "prettier",
                                      "bin", "prettier.cjs"),
                         " ".join(args))


def write(path, text, executable=False):
    with open(path, "w") as fh:
        fh.write(text)
    if executable:
        os.chmod(path, 0o755)
    return path