<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-07
-->

# Agent report — one-edit-among-three, stg arm

Agent session ses_eebd35501ffeb2yHtnWu6fMKDC, completed 2026-10-07 ~02:25 UTC.
Verbatim final report:

Staging succeeded with exactly the intended result. Report:

## How I identified the line

I compared the committed and working versions line by line:

- **`git show HEAD:app.py`** showed the committed file: line 1 `import os`, line 15 `def main():`, and `print(load(sys.argv[1]))`.
- **`cat -n app.py`** showed the working copy with three edits: line 1 → `import os.path`, line 15 → `def main(argv=None):`, and line 19 → `print(load(sys.argv[-1]))`.

The requested change — selecting the last command-line argument — is the `sys.argv[-1]` edit on working-tree **line 19**. `stg list` confirmed the same three change locations (`app.py:1`, `app.py:15`, `app.py:19`) with their new contents, addressing changes by working-tree line number.

## Commands run, in order

1. `git status --short` and `ls` — established the starting state (` M app.py`, nothing staged).
2. `git show HEAD:app.py` — read the committed version.
3. `cat -n app.py` — read the working copy with line numbers.
4. `stg --help` — learned the tool's interface (its documented exit codes: 0 = nothing matched, 1 = something matched, 2 = error).
5. `stg list` (plus confirming `git show :app.py` was empty) — listed stageable changes as `path:line`.
6. `stg stage app.py:19` — staged only the line-19 change; exit 1, meaning it matched (not an error).
7. Verification: `git show :app.py`, `git status --short`, `stg list`.

## Result

- **Staged content** is exactly HEAD plus the single change: `print(load(sys.argv[-1]))`. The staged version still has `import os` and `def main():`.
- **`git status --short` shows `MM`**: the file carries both staged and unstaged modifications.
- **`stg list` after staging** shows only `app.py:1` and `app.py:15` remaining unstaged — the two edits that were to be left alone.
- Nothing was committed; no files outside the repository directory were touched; no `git diff` output was read.

The staged result is correct — I see no problem with it.
