#!/usr/bin/env python3
"""E209 fetch -- every recipient page for the five IT codes, current and prior windows.

Mirrors E198's client: each response body is written to `raw/` with its sha256
before parsing, and a `.meta.json` records the exact request. A cached body is
reused only when the stored request key matches exactly, so a changed window or
code can never read a stale body back as fresh.
"""
import hashlib
import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
UA = "think-free-research/0.1 (+repository federal-spend entrant experiment)"
BASE = "https://api.usaspending.gov/api/v2/search/"

CODES = ["DA01", "DA10", "7A21", "7030", "D304"]
AWARD_TYPES = ["A", "B", "C", "D"]

WINDOWS = {
    "current": [{"start_date": "2023-01-01", "end_date": "2023-12-31"}],
    "prior": [{"start_date": "2018-01-01", "end_date": "2022-12-31"}],
}


def base_filters(window, **extra):
    f = {"time_period": window, "award_type_codes": AWARD_TYPES}
    f.update(extra)
    return f


def call(payload, capture_name, retries=2, pause=0.5):
    os.makedirs(RAW, exist_ok=True)
    url = BASE + "spending_by_category/recipient/"
    body = json.dumps(payload).encode()
    meta_path = os.path.join(RAW, capture_name + ".meta.json")
    for suffix in (".json", ".body"):
        body_path = os.path.join(RAW, capture_name + suffix)
        if os.path.exists(body_path) and os.path.exists(meta_path):
            try:
                prior = json.load(open(meta_path))
                if (prior.get("request") == payload
                        and prior.get("response", {}).get("endpoint") == url):
                    with open(body_path, "rb") as fh:
                        cached = fh.read()
                    meta = dict(prior["response"], reused=True)
                    try:
                        return (meta.get("status"),
                                json.loads(cached.decode("utf-8", "replace")), meta)
                    except Exception:
                        break
            except Exception:
                break
    last = (None, b"")
    status, raw = None, b""
    for attempt in range(retries + 1):
        req = urllib.request.Request(
            url, data=body,
            headers={"User-Agent": UA, "Content-Type": "application/json",
                     "Accept": "application/json"})
        try:
            with urllib.request.urlopen(
                    req, timeout=180,
                    context=ssl.create_default_context()) as r:
                status, raw = r.status, r.read()
            break
        except urllib.error.HTTPError as e:
            status, raw = e.code, e.read()
            last = (status, raw)
            if e.code not in (429, 500, 502, 503, 504) and attempt == retries:
                break
        except Exception as e:
            last = (None, ("%s: %s" % (type(e).__name__, e)).encode())
            raw = b""
            if attempt == retries:
                break
        time.sleep(pause * (attempt + 1))
    else:
        status, raw = last

    with open(os.path.join(RAW, capture_name + ".json"), "wb") as fh:
        fh.write(raw or b"")
    meta = {"endpoint": url, "status": status, "bytes": len(raw or b""),
            "sha256": hashlib.sha256(raw or b"").hexdigest()}
    with open(os.path.join(RAW, capture_name + ".meta.json"), "w") as fh:
        json.dump({"request": payload, "response": meta}, fh, indent=1,
                  sort_keys=True)
    try:
        parsed = json.loads((raw or b"").decode("utf-8", "replace"))
    except Exception:
        parsed = None
    return status, parsed, meta


def fetch_window(code, window_name):
    window = WINDOWS[window_name]
    all_results, statuses, unused = [], [], []
    page, has_next = 1, True
    while has_next:
        payload = {
            "filters": base_filters(window, psc_codes=[code]),
            "limit": 100, "page": page, "spending_level": "awards",
        }
        name = "%s_%s_p%d" % (window_name, code, page)
        st, parsed, meta = call(payload, name)
        statuses.append({"page": page, "status": st,
                         "reused": meta.get("reused", False)})
        if st != 200 or not isinstance(parsed, dict):
            break
        results = parsed.get("results") or []
        all_results.extend(results)
        msgs = parsed.get("messages") or []
        unused.extend(m for m in msgs
                      if isinstance(m, str) and "were not used" in m)
        page_meta = parsed.get("page_metadata") or {}
        has_next = page_meta.get("hasNext", False)
        page += 1
        if page > 500:
            statuses.append({"page": page, "status": "CEILING",
                             "reused": False})
            break
    return {"code": code, "window": window_name, "rows": all_results,
            "statuses": statuses, "unused_filters": unused}


def main():
    summary = {}
    for code in CODES:
        for window_name in WINDOWS:
            rec = fetch_window(code, window_name)
            summary["%s_%s" % (window_name, code)] = {
                "rows": len(rec["rows"]),
                "pages": len([s for s in rec["statuses"]
                              if s["status"] == 200]),
                "statuses": rec["statuses"],
                "unused_filters": rec["unused_filters"],
            }
            print("%s %s: %d rows, %d pages, unused=%d"
                  % (window_name, code, len(rec["rows"]),
                     summary["%s_%s" % (window_name, code)]["pages"],
                     len(rec["unused_filters"])), flush=True)
    with open(os.path.join(RAW, "fetch_summary.json"), "w") as fh:
        json.dump(summary, fh, indent=1, sort_keys=True)
    print("wrote fetch_summary.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
