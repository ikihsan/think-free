#!/usr/bin/env python3
"""E050 — registry-side lockfile breakage (E2 mechanism test).

E049 measured that 10 of 11 lockfile closures changed
over ~9 months, but Part A cannot separate "the project
chose to update" from "the registry moved under a pinned
input". This experiment tests the registry-side
mechanisms a lockfile's own bytes cannot protect
against, all measurable today.

**Question, declared before the run.** For every
(name, version) pinned in E049's ten PyPI-ecosystem old
snapshots, is that exact version yanked or absent on PyPI
today? And does every sdist/wheel URL those snapshots
recorded still resolve?

**Kill gate, declared before the run.** 0 of the sampled
pinned versions yanked or absent, and every recorded
artifact URL resolving, kills the registry-breakage
mechanism at this population. E2's registry claim then
survives only as the time-gated Part B re-run.

**Positive control.** The instrument must recover a real
yanked version through the project-level metadata endpoint
(`/pypi/{name}/json` lists every release with per-file
`yanked` flags) before any version-level verdict counts.

Every check is cached under `raw/rows/` and `raw/urls/`
as it completes, so an interrupted run resumes instead
of re-asking the registry. The first run's four "absent"
hits were instrument artifacts (extras in names, editable
self-entries); see `e049format.py` and the README.

--verify: re-read results.json; exit 0 iff a verdict and
the positive control are present.
"""
import hashlib
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import e049format

ROOT = Path(__file__).resolve().parent
E049 = ROOT.parent / "049-lockfile-closure"
RAW = ROOT / "raw"
ROWS = RAW / "rows"
URLS = RAW / "urls"
RESULTS = ROOT / "results.json"
CONTROL_PROJECTS = [
    "pip", "setuptools", "requests", "urllib3", "flake8",
    "black", "mypy", "pytest", "django", "flask", "numpy",
    "pandas", "twisted", "tox", "virtualenv", "wheel",
    "build", "boto3", "cryptography", "jinja2",
]
UA = {"User-Agent": "origin-e050 (research; repository owner)"}


def get_json(url, retries=3):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r), r.status
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None, 404
            if e.code == 429 and attempt < retries - 1:
                time.sleep(2.0 * (attempt + 1))
                continue
            return None, e.code
        except Exception:
            if attempt < retries - 1:
                time.sleep(1.0 * (attempt + 1))
                continue
            return None, "error"
    return None, "error:retries"


def positive_control():
    for proj in CONTROL_PROJECTS:
        doc, status = get_json(f"https://pypi.org/pypi/{proj}/json")
        if not doc:
            continue
        for ver in sorted(doc.get("releases", {}), reverse=True):
            files = doc["releases"][ver]
            yanked = sum(1 for f in files if f.get("yanked"))
            if yanked:
                return {
                    "project": proj, "version": ver,
                    "files_total": len(files),
                    "files_yanked": yanked,
                    "found_via": "project-level /pypi/{name}/json",
                }
        time.sleep(0.05)
    return None


def check_version(name, ver):
    doc, status = get_json(f"https://pypi.org/pypi/{name}/{ver}/json")
    if status == 404:
        return {"name": name, "version": ver, "status": "absent"}
    if not doc:
        return {"name": name, "version": ver, "status": str(status)}
    files = doc.get("urls", [])
    yanked = sum(1 for f in files if f.get("yanked"))
    return {
        "name": name, "version": ver, "status": "present",
        "files_total": len(files), "files_yanked": yanked,
        "yanked": bool(yanked),
    }


def check_url(url, retries=3):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=UA, method="HEAD")
            with urllib.request.urlopen(req, timeout=30) as r:
                return {"status": r.status}
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < retries - 1:
                time.sleep(2.0 * (attempt + 1))
                continue
            return {"status": e.code}
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(1.0 * (attempt + 1))
                continue
            return {"status": f"error:{type(e).__name__}"}
    return {"status": "error:retries"}


def cached_scan(items, cache_dir, check, keyfmt):
    """Check every item, caching one JSON per item on disk."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    out = []
    pending = []
    for key, item in items:
        cfile = cache_dir / (keyfmt.format(key=key))
        if cfile.exists():
            out.append(json.loads(cfile.read_text()))
        else:
            pending.append((key, item, cfile))
    total = len(items)
    for i, (key, item, cfile) in enumerate(pending):
        row = check(item)
        row["_key"] = key
        cfile.write_text(json.dumps(row, indent=2) + "\n")
        out.append(row)
        if (i + 1) % 100 == 0 or i == len(pending) - 1:
            print(f"  {len(out)}/{total} (pending {len(pending) - i - 1})")
        time.sleep(0.05)
    return out


def part_b_control():
    d = ROOT / "snapshot-b"
    d.mkdir(exist_ok=True)
    req = E049 / "requirements-fixed.txt"
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "download", "-r", str(req),
             "-d", str(d), "--quiet"],
            check=True, timeout=900,
        )
    except Exception as e:
        return {"error": str(e)}
    old = json.loads((E049 / "results.json").read_text())
    old_arts = old["part_b"]["artifacts"]
    new_arts = {f.name: hashlib.sha256(f.read_bytes()).hexdigest()
                for f in sorted(d.iterdir())}
    return {
        "requirements": req.read_text().splitlines(),
        "identical": sorted(k for k in old_arts
                             if old_arts[k] == new_arts.get(k)),
        "changed": sorted(k for k in set(old_arts) | set(new_arts)
                           if old_arts.get(k) != new_arts.get(k)),
    }


def main():
    if "--verify" in sys.argv:
        d = json.loads(RESULTS.read_text())
        assert d.get("verdict") and d.get("positive_control"), "incomplete"
        print("results.json complete:", d["verdict"])
        return 0

    RAW.mkdir(parents=True, exist_ok=True)
    control = positive_control()
    print("positive control:", control)
    if not control:
        print("INSTRUMENT FAILED: no yanked version recoverable; "
              "run is void")
        return 1
    (RAW / "positive_control.json").write_text(
        json.dumps(control, indent=2) + "\n")

    # Q1: yank/absence over every registry-pinned pair.
    pairs, excluded = set(), 0
    snap_root, pip_snaps, uv_snaps = e049format.snapshot_names()
    for fname, orig in pip_snaps:
        found, exc = e049format.parse_pairs(
            orig, (snap_root / fname).read_text())
        pairs |= found
        excluded += exc
    print(f"Q1: {len(pairs)} unique pinned pairs "
          f"({excluded} local/workspace entries excluded)")
    items = sorted((f"{n}__{v}", (n, v)) for n, v in pairs)
    rows = cached_scan(items, ROWS, lambda nv: check_version(*nv),
                       "{key}.json")

    # Q2: do the recorded artifact URLs still resolve?
    urls = set()
    for fname, _orig in uv_snaps:
        urls |= e049format.parse_urls(
            (snap_root / fname).read_text())
    print(f"Q2: {len(urls)} unique recorded artifact URLs")
    uitems = sorted((hashlib.sha1(u.encode()).hexdigest(), u)
                    for u in urls)
    url_rows = cached_scan(uitems, URLS, check_url, "{key}.json")

    # Q3: same-day Part B control.
    print("Q3: Part B control re-run")
    pb = part_b_control()

    yanked = sum(1 for r in rows if r.get("yanked"))
    absent = sum(1 for r in rows if r.get("status") == "absent")
    errors = sum(1 for r in rows
                 if r.get("status") not in ("present", "absent"))
    url_bad = sum(1 for r in url_rows if r.get("status") != 200)
    broken = yanked + absent + url_bad
    verdict = ("registry-breakage-observed" if broken
               else "control-errors-only" if errors
               else "no-registry-breakage")
    RESULTS.write_text(json.dumps({
        "date": "2026-10-07",
        "population": {
            "snapshots": pip_snaps, "unique_pairs": len(pairs),
            "local_entries_excluded": excluded,
            "recorded_urls": len(urls),
        },
        "positive_control": control,
        "q1_yank_absence": {"pairs": len(pairs), "yanked": yanked,
                            "absent": absent, "errors": errors},
        "q2_artifact_existence": {"urls": len(urls),
                                  "not_ok": url_bad},
        "q3_part_b_control": pb,
        "verdict": verdict,
    }, indent=2) + "\n")
    print("verdict:", verdict,
          f"(yanked={yanked}, absent={absent}, urls_bad={url_bad})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
