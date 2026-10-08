#!/usr/bin/env python3
"""E055 instrument: does `.git/index` hold exactly the bytes that were declared?

    python3 indexcheck.py check --repo DIR --intent FILE
    python3 indexcheck.py wrap  --repo DIR --intent FILE -- CMD [ARG ...]

The intent file maps a path to the exact content its index entry must hold:

    {"f.txt": "one\\ntwo\\nthree\\nFOUR\\n"}

or, for content that is not text, to its sha256:

    {"logo.png": {"sha256": "9f86d0..."}}

Two properties make this an instrument rather than a wrapper around an arm:

- **It reads the index and nothing else.** No arm's exit code, stdout, or
  coordinate vocabulary reaches it, so it cannot be right about an arm by
  construction. Declared in PROTOCOL.md.
- **It compares bytes.** E046's referee read lines back through Python's text
  mode and silently rewrote every CRLF to LF, which is how 23 correct rows of a
  real `requests` commit came to read as wrong (F079). Nothing here decodes
  before comparing; decoding happens only to name a differing line.

Exit codes: 0 every declared entry holds, 1 at least one does not or the
wrapped command failed, 2 usage error.
"""

import hashlib
import json
import os
import subprocess
import sys

GIT_ENV = dict(os.environ)
GIT_ENV.update({"GIT_CONFIG_NOSYSTEM": "1", "LC_ALL": "C",
                "GIT_PAGER": "cat", "PAGER": "cat"})


def git(args, cwd):
    p = subprocess.Popen(["git"] + args, cwd=cwd, env=GIT_ENV,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return p.returncode, out, err


def index_entry(repo, path):
    """The bytes the index holds for `path`, or None if it holds nothing.

    `git cat-file blob :path` rather than `git show :path`: the former names
    the object it is about to print, so a path git cannot resolve and a blob
    that happens to be empty cannot be confused for one another.
    """
    rc, out, err = git(["cat-file", "blob", ":" + path], repo)
    if rc != 0:
        return None, err.decode("utf-8", "replace").strip()
    return out, ""


def expected_bytes(spec):
    if isinstance(spec, str):
        return spec.encode("utf-8"), "text"
    return None, "sha256:" + spec["sha256"]


def first_difference(want, got):
    """(line number, want line, got line) for a text mismatch, else (None, ..).

    Only for the message. The verdict is already decided by byte equality, so a
    decoding failure here cannot change it.
    """
    for i, (a, b) in enumerate(zip(want.split(b"\n"), got.split(b"\n")), start=1):
        if a != b:
            return i, a[:120].decode("utf-8", "replace"), b[:120].decode("utf-8", "replace")
    return None, "", ""


def check_one(repo, path, spec):
    want, kind = expected_bytes(spec)
    got, why = index_entry(repo, path)
    row = {"path": path, "kind": kind}
    if got is None:
        # An entry may legitimately be absent: staging a deletion removes it.
        # So absence is compared against the declaration, not assumed a failure.
        if want == b"":
            row["verdict"] = "absent_as_declared"
            return row, True
        row["verdict"] = "absent"
        row["detail"] = why[:200]
        return row, False
    if want is None:
        row["verdict"] = "holds" if hashlib.sha256(got).hexdigest() == \
            spec["sha256"] else "sha256_mismatch"
        row["got_sha256"] = hashlib.sha256(got).hexdigest()
        return row, row["verdict"] == "holds"
    if got == want:
        row["verdict"] = "holds"
        return row, True
    row["verdict"] = "mismatch"
    row["want_bytes"] = len(want)
    row["got_bytes"] = len(got)
    row["got_sha256"] = hashlib.sha256(got).hexdigest()
    line, wl, gl = first_difference(want, got)
    if line is not None:
        row["first_diff_line"] = line
        row["want_line"] = wl
        row["got_line"] = gl
    return row, False


def check(repo, intent):
    rows, ok = [], True
    for path in sorted(intent):
        row, good = check_one(repo, path, intent[path])
        rows.append(row)
        ok = ok and good
    return rows, ok


def load_intent(path):
    with open(path) as fh:
        intent = json.load(fh)
    if not isinstance(intent, dict) or not intent:
        sys.exit("intent file must be a non-empty object of path -> content")
    return intent


def report(rows, ok, as_json):
    if as_json:
        print(json.dumps({"holds": ok, "entries": rows}, sort_keys=True, indent=2))
    else:
        for r in rows:
            mark = "ok  " if r["verdict"].startswith(("holds", "absent_as")) else "FAIL"
            print("%s %s %s" % (mark, r["path"], r["verdict"]), file=sys.stderr)
            if r["verdict"] == "mismatch" and "first_diff_line" in r:
                print("       line %d: index has %r, declared %r"
                      % (r["first_diff_line"], r["got_line"], r["want_line"]),
                      file=sys.stderr)
            if r["verdict"] == "sha256_mismatch":
                print("       index sha256 %s, declared %s"
                      % (r["got_sha256"], r["kind"].split(":", 1)[1]), file=sys.stderr)
        print("index holds the declared state: %s" % ("yes" if ok else "no"),
              file=sys.stderr)
    return 0 if ok else 1


def main(argv):
    if not argv or argv[0] not in ("check", "wrap"):
        sys.exit(__doc__.strip())
    mode, rest = argv[0], argv[1:]
    if "--" in rest and mode == "wrap":
        cut = rest.index("--")
        opts, cmd = rest[:cut], rest[cut + 1:]
    else:
        opts, cmd = rest, []
    repo, intent_path, as_json = ".", None, False
    i = 0
    while i < len(opts):
        if opts[i] == "--repo":
            repo = opts[i + 1]; i += 2
        elif opts[i] == "--intent":
            intent_path = opts[i + 1]; i += 2
        elif opts[i] == "--json":
            as_json = True; i += 1
        else:
            sys.exit("unknown option %r" % opts[i])
    if intent_path is None:
        sys.exit("--intent FILE is required")
    intent = load_intent(intent_path)
    if mode == "wrap":
        if not cmd:
            sys.exit("wrap needs a command after --")
        rc = subprocess.call(cmd, cwd=os.path.abspath(repo), env=GIT_ENV)
        rows, ok = check(repo, intent)
        if rc != 0:
            print("wrapped command exited %d" % rc, file=sys.stderr)
        return report(rows, ok, as_json) or (0 if rc == 0 else 1)
    rows, ok = check(repo, intent)
    return report(rows, ok, as_json)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
