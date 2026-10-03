"""Per-VM worktree isolation.

Two agents sharing one working tree share one index, one `sessions/active.json`
pointer, and one set of uncommitted changes, so their sessions cannot both be
open and neither can tell whose change it is looking at. A worktree per task
removes the collision at the filesystem level; a branch per task removes it in
git.

`.worktrees/` is gitignored, so an isolation mechanism cannot itself become
tracked content.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from . import gitutil, paths, sync, taskremote
from .tasks import TaskError

WORKTREE_DIRNAME = ".worktrees"
BRANCH_PREFIX = "task/"


class WorktreeError(RuntimeError):
    """Raised when a worktree cannot be created or removed safely."""


@dataclass
class Worktree:
    path: Path
    branch: str
    head: str
    task: str = ""
    base_branch: str = ""

    def as_dict(self) -> dict:
        return {
            "path": str(self.path),
            "branch": self.branch,
            "head": self.head[:12],
            "task": self.task,
        }


def worktree_root() -> Path:
    return paths.repo_root() / WORKTREE_DIRNAME


def branch_name(task_id: str, vm: str) -> str:
    return f"{BRANCH_PREFIX}{task_id}-{vm or 'local'}"


def default_vm() -> str:
    return gitutil.host_identity()[0]


def ensure_root() -> Path:
    """Create the worktree root and make sure git ignores it.

    The isolation mechanism must not be able to commit itself: a repository
    without the ignore rule would let `git add -A` capture another VM's entire
    working tree.
    """
    root = worktree_root()
    root.mkdir(parents=True, exist_ok=True)
    pattern = f"{WORKTREE_DIRNAME}/"
    ignore = paths.repo_root() / ".gitignore"
    text = ignore.read_text(encoding="utf-8") if ignore.exists() else ""
    if pattern not in text:
        with open(ignore, "a", encoding="utf-8") as handle:
            if text and not text.endswith("\n"):
                handle.write("\n")
            handle.write(f"{pattern}\n")
    return root


def is_registered(path: Path) -> bool:
    target = str(path.resolve())
    for row in gitutil.run(["worktree", "list", "--porcelain"]).stdout.splitlines():
        if row.startswith("worktree ") and row.split(" ", 1)[1] == target:
            return True
    return False


def list_worktrees() -> list[Worktree]:
    """Parse `git worktree list --porcelain` into plain data."""
    rows: list[Worktree] = []
    path = branch = ""
    for line in gitutil.run(["worktree", "list", "--porcelain"]).stdout.splitlines():
        if line.startswith("worktree "):
            path = line.split(" ", 1)[1]
        elif line.startswith("branch "):
            branch = line.split(" ", 1)[1].split("refs/heads/")[-1]
        elif not line.strip() and path:
            rows.append(Worktree(path=Path(path), branch=branch, head=""))
            path = branch = ""
    if path:
        rows.append(Worktree(path=Path(path), branch=branch, head=""))
    for row in rows:
        head = gitutil.text(["rev-parse", "--short", "HEAD"], row.path)
        row.head = head or ""
        row.task = row.branch[len(BRANCH_PREFIX) :].rsplit("-", 1)[0] if row.branch.startswith(BRANCH_PREFIX) else ""
    return rows


def add(task_id: str, vm: str = "", base: str = "", allow_contended: bool = False) -> Worktree:
    """Create an isolated worktree and branch for one task on one VM.

    Refuses when the task is already claimed on *another* VM, when this VM
    already has a worktree for it, or when the branch name is taken: each
    refusal is a case where two agents would otherwise end up editing the same
    files.

    A claim held by this VM does not refuse. `docs/operations/vm-execution.md`
    sequences `task claim` before `worktree add`, so refusing our own claim made
    the documented sequence impossible; and the VM is the unit of isolation
    anyway, because two agents on one machine share one working tree, one git
    index, and one `sessions/active.json`. A claim with no recorded VM is
    refused, since an unattributable claim cannot be shown to be ours.
    """
    from . import tasks

    vm = vm or default_vm()
    task = tasks.find(task_id)
    remote = sync.remote_name()
    base = base or sync.base_branch()

    holder = taskremote.holder(task_id)
    if holder and holder.get("agent") and holder.get("vm") != vm and not allow_contended:
        raise WorktreeError(
            f"{task_id} is claimed by {holder['agent']} on {holder.get('vm', '?')} "
            f"since {holder.get('ts', '?')}; pick another task or record a takeover"
        )

    branch = branch_name(task_id, vm)
    target = ensure_root() / f"{task_id}-{vm}"
    if target.exists() or is_registered(target):
        raise WorktreeError(f"{target} already exists; remove it or reuse it")
    existing = gitutil.text(["branch", "--list", branch])
    if existing:
        raise WorktreeError(f"branch {branch} already exists; another worktree owns it")

    start_point = f"{remote}/{base}" if remote else base
    if gitutil.run(["rev-parse", "--verify", "--quiet", start_point]).returncode != 0:
        raise WorktreeError(f"{start_point} does not exist; run 'tools/origin sync pull' first")
    result = gitutil.run(["worktree", "add", "-q", "-b", branch, str(target), start_point])
    if result.returncode != 0:
        raise WorktreeError(f"git worktree add failed: {(result.stderr + result.stdout).strip()}")
    head = gitutil.text(["rev-parse", "HEAD"], target)
    return Worktree(path=target, branch=branch, head=head, task=task.task_id, base_branch=base)


def remove(path: str | Path, force: bool = False) -> Worktree:
    """Remove a worktree. A dirty worktree needs `force`, never a silent loss."""
    target = Path(path)
    if not str(target.resolve()).startswith(str(worktree_root().resolve())):
        raise WorktreeError(f"refusing to remove a path outside {worktree_root()}")
    if not is_registered(target):
        raise WorktreeError(f"{target} is not a registered worktree")
    args = ["worktree", "remove"]
    if force:
        args.append("--force")
    args.append(str(target))
    result = gitutil.run(args)
    if result.returncode != 0:
        raise WorktreeError(
            f"worktree has uncommitted changes ({', '.join(gitutil.dirty_paths(target)[:5])}); "
            "commit, discard deliberately, or pass --force"
        )
    return Worktree(path=target, branch="", head="")


def render_list() -> str:
    rows = list_worktrees()
    if not rows:
        return "no worktrees"
    lines = ["| Path | Branch | Task | HEAD |", "|---|---|---|---|"]
    for row in rows:
        task = row.task or "-"
        lines.append(f"| `{row.path}` | {row.branch or '-'} | {task} | {row.head or '-'} |")
    return "\n".join(lines)
