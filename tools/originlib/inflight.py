"""Is an unfinished session still live, or has it been abandoned?

`session verify --strict` exists because a crashed run must not look successful
(D013). Its premise, "on a pushed commit nothing is in flight", is false for a
fleet that shares one base branch: `task claim` requires HEAD to equal the
remote base before it publishes a claim, so a claiming VM must push its session
start first. On 2026-10-03 that made every push on every VM red at the session
gate while one honest session was open.

So the gate cannot ask "is any session unfinished?" — that is true whenever the
fleet is working. It has to ask "is any session unfinished *and* provably still
being worked on?". This module answers that from the tree alone, with no
network and no new state:

    1. the `session_start` names a task, so the record says what work is open;
    2. that task file exists and its status is `claimed`;
    3. the claim on that task identifies *this* session — by `claim-session`,
       or, where no session was recorded, by `claim-agent` plus `claim-vm`
       matching the event's `actor` and `host`;
    4. the last entry for that task in `tasks/CLAIMS.jsonl` still opens a claim
       (`claim` or `takeover`) rather than closing one;
    5. the claim is younger than the lease.

Clause 1 is not mandatory on its own. `--task` is optional on `session start`
and a session may claim work without one, so a claim in the ledger that names
the session is accepted instead (see `_claim_naming`). That exception was not
designed; it was forced by the live record, where a real session on the other VM
read as abandoned while it was demonstrably working.

Every clause is falsifiable on its own, and each refusal names which clause
failed, because a gate that fails without saying why is the thing being fixed
here. Clause 5 is what keeps this from becoming a hiding place: a VM that dies
mid-session holds its claim until the claim is older than `DEFAULT_LEASE_HOURS`,
and from that moment its session fails the gate again. The cost is stated in
`DECISIONS-GATING.md` D025 — a crash inside the lease window is not detected by
this gate, it is detected by `task list --remote` naming the holder.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from . import tasks

# A claim older than this is assumed to belong to a VM that is gone. It is
# deliberately far above the longest honest session observed in this
# repository (about 70 minutes) and deliberately finite, because "in flight"
# with no upper bound is indistinguishable from "abandoned".
DEFAULT_LEASE_HOURS = 12.0

# Ledger actions that put a claim in force. Everything else ends one.
OPENING_ACTIONS = frozenset({"claim", "takeover"})


@dataclass
class Verdict:
    """Why an unfinished session is or is not still being worked on."""

    in_flight: bool
    reason: str
    task: str = ""
    agent: str = ""
    vm: str = ""
    age_h: float | None = None

    def note(self, session: str) -> str:
        """One line for `session verify`, naming task, holder, and claim age."""
        age = "unknown age" if self.age_h is None else f"{self.age_h:.1f}h ago"
        return (
            f"{session}: in flight (task {self.task}, claimed by {self.agent} "
            f"on {self.vm} {age})"
        )


def _parse_ts(text: str):
    try:
        stamp = datetime.fromisoformat(text)
    except (TypeError, ValueError):
        return None
    return stamp if stamp.tzinfo else stamp.replace(tzinfo=timezone.utc)


def _hours_since(text: str, now: datetime) -> float | None:
    stamp = _parse_ts(text)
    if stamp is None:
        return None
    return max(0.0, (now - stamp).total_seconds() / 3600.0)


def _task_by_id(task_id: str):
    for task in tasks.all_tasks():
        if task.task_id == task_id or task.path.name.startswith(f"{task_id}-"):
            return task
    return None


def _last_ledger_entry(task_id: str, history: list[dict]) -> dict | None:
    """The most recent ledger entry for a task, whatever its action.

    The whole history is read rather than `tasks.active_claims()`, because a
    refusal that can name the closing action ("the last action is `complete`")
    tells an operator what to fix, where "no claim in force" does not.
    """
    last: dict | None = None
    for entry in history:
        if entry.get("task") == task_id and "malformed" not in entry:
            last = entry
    return last


def _claim_identifies_session(task, session_id: str, start: dict) -> bool:
    """Does the task's claim name this session, or the machine running it?

    `claim-session` is the precise identifier when it was recorded. Older
    claims omit it, so fall back to agent plus host: weaker, but it still
    refuses a claim held by another machine, which is the case that matters.
    """
    recorded = (task.meta.get("claim-session") or "").strip()
    if recorded:
        return recorded == session_id
    agent = (task.meta.get("claim-agent") or "").strip()
    vm = (task.meta.get("claim-vm") or "").strip()
    if not agent and not vm:
        return False
    return agent == (start.get("actor") or "") and vm == (start.get("host") or "")


def _claim_naming(session_id: str, history: list[dict]) -> tuple[str, dict] | None:
    """Task and ledger entry for a claim in force that names this session.

    The `task` field of `session_start` is optional, and a session may claim its
    task without one. Observed on the live record: session
    `2026-10-03-037-repair-the-three-mission-records-corrupt` started with no
    `--task` and then claimed T-0021, whose ledger entry names the session. A
    predicate that only trusted the `task` field called that session abandoned
    and reddened the build while it was demonstrably working, which is the exact
    false red this module exists to remove.
    """
    found: tuple[str, dict] | None = None
    for entry in history:
        if "malformed" in entry or not entry.get("task"):
            continue
        if entry.get("session") == session_id:
            found = (str(entry["task"]), entry)
    return found


def _from_entry(
    entry: dict, task_id: str, agent: str, vm: str, lease_hours: float, now: datetime
) -> Verdict:
    """Apply the two clauses that depend on the ledger alone: opening and lease."""
    action = str(entry.get("action", ""))
    if action not in OPENING_ACTIONS:
        return Verdict(
            False,
            f"the last ledger action for {task_id} is {action!r}, not a claim",
            task=task_id,
            agent=agent,
            vm=vm,
        )
    age = _hours_since(str(entry.get("ts") or ""), now)
    if age is None:
        # An undatable claim is not a reason to fail someone's build, but it
        # must be visible, so the note says the age is unknown.
        return Verdict(
            True,
            "claim in force with no readable timestamp",
            task=task_id,
            agent=agent,
            vm=vm,
            age_h=None,
        )
    if age > lease_hours:
        return Verdict(
            False,
            f"the claim on {task_id} is {age:.1f}h old, past the {lease_hours:g}h lease",
            task=task_id,
            agent=agent,
            vm=vm,
            age_h=age,
        )
    return Verdict(True, "claim in force", task=task_id, agent=agent, vm=vm, age_h=age)


def classify(
    session_id: str,
    start: dict,
    *,
    lease_hours: float = DEFAULT_LEASE_HOURS,
    now: datetime | None = None,
    ledger: list[dict] | None = None,
) -> Verdict:
    """Decide whether an unfinished session is still in flight.

    `start` is the raw `session_start` event. `now` and `ledger` exist so tests
    can date a claim and supply a ledger without depending on the wall clock or
    on the file; both default to the real thing.
    """
    now = now or datetime.now(timezone.utc)
    history = tasks.claims() if ledger is None else ledger
    task_id = str((start.get("data") or {}).get("task") or "").strip()

    if not task_id:
        named = _claim_naming(session_id, history)
        if named is None:
            return Verdict(
                False,
                "the session_start records no task and no claim in the ledger names this session",
            )
        return _from_entry(
            named[1], named[0], str(named[1].get("agent") or ""),
            str(named[1].get("vm") or ""), lease_hours, now,
        )

    task = _task_by_id(task_id)
    if task is None:
        return Verdict(False, f"{task_id} is not in this tree", task=task_id)
    if task.status != "claimed":
        return Verdict(
            False,
            f"{task_id} is {task.status}, not claimed",
            task=task_id,
            agent=task.meta.get("claim-agent", ""),
            vm=task.meta.get("claim-vm", ""),
        )
    if not _claim_identifies_session(task, session_id, start):
        holder = (task.meta.get("claim-agent") or "?") + " on " + (task.meta.get("claim-vm") or "?")
        return Verdict(False, f"the claim on {task_id} is held by {holder}, not this session", task=task_id)

    # The task file says `claimed`; the ledger is the independent record, and it
    # is the one that survives a task file edited by hand.
    entry = _last_ledger_entry(task_id, history)
    if entry is None:
        return Verdict(False, f"{task_id} has no entry in the claim ledger", task=task_id)
    return _from_entry(
        entry,
        task_id,
        str(entry.get("agent") or task.meta.get("claim-agent") or ""),
        str(entry.get("vm") or task.meta.get("claim-vm") or ""),
        lease_hours,
        now,
    )
