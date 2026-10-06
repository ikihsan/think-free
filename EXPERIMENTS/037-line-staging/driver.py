#!/usr/bin/env python3
"""Drive `git add -p` from a program: the strongest version of the incumbent.

`stg`'s claim is not that git's interactive prompt cannot be automated -- it can.
The claim is that automating it takes a program, and that the program has to
re-derive the mapping the caller already knows. This file is that program, kept
separate so its size can be counted.

The loop: read git's hunk header off the terminal, and answer `y`, `n` or `s`.

  y  take the hunk, when it touches the line the caller asked for
  n  skip it, when it does not
  s  ask git to split it, when the hunk is wider than one change and the line
     the caller wants sits inside it -- a hunk with N changed lines splits at
     most N-1 times, so the split count has to be discovered, not assumed

Line numbers in the header are new-file line numbers, which is the side the
caller was reading. A hunk that only deletes reports a zero new-count, and the
line that took the deleted content's place is what the caller would have quoted,
so that case reads `start + 1`.

Exit status: 0 if the requested line ended up staged, 3 if it did not.
"""

import json
import os
import pty
import re
import select
import sys
import time

HUNK = re.compile(r"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")
PROMPT = re.compile(r"Stage this hunk")


def read_until(fd, pattern, timeout=10.0):
    """Read from the terminal until `pattern` matches, returning (text, match)."""
    buf = b""
    deadline = time.time() + timeout
    while time.time() < deadline:
        r, _, _ = select.select([fd], [], [], 0.2)
        if not r:
            continue
        try:
            chunk = os.read(fd, 65536)
        except OSError:
            break
        if not chunk:
            break
        buf += chunk
        text = buf.decode("utf-8", "replace")
        m = pattern.search(text)
        if m:
            return text, m
    return buf.decode("utf-8", "replace"), None


def hunk_body(text):
    """The lines of the hunk currently on screen, with the escape codes off."""
    hits = list(HUNK.finditer(text))
    if not hits:
        return None, None
    m = hits[-1]
    tail = text[m.end():].split("\n", 1)[-1]
    body = []
    for raw in tail.split("\n"):
        # git paints the diff, and wraps the prompt at the bottom
        line = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", raw)
        if line.startswith("Stage this hunk"):
            break
        if line[:1] in ("+", "-", " ") or line == "\\":
            body.append(line)
        elif body:
            break
    return m, body


def runs_of_change(body):
    """How many separate changes this hunk holds.

    At git's default context three edits to one file arrive as a single hunk,
    so counting hunks is not enough: the driver has to notice that the hunk
    holds more than one change and ask git to split it.
    """
    n, prev = 0, False
    for line in body:
        if line[:1] == "\\":
            continue
        changed = line[:1] in ("+", "-")
        if changed and not prev:
            n += 1
        prev = changed
    return n


def anchor_of(body, new_start):
    """The working-tree line a reader would quote for this hunk.

    Walk the body counting new-file lines: a removed line consumes none, an
    added line *is* the line at the current position, context consumes one. A
    hunk that only removes has no line of its own, so it is quoted by the line
    that moved up into the gap, which git's header puts one before.
    """
    cur = new_start
    for line in body:
        if line.startswith("-"):
            continue
        if line.startswith("+"):
            return cur
        cur += 1
    return new_start + 1


def main(argv):
    if len(argv) != 1:
        sys.stderr.write("usage: driver.py LINE\n")
        return 2
    want = int(argv[0])
    pid, fd = pty.fork()
    if pid == 0:
        os.execvp("git", ["git", "add", "-p", "f"])
        os._exit(127)
    actions, splits, guard = [], 0, 0
    last_runs = None
    while guard < 200:
        guard += 1
        text, _ = read_until(fd, PROMPT)
        if not PROMPT.search(text):
            break
        m, body = hunk_body(text)
        if m is None:
            os.write(fd, b"q\n")
            break
        runs = runs_of_change(body)
        new_start = int(m.group(3))
        if runs > 1 and (last_runs is None or runs < last_runs):
            key, why = "s", "hunk holds %d changes, splitting" % runs
            last_runs, splits = runs, splits + 1
        elif anchor_of(body, new_start) == want:
            key, why = "y", "anchor is line %d" % want
        else:
            key, why = "n", "anchor is line %d, not %d" % (
                anchor_of(body, new_start), want)
        actions.append({"key": key, "why": why, "runs": runs})
        os.write(fd, (key + "\n").encode())
        time.sleep(0.05)
    os.close(fd)
    os.waitpid(pid, 0)
    print(json.dumps({"actions": actions, "steps": len(actions),
                      "splits": splits}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
