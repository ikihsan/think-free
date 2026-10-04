"""A command's own write, declared by the bytes it wrote.

Reconciliation reports a file this session changed without declaring it, and the
tooling's own commands change files: `task claim`, `task complete` and
`task release` rewrite a task file's `task-meta` block, and every task command
appends a line to `tasks/CLAIMS.jsonl`. Those writes closed 37 sessions with
exit 4 naming the tooling itself (`observed` 2026-10-04, defect 12).

The declaration is carried by a `task_rewrite` event, which names the path and
the digests of what the command wrote, so the answer depends on the bytes rather
than on the session having declared something. Two shapes, because the files are
different:

* A task file has a `task-meta` block, so the digests are of that block and of
  everything outside it — an agent editing the body afterwards is reported while
  the command's own meta rewrite stays silent.
* An append-only ledger has no such structure, so the digest is of the whole
  file together with its size.

This module owns both shapes so the rule cannot be attached to one command and
missed by the next: `tasks.append_claim` is the only function that appends to the
ledger, and it declares here. The matching half lives in `reconcile`, which
answers whether the tree still holds those bytes.
"""

from __future__ import annotations

import hashlib

# The key that identifies a whole-file declaration, as opposed to a task file's
# two-part one. Reconciliation tells the shapes apart by this key and by nothing
# else — never by a path's name or its extension, which is how the previous rule
# hid every `.json`, `.jsonl` and `.log` edit (defect 12). The task-file shape's
# keys belong to `tasks`, which computes them.
WHOLE_FILE_KEY = "sha256"


def whole_file(path) -> dict:
    """sha256 and size of every byte in `path`.

    Read as bytes rather than as text: the ledger is JSON Lines today, but the
    digest is a claim about the file, and a claim that changes meaning with the
    decoder's newline handling is not a claim.
    """
    data = path.read_bytes()
    return {WHOLE_FILE_KEY: hashlib.sha256(data).hexdigest(), "size": len(data)}


def matches(target, recorded: dict) -> bool:
    """Does `target` still hold exactly the bytes `recorded` names?

    False rather than raising for a file that is gone or unreadable: the caller is
    asking whether a claim about the past still describes the tree, and a missing
    or unparseable file does not.
    """
    from . import tasks

    if not recorded or not target.is_file():
        return False
    if recorded.get(WHOLE_FILE_KEY):
        try:
            current = whole_file(target)
        except OSError:
            return False
        if recorded.get("size") is not None and recorded["size"] != current["size"]:
            return False
        return recorded[WHOLE_FILE_KEY] == current[WHOLE_FILE_KEY]
    return tasks.digests_match(target, recorded)


def record(active, rel: str, data: dict, summary: str, task_id: str = "") -> bool:
    """Append the `task_rewrite` event for one command write. True when it wrote.

    A repeated declaration of bytes already recorded is dropped: `task claim`
    followed by `task complete` writes the file twice, and the second event would
    say nothing the first did not. The check is on the digests rather than on the
    path, so a file edited between the two writes is declared again — which is the
    whole point of declaring bytes instead of a name.
    """
    from . import events

    if active is None:
        # Outside a session there is no record to write into, and inventing one
        # would be a worse lie than the missing entry.
        return False
    for event in events.events_for(active.session):
        if event.kind != "task_rewrite" or event.data.get("path") != rel:
            continue
        if all(event.data.get(key) == data.get(key) for key in data):
            return False
    events.append(
        active.session,
        "task_rewrite",
        {"summary": summary, "path": rel, "task": task_id, **data},
        actor=active.agent,
        host=active.host,
    )
    return True
