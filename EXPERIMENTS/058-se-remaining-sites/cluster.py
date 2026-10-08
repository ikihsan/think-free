"""E058 cluster: find vocabularies that recur across distinct requesters.

The first linkage (greedy average-link over title token sets) returned zero clusters
at every threshold, and diagnose.py showed why: on 6-token titles only 3143 of 19900
pairs share any token at all, and the true same-step pairs sit at J=0.40-0.62, so no
pairwise rule can assemble eight titles out of that sparse graph. Pairwise linkage is
discarded; it is kept in diagnose.py as the instrument's face-validity evidence.

Declared instrument, in full:

  unit        one question title; lowercased; HTML entities resolved; tokens of
              >=3 chars, not stopwords, not digits; single-suffix stripping only
  concepts    connected components of the token co-occurrence graph, where two tokens
              are linked when they co-occur in >= EDGE titles and both have df >= MINDF
  membership  a title belongs to a concept when it contains >= HIT tokens of it
  reporting   a concept is reported when >= MINUSERS distinct requesters meet MINROWS
              titles
  sweep       EDGE in {2,3,4,6} x MINUSERS in {5,8}, printed, so every G1 pass can be
              read as a function of the parameter instead of at one lucky setting
"""
import json
import os
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

STOP = set("""
a an the is are was were be been being am do does did doing done have has had having
i my me mine we our ours you your yours he him his she her hers it its they them their
this that these those there here what which who whom whose when where why how
can could would should will shall may might must not no nor so than then too very just
also as of at by for from in into on onto with without and or but if because while
during about over under again further once more most other some such own same only
best good better great way ways get getting got make making made use using used
new old any all one two three four five good bad better worse
question answer answers problem problems issue issues help need
please thanks thank hi hello guys people anyone someone everybody
know like want looking looking for something anything
difference between same different vs versus compared
work works working worked fine
possible reason cause
""".split())

SUFFIX = ("ings", "ing", "ies", "ied", "ers", "er", "ed", "es", "s")


def stem(w):
    if len(w) <= 4:
        return w
    for suf in SUFFIX:
        if w.endswith(suf) and len(w) - len(suf) >= 4:
            base = w[: len(w) - len(suf)]
            if suf == "ies":
                return base + "y"
            return base
    return w


def toks(title):
    t = title.lower().replace("&amp;", " and ").replace("&quot;", " ")
    out = []
    for w in "".join(c if c.isalnum() or c.isspace() else " " for c in t).split():
        if len(w) < 3 or w in STOP or w.isdigit():
            continue
        out.append(stem(w))
    return out


def components(tokens, df, edge, mindf):
    """Token co-occurrence graph -> connected components."""
    parent = {}

    def find(x):
        while parent.setdefault(x, x) != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    keep = set(t for t, c in df.items() if c >= mindf)
    for t in keep:
        find(t)
    co = Counter()
    for tset in tokens:
        present = sorted(set(tset) & keep)
        for i, a in enumerate(present):
            for b in present[i + 1:]:
                co[(a, b)] += 1
    linked = 0
    for (a, b), n in co.items():
        if n >= edge:
            union(a, b)
            linked += 1
    groups = defaultdict(set)
    for t in list(parent):
        groups[find(t)].add(t)
    return list(groups.values()), linked, len(parent)


def score(rows, tokens, group, hit=2):
    sel = [i for i, ts in enumerate(tokens) if len(set(ts) & group) >= hit]
    if not sel:
        return None
    ids = set(rows[i].get("owner", {}).get("user_id")
              for i in sel if rows[i].get("owner"))
    return {"rows": len(sel), "users": len(ids),
            "titles": [rows[i]["title"] for i in sel[:8]]}


def one_site(name, rows, edge, mindf, hit):
    tokens = [toks(r["title"]) for r in rows]
    df = Counter()
    for ts in tokens:
        for t in set(ts):
            df[t] += 1
    groups, linked, ntok = components(tokens, df, edge, mindf)
    out = []
    for g in groups:
        s = score(rows, tokens, g, hit)
        if s:
            s.update(site=name, terms=sorted(g, key=lambda t: -df[t])[:14])
            out.append(s)
    return out, {"tokens": ntok, "edges_linked": linked, "components": len(groups)}


def main():
    idx = json.load(open(os.path.join(RAW, "index.json")))
    byfile = defaultdict(list)
    for s in idx["sites"]:
        byfile[s["arm"]].append((s["name"], json.load(open(os.path.join(RAW, s["file"])))))

    sweep = {}
    for edge in (2, 3, 4, 6):
        for minusers in (5, 8):
            per = {}
            for arm in ("tail", "head"):
                tot = 0
                for name, rows in byfile[arm]:
                    cl, meta = one_site(name, rows, edge, 8, 2)
                    tot += sum(1 for c in cl if c["users"] >= minusers)
                per[arm] = tot
            sweep["edge=%d,minusers=%d" % (edge, minusers)] = per
    print(json.dumps(sweep, indent=1))

    EDGE, MINDF, HIT, MINUSERS = 4, 8, 2, 8
    out = {"params": {"edge": EDGE, "mindf": MINDF, "hit": HIT, "minusers": MINUSERS},
           "sweep": sweep, "arms": {}, "meta": {}}
    for arm in ("tail", "head"):
        allc = []
        for name, rows in byfile[arm]:
            cl, meta = one_site(name, rows, EDGE, MINDF, HIT)
            out["meta"][name] = meta
            allc.extend(c for c in cl if c["users"] >= MINUSERS)
        allc.sort(key=lambda c: -c["users"])
        out["arms"][arm] = allc
    with open(os.path.join(RAW, "clusters.json"), "w") as fh:
        json.dump(out, fh, indent=1)

    for arm in ("tail", "head"):
        cl = out["arms"][arm]
        print("\n=== %s: %d concepts with >=%d distinct requesters ===" % (arm, len(cl), MINUSERS))
        for c in cl[:45]:
            print("%3d u %3d r  %-26s %s" % (c["users"], c["rows"], c["site"][:26],
                                              " ".join(c["terms"][:9])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
