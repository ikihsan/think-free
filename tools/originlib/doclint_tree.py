"""The rules that decide from the repository as a whole, not from one file.

Split out of `doclint` on 2026-10-04 (T-0040) when that module reached 299 of
the 300 permitted lines and the `Finding` conversions had nowhere to go. The
division is by what a rule may read, which is the property that decides whether
it can also be run on its own:

* `doclint.py` holds the rules whose verdict comes from a single file: the line
  cap, `origin-meta`, and links. Each one is handed a path and returns a
  sentence about that path.
* this module holds the rules whose verdict comes from comparing files with
  each other, or from the mission record as a whole: orphans (nothing links to
  this document), generated freshness (a committed file against what its
  generator produces now), merge-conflict markers (one file's bytes), and the
  identifier record (findings, decisions, tasks and the defect list, which is
  the case that ended in defect 10 and T-0036).

A rule here cannot be checked by looking at the file it names. That is the whole
of D025's subject: three mission records reached the shared base holding conflict
markers while five rules read each of those files and reported nothing, and a
sixth rule did not read the defect list at all, so two VMs took defect 7 in the
same hour. Reading the record is this module's job, and keeping it separate is
what makes it visible that a rule is missing from both sides.
"""

from __future__ import annotations

from pathlib import Path

from . import conflicts, paths
from .finding import Finding

GENERATED_MARK = "<!-- generated-by:"


def events_all() -> list[str]:
    from . import events

    return events.all_sessions()


def active_session_id() -> str | None:
    from .activestate import load_active

    active = load_active()
    return active.session if active else None


def docindex_render() -> str:
    from . import docindex

    return docindex.render()


def check_orphans(result, files: list[Path], globs: list[str]) -> None:
    """Every Markdown file must be referenced by some other Markdown file.

    Exempt paths are skipped: vendored upstream material is not this
    repository's document graph and its internal files are not ours to link.
    """
    from .doclint import is_exempt

    base = paths.repo_root()
    docs = [
        p
        for p in files
        if p.suffix == ".md"
        and not is_exempt(p.relative_to(base).as_posix(), globs)
    ]
    haystack: list[tuple[str, str]] = []
    for path in docs:
        rel = path.relative_to(base).as_posix()
        haystack.append((rel, path.read_text(encoding="utf-8", errors="replace")))
    for path in docs:
        rel = path.relative_to(base).as_posix()
        text = dict(haystack)[rel]
        if GENERATED_MARK in text:
            continue
        stem = Path(rel).with_suffix("").as_posix()
        referenced = any(
            (rel in other or stem in other or Path(rel).name in other)
            for other_rel, other in haystack
            if other_rel != rel
        )
        if not referenced:
            result.violations.append(
                Finding.at(
                    rel, "orphan document; no other document links to it"
                )
            )


def check_generated(result) -> None:
    """Committed generated files must equal what the generators produce."""
    from . import report, tasks

    comparisons: list[tuple[Path, str]] = []
    # The active session is still being written to, so its report cannot be
    # final by definition. `session finish` regenerates it as its last act.
    active = active_session_id()
    for session in events_all():
        if session == active:
            continue
        comparisons.append((paths.session_report(session), report.render_session_report(session)))
    comparisons.append((paths.sessions_index(), report.render_sessions_index()))
    comparisons.append((paths.docs_index(), docindex_render()))
    comparisons.append((paths.tasks_index(), tasks.render_tasks_index()))
    for path, expected in comparisons:
        rel = path.relative_to(paths.repo_root()).as_posix()
        if not path.exists():
            result.violations.append(Finding.at(rel, "generated file missing"))
            continue
        actual = path.read_text(encoding="utf-8")
        if actual != expected:
            result.violations.append(
                Finding.at(
                    rel,
                    "generated file is stale; run 'tools/origin doc index'",
                )
            )


def check_conflicts(result, files: list[Path]) -> None:
    """No tracked file may still hold an unresolved merge conflict.

    Nothing else in this linter reads contents for anything but shape, which is
    why a conflicted file could be committed and pass every gate. A file that
    declares `origin-allow-conflict-markers` is reported as `info` rather than
    silently skipped, so a waiver cannot hide.
    """
    violations, infos = conflicts.report(files, paths.repo_root())
    result.violations.extend(violations)
    result.infos.extend(infos)


def check_identifiers(result) -> None:
    """No identifier may mean two things, and no index row may lack a body.

    Scoped to the mission record rather than to the tracked file list, because
    the property is about that record as a whole: two files each defining
    `F010` is one collision, not two findings. `idcheck` is the one entry point
    both gates read, so `sync land` sees exactly what is seen here (T-0036).
    """
    from . import idcheck

    for line in idcheck.report(paths.repo_root()):
        # The prefix is for the human reading the report; the location is the
        # one `idcheck` read, carried through rather than re-derived. Wrapping
        # without it is how the first run of this emitted an annotation that
        # named no file at all — the kill gate in T-0040 said that is dead.
        result.violations.append(
            Finding(
                f"identifier collision: {line}",
                getattr(line, "path", ""),
                getattr(line, "line", 0),
            )
        )