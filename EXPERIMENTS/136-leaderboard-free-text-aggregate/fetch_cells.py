#!/usr/bin/env python3
"""E136 G2: fetch the pre-declared cells' bytes, unauthenticated.

Fetches, into /tmp/opencode/e136/:
  - releases/v1.0.0/groups.json           (the site's published group table index)
  - every yi-34b run of the math family (7 subject runs x 3 files)
  - the yi-34b gsm run (3 files)
  - every yi-34b run of the mmlu family (5 subject runs x 3 files)

Run names are used in the URL path raw (colons/commas unencoded), the form
E135 fetched successfully. Every fetch records URL, HTTP status, byte count
and sha256 into manifest.json beside this script.
"""
import hashlib
import json
import os
import urllib.request

BUCKET = "https://storage.googleapis.com/crfm-helm-public"
OUTDIR = "/tmp/opencode/e136"
HERE = os.path.dirname(os.path.abspath(__file__))

MATH_SUBJECTS = [
    "algebra", "counting_and_probability", "geometry", "intermediate_algebra",
    "number_theory", "prealgebra", "precalculus",
]
MMLU_SUBJECTS = [
    "abstract_algebra", "college_chemistry", "computer_security",
    "econometrics", "us_foreign_policy",
]
MODEL = "01-ai_yi-34b"


def run_name(fam):
    """Expand a family spec into its run directory names (from the inventory)."""
    inv = json.load(open(os.path.join(HERE, "inventory.json")))
    prefix = "lite/benchmark_output/runs/v1.0.0/" + fam
    return sorted(r.strip("/") for r in inv["runs"]
                  if r.startswith(prefix) and MODEL in r)


def targets():
    t = [("groups.json",
          "lite/benchmark_output/releases/v1.0.0/groups.json")]
    for fam, subs in (("math", MATH_SUBJECTS), ("mmlu", MMLU_SUBJECTS)):
        for name in run_name(fam):
            for f in ("run_spec.json", "scenario_state.json", "stats.json"):
                t.append((f"{fam}__{name.split('/v1.0.0/')[1].split(',model=')[0]}__{f}",
                          f"{name}/{f}"))
    for name in run_name("gsm"):
        for f in ("run_spec.json", "scenario_state.json", "stats.json"):
            t.append((f"gsm__{f}", f"{name}/{f}"))
    return t


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    manifest = []
    for label, path in targets():
        url = BUCKET + "/" + path
        rec = {"label": label, "path": path, "url": url}
        try:
            req = urllib.request.Request(url,
                                         headers={"User-Agent": "e136-fetch/1.0"})
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
