#!/usr/bin/env python3
"""E137 G2: fetch the math_chain_of_thought runs for 01-ai_yi-6b, unauthenticated.

Fetches, into /tmp/opencode/e137/:
  - releases/v1.0.0/groups/math_chain_of_thought.json (the site's published group table)
  - every yi-6b run of the math family (7 subject runs x 3 files: run_spec, scenario_state, stats)
  - per_instance_stats.json for each of the 7 subject runs

Run names are used in the URL path raw (colons/commas unencoded). Every fetch
records URL, HTTP status, byte count and sha256 into manifest.json beside this
script.
"""
import hashlib
import json
import os
import urllib.request

BUCKET = "https://storage.googleapis.com/crfm-helm-public"
OUTDIR = "/tmp/opencode/e137"
HERE = os.path.dirname(os.path.abspath(__file__))

MATH_SUBJECTS = [
    "algebra", "counting_and_probability", "geometry", "intermediate_algebra",
    "number_theory", "prealgebra", "precalculus",
]
MODEL = "01-ai_yi-6b"


def run_name(fam):
    """Expand a family spec into its run directory names (from the inventory)."""
    inv = json.load(open(os.path.join(HERE, "inventory.json")))
    prefix = "lite/benchmark_output/runs/v1.0.0/" + fam
    return sorted(r.strip("/") for r in inv["runs"]
                  if r.startswith(prefix) and MODEL in r)


def targets():
    t = [("group_math_chain_of_thought.json",
          "lite/benchmark_output/releases/v1.0.0/groups/math_chain_of_thought.json")]
    for fam, subs in (("math", MATH_SUBJECTS),):
        for name in run_name(fam):
            for f in ("run_spec.json", "scenario_state.json", "stats.json"):
                t.append((f"{fam}__{name.split('/v1.0.0/')[1].split(',model=')[0]}__{f}",
                          f"{name}/{f}"))
            # per_instance_stats.json
            t.append((f"pis_{fam}_{name.split('/v1.0.0/')[1].split(',model=')[0]}.json",
                      f"{name}/per_instance_stats.json"))
    return t


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    manifest = []
    for label, path in targets():
        url = BUCKET + "/" + path
        rec = {"label": label, "path": path, "url": url}
        try:
            req = urllib.request.Request(url,
                                         headers={"User-Agent": "e137-fetch/1.0"})
            with urllib.request.urlopen(req, timeout=120) as fh:
                blob = fh.read()
            rec["status"] = 200
            rec["bytes"] = len(blob)
            rec["sha256"] = hashlib.sha256(blob).hexdigest()
            with open(os.path.join(OUTDIR, label), "wb") as fh:
                fh.write(blob)
        except Exception as exc:  # HTTPError and friends
            rec["status"] = getattr(exc, "code", None) or "error"
            rec["error"] = str(exc)[:200]
        manifest.append(rec)
        print(f"{rec['status']:>4} {rec.get('bytes', 0):>9}  {label}")

    with open(os.path.join(HERE, "manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=1)
        fh.write("\n")
    ok = sum(1 for m in manifest if m["status"] == 200)
    print(f"\n{ok}/{len(manifest)} fetched 200; manifest.json written")


if __name__ == "__main__":
    main()