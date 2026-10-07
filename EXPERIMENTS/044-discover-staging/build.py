#!/usr/bin/env python3
"""Build the E044 fixtures: one real git repository per (scenario, arm).

The scenarios are byte-identical to E043's — same committed `app.py`, same
working-tree edits, same requested change — so the two experiments differ only
in the treatment: E043 handed the agent the line number and allowed
`git diff`; E044 gives a semantic description of the change, no line number,
and no `git diff`.

Two things are kept apart on purpose, and one further thing is kept out of
the fixture entirely:

* `oracle/<scenario>.index` -- the literal content the index should hold when
  exactly the requested change is staged. Written **by hand** from the
  scenario description. No route under test reads it before the run.

* `oracle/<scenario>.line` -- the requested line number, located mechanically
  from an anchor substring and asserted against git's own `diff -U0`, so a
  fixture whose numbering drifted fails to build.

* E043 left `.expected_index` and `.requested_line` inside each fixture; a
  trial was one `ls ..` away from the answer. Here the fixture directories
  contain ONLY `app.py` and `.git`; the oracle lives in a sibling directory
  the agent is never given a path to.

Usage: build.py <experiment-root>   (rebuilds fixtures/ and oracle/ from scratch)
"""

import os
import shutil
import subprocess
import sys

BASE = """\
import os
import sys


def load(path):
    with open(path) as fh:
        return fh.read()


def save(path, data):
    with open(path, "w") as fh:
        fh.write(data)


def main():
    if len(sys.argv) < 2:
        print("usage: app.py PATH")
        return 1
    print(load(sys.argv[1]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
"""


def scenario(worktree, line_anchor, expected_index, describe):
    return {"worktree": worktree, "anchor": line_anchor,
            "expected_index": expected_index, "describe": describe}


# -- scenario 1: two ADJACENT modified lines (6 and 7); stage only the 2nd --
_adj_from = ("def load(path):\n"
             "    with open(path) as fh:\n"
             "        return fh.read()")
_adj_to = ("def load(path):\n"
           "    with open(path, \"rb\") as fh:\n"
           "        return fh.read().decode(\"utf-8\")")
_adj = BASE.replace(_adj_from, _adj_to)
# The oracle keeps the *second* edit (the decode) and drops the first.
_adj_keep_second = BASE.replace(_adj_from, _adj_from.replace(
    "        return fh.read()",
    "        return fh.read().decode(\"utf-8\")"))

# -- scenario 2: two ADJACENT inserted lines; stage only the first ----------
_ins = BASE.replace("import os\nimport sys",
                    "import os\nimport sys\nimport json\nimport re")
_ins_keep_first = BASE.replace("import os\nimport sys",
                               "import os\nimport sys\nimport json")

# -- scenario 3: one edited line among three scattered edits ----------------
_three = BASE.replace("import os", "import os.path") \
             .replace("def main():", "def main(argv=None):") \
             .replace("    print(load(sys.argv[1]))",
                      "    print(load(sys.argv[-1]))")
_three_keep = BASE.replace("    print(load(sys.argv[1]))",
                           "    print(load(sys.argv[-1]))")

SCENARIOS = {
    "adjacent-modifications": scenario(
        _adj, "decode(\"utf-8\")", _adj_keep_second,
        "two adjacent modified lines; stage only the second"),
    "two-line-insertion": scenario(
        _ins, "import json", _ins_keep_first,
        "two adjacent inserted lines; stage only the first"),
    "one-edit-among-three": scenario(
        _three, "print(load(sys.argv[-1]))", _three_keep,
        "one edited line among three scattered edits; stage only it"),
}


def run(args, cwd):
    e = dict(os.environ)
    e.update({"GIT_AUTHOR_NAME": "e044",
              "GIT_AUTHOR_EMAIL": "e044@example.invalid",
              "GIT_COMMITTER_NAME": "e044",
              "GIT_COMMITTER_EMAIL": "e044@example.invalid"})
    p = subprocess.Popen(args, cwd=cwd, env=e, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out, err = p.communicate()
    return p.returncode, out.decode("utf-8", "replace"), err.decode("utf-8", "replace")


def changed_new_lines(diff_u0):
    """New-file line numbers git itself says carry a change."""
    lines = set()
    for hunk in [l for l in diff_u0.split("\n") if l.startswith("@@")]:
        body = hunk.split("@@")[1].strip()  # "-a,b +c,d"
        new = body.split("+")[1]
        parts = new.split(",")
        start = int(parts[0])
        count = int(parts[1]) if len(parts) > 1 else 1
        for i in range(start, start + max(count, 1)):
            lines.add(i)
    return lines


def build(fixtures, oracle, name, spec, want_stg):
    path = os.path.join(fixtures, name + ("-stg" if want_stg else "-nostg"))
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)
    rc, _, err = run(["git", "init", "-q", "."], path)
    if rc != 0:
        raise RuntimeError("git init failed: " + err)
    with open(os.path.join(path, "app.py"), "w") as fh:
        fh.write(BASE)
    run(["git", "add", "app.py"], path)
    run(["git", "commit", "-qm", "import"], path)
    with open(os.path.join(path, "app.py"), "w") as fh:
        fh.write(spec["worktree"])

    worktree_lines = spec["worktree"].split("\n")
    matches = [i for i, l in enumerate(worktree_lines, 1)
               if spec["anchor"] in l]
    if len(matches) != 1:
        raise AssertionError("%s: anchor %r matched %d lines"
                             % (name, spec["anchor"], len(matches)))
    line = matches[0]

    rc, diff, _ = run(["git", "diff", "-U0"], path)
    changed = changed_new_lines(diff)
    if line not in changed:
        raise AssertionError(
            "%s: line %d (%r) is not a changed line; git says %s"
            % (name, line, worktree_lines[line - 1].strip(), sorted(changed)))

    # The hand-written oracle must differ from both HEAD and the worktree,
    # or "exact" would be satisfied by staging everything or nothing.
    rc, head, _ = run(["git", "show", "HEAD:app.py"], path)
    if spec["expected_index"] in (head, spec["worktree"]):
        raise AssertionError("%s: oracle is degenerate" % name)

    # Oracle files live OUTSIDE the fixture. The fixture keeps app.py + .git
    # and nothing else, so prepare.py can assert a trial is clean.
    with open(os.path.join(oracle, name + ".index"), "w") as fh:
        fh.write(spec["expected_index"])
    if want_stg:  # same line for both arms; write once, check agreement
        linefile = os.path.join(oracle, name + ".line")
        if os.path.exists(linefile):
            with open(linefile) as fh:
                assert int(fh.read().strip()) == line, name
        else:
            with open(linefile, "w") as fh:
                fh.write("%d\n" % line)
    return path, line


def main():
    root = sys.argv[1]
    fixtures = os.path.join(root, "fixtures")
    oracle = os.path.join(root, "oracle")
    for d in (fixtures, oracle):
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d)
    for name, spec in sorted(SCENARIOS.items()):
        for want in (False, True):
            path, line = build(fixtures, oracle, name, spec, want)
            print("%s\t%s\tline %d\t%s"
                  % (path, name, line, spec["describe"]))


if __name__ == "__main__":
    main()
