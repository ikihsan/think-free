#!/usr/bin/env python3
"""Capture the check-run annotations of named CI runs from the public API.

Why this exists (T-0046): `docs/operations/ci-diagnosis.md` stated that whether
GitHub files an annotation on the workflow command's `file=` property was
`unmeasured`, and that run `37189825232` showed `path=.github` beside an
emitted `::error file=tools/originlib/identifiers.py::`. Both statements were
read off this endpoint, and both turned out to be wrong. So the evidence is
captured here as bytes rather than as a reading of it.

What it does, in order, because the order is the point:

1. `GET /rate_limit` first. A 403 from the unauthenticated limit and an empty
   annotation list look identical to a shell pipeline, and treating the first
   as the second is how this repository recorded a false premise for two
   sessions (`FAILURES.md` F020).
2. `GET /actions/runs/<id>/jobs` for each run, and the `verify (3.12)` row's
   check run. The row is named because the five file-reading gate steps are
   guarded to it in `.github/workflows/ci.yml`.
3. `GET /check-runs/<id>/annotations`, kept verbatim.

No token, no dependency, and every response body written to `raw/` so the
numbers in the README can be re-derived rather than believed.

    python3 EXPERIMENTS/010-annotation-rendering/fetch_annotations.py
"""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw"
OWNER = "ikihsan"
REPO = "think-free"
ROW = "verify (3.12)"

# Four runs, and which arm each one is. See README.md; the point of the list is
# that a single run cannot answer the question, because the runs differ in
# whether the annotating step ran at all.
RUNS = [
    ("37191658964", "A", "Tests green, Documentation lint red: the annotator emitted one command"),
    ("37189825232", "B", "Tests red, so every later step with an if: was skipped"),
    ("37190842104", "C", "Tests red on all seven rows, same shape as B"),
    ("37192717297", "D", "clean tree: the control, where the annotator must stay silent"),
    # Added after the arms above ran, and labelled rather than folded into them:
    # arm E is the first pushed run on which the probe executed, so it is the
    # measurement the other four could only set up.
    ("37196459285", "E", "the first run carrying origin probe: every shape, measured"),
]


def get(url: str) -> tuple[int, bytes]:
    request = urllib.request.Request(url, headers={"User-Agent": "origin-010-probe"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()


def limit_state() -> dict:
    status, body = get(f"https://api.github.com/rate_limit")
    if status != 200:
        return {"http": status, "body": body.decode("utf-8", "replace")[:400]}
    core = json.loads(body)["resources"]["core"]
    return {"http": status, "limit": core["limit"], "remaining": core["remaining"], "used": core["used"]}


def main() -> int:
    RAW.mkdir(exist_ok=True)
    limit = limit_state()
    (RAW / "rate_limit.json").write_text(json.dumps(limit, indent=2, sort_keys=True) + "\n")
    print("rate_limit:", json.dumps(limit, sort_keys=True))
    if limit.get("http") != 200:
        print("refusing to read annotations through an unverified limit: a 403 and an empty list are not the same answer")
        return 3

    base = f"https://api.github.com/repos/{OWNER}/{REPO}"
    summary = []
    for run_id, arm, why in RUNS:
        status, body = get(f"{base}/actions/runs/{run_id}")
        if status != 200:
            print(f"run {run_id}: jobs? HTTP {status}")
            summary.append({"run": run_id, "arm": arm, "http": status})
            continue
        run = json.loads(body)
        status, body = get(f"{base}/actions/runs/{run_id}/jobs?per_page=100")
        if status != 200:
            print(f"run {run_id}: jobs HTTP {status}")
            summary.append({"run": run_id, "arm": arm, "http": status})
            continue
        jobs = json.loads(body)["jobs"]
        rows = {job["name"]: job["conclusion"] for job in jobs}
        row = next((job for job in jobs if job["name"] == ROW), None)
        if row is None:
            print(f"run {run_id}: no row named {ROW!r}")
            summary.append({"run": run_id, "arm": arm, "rows": sorted(rows), "row": None})
            continue
        check_run_id = row["check_run_url"].rsplit("/", 1)[1]
        status, body = get(f"{base}/check-runs/{check_run_id}/annotations?per_page=100")
        if status != 200:
            print(f"run {run_id}: annotations HTTP {status}")
            summary.append({"run": run_id, "arm": arm, "http": status})
            continue
        annotations = json.loads(body)
        (RAW / f"{run_id}.json").write_text(json.dumps(annotations, indent=2, sort_keys=True) + "\n")
        summary.append({
            "run": run_id,
            "arm": arm,
            "why": why,
            "head_sha": run["head_sha"],
            "conclusion": run["conclusion"],
            "check_run_id": check_run_id,
            "rows": rows,
            "annotations": len(annotations),
            "paths": sorted({str(item.get("path")) for item in annotations}),
        })
        print(f"run {run_id} arm {arm}: {len(annotations)} annotations, paths {summary[-1]['paths']}")

    (RAW / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())