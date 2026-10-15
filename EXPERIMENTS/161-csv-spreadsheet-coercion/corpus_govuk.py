#!/usr/bin/env python3
"""E161 frame D: CSVs published by public bodies on data.gov.uk.

Frame rule, declared before any file is fetched: the first 20 packages of the
catalogue's most-recently-modified list, in catalogue order, take the first
usable CSV resource of each.  These are files that councils and agencies
publish for people to open, a different population from the analyst datasets
in frames A-C: they carry postcodes, reference numbers and dates.
"""
import hashlib
import json
import os
import shutil
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "corpus-govuk")
UA = {"User-Agent": "think-free-e161"}
MAX_BYTES = 4 * 1000 * 1000
WANT = 12


def get_json(url):
    return json.loads(urllib.request.urlopen(
        urllib.request.Request(url, headers=UA), timeout=90).read().decode())


def get_bytes(url):
    return urllib.request.urlopen(
        urllib.request.Request(url, headers=UA), timeout=120).read()


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    api = ("https://data.gov.uk/api/3/action/package_search?rows=40"
           "&sort=metadata_modified+desc&q=")
    pkgs = get_json(api)["result"]["results"]
    manifest = []
    for pkg in pkgs:
        if len(manifest) >= WANT:
            break
        for res in pkg.get("resources", []):
            url = res.get("url", "")
            if not url.lower().split("?")[0].endswith(".csv"):
                continue
            try:
                data = get_bytes(url)
            except Exception as e:
                print("SKIP %s (%s)" % (url[:70], type(e).__name__))
                sys.stdout.flush()
                continue
            if not data or len(data) > MAX_BYTES:
                continue
            name = "govuk-%02d-%s" % (len(manifest),
                                      os.path.basename(url.split("?")[0]) or "data.csv")
            with open(os.path.join(OUT, name), "wb") as f:
                f.write(data)
            manifest.append({"source": "govuk", "url": url, "path": name,
                             "bytes": len(data),
                             "sha256": hashlib.sha256(data).hexdigest(),
                             "package": pkg.get("title", "")[:80]})
            print("got %-42s %8d  %s" % (name[:42], len(data),
                                         hashlib.sha256(data).hexdigest()[:12]))
            sys.stdout.flush()
            break
    with open(os.path.join(OUT, "manifest.json"), "w") as f:
        json.dump({"frame": "data.gov.uk package_search, metadata_modified desc, "
                            "first CSV resource of each of the first %d packages" % WANT,
                   "files": manifest}, f, indent=2, sort_keys=True)
    print("frame D: %d files" % len(manifest))


if __name__ == "__main__":
    main()