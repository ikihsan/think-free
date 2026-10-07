"""One addressable change: a maximal run of added/removed lines."""

def _clip(s, width=66):
    s = s.replace("\t", " ").rstrip()
    return s if len(s) <= width else s[:width - 1] + "…"



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

    def to_dict(self, anchor):
        """`anchor` is passed in because a file assigns one line per change and
        the assignment lives on the file, not on the change."""
        return {
            "anchor": anchor,
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
