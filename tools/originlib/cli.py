"""Command-line interface for the origin tooling.

Exit codes are part of the contract, because CI and VM scripts branch on them:

    0  success
    1  usage error
    2  lint violation
    3  verification failed (a declared check ran and did not pass)
    4  integrity violation (the record is inconsistent)
"""

from __future__ import annotations

import sys

from . import (
    annotate,
    cli_repo,
    cli_session,
    cli_sync,
    cli_task,
    idalloc,
    probe,
    session,
    sync,
    tasks,
    worktree,
)
from .cli_args import build_parser
from .usage import Usage

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_LINT = 2
EXIT_VERIFY = 3
EXIT_INTEGRITY = 4


DISPATCH = {
    "session": cli_session.dispatch,
    "task": cli_task.dispatch,
    "annotate": lambda args: annotate.dispatch(args.gate),
    "probe": probe.dispatch,
    "doc": cli_repo.dispatch_doc,
    "id": cli_repo.dispatch_id,
    "skills": cli_repo.dispatch_skills,
    "release": cli_repo.dispatch_release,
    "doctor": cli_repo.doctor,
    "preflight": cli_repo.preflight,
    "sync": cli_sync.dispatch_sync,
    "worktree": cli_sync.dispatch_worktree,
}


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        handler = DISPATCH.get(args.group)
        if handler is None:
            raise Usage(f"unknown command group: {args.group}")
        return handler(args)
    except (Usage, ValueError) as exc:
        print(f"origin: {exc}", file=sys.stderr)
        return EXIT_USAGE
    except (session.SessionError, tasks.TaskError, idalloc.AllocationError) as exc:
        print(f"origin: {exc}", file=sys.stderr)
        return EXIT_USAGE
    except (sync.SyncError, worktree.WorktreeError) as exc:
        # A refusal the fleet flow is *meant* to produce, not a crash. Uncaught,
        # it printed a traceback and exited 1 by accident of the interpreter
        # rather than by the contract, so a caller could not tell a refusal from
        # a bug.
        print(f"origin: {exc}", file=sys.stderr)
        return EXIT_USAGE
    except KeyboardInterrupt:
        print("origin: interrupted", file=sys.stderr)
        return EXIT_USAGE


if __name__ == "__main__":    sys.exit(main())
