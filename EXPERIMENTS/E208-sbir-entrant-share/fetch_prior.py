#!/usr/bin/env python3
"""E208: fetch every NIH RePORTER R41/R42 project for FY2018-FY2023.

Stopped by the API's own meta.total per fiscal year: no row cap, no sampling,
no seed. Writes raw/prior_years.json with one entry per year carrying the
reported total and the fetched rows, so G2 (per-year completeness) is checkable
from the file alone.

Deterministic; the only external input is the API.
"""
import json
import os
import time
import urllib.request

URL = "https://api.reporter.nih.gov/v2/projects/search"
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
os.makedirs(RAW, exist_ok=True)

YEARS = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]


def fetch_year(fiscal_year, activity_codes=("R41", "R42")):
    """All projects for one fiscal year, stopped by meta.total."""
    rows, seen, offset, reported_total = [], set(), 0, None
    while True:
        payload = json.dumps({
            "criteria": {"fiscal_years": [fiscal_year],
                         "activity_codes": list(activity_codes)},
            "offset": offset,
            "limit": 100,
        }).encode()
        req = urllib.request.Request(
            URL, data=payload,
            headers={"User-Agent": "think-free-research/0.1",
                     "Content-Type": "application/json"},
            method="POST")
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.load(r)
        results = data.get("results", [])
        if reported_total is None:
            reported_total = data.get("meta", {}).get("total", 0)
        if not results:
            break
        for row in results:
            aid = row.get("appl_id")
            if aid not in seen:
                seen.add(aid)
                rows.append(row)
        if len(rows) >= reported_total:
            break
        offset += 100
        time.sleep(0.05)
    return rows, reported_total


def main():
    out = {}
    for year in YEARS:
        rows, total = fetch_year(year)
        out[year] = {"reported_total": total, "fetched": len(rows), "rows": rows}
        print("FY%d R41/R42: reported %s, fetched %d" % (year, total, len(rows)),
              flush=True)
    with open(os.path.join(RAW, "prior_years.json"), "w") as f:
        json.dump(out, f)
    print("wrote raw/prior_years.json (%d bytes)" % os.path.getsize(
        os.path.join(RAW, "prior_years.json")))


if __name__ == "__main__":
    main()
