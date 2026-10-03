"""Environment verification.

Answers one question honestly: can this machine do the work a task requires?
Runs before a VM picks up a task, so an environment limitation is recorded as a
limitation rather than discovered as a mysterious failure.

Writes raw results to `.origin/doctor.json` (gitignored) and prints a summary.
"""

from __future__ import annotations

import json
import os
import platform
import shutil
import subprocess
import urllib.error
import urllib.request
from datetime import datetime

from . import gitutil, paths

OUTPUT = ".origin/doctor.json"
PROBES = (
    ("github_api", "https://api.github.com/repos/python/cpython"),
    ("arxiv", "https://arxiv.org/abs/1805.06358"),
)
TIMEOUT = 10
# Presence only. Values are never read, printed, or stored.
CREDENTIAL_ENV = ("GH_TOKEN", "GITHUB_TOKEN", "ANTHROPIC_API_KEY", "OPENAI_API_KEY")
VERSIONS = (
    ("python3", ["--version"]),
    ("git", ["--version"]),
    ("node", ["--version"]),
    ("rustc", ["--version"]),
    ("gcc", ["--version"]),
)


def _version(name: str, args: list[str]) -> dict:
    binary = shutil.which(name)
    if not binary:
        return {"present": False}
    try:
        result = subprocess.run(
            [name, *args], capture_output=True, text=True, timeout=20, check=False
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return {"present": True, "error": str(exc)}
    output = (result.stdout or result.stderr).strip().splitlines()
    return {"present": True, "path": binary, "version": output[0] if output else ""}


def _http(url: str) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": "origin-doctor"})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            body = response.read(2048)
            return {"status": response.status, "bytes_read": len(body)}
    except urllib.error.HTTPError as exc:
        return {"status": exc.code, "error": str(exc)}
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return {"status": None, "error": str(exc)}


def _memory() -> dict:
    info: dict = {}
    try:
        with open("/proc/meminfo", encoding="utf-8") as handle:
            for line in handle:
                key, _, value = line.partition(":")
                if key in {"MemTotal", "MemAvailable"}:
                    info[key] = value.strip()
    except OSError:
        info["error"] = "/proc/meminfo unreadable"
    return info


def _disk() -> dict:
    usage = shutil.disk_usage(paths.repo_root())
    return {"total_bytes": usage.total, "free_bytes": usage.free}


def _scheduler() -> dict:
    return {
        "crontab": bool(shutil.which("crontab")),
        "systemctl": bool(shutil.which("systemctl")),
        "systemd_user_running": _systemd_user_running(),
    }


def _systemd_user_running() -> bool | None:
    if not shutil.which("systemctl"):
        return None
    try:
        result = subprocess.run(
            ["systemctl", "--user", "is-system-running"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return result.stdout.strip() == "running"


def collect(network: bool = True) -> dict:
    root = paths.repo_root()
    git = gitutil.state()
    return {
        "schema": "origin.doctor/1",
        "observed_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "platform": platform.platform(),
        "python": platform.python_version(),
        "cpu_count": os.cpu_count(),
        "memory": _memory(),
        "disk": _disk(),
        "versions": {name: _version(name, args) for name, args in VERSIONS},
        "git": git.as_dict(),
        "credentials_present": {name: bool(os.environ.get(name)) for name in CREDENTIAL_ENV},
        "scheduler": _scheduler(),
        "network": {label: _http(url) for label, url in PROBES} if network else "skipped",
        "notes": [
            "credential checks test environment-variable presence only; values are never read",
            "resource figures are a snapshot on shared hardware and will fluctuate",
        ],
    }


def write(data: dict) -> str:
    target = paths.repo_root() / OUTPUT
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return OUTPUT


def summarize(data: dict) -> str:
    lines = [
        f"platform        {data['platform']}",
        f"python          {data['python']}",
        f"cpus            {data['cpu_count']}",
        f"memory          {data['memory'].get('MemTotal', '?')} (available {data['memory'].get('MemAvailable', '?')})",
        f"disk free       {data['disk']['free_bytes'] // (1024 * 1024)} MiB",
        f"git             head={data['git']['head'][:8] or 'none'} branch={data['git']['branch']} clean={data['git']['clean']}",
    ]
    for name, info in data["versions"].items():
        lines.append(f"tool {name:<11} {info.get('version') or ('absent' if not info.get('present') else 'unknown')}")
    for name, info in (data["network"] if isinstance(data["network"], dict) else {}).items():
        lines.append(f"net  {name:<11} status={info.get('status')} {info.get('error', '')}".rstrip())
    present = [name for name, value in data["credentials_present"].items() if value]
    lines.append(f"credentials     {', '.join(present) if present else 'none present'}")
    sched = data["scheduler"]
    lines.append(
        f"scheduler       crontab={sched['crontab']} systemd_user={sched['systemd_user_running']}"
    )
    return "\n".join(lines)