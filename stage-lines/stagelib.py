"""Parse `git diff -U0` into individually addressable changes.

The whole program rests on one idea: git already computes which lines changed,
but it only lets a human choose them by pressing keys at a terminal. This
module turns that same information into something a line number can point at.

A *change* here is one maximal run of consecutive added/removed lines, which is
the smallest unit `git apply --cached --unidiff-zero` accepts. It carries both
coordinates, because the line a person is looking at and the line number in git's
patch header are not always the same number:

- ``new_start`` / ``new_lines``: line numbers in the file as it is on the side
  being read. For a stage operation that is the working tree.
- ``old_start`` / ``old_lines``: line numbers on the other side.

Deleted lines have no line of their own in the new file, so they are anchored to
``new_start`` -- the working-tree line the content used to occupy -- and carry
``kind='delete'``. A pure insertion anchors to the line it was inserted *after*,
which is what git's own ``@@ -n,0 +m,1 @@`` header means.
"""

import re

_HUNK = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")
from stagelib_change import Change, _clip  # noqa: F401
from stagelib_split import _split_run



class FilePatch(object):
    """Every change git found in one file, plus the header to replay it."""

    def __init__(self, path, header, changes):
        self.path = path
        self.header = header      # shared and still filling while parsing
        self.changes = changes
        self.new_nlines = None    # filled in by the caller, who knows the file

    @property
    def binary(self):
        """git prints no `+++` line for a binary file, only this."""
        return any(l.startswith("Binary files ") or l.startswith("GIT binary")
                   for l in self.header)

    def select(self, lo, hi):
        return [c for c in self.changes if c.covers(lo, hi, self.new_nlines)]

    def render(self, changes):
        """A patch `git apply --unidiff-zero` will accept for exactly these."""
        out = []
        for line in self.header:
            if line.startswith("index "):
                # a stale blob hash makes git apply reject the patch
                continue
            out.append(line + "\n")
        for c in changes:
            out.append(c.header() + "\n")
            out.extend(l + "\n" for l in c.body)
        return "".join(out)




def parse(text):
    """`git diff -U0` text -> {path: FilePatch} with changes split to single runs."""
    files = {}
    path = None
    header = []
    binary = False
    hunk = None          # [old_start, old_lines, new_start, new_lines, body]

    def flush_hunk():
        if hunk is None or path is None:
            return
        old_start, old_lines, new_start, new_lines, body = hunk
        old_pos, new_pos = old_start, new_start
        runs = []
        group = []
        group_old = group_new = None

        def close_group():
            if group:
                runs.extend(_split_run(group, group_old, group_new))
                del group[:]

        for line in body:
            if line.startswith("\\"):
                if group:
                    group.append(line)
                continue
            tag = line[:1]
            if tag == " ":
                close_group()
                old_pos += 1
                new_pos += 1
            elif tag == "-" or tag == "+":
                if not group:
                    group_old, group_new = old_pos, new_pos
                group.append(line)
                if tag == "-":
                    old_pos += 1
                else:
                    new_pos += 1
            else:
                close_group()
        close_group()
        files[path].changes.extend(runs)

    for raw in text.split("\n"):
        if raw.startswith("diff --git "):
            flush_hunk()
            hunk = None
            path = None
            header = []
            # register the file even if it never gets a `+++` line, which is
            # what happens to a binary file: git only prints
            # `Binary files a/x and b/x differ`
            m = re.match(r"^diff --git a/(.*) b/(.*)$", raw)
            if m and m.group(1) == m.group(2):
                path = m.group(2)
        elif raw.startswith("@@"):
            flush_hunk()
            m = _HUNK.match(raw)
            if m is None:
                raise ValueError("unparsable hunk header: %r" % raw)
            hunk = [int(m.group(1)), int(m.group(2) or 1),
                    int(m.group(3)), int(m.group(4) or 1), []]
        elif hunk is None:
            header.append(raw)
            if raw.startswith("+++ "):
                name = raw[4:].split("\t")[0]
                if name == "/dev/null":
                    path = None
                else:
                    # git writes the post-image as `b/<path>`, optionally
                    # followed by a timestamp when --full-index is in play
                    path = name[2:] if name.startswith("b/") else name
            if path is not None and path not in files:
                # the header list is shared and kept filling, so a FilePatch
                # registered before its `+++` line still renders a full patch
                files[path] = FilePatch(path, header, [])
        else:
            if raw.startswith("\\"):
                # "\ No newline at end of file" is its own patch line and must
                # stay its own line, or git apply rejects the patch back.
                hunk[4].append(raw)
                continue
            if raw[:1] in ("+", "-", " ") and raw != "":
                hunk[4].append(raw)
    flush_hunk()
    return files
