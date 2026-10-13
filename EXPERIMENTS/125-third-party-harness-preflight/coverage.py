"""E125 step 5 -- how much of a harness's committed data can a generic reader
open at all, and does any of it carry model output?

`probe.py` selects candidate files by *name*, and the population of data files is
large: 3,341 across the 22 repositories. Selecting by name is a convention, and
a harness that writes its outputs to `records.jsonl` is invisible to it. This
step samples the **whole** data-file population instead, on one declared
mechanical rule applied identically to all 22 repositories:

    sort paths; let k = ceil(n / 120); take every k-th, at most 120 per repository

and it records, per file, whether `load_rows` can open it and which side of a
key/output pair its *fields* say it is. The answer decides what the zero in
`pairs.json` is: files the reader cannot open (a format limit), or files with no
output side at all (an absence).
"""

import json
import math
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from probe import (DATA_EXT, MAX_BYTES, blob, classify, listing,  # noqa: E402
                   load_rows)

PER_REPO = 120

REASONS = ("unsupported format", "git-lfs pointer", "top-level object",
           "not a list of flat records", "jsonl line does not parse", "empty file",
           "not utf-8", "fewer than two rows", "csv parse failed", "tsv parse failed",
           "blob unavailable")


def reason_of(why):
    for r in REASONS:
        if r in why:
            return r
    return why


def main():
    with open(os.path.join(HERE, "trees.json")) as fh:
        trees = json.load(fh)

    total_files = 0
    sampled = 0
    readable = 0
    reasons = Counter()
    sides = Counter()
    per_repo = []
    field_freq = Counter()
    outputish_paths = []

    for repo in trees["repositories"]:
        slug = repo["full_name"].replace("/", "__")
        entry = {"full_name": repo["full_name"], "commit": repo.get("commit"),
                 "data_files": 0, "sampled": 0, "readable": 0, "sides": Counter(),
                 "reasons": Counter()}
        if not repo.get("commit"):
            per_repo.append(entry)
            continue
        files = listing(slug)
        data = sorted(p for s, p in files if DATA_EXT.search(p) and 0 < s < MAX_BYTES)
        entry["data_files"] = len(data)
        total_files += len(data)
        k = max(1, int(math.ceil(len(data) / float(PER_REPO))))
        take = data[::k][:PER_REPO]
        entry["step"] = k
        entry["sampled"] = len(take)
        sampled += len(take)
        for path in take:
            raw = blob(repo["full_name"], repo["commit"], path)
            rows, how = load_rows(raw, path)
            if rows is None or len(rows) < 2:
                r = reason_of(how)
                reasons[r] += 1
                entry["reasons"][r] += 1
                continue
            readable += 1
            entry["readable"] += 1
            rec = classify(rows)
            sides[rec["side"]] += 1
            entry["sides"][rec["side"]] += 1
            for f in list(rec["id_fields"]) + list(rec["key_fields"]) + list(rec["output_fields"]):
                field_freq[f] += 1
            if rec["output_fields"]:
                outputish_paths.append({"full_name": repo["full_name"], "path": path,
                                         "n": rec["n"], "output_fields": rec["output_fields"],
                                         "key_fields": rec["key_fields"]})
        per_repo.append({kk: (dict(vv) if isinstance(vv, Counter) else vv)
                         for kk, vv in entry.items()})
        print("%-38s data %4d step %3d sampled %3d readable %3d  %s"
              % (repo["full_name"], entry["data_files"], k, entry["sampled"],
                 entry["readable"], dict(entry["sides"])))

    out = {"experiment": "E125", "rule": "every k-th of the sorted data-file listing, k=ceil(n/%d)" % PER_REPO,
           "totals": {"data_files_in_population": total_files, "sampled": sampled,
                      "readable_by_generic_loader": readable,
                      "readable_fraction": round(float(readable) / sampled, 4) if sampled else 0.0},
           "sides": dict(sides), "unreadable_reasons": dict(reasons),
           "field_frequencies": dict(field_freq.most_common(60)),
           "files_with_output_shaped_fields": outputish_paths,
           "per_repository": per_repo}
    with open(os.path.join(HERE, "coverage.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)

    print("\npopulation %d data files, sampled %d, readable %d (%.4f)"
          % (total_files, sampled, readable, out["totals"]["readable_fraction"]))
    print("sides: %s" % dict(sides))
    print("unreadable reasons: %s" % dict(reasons.most_common()))
    print("files carrying output-shaped fields: %d" % len(outputish_paths))


if __name__ == "__main__":
    sys.exit(main())