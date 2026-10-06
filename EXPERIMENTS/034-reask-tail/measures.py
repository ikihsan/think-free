"""E034 — the measurements, split out of tally.py at the 300-line cap: descriptive
statistics and the response-channel record, with no gate attached. `tally.py` is the gate
table and the printer. Nothing here decides a verdict; everything here is recomputed from
the committed bytes so that `tally.py --check` can disagree with what is recorded.

The label is Stack Exchange's `closed_reason`; the arms are the route's own ordering; the
population was declared in PROTOCOL.md before the first fetch.
"""

"""E034 — the gate table. PROTOCOL.md section 5, recomputed from the committed bytes.

`tally.py` prints the table and writes raw/tally.json. `tally.py --check` is the
verification command: it re-reads raw/pages.jsonl, re-hashes every response body it
logged, recomputes every rate, and exits non-zero if anything disagrees with what is
recorded, if a declared arm is missing, or if a gate that must hold does not.

No gate here is decided by a number this file produced. The label is Stack Exchange's
`closed_reason`; the arms are the route's own ordering; the population was declared
before the first fetch.
"""

import collections
import hashlib
import json
import math
import os
import sys

import reask

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

# PROTOCOL.md section 4. `Duplicate` is the literal Stack Exchange writes today.
# `exact duplicate` is the legacy spelling of the same moderation act and 9 rows carry
# it; the declared label excludes it, and S1 reports the difference rather than hiding it.
DUPLICATE = "Duplicate"
DUPLICATE_SET = ("Duplicate", "exact duplicate")

CHANNELS = [                                    # PROTOCOL.md section 2, D5
    ("question page, browser UA", "403 Cloudflare challenge", "travel.stackexchange.com/questions/189910"),
    ("stackoverflow.com, browser UA", "403 Cloudflare challenge", "stackoverflow.com/questions/189910"),
    ("stackprinter.appspot.com x3", "200, 1213 B, server too busy", "export?question=189910"),
    ("stackprinter www x1", "200, 1213 B, server too busy", "www.stackprinter.com/export"),
    ("SEDE query page and a saved query", "403 Cloudflare challenge", "data.stackexchange.com"),
    ("question comments", "200, no system comment naming a canonical", "/questions/{id}/comments"),
    ("answer closed_details", "200, field absent", "/questions/{id}/answers"),
    ("API closed_details filter", "400 invalid filter; not in filters/create", "filters/create"),
    ("four vectorised {ids} routes", "no_method (E033)", "/questions/1644,1011"),
]


def newcombe(k1, n1, k2, n2, z=1.96):
    """CI95 for p1 - p2, so the interval reported is the interval of the difference."""
    if n1 == 0 or n2 == 0:
        return (None, None)
    p1, p2 = k1 / float(n1), k2 / float(n2)
    l1, u1 = reask.wilson(k1, n1, z)
    l2, u2 = reask.wilson(k2, n2, z)
    d = p1 - p2
    lo = d - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2)
    hi = d + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)
    return (max(-1.0, lo), min(1.0, hi))


def arm_stats(rows):
    k = sum(1 for r in rows if r["closed_reason"] == DUPLICATE)
    n = len(rows)
    _k, _n, p, lo, hi = reask._rate(rows)
    scores = [r["score"] for r in rows if r.get("score") is not None]
    return {"n": n, "dup": k, "rate": p, "ci": [lo, hi],
            "score_min": min(scores) if scores else None,
            "score_max": max(scores) if scores else None}


def accepted_share(rows):
    """D4. Of the rows closed as duplicates, how many carry an accepted answer."""
    dups = [r for r in rows if r["closed_reason"] == DUPLICATE]
    k = sum(1 for r in dups if not r.get("accepted_answer_id"))
    n = len(dups)
    lo, hi = reask.wilson(k, n)
    return {"dups": n, "no_accepted_answer": k,
            "share": (k / float(n)) if n else None, "ci": [lo, hi]}


def digest_ok(pages):
    """Every logged sha256 must be the hash of the body committed beside it."""
    bad = []
    for p in pages:
        body = p.get("body")
        if body is None:
            bad.append((p.get("url"), "no body committed"))
            continue
        h = hashlib.sha256(body.encode("utf-8")).hexdigest()
        if h != p["sha256"]:
            bad.append((p.get("url"), h))
    return bad


def build():
    pages = [json.loads(l) for l in open(os.path.join(RAW, "pages.jsonl")) if l.strip()]
    # Only the declared sample, never `reask.load()`: load() returns every sample, and a
    # declared gate that absorbs an amendment sample double-counts the two tags R1
    # re-reads at a later page and quietly reports the replication as the result.
    declared = reask.load_sample("declared")
    assert all(r.get("sample", "declared") == "declared" for r in declared), \
        "the declared population contains an amendment row"
    samples = {}
    overlap = {}
    seen = {(r["site"], r["question_id"]) for r in declared}
    for name in ("r1", "r2"):
        allr = reask.load_sample(name.upper())
        overlap[name] = [r for r in allr if (r["site"], r["question_id"]) in seen]
        samples[name] = [r for r in allr if (r["site"], r["question_id"]) not in seen]

    arms = collections.OrderedDict()
    for tag in reask.DECLARED_TAGS:
        arms[tag] = collections.OrderedDict(
            (arm, [r for r in declared if r["tag"] == tag and r["arm"] == arm])
            for arm in ("tail", "head", "default"))
    per_tag = {t: {a: arm_stats(v) for a, v in av.items()} for t, av in arms.items()}
    pooled = {a: [r for r in declared if r["arm"] == a]
              for a in ("tail", "head", "default")}
    pooled_stats = {a: arm_stats(v) for a, v in pooled.items()}

    # D2 matched-n: each arm truncated to the smallest per-tag arm, so unequal n cannot
    # carry a pooled difference on its own.
    matched = collections.defaultdict(list)
    for tag, av in arms.items():
        n = min(len(v) for v in av.values())
        for a in av:
            matched[a] += av[a][:n]
    matched_stats = {a: arm_stats(v) for a, v in matched.items()}

    # S1: the legacy literal.
    sens = {}
    for a, v in pooled.items():
        k = sum(1 for r in v if r["closed_reason"] in DUPLICATE_SET)
        n = len(v)
        lo, hi = reask.wilson(k, n)
        sens[a] = {"n": n, "dup": k, "rate": k / float(n), "ci": [lo, hi]}

    # A4: disjoint interval pairs, and how many tags clear the n >= 50 floor.
    eligible = {t: per_tag[t]["tail"] for t in per_tag if per_tag[t]["tail"]["n"] >= 50}
    disjoint = []
    names = sorted(eligible)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = eligible[names[i]], eligible[names[j]]
            if a["ci"][1] < b["ci"][0] or b["ci"][1] < a["ci"][0]:
                disjoint.append([names[i], names[j]])

    # D6, AMENDMENT-1 R2's confound test. PROTOCOL.md section 7 declared it as a binary
    # gate and the binary form turned out to be ill-formed — baggage overlaps calculus but
    # is disjoint from probability, so both declared branches could fire. The unambiguous
    # statistic is how often two tags on the *same* site are distinguishable at all: if
    # site drove the rate, within-site pairs would rarely separate and cross-site pairs
    # would almost always.
    site_of = {t[2]: t[1] for t in reask.TAGS}
    r2_eligible = {t: arm_stats([r for r in samples["r2"] if r["tag"] == t])
                   for t in sorted({r["tag"] for r in samples["r2"]})}
    pool_eligible = dict(eligible)
    pool_eligible.update({t: s for t, s in r2_eligible.items() if s["n"] >= 50})
    within = [0, 0]
    cross = [0, 0]
    allnames = sorted(pool_eligible)
    for i in range(len(allnames)):
        for j in range(i + 1, len(allnames)):
            a, b = pool_eligible[allnames[i]], pool_eligible[allnames[j]]
            sep = a["ci"][1] < b["ci"][0] or b["ci"][1] < a["ci"][0]
            same = site_of[allnames[i]] == site_of[allnames[j]]
            tgt = within if same else cross
            tgt[0] += int(sep)
            tgt[1] += 1
    d6 = {"within_site_disjoint": within[0], "within_site_pairs": within[1],
          "cross_site_disjoint": cross[0], "cross_site_pairs": cross[1],
          "within_site_density": (within[0] / within[1]) if within[1] else None,
          "cross_site_density": (cross[0] / cross[1]) if cross[1] else None}

    # D7, from the committed bytes with no new fetch: the tail arm is the *most
    # downvoted* questions, and a question closed as a duplicate may accumulate downvotes
    # because it was closed. If that reverse path carried the whole effect, the gradient
    # would live only at negative scores. E033's low tertile had median 1 and its closures
    # sat at -2..+4, so it is checked here rather than assumed.
    bands = [("s<=-3", lambda s: s <= -3), ("-2..0", lambda s: -2 <= s <= 0),
             ("1..2", lambda s: 1 <= s <= 2), ("s>=3", lambda s: s >= 3)]
    tail_bands = {}
    for name, pred in bands:
        tail_bands[name] = arm_stats([r for r in pooled["tail"]
                                      if r["score"] is not None and pred(r["score"])])

    b1 = {"tail": accepted_share(pooled["tail"]), "default": accepted_share(pooled["default"])}
    b1["difference_ci95"] = list(newcombe(b1["tail"]["no_accepted_answer"], b1["tail"]["dups"],
                                          b1["default"]["no_accepted_answer"],
                                          b1["default"]["dups"]))

    rep = {t: arm_stats([r for r in samples["r1"] if r["tag"] == t]) for t in
           sorted({r["tag"] for r in samples["r1"]})}
    return {"pages": pages, "declared": declared, "samples": samples,
            "overlap": overlap, "per_tag": per_tag, "pooled": pooled_stats,
            "matched": matched_stats, "sensitivity": sens, "eligible": eligible,
            "disjoint": disjoint, "b1": b1, "replication": rep, "r2": r2_eligible,
            "d6": d6, "d7": tail_bands}
