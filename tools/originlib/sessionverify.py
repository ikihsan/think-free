"""The integrity gate over every session record.

Split out of `cli_session.py` on 2026-10-04 (T-0047) when a seventh line of
reporting pushed that file to 302 of the 300 permitted lines, and by invariant:
`cli_session` dispatches the `origin session` subcommands, while this reads the
whole event stream of every session and decides whether the record is sound.
Adding a fact to the close report and adding a fact to that gate are different
kinds of change, and the cap keeps finding the difference by being inconvenient.

The two entry points answer one question in two shapes. `verify_sessions` prints
what a VM reads; `origin annotate` needs the *violations* to publish as
check-run annotations, and capturing stdout to get them is the shape of mistake
D025 describes — reading back a field another layer formatted for a person.
"""

from __future__ import annotations

from . import events, inflight, paths
from .doclint_tree import active_session_id
from .finding import Finding

EXIT_OK = 0
EXIT_INTEGRITY = 4


def verify_sessions(strict: bool = False, lease_hours: float | None = None) -> int:
    """Check every session record, print the report, and exit 4 on a problem."""
    report, problems = session_report(strict=strict, lease_hours=lease_hours)
    print(report)
    return EXIT_INTEGRITY if problems else EXIT_OK


def session_report(strict: bool = False, lease_hours: float | None = None):
    """The rendered report and the violations behind it, without printing.

    The session currently in flight is reported as in-progress rather than
    failed: by definition it has no `session_end` yet, and flagging that would
    make `preflight` unusable during work. CI passes `strict`, where nothing is
    in flight and an unfinished session genuinely is a failure.

    A session on *another* VM is judged by `inflight.classify`, not by this
    VM's knowledge: an unfinished session whose task is still claimed by that
    session is in flight, and one whose claim is gone, closed, superseded, or
    older than the lease is abandoned. `lease_hours=None` uses the recorded
    default rather than a value frozen here, so the flag and the constant
    cannot drift apart.
    """
    lease = inflight.DEFAULT_LEASE_HOURS if lease_hours is None else lease_hours
    problems: list[Finding] = []
    notes: list[str] = []
    in_flight = active_session_id()
    sessions = events.all_sessions()
    for name in sessions:
        path = paths.events_file(name)
        rel = paths.paths_repo_relative(path)
        raw = events.read(path)
        seqs = []
        kinds: list[str] = []
        for item in raw:
            for issue in events.validate(item):
                problems.append(Finding.at(rel, issue))
            if isinstance(item.get("seq"), int):
                seqs.append(item["seq"])
            if "kind" in item:
                kinds.append(item["kind"])
        if seqs != list(range(1, len(seqs) + 1)):
            problems.append(
                Finding.at(rel, f"sequence is not 1..n contiguous: {seqs[:8]}...")
            )
        if kinds.count("session_start") != 1:
            problems.append(Finding.at(rel, "expected exactly one session_start"))
        if kinds.count("session_end") > 1:
            problems.append(Finding.at(rel, "more than one session_end"))
        if kinds and kinds[-1] != "session_end":
            unfinished = f"last event is {kinds[-1]!r}; session may be unfinished"
            if name == in_flight and not strict:
                notes.append(f"{name}: in progress ({kinds[-1]})")
            else:
                start = next((e for e in raw if e.get("kind") == "session_start"), {})
                verdict = inflight.classify(name, start, lease_hours=lease)
                if verdict.in_flight:
                    notes.append(verdict.note(name))
                else:
                    problems.append(Finding.at(rel, f"{unfinished}; {verdict.reason}"))
        if not events.SESSION_ID.match(name):
            problems.append(Finding.at(rel, "directory name is not a valid session id"))
        if not paths.session_report(name).exists():
            problems.append(
                Finding.at(
                    paths.paths_repo_relative(paths.session_report(name)),
                    "report README.md missing",
                )
            )
        for item in raw:
            if item.get("kind") != "command":
                continue
            data = item.get("data", {})
            log = data.get("log")
            if not log:
                problems.append(
                    Finding.at(rel, f"seq {item.get('seq')}: command event has no log reference")
                )
                continue
            log_path = paths.repo_root() / log
            if not log_path.exists():
                problems.append(Finding.at(log, f"seq {item.get('seq')}: log missing"))
                continue
            total = len(log_path.read_text(encoding="utf-8", errors="replace").splitlines())
            end_line = data.get("log_line_end")
            if isinstance(end_line, int) and end_line > total:
                problems.append(
                    Finding.at(log, f"seq {item.get('seq')}: log line {end_line} beyond {total}")
                )
    for name in ("docs/INDEX.md", "sessions/INDEX.md", "tasks/INDEX.md"):
        if not (paths.repo_root() / name).exists():
            problems.append(Finding.at(name, "generated index missing"))
    lines = [f"session verify: {len(sessions)} session(s) checked"]
    lines.extend(f"  note  {note}" for note in notes)
    lines.extend(f"  FAIL  {problem}" for problem in problems)
    lines.append(
        "session verify: OK" if not problems else f"session verify: {len(problems)} problem(s)"
    )
    return "\n".join(lines), problems