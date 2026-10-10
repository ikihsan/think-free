#!/usr/bin/env python3
"""What does a central-directory read actually transfer?

`build_index.py` counted requests and bytes for the 4,962-project resume it
completed and lost the earlier runs', so `raw-projects.jsonl` records
`wheel_bytes` -- the size of the wheel -- and not the bytes that moved. The two
are not the same number, and the difference is the whole claim in
`pyprovides/README.md`: "a 12 MB wheel is answered from a 64 KiB window". This
file measures the second number directly, on a sample of the projects the build
already read, so the transfer figure in E090's cost section is observed on a
sample and labelled as an extrapolation to the full build rather than presented
as a total that was never recorded.

Sampling unit: a distinct project, drawn at random from the projects whose
`status` is `ok`, with a fixed seed declared here. `wheel_bytes` is the full
size of the wheel the build chose; `bytes_fetched` and `requests` are what
re-reading that wheel's central directory moved.

status: draft. Run: python3 transfer_cost.py [n]
"""

import json
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, os.pardir, os.pardir, "pyprovides"))
import pyprovides                                    # noqa: E402
from pyprovides import pypi, _pick_wheel, _central_directory  # noqa: E402

RAW = os.path.join(HERE, "raw-projects.jsonl")
OUT = os.path.join(HERE, "transfer-cost.json")
SEED = 20261010

_bytes = [0]
_requests = [0]
_real_get = pyprovides._get


def counting_get(url, headers=None, timeout=30):
    body, hdr = _real_get(url, headers=headers, timeout=timeout)
    _requests[0] += 1
    _bytes[0] += len(body)
    return body, hdr


pyprovides._get = counting_get


def main(argv):
    n = int(argv[1]) if len(argv) > 1 else 60
    rows = {}
    with open(RAW) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            if r.get("status") == "ok":
                rows.setdefault(r["project"], r)
    pool = sorted(rows)
    rng = random.Random(SEED)
    sample = rng.sample(pool, min(n, len(pool)))

    out_rows = []
    for name in sample:
        b0, q0, t0 = _bytes[0], _requests[0], time.time()
        try:
            ok, payload = pypi(name)
            if not ok:
                out_rows.append({"project": name, "status": "no-such-project"})
                continue
            wheel = _pick_wheel(payload)
            if wheel is None:
                out_rows.append({"project": name, "status": "no-wheel"})
                continue
            total, cd = _central_directory(wheel["url"], wheel.get("size"))
            out_rows.append({
                "project": name, "status": "ok",
                "wheel_bytes": total, "wheel": wheel["filename"],
                "bytes_fetched": _bytes[0] - b0,
                "requests": _requests[0] - q0,
                "seconds": round(time.time() - t0, 3)})
        except Exception as exc:                        # noqa: BLE001
            out_rows.append({"project": name,
                             "status": "read-error:%s" % type(exc).__name__})

    good = [r for r in out_rows if r["status"] == "ok"]

    def dist(key):
        v = sorted(r[key] for r in good)
        if not v:
            return {}
        return {"n": len(v), "p50": v[len(v) // 2],
                "p90": v[int(0.9 * len(v))], "p99": v[min(len(v) - 1,
                                                          int(0.99 * len(v)))],
                "max": v[-1], "mean": round(sum(v) / len(v), 1),
                "total": sum(v)}

    fb, wb, rq = dist("bytes_fetched"), dist("wheel_bytes"), dist("requests")
    n_ok = sum(1 for line in open(RAW) if '"status": "ok"' in line)
    ratio = (fb["mean"] / wb["mean"]) if fb.get("mean") and wb.get("mean") else None
    doc = {
        "schema": "e090.transfer-cost/1",
        "seed": SEED,
        "sampling_unit": "a distinct project with status ok, drawn at random "
                         "from the projects build_index.py read",
        "sampled": len(out_rows),
        "measured_ok": len(good),
        "bytes_fetched": fb,
        "requests": rq,
        "wheel_bytes": wb,
        "fetched_share_of_wheel": round(ratio, 6) if ratio else None,
        "extrapolation_note": "the full build's transferred bytes were not "
                              "logged for the first %d projects; the total below "
                              "is the measured per-project distribution "
                              "multiplied by the number of ok projects, and is "
                              "labelled inferred"
                              % (15000 - n_ok if n_ok else 0),
        "extrapolated_full_build_bytes": int(fb["mean"] * 15000)
                                        if fb.get("mean") else None,
        "extrapolated_full_build_requests": int(rq["mean"] * 15000)
                                            if rq.get("mean") else None,
        "rows": out_rows,
    }
    with open(OUT, "w") as fh:
        json.dump(doc, fh, indent=1, sort_keys=True)
    print("sampled %d, ok %d" % (len(out_rows), len(good)))
    print("bytes fetched per project:", json.dumps(fb))
    print("requests per project:", json.dumps(rq))
    print("wheel bytes per project:", json.dumps(wb))
    print("fetched share of wheel: %s" % doc["fetched_share_of_wheel"])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))