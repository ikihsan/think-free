"""Command-line grammar for the origin tooling.

Split out of `cli.py` so that the parser and the dispatch table can each stay
readable: the arguments are a long flat list, and the code that acts on them is
a short one. The exit-code contract and every refusal stay in `cli.py`, because
that is where CI and VM scripts read them.
"""

from __future__ import annotations

import argparse

from . import inflight, session


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="origin",
        description="Session logging, task dispatch, documentation lint, and skill checks.",
    )
    sub = parser.add_subparsers(dest="group", required=True)

    # ------------------------------------------------------------- session
    session_parser = sub.add_parser("session", help="record and verify agent sessions")
    session_sub = session_parser.add_subparsers(dest="action", required=True)

    start = session_sub.add_parser("start", help="open a session before doing any work")
    start.add_argument("--goal", required=True)
    start.add_argument("--task", default="")
    start.add_argument("--agent", default="")
    start.add_argument(
        "--no-sync",
        dest="sync",
        action="store_false",
        help="do not fetch and fast-forward onto the shared base first",
    )

    for name, help_text in (
        ("step", "record a milestone"),
        ("note", "record an observation"),
        ("decision", "record a decision with optional references"),
        ("block", "record a blocker"),
    ):
        item = session_sub.add_parser(name, help=help_text)
        item.add_argument("text")
        if name == "decision":
            item.add_argument("--refs", nargs="*", default=[])

    result = session_sub.add_parser("experiment-result", help="record an experiment outcome")
    result.add_argument("experiment")
    result.add_argument("text")
    result.add_argument("--refs", nargs="*", default=[])

    artifact = session_sub.add_parser("artifact", help="record produced files with their hashes")
    artifact.add_argument("paths", nargs="*")
    artifact.add_argument("--note", dest="note_text", default="")
    artifact.add_argument(
        "--dir",
        action="append",
        default=[],
        help="record every file under this directory (repeatable)",
    )

    finish = session_sub.add_parser("finish", help="reconcile, close, and regenerate reports")
    finish.add_argument("--outcome", required=True, choices=session.OUTCOMES)
    finish.add_argument("--summary", required=True)
    finish.add_argument("--next", dest="next_steps", required=True)
    finish.add_argument(
        "--push",
        action="store_true",
        help="commit this session's own record and push the branch before exiting",
    )

    session_sub.add_parser("status", help="show the active session")
    verify = session_sub.add_parser("verify", help="check every session record for integrity")
    verify.add_argument(
        "--strict",
        action="store_true",
        help="also fail for the session running in this working tree (use in CI)",
    )
    verify.add_argument(
        "--lease-hours",
        type=float,
        default=None,
        metavar="H",
        help=(
            "how old a task claim may be while its unfinished session still counts as "
            f"in flight (default {inflight.DEFAULT_LEASE_HOURS:g})"
        ),
    )
    resume = session_sub.add_parser("resume", help="compressed brief for continuing work")
    resume.add_argument("session_id", nargs="?", default="")
    session_sub.add_parser("list", help="list recorded sessions")

    # ---------------------------------------------------------------- task
    task_parser = sub.add_parser("task", help="create, claim, verify, and complete tasks")
    task_sub = task_parser.add_subparsers(dest="action", required=True)

    new = task_sub.add_parser("new", help="create a task file from the template")
    new.add_argument("--goal", required=True)
    new.add_argument("--verify", required=True, help="runnable command that proves completion")
    new.add_argument("--rationale", default="")
    # `append`, because these two are the ones a writer repeats. Declared with a
    # string default and no action, argparse keeps the *last* occurrence and drops
    # the rest without a word: five `--acceptance` values left one line in the task
    # file, which is the record of what "done" means (defect 11).
    new.add_argument("--steps", action="append", default=[], metavar="STEP")
    new.add_argument("--acceptance", action="append", default=[], metavar="CRITERION")
    new.add_argument("--preconditions", default="")
    new.add_argument("--rollback", default="")

    listing = task_sub.add_parser("list", help="list tasks")
    listing.add_argument("--status", default="")
    listing.add_argument(
        "--remote",
        action="store_true",
        help="list the tasks as the shared remote records them, not this working tree",
    )

    claim = task_sub.add_parser("claim", help="claim a task for an agent and machine")
    claim.add_argument("task_id")
    claim.add_argument("--agent", default="")
    claim.add_argument("--vm", default="")
    claim.add_argument(
        "--takeover",
        default="",
        metavar="REASON",
        help="claim a task held by a dead VM, recording why",
    )
    push_group = claim.add_mutually_exclusive_group()
    push_group.add_argument(
        "--push",
        dest="push",
        action="store_true",
        default=None,
        help="publish the claim so other VMs can see it (default when a remote exists)",
    )
    push_group.add_argument(
        "--no-push",
        dest="push",
        action="store_false",
        help="record the claim in this working tree only; other VMs cannot see it",
    )

    task_sub.add_parser("verify", help="run a task's declared verification command").add_argument(
        "task_id"
    )

    complete = task_sub.add_parser("complete", help="mark a task done")
    complete.add_argument("task_id")
    complete.add_argument("--summary", required=True)
    complete.add_argument("--evidence", nargs="*", default=[])

    cancel = task_sub.add_parser("cancel", help="mark a task cancelled")
    cancel.add_argument("task_id")
    cancel.add_argument("--reason", required=True)

    release = task_sub.add_parser("release", help="return a claimed task to the pool")
    release.add_argument("task_id")
    release.add_argument("--reason", default="")
    release.add_argument("--agent", default="")
    release.add_argument("--vm", default="")

    # ------------------------------------------------------------------- id
    id_parser = sub.add_parser(
        "id", help="allocate an F, D or T identifier from the shared base"
    )
    id_sub = id_parser.add_subparsers(dest="action", required=True)
    id_next = id_sub.add_parser(
        "next", help="print the next free identifier and the record it was read from"
    )
    # Deliberately not an argparse `choices`: a mistyped kind is a usage error,
    # which is exit 1 here, and letting argparse exit 2 would report it as a
    # lint violation.
    id_next.add_argument("kind")
    id_next.add_argument(
        "--json",
        action="store_true",
        help="print the whole allocation record, including every number that was read",
    )

    # ----------------------------------------------------------------- sync
    sync_parser = sub.add_parser(
        "sync", help="fetch, fast-forward, publish, and land work for other VMs"
    )
    sync_sub = sync_parser.add_subparsers(dest="action", required=True)
    sync_sub.add_parser("status", help="branch, divergence, dirty paths, rebase state")
    sync_sub.add_parser("pull", help="fetch and fast-forward onto the shared base")
    push_cmd = sync_sub.add_parser("push", help="publish the current branch; never forces")
    push_cmd.add_argument("--branch", default="")
    push_cmd.add_argument("--set-upstream", action="store_true")
    land = sync_sub.add_parser("land", help="rebase this branch onto the base and push it")
    land.add_argument("--branch", default="", help="base branch to land on (default: detected)")

    # ------------------------------------------------------------- worktree
    wt_parser = sub.add_parser("worktree", help="isolate a task in its own directory and branch")
    wt_sub = wt_parser.add_subparsers(dest="action", required=True)
    wt_add = wt_sub.add_parser("add", help="create a worktree and branch for one task")
    wt_add.add_argument("task")
    wt_add.add_argument("--vm", default="", help="defaults to this machine's hostname")
    wt_add.add_argument("--base", default="", help="base branch to branch from (default: detected)")
    wt_sub.add_parser("list", help="list worktrees and the tasks they hold")
    wt_remove = wt_sub.add_parser("remove", help="remove a worktree")
    wt_remove.add_argument("path")
    wt_remove.add_argument("--force", action="store_true", help="discard uncommitted work")

    # ----------------------------------------------------------------- doc
    doc_parser = sub.add_parser("doc", help="documentation lint and index generation")
    doc_sub = doc_parser.add_subparsers(dest="action", required=True)
    lint = doc_sub.add_parser("lint", help="line caps, metadata, links, orphans, staleness")
    lint.add_argument("--quiet", action="store_true")
    index = doc_sub.add_parser("index", help="regenerate docs, sessions, and tasks indexes")
    index.add_argument("--check", action="store_true", help="fail if anything would change")

    # ------------------------------------------------------------- annotate
    # Every gate is named after the command that runs it, and its own flags
    # follow, so the CI step and the command a VM would type to reproduce it
    # are the same string. `argparse.REMAINDER` is what makes that possible:
    # `--quiet` and `--strict` belong to the gate, not to this wrapper.
    annotate_parser = sub.add_parser(
        "annotate",
        help="run a gate and re-emit its violations as check-run annotations",
    )
    annotate_parser.add_argument(
        "gate",
        nargs=argparse.REMAINDER,
        help="the gate to run and its own flags, e.g. 'doc lint', 'session verify --strict'",
    )

    # -------------------------------------------------------------- skills
    skills_parser = sub.add_parser("skills", help="skill layout, mirroring, and vendor drift")
    skills_sub = skills_parser.add_subparsers(dest="action", required=True)
    skills_sub.add_parser("check", help="naming rules and cross-agent mirrors")
    skills_sub.add_parser("hash", help="record vendored file hashes")
    skills_sub.add_parser("verify", help="detect modification of vendored skills")
    sync = skills_sub.add_parser("sync", help="create missing .claude/skills mirrors")
    sync.add_argument("--copy", action="store_true", help="copy instead of symlink")

    # ------------------------------------------------------------- release
    release_parser = sub.add_parser(
        "release", help="enforce RELEASE-MANIFEST.md, the authority on what is public"
    )
    release_sub = release_parser.add_subparsers(dest="action", required=True)
    release_sub.add_parser("check", help="check the manifest against this tree")

    # --------------------------------------------------------------- tools
    doc_parser_moved = sub.add_parser("doctor", help="verify this machine can run the work")
    doc_parser_moved.add_argument("--offline", action="store_true")
    doc_parser_moved.add_argument("--json", action="store_true", help="print raw JSON")
    preflight = sub.add_parser("preflight", help="lint plus session verification, for CI and VM start")
    preflight.add_argument(
        "--strict",
        action="store_true",
        help="also fail for the session running in this working tree (use in CI)",
    )
    preflight.add_argument(
        "--lease-hours",
        type=float,
        default=None,
        metavar="H",
        help="claim age at which an unfinished session stops counting as in flight",
    )
    return parser

