#!/usr/bin/env python3
"""E136: manifest of the fetched third-party bytes, by sha256.

Repository rule: third-party bulk input is recorded by hash and never
committed. This manifest lets anyone re-fetch the same URLs and verify the
bytes the recomputation read. Covers every byte this experiment fetched:
the 40 run/group files from fetch_cells.py, the published group table, and
the 7 per-instance-stats files.
"""
import hashlib
import json
import os

D = "/tmp/opencode/e136"
HERE = os.path.dirname(os.path.abspath(__file__))

EXTRA = {
    "group_math_chain_of_thought.json":
        "https://storage.googleapis.com/crfm-helm-public/lite/benchmark_output/"
        "releases/v1.0.0/groups/math_chain_of_thought.json",
}
for s in ["algebra", "counting_and_probability", "geometry",
          "intermediate_algebra", "number_theory", "prealgebra",
          "precalculus"]:
    run = ("math:subject=%s,level=1,use_official_examples=False,"
           "use_chain_of_thought=True,model=01-ai_yi-34b" % s)
    EXTRA["pis_math_%s.json" % s] = (
        "https://storage.googleapis.com/crfm-helm-public/lite/benchmark_output/"
        "runs/v1.0.0/%s/per_instance_stats.json" % run)


def main():
    urls = {}
    for m in json.load(open(os.path.join(HERE, "manifest.json"))):
        fname = m["label"]
        urls[os.path.join(D, fname)] = m["url"]
    urls.update({os.path.join(D, k): v for k, v in EXTRA.items()})

    manifest = []
    for path, url in sorted(urls.items()):
        if not os.path.exists(path):
            manifest.append({"file": os.path.basename(path), "url": url,
                             "status": "missing"})
            continue
        blob = open(path, "rb").read()
        manifest.append({
            "file": os.path.basename(path),
            "url": url,
            "bytes": len(blob),
            "sha256": hashlib.sha256(blob).hexdigest(),
            "fetched": "2026-10-14",
        })

    out = os.path.join(HERE, "fetched-manifest.json")
    with open(out, "w") as fh:
        json.dump(manifest, fh, indent=1)
        fh.write("\n")
    ok = sum(1 for m in manifest if "sha256" in m)
    print(f"{ok}/{len(manifest)} bytes hashed; {out} written")


if __name__ == "__main__":
    main()
