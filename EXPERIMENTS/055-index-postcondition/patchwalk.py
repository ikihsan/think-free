#!/usr/bin/env python3
"""E055 Amendment 3: read the arm's *primary* output, which marks carried lines.

`k3probe.py` reads `--as-numbered-lines`, an **optional** report that prints every
line the selection *spans*. Away from `-U0` that list holds context lines beside
carried ones, so the reader cannot tell a carried change from a neighbour the hunk
merely touches — which is what left K3 `not_evaluated` there (`ceiling.py`, C10
falsified).

This reader asks the tool's **primary** output instead: `filterdiff --lines=N`
emits a unified diff, where a carried line is a `+`/`-` body line and a context
line begins with a space. That distinction is present at every context, so the
same question is decidable everywhere.

    $ git diff | filterdiff --lines=2      # a,b,c,d,e -> a,B,c,d,e
    @@ -1,5 +1,5 @@
     a
    -b
    +B
     c

Two controls hold it, both declared in PROTOCOL.md's Amendment 3 and both
adverse to the conclusion:

- **C11** the walk must equal `git diff --cached -U0`'s own statement of what the
  index touches, so this reader is not merely agreeing with `k3probe`.
- **C12** on an exact selection it must report the wanted line and nothing else,
  so it cannot be satisfied by a reader that returns the whole hunk.
"""

import re

from gitenv import FILTERDIFF, ctx_env, sh

HUNK = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")
BODY = re.compile(r"^([+\- ])(.*)$")


def walk(patch):
    """(old_lines, new_lines) the patch carries, read from `+`/`-` markers alone.

    Context lines advance both counters and are deliberately **not** reported:
    reporting them is the defect this module exists to avoid. The `\\ No newline
    at end of file` marker and the trailing empty line git writes after the last
    body line are skipped rather than counted as a context line, because git does
    not number them and counting them would shift every later line.
    """
    old_at = new_at = None
    old, new = set(), set()
    for raw in patch.split("\n"):
        m = HUNK.match(raw)
        if m:
            old_at, new_at = int(m.group(1)), int(m.group(3))
            continue
        if raw.startswith(("--- ", "+++ ", "diff ", "index ", "@@")):
            continue
        if old_at is None or raw.startswith("\\"):
            continue
        if raw == "":
            # Only the terminal empty string is a real line; an empty body line is
            # a context line for a blank line, which git writes as a single space.
            continue
        b = BODY.match(raw)
        if not b:
            continue
        prefix = b.group(1)
        if prefix == "+":
            new.add(new_at)
            new_at += 1
        elif prefix == "-":
            old.add(old_at)
            old_at += 1
        else:
            old_at += 1
            new_at += 1
    return old, new


def selected_patch(repo, want, context=None, env=None):
    """The arm's own stdout: the patch `filterdiff --lines=want` selected.

    The context is passed the way every other arm here receives it, through
    `ctx_env`, so `None` really is git's own default rather than a hard-coded 3.
    """
    e = dict(ctx_env(context))
    e.update(env or {})
    return sh(["bash", "-c", "git diff --no-color -- f.txt | %s --lines=%d"
               % (FILTERDIFF, want)], repo, e)


def carried(repo, want, context=None, env=None):
    """What the tool's own primary output says it carries, and whether it ran."""
    rc, out, err = selected_patch(repo, want, context, env)
    if rc != 0:
        return None, None, "filterdiff --lines=%d exited %d: %s" % (
            want, rc, (err or out)[:160]), out
    old, new = walk(out)
    if not old and not new:
        return old, new, "the selection carried no line", out
    return old, new, None, out


def verdict(carried_result, want):
    """K3's question, asked of the patch markers.

    `claims_only_the_wanted_line` is true when the patch names no line the caller
    did not ask for. `caller_can_derive_the_verdict` is true when it names at
    least one — the caller then knows from the tool's own output that more than
    the wanted line moved, which is what `indexcheck` would have told them by
    reading `.git/index`.
    """
    old, new, why, raw = carried_result
    if old is None:
        return {"saw_any_line": False, "claims_only_the_wanted_line": None,
                "caller_can_derive_the_verdict": None, "why": why,
                "raw": (raw or "")[:400]}
    beyond = sorted((old | new) - {want})
    return {"saw_any_line": bool(old or new),
            "carried_old_lines": sorted(old),
            "carried_new_lines": sorted(new),
            "named_lines_beyond_want": beyond,
            "claims_only_the_wanted_line": (old | new) == {want},
            "caller_can_derive_the_verdict": bool(beyond),
            "why": why, "raw": (raw or "")[:400]}


def derive_verdict(repo, want, context=None, env=None):
    """`carried` then `verdict`, in one call, as `k3probe` presents itself."""
    return verdict(carried(repo, want, context, env), want)
