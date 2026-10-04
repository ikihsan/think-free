"""Can git actually obtain a credential here, and what should `doctor` say?

The functional half of the push-credential report T-0024 added to `doctor`. It
runs `git credential fill`, which is the only probe tried that actually
discriminates, and it is the only module in `originlib` that has ever held a
credential value — for the length of one local, from which it keeps a boolean.

Two designs were tried first and are recorded here because both are the failure
this repository keeps making, and both look correct:

* **`git ls-remote <remote>`.** `observed` 2026-10-03: this remote is public
  (`GET /repos/ikihsan/think-free` answers 200 unauthenticated), so `ls-remote`
  exits 0 with no credential at all. A gate built on it could not fail, which is
  `FAILURES.md` F010 with extra steps.
* **Listing the helper files.** `instance-20260717-0947`'s helper survived the
  `/tmp` clear; the script it invoked did not. A report built from listings says
  `configured` on the machine that cannot push.

What `configured` does **not** mean: that the credential can push, or anything
about what it is permitted to do. Proving write authorisation needs either a
write to the remote or the App's settings page, and
`docs/operations/github-app.md` already records that nobody here can read the
latter. The verdict is deliberately coarser than "works", and
`docs/operations/doctor.md` states the whole contract.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

from . import paths, pushcred

PROBE_TIMEOUT = 60


def _carries_secret(ok: bool, stdout: str) -> bool:
    """Whether git's answer contained a *non-empty* password.

    `password=` with nothing after it is not a credential. The first version of
    this check looked for the substring `password=` and so called a healthy
    helper whose token generator had vanished — the same proxy-for-the-clause
    mistake `DECISIONS.md` D024 records, caught by
    `test_the_recorded_defect_shape_is_reported_broken` in
    `tests/test_pushcred.py`.

    The value is read here and goes nowhere else: the caller receives a bool and
    the string it came from is a local, dropped on return.
    """
    if not ok:
        return False
    for line in stdout.splitlines():
        name, _, value = line.partition("=")
        if name.strip() == "password" and value.strip():
            return True
    return False


def functional(scheme: str, host: str, network: bool = True) -> dict:
    """Ask git for a credential and report only whether it got one.

    `git credential fill` writes the secret to stdout. It is captured into a
    local that is never returned, logged, or interpolated into an error, so the
    only things that leave this function are an exit code, a boolean, and git's
    own one-line complaint. Skipped under `--offline`, where the App's helper
    needs the network to mint a token and an offline probe would report a
    credential as missing rather than untested.
    """
    if not scheme or not host:
        return {"ran": False, "reason": "no https remote to authenticate against"}
    if not network:
        return {"ran": False, "reason": "offline"}
    try:
        done = subprocess.run(
            ["git", "credential", "fill"],
            input=f"protocol={scheme}\nhost={host}\n\n",
            cwd=str(paths.repo_root()),
            capture_output=True,
            text=True,
            timeout=PROBE_TIMEOUT,
            check=False,
            env={
                **os.environ,
                "GIT_TERMINAL_PROMPT": "0",
                "GIT_ASKPASS": "",
                "GIT_CONFIG_SYSTEM": "/dev/null",
            },
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return {"ran": True, "exit_code": None, "obtained": False, "git_said": str(exc)[:160]}
    complaint = ""
    for line in (done.stderr or "").strip().splitlines():
        if "fatal:" in line or "error:" in line or "invalid credential" in line:
            complaint = line.strip()[:160]
    return {
        "ran": True,
        "exit_code": done.returncode,
        "obtained": _carries_secret(done.returncode == 0, done.stdout or ""),
        "git_said": complaint,
    }


def collect(network: bool = True) -> dict:
    """Everything about this machine's push credential, and a verdict on it."""
    target = pushcred.remote()
    configured = pushcred.helpers()
    material = pushcred.app_material()
    probe = functional(target["scheme"], target["host"], network=network)
    warnings: list[str] = []

    for entry in configured:
        if entry["kind"] != "program":
            continue
        if not entry.get("exists"):
            warnings.append(f"credential.helper names {entry['path']}, which does not exist")
        elif not entry.get("executable"):
            warnings.append(f"credential.helper names {entry['path']}, which is not executable")
        for dependency in entry.get("outside_home", []):
            warnings.append(
                f"{entry['path']} depends on {dependency}, outside this user's home directory"
            )
    for key in material["keys"]:
        if key["mode"] not in ("600", "400"):
            warnings.append(
                f"{key['path']} is mode {key['mode']}; a private key must be 0600 or 0400"
            )

    broken_helper = any(
        entry["kind"] == "program" and not (entry.get("exists") and entry.get("executable"))
        for entry in configured
    )
    any_mechanism = bool(
        [name for name in ("GH_TOKEN", "GITHUB_TOKEN") if os.environ.get(name)]
        or configured
        or material["keys"]
    )
    # Order matters, and the first version had it backwards: a machine with no
    # credential at all was reported `broken`, which is the incident that cost
    # this fleet a push and would send the next agent hunting a helper that was
    # never configured. Absence and breakage are different states.
    if not any_mechanism:
        verdict = "unavailable"
        if probe["ran"]:
            warnings.append(
                "no credential mechanism is configured, so git has nothing to obtain one with"
            )
    elif broken_helper:
        verdict = "broken"
    elif probe["ran"] and not probe["obtained"]:
        verdict = "broken"
        warnings.insert(0, probe["git_said"] or "git could not obtain a credential")
    else:
        verdict = "configured"

    return {
        "verdict": verdict,
        "remote": target,
        "helpers": configured,
        "app": material,
        "functional": probe,
        "warnings": warnings,
    }