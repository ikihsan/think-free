"""E035 -- the free reads. PROTOCOL.md section 3's R1-R4, computed over E034's committed
bytes. No fetch, no new rows.

Per D061 every result is tied to the sha256 of the bytes it was read from; `digest()`
prints them and `tally.py` refuses to print a verdict if they do not match what README.md
declares. Nothing here decides a gate -- these results are what section 3 declares, and a
reader can rerun them against the same three files.
"""

import collections
import hashlib
import json
import math
import os
import statistics

HERE = os.path.dirname(os.path.abspath(__file__))
E034_RAW = os.path.normpath(os.path.join(HERE, "..", "034-reask-tail", "raw"))

# PROTOCOL.md section 4: the same eight tags E034 declared, so U is comparable to it.
TAGS = [
    ("stackoverflow", "git"), ("stackoverflow", "regex"),
    ("stackoverflow", "python"), ("stackoverflow", "docker"),
    ("stackoverflow", "excel-formula"), ("travel", "customs"),
    ("math", "linear-algebra"), ("math", "probability"),
]
SOURCES = ("harvest.jsonl", "r1.jsonl", "r2.jsonl")

# D063: closed_reason is ten literals and two of them spell the same thing. E034 recorded
# this after the fact; a reader of this file must not have to rediscover it.
DUPLICATE_LITERALS = ("duplicate", "exact duplicate")


def is_duplicate(row):
    return (row.get("closed_reason") or "").strip().lower() in DUPLICATE_LITERALS


def digest():
    """sha256 of each input file, so a result can be tied to the bytes behind it."""
    out = {}
    for name in SOURCES:
        path = os.path.join(E034_RAW, name)
        with open(path, "rb") as fh:
            out[name] = hashlib.sha256(fh.read()).hexdigest()
    return out


def load_e034():
    rows = []
    for name in SOURCES:
        with open(os.path.join(E034_RAW, name)) as fh:
            for line in fh:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
    return rows


def tail_ids(rows):
    """E034's tail population as an id set per tag, across every arm file that holds one."""
    ids = collections.defaultdict(set)
    for r in rows:
        if r.get("arm") == "tail":
            ids[(r["site"], r["tag"])].add(r["question_id"])
    return ids


def r1_disjointness(rows):
    """R1: do the Active and tail arms contain the same questions? Compared by score band,
    because ids cannot overlap -- the two arms are different routes' orderings of one tag."""
    out = []
    for site, tag in TAGS:
        arms = {}
        for arm in ("tail", "default"):
            sc = [r["score"] for r in rows
                  if r.get("arm") == arm and r["site"] == site and r["tag"] == tag]
            if sc:
                arms[arm] = (min(sc), max(sc))
        if len(arms) != 2:
            out.append((site, tag, None))
            continue
        (tl, th), (dl, dh) = arms["tail"], arms["default"]
        lo, hi = max(tl, dl), min(th, dh)
        out.append((site, tag, None if lo > hi else (lo, hi)))
    return out


def r2_seen(rows):
    """R2: within the tail arm, are duplicate rows viewed more or less than their
    neighbours, and how old is the population? If the duplicates were being overlooked
    this is where it would show."""
    newest = max(r.get("creation_date") or 0 for r in rows)
    out = {}
    for arm in ("tail", "head", "default"):
        sub = [r for r in rows if r.get("arm") == arm]
        views = [r["view_count"] for r in sub if r.get("view_count") is not None]
        ages = [(newest - r["creation_date"]) / 86400.0 / 365.25
                for r in sub if r.get("creation_date")]
        out[arm] = {"n": len(sub),
                    "views_median": statistics.median(views) if views else None,
                    "age_median_yr": round(statistics.median(ages), 2) if ages else None}
    tail = [r for r in rows if r.get("arm") == "tail"]
    for lbl, sub in (("duplicate", [r for r in tail if is_duplicate(r)]),
                     ("not_duplicate", [r for r in tail if not is_duplicate(r)])):
        views = [r["view_count"] for r in sub if r.get("view_count") is not None]
        ages = [(newest - r["creation_date"]) / 86400.0 / 365.25
                for r in sub if r.get("creation_date")]
        out["tail_" + lbl] = {"n": len(sub),
                              "views_median": statistics.median(views) if views else None,
                              "views_mean": round(statistics.mean(views), 1) if views else None,
                              "age_median_yr": round(statistics.median(ages), 2) if ages else None}
    return out


def per_tag_tail(rows):
    cells = collections.defaultdict(lambda: [0, 0])
    for r in rows:
        if r.get("arm") == "tail":
            c = cells[(r["site"], r["tag"])]
            c[0] += 1
            c[1] += 1 if is_duplicate(r) else 0
    return cells


def r3_variance(rows):
    """R3: between-tag excess variance on the arcsine scale -- observed spread minus what
    binomial sampling alone produces at these n. Positive means the spread is real.

    Tags with n < 50 are excluded by E034's own A4 convention. One eligible cell reads
    exactly 0 (excel-formula); arcsin(sqrt(0)) = 0 is defined, which logit would not be,
    so the arcsine transform is what makes the zero cell usable rather than dropped.
    """
    cells = {k: v for k, v in per_tag_tail(rows).items() if v[0] >= 50}

    def excess(subset):
        vals = [(math.asin(math.sqrt(d / float(n))), 1.0 / (4.0 * n)) for n, d in subset]
        if len(vals) < 2:
            return None
        mean = sum(v[0] for v in vals) / len(vals)
        obs = sum((v[0] - mean) ** 2 for v in vals) / (len(vals) - 1)
        exp = sum(v[1] for v in vals) / (len(vals) - 1)
        return round(obs - exp, 4)

    by_site = collections.defaultdict(list)
    for (site, _tag), v in cells.items():
        by_site[site].append(v)
    return {"pooled": excess(list(cells.values())),
            "by_site": {s: {"tags": len(v), "excess": excess(v)}
                        for s, v in sorted(by_site.items())},
            "eligible": {"%s/%s" % k: v for k, v in sorted(cells.items())}}


def r4_score_predicts_rate(rows):
    """R4: does a tag's tail arm sit at a different score depth from its neighbours, and
    does that depth predict its rate? This is the objection to using a rank-selected tail
    across tags with different score distributions."""
    cells = per_tag_tail(rows)
    pts = [(sum(r["score"] for r in rows
                if r.get("arm") == "tail" and (r["site"], r["tag"]) == k) / float(n),
            d / float(n))
           for k, (n, d) in cells.items()]
    n = len(pts)
    mx = sum(p[0] for p in pts) / n
    my = sum(p[1] for p in pts) / n
    num = sum((x - mx) * (y - my) for x, y in pts)
    den = math.sqrt(sum((x - mx) ** 2 for x, _ in pts) * sum((y - my) ** 2 for _, y in pts))
    r = num / den if den else 0.0
    t = r * math.sqrt((n - 2) / max(1e-12, 1 - r * r))
    return {"tags": n, "pearson_r": round(r, 4), "t": round(t, 3), "df": n - 2,
            "established": abs(t) > 2.306}


def run():
    rows = load_e034()
    return {"input_sha256": digest(), "rows_read": len(rows),
            "R1_active_vs_tail_score_band": r1_disjointness(rows),
            "R2_seen": r2_seen(rows), "R3_variance": r3_variance(rows),
            "R4_score_predicts_rate": r4_score_predicts_rate(rows)}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True, default=str))
