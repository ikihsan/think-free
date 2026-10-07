<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-07
-->

# Agent report — adjacent-modifications, nostg arm

Agent session ses_eebd7a234ffetJt0S062nhU2LM, completed 2026-10-07 ~02:21 UTC.
Verbatim final report:

Staging succeeded exactly as required. Here is my report.

## How I identified the line to stage

I compared the committed version (`git show HEAD:app.py`) against the working copy (`cat -n app.py`). The committed `load()` function was:

```python
def load(path):
    with open(path) as fh:
        return fh.read()
```

The working copy has exactly two adjacent changes, both inside `load()`:

| Working-tree line | Change | Action |
|---|---|---|
| Line 6 | `open(path)` → `open(path, "rb")` (binary mode) | **left unstaged** |
| Line 7 | `fh.read()` → `fh.read().decode("utf-8")` (UTF-8 decode) | **staged** |

Since the index matched HEAD (nothing was staged), I built a patch whose context is the HEAD content — crucially with line 6 in its *original* form (`with open(path) as fh:`) as context — and applied it to the index only, so the working tree was untouched.

## Commands run, in order

1. `git show HEAD:app.py` — read committed version
2. `cat -n app.py` — read working copy with line numbers
3. `git status --short && git status` — confirmed nothing staged (` M app.py`)
4. `git show :app.py` — confirmed index == HEAD
5. `git apply --cached - <<'PATCH' ... PATCH` — applied a single-hunk patch (`@@ -5,6 +5,6 @@`) to the index only, changing line 7 to `return fh.read().decode("utf-8")` while keeping line 6 as context; exit code 0
6. `git show :app.py` and `git status --short && cat -n app.py` — verification

## Result — staging succeeded

- **Staged version** contains only the decode change: line 6 remains `with open(path) as fh:`, line 7 is `return fh.read().decode("utf-8")`.
- **Working tree** still contains both changes (`"rb"` on line 6, `.decode("utf-8")` on line 7).
- `git status --short` shows `MM app.py`, confirming the file has both staged and unstaged modifications — the binary-mode change remains unstaged.
- Nothing was committed, no diff output was read, and no files outside the repository were touched (the patch was fed via stdin; no temporary files were created).

The staged result is correct.
