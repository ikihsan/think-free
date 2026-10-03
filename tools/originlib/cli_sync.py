"""CLI handlers for `origin sync` and `origin worktree`.

These two groups are the fleet-facing half of the tooling: everything that
decides whether this VM's work can safely coexist with another VM's.
"""

from __future__ import annotations

import json

from . import sync, worktree

EXIT_OK = 0
EXIT_USAGE = 1


def dispatch_sync(args: argparse.Namespace) -> int:
    if args.action == "status":
        report = sync.status()
        print(json.dumps(report, indent=2, sort_keys=True))
        if report["rebase_in_progress"]:
            print("  a rebase is in progress; resolve it or run 'git rebase --abort'")
            return EXIT_USAGE
        return EXIT_OK
    if args.action == "pull":
        outcome = sync.pull()
        verb = "fast-forwarded to" if outcome["fast_forwarded"] else "already at"
        print(f"{outcome['remote']}/{outcome['base_branch']}: {verb} the base (was behind {outcome['behind_before']})")
        return EXIT_OK
    if args.action == "push":
        outcome = sync.push(args.branch or "", set_upstream=args.set_upstream)
        print(f"pushed {outcome['branch']} -> {outcome['remote']} at {outcome['head'][:12]}")
        return EXIT_OK
    if args.action == "land":
        outcome = sync.land(args.branch or "")
        resolved = outcome.get("resolved") or []
        print(f"landed on {outcome['branch']} at {outcome.get('head', '')[:12]}")
        for name in resolved:
            print(f"  regenerated {name} to resolve the merge")
        return EXIT_OK
    raise ValueError(f"unknown sync action: {args.action}")


def dispatch_worktree(args: argparse.Namespace) -> int:
    if args.action == "add":
        info = worktree.add(args.task, vm=args.vm or "", base=args.base or "")
        print(f"{info.task} worktree for {info.branch}")
        print(f"  path: {info.path}")
        print(f"  head: {info.head[:12]}  (from {sync.remote_name()}/{info.base_branch})")
        print(f"  next: cd {info.path} && tools/origin task claim {info.task}")
        return EXIT_OK
    if args.action == "list":
        print(worktree.render_list())
        return EXIT_OK
    if args.action == "remove":
        info = worktree.remove(args.path, force=args.force)
        print(f"removed worktree {info.path}")
        return EXIT_OK
    raise ValueError(f"unknown worktree action: {args.action}")
