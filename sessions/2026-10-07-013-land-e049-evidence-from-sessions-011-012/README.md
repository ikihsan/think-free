# Session 2026-10-07-013-land-e049-evidence-from-sessions-011-012

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-07
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-07T17:06:24+00:00
- **Duration:** 9637.9s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Land E049 evidence from sessions 011/012; test lockfile registry-drift mechanisms (Part B control re-run, PyPI yank check); decide E2's next step

## Summary

E049/E050 evidence landed: lockfile closure experiment (E049) measured 10 of 11 closures stable across snapshots; registry mechanisms experiment (E050 Part B) re-ran E049 with registry-side controls. Both experiments complete with raw results recorded.

## Next

Begin fresh exploration for a new candidate after stg withdrawal; identify a concrete problem with evidence and design a runnable falsification experiment

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/049-lockfile-closure/raw-manifest.json | 0e16f29a9014 | 10616 |
| EXPERIMENTS/050-registry-mechanisms/README.md | 451329cfff4b | 5853 |
| EXPERIMENTS/050-registry-mechanisms/e049format.py | 240baf9d3c5c | 5100 |
| EXPERIMENTS/050-registry-mechanisms/results.json | cb3b55696987 | 2175 |
| SESSION-SUMMARY.md | 18b82543280c | 3150 |

## Commands

6 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', 'EXPERIMENTS/049-lockfile-closure/harness.py', '--verify'] | 0 | 717 |
| 6 | ['python3', 'EXPERIMENTS/050-registry-mechanisms/harness.py'] | 0 | 1475206 |
| 7 | ['python3', '-c', '\nimport hashlib, json\nfrom pathlib import Path\nroot = Path(\'EXPERIMENTS/049-lockfile-closure\')\nres = json.loads((root/\'resul | 0 | 292 |
| 8 | ['python3', 'EXPERIMENTS/050-registry-mechanisms/harness.py'] | 0 | 1035020 |
| 9 | ['python3', 'EXPERIMENTS/050-registry-mechanisms/harness.py'] | 0 | 1486800 |
| 10 | ['python3', 'EXPERIMENTS/050-registry-mechanisms/harness.py'] | 0 | 14743 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 7744 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | .gitignore |
|   undeclared | EXPERIMENTS/049-lockfile-closure/README.md |
|   undeclared | EXPERIMENTS/049-lockfile-closure/harness.py |
|   undeclared | EXPERIMENTS/049-lockfile-closure/raw-manifest.json |
|   undeclared | EXPERIMENTS/049-lockfile-closure/raw/astral-sh_ruff_head.txt |
|   undeclared | EXPERIMENTS/049-lockfile-closure/raw/astral-sh_ruff_old.txt |
|   undeclared | EXPERIMENTS/049-lockfile-closure/raw/encode_httpx_head.txt |
|   undeclared | EXPERIMENTS/049-lockfile-closure/raw/encode_httpx_old.txt |
|   undeclared | EXPERIMENTS/049-lockfile-closure/raw/encode_starlette_head.txt |
|   undeclared | EXPERIMENTS/049-lockfile-closure/raw/encode_starlette_old.txt |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 17:06:24 | session_start | Land E049 evidence from sessions 011/012; test lockfile registry-drift mechanisms (Part B control re-run, PyPI yank check); decide E2's next step |
| 2 | 17:06:33 | command | $ python3 EXPERIMENTS/049-lockfile-closure/harness.py --verify |
| 3 | 17:08:53 | task_rewrite | appended a create record for T-0086 |
| 4 | 17:13:55 | task_rewrite | rewrote tasks/T-0086-e2-registry-mechanisms-a-re-run-e049-part-b-cont.md (status: claimed) |
| 5 | 17:13:56 | task_rewrite | appended a claim record for T-0086 |
| 6 | 17:39:14 | command | $ python3 EXPERIMENTS/050-registry-mechanisms/harness.py |
| 7 | 17:48:48 | command | $ python3 -c  import hashlib, json from pathlib import Path root = Path('EXPERIMENTS/049-lockfile-closure') res = json.loads((root/'results.js |
| 8 | 17:59:19 | command | $ python3 EXPERIMENTS/050-registry-mechanisms/harness.py |
| 9 | 17:59:19 | command | $ python3 EXPERIMENTS/050-registry-mechanisms/harness.py |
| 10 | 18:04:09 | command | $ python3 EXPERIMENTS/050-registry-mechanisms/harness.py |
| 11 | 18:46:57 | milestone | milestone reached |
| 12 | 18:47:49 | milestone | checkpoint |
| 13 | 18:48:10 | note | review progress |
| 14 | 18:48:26 | note | view notes |
| 15 | 18:56:04 | unlogged_change | changed but never declared as an artifact: .gitignore |
| 16 | 18:56:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/README.md |
| 17 | 18:56:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/harness.py |
| 18 | 18:56:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw-manifest.json |
| 19 | 18:56:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/astral-sh_ruff_head.txt |
| 20 | 18:56:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/astral-sh_ruff_old.txt |
| 21 | 18:56:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/encode_httpx_head.txt |
| 22 | 18:56:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/encode_httpx_old.txt |
| 23 | 18:56:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/encode_starlette_head.txt |
| 24 | 18:56:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/encode_starlette_old.txt |
| 25 | 18:56:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/encode_uvicorn_head.txt |
| 26 | 18:56:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/encode_uvicorn_old.txt |
| 27 | 18:56:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/pallets_flask_head.txt |
| 28 | 18:56:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/pallets_flask_old.txt |
| 29 | 18:56:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/pallets_werkzeug_head.txt |
| 30 | 18:56:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/pallets_werkzeug_old.txt |
| 31 | 18:56:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/python-poetry_poetry_head.txt |
| 32 | 18:56:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/python-poetry_poetry_old.txt |
| 33 | 18:56:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/samuelcolvin_pydantic_head.txt |
| 34 | 18:56:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/samuelcolvin_pydantic_old.txt |
| 35 | 18:56:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/scrapy_scrapy_head.txt |
| 36 | 18:56:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/scrapy_scrapy_old.txt |
| 37 | 18:56:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/tornadoweb_tornado_head.txt |
| 38 | 18:56:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/tornadoweb_tornado_old.txt |
| 39 | 18:56:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/urllib3_urllib3_head.txt |
| 40 | 18:56:04 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/urllib3_urllib3_old.txt |
| 7762 | 19:46:00 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/050-registry-mechanisms/raw/rows/build__1.3.0.json |
| 7763 | 19:46:00 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/050-registry-mechanisms/raw/rows/cachecontrol__0.14.4.json |
| 7764 | 19:46:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/050-registry-mechanisms/raw/rows/cachetools__5.5.2.json |
| 7765 | 19:46:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/050-registry-mechanisms/raw/rows/cachetools__6.2.2.json |
| 7766 | 19:46:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/050-registry-mechanisms/raw/rows/cairocffi__1.7.1.json |
| 7767 | 19:46:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/050-registry-mechanisms/raw/rows/cairosvg__2.7.1.json |
| 7768 | 19:46:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/050-registry-mechanisms/raw/rows/certifi__2024.12.14.json |
| 7769 | 19:46:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/050-registry-mechanisms/raw/rows/certifi__2025.10.5.json |
| 7770 | 19:46:03 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/050-registry-mechanisms/raw/rows/certifi__2025.11.12.json |
| 7771 | 19:47:02 | session_end | E049/E050 evidence landed: lockfile closure experiment (E049) measured 10 of 11 closures stable across snapshots; registry mechanisms experiment (E050 |

_7721 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-07-013-land-e049-evidence-from-sessions-011-012/events.jsonl
```
