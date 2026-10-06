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


class Change(object):
    """One addressable run of consecutive changed lines."""

    __slots__ = ("old_start", "old_lines", "new_start", "new_lines", "body")

    def __init__(self, old_start, old_lines, new_start, new_lines, body):
        self.old_start = old_start
        self.old_lines = old_lines
        self.new_start = new_start
        self.new_lines = new_lines
        # body lines keep the trailing "\ No newline at end of file" marker
        # glued on, because git apply needs it to accept the patch back.
        self.body = body

    @property
    def added(self):
        return sum(1 for l in self.body if l.startswith("+"))

    @property
    def removed(self):
        return sum(1 for l in self.body if l.startswith("-"))

    @property
    def kind(self):
        if self.removed and not self.added:
            return "delete"
        if self.added and not self.removed:
            return "add"
        return "modify"

    def anchor(self, new_nlines):
        """The line number a person would quote for this change.

        Adds and modifications are anchored at their first line in the file as it
        reads now. A deletion is anchored at the line that *took its place* --
        the line whose content moved up because the deletion happened -- so that
        every addressable change names a line that exists in the current file.
        At end of file there is no such line, so it falls back to the last one.
        """
        if self.kind != "delete":
            return max(1, self.new_start)
        nxt = self.new_start + 1
        return nxt if nxt <= new_nlines else max(1, new_nlines)

    def covers(self, lo, hi, new_nlines):
        """Does this change intersect the inclusive line range [lo, hi]?"""
        return lo <= self.anchor(new_nlines) <= hi

    def header(self):
        return "@@ -%d,%d +%d,%d @@" % (self.old_start, self.old_lines,
                                       self.new_start, self.new_lines)

    def preview(self):
        """One short human line, for `stg list`."""
        want = "-" if self.kind == "delete" else "+"
        for l in self.body:
            if l.startswith(want):
                return want + _clip(l[1:])
        return ""

    def to_dict(self, new_nlines):
        a = self.anchor(new_nlines)
        return {
            "anchor": a,
            "kind": self.kind,
            "old_start": self.old_start,
            "old_lines": self.old_lines,
            "new_start": self.new_start,
            "new_lines": self.new_lines,
            "added": self.added,
            "removed": self.removed,
            "preview": self.preview(),
            "lines": [l[1:] for l in self.body if l[:1] in ("+", "-", " ")],
        }

    def __repr__(self):
        return "<Change %s %s>" % (self.header(), self.kind)


def _clip(s, width=66):
    s = s.replace("\t", " ").rstrip()
    return s if len(s) <= width else s[:width - 1] + "…"


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


def _split_run(group, group_old, group_new):
    """Cut one maximal run of +/- lines into the smallest hunks git will take.

    git writes a hunk's removed lines first and its added lines after, so a run
    of `n` removes followed by `m` adds means: the first `min(n, m)` removes pair
    with the first `min(n, m)` adds, line for line. Cutting there is exactly
    what `git add -p`'s `s` command does, and each piece is a hunk `git apply`
    will take on its own. Any surplus on one side is a pure insertion or a pure
    deletion and cannot be cut further without inventing context.

    A side that consumes no lines still needs a start number: git writes the
    count of the *other* side and anchors the empty side at the line the content
    sits next to. ``@@ -9,0 +10,1 @@`` is an insertion after old line 9, and
    ``@@ -3,2 +2,0 @@`` is a deletion whose following line is new line 2.
    """
    content = [l for l in group if l[:1] in ("+", "-")]
    if not content:
        return []
    marks = {}
    seen = 0
    for line in group:
        if line.startswith("\\"):
            if seen:
                marks[seen - 1] = marks.get(seen - 1, []) + [line]
            continue
        seen += 1

    def take(idxs, old_at, new_at):
        body = []
        nold = nnew = 0
        for i in idxs:
            body.append(content[i])
            body.extend(marks.get(i, []))
            if content[i].startswith("-"):
                nold += 1
            else:
                nnew += 1
        return Change(old_start=group_old + old_at, old_lines=nold,
                      new_start=group_new + new_at, new_lines=nnew,
                      body=body)

    nrem = sum(1 for l in content if l.startswith("-"))
    nadd = len(content) - nrem
    pairs = min(nrem, nadd)
    out = []
    for j in range(pairs):
        # remove j pairs with add j, and each pair is a hunk on its own
        out.append(take([j, nrem + j], j, j))
    if nrem > nadd:
        out.append(take(list(range(nadd, nrem)), nadd, nadd))
    elif nadd > nrem:
        out.append(take(list(range(nrem, nadd)), nrem, nrem))
    return out


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
