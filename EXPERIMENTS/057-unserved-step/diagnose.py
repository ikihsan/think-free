"""E057 instrument diagnostics: why did the clustering return nothing?

Reports, on real rows only: token survival, the stemmer's actual output on the words
that matter, and the distribution of nearest-neighbour Jaccard. A clustering that
returns zero clusters is either too strict or broken; this says which.
"""
import itertools
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cluster as C  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")


def main():
    print("stemmer spot-check:")
    for w in ("printing", "printed", "prints", "levels", "leveling", "leveled",
              "leaking", "leaked", "leaks", "adhesion", "adhering", "brim", "skirt"):
        print("   %-10s -> %s" % (w, C.stem(w)))

    idx = json.load(open(os.path.join(RAW, "index.json")))
    site = next(s for s in idx["sites"] if s["arm"] == "tail")
    rows = json.load(open(os.path.join(RAW, site["file"])))
    print("\n%s (%s) %d rows" % (site["name"], site["arm"], len(rows)))
    lens = [len(C.toks(r["title"])) for r in rows]
    print("token count per title: empty=%d  mean=%.1f  median=%d"
          % (sum(1 for l in lens if l == 0), sum(lens) / float(len(lens)),
             sorted(lens)[len(lens) // 2]))

    df = Counter()
    for r in rows:
        for t in C.toks(r["title"]):
            df[t] += 1
    print("distinct tokens=%d  tokens with df>=8: %d" % (len(df), sum(1 for c in df.values() if c >= 8)))
    print("top 30 df:", ", ".join("%s:%d" % (t, c) for t, c in df.most_common(30)))

    sets = [C.toks(r["title"]) for r in rows]
    best = []
    for i, j in itertools.combinations(range(len(rows)), 2):
        if sets[i] and sets[j]:
            v = C.jac(sets[i], sets[j])
            if v > 0:
                best.append((v, i, j))
    best.sort(reverse=True)
    print("\nnonzero title pairs: %d of %d" % (len(best), len(rows) * (len(rows) - 1) // 2))
    print("top 12 nearest pairs:")
    for v, i, j in best[:12]:
        print("  %.2f  %-58s ||  %s" % (v, rows[i]["title"][:58], rows[j]["title"][:58]))

    # how many distinct-user sets of size>=8 exist at all, ignoring coherence?
    print("\nhow many titles share the single most common token with >=8 distinct users?")
    for t, c in df.most_common(8):
        ids = set(r.get("owner", {}).get("user_id") for r in rows
                  if t in C.toks(r["title"]) and r.get("owner"))
        print("   %-12s rows=%3d distinct_users=%3d" % (t, c, len(ids)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
