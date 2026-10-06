#!/usr/bin/env python3
"""Shared harness: a throwaway git repository per test, and real assertions.

No mocks: every assertion is made against `git diff --cached` output, because the
whole claim of this tool is that the index it leaves behind is a real index git
will commit. Run with:  python3 stage-lines/test_stg.py
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
STG = os.path.join(HERE, "stg")
sys.path.insert(0, HERE)
from stagelib import parse  # noqa: E402

_HUNK_RANGE = re.compile(r"^@@ -\d+(?:,\d+)? \+\d+(?:,\d+)? @@")


def run(args, cwd, input=None):
    return subprocess.run(args, cwd=cwd, input=input, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, universal_newlines=True)


def git(args, cwd):
    p = run(["git"] + args, cwd)
    if p.returncode != 0:
        raise AssertionError("git %s failed: %s" % (" ".join(args), p.stderr))
    return p.stdout


class Repo(object):
    def __init__(self):
        self.dir = tempfile.mkdtemp(prefix="stg-test-")
        git(["init", "-q", "."], self.dir)
        git(["config", "user.email", "t@example.com"], self.dir)
        git(["config", "user.name", "t"], self.dir)
        git(["config", "core.autocrlf", "false"], self.dir)

    def write(self, name, text):
        path = os.path.join(self.dir, name)
        with open(path, "w", newline="") as fh:
            fh.write(text)
        return path

    def commit(self, msg="c"):
        git(["add", "-A"], self.dir)
        git(["commit", "-qm", msg], self.dir)

    def stg(self, *args):
        return run([sys.executable, STG] + list(args), self.dir)

    def staged(self, name=None):
        args = ["diff", "--cached", "-U0"]
        if name:
            args += ["--", name]
        return git(args, self.dir)

    def staged_body(self, name=None):
        """The staged diff without git's own `index <hash>..<hash>` line.

        That line names blob ids that depend on git's version and on the exact
        bytes, so asserting on it would test the interpreter, not the tool.
        """
        out = []
        for l in self.staged(name).split("\n"):
            if not l or l.startswith("index "):
                continue
            m = _HUNK_RANGE.match(l)
            # git appends the enclosing function or section name to a hunk
            # header; that is display, not part of the patch we wrote
            if m:
                l = m.group(0)
            out.append(l + "\n")
        return "".join(out)

    def hunks(self, name=None, cached=False):
        args = ["diff", "-U0"] + (["--cached"] if cached else [])
        if name:
            args += ["--", name]
        out = []
        for l in git(args, self.dir).split("\n"):
            m = _HUNK_RANGE.match(l)
            if m:
                # drop the `@@ ... @@ <section heading>` suffix git adds
                out.append(m.group(0))
        return out

    def unstaged_hunks(self, name=None):
        return self.hunks(name)

    def staged_file_content(self, name):
        """The bytes now in the index for this file.

        Asserting on the staged diff cannot see an over-staging bug: a hunk that
        carries two changes when one was asked for still prints one clean hunk.
        The index content is what the user gets, so it is what a test must read.
        """
        return git(["show", ":" + name], self.dir)

    def cleanup(self):
        shutil.rmtree(self.dir, ignore_errors=True)
