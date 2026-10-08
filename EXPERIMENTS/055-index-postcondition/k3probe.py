#!/usr/bin/env python3
"""E055 K3 probe: can the caller derive the same verdict from the tool's own output?

KILL-C's K3 asks whether `indexcheck` would be re-reporting something the arm
already said. That is a question about what the tool *prints*, so it is answered by
printing it, not by reasoning about it.

The mechanism is `filterdiff`'s documented `--as-numbered-lines=after`: fed the same
selector, it reports the **absolute new-file line number** of every line the
selection carries, one per line, as `<n>\t:<text>`. Measured on bytes before this
file was written:

    $ git diff -U0 | filterdiff --lines=2 | filterdiff --as-numbered-lines=after
    1	:A
    2	:B

for a file line 2 the caller named, on a hunk that also carries line 1. Those two
lines are the whole post-state: the caller knows from the tool's own output that both
line 1 and line 2 will be replaced, which is exactly the verdict `indexcheck` reaches
from `.git/index`.

Two controls keep this from being a reading rather than a measurement:

- **C5** on a case where the tool *does* over-stage, the reported set must be
  strictly larger than the wanted line. A probe that cannot see an over-stage would
  make K3's negative answer meaningless.
- **C6** on a case where the tool stages exactly the wanted line, the reported set
  must equal it. A probe that reports the wrong set would satisfy C5 by accident.

The probe reads the tool's stdout and never `.git/index`, so it is a statement about
the tool, not a second opinion about the index.
"""

import re

from gitenv import FILTERDIFF, sh

NUMBERED = re.compile(r"^(\d+)\t:(.*)$")


def _lines(stdout):
    return {int(m.group(1)): m.group(2)
            for m in (NUMBERED.match(raw) for raw in stdout.split("\n")) if m}


def carried_lines(repo, want, env=None):
    """What the tool's own `--as-numbered-lines` reports for a `--lines=want` selection.

    Both halves are read, because **neither alone is the selection**:

    - `after` numbers the lines that exist in the new file, so a carried
      **deletion** has no number there and is invisible to it. Measured:
      `--as-numbered-lines=after` on a hunk that replaces line 1 *and deletes*
      line 2 prints `1 :A` and nothing else, while the index loses line 2.
    - `before` numbers the lines that exist in the old file, so a carried
      **addition** has no number there and is invisible to it.

    A caller who wants to know what a selection will do has to read both, so this
    does. Returns (after_lines, before_lines, why, raw) or (None, None, why, raw).
    """
    base = ("git diff -U0 --no-color -- f.txt | %s --lines=%d | %%s "
            "--as-numbered-lines=%%s" % (FILTERDIFF, want))
    got = {}
    raw = []
    for side in ("after", "before"):
        rc, out, err = sh(["bash", "-c", base % (FILTERDIFF, side)], repo, env)
        if rc != 0:
            return None, None, None, "probe pipeline (%s) exited %d: %s" % (
                side, rc, (err or out)[:160]), out
        got[side] = _lines(out)
        raw.append(out)
    joined = "".join(raw)
    said = bool(got["after"] or got["before"])
    return (got["after"], got["before"],
            None if said else "no line was reported for this selection", joined)


def touched(repo_after, want):
    """What the tool's own two reports imply about the index, in one comparison.

    `after` names the new-file lines the selection writes and `before` the old-file
    lines it removes. Both are read here so a carried deletion or a carried addition
    is visible; the caller gets the same information `indexcheck` gives, from the
    tool, without reading `.git/index`.

    `claims_only_the_wanted_line` is K3's question. It is true when the reports name
    no line other than the one the caller asked for, and it is the condition under
    which the tool's own output cannot tell the caller that more changed.
    """
    after, before, why, raw = repo_after
    if after is None:
        return {"saw_any_line": False, "claims_only_the_wanted_line": None,
                "why": why, "raw": (raw or "")[:400]}
    wrote = sorted(after)
    removed = sorted(n for n in before if n not in after)
    extra = sorted(n for n in set(wrote) | set(before) if n != want)
    return {"saw_any_line": bool(after or before),
            "wrote_lines": wrote, "before_lines": sorted(before),
            "removed_old_lines": removed,
            "named_lines_beyond_want": extra,
            "claims_only_the_wanted_line": set(wrote) | set(before) == {want},
            "caller_can_derive_the_verdict": bool(extra),
            "why": why, "raw": (raw or "")[:400]}


def derive_verdict(repo, want, env=None):
    """`carried_lines` then `touched`: does the tool's own output give the verdict?"""
    return touched(carried_lines(repo, want, env), want)
