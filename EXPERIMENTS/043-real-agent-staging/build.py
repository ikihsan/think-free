#!/usr/bin/env python3
"""Build the E043 fixtures: one real git repository per (scenario, arm).

Each fixture is a fresh repository with a committed file and a dirty working
tree carrying a known set of edits.

Two things are kept apart on purpose:

* `.expected_index` -- the literal content the index should hold when exactly
  the requested change is staged. It is written **by hand** from the scenario
  description below. No route under test (stg, filterdiff, a hand-written
  plumbing route, or the agent's own) ever reads it before the run, so it is
  an independent oracle and not a re-derivation of any selector.

* the requested line number -- located mechanically from an anchor substring
  and then **asserted against git's own `diff -U0`**, so a fixture whose
  numbering has drifted fails to build instead of quietly scoring the wrong
  line as correct.
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
# Asking for the *second* of the pair is the case `git add -p`'s own split
# cannot reach: `git diff -U0` emits one hunk with two removes and two adds,
# so the coordinate has to be resolved by pairing them line for line.
_adj_from = ("def load(path):\n"
             "    with open(path) as fh:\n"
             "        return fh.read()")
_adj_to = ("def load(path):\n"
           "    with open(path, \"rb\") as fh:\n"
           "        return fh.read().decode(\"utf-8\")")
_adj = BASE.replace(_adj_from, _adj_to)
# The oracle keeps the *first* edit (the `rb` mode) and drops the second.
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
    e.update({"GIT_AUTHOR_NAME": "e043",
              "GIT_AUTHOR_EMAIL": "e043@example.invalid",
              "GIT_COMMITTER_NAME": "e043",
              "GIT_COMMITTER_EMAIL": "e043@example.invalid"})
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


def build(root, name, spec, want_stg):
    path = os.path.join(root, name + ("-stg" if want_stg else "-nostg"))
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

    with open(os.path.join(path, ".expected_index"), "w") as fh:
        fh.write(spec["expected_index"])
    with open(os.path.join(path, ".requested_line"), "w") as fh:
        fh.write("%d\n" % line)
    return path, line


def main():
    root = sys.argv[1]
    if os.path.exists(root):
        shutil.rmtree(root)
    os.makedirs(root)
    for name, spec in sorted(SCENARIOS.items()):
        for want in (False, True):
            path, line = build(root, name, spec, want)
            print("%s\t%s\tline %d\t%s" % (path, name, line, spec["describe"]))


if __name__ == "__main__":
    main()