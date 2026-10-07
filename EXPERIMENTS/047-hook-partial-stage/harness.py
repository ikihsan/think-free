#!/usr/bin/env python3
"""E047 — does a shipped git hook runner fold a partially-staged file's
unstaged hunk into the commit?

The oracle is bytes and nothing else. The claim under test is a correctness
claim: a specific line of content that the user chose not to stage reaches their
commit. There is nothing to grade, score, or ask a model about. `git show :app.js`
and `git cat-file blob HEAD:app.js` either contain the marker or they do not.

Why the commit is made by git and not by the harness. Three of these runners
protect the user by manipulating the index and the worktree *around* the hook —
lint-staged calls it stashing, lefthook calls it hiding, pre-commit does it too.
That is the mechanism under test, so the hook must be reached the way a user
reaches it: `git commit`, through the runner's own installed hook. Invoking
`lefthook run pre-commit` by hand and committing with `--no-verify` would skip
the hiding and report a sweep for lefthook that a real user never gets.

Two readings, because a hook may block the commit rather than make it. What the
runner *staged* is read from the index; what the user would *get* is read from
the commit when one exists. The verdict prefers the commit, because the claim is
about the commit. An arm that reformats and blocks is recorded as blocked, with
its index state, rather than being silently turned into a clean result.

The positive control, and why the experiment is void without it. C0 is the naive
hand-written hook: format the file, `git add` the file. That pattern is what the
two issues in the corpus describe, and everyone agrees it sweeps. If C0 does not
report a sweep on these bytes, this harness cannot detect a sweep, and every
other arm's "clean" is a fact about the harness rather than about the runner. C0
runs first and the run exits non-zero if it does not fail. A gate that cannot
fail is F010; this one is required to fail on the arm it was built to fail on.

The fixture. One file, `app.js`, twelve lines, two changed regions six unchanged
lines apart so they cannot collapse into one hunk at git's default context:

  * region A (staged) — badly spaced, so `prettier --write` must rewrite it. An
    arm where the formatter did not run cannot report "clean" meaningfully, so
    `formatter_ran` is checked on every arm and an arm that fails it is
    INCONCLUSIVE rather than clean.
  * region B (unstaged) — a marker line, already well formatted, so prettier
    leaves its bytes alone and the only way it reaches the commit is by being
    staged.

Staging is arranged without any interactive command: region A is written and
staged while region B does not yet exist, so `git add app.js` stages exactly the
hunk region B later modifies. That is `git add -p` with the answer already
known, and it keeps every arm independent of this repository's own tooling.

Run: python3 EXPERIMENTS/047-hook-partial-stage/harness.py
Writes raw/results.json. Exit 0 when the control failed as required, 1 otherwise.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
ROOT = os.environ.get("E047_ROOT", "/tmp/opencode/e047")
MARKER = "UNSTAGED_SWEEP_MARKER"
REFORMATTED = "const a = 1;"
BADSPACED = "const a   =   1;"

GOOD = """\
// fixture header
const a = 1;
// separator one
// separator two
// separator three
// separator four
// separator five
const b = 2;
// footer one
// footer two
"""

WORKTREE = """\
// fixture header
const a   =   1;
// separator one
// separator two
// separator three
// separator four
// separator five
const %s = "swept";
const b = 2;
// footer one
// footer two
""" % MARKER


class ArmError(Exception):
    pass


def git_bin():
    """The git this experiment runs, which is not necessarily the VM's git.

    lefthook 2.x requires git >= 2.31 and lint-staged 17 requires >= 2.32, so
    `setup.sh` builds a current git and this harness uses it throughout. Staying
    on the system git would have made both runners refuse to start, and the
    results would have recorded that as "no sweep" for arms that never ran.
    """
    built = os.path.join(ROOT, "git", "bin", "git")
    return built if os.path.exists(built) else "git"


def git(repo, *args):
    p = subprocess.run([git_bin(), "-C", repo] + list(args),
                       capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError("git %s -> %s" % (" ".join(args), p.stderr.strip()))
    return p.stdout


def sh(cmd, cwd, timeout=240):
    p = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True,
                       text=True, timeout=timeout, env=env(repo=cwd))
    return p.returncode, p.stdout + p.stderr


def env(repo=None, **extra):
    e = dict(os.environ)
    e["PATH"] = os.path.join(ROOT, "node", "bin") + ":" \
        + os.path.join(ROOT, "git", "bin") + ":" \
        + os.path.join(ROOT, "bin") + ":" + e.get("PATH", "")
    e["E047_ROOT"] = ROOT
    e["npm_config_yes"] = "true"
    if repo:
        e["LEFTHOOK_VERBOSE"] = "1"
    e.update(extra)
    return e


def node_bin():
    """Absolute path to the node this experiment installed.

    Absolute, never from PATH: git replaces PATH inside a hook with its own
    `/usr/local/sbin:...:/bin` list, so a hook body that says `node` gets
    "node: not found" on a machine where node is installed and on PATH. That
    cost one run here, and it produced two arms that did nothing at all while
    reporting an error rather than a result.
    """
    return os.path.join(ROOT, "node", "bin", "node")


def prettier_cmd(repo, *args):
    return "%s %s %s" % (node_bin(),
                         os.path.join(ROOT, "npm", "node_modules", "prettier",
                                      "bin", "prettier.cjs"),
                         " ".join(args))


def build_repo():
    """A repo with region A staged and region B unstaged, byte for byte."""
    repo = tempfile.mkdtemp(prefix="e047-")
    # `git init -b` needs git 2.28 and this VM runs 2.25.1, so the branch name
    # is set the portable way. The branch's name is irrelevant to the oracle;
    # that the first commit is the one `base` is not.
    git(repo, "init", "-q")
    git(repo, "checkout", "-q", "-b", "main")
    git(repo, "config", "user.email", "e047@example.invalid")
    git(repo, "config", "user.name", "E047")
    git(repo, "config", "commit.gpgsign", "false")
    git(repo, "config", "core.autocrlf", "false")
    path = os.path.join(repo, "app.js")
    with open(path, "w") as fh:
        fh.write(GOOD)
    git(repo, "add", "app.js")
    git(repo, "commit", "-q", "-m", "base")
    # Region A only: the marker does not exist yet, so this stages exactly A.
    with open(path, "w") as fh:
        fh.write(GOOD.replace(REFORMATTED, BADSPACED))
    git(repo, "add", "app.js")
    # Now region B appears in the worktree and stays unstaged.
    with open(path, "w") as fh:
        fh.write(WORKTREE)
    return repo


def verify_fixture(repo):
    """Assert the fixture is what the experiment claims, before any arm runs."""
    staged = git(repo, "show", ":app.js")
    worktree = open(os.path.join(repo, "app.js")).read()
    unstaged = git(repo, "diff", "--", "app.js")
    problems = []
    if MARKER in staged:
        problems.append("the marker is already staged")
    if BADSPACED not in staged:
        problems.append("region A is not staged")
    if MARKER not in worktree:
        problems.append("the marker is not in the worktree")
    if MARKER not in unstaged:
        problems.append("the marker is not in the unstaged diff")
    # Counted as hunk *headers*, not occurrences of "@@": git writes two per
    # header (`@@ -a,b +c,d @@`) plus optional trailing context, so a substring
    # count reports two for every single hunk. That mistake made a correct
    # fixture look broken on this experiment's first run.
    hunks = sum(1 for line in unstaged.splitlines() if line.startswith("@@"))
    if hunks != 1:
        problems.append("the unstaged diff has %d hunks, expected 1" % hunks)
    return problems


def read(repo, rev, path="app.js"):
    try:
        return git(repo, "show", "%s:%s" % (rev, path))
    except RuntimeError:
        return None


def head_moved(repo):
    try:
        return git(repo, "log", "-1", "--format=%s").strip() != "base"
    except RuntimeError:
        return False


def judge(repo):
    """The question, on bytes, with the control that gives it an answer."""
    index_blob = read(repo, ":")
    commit_blob = read(repo, "HEAD") if head_moved(repo) else None
    primary, source = ((commit_blob, "commit")
                       if commit_blob is not None
                       else (index_blob, "index"))
    if primary is None:
        return {"error": "neither a commit nor a readable index", "verdict": "ERROR"}
    worktree = open(os.path.join(repo, "app.js")).read() \
        if os.path.exists(os.path.join(repo, "app.js")) else ""
    formatter_ran = REFORMATTED in primary and BADSPACED not in primary
    swept = MARKER in primary
    if not formatter_ran:
        verdict = "INCONCLUSIVE: the formatter did not run, so nothing was tested"
    elif swept:
        verdict = "SWEEP"
    else:
        verdict = "clean"
    return {
        "swept": swept,
        "formatter_ran": formatter_ran,
        "read_from": source,
        "commit_made": commit_blob is not None,
        "marker_left_in_worktree": MARKER in worktree,
        "index_blob": index_blob,
        "committed_blob": commit_blob,
        "worktree_after": worktree,
        "verdict": verdict,
    }


def write(path, text, executable=False):
    with open(path, "w") as fh:
        fh.write(text)
    if executable:
        os.chmod(path, 0o755)
    return path


def run_arm(name, install, note="", expect_sweep=None, keep=False):
    """Build the fixture, let the arm install itself, commit, and judge.

    `install` writes the runner's configuration into the repo and is the only
    thing that differs between arms of the same runner. `expect_sweep` is the
    arm's declared prediction; recording it is what lets a post-hoc reading of
    the results be checked against what was expected beforehand.
    """
    repo = build_repo()
    problems = verify_fixture(repo)
    if problems:
        shutil.rmtree(repo, ignore_errors=True)
        return {"arm": name, "error": "fixture: " + "; ".join(problems),
                "verdict": "ERROR", "expect_sweep": expect_sweep}
    install_log = ""
    try:
        install_log = install(repo)
    except Exception as exc:
        shutil.rmtree(repo, ignore_errors=True)
        return {"arm": name, "error": "install: %s" % exc, "verdict": "ERROR",
                "install_log": install_log, "expect_sweep": expect_sweep}
    code, log = sh("git commit -q -m under-test", repo)
    result = judge(repo)
    result.update({
        "arm": name,
        "note": note,
        "expect_sweep": expect_sweep,
        "commit_exit": code,
        "commit_log": log[-3000:],
        "install_log": str(install_log)[-2000:],
    })
    result["matched_expectation"] = (
        None if expect_sweep is None
        else (result.get("swept") == expect_sweep
              and result.get("formatter_ran") is True)
    )
    if keep or os.environ.get("E047_KEEP"):
        result["repo"] = repo
    else:
        shutil.rmtree(repo, ignore_errors=True)
    return result


# --- arms ------------------------------------------------------------------
# Each install() is the runner's real configuration, copied from its own
# documentation rather than invented here. `expect_sweep` is the prediction the
# arm's own source and documentation imply, recorded before it runs.


def install_naive(repo):
    """C0 — the hand-written hook the corpus issues describe.

    Format the file, stage the file. The pattern `git add -p` defeats, and the
    positive control the whole experiment rests on.
    """
    hooks = os.path.join(repo, ".git", "hooks")
    os.makedirs(hooks, exist_ok=True)
    write(os.path.join(hooks, "pre-commit"),
          "#!/bin/sh\n"
          "%s --write app.js\n"
          "git add -- app.js\n" % prettier_cmd(repo),
          executable=True)
    return "wrote .git/hooks/pre-commit"


def install_none(repo):
    """B0 — no hook at all.

    Establishes that the fixture's marker does not reach a commit on its own.
    Without this, a "clean" arm cannot be distinguished from a fixture that was
    never staged the way the experiment says it was.
    """
    return "no hook installed"


def install_lefthook(repo):
    """A1 — lefthook with `stage_fixed`, the pattern the corpus issue names."""
    write(os.path.join(repo, "lefthook.yml"),
          "pre-commit:\n"
          "  parallel: false\n"
          "  jobs:\n"
          "    - name: format\n"
          "      glob: \"*.js\"\n"
          "      run: %s --write {staged_files}\n"
          "      stage_fixed: true\n" % prettier_cmd(repo))
    code, log = sh("%s/bin/lefthook install" % ROOT, repo)
    return "lefthook install -> %d\n%s" % (code, log)


def install_lefthook_nofix(repo):
    """A1b — lefthook with `stage_fixed` absent.

    The control for A1: if A1 is clean and this one sweeps, then `stage_fixed`
    is doing the hiding, which is the claim under test rather than lefthook's
    general behaviour.
    """
    write(os.path.join(repo, "lefthook.yml"),
          "pre-commit:\n"
          "  parallel: false\n"
          "  jobs:\n"
          "    - name: format\n"
          "      glob: \"*.js\"\n"
          "      run: %s --write {staged_files}\n" % prettier_cmd(repo))
    code, log = sh("%s/bin/lefthook install" % ROOT, repo)
    return "lefthook install -> %d\n%s" % (code, log)


def install_precommit(repo):
    """A2 — pre-commit, with the hook body a pre-commit user has to write.

    pre-commit supplies the framework; the staging decision inside the hook is
    the user's. So this arm is the naive pattern reached through pre-commit, and
    it is the arm that shows whether pre-commit's own unstaged-change handling
    covers a hook that stages explicitly.
    """
    write(os.path.join(repo, ".pre-commit-config.yaml"),
          "repos:\n"
          "  - repo: local\n"
          "    hooks:\n"
          "      - id: format-and-stage\n"
          "        name: format and stage\n"
          "        entry: bash -c '%s --write app.js; git add -- app.js'\n"
          "        language: system\n"
          "        pass_filenames: false\n"
          "        always_run: true\n" % prettier_cmd(repo))
    code, log = sh("%s/venv/bin/pre-commit install" % ROOT, repo)
    return "pre-commit install -> %d\n%s" % (code, log)


def install_lintstaged(extra_flags=""):
    """A3 — lint-staged, wired the way its own documentation wires it.

    lint-staged is a CLI, not a framework: the wiring is a git hook that calls
    it. Writing only `.lintstagedrc.json` would leave the arm doing nothing and
    reporting "clean" for the wrong reason, so the hook is installed here and it
    is that hook which reaches the commit.
    """
    def _install(repo):
        write(os.path.join(repo, ".lintstagedrc.json"),
              '{"*.js": "%s --write"}\n' % prettier_cmd(repo))
        write(os.path.join(repo, "package.json"),
              '{"name":"e047","private":true}\n')
        hooks = os.path.join(repo, ".git", "hooks")
        os.makedirs(hooks, exist_ok=True)
        write(os.path.join(hooks, "pre-commit"),
              "#!/bin/sh\n"
              "exec %s %s %s\n"
              % (node_bin(),
                 os.path.join(ROOT, "npm", "node_modules", "lint-staged",
                              "bin", "lint-staged.js"),
                 extra_flags),
              executable=True)
        return ("wrote .lintstagedrc.json and a pre-commit hook calling "
                "lint-staged %s" % (extra_flags or "(no flags: the defaults)"))
    return _install


def install_lintstaged_nostash(repo):
    """A4 — lint-staged with `--no-stash`.

    The control for A3. Stashing is lint-staged's documented default protection
    and `--no-stash` is the documented way to turn it off, so if A3 is clean and
    this one sweeps, the protection is the default rather than an accident.
    """
    return install_lintstaged("--no-stash")(repo)


def install_husky(repo):
    """A5 — husky, which supplies no staging of its own.

    husky v9 keeps the user's scripts in `.husky/` and points `core.hooksPath`
    at its own dispatcher. Its installer is driven by an npm lifecycle script,
    which a bare test repository has no equivalent of, so `core.hooksPath` is
    set to `.husky` directly. That is the dispatcher git ends up running the
    user's `.husky/pre-commit` through anyway; the deviation is recorded because
    it is a deviation.
    """
    os.makedirs(os.path.join(repo, ".husky"), exist_ok=True)
    write(os.path.join(repo, "package.json"),
          '{"name":"e047","private":true,"devDependencies":{}}\n')
    write(os.path.join(repo, ".husky", "pre-commit"),
          "%s --write app.js\ngit add -- app.js\n" % prettier_cmd(repo),
          executable=True)
    git(repo, "config", "core.hooksPath", ".husky")
    return "wrote .husky/pre-commit and set core.hooksPath=.husky"


def install_stash_idiom(repo):
    """X1 — the strongest accessible alternative, with no framework at all.

    `git stash push --keep-index` hides the unstaged half around the formatter,
    which is a documented git idiom available to anyone. If this is clean, the
    hazard has a two-line remedy that does not need a new tool, and that is a
    fact about the candidate's value, not only about lefthook.
    """
    write(os.path.join(repo, ".git", "hooks", "pre-commit"),
          "#!/bin/sh\n"
          "git stash push --keep-index -q -m e047-hide || exit 0\n"
          "trap 'git stash pop -q' EXIT INT TERM\n"
          "%s --write app.js\n"
          "git add -- app.js\n" % prettier_cmd(repo),
          executable=True)
    return "wrote .git/hooks/pre-commit with git stash push --keep-index"


ARMS = [
    ("C0-naive-shell-hook", install_naive,
     "positive control: the hand-written hook the corpus issues describe",
     True),
    ("B0-no-hook", install_none,
     "control: the fixture does not commit the marker on its own", False),
    ("A1-lefthook-stage_fixed", install_lefthook,
     "lefthook with stage_fixed, the pattern nextjs-app-template#95 names",
     None),
    ("A1b-lefthook-no-stage_fixed", install_lefthook_nofix,
     "lefthook without stage_fixed: isolates what stage_fixed does", None),
    ("A2-precommit-local-hook", install_precommit,
     "pre-commit, hook body stages explicitly", True),
    ("A3-lint-staged-default", install_lintstaged(),
     "lint-staged on its default configuration", None),
    ("A4-lint-staged-no-stash", install_lintstaged_nostash,
     "lint-staged with --no-stash", None),
    ("A5-husky", install_husky,
     "husky: no staging of its own, so the naive pattern again", True),
    ("X1-git-stash-keep-index", install_stash_idiom,
     "the plain git idiom, no framework", False),
]


def main():
    os.makedirs(RAW, exist_ok=True)
    results = []
    for name, install, note, expect in ARMS:
        result = run_arm(name, install, note=note, expect_sweep=expect)
        results.append(result)
        print("%-30s %-14s expect_sweep=%-5s %s"
              % (name, result.get("verdict", "?"), expect,
                 (result.get("error") or "")[:80]))
    control = results[0]
    control_failed = control.get("swept") is True
    # The second control, on the fixture rather than on a runner: with no hook at
    # all the marker must stay out of the commit, and the formatter must not have
    # run. If either fails, the fixture is not the repository the experiment
    # describes and every arm is measuring something else.
    blank = next((r for r in results if r["arm"] == "B0-no-hook"), {})
    fixture_ok = (blank.get("swept") is False
                  and blank.get("formatter_ran") is False)
    payload = {
        "fixture": {
            "good": GOOD,
            "worktree_under_test": WORKTREE,
            "marker": MARKER,
            "note": "region A staged and badly spaced; region B the unstaged "
                    "marker line. Six unchanged lines apart, so they are two "
                    "hunks at git's default context.",
        },
        "versions": read_versions(),
        "arms": results,
        "control_swept": control_failed,
        "fixture_control_ok": fixture_ok,
        "verdict": ("the harness detects a sweep, so every 'clean' below is a "
                    "statement about the runner"
                    if control_failed else
                    "THE HARNESS FAILED ITS CONTROL: it cannot detect a sweep, "
                    "so no other arm's result means anything"),
    }
    with open(os.path.join(RAW, "results.json"), "w") as fh:
        json.dump(payload, fh, indent=2, sort_keys=True)
    print()
    print("control C0 swept: %s   (must be True)" % control_failed)
    print("fixture control B0 clean and no formatter: %s   (must be True)" % fixture_ok)
    print("wrote %s" % os.path.join(RAW, "results.json"))
    return 0 if (control_failed and fixture_ok) else 1


def read_versions():
    versions = {}
    for name, path in (
        ("lefthook", "logs/lefthook.version"),
        ("pre-commit", "logs/pre-commit.version"),
        ("node", "logs/node.version"),
        ("lint-staged", "logs/lint-staged.version"),
        ("husky", "logs/husky.version"),
        ("prettier", "logs/prettier.version"),
    ):
        full = os.path.join(ROOT, path)
        versions[name] = open(full).read().strip() if os.path.exists(full) else None
    for name, path in (("lefthook.sha256", "logs/lefthook.sha256"),
                       ("node.sha256", "logs/node.sha256")):
        full = os.path.join(ROOT, path)
        versions[name] = open(full).read().split()[0] if os.path.exists(full) else None
    try:
        versions["git"] = subprocess.run(["git", "--version"],
                                         capture_output=True, text=True).stdout.strip()
    except Exception:
        versions["git"] = None
    return versions


if __name__ == "__main__":
    sys.exit(main())