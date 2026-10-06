#!/usr/bin/env python3
"""Calibrate the subtree reconstruction against the Firebase item API.

E039 protocol: where the Algolia row and the Firebase item disagree, the
disagreement is recorded rather than resolved in Algolia's favour by default.

Writes calibration.json. Run before the capture, on a declared sample.
"""
import json, os, random, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "think-free-research"}
ALGOLIA = "https://hn.algolia.com/api/v1/items/%s"
FIREBASE = "https://hacker-news.firebaseio.com/v0/item/%s.json"


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return json.load(r)


def algolia_subtree(item_id):
    """Size and depth of the comment subtree the Algolia items endpoint returns."""
    d = get(ALGOLIA % item_id)
    subtree = d.get("children") or []

    def walk(nodes, level=1):
        n = 0
        top = level
        for c in nodes:
            n += 1
            sub = walk(c.get("children") or [], level + 1)
            n += sub[0]
            top = max(top, sub[1])
        return n, top

    size, height = walk(subtree)
    return {"root": item_id, "children": len(subtree), "size": size, "depth": height}


def firebase_descendants(item_id):
    """Full descendant count by walking Firebase item-by-item."""
    seen = set()
    stack = [item_id]
    total = 0
    while stack:
        i = stack.pop()
        if i in seen:
            continue
        seen.add(i)
        try:
            it = get(FIREBASE % i)
        except Exception:
            continue
        if not it:
            continue
        for k in (it.get("kids") or []):
            total += 1
            stack.append(k)
        time.sleep(0.05)
    return total


def main():
    corpus = os.path.join(HERE, "..", "012-candidate-harvest", "raw",
                          "hn_needs_2026-10-04.jsonl")
    rows = [json.loads(l) for l in open(corpus)]
    # Declared sample: a fixed seed, 12 rows, so the calibration population is
    # reproducible and not chosen after seeing agreement.
    sample = random.Random(21).sample(rows, 12)

    out = {"sample_size": len(sample), "seed": 21, "rows": [], "agreement": {}}
    agree = disagree = unreachable = 0
    for r in sample:
        a = algolia_subtree(r["id"])
        time.sleep(0.3)
        f = firebase_descendants(r["id"])
        same = (a["size"] == f)
        if same:
            agree += 1
        else:
            disagree += 1
        out["rows"].append({
            "id": r["id"], "created": r["created"],
            "algolia_children": a["children"], "algolia_subtree_size": a["size"],
            "algolia_depth": a["depth"], "firebase_descendants": f,
            "agree": same,
        })
        print(r["id"], "algolia=%d" % a["size"], "firebase=%d" % f, "agree" if same else "DISAGREE")

    out["agreement"] = {"agree": agree, "disagree": disagree}
    # The capture will use Algolia for both arms, so the figure that decides
    # whether it may is not per-row agreement but whether disagreement could
    # systematically favour one arm. A disagreement is only tolerable if it
    # cannot move a need comment across the reply-rate threshold.
    out["max_disagreement"] = max(
        [abs(r["algolia_subtree_size"] - r["firebase_descendants"]) for r in out["rows"]] or [0])
    with open(os.path.join(HERE, "calibration.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print("agree=%d disagree=%d max_gap=%d" % (agree, disagree, out["max_disagreement"]))


if __name__ == "__main__":
    main()