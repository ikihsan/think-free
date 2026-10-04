"""What credential mechanism this machine has configured.

The mechanism half of the push-credential report T-0024 added to `doctor`
(T-0024, 2026-10-03). `doctor` used to read four environment variables and
nothing else, so it printed `credentials none present` on a VM whose pushes are
made by a GitHub App key reached through git's `credential.helper`, on a VM
whose helper pointed at a file `/tmp` had taken, and on a VM with no credential
at all. Three different machines, one identical line: a report of a property
never inspected, which is what `DECISIONS.md` D025 forbids.

`instance-20260717-0947` lost every push that way, and this module exists so the
next VM sees it while it is still only a warning. Full rationale, including the
two designs that were tried and rejected, is in
`docs/operations/doctor.md`.

Everything here is a read. No command is executed, no file contents are
returned, and nothing in this module has ever seen a credential value — that is
`pushprobe`'s job, and the split is deliberate so the boundary is visible in the
file layout rather than in a comment.

Key files are reported by path, mode, and byte count. That is the presence-only
rule `docs/policy/permissions-and-safety.md` sets for environment tokens, applied
to the credential this fleet actually uses.
"""

from __future__ import annotations

import os
import re
import stat
from pathlib import Path

from . import gitutil

APP_DIR = "github-app"
KEY_SUFFIXES = (".pem", ".p8", ".key")
APP_ID_NAMES = ("app-id",)
BUILTIN_HELPERS = {"store", "cache"}
# Read to name a helper's shape; never used to fetch anything.
URL_LIKE = re.compile(r"\b[a-zA-Z][a-zA-Z0-9+.-]*://[^\s'\"<>]*")
ABSOLUTE_PATH = re.compile(r"(?<![\w.~$/-])/(?:[A-Za-z0-9._+-]+/)*[A-Za-z0-9._+-]+")
# System paths are durable; flagging them would make every helper look broken.
STABLE_PREFIXES = ("/bin/", "/sbin/", "/usr/", "/etc/", "/lib/", "/opt/")
STABLE_EXACT = {"/dev/null", "/dev/stdin", "/dev/stdout", "/dev/stderr", "/dev/zero"}
MAX_DEPENDENCIES = 20


def home() -> Path:
    return Path(os.path.expanduser("~"))


def app_dir() -> Path:
    base = os.environ.get("XDG_CONFIG_HOME") or str(home() / ".config")
    return Path(base) / APP_DIR


def remote() -> dict:
    """Where pushes go, with any userinfo stripped before it is recorded."""
    name = gitutil.text(["remote"]).splitlines()
    if not name:
        return {"configured": False, "remote": "", "scheme": "", "host": ""}
    target = gitutil.text(["remote", "get-url", name[0]])
    parsed = re.match(r"^(?P<scheme>[a-zA-Z][\w+.-]*)://(?:[^@/]*@)?(?P<host>[^/:]+)", target)
    if not parsed:
        return {"configured": True, "remote": target, "scheme": "", "host": ""}
    return {
        "configured": True,
        "remote": f"{parsed.group('scheme')}://{parsed.group('host')}",
        "scheme": parsed.group("scheme"),
        "host": parsed.group("host"),
    }


def classify(value: str) -> dict:
    """One `credential.helper` value, split into a shape a report can read.

    `store` and `cache` are git's own; `!` is a shell snippet git evaluates;
    anything else is a program to run, with its arguments split off so the
    program itself can be stat'ed rather than the whole command line.
    """
    entry: dict = {"value": value, "kind": "other", "path": ""}
    if value.startswith("!"):
        entry["kind"] = "shell"
    elif value.split(" ", 1)[0] in BUILTIN_HELPERS:
        entry["kind"] = "builtin"
    else:
        program = value.split(" ", 1)[0]
        expanded = Path(os.path.expanduser(program))
        entry.update(
            kind="program",
            path=str(expanded),
            exists=expanded.exists(),
            executable=expanded.exists() and os.access(expanded, os.X_OK),
            mode=_mode(expanded),
            outside_home=sorted(external_paths(expanded)),
        )
    return entry


def _mode(path: Path) -> str:
    try:
        return oct(stat.S_IMODE(path.stat().st_mode)).replace("0o", "")
    except OSError:
        return ""


def helpers() -> list[dict]:
    """Every configured helper, in git's own order. Empty when none is set."""
    result = gitutil.run(["config", "--get-all", "credential.helper"])
    if result.returncode not in (0, 1):
        return []
    return [classify(line.strip()) for line in result.stdout.splitlines() if line.strip()]


def external_paths(script: Path) -> list[str]:
    """Absolute paths a helper script invokes that are not the user's own.

    The fragility being reported is a credential mechanism that depends on
    something outside the home directory: `/tmp` is cleared on reboot, and that
    is exactly how this fleet lost push once already. On `instance-20260717-0944`
    the live helper was intact, mode 0700, and one reboot from failing.

    URLs are removed first so `https://api.github.com/app/...` is not read as a
    path, and the script's text is never returned — only the path tokens, which
    is all a report needs to name the dependency.
    """
    if not script.is_file():
        return []
    try:
        text = script.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    stripped = URL_LIKE.sub(" ", text)
    root = str(home().resolve())
    found: list[str] = []
    for match in ABSOLUTE_PATH.findall(stripped):
        if match in STABLE_EXACT or match.startswith(STABLE_PREFIXES):
            continue
        if match.startswith(root + "/"):
            continue
        if match not in found:
            found.append(match)
    return sorted(found)[:MAX_DEPENDENCIES]


def app_material() -> dict:
    """App key and id files by path, mode, and size. Never their contents."""
    directory = app_dir()
    keys: list[dict] = []
    ids: list[str] = []
    if directory.is_dir():
        for item in sorted(directory.iterdir()):
            if not item.is_file():
                continue
            if item.suffix in KEY_SUFFIXES:
                keys.append({"path": str(item), "mode": _mode(item), "bytes": item.stat().st_size})
            elif item.name in APP_ID_NAMES:
                ids.append(str(item))
    return {"dir": str(directory), "keys": keys, "ids": ids}


def summarize(data: dict) -> str:
    """One line for the human view, then one line per problem worth seeing."""
    target = data["remote"]
    where = f"{target['remote']} via " if target.get("remote") else ""
    helpers = ", ".join(entry["value"] for entry in data["helpers"]) or "no credential.helper"
    parts = [f"{where}{helpers}"]
    if data["app"]["keys"]:
        parts.append(f"{len(data['app']['keys'])} App key file(s)")
    if data["functional"].get("ran"):
        parts.append(
            "credential obtained" if data["functional"]["obtained"] else "no credential obtained"
        )
    elif data["functional"].get("reason"):
        parts.append(f"probe skipped ({data['functional']['reason']})")
    healthy = data["verdict"] == "configured"
    lines = [f"push credential {'OK' if healthy else data['verdict']}: " + "; ".join(parts)]
    lines += [f"  warn  {warning}" for warning in data["warnings"]]
    return "\n".join(lines)