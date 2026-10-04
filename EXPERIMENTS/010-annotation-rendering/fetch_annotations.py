#!/usr/bin/env python3
"""Capture the check-run annotations of named CI runs from the public API.

Why this exists (T-0046): `docs/operations/ci-diagnosis.md` stated that whether
GitHub files an annotation on the workflow command's `file=` property was
`unmeasured`, and that run `37189825232` showed `path=.github` beside an
emitted `::error file=tools/originlib/identifiers.py::`. Both statements were
read off this endpoint, and both turned out to be wrong. So the evidence is
captured here as bytes rather than as a reading of it.

What it does, in order, because the order is the point:

1. `GET /rate_limit` first, and **refuse to start a batch the remaining budget
   cannot cover** — two calls per run plus one for the limit itself. A 403 from
   the unauthenticated limit and an empty annotation list look identical to a
   shell pipeline, and treating the first as the second is how this repository
   recorded a false premise for two sessions (`FAILURES.md` F020). The same
   confusion makes a *partly* finished batch worse than a refused one: a summary
   recording 403s for half its arms reads like evidence about those runs, and is
   evidence about the limit instead. This was found by running it: the first
   version overwrote a good `summary.json` with seven 403s.
2. `GET /actions/runs/<id>/jobs` for each run, and the `verify (3.12)` row's
   check run. The row is named because the five file-reading gate steps and the
   probe are guarded to it in `.github/workflows/ci.yml`.
3. `GET /check-runs/<id>/annotations`, kept verbatim.

A run whose capture already exists is skipped, so the next run costs only what it
still needs. `--refresh` re-fetches everything.

No token, no dependency, and every response body written to `raw/` so the
numbers in the README can be re-derived rather than believed.

    python3 EXPERIMENTS/010-annotation-rendering/fetch_annotations.py [--refresh]
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
    # Arms F to J are the run census added in T-0049, one capture per run that
    # passed since this list was written. They are a census rather than an
    # experiment: each is accounted for with the cause its own annotations name,
    # and none of them was reproduced on a VM to find out.
    ("37196594583", "F", "red on the session step: the session had been started and not claimed"),
    ("37196559251", "G", "green, and the first run whose probe annotations are all the file has"),
    ("37197291442", "H", "red on Documentation lint: a broken link in another VM's task file"),
    ("37197942512", "I", "red on the session step: a work commit published while its session was open"),
    ("37198002763", "J", "green on the tip, with every session closed"),
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


COST_PER_RUN = 2


def main() -> int:
    refresh = "--refresh" in sys.argv[1:]
    RAW.mkdir(exist_ok=True)
    limit = limit_state()
    (RAW / "rate_limit.json").write_text(json.dumps(limit, indent=2, sort_keys=True) + "\n")
    print("rate_limit:", json.dumps(limit, sort_keys=True))
    if limit.get("http") != 200:
        print("refusing to read annotations through an unverified limit: a 403 and an empty list are not the same answer")
        return 3
    wanted = [entry for entry in RUNS if refresh or not (RAW / f"{entry[0]}.json").is_file()]
    needed = 1 + COST_PER_RUN * len(wanted)
    if len(wanted) < len(RUNS):
        print(f"{len(RUNS) - len(wanted)} arm(s) already captured; skipping them")
    if limit.get("remaining", 0) < needed:
        print(
            f"refusing to start: {len(wanted)} arm(s) need {needed} requests and "
            f"{limit.get('remaining')} remain. A partly fetched batch is worse than "
            f"none: a summary holding 403s reads like evidence about those runs, and is "
            f"evidence about the limit. Run again after the reset, or with --refresh "
            f"once there is budget for everything."
        )
        return 3

    base = f"https://api.github.com/repos/{OWNER}/{REPO}"
    for run_id, arm, why in wanted:
        status, body = get(f"{base}/actions/runs/{run_id}/jobs?per_page=100")
        if status != 200:
            print(f"run {run_id} arm {arm}: jobs HTTP {status}")
            continue
        jobs = json.loads(body)["jobs"]
        row = next((job for job in jobs if job["name"] == ROW), None)
        if row is None:
            print(f"run {run_id} arm {arm}: no row named {ROW!r}")
            continue
        check_run_id = row["check_run_url"].rsplit("/", 1)[1]
        status, body = get(f"{base}/check-runs/{check_run_id}/annotations?per_page=100")
        if status != 200:
            print(f"run {run_id} arm {arm}: annotations HTTP {status}")
            continue
        annotations = json.loads(body)
        (RAW / f"{run_id}.json").write_text(json.dumps(annotations, indent=2, sort_keys=True) + "\n")
        print(f"run {run_id} arm {arm}: {len(annotations)} annotations captured")
    return 0


def render_summary() -> dict:
    """What `raw/` holds, never what the last attempt did.

    The first version accumulated a summary as it went and overwrote a good one
    with `{"arm": "D", "http": 403}` for two arms whose captures were on disk —
    which reads as an observation about those runs and is an observation about the
    rate limit. So the summary is a rendering of the directory: an arm is either
    captured, with the paths its annotations carry, or it is not captured, and
    which arm is which is visible from the filesystem rather than from a log.
    """
    out = []
    for run_id, arm, why in RUNS:
        capture = RAW / f"{run_id}.json"
        entry = {"run": run_id, "arm": arm, "why": why, "captured": capture.is_file()}
        if entry["captured"]:
            annotations = json.loads(capture.read_text(encoding="utf-8"))
            entry["annotations"] = len(annotations)
            entry["paths"] = sorted({str(item.get("path")) for item in annotations})
            entry["filed"] = sorted({
                str(item.get("path")) for item in annotations
                if str(item.get("path")) not in (".github", "None")
            })
        out.append(entry)
    return out



def write_summary() -> None:
    RAW.mkdir(exist_ok=True)
    (RAW / "summary.json").write_text(
        json.dumps(render_summary(), indent=2, sort_keys=True) + "\n"
    )


if __name__ == "__main__":
    status = main()
    write_summary()
    sys.exit(status)