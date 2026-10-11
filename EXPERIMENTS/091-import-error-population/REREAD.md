<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-11
-->

# E091 re-read — hand judgment of all 25 `names_module_no_dist` rows

Session 2026-10-11-001. E091's classifier counted 25 of 858 reports (2.91%)
as help-seeking questions naming a module but no distribution, passing its
≥1% gate. Session 2026-10-10-009 then asserted NONE of the 25 is genuine, in
46 seconds with no commands and no committed artifact. This file settles it
by reading every row's committed body.

## Rubric (fixed before any body was read)

**genuine** — the reporter hits an import error for module X, asks what to
install or get, names no distribution, and installing a distribution is the
fix. **not-genuine** — X is the reporter's own file, stdlib, already
installed (env/path/venv breakage), a maintainer bug report, or no
distribution is involved. **borderline** — asks, but the row cannot tell
whether a distribution is the answer.

## Verdicts (23 distinct URLs; pyspark and unidecode were harvested twice)

| # | module | verdict | one-line reason |
|---|---|---|---|
| 1 | exceptions | not-genuine | py2-ism inside installed docx; fix is upgrading docx |
| 2 | dbus | not-genuine | dbus-python/pydbus already installed; build/env failure |
| 3 | dir_one | not-genuine | own local files; no distribution exists |
| 4 | mido | not-genuine | distribution already installed and named; env issue |
| 5 | module1 | not-genuine | own package under notebook kernel; path semantics |
| 6 | telegram | **genuine** | "What do I have to install?"; answer is python-telegram-bot |
| 7 | pyspark | not-genuine | in pip list; SPARK_HOME/PYTHONPATH breakage (×2 rows) |
| 8 | pygame | not-genuine | installed; venv/interpreter mismatch |
| 9 | MT | not-genuine | own project; relative-import structure |
| 10 | board | not-genuine | importable as user; sudo env split |
| 11 | streamlit | not-genuine | installed; debugger interpreter mismatch |
| 12 | google | not-genuine | google-generativeai named and tried; venv issue |
| 13 | unidecode | not-genuine | installed via conda; PATH mismatch (×2 rows) |
| 14 | source_salesforce | not-genuine | transitive dep bug report; never asks what to install |
| 15 | graphics | borderline | asks for guidance; glumpy install vs local files unclear |
| 16 | coincurve | not-genuine | py2/py3 confusion; name equals its distribution |
| 17 | umail | not-genuine | MicroPython/Thonny; no PyPI distribution involved |
| 18 | mpuserver | borderline | "where can this file be found"; repo file vs dist unclear |
| 19 | voluptuous_openapi | not-genuine | container-update bug report to the maintainer |
| 20 | examples | not-genuine | node's own package missing; repo packaging bug |
| 21 | docker | **genuine** | "installation step missed?"; engine runs, `docker` dist missing |
| 22 | clients | not-genuine | repo's own package not downloaded |
| 23 | DepthFlow | not-genuine | casing bug inside the node; maintainer report |

Per-row rationale in `reread.json`. Bodies: `raw/api/`, via `classified.jsonl` URLs.

## Tally (reproduces via `reread.json` + `classified.jsonl`)

- Strict: **2/858 = 0.0023**, Wilson CI95 [0.0006, 0.0085] — excludes 0.01.
- Inclusive (genuine + borderline): **4/858 = 0.0047**, CI95 [0.0018, 0.0119].
- Both fail E091's own ≥1% gate. The "NONE genuine" claim is corrected to
  two (telegram, docker); the gate conclusion — line closes — stands.

## Instrument defects found (both load-bearing on the count, neither on the verdict)

1. **Double harvest.** Overlapping queries counted two URLs twice (25 rows =
   23 distinct), inflating the numerator by 9%.
2. **Own-rule violations.** Rows 2, 4, 7, 12 name a distribution yet counted
   as naming none; the `needs X` rationale is mechanical (`dbus`→`dbus`,
   whose real provider is dbus-python).
3. **README describes rows that are not in the data.** The "most common
   gaps" list (cv2, sklearn, yaml, bs4, crypto, jwt, dateutil, dotenv) names
   modules appearing in **0 of the 25 rows**; corrected in place.

## What this does not close

The forward mechanism (0.931, E085) and the query-time reverse answer are
untouched — what died is the demand population for them, not the instruments.
Reopening needs a new population measurement that clears 1% genuine, not a
re-read of these rows.
