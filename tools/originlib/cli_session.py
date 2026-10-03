"""CLI handlers for `origin session`.

Also owns `verify_sessions`, which CI and VM preflight both call.
"""

from __future__ import annotations

import json

from . import events, inflight, paths, report, session
from .doclint import active_session_id

EXIT_OK = 0
EXIT_INTEGRITY = 4



def dispatch(args: argparse.Namespace) -> int:
    if args.action == "start":
        active = session.start(
            args.goal,
            agent=args.agent or None,
            task=args.task or None,
            sync_remote=bool(getattr(args, "sync", True)),
        )
        print(f"session {active.session} started")
        print(f"  goal:  {active.goal}")
        print(f"  agent: {active.agent}   host: {active.host}   branch: {active.branch}")
        if not getattr(args, "sync", True):
            print("  sync:  skipped (--no-sync); this tree may be behind the shared base")
        print("  log work with: tools/x -- <command>")
        return EXIT_OK
    if args.action == "step":
        print(f"seq {session.step(args.text).seq}")
        return EXIT_OK
    if args.action == "note":
        print(f"seq {session.note(args.text).seq}")
        return EXIT_OK
    if args.action == "decision":
        event = session.decision(args.text, args.refs)
        print(f"seq {event.seq}  decision recorded")
        print("  remember to update DECISIONS.md in this session's commit")
        return EXIT_OK
    if args.action == "block":
        print(f"seq {session.block(args.text).seq}")
        print("  remember to update STATE.md before finishing")
        return EXIT_OK
    if args.action == "experiment-result":
        event = session.experiment_result(args.experiment, args.text, args.refs)
        print(f"seq {event.seq}  experiment result recorded")
        return EXIT_OK
    if args.action == "artifact":
        if not args.paths and not args.dir:
            raise ValueError("give one or more paths, or at least one --dir")
        targets, skipped = _expand_artifact_targets(args.paths, args.dir)
        for target in targets:
            event = session.artifact(target, args.note_text)
            print(f"seq {event.seq}  {event.data['path']}  {event.data['sha256'][:12]}")
        print(f"{len(targets)} artifact(s) recorded")
        for ignored in skipped:
            print(f"  skipped (gitignored)  {ignored}")
        return EXIT_OK
    if args.action == "finish":
        result = session.finish(
            args.outcome, args.summary, args.next_steps, push=bool(getattr(args, "push", False))
        )
        report.regenerate_session(result["session"])
        report.regenerate_sessions_index()
        _print_finish(result)
        if result.get("pushed"):
            print(f"  pushed: {result['pushed'][:12]} (session commit {result['session_commit'][:12]})")
        return EXIT_INTEGRITY if (result["unlogged"] or result["missing"]) else EXIT_OK
    if args.action == "status":
        state = session.status()
        print(json.dumps(state, indent=2, sort_keys=True))
        return EXIT_OK
    if args.action == "list":
        for name in reversed(events.all_sessions()):
            items = events.events_for(name)
            end = next((e for e in items if e.kind == "session_end"), None)
            print(f"{name}  {end.data.get('outcome') if end else 'unfinished'}")
        return EXIT_OK
    if args.action == "resume":
        return _resume(args.session_id)
    if args.action == "verify":
        return verify_sessions(
            strict=bool(getattr(args, "strict", False)),
            lease_hours=getattr(args, "lease_hours", None),
        )
    raise Usage(f"unknown session action: {args.action}")


def _expand_artifact_targets(paths: list[str], directories: list[str]) -> tuple[list[str], list[str]]:
    """Expand --dir into individual files, so every artifact gets its own hash.

    Declaration is per file by design: a hash of a directory says nothing about
    the contents, and the whole point is that a reader can check one artifact.
    """
    from pathlib import Path

    from . import gitutil

    targets: list[str] = [item for item in paths if not gitutil.is_ignored(item)]
    skipped: list[str] = [item for item in paths if gitutil.is_ignored(item)]
    for directory in directories:
        base = Path(paths_module_root() or ".").resolve() / directory
        if not base.is_dir():
            raise ValueError(f"--dir is not a directory: {directory}")
        for item in sorted(base.rglob("*")):
            if not item.is_file():
                continue
            rel = item.relative_to(Path(paths_module_root())).as_posix()
            if gitutil.is_ignored(rel):
                skipped.append(rel)
                continue
            targets.append(rel)
    seen: set[str] = set()
    unique: list[str] = []
    for target in targets:
        if target not in seen:
            seen.add(target)
            unique.append(target)
    return unique, skipped


def paths_module_root() -> str:
    from . import paths

    return str(paths.repo_root())


def _print_finish(result: dict) -> None:
    print(f"session {result['session']} finished: {result['outcome']} in {result['elapsed_s']}s")
    print(f"  declared artifacts: {len(result['declared'])}")
    print(f"  working-tree changes: {len(result['changed'])}")
    if result["unlogged"]:
        print(f"  UNLOGGED ({len(result['unlogged'])}): declare them or revert them")
        for rel in result["unlogged"]:
            print(f"    - {rel}")
    if result["missing"]:
        print(f"  MISSING declared artifacts ({len(result['missing'])}):")
        for rel in result["missing"]:
            print(f"    - {rel}")
    for record, kinds in result["documentation_gaps"].items():
        print(f"  DOC GAP: {record} not updated although the session recorded {', '.join(kinds)}")
    print(f"  report: {paths.paths_repo_relative(paths.session_report(result['session']))}")


def _resume(session_id: str) -> int:
    if not session_id:
        state = session.status()
        if not state.get("active"):
            print("no active session; nothing to resume")
            return EXIT_OK
        session_id = state["session"]
    if session_id not in events.all_sessions():
        raise Usage(f"no such session: {session_id}")
    items = events.events_for(session_id)
    start = next((e for e in items if e.kind == "session_start"), None)
    end = next((e for e in items if e.kind == "session_end"), None)
    print(f"session     {session_id}")
    print(f"goal        {(start.data.get('goal') if start else '?')}")
    print(f"agent       {(start.raw.get('actor') if start else '?')}")
    print(f"outcome     {(end.data.get('outcome') if end else 'UNFINISHED')}")
    if end:
        print(f"next        {end.data.get('next', '')}")
    print("decisions:")
    for item in items:
        if item.kind == "decision":
            print(f"  [{item.seq}] {item.summary()}")
    print("last five events:")
    for item in items[-5:]:
        print(f"  [{item.seq}] {item.kind}: {item.summary()}")
    print(f"full record {paths.paths_repo_relative(paths.events_file(session_id))}")
    return EXIT_OK


def verify_sessions(strict: bool = False, lease_hours: float | None = None) -> int:
    """Check every session record. Exit 4 on a problem.

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
    problems: list[str] = []
    notes: list[str] = []
    in_flight = active_session_id()
    sessions = events.all_sessions()
    for name in sessions:
        path = paths.events_file(name)
        raw = events.read(path)
        seqs = []
        kinds: list[str] = []
        for item in raw:
            for issue in events.validate(item):
                problems.append(f"{name}: {issue}")
            if isinstance(item.get("seq"), int):
                seqs.append(item["seq"])
            if "kind" in item:
                kinds.append(item["kind"])
        if seqs != list(range(1, len(seqs) + 1)):
            problems.append(f"{name}: sequence is not 1..n contiguous: {seqs[:8]}...")
        if kinds.count("session_start") != 1:
            problems.append(f"{name}: expected exactly one session_start")
        if kinds.count("session_end") > 1:
            problems.append(f"{name}: more than one session_end")
        if kinds and kinds[-1] != "session_end":
            message = f"{name}: last event is {kinds[-1]!r}; session may be unfinished"
            if name == in_flight and not strict:
                notes.append(f"{name}: in progress ({kinds[-1]})")
            else:
                start = next((e for e in raw if e.get("kind") == "session_start"), {})
                verdict = inflight.classify(name, start, lease_hours=lease)
                if verdict.in_flight:
                    notes.append(verdict.note(name))
                else:
                    problems.append(f"{message}; {verdict.reason}")
        if not events.SESSION_ID.match(name):
            problems.append(f"{name}: directory name is not a valid session id")
        if not paths.session_report(name).exists():
            problems.append(f"{name}: report README.md missing")
        for item in raw:
            if item.get("kind") != "command":
                continue
            data = item.get("data", {})
            log = data.get("log")
            if not log:
                problems.append(f"{name} seq {item.get('seq')}: command event has no log reference")
                continue
            log_path = paths.repo_root() / log
            if not log_path.exists():
                problems.append(f"{name} seq {item.get('seq')}: log {log} missing")
                continue
            total = len(log_path.read_text(encoding="utf-8", errors="replace").splitlines())
            end_line = data.get("log_line_end")
            if isinstance(end_line, int) and end_line > total:
                problems.append(f"{name} seq {item.get('seq')}: log line {end_line} beyond {total}")
    for name in ("docs/INDEX.md", "sessions/INDEX.md", "tasks/INDEX.md"):
        if not (paths.repo_root() / name).exists():
            problems.append(f"{name}: generated index missing")
    print(f"session verify: {len(sessions)} session(s) checked")
    for note in notes:
        print(f"  note  {note}")
    for problem in problems:
        print(f"  FAIL  {problem}")
    print("session verify: OK" if not problems else f"session verify: {len(problems)} problem(s)")
    return EXIT_INTEGRITY if problems else EXIT_OK

