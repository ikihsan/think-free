#!/usr/bin/env python3
"""E041 scaling: clustering primitives, split from the curve at the 300-line cap.

**Split by invariant.** This file holds *how clusters are formed* — the edge list,
single-link components, and the subsample draw. `scaling.py` holds *what the curve
means* — the growth exponent, the gates, and the readout. A threshold and the
statistic it licenses must not be editable in the same place, which is the reason
`EXPERIMENTS/040-need-clustering/` split its own `gates.py` from `tally.py` and the
reason `DECISIONS-SCREENING-9.md` D069 exists.

`PROTOCOL-scaling.md` fixes the question and the grid; `AMENDMENT-3` fixes three
provisions, and two of them live here:

- **The edge list is exact, not approximate.** Single-link clustering at `tau` is the
  connected components of the graph whose edges are the pairs at or above `tau`, so
  holding every pair at or above the grid's minimum and union-finding upward gives the
  same components a fresh O(n^2) pass would. `scaling.py` asserts that equivalence at
  full size against E040's own dense `cluster_stats` before it reports anything.
- **`subsample_indices` returns row positions, not row ids.** An earlier version
  returned ids, which are strings, and every downstream lookup then missed the corpus
  and contributed no edges: the result was a clean, plausible, entirely fictional
  curve of **0.00 across all nine sizes and both arms**. The guard now in `scaling.py`
  asserts the full-size draw is the whole arm, so that failure cannot recur silently.

The instrument is E040's, imported rather than reimplemented. E040's own
`tally.py` is loaded **by path** rather than by name, because this directory also has
a `tally.py` in some earlier revisions and a bare `from tally import ...` would resolve
to whichever came first on `sys.path`.
"""
import array
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
E040DIR = os.path.join(os.path.dirname(HERE), "040-need-clustering")
sys.path.insert(0, E040DIR)

import importlib.util                            # noqa: E402
_spec = importlib.util.spec_from_file_location(
    "e040_tally", os.path.join(E040DIR, "tally.py"))
_e040 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_e040)
cluster_stats = _e040.cluster_stats

# PROTOCOL-scaling.md, "Fixed before computation".
N_GRID = [100, 175, 275, 400, 550, 750, 1000, 1250, 1391]
RESAMPLES = 40
SEED = 20261006
BOOT = 4000
ARMS = ("A", "B")
QUALIFY = 3     # >=3 rows, >=3 distinct stories, >=3 distinct authors
BOOTSTRAP = 4000


def tk(t):
    """One key format for every tau everywhere.

    `str(0.2)` is '0.2' and `str(0.15)` is '0.15', so a lookup keyed on '0.20'
    raises KeyError while the same tau is present under another name -- a
    dictionary that looks complete and is not.
    """
    return "%.2f" % t


# E040's own arm-A figures. AMENDMENT-5: these are the values in E040's
# `raw/tally.json`, its run's own record, NOT the values in its README prose -- the
# prose says "0 at every threshold from 0.20 up" and the artifact says 1 at 0.20 and
# 1 at 0.25. The artifact is the record; the sentence was stale.
E040_PUBLISHED = {"0.15": 8, "0.20": 1, "0.25": 1,
                  "0.30": 0, "0.35": 0, "0.40": 0, "0.45": 0, "0.50": 0}
E040_PUBLISHED_SRC = "EXPERIMENTS/040-need-clustering/raw/tally.json gates.G4"


def percentile(sorted_vals, q):
    k = max(0, min(len(sorted_vals) - 1, int(q * len(sorted_vals))))
    return sorted_vals[k]


def load_arm(arm):
    path = os.path.join(E040DIR, "raw", "arm_%s.jsonl" % arm)
    rows = [json.loads(l) for l in open(path)]
    return rows, [r["text"] for r in rows]


def edge_list(vecs, keep_at):
    """Every pair at or above `keep_at`, once, as two flat int arrays and a float.

    Inverted-index accumulation, so only pairs sharing a term are touched; a dense
    O(n^2) pass over short technical text in pure Python is what this avoids.
    AMENDMENT-3 provision 3 asserts the resulting components match E040's dense
    pass exactly, at full size, before the curve is reported.
    """
    n = len(vecs)
    post = {}
    for i, v in enumerate(vecs):
        for term, w in v.items():
            post.setdefault(term, []).append((i, w))
    seen = set()
    src, dst, val = array.array("i"), array.array("i"), array.array("f")
    for i in range(n):
        acc = {}
        vi = vecs[i]
        for term, w in vi.items():
            for j, wj in post[term]:
                if j > i:
                    acc[j] = acc.get(j, 0.0) + w * wj
        for j, s in acc.items():
            if s >= keep_at:
                key = (i, j)
                if key in seen:
                    continue
                seen.add(key)
                src.append(i)
                dst.append(j)
                val.append(s)
    return src, dst, val


def components(rows, members, src, dst, val, tau):
    """Single-link components over edges at or above `tau`, restricted to `members`.

    Returns the qualifying clusters only, in E040's own terms: size, distinct
    stories, distinct authors.
    """
    inside = set(members)
    parent = {i: i for i in members}

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    for e in range(len(src)):
        if val[e] < tau:
            continue
        a, b = src[e], dst[e]
        if a not in inside or b not in inside:
            continue
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    groups = {}
    for i in members:
        groups.setdefault(find(i), []).append(i)
    out = []
    for mem in groups.values():
        if len(mem) < QUALIFY:
            continue
        stories = len(set(rows[m]["story_id"] for m in mem))
        authors = len(set(rows[m]["author"] for m in mem))
        if stories >= QUALIFY and authors >= QUALIFY:
            out.append({"size": len(mem), "stories": stories, "authors": authors})
    return out


def subsample_indices(ids, n, seed=SEED, rep=0):
    """Deterministic draw without replacement by a fixed hash of the row id.

    Reproducible, and a given (n, rep) does not depend on any earlier draw, so
    adding a grid point reproduces the old points exactly.

    Returns **row positions**, hashed by id. Returning the ids themselves -- which
    are strings -- made every downstream lookup miss the corpus and contribute no
    edges, so every count came back 0.00 and looked like a result.
    """
    keyed = []
    for pos, row_id in enumerate(ids):
        h = seed
        for ch in str(row_id):
            h = (h * 131 + ord(ch)) % 2147483647
        keyed.append((h, rep, pos))
    keyed.sort()
    return [pos for _, _, pos in keyed[:n]]
