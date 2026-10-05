#!/usr/bin/env python3
"""Join 016's artifact type to 015's serving figures, per arm.

The floors and the three-way answer (served / not served / undecided) are imported
from 015 rather than restated. A second copy of "clears a declared floor" in this
repository is how a comparison ends up measuring two different definitions, and
015's own `INSTRUMENT_CORRECTION` is the record of that having already happened
once.

What is added here is the cross-tabulation and nothing else: `by_arm_and_class`
answers "of the rows a prior-art screen consulted in a young vocabulary, how many
were prose, and do the prose rows clear a serving floor at the rate the code rows
do".

    python3 servingjoin.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PREV = os.path.join(os.path.dirname(HERE), "015-incumbent-serving")
for path in (PREV, HERE):
    if path not in sys.path:
        sys.path.insert(0, path)

import rootlisting            # noqa: E402
import verdict as floors      # noqa: E402

ARMS = ("mature", "young", "placebo")
CLASSES = ("executable", "document", "unreadable")


def previous_serving():
    """Every row 015 measured, keyed by repository, with its arm."""
    with open(os.path.join(PREV, "results.json")) as fh:
        prev = json.load(fh)
    out = {}
    for key, arm in (("incumbents", "mature"), ("cluster", "young"),
                     ("placebo", "placebo")):
        for r in prev[key]:
            out[r["repo"]] = (arm, r)
    for r in (prev.get("placebo_control") or {}).get("controls", []):
        out[r["repo"]] = ("placebo", r)
    return out, prev


def joined_rows(classifications=None):
    cache = None
    cache_path = os.path.join(HERE, "raw", "rootlistings.json")
    if os.path.exists(cache_path):
        with open(cache_path) as fh:
            cache = json.load(fh)
    classes = classifications if classifications is not None \
        else {n: classification_class(cache, n) for n in cache}
    measured, _ = previous_serving()
    rows = []
    for row in rootlisting.population():
        name = row["repo"]
        info = classes.get(name) or {"class": "unreadable",
                                     "reason": "not_fetched", "hits": []}
        arm, prev = measured.get(name, (None, {}))
        rate, cumulative, undecided = floors.classify(prev) if prev else (0, 0, True)
        rows.append({
            "repo": name, "arm": row["arm"], "group": row["group"],
            "need": row["need"], "stars": row["stars"],
            "class": info["class"], "class_reason": info.get("reason"),
            "hits": info.get("hits", []),
            "releases": info.get("releases"),
            "root_size": info.get("root_size"),
            "measured_by_015": prev is not None,
            "served": floors.served(prev) if prev else None,
            "best_rate": rate, "best_cumulative": cumulative,
            "undecided": undecided,
        })
    return rows


def classification_class(cache, name):
    entry = cache.get(name) if isinstance(cache, dict) else None
    from classification import classify
    return classify(entry)


def cross(rows, arm=None):
    """class -> {n, decided, served, served_share}, for one arm or all."""
    out = {c: {"n": 0, "decided": 0, "served": 0, "served_share": None,
               "served_repos": [], "stars_median": None} for c in CLASSES}
    buckets = {c: [] for c in CLASSES}
    for r in rows:
        if arm and r["arm"] != arm:
            continue
        if r["class"] in buckets:
            buckets[r["class"]].append(r)
    for cls, group in buckets.items():
        decided = [r for r in group if not r["undecided"]]
        hits = [r for r in decided if r["served"]]
        stars = sorted(r["stars"] for r in group)
        out[cls]["n"] = len(group)
        out[cls]["decided"] = len(decided)
        out[cls]["served"] = len(hits)
        out[cls]["served_share"] = (len(hits) / float(len(decided))) if decided else None
        out[cls]["served_repos"] = sorted(r["repo"] for r in hits)
        out[cls]["stars_median"] = stars[len(stars) // 2] if stars else None
        out[cls]["repos"] = sorted(r["repo"] for r in group)
    return out


def by_arm_and_class(rows):
    return {arm: cross(rows, arm) for arm in ARMS}


if __name__ == "__main__":
    rows = joined_rows()
    print(json.dumps({"rows": len(rows),
                      "unfetched": sum(1 for r in rows if r["class"] == "unreadable"
                                       and r["class_reason"] == "not_fetched"),
                      "arms": by_arm_and_class(rows)},
                     indent=1, sort_keys=True))