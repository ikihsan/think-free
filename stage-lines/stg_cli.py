#!/usr/bin/env python3
"""stg - stage part of a file by line number, without a terminal.

`git add -p` can only be driven by a person at a TTY. So can every other
interactive selector in a developer's toolbox, which is why none of them are
reachable from a script, a CI job, an editor keybinding, or an AI coding agent.
`stg` gives the same operation a scriptable interface addressed in the
coordinates you are already looking at: the line numbers of the file.

    stg list                          every stageable change, as path:line
    stg list --json                   the same, for a program
    stg stage src/app.py:42           stage the change on line 42
    stg stage src/app.py:42-51        stage every change in lines 42..51
    stg stage src/app.py:42,docs/a:8  several at once
    stg unstage src/app.py:42         the mirror, addressed by index line
    stg split src/app.py              stage every change, or none

Exit status: 0 nothing matched, 1 something did, 2 usage or git error.
"""

import json
import os
import subprocess
import sys

from stagelib import parse  # noqa: E402

USAGE = __doc__


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


# ---------------------------------------------------------------- commands

def cmd_list(repo, args):
    as_json = "--json" in args
    files = unstaged(repo)
    rows = []
    for path in sorted(files):
        fp = files[path]
        if fp.binary:
            rows.append({"path": path, "binary": True, "changes": []})
            continue
        for c in fp.changes:
            rows.append({"path": path, "binary": False,
                         "change": c.to_dict(fp.new_nlines)})
    for path in sorted(untracked(repo)):
        rows.append({"path": path, "untracked": True, "changes": []})

    if as_json:
        print(json.dumps(rows, indent=2, sort_keys=True))
    else:
        for r in rows:
            if r.get("untracked"):
                print("%s\t(new file, not in the index)" % r["path"])
                continue
            if r.get("binary"):
                print("%s\t(binary)" % r["path"])
                continue
            c = r["change"]
            a = c["anchor"]
            last = a + max(c["new_lines"], 1) - 1
            span = str(a) if last <= a else "%d-%d" % (a, last)
            print("%s:%s\t%s\t%s" % (r["path"], span, c["kind"],
                                     c["preview"].lstrip("+-")))
    return 1 if rows else 0


def cmd_stage(repo, args, reverse=False):
    intent = "unstage" if reverse else "stage"
    if not args:
        die(USAGE)
    for a in args:
        if a.startswith("-"):
            die("unknown option %r" % a)

    source = staged(repo) if reverse else unstaged(repo)

    # A spec is `path`, `path:N` or `path:LO-HI`. Commas separate more specs:
    #
    #     stg stage f.py:1,3-5 g.py:2
    #
    # so a comma-separated run is a list of line ranges in one file, and a bare
    # `3-5` inherits the path from the part before it. A path containing a comma
    # is the one thing this grammar cannot express, so an argument that parses
    # whole *and* names a file we can see is taken as a single spec instead.
    specs = []
    for a in args:
        try:
            whole, _, _ = parse_spec(a)
        except ValueError:
            whole = None
        if whole is not None and whole in source:
            specs.append(a)
            continue
        path = None
        for part in a.split(","):
            part = part.strip()
            if not part:
                continue
            if ":" in part:
                p, _, _rng = part.rpartition(":")
                if p:
                    path = p
                specs.append(part)
            elif path is None:
                die("spec %r: %r has no file path" % (a, part))
            else:
                specs.append("%s:%s" % (path, part))

    selected = []
    for spec in specs:
        path, lo, hi = read_spec(spec)
        fp = source.get(path)
        if fp is None:
            die("no %s change in %s" % (intent, path))
        if fp.binary:
            die("%s is binary; use plain `git %s`" % (path, intent))
        if lo is None:
            picked = list(fp.changes)
        else:
            if hi > max(fp.new_nlines, 1):
                die("%s has %d line%s; you asked for %d"
                    % (path, fp.new_nlines,
                       "" if fp.new_nlines == 1 else "s", hi))
            picked = fp.select(lo, hi)
        if not picked:
            die("no %s change matches %s" % (intent, spec))
        selected.append((fp, picked))

    # one patch per file: git apply wants a single coherent file header
    by_path = {}
    for fp, picked in selected:
        by_path.setdefault(fp.path, (fp, []))[1].extend(picked)
    for path in sorted(by_path):
        fp, picked = by_path[path]
        apply_patch(repo, fp.render(picked), reverse=reverse)
        for c in picked:
            print("%s %s:%d" % (intent, path, c.anchor(fp.new_nlines)))
    return 1


def cmd_split(repo, args):
    """`git add -p`'s split, applied to every hunk at once, or reported."""
    all_of_them = "--all" in args
    paths = [a for a in args if not a.startswith("-")]
    if not all_of_them and not paths:
        die("give at least one path, or --all")
    files = unstaged(repo)
    for path in (paths or sorted(files)):
        fp = files.get(path)
        if fp is None:
            die("no unstaged change in %s" % path)
        if fp.binary:
            die("%s is binary" % path)
        if all_of_them:
            apply_patch(repo, fp.render(fp.changes))
        print("%s %s: %d stageable change%s" % (
            "staged" if all_of_them else "listed", path, len(fp.changes),
            "" if len(fp.changes) == 1 else "s"))
    return 1


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(USAGE)
        return 0
    cmd, rest = argv[0], argv[1:]
    if cmd not in ("list", "stage", "unstage", "split"):
        die("unknown command %r\n\n%s" % (cmd, USAGE))
    repo = find_repo(os.getcwd())
    if repo is None:
        die("not inside a git repository")
    rc = {"list": cmd_list, "stage": lambda r, a: cmd_stage(r, a),
          "unstage": lambda r, a: cmd_stage(r, a, reverse=True),
          "split": cmd_split}[cmd](repo, rest)
    return rc


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
