<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-07
-->

# Agent report — one-edit-among-three, nostg arm

Agent session ses_eebd7a22dffeuZRSZxkuMNDPlw, completed 2026-10-07 ~02:21 UTC.
Verbatim final report:

Staging succeeded. Here is the full report.

## How I identified the line

I compared the committed version (`git show HEAD:app.py`) with the working copy (`cat -n app.py`). The file contains exactly three edits:

| Edit | Committed | Working | Working-tree line |
|---|---|---|---|
| 1 | `import os` | `import os.path` | 1 |
| 2 | `def main():` | `def main(argv=None):` | 15 |
| 3 | `print(load(sys.argv[1]))` | `print(load(sys.argv[-1]))` | **19** |

The target change — selecting the last command-line argument via `sys.argv[-1]` — is on **line 19** of the working tree. Lines 1 and 15 had to remain unstaged.

## Exact commands run (in order)

Each prefixed with the required `export PATH=...:$PATH &&`:

1. `git show HEAD:app.py` — read committed version
2. `cat -n app.py` — read working copy with line numbers
3. `git status --short && git ls-files -s app.py` — confirmed nothing staged yet (` M`), mode `100644`
4. `git show :app.py | head -5` — confirmed index matched HEAD
5. `git show HEAD:app.py | sed 's/print(load(sys\.argv\[1\]))/print(load(sys.argv[-1]))/' | git hash-object -w --stdin` — built the intended staged content (HEAD + only the line-19 edit) as blob `cecd9aa1d75ae05227666ffb1c66edca8cfb47c8`
6. `git update-index --cacheinfo 100644,cecd9aa1d75ae05227666ffb1c66edca8cfb47c8,app.py` — staged that blob
7. Verification: `git show :app.py`, `git status --short && git ls-files -s app.py`, `cat app.py`

I deliberately avoided `git add -p`/`--patch`, since its interactive UI displays diff hunks, which would count as reading diff output and invalidate the run. Instead I constructed the desired staged blob directly from the allowed committed/working versions.

## Result — staging succeeded

- **Staged version** (`git show :app.py`): identical to HEAD except line 19 now reads `print(load(sys.argv[-1]))` — exactly one change.
- **Working copy**: untouched; still contains all three edits (`import os.path`, `def main(argv=None):`, `sys.argv[-1]`).
- **Status**: `MM app.py` — one change staged, the other two (`import os.path` on line 1, `def main(argv=None):` on line 15) remain unstaged.
- Nothing was committed; nothing outside the repository directory was read or modified.

The staged result is correct.
