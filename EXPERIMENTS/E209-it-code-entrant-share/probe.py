#!/usr/bin/env python3
"""E209 instrument probe -- ONE page, reconnaissance only.

Not the experiment population. This checks, before any protocol is written,
that `spending_by_category/recipient/` accepts a single-calendar-year
`time_period`, that the recipient objects carry a stable identity field, and
that pagination metadata is well formed. E198 used a six-year window; this
probe establishes that a one-year window behaves the same way.
"""
import json
import os
import sys
import urllib.request

BASE = "https://api.usaspending.gov/api/v2/search/"
UA = "think-free-research/0.1 (+repository federal-spend entrant experiment probe)"
HERE = os.path.dirname(os.path.abspath(__file__))


def post(endpoint, payload):
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        BASE + endpoint, data=body,
        headers={"User-Agent": UA, "Content-Type": "application/json",
                 "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.status, json.loads(r.read().decode("utf-8", "replace"))


def main():
    out = {}
    # One IT code, single calendar year (FY2023 in this record's convention).
    payload = {
        "filters": {
            "time_period": [{"start_date": "2023-01-01", "end_date": "2023-12-31"}],
            "award_type_codes": ["A", "B", "C", "D"],
            "psc_codes": ["DA01"],
        },
        "limit": 100,
        "page": 1,
        "spending_level": "awards",
    }
    status, parsed = post("spending_by_category/recipient/", payload)
    results = parsed.get("results") or []
    out["da01_2023"] = {
        "status": status,
        "n_results": len(results),
        "hasNext": (parsed.get("page_metadata") or {}).get("hasNext"),
        "messages": parsed.get("messages"),
        "result_keys": sorted(results[0].keys()) if results else [],
        "sample": results[0] if results else None,
        "recipient_id_present": sum(1 for r in results if r.get("recipient_id")),
        "uei_present": sum(1 for r in results if r.get("uei")),
        "code_present": sum(1 for r in results if r.get("code")),
    }
    # Control: a well-formed non-existent code must return a well-formed empty 200.
    ctl = dict(payload)
    ctl["filters"] = dict(payload["filters"], psc_codes=["ZZZZ"])
    status2, parsed2 = post("spending_by_category/recipient/", ctl)
    out["ctl_zzzz"] = {"status": status2, "n_results": len(parsed2.get("results") or [])}
    path = os.path.join(HERE, "raw_probe.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
