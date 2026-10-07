#!/usr/bin/env python3
"""Prepare one agent trial: a fresh copy of a fixture, and the task text.

Usage: prepare.py <fixture-root> <scenario> <arm>

`arm` is `stg` or `nostg`. Prints the trial directory.

The trial directory must contain ONLY what the agent is allowed to see. The
oracle and the requested-line number are hoisted into <fixture-root>/oracle/
so an agent cannot read them: an agent that diffs against `.expected_index` is
scoring itself, and a run that did that is contaminated, not evidence.
"""

import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))       # EXPERIMENTS/043-.../
EXPERIMENTS = os.path.dirname(HERE)                     # EXPERIMENTS/
ROOT = os.path.dirname(EXPERIMENTS)                     # think-free/
STG_DIR = os.path.join(ROOT, "stage-lines")
# A directory already on PATH, so "stg is installed" is literally true for the
# agent rather than true only inside the fixture.
REAL_BIN_DIR = "/usr/local/bin"

TASK = """\
You are working in the git repository at {trial}. It has one committed file,
app.py, with uncommitted edits.

Task: stage ONLY the change on line {line} of app.py. Leave every other
change unstaged. Do not commit.

When you are done, report what you did: the commands you ran, and whether
staging succeeded.
{tool_hint}"""

# Never leave these in a trial the agent can read.
QUARANTINE = (".expected_index", ".requested_line", ".task.txt")


def sh(args, cwd=None):
    p = subprocess.Popen(args, cwd=cwd, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out, err = p.communicate()
    return p.returncode, out.decode("utf-8", "replace"), err.decode("utf-8", "replace")


def main():
    fixture_root, scenario, arm = sys.argv[1], sys.argv[2], sys.argv[3]
    src = os.path.join(fixture_root, scenario + "-" + arm)
    trial = src + "-trial"
    if os.path.exists(trial):
        shutil.rmtree(trial)
    shutil.copytree(src, trial)

    with open(os.path.join(trial, ".requested_line")) as fh:
        line = int(fh.read().strip())

    oracle_dir = os.path.join(fixture_root, "oracle")
    os.makedirs(oracle_dir, exist_ok=True)
    shutil.copyfile(os.path.join(trial, ".expected_index"),
                    os.path.join(oracle_dir, scenario + ".index"))
    with open(os.path.join(oracle_dir, scenario + ".line"), "w") as fh:
        fh.write("%d\n" % line)
    for junk in QUARANTINE:
        p = os.path.join(trial, junk)
        if os.path.exists(p):
            os.remove(p)

    hint = ""
    if arm == "stg":
        # The tool must be genuinely on the PATH the agent runs under, not
        # merely dropped in the repository: three agents reported
        # `stg: command not found` when it sat in an untracked .bin/, which
        # silently turns the stg arm into a second nostg arm. Install a real
        # launcher into a PATH directory for the duration of the trial.
        bindir = REAL_BIN_DIR
        os.makedirs(bindir, exist_ok=True)
        rc, py, _ = sh(["which", "python3"])
        py = py.strip() or "python3"
        launcher = os.path.join(bindir, "stg")
        with open(launcher, "w") as fh:
            fh.write('#!/bin/sh\nexec %s %s/stg_cli.py "$@"\n'
                     % (py, STG_DIR))
        os.chmod(launcher, 0o755)
        rc, _, err = sh(["stg", "--help"], trial)
        if rc != 0:
            raise RuntimeError("stg not resolvable on PATH: " + err)
        hint = ("\n\nNote: a command named `stg` is on PATH. `stg --help` "
                "documents it. Use it if it helps; it is not required.\n")

    text = TASK.format(trial=trial, line=line, tool_hint=hint)
    # Record the prompt outside the trial, so the agent cannot read its own
    # instructions back.
    with open(os.path.join(oracle_dir, scenario + "." + arm + ".task.txt"),
              "w") as fh:
        fh.write(text)
    print(trial)


if __name__ == "__main__":
    main()