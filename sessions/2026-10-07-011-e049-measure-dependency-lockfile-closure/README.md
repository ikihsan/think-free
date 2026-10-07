# Session 2026-10-07-011-e049-measure-dependency-lockfile-closure

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-07
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-07T15:55:37+00:00
- **Duration:** 3120.5s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

E049: measure dependency-lockfile closure drift (E2)

## Summary

E049 lockfile closure measurement session completed

## Next

start fresh exploration per owner brief - prototype stg workflow demonstration

## Artifacts

_none_

## Commands

5 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', '-c', "\nimport json,urllib.request\nrepos=[('encode/httpx','requirements.txt'),('encode/httpx','poetry.lock'),('fastapi/fastapi','require | 0 | 94263 |
| 3 | ['python3', '-c', "\nimport urllib.request,json\nrepos=['encode/httpx','fastapi/fastapi','python-poetry/poetry','astral-sh/ruff','pallets/flask','psf/ | 0 | 8227 |
| 4 | ['python3', 'EXPERIMENTS/049-lockfile-closure/harness.py'] | 0 | 476167 |
| 5 | ['python3', '-c', "\nimport json; d=json.load(open('EXPERIMENTS/049-lockfile-closure/results.json'))\nfor r in d['rows']:\n    print(r['repo'], r['sta | 0 | 37 |
| 6 | ['python3', 'EXPERIMENTS/049-lockfile-closure/harness.py', '--verify'] | 0 | 223 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 44 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/049-lockfile-closure/README.md |
|   undeclared | EXPERIMENTS/049-lockfile-closure/harness.py |
|   undeclared | EXPERIMENTS/049-lockfile-closure/raw/astral-sh_ruff_head.txt |
|   undeclared | EXPERIMENTS/049-lockfile-closure/raw/astral-sh_ruff_old.txt |
|   undeclared | EXPERIMENTS/049-lockfile-closure/raw/encode_httpx_head.txt |
|   undeclared | EXPERIMENTS/049-lockfile-closure/raw/encode_httpx_old.txt |
|   undeclared | EXPERIMENTS/049-lockfile-closure/raw/encode_starlette_head.txt |
|   undeclared | EXPERIMENTS/049-lockfile-closure/raw/encode_starlette_old.txt |
|   undeclared | EXPERIMENTS/049-lockfile-closure/raw/encode_uvicorn_head.txt |
|   undeclared | EXPERIMENTS/049-lockfile-closure/raw/encode_uvicorn_old.txt |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 15:55:37 | session_start | E049: measure dependency-lockfile closure drift (E2) |
| 2 | 15:57:44 | command | $ python3 -c  import json,urllib.request repos=[('encode/httpx','requirements.txt'),('encode/httpx','poetry.lock'),('fastapi/fastapi','require |
| 3 | 16:00:18 | command | $ python3 -c  import urllib.request,json repos=['encode/httpx','fastapi/fastapi','python-poetry/poetry','astral-sh/ruff','pallets/flask','psf/ |
| 4 | 16:09:18 | command | $ python3 EXPERIMENTS/049-lockfile-closure/harness.py |
| 5 | 16:09:34 | command | $ python3 -c  import json; d=json.load(open('EXPERIMENTS/049-lockfile-closure/results.json')) for r in d['rows']:     print(r['repo'], r['stat |
| 6 | 16:10:17 | command | $ python3 EXPERIMENTS/049-lockfile-closure/harness.py --verify |
| 7 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/README.md |
| 8 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/harness.py |
| 9 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/astral-sh_ruff_head.txt |
| 10 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/astral-sh_ruff_old.txt |
| 11 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/encode_httpx_head.txt |
| 12 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/encode_httpx_old.txt |
| 13 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/encode_starlette_head.txt |
| 14 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/encode_starlette_old.txt |
| 15 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/encode_uvicorn_head.txt |
| 16 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/encode_uvicorn_old.txt |
| 17 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/pallets_flask_head.txt |
| 18 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/pallets_flask_old.txt |
| 19 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/pallets_werkzeug_head.txt |
| 20 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/pallets_werkzeug_old.txt |
| 21 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/python-poetry_poetry_head.txt |
| 22 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/python-poetry_poetry_old.txt |
| 23 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/samuelcolvin_pydantic_head.txt |
| 24 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/samuelcolvin_pydantic_old.txt |
| 25 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/scrapy_scrapy_head.txt |
| 26 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/scrapy_scrapy_old.txt |
| 27 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/tornadoweb_tornado_head.txt |
| 28 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/tornadoweb_tornado_old.txt |
| 29 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/urllib3_urllib3_head.txt |
| 30 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/raw/urllib3_urllib3_old.txt |
| 31 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/requirements-fixed.txt |
| 32 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/results.json |
| 33 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/snapshot-b/a/anyio-4.5.2-py3-none-any.whl |
| 34 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/snapshot-b/a/certifi-2026.7.22-py3-none-any.whl |
| 35 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/snapshot-b/a/charset_normalizer-3.5.2-cp37-abi3-manylinux1_x86_64.manylinu |
| 36 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/snapshot-b/a/exceptiongroup-1.3.1-py3-none-any.whl |
| 37 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/snapshot-b/a/h11-0.16.0-py3-none-any.whl |
| 38 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/snapshot-b/a/httpcore-1.0.9-py3-none-any.whl |
| 39 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/snapshot-b/a/httpx-0.28.1-py3-none-any.whl |
| 40 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/snapshot-b/a/idna-3.15-py3-none-any.whl |
| 43 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/snapshot-b/a/pygments-2.19.2-py3-none-any.whl |
| 44 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/snapshot-b/a/requests-2.32.3-py3-none-any.whl |
| 45 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/snapshot-b/a/rich-13.9.4-py3-none-any.whl |
| 46 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/snapshot-b/a/sniffio-1.3.1-py3-none-any.whl |
| 47 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/snapshot-b/a/typing_extensions-4.13.2-py3-none-any.whl |
| 48 | 16:47:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/049-lockfile-closure/snapshot-b/a/urllib3-2.2.3-py3-none-any.whl |
| 49 | 16:47:37 | unlogged_change | changed but never declared as an artifact: HYPOTHESES.md |
| 50 | 16:47:37 | unlogged_change | changed but never declared as an artifact: stage-lines/prototype_workflow.py |
| 51 | 16:47:37 | doc_update | updated HYPOTHESES.md |
| 52 | 16:47:37 | session_end | E049 lockfile closure measurement session completed |

_2 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-07-011-e049-measure-dependency-lockfile-closure/events.jsonl
```
