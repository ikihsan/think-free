"""CLI handlers for `origin task`."""

from __future__ import annotations

from . import session, taskops, tasks

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_VERIFY = 3


def dispatch(args: argparse.Namespace) -> int:
    if args.action == "new":
        task = taskops.create(
            args.goal,
            args.verify,
            rationale=args.rationale,
            steps=args.steps,
            acceptance=args.acceptance,
            preconditions=args.preconditions,
            rollback=args.rollback,
        )
        print(f"created {task.task_id}  {task.path.name}")
        print(f"  verify: {args.verify}")
        return EXIT_OK
    if args.action == "list":
        tasks.print_list(args.status)
        return EXIT_OK
    if args.action == "claim":
        agent = args.agent or session.status().get("agent", "")
        active = session.status()
        task = taskops.claim(args.task_id, agent, args.vm, active.get("session", ""))
        print(f"{task.task_id} claimed by {agent} on {args.vm or 'unknown-vm'}")
        return EXIT_OK
    if args.action == "verify":
        task = tasks.find(args.task_id)
        outcome = taskops.run_verification(task)
        if not outcome.get("ran"):
            print(f"{task.task_id}: {outcome['reason']}")
            return EXIT_USAGE
        print(f"{task.task_id}: `{outcome['command']}` -> exit {outcome['exit_code']} in {outcome['duration_s']}s")
        if outcome["exit_code"] != 0:
            tail = (outcome["stdout_tail"] + outcome["stderr_tail"]).strip().splitlines()
            for line in tail[-15:]:
                print(f"  | {line}")
        return EXIT_OK if outcome["exit_code"] == 0 else EXIT_VERIFY
    if args.action == "complete":
        taskops.transition(args.task_id, "done", args.summary, evidence=args.evidence)
        print(f"{args.task_id} completed")
        print("  remember to update STATE.md and ROADMAP.md in this session's commit")
        return EXIT_OK
    if args.action == "cancel":
        taskops.transition(args.task_id, "cancelled", args.reason)
        print(f"{args.task_id} cancelled: {args.reason}")
        return EXIT_OK
    raise Usage(f"unknown task action: {args.action}")

