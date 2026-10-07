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
        self._anchors = None      # filled in by anchors(), once per file

    @property
    def binary(self):
        """git prints no `+++` line for a binary file, only this."""
        return any(l.startswith("Binary files ") or l.startswith("GIT binary")
                   for l in self.header)

    def anchors(self):
        """change -> the line that names it, one line per change where possible.

        A deletion has no line of its own: it is anchored to the line whose
        content moved up, which is the next line in the file as it reads now.
        That fallback can collide -- an insertion landing on exactly that line
        gives one coordinate two changes, and `stg f:80` then staged an 8-line
        deletion *and* a 1-line insertion while printing the coordinate twice.
        Real commit, real corpus, `EXPERIMENTS/046-real-changes`.

        So a deletion keeps its documented address -- the line whose content moved
        up -- and only moves to the line above when that line is already spoken
        for. Changes that occupy a line claim it first, because a line on disk is
        evidence of what is there.
        """
        if self._anchors is None:
            self._anchors = {}
            taken = set()
            for c in self.changes:
                if c.kind == "delete":
                    continue
                a = max(1, c.new_start)
                if a not in taken:
                    self._anchors[id(c)] = a
                    taken.add(a)
            for c in self.changes:
                if c.kind != "delete":
                    continue
                n = self.new_nlines
                preferred = c.anchor(n)
                free = [x for x in (preferred, c.new_start)
                        if 1 <= x <= n and x not in taken]
                a = free[0] if free else preferred
                while a in taken and a > 1:
                    a -= 1
                self._anchors[id(c)] = a
                taken.add(a)
        return self._anchors

    def anchor_of(self, change):
        return self.anchors().get(id(change)) or change.anchor(self.new_nlines)

    def select(self, lo, hi):
        """Select changes that intersect the line range [lo, hi].

        When lo == hi (a specific line is requested), changes that span
        multiple lines are split so only the requested line is included, and at
        most one change is returned: a coordinate that names two changes is not
        an address. When lo < hi (a line range), the full changes intersecting
        the range are returned, as before.
        """
        result = []
        for c in self.changes:
            if not (lo <= self.anchor_of(c) <= hi):
                continue
            if lo == hi and c.new_lines > 1:
                # Split multi-line change: only include the portion
                # up to and including the requested line lo.
                # The change's anchor is its first line (new_start).
                # Line lo is at position (lo - new_start + 1) within the change.
                n = lo - c.new_start + 1  # 1-indexed position
                n = max(1, min(n, c.new_lines, len(c.body)))
                # Take only the first n body lines
                c.new_lines = n
                c.body = c.body[:n]
            result.append(c)
        if lo == hi and len(result) > 1:
            occupying = [c for c in result if c.kind != "delete"]
            result = occupying[:1] if occupying else result[:1]
        return result

    def render(self, changes):
        """A patch `git apply --unidiff-zero` will accept for exactly these.

        Two renderings, because git does not accept one patch shape for both
        situations and the difference is not cosmetic:

        - **A tracked file.** One hunk per change, as written.
        - **A new file** (`git add -N` has put an empty index entry in place).
          Two changes apply at once here. Naming `/dev/null` makes git refuse the
          patch outright -- `fresh.py: already exists in index`, exit 2 -- which is
          why every line of every new file used to be unreachable. Naming the path
          on both sides turns the patch into an edit of that empty entry, which git
          accepts. But separate hunks are then wrong: each carries `-0,0` and
          `+N,1`, and applied together they land in reverse, so `split --all` on a
          three-line new file staged `three two one`. One hunk carrying every
          selected line, in order, is the shape git agrees with.

        Measured over 435 addresses of 15 real file-creation commits in three
        repositories in `EXPERIMENTS/046-real-changes`.
        """
        creating = any(l.startswith("--- /dev/null") for l in self.header)
        out = []
        for line in self.header:
            if line.startswith("index "):
                # a stale blob hash makes git apply reject the patch
                continue
            if line.startswith("--- /dev/null"):
                out.append("--- a/" + self.path + "\n")
                continue
            out.append(line + "\n")
        if creating:
            added = [l for c in changes for l in c.body]
            out.append("@@ -0,0 +1,%d @@\n" % len(added))
            out.extend(l + "\n" for l in added)
            return "".join(out)
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
