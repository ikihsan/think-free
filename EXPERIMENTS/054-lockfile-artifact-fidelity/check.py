#!/usr/bin/env python3
"""E054: for artifacts pinned in E049's old uv.lock snapshots, fetch the
recorded URL today and compare the live bytes' sha256 to the hash the
lockfile recorded in 2025-09..2025-12."""
import hashlib
import json
import re
import sys
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

RAW = Path("EXPERIMENTS/049-lockfile-closure/raw")
OUT = Path("EXPERIMENTS/054-lockfile-artifact-fidelity/results.json")
SAMPLE_EVERY = 7  # deterministic stride over the sorted URL set

ENTRY = re.compile(r'url = "([^"]+)", hash = "sha256:([0-9a-f]{64})"')


def collect():
    entries = {}
    for path in sorted(RAW.glob("*_old.txt")):
        for url, digest in ENTRY.findall(path.read_text()):
            entries[url] = {"url": url, "recorded_sha256": digest, "where": path.name}
    return [entries[u] for u in sorted(entries)]


def fetch(entry):
    req = urllib.request.Request(entry["url"], headers={"User-Agent": "think-free-e054"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read()
        live = hashlib.sha256(body).hexdigest()
        return {**entry, "status": "ok", "live_sha256": live,
                "match": live == entry["recorded_sha256"], "bytes": len(body)}
    except urllib.error.HTTPError as e:
        return {**entry, "status": f"http_{e.code}", "match": False}
    except Exception as e:  # noqa: BLE001 - record, do not crash
        return {**entry, "status": type(e).__name__, "match": False}


def main():
    all_entries = collect()
    sample = all_entries[::SAMPLE_EVERY]
    print(f"pool={len(all_entries)} sample={len(sample)}")
    rows = []
    started = time.time()
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(fetch, e) for e in sample]
        for i, fut in enumerate(as_completed(futures), 1):
            rows.append(fut.result())
            if i % 50 == 0:
                print(f"  {i}/{len(sample)} done", flush=True)
    mismatches = [r for r in rows if r["status"] == "ok" and not r["match"]]
    failures = [r for r in rows if r["status"] != "ok"]
    verdict = "artifact-drift-observed" if mismatches else (
        "artifacts-unavailable" if failures and len(failures) == len(rows) else "no-artifact-drift")
    result = {
        "date": "2026-10-08",
        "pool": len(all_entries),
        "sample": len(rows),
        "stride": SAMPLE_EVERY,
        "elapsed_s": round(time.time() - started, 1),
        "matches": sum(1 for r in rows if r.get("match")),
        "byte_mismatches": len(mismatches),
        "fetch_failures": len(failures),
        "verdict": verdict,
        "mismatch_rows": mismatches[:10],
        "failure_rows": failures[:10],
    }
    OUT.write_text(json.dumps(result, indent=2))
    print(json.dumps({k: v for k, v in result.items() if not isinstance(v, list)}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
