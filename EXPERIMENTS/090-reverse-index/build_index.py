#!/usr/bin/env python3
"""Build the module -> distribution reverse index over the top-K PyPI projects.

The index is read straight out of each project's wheel central directory, so an
entry in it is a fact about a file list rather than an inference. Resumable: one
JSONL line per project, appended under an flock, so an interrupted run resumes
without re-reading anything.

Cost accounting is per project, not per run, and the run reports the
distribution rather than the mean - a build's cost is its tail.

status: draft. Run: python3 build_index.py [K]
"""

import fcntl
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(
    os.path.join(HERE, os.pardir, os.pardir, "pyprovides")))
import pyprovides                                    # noqa: E402
from pyprovides import pypi, _pick_wheel, _central_directory, \
    entry_names, top_level_modules                    # noqa: E402

RANKED = os.path.join(HERE, "top-pypi-packages.min.json")
OUT = os.path.join(HERE, "index")
RAW = os.path.join(HERE, "raw-projects.jsonl")
WORKERS = 24

_bytes = [0]
_requests = [0]
_real_get = pyprovides._get


def counting_get(url, headers=None, timeout=30):
    body, hdr = _real_get(url, headers=headers, timeout=timeout)
    _requests[0] += 1
    _bytes[0] += len(body)
    return body, hdr


pyprovides._get = counting_get


def _lock(path):
    """An exclusive flock, held for the whole append. Returns the fd."""
    fd = os.open(path, os.O_CREAT | os.O_RDWR, 0o644)
    fcntl.flock(fd, fcntl.LOCK_EX)
    return fd


def ranked_projects(path=RANKED):
    """[(name, download_count)] in the order the public list gives."""
    with open(path) as fh:
        doc = json.load(fh)
    rows = doc["rows"]
    return [(r["project"], r["download_count"]) for r in rows], doc


def already_done(path=RAW):
    done = {}
    if not os.path.exists(path):
        return done
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except ValueError:
                continue
            done[row["project"]] = row
    return done


def read_one(name):
    t0 = time.time()
    row = {"project": name, "status": None, "modules": [], "seconds": 0.0,
           "wheel_bytes": 0}
    try:
        ok, payload = pypi(name)
        if not ok:
            row["status"] = "no-such-project"
            return row
        row["version"] = payload["info"]["version"]
        wheel = _pick_wheel(payload)
        if wheel is None:
            row["status"] = "no-wheel"
            return row
        total, cd = _central_directory(wheel["url"], wheel.get("size"))
        row["status"] = "ok"
        row["wheel"] = wheel["filename"]
        row["wheel_bytes"] = total
        row["modules"] = sorted(top_level_modules(entry_names(cd)))
    except Exception as exc:                            # noqa: BLE001
        row["status"] = "read-error:%s" % type(exc).__name__
    row["seconds"] = round(time.time() - t0, 3)
    return row


def main(argv):
    k = int(argv[1]) if len(argv) > 1 else 15000
    projects, doc = ranked_projects()
    projects = projects[:k]
    done = already_done()
    todo = [n for n, _ in projects if n not in done]
    print("ranked=%d  already=%d  todo=%d  source_last_update=%s"
          % (len(projects), len(done), len(todo), doc.get("last_update")),
          flush=True)

    os.makedirs(OUT, exist_ok=True)
    started = time.time()
    b0, r0 = _bytes[0], _requests[0]
    # The flock is what makes the append safe: two runs of this script were
    # started by mistake on 2026-10-10 and produced 6,504 duplicate projects,
    # because the docstring claimed a lock the code did not take. A second
    # process now waits here instead of interleaving lines.
    lock = _lock(RAW + ".lock")
    try:
        done = already_done()
        todo = [n for n, _ in projects if n not in done]
        print("  under lock: already=%d todo=%d" % (len(done), len(todo)),
              flush=True)
        fh = open(RAW, "a")
        n_ok = 0
        try:
            with ThreadPoolExecutor(WORKERS) as ex:
                for row in ex.map(read_one, todo):
                    fh.write(json.dumps(row, sort_keys=True) + "\n")
                    if row["status"] == "ok":
                        n_ok += 1
                    if (n_ok % 250) == 0:
                        fh.flush()
                        el = time.time() - started
                        rate = (n_ok + len(done)) / max(el, 1e-9)
                        print("  %d/%d  %.0fs  %.1f proj/s  %.1f MB fetched"
                              % (n_ok, len(todo), el, rate,
                                 (_bytes[0] - b0) / 1e6), flush=True)
        finally:
            fh.close()
    finally:
        fcntl.flock(lock, fcntl.LOCK_UN)
        os.close(lock)
    el = time.time() - started
    print("done in %.0fs  requests=%d  bytes=%.1f MB"
          % (el, _requests[0] - r0, (_bytes[0] - b0) / 1e6), flush=True)
    write_index(projects)
    return 0


def write_index(projects=None):
    """module -> [projects], from every project read so far."""
    done = already_done()
    if projects is None:
        projects = [(r["project"], 0) for r in done.values()]
    order = {n: i for i, (n, _c) in enumerate(projects)}
    index = {}
    for name, row in done.items():
        if row["status"] != "ok":
            continue
        for m in row["modules"]:
            index.setdefault(m, []).append(name)
    rows = sorted(index.items())
    with open(os.path.join(OUT, "index.json"), "w") as fh:
        json.dump({"schema": "e090.index/1", "projects_read": len(done),
                   "modules": len(rows), "index": dict(rows)}, fh, sort_keys=True)
    with open(os.path.join(OUT, "module-provides.tsv"), "w") as fh:
        for m, ps in rows:
            for p in sorted(ps, key=lambda n: order.get(n, 10 ** 9)):
                fh.write("%s\t%s\n" % (m, p))
    print("index: %d modules from %d projects" % (len(rows), len(done)))
    return len(rows)


if __name__ == "__main__":
    sys.exit(main(sys.argv))