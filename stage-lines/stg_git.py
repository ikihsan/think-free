#!/usr/bin/env python3
"""Everything `stg` does to a git repository, apart from deciding what to ask for.

Split out of `stg_cli.py` at the 300-line cap and by invariant: this file is the
boundary to git -- reading diffs, counting lines, applying patches -- while
`stg_cli.py` is the interface. `misplaced_insertions` belongs here because the rule
it encodes is about what `git apply` accepts, not about how the tool is addressed.
"""

import os
import subprocess
import sys

from stagelib import parse

def git(args, repo):
    p = subprocess.Popen(["git"] + args, cwd=repo,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return p.returncode, out.decode("utf-8", "replace"), \
        err.decode("utf-8", "replace")


def find_repo(start):
    d = os.path.abspath(start)
    while True:
        if os.path.exists(os.path.join(d, ".git")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def unstaged(repo):
    """git diff -U0 between the index and the working tree."""
    rc, out, err = git(["diff", "-U0", "--no-color", "--no-ext-diff"], repo)
    if rc != 0:
        die("git diff failed: " + err.strip())
    return annotate(repo, parse(out))


def staged(repo):
    """git diff -U0 between HEAD and the index."""
    rc, out, err = git(["diff", "--cached", "-U0", "--no-color",
                        "--no-ext-diff"], repo)
    if rc != 0:
        die("git diff --cached failed: " + err.strip())
    return annotate(repo, parse(out), reverse=True)


def untracked(repo):
    rc, out, _ = git(["ls-files", "--others", "--exclude-standard"], repo)
    return [l for l in out.split("\n") if l]


def line_count(repo, path, reverse=False):
    """How many lines the file has on the side the user is looking at.

    For a stage that is the working tree; for an unstage it is the index.
    """
    if reverse:
        rc, out, err = git(["show", ":" + path], repo)
        if rc != 0:
            return None
    else:
        try:
            with open(os.path.join(repo, path), "rb") as fh:
                out = fh.read().decode("utf-8", "replace")
        except (IOError, OSError):
            return None
    if out == "":
        return 0
    return out.count("\n") + (0 if out.endswith("\n") else 1)


def annotate(repo, files, reverse=False):
    for path, fp in files.items():
        fp.new_nlines = line_count(repo, path, reverse) or 0
    return files


def parse_spec(spec):
    """'path/to/file.py:42' -> (path, 42, 42); 'path:42-51' -> (path, 42, 51).

    A bare 'path' or 'path:' means the whole file, and comes back as lo=None.
    Raises ValueError on anything malformed, so a caller can fall back to
    treating the argument as a list.
    """
    if ":" not in spec:
        return spec, None, None
    path, _, rng = spec.rpartition(":")
    if not path:
        raise ValueError("no file path before the line number")
    if not rng:
        return path, None, None
    a, sep, b = rng.partition("-")
    if not sep:
        b = a
    try:
        lo, hi = int(a), int(b)
    except ValueError:
        raise ValueError("%r is not a line number or range" % rng)
    if lo < 1 or hi < lo:
        raise ValueError("bad line range")
    return path, lo, hi


def read_spec(spec):
    try:
        return parse_spec(spec)
    except ValueError as exc:
        die("spec %r: %s" % (spec, exc))


def ends_with_newline(repo, path):
    """Does the working-tree file end with a newline?

    A file that does not has an unterminated last line, and that changes what
    `git apply --unidiff-zero` will accept.
    """
    try:
        with open(os.path.join(repo, path), "rb") as fh:
            data = fh.read()
    except (IOError, OSError):
        return True
    return data.endswith(b"\n")


def misplaced_insertions(fp, repo, picked):
    """Insertions git would place after the file's unterminated last line.

    `git apply --cached --unidiff-zero` cannot express "a terminated line before
    an unterminated one". Asking for the second of two lines inserted just above
    such a file's last line produces a patch git accepts with exit 0, and the
    index comes back with the new text glued onto the end of the previous line:
    two logical lines silently merged, reported as staged. Measured on a real
    `requests` commit in EXPERIMENTS/046-real-changes.

    There is no patch shape that does the right thing here, so the request is
    refused by name rather than answered wrongly. The bound is the line count of
    the **index**, not of the working tree: an insertion addressed past the last
    line the index actually holds is the one git appends instead of inserting.
    """
    if ends_with_newline(repo, fp.path):
        return []
    held = line_count(repo, fp.path, reverse=True)
    if held is None:
        return []
    return [c for c in picked
            if c.old_lines == 0 and c.new_lines > 0 and c.new_start > held]


def apply_patch(repo, text, reverse=False):
    args = ["apply", "--cached", "--unidiff-zero", "-"]
    if reverse:
        args.insert(1, "-R")
    p = subprocess.Popen(["git"] + args, cwd=repo,
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out, err = p.communicate(text.encode("utf-8"))
    if p.returncode != 0:
        die("git apply refused the patch:\n" + err.decode("utf-8", "replace"))


def die(msg, code=2):
    sys.stderr.write("stg: %s\n" % msg)
    raise SystemExit(code)
