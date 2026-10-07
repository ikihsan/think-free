#!/usr/bin/env python3
"""E047 — one arm per hook runner, each installed the way its own docs install it.

Split out of `harness.py` at the 300-line cap, by invariant: this file is the
*configuration* of the population, and nothing here decides a verdict. Each
`install()` writes exactly one runner's real configuration into a throwaway
repository and returns a log; the fixture, the oracle and the controls are in the
other modules, so a reader can see what each runner was given without reading
what was concluded about it.

`expect_sweep` is the arm's **declared prediction**, recorded before it runs.
That is what makes a later reading checkable rather than merely plausible: A2 and
A5 carry the identical hook body and differ only in whether the framework manages
unstaged changes, and pre-commit's prediction was wrong in a way worth being able
to point at.

Two deviations from a real installation, both recorded because they are
deviations. lint-staged is wired by a git hook that calls it, because it is a CLI
rather than a framework and the wiring is part of what is being tested. husky is
wired by setting `core.hooksPath` directly, because its installer runs from an npm
lifecycle script that a bare test repository has no equivalent of; git ends up
running the same `.husky/pre-commit` either way.
"""

import os

from gitenv import ROOT, git, node_bin, prettier_cmd, sh, write

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
     "control: the fixture does not commit the marker on its own", None),
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
