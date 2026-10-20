#!/usr/bin/env python3
"""E136 G1: enumerate the HELM lite v1.0.0 run inventory, unauthenticated.

GCS JSON API listing with delimiter='/' so each returned prefix is one run
directory. Paginates if the bucket returns a nextPageToken.

Writes inventory.json next to this script and prints a summary.
"""
import json
import os
import urllib.parse
import urllib.request

BUCKET = "crfm-helm-public"
PREFIX = "lite/benchmark_output/runs/v1.0.0/"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventory.json")


def list_page(token=None):
    params = {
        "prefix": PREFIX,
        "delimiter": "/",
        "maxResults": "1000",
    }
    if token:
        params["pageToken"] = token
    url = ("https://storage.googleapis.com/storage/v1/b/"
           + BUCKET + "/o?" + urllib.parse.urlencode(params))
    req = urllib.request.Request(url, headers={"User-Agent": "e136-inventory/1.0"})
    with urllib.request.urlopen(req, timeout=60) as fh:
        return json.load(fh), url


def main():
    runs = []
    url = None
    token = None
    pages = 0
    while True:
        data, url = list_page(token)
        pages += 1
        runs.extend(data.get("prefixes", []))
        token = data.get("nextPageToken")
        if not token:
            break

    # run dir names look like: "<scenario>:<sub>=<val>,method=<m>,model=<org__name>"
    # extract scenario group = everything before ",method="
    scen = {}
    for r in runs:
        name = r[len(PREFIX):].strip("/")
        group = name.split(",method=")[0]
        scen.setdefault(group, []).append(name)

    inv = {
        "url": url,
        "pages": pages,
        "run_dirs": len(runs),
        "scenario_groups": {k: len(v) for k, v in sorted(scen.items())},
        "runs": sorted(runs),
    }
    with open(OUT, "w") as fh:
        json.dump(inv, fh, indent=1)
        fh.write("\n")

    print(f"run dirs listed        : {len(runs)} (pages: {pages})")
    print(f"scenario groups        : {len(scen)}")
    for g, runs_in_g in sorted(scen.items()):
        print(f"  {len(runs_in_g):4d}  {g}")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
