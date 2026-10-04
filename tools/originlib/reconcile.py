"""Git-versus-record reconciliation.

Compares the working tree against the session's declared artifacts, so a file
the agent changed but never declared becomes an explicit `unlogged_change` event
instead of a silent gap in the record.

This is what makes "everything is logged" a checkable property rather than a
promise: the failure mode is reported, not prevented.
"""

from __future__ import annotations

from . import events, landed, paths

# A mission record is *implicated* by these event kinds. If such an event lands
# but the corresponding record did not change in git, that is an integrity gap
# worth reporting rather than leaving for a reader to notice.
#
# Each entry is (mode, records):
#
#   "all"  every record must change. An experiment result has to reach both the
#          hypothesis record and the failure record; weakening that to "either"
#          would let a disproved candidate be recorded in only one place.
#   "any"  at least one record must change, and the report names records[0].
#          The decision log is split by invariant across five files, so the
#          event cannot say which entry was written and demanding all five
#          would report a gap on every correct session.
IMPLICATIONS = {
    "decision": (
        "any",
        (
            "DECISIONS.md",
            "DECISIONS-PRACTICE.md",
            "DECISIONS-FOUNDATION.md",
            "DECISIONS-SCREENING.md",
            "DECISIONS-GATING.md",
            "DECISIONS-SESSIONS.md",
        ),
    ),
    "experiment_result": ("all", ("HYPOTHESES.md", "FAILURES.md")),
    "block": ("all", ("STATE.md",)),
}


def reconcile(active) -> dict:
    """Compare the working tree against the session's declared artifacts.

    `own` is what this session changed and `landed` is what it merely brought in
    from the shared base. Both are reported: an excluded path is the one an
    operator would want explained, so it is printed rather than dropped.
    """
    declared = {
        event.data["path"]
        for event in events.events_for(active.session)
        if event.kind == "artifact" and event.data.get("path")
    }
    landed_paths = landed.landed_paths(active.session)
    changed = landed.session_changes(active)
    unlogged = [
        rel
        for rel in changed
        if rel not in declared and not _is_own_session_file(active, rel)
    ]
    for rel in unlogged:
        events.append(
            active.session,
            "unlogged_change",
            {
                "summary": f"changed but never declared as an artifact: {rel}",
                "path": rel,
            },
            actor=active.agent,
            host=active.host,
        )
    missing = sorted(p for p in declared if not (paths.repo_root() / p).exists())
    for rel in missing:
        events.append(
            active.session,
            "integrity_error",
            {
                "summary": f"declared artifact no longer exists: {rel}",
                "path": rel,
                "action": "artifact-missing",
            },
            actor=active.agent,
            host=active.host,
        )
    return {
        "declared": sorted(declared),
        "own": changed,
        "landed": sorted(landed_paths),
        "unlogged": unlogged,
        "missing": missing,
    }


GENERATED_MARK = "generated-by: origin"


def _is_own_session_file(active, rel: str) -> bool:
    """Bookkeeping the tooling maintains, not work the session produced.

    Without this, regenerating an index during a session would be reported as
    an undeclared change, which would train readers to ignore the report.
    """
    if rel == "sessions/active.json":
        return True
    if rel.startswith(f"sessions/{active.session}/"):
        return True
    if _is_generated(rel):
        return True
    return _is_vendored(rel)


def _is_vendored(rel: str) -> bool:
    """Vendored content is covered by hash verification, not by declaration.

    `origin skills verify` compares every vendored file against the recorded
    digest, which is a stronger check than an artifact event. Declaring 89 files
    per vendor update would add noise without adding assurance.
    """
    from .doclint import declared_exemptions, is_exempt

    return is_exempt(rel, declared_exemptions())


def _is_generated(rel: str) -> bool:
    target = paths.repo_root() / rel
    if not target.is_file():
        return False
    try:
        with open(target, "r", encoding="utf-8", errors="replace") as handle:
            return GENERATED_MARK in handle.read(2048)
    except OSError:
        return False


def doc_implications(active) -> dict[str, list[str]]:
    """Mission records implied by this session's events that did not change.

    Each event kind carries its own mode: "any" reports one gap naming the group
    when nothing in it moved, "all" reports one gap per record that did not.

    A record another VM landed does not discharge this session's obligation, so
    the same attribution rule applies here: only this session's own changes count.
    """
    changed = set(landed.session_changes(active))
    triggered: dict[str, set[str]] = {}
    for event in events.events_for(active.session):
        implication = IMPLICATIONS.get(event.kind)
        if implication:
            triggered[event.kind] = set(implication[1])
    gaps: dict[str, list[str]] = {}
    for kind, records in triggered.items():
        mode, group = IMPLICATIONS[kind]
        if mode == "any":
            if any(record in changed for record in records):
                continue
            gaps[group[0]] = [kind]
            continue
        for record in sorted(records - changed):
            gaps[record] = sorted(gaps.get(record, []) + [kind])
    return gaps