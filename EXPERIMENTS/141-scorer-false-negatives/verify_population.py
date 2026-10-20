#!/usr/bin/env python3
"""E141 G0 (provenance): re-hash every population file before any measurement.

Exits 3 on any mismatch or inversion. The E136/E137 fetch caches live in
/tmp and were written by two sessions; E137 re-fetched GSM into the paths E136
recorded for yi-34b, so a naive read of `/tmp/opencode/e136/gsm__scenario_state.json`
silently reads the other model's rows. This script is what stops that.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))

E136 = "/tmp/opencode/e136"
E137 = "/tmp/opencode/e137"

BASE = ("https://storage.googleapis.com/crfm-helm-public/lite/benchmark_output/runs/"
        "v1.0.0/")

# `as` is the local file; `key` is the name the manifest recorded it under. They
# differ for P3: E136 fetched GSM for yi-34b as `gsm__scenario_state.json`, and
# E137 later overwrote that path with yi-6b bytes, so the yi-34b copy carries a
# suffixed local name. P4 has no manifest row at all -- E137 used those bytes for
# a result without recording their provenance -- so P4 is verified by re-fetching
# from the published URL and comparing, which is stronger, not weaker.
CELLS = {
    "P1": {"dir": E136, "glob": "math__math:subject=*__scenario_state.json",
           "manifest": "136-leaderboard-free-text-aggregate", "model": "01-ai/yi-34b"},
    "P2": {"dir": E137, "glob": "math__math:subject=*__scenario_state.json",
           "manifest": "137-leaderboard-cross-model-agreement", "model": "01-ai/yi-6b"},
    "P3": {"dir": E136, "files": [("gsm__scenario_state_yi34b.json",
                                   "gsm__scenario_state.json")],
           "manifest": "136-leaderboard-free-text-aggregate", "model": "01-ai/yi-34b"},
    "P4": {"dir": E137, "files": [("gsm__scenario_state.json", None)],
           "refetch": BASE + "gsm:model=01-ai_yi-6b/scenario_state.json",
           "model": "01-ai/yi-6b"},
}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _compare_with_published(cell, path, digest, url):
    """P4 has no manifest row. Re-fetch the published bytes and compare.

    A network failure is reported as unverified rather than as a pass: the
    experiment's gates assume every cell was checked, so a silent skip would
    make the whole run look cleaner than it is.
    """
    import urllib.request

    try:
        with urllib.request.urlopen(url, timeout=120) as resp:
            fresh = hashlib.sha256(resp.read()).hexdigest()
    except Exception as exc:                                    # noqa: BLE001
        print("PROBLEM: %s: could not re-fetch %s (%s)" % (cell, url, exc))
        return False
    if fresh != digest[0]:
        print("PROBLEM: %s: %s on disk is %s, published bytes are %s"
              % (cell, path, digest[0][:12], fresh[:12]))
        return False
    print("  %s re-fetched from the published URL: sha256 matches" % cell)
    return True


def main():
    import glob

    problems = []
    report = {"cells": {}, "note": "sha256 and byte length against the manifest recorded at fetch time"}

    for cell, spec in sorted(CELLS.items()):
        recorded = {}
        if "manifest" in spec:
            mpath = os.path.join(REPO, "EXPERIMENTS", spec["manifest"],
                                 "fetched-manifest.json")
            if not os.path.exists(mpath):
                problems.append("%s: manifest missing at %s" % (cell, mpath))
                continue
            for e in json.load(open(mpath)):
                # Some manifest rows record a `status` instead of a digest
                # (requests that did not return the bytes). Those are not
                # verifiable and are not populations.
                if "sha256" in e:
                    recorded[e["file"]] = (e["sha256"], e["bytes"])

        if "files" in spec:
            items = list(spec["files"])
        else:
            items = [(n, n) for n in sorted(
                os.path.basename(p)
                for p in glob.glob(os.path.join(spec["dir"], spec["glob"])))]

        rows = 0
        verified = 0
        checked = 0
        for local, key in items:
            path = os.path.join(spec["dir"], local)
            if not os.path.exists(path):
                problems.append("%s: absent %s" % (cell, path))
                continue
            digest = (sha256(path), os.path.getsize(path))
            if "refetch" in spec:
                if not _compare_with_published(cell, path, digest, spec["refetch"]):
                    continue
            else:
                want = recorded.get(key)
                if want is None:
                    problems.append("%s: %s is not in the manifest" % (cell, local))
                    continue
                if digest != want:
                    problems.append("%s: %s does not match the manifest (%d bytes "
                                    "on disk, %d recorded)"
                                    % (cell, local, digest[1], want[1]))
                    continue
            verified += 1
            checked += 1
            state = json.load(open(path))
            model = state.get("adapter_spec", {}).get("model")
            if model != spec["model"]:
                problems.append("%s: %s carries model %r, cell declares %r"
                                % (cell, local, model, spec["model"]))
            rows += len(state.get("request_states", []))
        report["cells"][cell] = {"files": len(items), "verified": verified,
                                 "rows": rows, "model": spec["model"]}
        print("%s  %-11s files %2d verified %2d  rows %4d"
              % (cell, spec["model"], len(items), verified, rows))

    report["ok"] = not problems
    report["problems"] = problems
    with open(os.path.join(HERE, "population_verification.json"), "w") as fh:
        json.dump(report, fh, indent=1, sort_keys=True)
        fh.write("\n")

    if problems:
        for p in problems:
            print("PROBLEM: %s" % p)
        print("population verification: FAIL")
        return 3
    print("population verification: OK (4 cells)")
    return 0


if __name__ == "__main__":
    sys.exit(main())