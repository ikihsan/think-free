#!/usr/bin/env python3
"""E174: recompute every E170 arm from E170's own raw responses.

Reads only committed files:

  raw/rawlog.json   the raw responses, in the order run.py appended them
  raw/rows.json     the per-row queries and targets

The stored per-arm rank is **never read**: rank is re-derived from the returned
`html_url` list by target identity, which is the same identity test run.py used.
If the replayed query strings do not match the raw log string-for-string, the
alignment is reported as failed rather than assumed (G2).
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
E170 = os.path.join(os.path.dirname(HERE), "170-fix-reachability-rank")
sys.path.insert(0, E170)
import ghsearch as gs  # noqa: E402  (committed by E170; arms() only)

GLOBAL_ARMS = ("A0_bare_global", "A0_quoted_global", "A1_global", "A2_global")
SCOPED_ARMS = ("A0_bare_repo", "A0_quoted_repo", "A1_repo")
# E170 wrote these seven; A2_global is the owner-stripped component form.
ALL_ARMS = ("A0_bare_global", "A0_quoted_repo", "A0_quoted_global", "A0_bare_repo",
            "A1_global", "A1_repo", "A2_global")
SCOPED_FAMILY = ("A0_bare_repo", "A0_quoted_repo", "A1_repo")


def wilson(k, n, z=1.959963984540054):
    if not n:
        return [None, None]
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(max(0.0, centre - half), 4), round(min(1.0, centre + half), 4)]


def mcnemar_exact(a_only, b_only):
    """Two-sided exact McNemar: 2 * 0.5 ** (a_only + b_only)."""
    n = a_only + b_only
    if n == 0:
        return 1.0
    return round(2 * 0.5 ** n, 6)


def replay(rawlog, rows):
    """Zip raw responses to rows by replaying run.py's append order."""
    it = iter(rawlog)
    aligned, mismatches = [], []
    for r in rows:
        rec = {"qid": r["qid"], "control": next(it), "placebo": next(it)}
        for name, query in gs.arms(r, r["target"]):
            got = next(it)
            rec[name] = got
            # Two-sided proof of alignment: the query this driver would send now
            # must equal the query the raw log recorded, and the raw log's own
            # arm label must equal the arm name this driver expected.
            if got.get("query") != query:
                mismatches.append({"qid": r["qid"], "arm": name,
                                   "replayed": query, "logged": got.get("query")})
            if got.get("arm") != name:
                mismatches.append({"qid": r["qid"], "arm": name,
                                   "logged_arm": got.get("arm")})
        aligned.append(rec)
    return aligned, mismatches, list(it)


def rank_from_urls(urls, target):
    want = gs.target_key(target)
    for i, u in enumerate(urls or [], start=1):
        m = gs._TRACK.search(u or "")
        if m and gs.norm_target(m.group(1), m.group(2), int(m.group(3))) == want:
            return i
    return None


def main():
    with open(os.path.join(E170, "raw", "rawlog.json")) as fh:
        rawlog = json.load(fh)
    with open(os.path.join(E170, "raw", "rows.json")) as fh:
        rows = json.load(fh)
    with open(os.path.join(E170, "raw", "summary.json")) as fh:
        stored = json.load(fh)["arms"]

    aligned, mismatches, leftover = replay(rawlog, rows)

    # ---- G2: the alignment must be proven by string equality ---------------
    g2 = {"records": len(rawlog), "consumed": len(rawlog) - len(leftover),
          "leftover": len(leftover), "query_string_mismatches": len(mismatches),
          "pass": not mismatches and not leftover}

    # ---- recompute reach per arm, two denominators ------------------------
    hits, of_all, of_queried = {}, {}, {}
    ranks = {}
    for name in ALL_ARMS:
        h = q = 0
        ranks[name] = []
        for i, rec in enumerate(aligned):
            got = rec.get(name)
            rk = rank_from_urls((got or {}).get("urls"), rows[i]["target"])
            ranks[name].append(rk)
            if got is None:
                continue
            q += 1
            if rk is not None:
                h += 1
        hits[name], of_queried[name], of_all[name] = h, q, len(aligned)

    # ---- G1: equality with the stored arms ---------------------------------
    g1_rows = []
    for name in ALL_ARMS:
        s = stored.get(name, {})
        g1_rows.append({
            "arm": name, "stored_hits": s.get("hits_top10"),
            "stored_of": s.get("of"), "stored_rate": s.get("rate"),
            "recomputed_hits": hits[name], "recomputed_of": of_all[name],
            "recomputed_rate": round(hits[name] / of_all[name], 4) if of_all[name] else None,
            "of_rows_with_a_query": of_queried[name],
            "median_total": s.get("median_total"),
            "equal": s.get("hits_top10") == hits[name] and s.get("of") == of_all[name],
        })
    g1 = {"pass": all(r["equal"] for r in g1_rows), "arms": g1_rows}

    # ---- G3: scoped vs global, paired on the same rows --------------------
    def paired(a, b):
        a_only = b_only = both = neither = 0
        for ra, rb in zip(ranks[a], ranks[b]):
            ha, hb = ra is not None, rb is not None
            if ha and hb:
                both += 1
            elif ha:
                a_only += 1
            elif hb:
                b_only += 1
            else:
                neither += 1
        return {"a": a, "b": b, "both": both, "a_only": a_only, "b_only": b_only,
                "neither": neither, "a_rate": round((both + a_only) / len(ranks[a]), 4),
                "b_rate": round((both + b_only) / len(ranks[b]), 4),
                "mcnemar_exact_p": mcnemar_exact(a_only, b_only),
                "a_ci95": wilson(both + a_only, len(ranks[a])),
                "b_ci95": wilson(both + b_only, len(ranks[b]))}

    comparisons = [paired("A1_repo", "A1_global"),
                   paired("A0_quoted_repo", "A0_quoted_global"),
                   paired("A0_bare_repo", "A0_bare_global")]

    # union: does any scoped query reach the fix, and any global one?
    union = {}
    for label, fam in (("scoped_union", SCOPED_FAMILY), ("global_union", GLOBAL_ARMS)):
        h = sum(1 for i in range(len(aligned))
                if any(ranks[a][i] is not None for a in fam if a in ranks))
        union[label] = {"hits": h, "of": len(aligned),
                        "rate": round(h / len(aligned), 4), "ci95": wilson(h, len(aligned))}
    union["scoped_only"] = sum(1 for i in range(len(aligned))
                               if any(ranks[a][i] is not None for a in SCOPED_FAMILY)
                               and not any(ranks[a][i] is not None for a in GLOBAL_ARMS))
    union["global_only"] = sum(1 for i in range(len(aligned))
                               if any(ranks[a][i] is not None for a in GLOBAL_ARMS)
                               and not any(ranks[a][i] is not None for a in SCOPED_FAMILY))
    # The union comparison is the one clean statement of the omitted finding:
    # same 13 rows, any of the three scoped query forms against any of the four
    # global ones.  both = |scoped ∩ global|, computed from the two hit sets.
    both = union["scoped_union"]["hits"] - union["scoped_only"]
    union["paired"] = {"both": both, "scoped_only": union["scoped_only"],
                       "global_only": union["global_only"],
                       "neither": len(aligned) - both - union["scoped_only"]
                                  - union["global_only"],
                       "mcnemar_exact_p": mcnemar_exact(union["scoped_only"],
                                                       union["global_only"])}

    # ---- the bar E170 declared --------------------------------------------
    best_scoped = max(((hits[a] / of_all[a], a) for a in SCOPED_FAMILY))
    bar = {"declared_bar": 0.30, "best_scoped_arm": best_scoped[1],
           "best_scoped_rate": round(best_scoped[0], 4),
           "best_scoped_ci95": wilson(hits[best_scoped[1]], of_all[best_scoped[1]]),
           "point_estimate_clears_bar": best_scoped[0] >= 0.30,
           "lower_bound_clears_bar": wilson(hits[best_scoped[1]], of_all[best_scoped[1]])[0] >= 0.30,
           "note": "primary denominator is all 13 rows, the conservative choice E170 "
                   "itself made when it reported A0_global as 1/13; the arm's own "
                   "denominator is reported beside it because the literal arms only "
                   "produce a query for rows that have a quoted literal",
           "per_arm_own_denominator": {
               a: {"hits": hits[a], "of": of_queried[a],
                   "rate": round(hits[a] / of_queried[a], 4) if of_queried[a] else None,
                   "ci95": wilson(hits[a], of_queried[a])}
               for a in ALL_ARMS}}

    out = {"experiment": "E174", "source": "E170 committed raw responses",
           "rows": len(aligned), "G1": g1, "G2": g2, "G3": comparisons,
           "union": union, "bar": bar,
           "scoped_arms": sorted(SCOPED_FAMILY), "global_arms": sorted(GLOBAL_ARMS),
           "row_ranks": {r["qid"]: {a: ranks[a][i] for a in ALL_ARMS}
                         for i, r in enumerate(aligned)}}
    dest = os.path.join(HERE, "results.json")
    with open(dest, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(json.dumps({k: v for k, v in out.items() if k != "row_ranks"}, indent=1))
    print("wrote %s" % dest)


if __name__ == "__main__":
    main()