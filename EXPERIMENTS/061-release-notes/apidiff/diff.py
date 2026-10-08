"""API diff logic for apidiff."""

from __future__ import annotations


def signature_delta(old: dict, new: dict) -> list[str]:
    """How a signature changed. Empty means unchanged."""
    deltas: list[str] = []
    for field in ("required", "optional", "kwonly_required", "kwonly_optional"):
        added = [a for a in new[field] if a not in old[field]]
        removed = [a for a in old[field] if a not in new[field]]
        if added:
            if field in ("required", "kwonly_required"):
                deltas.append(f"required parameter added: {', '.join(added)}")
            else:
                deltas.append(f"optional parameter added: {', '.join(added)}")
        if removed:
            deltas.append(f"parameter removed: {', '.join(removed)}")
    if old["varargs"] != new["varargs"]:
        deltas.append("*args/**kwargs changed")
    return deltas


def diff_api(old: dict, new: dict) -> list[dict]:
    """One record per public API change, classified."""
    changes: list[dict] = []
    for name in sorted(set(old) | set(new)):
        was, now = old.get(name), new.get(name)
        if was is None:
            changes.append({"name": name, "change": "added", "breaking": False,
                            "detail": f"new {now['kind']}"})
            continue
        if now is None:
            hidden = was.get("publicity") == "not-in-__all__"
            changes.append({
                "name": name,
                "change": "removed",
                "breaking": not hidden,
                "detail": f"{was['kind']} removed"
                          + (" (was not in __all__)" if hidden else ""),
            })
            continue
        if was["kind"] != now["kind"]:
            changes.append({"name": name, "change": "kind-changed",
                            "breaking": True,
                            "detail": f"{was['kind']} became {now['kind']}"})
            continue
        if was["kind"] in ("function", "method"):
            deltas = signature_delta(was["signature"], now["signature"])
            if deltas:
                breaking = any(
                    d.startswith(("required parameter added", "parameter removed"))
                    for d in deltas
                )
                changes.append({"name": name, "change": "signature",
                                "breaking": breaking, "detail": "; ".join(deltas)})
            if was.get("async") != now.get("async"):
                changes.append({"name": name, "change": "sync-async",
                                "breaking": True,
                                "detail": "sync became async or vice versa"})
        elif was["kind"] == "class":
            if was["bases"] != now["bases"]:
                changes.append({"name": name, "change": "bases",
                                "breaking": False, "detail": "base classes changed"})
        elif was["kind"] == "reexport":
            if was.get("from") != now.get("from"):
                changes.append({"name": name, "change": "reexport-source",
                                "breaking": False,
                                "detail": f"re-exported from {now.get('from')}"})
    return changes