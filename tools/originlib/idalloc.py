"""Identifiers are allocated from the shared base, never from this working tree.

F, D and T numbers are how this repository refers to its own findings, decisions
and tasks, so a number that means two things breaks a reference rather than
looking untidy: twelve times between 2026-10-03 and 2026-10-04 two VMs took the
same number, and each repair was a renumbering commit. The evidence is dated -
`83aa9a4` and `569a7ce` each added a different `tasks/T-0024-*.md`, and this
VM's own task went through T-0026, T-0027, T-0028 and T-0029 before it was
published. A working tree is one VM's opinion of the ledger; the remote is the
ledger.

What is read, and why:

- **T** from the task files *and* `tasks/CLAIMS.jsonl`. A withdrawn task must
  not hand its number to the next one, because claims and session records refer
  to it by number.
- **F** from `## Fnnn` definitions and `| Fnnn |` rows in the root `FAILURES*`
  files. A row with no definition is an allocated number too, and that is the
  state a half-finished renumbering leaves behind.
- **D** from `## Dnnn` definitions and the spans in `DECISIONS*`, which declare
  both endpoints of everything they cover.

Every error is conservative in the safe direction: a number only *mentioned* in
prose is ignored, and a number defined anywhere is never reused.

The ceiling, stated rather than implied: this narrows the window to two VMs
allocating between their own fetches. Two reads cannot be made atomic by
reading either of them. The other half of the fix - a gate that refuses a commit
defining one identifier twice - is T-0030.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from . import gitutil, paths, sync

# Widths differ because the kinds were born apart: tasks were numbered in a
# template, findings in a table, decisions in a split log.
PREFIX = {"T": "T-", "F": "F", "D": "D"}
WIDTH = {"T": 4, "F": 3, "D": 3}
FAILURE_FILES = re.compile(r"^FAILURES[^/]*\.md$")
DECISION_FILES = re.compile(r"^DECISIONS[^/]*\.md$")
TASK_FILE = re.compile(r"^tasks/(T-(\d{4})-[^/]*\.md)$")
LEDGER_TASK = re.compile(r'"task"\s*:\s*"T-(\d{4})"')
DEFINITION = {"F": re.compile(r"^##\s+F(\d{3})\b"), "D": re.compile(r"^##\s+D(\d{3})\b")}
# A table row, an index row, or an index span: `| F010 | ... |`, `| D024-D029 |`.
NUMBERED_CELL = {"F": re.compile(r"F(\d{3})"), "D": re.compile(r"D(\d{3})")}
DOCUMENTS = {"F": FAILURE_FILES, "D": DECISION_FILES}


class AllocationError(RuntimeError):
    """Raised for an unknown identifier kind. Maps to exit code 1."""


@dataclass
class Allocation:
    """One number, and the record of what it was read from.

    `remote_read` and `fetched` are separate fields on purpose. Three states are
    distinguishable, and a caller that collapses them reports a confident number
    in every one (D030): a base that was read and is current; a base that was
    read but could not be refreshed, so the number may already be stale; and a
    base that could not be read at all.
    """

    kind: str
    next_id: str
    highest: int
    local_highest: int = 0
    remote_ref: str = ""
    remote_sha: str = ""
    remote_highest: int = 0
    remote_read: bool = False
    fetched: bool = True
    unreachable: str = ""
    defined: list[str] = field(default_factory=list)

    def label(self, number: int) -> str:
        return f"{PREFIX[self.kind]}{number:0{WIDTH[self.kind]}d}"

    def source(self) -> str:
        """One line saying which record the number was read from."""
        if not self.remote_ref:
            return "this working tree only (no shared base configured)"
        if not self.remote_read:
            reason = self.unreachable or "not read"
            return f"this working tree only ({self.remote_ref} unread: {reason})"
        base = f"{self.remote_ref}@{self.remote_sha[:7]}"
        if not self.fetched:
            reason = self.unreachable or "not refreshed"
            return f"{base}, last seen before a fetch failed ({reason}), and this working tree"
        return f"{base} and this working tree (highest {self.label(self.highest)})"

    def as_dict(self) -> dict:
        return {
            "kind": self.kind,
            "next_id": self.next_id,
            "highest": self.highest,
            "local_highest": self.local_highest,
            "remote_ref": self.remote_ref,
            "remote_sha": self.remote_sha,
            "remote_highest": self.remote_highest,
            "remote_read": self.remote_read,
            "fetched": self.fetched,
            "unreachable": self.unreachable,
            "defined": sorted(self.defined),
            "source": self.source(),
        }


# ------------------------------------------------------------------ the ref


def base_ref() -> str:
    """The shared base branch as the remote names it, or "" with no remote."""
    remote = sync.remote_name()
    return f"{remote}/{sync.base_branch()}" if remote else ""


def ref_exists(ref: str) -> bool:
    return bool(ref) and gitutil.run(["rev-parse", "--verify", "--quiet", ref]).returncode == 0


def tracked_at(ref: str) -> list[str]:
    """Every path git records at `ref`, in one `ls-tree` call."""
    result = gitutil.run(["ls-tree", "-r", "--name-only", ref])
    return [line.strip() for line in result.stdout.splitlines()] if result.returncode == 0 else []


def text_at(ref: str, path: str) -> str:
    return gitutil.text(["show", f"{ref}:{path}"])


# --------------------------------------------------------------- the readers


def _numbers(text: str, kind: str) -> set[int]:
    """Defined and listed numbers in one document.

    Headings and table rows count. Prose does not: a sentence that says "see
    F010" refers to a number someone else allocated, and treating a citation as
    an allocation would make the allocator drift upward with every citation.
    """
    found: set[int] = set()
    definition = DEFINITION[kind]
    cell = NUMBERED_CELL[kind]
    for line in text.splitlines():
        match = definition.match(line)
        if match:
            found.add(int(match.group(1)))
        elif line.lstrip().startswith("|"):
            found.update(int(number) for number in cell.findall(line))
    return found


def _task_numbers_at(ref: str) -> set[int]:
    numbers: set[int] = set()
    for path in tracked_at(ref):
        match = TASK_FILE.match(path)
        if match:
            numbers.add(int(match.group(2)))
        elif path == "tasks/CLAIMS.jsonl":
            numbers.update(int(n) for n in LEDGER_TASK.findall(text_at(ref, path)))
    return numbers


def _doc_numbers_at(ref: str, kind: str) -> set[int]:
    pattern = DOCUMENTS[kind]
    numbers: set[int] = set()
    for path in tracked_at(ref):
        if pattern.match(path):
            numbers |= _numbers(text_at(ref, path), kind)
    return numbers


def _task_numbers_local() -> set[int]:
    directory = paths.tasks_dir()
    numbers: set[int] = set()
    for path in directory.iterdir() if directory.exists() else []:
        match = TASK_FILE.match(f"tasks/{path.name}")
        if match and path.is_file():
            numbers.add(int(match.group(2)))
    ledger = paths.claims_file()
    if ledger.exists():
        numbers.update(int(n) for n in LEDGER_TASK.findall(ledger.read_text(encoding="utf-8", errors="replace")))
    return numbers


def local_numbers(kind: str) -> set[int]:
    """Every number this working tree defines, committed or not.

    Uncommitted definitions count: the number a VM is about to commit is one it
    must not hand out a second time.
    """
    kind = kind.upper()
    if kind == "T":
        return _task_numbers_local()
    root = paths.repo_root()
    pattern = DOCUMENTS[kind]
    numbers: set[int] = set()
    for path in sorted(root.glob("*.md")):
        if pattern.match(path.name):
            numbers |= _numbers(path.read_text(encoding="utf-8", errors="replace"), kind)
    return numbers


def remote_numbers(kind: str, ref: str) -> set[int]:
    """Every number the shared base defines at `ref`."""
    kind = kind.upper()
    return _task_numbers_at(ref) if kind == "T" else _doc_numbers_at(ref, kind)


# ---------------------------------------------------------------- allocation


def _fetch_failure() -> str:
    result = gitutil.run(["fetch", "--quiet", sync.remote_name()])
    said = (result.stderr or "") + (result.stdout or "")
    if result.returncode == 0:
        return ""
    first = next((line.strip() for line in said.splitlines() if line.strip()), "")
    return first[:140] if first else f"fetch exited {result.returncode}"


def allocate(kind: str, ref: str = "", fetch: bool = True) -> Allocation:
    """The next free number of `kind`, read from the shared base when there is one.

    Fetches first when a remote exists and no ref was named, because a stale
    remote-tracking ref is exactly the defect this replaces: the previous
    allocator read a tree that could be hours behind with no way to tell.
    """
    kind = (kind or "").strip().upper()
    if kind not in WIDTH:
        known = ", ".join(PREFIX[name].rstrip("-") for name in ("T", "F", "D"))
        raise AllocationError(f"unknown identifier kind {kind or '(none)'}; this repository numbers {known}")
    remote_ref = ref or base_ref()
    fetched = True
    unreachable = ""
    if remote_ref and fetch and not ref:
        failure = _fetch_failure()
        fetched = not failure
        unreachable = failure
    local = local_numbers(kind)
    remote: set[int] = set()
    remote_sha = ""
    read = False
    if remote_ref and ref_exists(remote_ref):
        remote = remote_numbers(kind, remote_ref)
        remote_sha = gitutil.text(["rev-parse", remote_ref])
        read = True
    elif remote_ref:
        fetched = False
        unreachable = unreachable or f"{remote_ref} is not fetched"
    everything = local | remote
    highest = max(everything) if everything else 0
    allocation = Allocation(
        kind=kind,
        next_id="",
        highest=highest,
        local_highest=max(local) if local else 0,
        remote_ref=remote_ref,
        remote_sha=remote_sha,
        remote_highest=max(remote) if remote else 0,
        remote_read=read,
        fetched=fetched,
        unreachable=unreachable,
        defined=sorted(f"{PREFIX[kind]}{n:0{WIDTH[kind]}d}" for n in everything),
    )
    allocation.next_id = allocation.label(highest + 1)
    return allocation


def next_identifier(kind: str, ref: str = "", fetch: bool = True) -> str:
    return allocate(kind, ref, fetch).next_id