#!/usr/bin/env python3
"""Run E016's declared phrasings over the two machine corpora.

Reads EXPERIMENTS/016-prior-art-adjudication/phrasings.json, which was committed
before this script existed, and appends one raw record per query to raw/. It
never decides anything: a hit is not a verdict. Attribution is a separate,
recorded step, because F030 showed a count cannot be the property.

Standard library only. Paced for the unauthenticated limits: GitHub search
10/min, crates.io 1/s, npm and PyPI generously but not freely.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
UA = "think-free-e015/1 (+adjudication probe; contact: repository owner)"
GH_SEARCH = "https://api.github.com/search/repositories?q={q}+in:name,description&per_page=5"
NPM_SEARCH = "https://registry.npmjs.org/-/v1/search?text={q}&size=5"
CRATES_SEARCH = "https://crates.io/api/v1/crates?q={q}&per_page=5"
PYPI_SIMPLE = "https://pypi.org/simple/"

# Seconds between requests, per host, from each host's published unauthenticated
# limit. A refused answer is recorded as `refused` and never as an absence.
PACE = {"api.github.com": 7.0, "crates.io": 1.2, "registry.npmjs.org": 1.5}
_last = {}


def fetch(url, host):
    wait = PACE.get(host, 1.0)
    delta = time.time() - _last.get(host, 0.0)
    if delta < wait:
        time.sleep(wait - delta)
    _last[host] = time.time()
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=40) as fh:
            return fh.getcode(), fh.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()
    except Exception as exc:  # network shape, not a verdict either
        return "error:%s" % type(exc).__name__, str(exc).encode()


def append(name, record):
    with open(os.path.join(RAW, name), "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, sort_keys=True) + "\n")


def load_phrasings():
    with open(os.path.join(HERE, "phrasings.json"), encoding="utf-8") as fh:
        return json.load(fh)


def strip_html(text):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text or "")).strip()


def pypi_index():
    """PyPI's search endpoint answers a bot challenge, so the complete project
    name list is used instead. Names only, no descriptions: that is the cost of
    bypassing the challenge, and it is stated rather than hidden."""
    cache = os.path.join(RAW, "pypi-simple-index.txt")
    if os.path.exists(cache):
        with open(cache, encoding="utf-8", errors="replace") as fh:
            names = [ln.strip() for ln in fh]
        with open(os.path.join(RAW, "pypi-simple-meta.json"), encoding="utf-8") as fh:
            meta = json.load(fh)
        return names, meta
    code, body = fetch(PYPI_SIMPLE, "pypi.org")
    if code != 200:
        raise SystemExit("pypi simple index unavailable: %s" % code)
    text = body.decode("utf-8", "replace")
    names = re.findall(r">([^<]+)</a>", text)
    digest = hashlib.sha256(body).hexdigest()
    meta = {
        "url": PYPI_SIMPLE,
        "http_status": code,
        "bytes": len(body),
        "sha256": digest,
        "project_names": len(names),
        "note": "PyPI /search/ returned a 200 'Client Challenge' page on 2026-10-04, "
                "so the full name index was used instead. Names only, no descriptions.",
    }
    with open(os.path.join(RAW, "pypi-simple-meta.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1, sort_keys=True)
    with open(cache, "w", encoding="utf-8") as fh:
        fh.write("\n".join(names))
    return names, meta


def run_github(item, phrasing):
    url = GH_SEARCH.format(q=urllib.parse.quote_plus(phrasing))
    code, body = fetch(url, "api.github.com")
    rec = {"corpus": "github", "index": item["index"], "name": item["name"],
           "phrasing": phrasing, "http_status": code, "url": url}
    if code == 200:
        data = json.loads(body.decode("utf-8"))
        rec["total_count"] = data.get("total_count")
        rec["top"] = [
            {"repo": it.get("full_name"), "stars": it.get("stargazers_count"),
             "description": strip_html(it.get("description"))[:220],
             "pushed_at": it.get("pushed_at")}
            for it in data.get("items", [])
        ]
    else:
        rec["refused"] = body[:200].decode("utf-8", "replace")
    append("github_search.jsonl", rec)
    return rec


def run_npm(item, keyword):
    url = NPM_SEARCH.format(q=urllib.parse.quote_plus(keyword))
    code, body = fetch(url, "registry.npmjs.org")
    rec = {"corpus": "npm", "index": item["index"], "name": item["name"],
           "keyword": keyword, "http_status": code, "url": url}
    if code == 200:
        data = json.loads(body.decode("utf-8"))
        rec["total"] = data.get("total")
        rec["top"] = [
            {"package": o["package"]["name"], "version": o["package"].get("version"),
             "monthly_downloads": o.get("downloads", {}).get("monthly"),
             "description": strip_html(o["package"].get("description"))[:200]}
            for o in data.get("objects", [])
        ]
    else:
        rec["refused"] = body[:200].decode("utf-8", "replace")
    append("registry_search.jsonl", rec)
    return rec


def run_crates(item, keyword):
    url = CRATES_SEARCH.format(q=urllib.parse.quote_plus(keyword))
    code, body = fetch(url, "crates.io")
    rec = {"corpus": "crates", "index": item["index"], "name": item["name"],
           "keyword": keyword, "http_status": code, "url": url}
    if code == 200:
        data = json.loads(body.decode("utf-8"))
        rec["total"] = (data.get("meta") or {}).get("total")
        rec["top"] = [
            {"crate": c.get("name"), "recent_downloads": c.get("recent_downloads"),
             "description": strip_html(c.get("description"))[:200]}
            for c in data.get("crates", [])
        ]
    else:
        rec["refused"] = body[:200].decode("utf-8", "replace")
    append("registry_search.jsonl", rec)
    return rec


def main():
    os.makedirs(RAW, exist_ok=True)
    spec = load_phrasings()
    items = spec["items"]
    # Positive controls first, so a procedure that cannot recover them is caught
    # before it produces an answer about the rest.
    items.sort(key=lambda it: (not it.get("control", False), it["index"]))

    names, meta = pypi_index()
    print("pypi names: %d" % len(names), flush=True)

    for item in items:
        for phrasing in item["github"]:
            rec = run_github(item, phrasing)
            print("gh  %2d %-18s %-46s total=%s" % (
                item["index"], item["name"], phrasing[:46], rec.get("total_count")), flush=True)
        for keyword in item["registry"]:
            hits = [n for n in names if keyword.replace(" ", "-") in n.lower() or keyword in n.lower()]
            append("registry_search.jsonl", {
                "corpus": "pypi", "index": item["index"], "name": item["name"],
                "keyword": keyword, "http_status": 200,
                "url": meta["url"], "match_rule": "substring of the project name, case-insensitive",
                "total": len(hits), "top": [{"package": h} for h in sorted(hits)[:8]],
            })
            print("pypi %2d %-18s %-46s names=%d" % (
                item["index"], item["name"], keyword[:46], len(hits)), flush=True)
            rec = run_npm(item, keyword)
            print("npm %2d %-18s %-46s total=%s" % (
                item["index"], item["name"], keyword[:46], rec.get("total")), flush=True)
            rec = run_crates(item, keyword)
            print("crs %2d %-18s %-46s total=%s" % (
                item["index"], item["name"], keyword[:46], rec.get("total")), flush=True)

    with open(os.path.join(RAW, "probe_run.json"), "w", encoding="utf-8") as fh:
        json.dump({"items": len(items), "queries": "3 registries x keywords + 2 github phrasings per item",
                   "pypi": meta, "pace_seconds": PACE, "user_agent": UA}, fh, indent=1, sort_keys=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
