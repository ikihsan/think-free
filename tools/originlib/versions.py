"""Whether the suite has been exercised on the versions this VM is running.

`doctor` answers "can this machine do the work", and it prints the interpreter and
git it found. Until now that was the whole of it: the numbers were reported and
never compared against the two records of what the suite has actually run on —
`tests/git-versions.json` and `tests/python-versions.json`. So a VM on Python
3.9 looked exactly like one on 3.8.10 in the report, and the only way to learn
the difference was to open the record by hand.

Three states, and the distinction is the point:

- **exercised** — some entry names this version. Not "supported": an entry's own
  `scope` says how much of the suite that version ran, and a version that ran an
  older suite is reported with its scope so the reader can weigh it.
- **unrecorded** — the record was read and does not name this version. This is
  the state that matters: the VM is running something no run has ever covered.
- **unreadable** — the record is missing or does not parse. Distinct from
  *unrecorded* on purpose, because a check that cannot tell "we looked and it is
  not there" from "we could not look" reports a confident answer in both cases
  (D030, and the same reasoning D025 requires of every gate here).

Matching is by version string, not by minor version. The records mix patch-level
entries (`3.8.10`, `2.25.1`) with a minor-level one (`3.12`, CI's pin), so a
prefix match is what makes `3.12.7` find CI's `3.12` entry. That is deliberate
and it is a weaker claim than equality, which is why the entry's own `scope` is
carried into the result rather than summarised away — and, since T-0034 gave one
record two environments per minor version, so is the entry's own `where`. A
report that says `exercised` without saying *where that ran* is a claim about
this machine that the record cannot support.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field

from . import paths

# The two records, by the tool whose version they cover. `tool` is the key under
# `doctor`'s `versions` mapping, so a record and a tool cannot drift apart
# silently: an unknown tool has no record and is reported as such.
RECORDS = {
    "python3": ("tests/python-versions.json", "python"),
    "git": ("tests/git-versions.json", "git"),
}

EXERCISED = "exercised"
UNRECORDED = "unrecorded"
UNREADABLE = "unreadable"

# `git version 2.25.1`, `Python 3.8.10`, `Python 3.12.15 (main, ...)`.
VERSION_TOKEN = re.compile(r"(\d+\.\d+(?:\.\d+)?)")


@dataclass
class Match:
    """One tool's version against the record that covers it."""

    tool: str
    version: str = ""
    state: str = UNRECORDED
    record: str = ""
    scope: str = ""
    matched: str = ""
    detail: str = ""
    where: str = ""
    entries: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {
            "tool": self.tool,
            "version": self.version,
            "state": self.state,
            "record": self.record,
            "scope": self.scope,
            "matched": self.matched,
            "where": self.where,
            "detail": self.detail,
            "entries": sorted(self.entries),
        }


def extract_version(output: str) -> str:
    """The first version-looking token in a `--version` line."""
    match = VERSION_TOKEN.search(output or "")
    return match.group(1) if match else ""


def _load(relative: str) -> tuple[dict | None, str]:
    """Read one record. `(None, why)` when it cannot be used."""
    path = paths.repo_root() / relative
    if not path.exists():
        return None, f"{relative} is absent"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, f"{relative} did not parse: {exc}"
    if not isinstance(data.get("verified"), list):
        return None, f"{relative} has no verified list"
    return data, ""


def compare(tool: str, version: str, root=None) -> Match:
    """Compare one tool's version against the record that covers it.

    An unknown tool is `unrecorded` with the reason in `detail`: the tooling
    probes five binaries and only two have records, and pretending otherwise
    would report a gap where there is only no claim.
    """
    if tool not in RECORDS:
        return Match(tool=tool, version=version, state=UNRECORDED, detail="no record covers this tool")
    relative, key = RECORDS[tool]
    match = Match(tool=tool, version=version, record=relative)
    data, why = _load(relative)
    if data is None:
        match.state = UNREADABLE
        match.detail = why
        return match
    entries = [entry for entry in data["verified"] if isinstance(entry, dict) and entry.get(key)]
    match.entries = [str(entry[key]) for entry in entries]
    # Longest recorded version first. Both `3.12.15` and a bare `3.12` match a
    # VM reporting `3.12.15`, and only the specific entry says what that
    # interpreter actually ran — iterating in file order returned whichever came
    # first, which is a coin toss on record layout rather than a decision.
    for entry in sorted(entries, key=lambda item: -len(str(item[key]))):
        recorded = str(entry[key])
        # Dotted-prefix match only: `2.25` must not match `2.250.1`.
        if version == recorded or version.startswith(recorded + ".") or recorded.startswith(version + "."):
            match.state = EXERCISED
            match.matched = recorded
            match.scope = str(entry.get("scope", ""))
            # Which environment that entry describes. A VM reading `exercised`
            # needs to know which run that was: with one record covering seven
            # minors from two environments (a portable build on a VM, and a CI
            # row), a matched patch-level entry can shadow the minor-level CI
            # entry, and "exercised" would then describe somebody else's machine.
            match.where = str(entry.get("where", ""))
            return match
    match.state = UNRECORDED
    match.detail = f"no entry in {relative} names {version or '(no version reported)'}"
    return match


def compare_all(versions: dict, root=None) -> list[Match]:
    """Every probed tool that has a record, plus the ones that do not.

    Tools without a record are included deliberately: `node`, `rustc` and `gcc`
    are probed and are not covered by any suite record, and saying so is more
    honest than leaving them out of a comparison that claims to be complete.
    """
    out = []
    for tool in sorted(set(versions) | set(RECORDS)):
        info = versions.get(tool, {})
        out.append(compare(tool, extract_version(str(info.get("version", "")))))
    return out


def summarize(matches: list[Match]) -> list[str]:
    """One line per tool, naming the record consulted and the scope matched."""
    lines = []
    for match in matches:
        if match.state == EXERCISED:
            note = f"exercised ({match.record}: {match.matched})"
            if match.scope:
                note += f"; {match.scope}"
            if match.where:
                note += f"; run on {match.where}"
        elif match.state == UNREADABLE:
            note = f"record unreadable - {match.detail}"
        elif match.record:
            note = f"NOT exercised - {match.detail}"
        else:
            note = f"no record - {match.detail}"
        lines.append(f"versions {match.tool:<9} {match.version or '(none)':<10} {note}")
    return lines