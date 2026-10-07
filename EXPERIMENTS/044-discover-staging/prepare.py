#!/usr/bin/env python3
"""Prepare one agent trial: a fresh copy of a fixture, a git shim, the task.

Usage: prepare.py <experiment-root> <scenario> <arm>

`arm` is `stg` or `nostg`. Prints the trial directory, then the task file.

Layout, and why:

* trials/<scenario>-<arm>-trial/ -- the ONLY directory the agent is told
  about. Its parent holds only sibling trials. A trial contains exactly
  `app.py` and `.git`; this script asserts that, because E043 lost a run to
  an agent reading the oracle file that was sitting in its trial.

* oracle/ -- the answers, the task texts, and the shim logs. The agent is
  never given a path into it.

* gitbin/<trial>/git -- a policy shim that refuses `git diff` (the simulated
  harness restriction) and logs every call with cwd, the STG_INTERNAL marker,
  and the exit status. The log is the compliance record: an agent whose
  report claims git commands the log does not show went around the shim, and
  that run is not evidence. The shim passes `diff` through when STG_INTERNAL
  is set, which only the `stg` launcher does -- the tool's own plumbing is
  not the agent reading a diff, which is the thing being simulated away.

Arm integrity: the `stg` arm installs a real launcher into /usr/local/bin
(E043's first pass dropped `stg` into an untracked .bin/ and three agents
reported `command not found` -- a treatment arm that was not one); the
`nostg` arm REMOVES that launcher and asserts `stg` resolves nowhere on
PATH, so run order cannot contaminate either arm.
"""

import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))          # think-free/
STG_DIR = os.path.join(ROOT, "stage-lines")
REAL_BIN_DIR = "/usr/local/bin"

SHIM = """\
#!/bin/sh
# E044 policy shim: this harness gives agents no `git diff` output.
# Logs every call: time, cwd, STG_INTERNAL marker, args, exit status.
LOG="@@LOG@@"
printf '%s\\t%s\\t%s\\t%s\\n' "$(date -u +%H:%M:%S)" "$(pwd)" \\
    "${STG_INTERNAL:--}" "$*" >> "$LOG"
if [ -z "$STG_INTERNAL" ]; then
    for a in "$@"; do
        if [ "$a" = "diff" ]; then
            printf '%s\\tREFUSED\\tdiff\\n' "$(date -u +%H:%M:%S)" >> "$LOG"
            echo "git: diff output is disabled in this environment" >&2
            exit 1
        fi
    done
fi
"@@REALGIT@@" "$@"
rc=$?
printf '%s\\trc=%d\\n' "$(date -u +%H:%M:%S)" "$rc" >> "$LOG"
exit $rc
"""

LAUNCHER = """\
#!/bin/sh
# E044 stg launcher. STG_INTERNAL lets the tool's own plumbing through the
# policy shim; the agent's shell does not have it set.
STG_INTERNAL=1
export STG_INTERNAL
exec @@PY@@ @@STGDIR@@/stg_cli.py "$@"
"""

TASK = """\
You are working in the git repository at {trial}. It has one committed file,
app.py, which now has uncommitted edits.

Environment policy: this harness does not give agents `git diff` output. The
`git` on your PATH is a policy wrapper that refuses `git diff`. Do not bypass
the wrapper -- for example by calling another git binary directly, or by
re-enabling diff output: a run that reads diff output is invalid and will be
discarded. You may read the committed version with `git show HEAD:app.py`,
the staged version with `git show :app.py`, and the working copy with
`cat app.py`.

Begin EVERY shell command with:
    export PATH={gitbin}:$PATH &&
(the shell may not remember environment between commands, so re-export each
time).

Task: {describe} You are NOT told a line number. Work out which change is
meant -- and exactly which working-tree line it sits on -- by comparing the
committed and working versions. Stage only that change; leave every other
change unstaged. Do not commit anything. Work only inside this repository
directory; do not read or modify anything outside it.

When you are done, report: how you identified the line to stage, the exact
commands you ran in order, and whether staging succeeded. If you believe the
staged result is wrong, say so.
{tool_hint}"""

# Per-scenario description of the ONE change to stage, phrased semantically.
# The agent is never told a line number.
DESCRIBE = {
    "adjacent-modifications": (
        "Stage ONLY the change that decodes the file's content as UTF-8 "
        "(the addition of `.decode(\"utf-8\")`). Leave the adjacent "
        "change that opens the file in binary mode unstaged."),
    "two-line-insertion": (
        "Stage ONLY the change that adds the line `import json`. Leave "
        "the adjacent `import re` insertion unstaged."),
    "one-edit-among-three": (
        "Stage ONLY the change that selects the last command-line "
        "argument when printing (`sys.argv[-1]`). Leave the other two "
        "edits unstaged."),
}

TRIAL_ALLOWED = ("app.py", ".git")


def sh(args, cwd=None):
    p = subprocess.Popen(args, cwd=cwd, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out, err = p.communicate()
    return p.returncode, out.decode("utf-8", "replace"), err.decode("utf-8", "replace")


def main():
    root, scenario, arm = sys.argv[1], sys.argv[2], sys.argv[3]
    fixtures = os.path.join(root, "fixtures")
    trials = os.path.join(root, "trials")
    oracle = os.path.join(root, "oracle")
    gitbins = os.path.join(root, "gitbin")
    name = scenario + "-" + arm
    src = os.path.join(fixtures, name)
    trial = os.path.join(trials, name + "-trial")
    if os.path.exists(trial):
        shutil.rmtree(trial)
    os.makedirs(trials, exist_ok=True)
    shutil.copytree(src, trial)

    stray = sorted(f for f in os.listdir(trial) if f not in TRIAL_ALLOWED)
    if stray:
        raise RuntimeError("fixture carries files the agent must not see: "
                           + ", ".join(stray))

    with open(os.path.join(oracle, scenario + ".line")) as fh:
        line = int(fh.read().strip())

    # Per-trial shim. The log lands in oracle/, outside anything the agent
    # is told about.
    gitbin = os.path.join(gitbins, name + "-trial")
    os.makedirs(gitbin, exist_ok=True)
    real_git = shutil.which("git")
    log = os.path.join(oracle, "shim-%s.log" % name)
    if os.path.exists(log):
        os.remove(log)
    shim = os.path.join(gitbin, "git")
    with open(shim, "w") as fh:
        fh.write(SHIM.replace("@@REALGIT@@", real_git)
                     .replace("@@LOG@@", os.path.abspath(log)))
    os.chmod(shim, 0o755)

    hint = ""
    launcher = os.path.join(REAL_BIN_DIR, "stg")
    if arm == "stg":
        rc, py, _ = sh(["which", "python3"])
        py = py.strip() or sys.executable or "python3"
        with open(launcher, "w") as fh:
            fh.write(LAUNCHER.replace("@@PY@@", py)
                             .replace("@@STGDIR@@", STG_DIR))
        os.chmod(launcher, 0o755)
        rc, out, err = sh(["stg", "--help"], trial)
        if rc != 0 or "stg" not in out:
            raise RuntimeError("stg not resolvable on PATH: " + err)
        hint = ("\nNote: a command named `stg` is on PATH. `stg --help` "
                "documents it. Use it if it helps; it is not required.\n")
    else:
        if os.path.exists(launcher):
            os.remove(launcher)
        rc, out, _ = sh(["which", "stg"])
        if rc == 0:
            raise RuntimeError("stg still resolves on PATH in a nostg arm: "
                               + out)

    text = TASK.format(trial=os.path.abspath(trial),
                       describe=DESCRIBE[scenario],
                       gitbin=os.path.abspath(gitbin),
                       tool_hint=hint)
    taskfile = os.path.join(oracle, "%s.%s.task.txt" % (scenario, arm))
    with open(taskfile, "w") as fh:
        fh.write(text)
    print(trial)
    print(taskfile)


if __name__ == "__main__":
    main()
