<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-21
-->

# E208 amendment 1 — the analysis output is `gates.json`, not `results.json`

**Date:** 2026-10-21, after the first (and only) analysis run.

The protocol named the analysis output `results.json`. This repository's
`.gitignore` carries bare-name rules (`results.json`, …) after its raw-data
negation block, so `session artifact` reported the file as **skipped
(gitignored)** — the gate record would have sat on disk undeclared, the F142
shape this record exists to prevent.

The output name in `analyze.py` is therefore `gates.json` (the same convention
E202 used). **No threshold, definition, window, seed or computation changed.**
Verified rather than asserted: the renamed run's output is **byte-identical**
to the pre-rename file (`cmp`, exit 0; the removed file contained no filename
reference). The pre-rename file was deleted after the comparison; the command
is in the session log.
