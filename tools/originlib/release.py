"""Release-manifest enforcement.

`RELEASE-MANIFEST.md` is the authority on which paths are public. Until now it
was maintained by hand and reviewed, so its own preamble said so: *a path listed
as public here is a human claim rather than a machine guarantee*. This module is
that guarantee, and it reads the same two tables rather than a second copy of
them, because a second copy is a second thing to forget.

Six properties, each with a clause that can fail on its own (seeded in
`tests/test_release.py`):

1. **No wildcards.** Manifest rule 1 says a path not listed is not published,
   and a glob would silently publish more than its author read.
2. **Every tracked top-level entry is classified exactly once.** A new root
   file with no row is not a small omission: it decides, by default, whether it
   is public. Seven entries had no row at all before this check existed.
3. **A declared-public path exists, unless it says `pending`.** `LICENSE` is
   declared public and does not exist, which is a real release blocker and must
   be visible rather than assumed. A `pending` path that then appears fails too,
   so the marker cannot outlive its reason.
4. **No public path sits inside an internal directory**, and vice versa. One
   path cannot have two audiences.
5. **No classified path contains a credential shape.** Manifest rule 3 covers
   internal records as well as public ones; the check uses the existing scanner
   rather than a second pattern list.
6. **The front door agrees with the manifest about what exists.** Manifest rule
   4 forbids describing unreleased behaviour as shipped. The decidable part of
   that is agreement: the manifest declares a state, `README.md` must declare
   the same one, and publishing a product means changing both in one commit.

What this does **not** decide, stated here so the guarantee is not read as
broader than it is:

* It does not judge whether the declared state is *true*. A manifest and a
  README that agree on a false claim still pass.
* It does not check prose for accuracy, and it does not read a path's meaning.
* It classifies tracked files. A file that is not tracked is not published and
  is not checked, which is the same rule `docfiles` already uses.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from . import docfiles, paths, secrets
from .finding import Finding

MANIFEST_NAME = "RELEASE-MANIFEST.md"
FRONT_DOOR = "README.md"
STATE_DIRECTIVE = re.compile(r"<!--\s*origin-release-state:\s*(?P<state>[a-z-]+)\s*-->")
KNOWN_STATES = ("no-public-product", "public-product")
PUBLIC_HEADING = re.compile(r"^##\s+Public by default\s*$", re.MULTILINE)
INTERNAL_HEADING = re.compile(r"^##\s+Internal by default\s*$", re.MULTILINE)
PENDING = "pending"
TOKEN = re.compile(r"`([^`]+)`")
TABLE_ROW = re.compile(r"^\|(?P<cells>.+)\|\s*$")
WILDCARDS = ("*", "?", "[", "]")


@dataclass(frozen=True)
class Entry:
    """One declared path and whether it is expected to be absent."""

    path: str
    pending: bool = False

    @property
    def covered(self) -> str:
        """This entry as it may stand in a table cell."""
        return f"`{self.path}`" + (f" ({PENDING})" if self.pending else "")


@dataclass
class Result:
    violations: list[str] = field(default_factory=list)
    infos: list[str] = field(default_factory=list)
    checked: int = 0

    @property
    def ok(self) -> bool:
        return not self.violations

    def render(self) -> str:
        lines = [f"release check: {self.checked} path(s) checked"]
        for note in self.infos:
            lines.append(f"  info  {note}")
        for problem in self.violations:
            lines.append(f"  FAIL  {problem}")
        lines.append("release check: OK" if self.ok else f"release check: {len(self.violations)} violation(s)")
        return "\n".join(lines)


def _section(text: str, heading: re.Pattern[str]) -> str:
    """Body of the first section whose heading matches, up to the next `##`."""
    start = heading.search(text)
    if start is None:
        return ""
    rest = text[start.end() :]
    end = re.search(r"^##\s", rest, re.MULTILINE)
    return rest[: end.start()] if end else rest


def parse_entries(section: str) -> list[Entry]:
    """Declared entries from one manifest table, in document order.

    A path is a backticked token in the row's first cell. Anything else in a
    row is prose, which is how a row can promise a future path without
    classifying one today.
    """
    entries: list[Entry] = []
    for line in section.splitlines():
        row = TABLE_ROW.match(line.strip())
        if row is None:
            continue
        cells = row.group("cells").split("|")
        if not cells or set(cells[0].strip()) <= {"-", " "}:
            continue
        first = cells[0]
        lowered = first.lower()
        pending = PENDING in lowered
        for token in TOKEN.findall(first):
            entries.append(Entry(path=token.strip(), pending=pending))
    return entries


def parse(root: Path | None = None) -> tuple[list[Entry], list[Entry], str]:
    """`(public, internal, declared_state)` from the manifest.

    An unreadable or state-less manifest yields empty lists and an empty state,
    which every check below then reports, rather than an empty pass.
    """
    manifest = (root or paths.repo_root()) / MANIFEST_NAME
    if not manifest.exists():
        return [], [], ""
    text = manifest.read_text(encoding="utf-8")
    state = STATE_DIRECTIVE.search(text)
    return (
        parse_entries(_section(text, PUBLIC_HEADING)),
        parse_entries(_section(text, INTERNAL_HEADING)),
        state.group("state") if state else "",
    )


def _top_level(files: list[Path], base: Path) -> list[str]:
    return sorted({path.relative_to(base).parts[0] for path in files})


def _within(directory: str, path: str) -> bool:
    """Whether `path` sits inside a declared directory. A trailing `/` marks one."""
    return directory.endswith("/") and path != directory and path.startswith(directory)


def _covers(declared: str, entry: str) -> bool:
    """Whether a declared path accounts for a top-level tree entry.

    A declared *file* accounts only for itself. If `a/b.md` classified the whole
    `a/` directory, adding `a/secret.md` would publish it without anyone
    deciding to, which is the failure rule 1 exists to prevent.
    """
    if declared.endswith("/"):
        return declared == entry + "/"
    return declared == entry


def check_no_wildcards(result: Result, public: list[Entry], internal: list[Entry]) -> None:
    for kind, entries in (("public", public), ("internal", internal)):
        for entry in entries:
            bad = [char for char in WILDCARDS if char in entry.path]
            if bad:
                result.violations.append(
                    Finding.at(MANIFEST_NAME, f"{kind} entry `{entry.path}` uses a "
                               "wildcard; rule 1 says a path not listed is not "
                               "published, so a glob publishes more than its "
                               "author read"))


def check_coverage(result: Result, public: list[Entry], internal: list[Entry], entries: list[str]) -> None:
    """Every tracked top-level entry is claimed by exactly one table."""
    for entry in entries:
        is_public = any(_covers(item.path, entry) for item in public)
        is_internal = any(_covers(item.path, entry) for item in internal)
        if is_public and is_internal:
            result.violations.append(
                Finding.at(entry, "classified as both public and internal; a path "
                                  "has one audience"))
        elif not is_public and not is_internal:
            result.violations.append(
                Finding.at(entry, "tracked at the top level but classified by "
                                  "neither manifest table"))


def check_existence(result: Result, public: list[Entry], internal: list[Entry], base: Path) -> None:
    for kind, entries in (("public", public), ("internal", internal)):
        for entry in entries:
            exists = (base / entry.path).exists()
            if entry.pending and exists:
                result.violations.append(
                    Finding.at(entry.path,
                               f"declared {kind} and marked {PENDING}, but it "
                               "exists; drop the marker in the commit that "
                               "creates it"))
            elif not entry.pending and not exists:
                result.violations.append(
                    Finding.at(entry.path,
                               f"declared {kind} but absent; create it or mark it "
                               f"{PENDING} so the absence is a decision rather "
                               "than an oversight"))


def check_containment(result: Result, public: list[Entry], internal: list[Entry]) -> None:
    """One path cannot sit inside a directory declared with the other audience."""
    for entry in public:
        for other in internal:
            if _within(other.path, entry.path):
                result.violations.append(
                    Finding.at(entry.path, "declared public but sits inside "
                                           f"internal `{other.path}`"))
    for entry in internal:
        for other in public:
            if _within(other.path, entry.path):
                result.violations.append(
                    Finding.at(entry.path, "declared internal but sits inside "
                                           f"public `{other.path}`, which "
                                           "publishes it by rule 1"))


def check_secrets(
    result: Result, public: list[Entry], internal: list[Entry], files: list[Path], base: Path
) -> None:
    """Manifest rule 3 covers internal records too, so scan both tables."""
    declared = {item.path.rstrip("/") for item in public + internal}
    for path in files:
        top = path.relative_to(base).parts[0]
        if not any(_covers(item, top) for item in declared):
            continue
        found = secrets.scan_file(path)
        if found:
            result.violations.append(
                Finding.at(path.relative_to(base).as_posix(),
                           f"credential-shaped text ({', '.join(found)}); manifest "
                           "rule 3 forbids it in a published or internal record"))


def check_front_door(result: Result, state: str, base: Path) -> None:
    """The manifest's declared state and the front door must agree."""
    if not state:
        result.violations.append(
            Finding.at(MANIFEST_NAME, "no <!-- origin-release-state: ... --> "
                           "directive, so there is no declared state to check; "
                           f"expected one of {', '.join(KNOWN_STATES)}"))
        return
    if state not in KNOWN_STATES:
        result.violations.append(
            Finding.at(MANIFEST_NAME, f"release state `{state}` is not one of "
                                      f"{', '.join(KNOWN_STATES)}"))
        return
    front = base / FRONT_DOOR
    if not front.exists():
        result.violations.append(
            Finding.at(FRONT_DOOR, "missing, so the front door cannot declare "
                                   "a state"))
        return
    declared = STATE_DIRECTIVE.search(front.read_text(encoding="utf-8"))
    if declared is None:
        result.violations.append(
            Finding.at(FRONT_DOOR, "no <!-- origin-release-state: ... --> "
                                   "directive; it must match the manifest's "
                                   f"`{state}`"))
    elif declared.group("state") != state:
        result.violations.append(
            Finding.at(FRONT_DOOR, f"declares release state "
                                   f"`{declared.group('state')}` but {MANIFEST_NAME} "
                                   f"declares `{state}`; rule 4 requires both to "
                                   "change together"))


def check(root: Path | None = None) -> Result:
    """Every rule, in the order a reader should fix them."""
    base = root or paths.repo_root()
    files = docfiles.tracked_files(base)
    public, internal, state = parse(base)
    result = Result(checked=len(public) + len(internal))
    check_no_wildcards(result, public, internal)
    check_coverage(result, public, internal, _top_level(files, base))
    check_existence(result, public, internal, base)
    check_containment(result, public, internal)
    check_secrets(result, public, internal, files, base)
    check_front_door(result, state, base)
    return result