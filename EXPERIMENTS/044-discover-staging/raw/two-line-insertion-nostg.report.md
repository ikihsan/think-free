<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-07
-->

# Agent report — two-line-insertion, nostg arm

Agent session ses_eebd7a22fffeGgOBEI8YA1JS8Z, completed 2026-10-07 ~02:22 UTC.
Verbatim final report:

Staging succeeded and the result is correct. Report:

## How I identified the line

I compared the committed and working versions (no `git diff` used):

- `git show HEAD:app.py` → lines 1–2 are `import os`, `import sys`, followed by blank lines.
- `cat app.py` → `import os` (line 1), `import sys` (line 2), **`import json` (line 3)**, `import re` (line 4), then blank lines.

So the change to stage is the insertion of `import json` on **working-tree line 3**, immediately after `import sys`; the adjacent `import re` on line 4 had to stay unstaged. The index was untouched (`git show :app.py` matched HEAD), so staging meant producing "HEAD + `import json`" in the index.

## Commands run, in order

All from the trial directory, each prefixed with the required `export PATH=...:$PATH &&`:

1. `git show HEAD:app.py` — read committed version
2. `cat app.py` — read working copy
3. `git status --short` + `git show :app.py | head -5` — confirmed unstaged state
4. First `git apply --cached` with a 2-context-line hunk (`@@ -1,2 +1,3 @@`) — **failed**: "patch does not apply"; git 2.25.1 couldn't anchor a hunk with leading context only
5. Diagnostics: `git show :app.py | od -c | head -8`, `git apply --cached --verbose --check`, `which git`, `env | grep -iE 'git|index'`, `git config --list --local`, `ls -la` — confirmed index bytes were exactly `import os\nimport sys\n\n\n...`, no weird config/env
6. `git apply --cached --check --verbose` with a fuller hunk including trailing context — passed
7. The successful staging command, patch via stdin heredoc (no temp files left behind):
   ```
   git apply --cached --verbose <<'EOF'
   --- a/app.py
   +++ b/app.py
   @@ -1,4 +1,5 @@
    import os
    import sys
   +import json


    def load(path):
   EOF
   ```
   → "Applied patch app.py cleanly", exit 0.
8. Verification: `git show :app.py`, `git status --short`, `cat app.py`

## Result — correct

- **Staged version** = HEAD + `import json` after `import sys`, with **no** `import re` — exactly the requested change.
- **Working copy** unchanged, still contains both insertions.
- `git status --short` shows `MM app.py`: a staged change plus a remaining unstaged change (the `import re` insertion).
- Nothing committed; nothing outside the repo directory read or modified; the diff-blocking wrapper was not bypassed.
