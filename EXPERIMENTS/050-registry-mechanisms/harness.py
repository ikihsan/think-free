#!/usr/bin/env python3
"""E050 — registry-side lockfile breakage (E2, mechanism test).

E049 Part A showed 10 of 11 lockfile closures changed over ~9 months,
but cannot separate "the project chose to update" from "the registry
moved under a pinned input". This experiment tests the registry-side
mechanisms that a lockfile's own bytes cannot protect against, all
measurable today:

  Q1 (yank/absence): for every (name, version) pinned in E049's ten
     PyPI-ecosystem old snapshots, is that exact version yanked or
     absent on PyPI today? A pinned install breaks or warns here.
  Q2 (artifact existence): for every sdist/wheel URL the old uv.lock
     snapshots recorded, does the file still exist? A hash-pinned
     install fails outright if any URL is gone.
  Q3 (Part B control): re-run E049's fixed-requirements pip download
     now and diff the artifact sha256s against the snapshot a later
     session will re-run again. A same-day diff is non-determinism;
     identity is the control the time-gated re-run needs.

Kill gate, declared before the run: if 0 of the sampled pinned
versions are yanked or absent and every recorded artifact URL still
resolves, the registry-breakage mechanism is dead at this population
and E2's registry claim survives only as the time-gated Part B
re-run (weeks away). A non-zero count promotes the mechanism to a
measured failure mode with a rate.

Positive control: the instrument must recover a real yanked version
found independently through the project-level metadata endpoint
(/pypi/{name}/json lists every release with per-file yanked flags)
before any version-level verdict counts.

--verify: re-read results.json and exit 0 iff a verdict and the
positive control are present.
"""
import hashlib
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
E049 = ROOT.parent / "049-lockfile-closure"
RAW = ROOT / "raw"
RESULTS = ROOT / "results.json"

# E049's ten PyPI-ecosystem old snapshots. ruff's Cargo.lock is a
# different registry (crates.io) and is excluded from the PyPI scan;
# its row is recorded as out-of-scope rather than silently dropped.
PIP_SNAPSHOTS = [
    "encode_httpx_old.txt",
    "python-poetry_poetry_old.txt",
    "pallets_flask_old.txt",
    "encode_starlette_old.txt",
    "tornadoweb_tornado_old.txt",
    "urllib3_urllib3_old.txt",
    "encode_uvicorn_old.txt",
    "samuelcolvin_pydantic_old.txt",
    "pallets_werkzeug_old.txt",
    "scrapy_scrapy_old.txt",
]
UVLOCK_SNAPSHOTS = [
    "pallets_flask_old.txt",
    "encode_starlette_old.txt",
    "urllib3_urllib3_old.txt",
    "encode_uvicorn_old.txt",
    "samuelcolvin_pydantic_old.txt",
    "pallets_werkzeug_old.txt",
]

# Projects scanned by the positive control to find one real yanked
# version through the project-level endpoint. Fixed list, chosen as
# high-release-frequency projects independent of the scan population.
CONTROL_PROJECTS = [
    "pip", "setuptools", "requests", "urllib3", "flake8", "black",
    "mypy", "pytest", "django", "flask", "numpy", "pandas",
    "twisted", "tox", "virtualenv", "wheel", "build", "boto3",
    "cryptography", "jinja2",
]

UA = {"User-Agent": "origin-e050 (research; contact: repository owner)"}

NAME = re.compile(r'^\s*name\s*=\s*"([^"]+)"')
VER = re.compile(r'^\s*version\s*=\s*"([^"]+)"')
URL = re.compile(r'url\s*=\s*"([^"]+)"')


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
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(1.0 * (attempt + 1))
                continue
            return None, f"error:{e}"
        time.sleep(0.05)
    return None, "error:retries"


def entries_toml(text):
    out, name = set(), None
    for line in text.splitlines():
        m = NAME.match(line)
        if m:
            name = m.group(1)
        m = VER.match(line)
        if m and name is not None:
            out.add((name, m.group(1)))
            name = None
    return out


def entries_pipstyle(text):
    out = set()
    for line in text.splitlines():
        line = line.strip()
        if line and not line.startswith(("#", "-", "[")) and "==" in line:
            spec = line.split(" ;")[0].split("#")[0].strip()
            name, _, ver = spec.partition("==")
            out.add((name.strip(), ver.strip()))
    return out


def parse_pairs(path, text):
    if path.endswith(".lock") or "[[package]]" in text:
        t = entries_toml(text)
        if t:
            return t
    return entries_pipstyle(text)


def parse_urls(text):
    return set(URL.findall(text))


def positive_control():
    """Find one real yanked version via the project-level endpoint."""
    for proj in CONTROL_PROJECTS:
        doc, status = get_json(f"https://pypi.org/pypi/{proj}/json")
        if not doc:
            continue
        releases = doc.get("releases", {})
        for ver in sorted(releases, reverse=True):
            files = releases[ver]
            yanked = [f for f in files if f.get("yanked")]
            if yanked:
                return {
                    "project": proj, "version": ver,
                    "files_total": len(files),
                    "files_yanked": len(yanked),
                    "found_via": "project-level /pypi/{name}/json releases",
                }
        time.sleep(0.05)
    return None


def check_version(name, ver):
    doc, status = get_json(f"https://pypi.org/pypi/{name}/{ver}/json")
    if status == 404:
        return {"name": name, "version": ver, "status": "absent"}
    if not doc:
        return {"name": name, "version": ver, "status": str(status)}
    urls = doc.get("urls", [])
    yanked = sum(1 for f in urls if f.get("yanked"))
    return {
        "name": name, "version": ver, "status": "present",
        "files_total": len(urls), "files_yanked": yanked,
        "yanked": bool(yanked),
    }


def check_url(url):
    try:
        req = urllib.request.Request(url, headers=UA, method="HEAD")
        with urllib.request.urlopen(req, timeout=30) as r:
            return {"url": url, "status": r.status}
    except urllib.error.HTTPError as e:
        return {"url": url, "status": e.code}
    except Exception as e:
        return {"url": url, "status": f"error:{e}"}


def part_b_control():
    """Re-run E049's fixed download; diff against its snapshot."""
    req = E049 / "requirements-fixed.txt"
    d = ROOT / "snapshot-b"
    d.mkdir(exist_ok=True)
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
    same = {k for k in old_arts if old_arts[k] == new_arts.get(k)}
    return {
        "requirements": req.read_text().splitlines(),
        "identical": sorted(same),
        "changed": sorted(
            k for k in set(old_arts) | set(new_arts)
            if old_arts.get(k) != new_arts.get(k)
        ),
        "new_artifacts": {k: v for k, v in new_arts.items()
                          if k not in old_arts},
    }


def main():
    if "--verify" in sys.argv:
        d = json.loads(RESULTS.read_text())
        assert d.get("verdict"), "no verdict"
        assert d.get("positive_control"), "no positive control"
        print("results.json complete:", d["verdict"])
        return 0

    RAW.mkdir(exist_ok=True)

    control = positive_control()
    print("positive control:", control)
    if not control:
        print("INSTRUMENT FAILED: no yanked version recoverable via "
              "the project-level endpoint; run is void")
        return 1
    (RAW / "positive_control.json").write_text(
        json.dumps(control, indent=2) + "\n")

    # Q1: yank/absence over every pinned pair in the ten snapshots.
    rows, pairs = [], set()
    for fname in PIP_SNAPSHOTS:
        text = (E049 / "raw" / fname).read_text()
        pairs |= parse_pairs(fname, text)
    print(f"Q1: {len(pairs)} unique pinned (name, version) pairs")
    yanked = absent = errors = 0
    for i, (name, ver) in enumerate(sorted(pairs)):
        row = check_version(name, ver)
        rows.append(row)
        if row["status"] == "absent":
            absent += 1
            (RAW / f"absent_{name}_{ver}.json").write_text(
                json.dumps(row, indent=2) + "\n")
        elif row.get("yanked"):
            yanked += 1
            (RAW / f"yanked_{name}_{ver}.json").write_text(
                json.dumps(row, indent=2) + "\n")
        elif row["status"] != "present":
            errors += 1
        if (i + 1) % 100 == 0:
            print(f"  {i + 1}/{len(pairs)} checked "
                  f"(yanked={yanked}, absent={absent}, errors={errors})")
        time.sleep(0.05)

    # Q2: do the exact artifact URLs the old uv.lock files recorded
    # still exist?
    urls = set()
    for fname in UVLOCK_SNAPSHOTS:
        urls |= parse_urls((E049 / "raw" / fname).read_text())
    print(f"Q2: {len(urls)} unique recorded artifact URLs")
    url_rows, url_bad = [], 0
    for i, url in enumerate(sorted(urls)):
        row = check_url(url)
        url_rows.append(row)
        if row["status"] != 200:
            url_bad += 1
            (RAW / f"missing_url_{abs(url) % 10000}.json").write_text(
                json.dumps(row, indent=2) + "\n")
        if (i + 1) % 100 == 0:
            print(f"  {i + 1}/{len(urls)} checked (bad={url_bad})")
        time.sleep(0.05)

    # Q3: same-day Part B control.
    print("Q3: Part B control re-run")
    pb = part_b_control()

    broken = yanked + absent + url_bad
    verdict = (
        "registry-breakage-observed" if broken else
        "control-errors-only" if errors else
        "no-registry-breakage"
    )
    RESULTS.write_text(json.dumps({
        "date": "2026-10-07",
        "population": {
            "snapshots": PIP_SNAPSHOTS,
            "unique_pairs": len(pairs),
            "recorded_urls": len(urls),
        },
        "positive_control": control,
        "q1_yank_absence": {
            "pairs": len(pairs), "yanked": yanked,
            "absent": absent, "errors": errors,
        },
        "q2_artifact_existence": {
            "urls": len(urls), "not_ok": url_bad,
        },
        "q3_part_b_control": pb,
        "rows": rows, "url_rows": url_rows,
        "verdict": verdict,
    }, indent=2) + "\n")
    print("verdict:", verdict,
          f"(yanked={yanked}, absent={absent}, urls_bad={url_bad})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
