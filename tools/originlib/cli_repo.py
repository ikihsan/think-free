"""CLI handlers for `origin doc`, `origin skills`, `origin release`, doctor."""

from __future__ import annotations

import argparse
import json

from . import docindex, doclint, doctor, events, paths, release, report, skillsync, tasks
from .cli_session import verify_sessions

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_LINT = 2


def dispatch_doc(args: argparse.Namespace) -> int:
    if args.action == "lint":
        result = doclint.lint()
        if not args.quiet or not result.ok:
            print(result.render())
        return EXIT_OK if result.ok else EXIT_LINT
    if args.action == "index":
        # Session reports change as events arrive, including the active
        # session's. Regenerate them first so a lint run straight afterwards
        # does not report the active session as stale.
        for name in events.all_sessions():
            report.regenerate_session(name)
        # Order matters: docs/INDEX.md summarises the other two indexes, so
        # they must reach their final content first.
        generators = (
            ("sessions/INDEX.md", report.render_sessions_index, report.regenerate_sessions_index),
            ("tasks/INDEX.md", tasks.render_tasks_index, tasks_index_write),
            ("docs/INDEX.md", docindex.render, docindex_write),
        )
        paths_to = (
            paths.sessions_index(),
            paths.tasks_index(),
            paths.docs_index(),
        )
        changed = [
            name for (name, renderer, _), target in zip(generators, paths_to)
            if renderer() != _read(target)
        ]
        if args.check:
            if changed:
                print("doc index: stale -> " + ", ".join(changed))
                return EXIT_LINT
            print("doc index: current")
            return EXIT_OK
        for (name, renderer, _), target in zip(generators, paths_to):
            if name in changed:
                report.write_if_changed(target, renderer())
                print(f"updated {name}")
        if not changed:
            print("doc index: already current")
        return EXIT_OK
    raise Usage(f"unknown doc action: {args.action}")


def _read(path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def docindex_write() -> None:
    report.write_if_changed(paths.docs_index(), docindex.render())


def tasks_index_write() -> None:
    report.write_if_changed(paths.tasks_index(), tasks.render_tasks_index())


def dispatch_skills(args: argparse.Namespace) -> int:
    if args.action == "check":
        result = skillsync.check()
        print(result.render())
        return EXIT_OK if result.ok else EXIT_LINT
    if args.action == "sync":
        result = skillsync.sync(use_copies=args.copy)
        print(result.render())
        return EXIT_OK if result.ok else EXIT_LINT
    if args.action == "hash":
        target = skillsync.write_hashes()
        print(f"recorded vendored hashes in {paths.paths_repo_relative(target)}")
        return EXIT_OK
    if args.action == "verify":
        result = skillsync.verify_vendor()
        print(result.render())
        return EXIT_OK if result.ok else EXIT_INTEGRITY
    raise Usage(f"unknown skills action: {args.action}")


def dispatch_release(args: argparse.Namespace) -> int:
    if args.action == "check":
        result = release.check()
        print(result.render())
        return EXIT_OK if result.ok else EXIT_LINT
    raise Usage(f"unknown release action: {args.action}")


def doctor(args: argparse.Namespace) -> int:
    from . import doctor

    data = doctor.collect(network=not args.offline)
    written = doctor.write(data)
    if args.json:
        print(json.dumps(data, indent=2, sort_keys=True))
    else:
        print(doctor.summarize(data))
        print(f"raw          {written}")
    return EXIT_OK


def preflight(args: argparse.Namespace) -> int:
    lint_result = doclint.lint()
    print(lint_result.render())
    skills_result = skillsync.check()
    print(skills_result.render())
    session_result = verify_sessions(strict=bool(getattr(args, "strict", False)))
    ok = lint_result.ok and skills_result.ok and session_result == EXIT_OK
    print("preflight: OK" if ok else "preflight: FAILED")
    return EXIT_OK if ok else EXIT_LINT

