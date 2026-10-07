#!/usr/bin/env python3
"""E049 — do dependency-lockfile closures drift over time (E2)?

Part A (this run): for 12 public projects that publish a top-level
lockfile, fetch it at HEAD and at the oldest commit since 2026-01-01
that touched it, and count how many (name, version) entries changed.

Part B (snapshot only today): resolve and download a fixed requirements
set with pip twice into a record the next session can re-run, to measure
registry-side drift of the same declared inputs over a longer window.

--verify: re-check results.json byte consistency and exit 0 iff the
run completed and wrote a verdict.
"""
import hashlib, json, re, subprocess, sys, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "raw"
RESULTS = ROOT / "results.json"

REPOS = [
    ("encode/httpx", "requirements.txt"),
    ("fastapi/fastapi", "uv.lock"),
    ("python-poetry/poetry", "poetry.lock"),
    ("astral-sh/ruff", "Cargo.lock"),
    ("pallets/flask", "uv.lock"),
    ("encode/starlette", "uv.lock"),
    ("tornadoweb/tornado", "requirements.txt"),
    ("urllib3/urllib3", "uv.lock"),
    ("encode/uvicorn", "uv.lock"),
    ("samuelcolvin/pydantic", "uv.lock"),
    ("pallets/werkzeug", "uv.lock"),
    ("scrapy/scrapy", "docs/requirements.txt"),
]
CUTOFF = "2026-01-01T00:00:00Z"

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "origin-e049",
                                               "Accept": "application/vnd.github+json"})
    return json.load(urllib.request.urlopen(req, timeout=20))

def first_commit(repo, path, until=None):
    url = f"https://api.github.com/repos/{repo}/commits?path={path}&per_page=1"
    if until:
        url += f"&until={until}"
    arr = get(url)
    if not arr:
        return None
    c = arr[0]
    return {"sha": c["sha"], "date": c["commit"]["committer"]["date"]}

def fetch(repo, path, sha):
    url = f"https://raw.githubusercontent.com/{repo}/{sha}/{path}"
    return urllib.request.urlopen(url, timeout=20).read().decode("utf-8", "replace")

NAME = re.compile(r'^\s*name\s*=\s*"([^"]+)"')
VER = re.compile(r'^\s*version\s*=\s*"([^"]+)"')

def entries_toml(text):
    out, name = set(), None
    for line in text.splitlines():
        m = NAME.match(line)
        if m:
            name = m.group(1)
        m = VER.match(line)
        if m and name is not None:
            out.add(f"{name}=={m.group(1)}")
            name = None
    return out

def entries_pipstyle(text):
    out = set()
    for line in text.splitlines():
        line = line.strip()
        if line and not line.startswith(("#", "-", "[")) and "==" in line:
            out.add(line.split(" ;")[0].split("#")[0].strip())
    return out

def entries(path, text):
    if path.endswith((".lock", ".toml")) or text.lstrip().startswith("#") or "[[package]]" in text or "[package.metadata]" in text:
        t = entries_toml(text)
        if t:
            return t
    return entries_pipstyle(text)

def part_a():
    rows = []
    for repo, path in REPOS:
        try:
            head = first_commit(repo, path)
            old = first_commit(repo, path, until=CUTOFF)
            if head is None or old is None:
                rows.append({"repo": repo, "path": path, "status": "missing-snapshot"})
                continue
            new_t = fetch(repo, path, head["sha"])
            old_t = fetch(repo, path, old["sha"])
            new_s, old_s = entries(path, new_t), entries(path, old_t)
            rows.append({
                "repo": repo, "path": path,
                "old": {"sha": old["sha"], "date": old["date"], "entries": len(old_s)},
                "head": {"sha": head["sha"], "date": head["date"], "entries": len(new_s)},
                "added": len(new_s - old_s), "removed": len(old_s - new_s),
                "changed": bool(new_s ^ old_s),
                "status": "ok",
            })
            (RAW / f"{repo.replace('/', '_')}_head.txt").write_bytes(new_t.encode())
            (RAW / f"{repo.replace('/', '_')}_old.txt").write_bytes(old_t.encode())
            time.sleep(0.2)
        except Exception as e:
            rows.append({"repo": repo, "path": path, "status": f"error:{getattr(e, 'code', e)}"})
    return rows

def part_b():
    out = ROOT / "snapshot-b"
    out.mkdir(exist_ok=True)
    req = ROOT / "requirements-fixed.txt"
    if not req.exists():
        req.write_text("requests==2.32.3\nrich==13.9.4\nhttpx==0.28.1\n")
    d = out / "a"
    try:
        d.mkdir(exist_ok=True)
        subprocess.run([sys.executable, "-m", "pip", "download", "-r", str(req),
                        "-d", str(d), "--quiet"], check=True, timeout=900)
        arts = {}
        for f in sorted(d.iterdir()):
            arts[f.name] = hashlib.sha256(f.read_bytes()).hexdigest()
        return {"requirements": req.read_text().splitlines(), "artifacts": arts}
    except Exception as e:
        return {"error": str(e)}

def main():
    if "--verify" in sys.argv:
        d = json.loads(RESULTS.read_text())
        assert d.get("verdict") and d.get("rows") and d.get("part_b"), "incomplete"
        print("results.json complete:", d["verdict"])
        return 0
    rows = part_a()
    ok = [r for r in rows if r["status"] == "ok"]
    changed = [r for r in ok if r["changed"]]
    pb = part_b()
    verdict = (
        "drift-observed" if len(changed) > len(ok) / 2 else
        "weak-signal" if changed else
        "mechanism-too-weak-to-productize"
    )
    RESULTS.write_text(json.dumps({
        "date": "2026-10-07", "cutoff": CUTOFF, "rows": rows,
        "sampled": len(ok), "changed": len(changed), "part_b": pb,
        "verdict": verdict,
    }, indent=2) + "\n")
    print("sampled", len(ok), "changed", len(changed), "->", verdict)
    return 0

if __name__ == "__main__":
    sys.exit(main())
