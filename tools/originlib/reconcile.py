"""Git-versus-record reconciliation.

Compares the working tree against the session's declared artifacts, so a file
the agent changed but never declared becomes an explicit `unlogged_change` event
instead of a silent gap in the record.

This is what makes "everything is logged" a checkable property rather than a
promise: the failure mode is reported, not prevented.
"""

from __future__ import annotations

from . import events, gitutil, paths

# A mission record is *implicated* by these event kinds. If such an event lands
# but the corresponding record did not change in git, that is an integrity gap
# worth reporting rather than leaving for a reader to notice.
IMPLICATIONS = {
    "decision": ("DECISIONS.md",),
    "experiment_result": ("HYPOTHESES.md", "FAILURES.md"),
    "block": ("STATE.md",),
}


def reconcile(active) -> dict:
    """Compare the working tree against the session's declared artifacts."""
    declared = {
        event.data["path"]
        for event in events.events_for(active.session)
        if event.kind == "artifact" and event.data.get("path")
    }
    changed = gitutil.changed_paths(active.start_head)
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
        "changed": changed,
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
    """Mission records implied by this session's events that did not change."""
    changed = set(gitutil.changed_paths(active.start_head))
    implied: dict[str, set[str]] = {}
    for event in events.events_for(active.session):
        for record in IMPLICATIONS.get(event.kind, ()):
            implied.setdefault(record, set()).add(event.kind)
    return {
        record: sorted(kinds)
        for record, kinds in sorted(implied.items())
        if record not in changed
    }