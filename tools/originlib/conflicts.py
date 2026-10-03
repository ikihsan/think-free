"""Unresolved merge-conflict markers in repository content.

Why this module exists (`FAILURES.md` F013, 2026-10-03): commit `fd7b4a1`
committed three mission records to the shared base with `<<<<<<< HEAD` still in
them. `doc lint` passed, `session verify --strict` passed, and CI was green,
because no gate read file *contents* for markers — only for line count,
metadata, links, and generated-file drift. Three corrupted records then became
the reload point every future session starts from.

The rule is deliberately narrow, because a gate that cries wolf is a gate
people learn to skip:

* Only git's own marker shape counts: exactly seven characters (`<` for an
  opening side, `|` for the diff3 base, `>` for the closing side) at column 0,
  followed by end-of-line or a space and a label. Fewer or more characters, or
  an indented one, is prose — git's `text` merge driver never writes those.
* A line of exactly seven `=` is a marker **only between an opening and a
  closing marker in the same file**. On its own it is ordinary text: an
  underline, a table rule, a separator in an appended command log. Eighty-odd
  such lines exist in `sessions/*/commands.log` and none is a conflict.
* A block with no closing marker, and a closing marker with no block, are both
  reported. The committed corruption in `DECISIONS-GATING.md` had a duplicated
  terminator with nothing open, which a "look for `<<<<<<<`" rule would have
  missed on the file it had already been fixed in.
* Binary and undecodable files are skipped rather than guessed at, for the same
  reason `secrets.scan_file` skips them.

Known limitation, stated rather than implied: a marker indented inside a
fenced code block is not detected. git does not produce one, and treating an
indented example in a document as corruption would be the worse failure.

A file whose *text* must contain a marker at the start of a line — a process
document showing a reader what an unresolved conflict looks like — declares
`origin-allow-conflict-markers` and is reported as `info` rather than skipped
silently. This module and its tests quote the marker mid-sentence, which the
rule correctly ignores, so neither needs the waiver today.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

# git writes seven characters, then a space, then the ref or label.
OPENING = re.compile(r"^<{7}(?:\s.*)?$")
BASE = re.compile(r"^\|{7}(?:\s.*)?$")
CLOSING = re.compile(r"^>{7}(?:\s.*)?$")
SEPARATOR = re.compile(r"^={7}[ \t]*$")
NUL_WINDOW = 8192

# Same shape of waiver as the secret scanner's (D012): declared in the file,
# applies to that file only, and is reported rather than silent. Trailing prose
# is allowed after the name so a file can say why it needs the exception, and
# the line must still begin with a comment marker followed by the exact name.
WAIVER = re.compile(
    r"^[ \t]*(?:#|//|<!--)[ \t]*origin-allow-conflict-markers"
    r"(?:[ \t]*-->|[ \t]*:[^\n]*)?[ \t]*$",
    re.MULTILINE,
)
WAIVER_WINDOW_LINES = 40


@dataclass(frozen=True)
class Finding:
    """One thing wrong with a file, located by 1-based line number."""

    line: int
    detail: str


def scan(text: str) -> list[Finding]:
    """Every unresolved conflict marker in text, in line order.

    A block is reported once, at its opening marker, because it is one mistake
    with one fix and a reader told "lines 20, 21, 22" has to work out that they
    are one thing.

    Every block is reported, including a well-formed one: a complete
    `<<<<<<< / ======= / >>>>>>>` triple is what a committed unresolved conflict
    actually looks like, and a rule that only reported malformed blocks would
    have passed the three files this module exists for. That was the first
    implementation here, and the check against the pre-fix tree is what found
    it (F013).
    """
    findings: list[Finding] = []
    opened: int | None = None
    separated = False
    for number, line in enumerate(text.splitlines(), start=1):
        if OPENING.match(line):
            if opened is not None:
                findings.append(
                    Finding(opened, "unresolved conflict block opens again before it closes")
                )
            opened = number
            separated = False
            continue
        if BASE.match(line):
            # diff3 style puts the common ancestor here, between the opening
            # marker and the divider. It is part of the same block.
            if opened is None:
                opened = number
            continue
        if opened is None:
            if CLOSING.match(line):
                findings.append(Finding(number, "conflict terminator with no open block"))
            continue
        if SEPARATOR.match(line):
            separated = True
        elif CLOSING.match(line):
            detail = (
                f"unresolved conflict block; terminator on line {number}"
                if separated
                else "unresolved conflict block with no ======= divider"
            )
            findings.append(Finding(opened, detail))
            opened = None
            separated = False
    if opened is not None:
        findings.append(Finding(opened, "unresolved conflict block with no terminator"))
    findings.sort(key=lambda item: item.line)
    return findings


def waived(text: str) -> bool:
    """Whether this file declares itself exempt, in its first 40 lines."""
    head = "\n".join(text.splitlines()[:WAIVER_WINDOW_LINES])
    return bool(WAIVER.search(head))


def read_text(path: Path) -> str | None:
    """Text content, or None when the file is binary or undecodable."""
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if b"\x00" in data[:NUL_WINDOW]:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


def scan_file(path: Path) -> tuple[list[Finding], bool]:
    """Findings for one file, and whether a waiver suppressed them."""
    text = read_text(path)
    if text is None:
        return [], False
    return scan(text), waived(text)


def report(files: list[Path], base: Path) -> tuple[list[str], list[str]]:
    """Findings as lint lines: `(violations, infos)`.

    Lives here rather than in `doclint` so the linter keeps its line budget,
    and so this rule can be run over a tree on its own.
    """
    violations: list[str] = []
    infos: list[str] = []
    for path in files:
        found, allowed = scan_file(path)
        rel = path.relative_to(base).as_posix()
        if allowed and found:
            infos.append(
                f"{rel}: {len(found)} unresolved conflict block(s) waived by declaration"
            )
            continue
        for item in found:
            violations.append(f"{rel}:{item.line}: {item.detail}")
    return violations, infos