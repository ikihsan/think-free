#!/usr/bin/env python3
"""Assemble the E161 corpus from the three already-fetched sources.

  A. vega/vega-datasets   data/*.csv              (git clone, sparse checkout)
  B. rfordatascience/tidytuesday data/2024/*/*.csv (git clone, sparse checkout)
  C. ourworldindata grapher exports               (https)

Frame rule, declared before any file is opened: for each source the first N
paths in sorted order, N = 12.  No file is inspected before it is selected.
Records url, byte size and sha256 for every file taken.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "corpus")
N = 12
UA = "think-free-e161-corpus"

OWID = ["population", "gdp-per-capita", "life-expectancy", "co2-emissions",
        "child-mortality", "internet-users", "urban-population",
        "primary-education", "measles-vaccination", "air-pollution",
        "share-of-women-in-parliament", "electricity-generation"]

SOURCES = [
    ("vega", "/tmp/opencode/vd/data", "https://github.com/vega/vega-datasets"),
    ("tidytuesday", "/tmp/opencode/tt/data/2024",
     "https://github.com/rfordatascience/tidytuesday"),
]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    manifest = []
    for name, root, url in SOURCES:
        if not os.path.isdir(root):
            print("MISSING %s %s" % (name, root))
            continue
        paths = []
        for dirpath, _dirnames, filenames in os.walk(root):
            for f in sorted(filenames):
                if f.lower().endswith(".csv"):
                    paths.append(os.path.join(dirpath, f))
        for i, src in enumerate(sorted(paths)[:N]):
            dst = os.path.join(OUT, "%s-%02d-%s" % (name, i, os.path.basename(src)))
            shutil.copyfile(src, dst)
            manifest.append({"source": name, "url": url + "/blob/main/"
                             + os.path.relpath(src, root.replace("/data/2024", "/data/2024").replace(root, root)),
                             "path": os.path.basename(dst), "bytes": os.path.getsize(dst),
                             "sha256": sha256_file(dst)})
    for i, slug in enumerate(OWID[:N]):
        url = "https://ourworldindata.org/grapher/%s.csv" % slug
        dst = os.path.join(OUT, "owid-%02d-%s.csv" % (i, slug))
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
        except Exception as e:
            print("SKIP %s %s" % (url, e))
            continue
        with open(dst, "wb") as f:
            f.write(data)
        manifest.append({"source": "ourworldindata", "url": url,
                         "path": os.path.basename(dst), "bytes": len(data),
                         "sha256": hashlib.sha256(data).hexdigest()})
    with open(os.path.join(OUT, "manifest.json"), "w") as f:
        json.dump({"frame": "first %d paths in sorted order per source" % N,
                   "files": manifest}, f, indent=2, sort_keys=True)
    for m in manifest:
        print("%-46s %9d  %s" % (m["path"], m["bytes"], m["sha256"][:12]))
    print("corpus: %d files, %d sources"
          % (len(manifest), len({m["source"] for m in manifest})))
    sys.stdout.flush()


if __name__ == "__main__":
    main()