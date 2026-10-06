"""E034 — the gate table. PROTOCOL.md section 5, recomputed from the committed bytes.

`tally.py` prints the table and writes raw/tally.json. `tally.py --check` is the
verification command: it re-reads raw/pages.jsonl, re-hashes every response body it
logged, recomputes every rate, and exits non-zero if anything disagrees with what is
recorded, if a declared arm is missing, or if the population is not the declared one.

`--check` is verification, not the verdict: a gate that fails is a result, so it is
printed and recorded but does not fail verification. `--gates` asserts the gate outcomes
and is the command that exits 3.
"""

import collections
import json
import os
import sys

import reask
from measures import CHANNELS, DUPLICATE, DUPLICATE_SET, RAW, arm_stats, build, digest_ok

def gates(d):
    p = d["pages"]
    pool, match = d["pooled"], d["matched"]
    allr = d["declared"] + [r for v in d["samples"].values() for r in v]
    closed_no_reason = sum(1 for r in allr if r["closed_date"] and not r["has_closed_reason_key"])
    no_key = sum(1 for r in allr if not r["has_closed_reason_key"])
    bad_status = sum(1 for x in p if x["status"] != 200)
    tails_with_dup = sum(1 for t in d["per_tag"] if d["per_tag"][t]["tail"]["dup"] > 0)
    lo_t, hi_def = pool["tail"]["ci"][0], pool["default"]["ci"][1]
    lo_t2, hi_head = pool["tail"]["ci"][0], pool["head"]["ci"][1]
    mt, mh, md = match["tail"]["ci"], match["head"]["ci"], match["default"]["ci"]
    b1lo, b1hi = d["b1"]["difference_ci95"]
    rep_ok = []
    for t, st in d["replication"].items():
        base = d["per_tag"][t]["tail"]
        rep_ok.append("%s %.3f->%.3f %s" % (t, base["rate"], st["rate"],
                                            "ok" if not (st["ci"][1] < base["ci"][0]
                                                         or base["ci"][1] < st["ci"][0])
                                            else "MISSED"))
    dd = d["d6"]
    lit = collections.Counter(r["closed_reason"] for r in allr)
    return [
        ("A1a", "every logged request returned 200", "%d of %d non-200" % (bad_status, len(p)),
         bad_status == 0),
        ("A1b", "no row is closed without stating a reason — the substitution for the "
                "declared key rule, which the API's own behaviour makes unsatisfiable",
         "%d closed rows with no reason key, of %d rows" % (closed_no_reason, len(allr)),
         closed_no_reason == 0),
        ("A1c", "declared disclosure: the key is absent on open rows, not missing data",
         "%d of %d rows carry no closed_reason key" % (no_key, len(allr)), None),
        ("A1d", "declared disclosure: the label is a set of literals, not one",
         "%d rows carry 'exact duplicate', which the primary label excludes"
         % lit.get("exact duplicate", 0), None),
        ("A2", "at least 3 of 8 tags have a duplicate closure in the tail arm",
         "%d of 8" % tails_with_dup, tails_with_dup >= 3),
        ("A3a", "pooled tail CI95 lower > pooled default (Active tab) CI95 upper",
         "%.4f > %.4f" % (lo_t, hi_def), lo_t > hi_def),
        ("A3b", "pooled tail CI95 lower > pooled head CI95 upper",
         "%.4f > %.4f" % (lo_t2, hi_head), lo_t2 > hi_head),
        ("A3b-matched", "matched-n tail CI95 lower > matched-n head CI95 upper",
         "%.4f > %.4f" % (mt[0], mh[1]), mt[0] > mh[1]),
        ("A3a-matched", "matched-n tail CI95 lower > matched-n default CI95 upper",
         "%.4f > %.4f" % (mt[0], md[1]), mt[0] > md[1]),
        ("A4", "two tags with tail n>=50 have disjoint tail CI95s  [KILL GATE]",
         "%d tags eligible, %d disjoint pairs: %s" % (
             len(d["eligible"]), len(d["disjoint"]),
             ", ".join("%s|%s" % (a, b) for a, b in d["disjoint"][:4])),
         len(d["disjoint"]) >= 1),
        ("R1", "AMENDMENT-1: the two tags that decide A4 reproduce on the next pages",
         "; ".join(rep_ok), bool(rep_ok) and "MISSED" not in " ".join(rep_ok)),
        ("D6", "AMENDMENT-1: same-site tag pairs separate as often as cross-site pairs, so "
               "the spread is not a site artefact",
         "within-site %d/%d = %.2f vs cross-site %d/%d = %.2f" % (
             dd["within_site_disjoint"], dd["within_site_pairs"], dd["within_site_density"],
             dd["cross_site_disjoint"], dd["cross_site_pairs"], dd["cross_site_density"]),
         dd["within_site_density"] >= dd["cross_site_density"]),
        ("B1", "tail minus default share of duplicates with no accepted answer, CI95 "
               "excludes 0", "[%+.4f, %+.4f]" % (b1lo, b1hi),
         b1lo is not None and (b1lo > 0 or b1hi < 0)),
        ("D7", "declared, not a gate: within the tail the peak is at score 0, not at the "
               "most-downvoted, so closure earning its own downvotes does not explain the "
               "whole gradient — and the tail never reaches score +1, which is why it cannot",
         "; ".join("%s %d/%d=%s" % (k, v["dup"], v["n"],
                                    "-" if v["rate"] is None else "%.3f" % v["rate"])
                   for k, v in d["d7"].items()), None),
    ]


def table(rows, out=sys.stdout):
    width = max(len(n) for n, _d, _v, _o in rows)
    for name, rule, detail, outcome in rows:
        mark = "n/a " if outcome is None else ("pass" if outcome else "FAIL")
        out.write("%-*s %-4s %s\n" % (width, name, mark, detail))
        out.write("%-*s       rule: %s\n" % (width, "", rule))
    return 0 if all(o for _n, _r, _d, o in rows if o is not None) else 3


def main(argv):
    # `--check` is verification: it asks whether the run is the run that was declared and
    # whether the committed bytes still say so. It is not the verdict. A gate that fails
    # is a result, so it is printed and recorded but does not fail verification;
    # `--gates` asserts the gate outcomes and is the command that exits 3.
    check = "--check" in argv
    strict = "--gates" in argv
    d = build()
    g = gates(d)

    problems = []
    bad_digests = digest_ok(d["pages"])
    if bad_digests:
        problems.append("digest mismatch on %d logged responses: %s"
                        % (len(bad_digests), bad_digests[:2]))
    declared_arms = {(p["tag"], p["arm"]) for p in d["pages"]}
    for tag in reask.DECLARED_TAGS:
        for arm in ("tail", "head", "default"):
            if (tag, arm) not in declared_arms:
                problems.append("declared arm never fetched: %s/%s" % (tag, arm))
    for tag in [t[2] for t in reask.TAGS if t[2] not in reask.DECLARED_TAGS]:
        if (tag, "tail") not in declared_arms:
            problems.append("AMENDMENT-1 R2 tail arm never fetched: %s" % tag)
    for t in d["per_tag"]:
        if d["per_tag"][t]["tail"]["n"] == 0:
            problems.append("empty tail arm: %s" % t)
    if len(d["declared"]) == 0:
        problems.append("no declared population committed")

    rc = table(g)
    out = sys.stdout.write
    out("\npooled, primary literal %r\n" % DUPLICATE)
    for a in ("tail", "head", "default"):
        s = d["pooled"][a]
        out("  %-8s n=%-4d dup=%-3d rate=%.4f CI95[%.4f,%.4f] score[%s,%s]\n" % (
            a, s["n"], s["dup"], s["rate"], s["ci"][0], s["ci"][1], s["score_min"],
            s["score_max"]))
    out("\nmatched-n (each arm truncated to the smallest per-tag arm)\n")
    for a in ("tail", "head", "default"):
        s = d["matched"][a]
        out("  %-8s n=%-4d dup=%-3d rate=%.4f CI95[%.4f,%.4f]\n" % (
            a, s["n"], s["dup"], s["rate"], s["ci"][0], s["ci"][1]))
    out("\nper-tag tail rate, and the Active-tab rate it is being compared against\n")
    for t, v in d["per_tag"].items():
        out("  %-24s tail %d/%d=%.4f [%.4f,%.4f]   default %d/%d=%.4f\n" % (
            t, v["tail"]["dup"], v["tail"]["n"], v["tail"]["rate"], v["tail"]["ci"][0],
            v["tail"]["ci"][1], v["default"]["dup"], v["default"]["n"], v["default"]["rate"]))
    out("\nS1 sensitivity: adding the legacy literal 'exact duplicate'\n")
    for a in ("tail", "head", "default"):
        s, b = d["sensitivity"][a], d["pooled"][a]
        out("  %-8s %d/%d=%.4f (was %d/%d=%.4f)\n" % (a, s["dup"], s["n"], s["rate"],
                                                     b["dup"], b["n"], b["rate"]))
    out("\nB1: duplicates with no accepted answer\n")
    for a in ("tail", "default"):
        b = d["b1"][a]
        out("  %-8s %d/%d=%.4f CI95[%.4f,%.4f]\n" % (a, b["no_accepted_answer"], b["dups"],
                                                    b["share"], b["ci"][0], b["ci"][1]))
    out("  difference (tail - default) CI95 [%+.4f, %+.4f]\n" % tuple(d["b1"]["difference_ci95"]))
    out("\nD7 the tail arm split by score: is the gradient only downvotes?\n")
    for k, v in d["d7"].items():
        if not v["n"]:
            out("  %-6s n=0\n" % k)
            continue
        out("  %-6s n=%-4d dup=%-3d rate=%.4f CI95[%.4f,%.4f]\n" % (
            k, v["n"], v["dup"], v["rate"], v["ci"][0], v["ci"][1]))
    out("  head   n=%-4d dup=%-3d rate=%.4f CI95[%.4f,%.4f]  (scores all >= %s)\n" % (
        d["pooled"]["head"]["n"], d["pooled"]["head"]["dup"], d["pooled"]["head"]["rate"],
        d["pooled"]["head"]["ci"][0], d["pooled"]["head"]["ci"][1],
        d["pooled"]["head"]["score_min"]))
    out("\nAMENDMENT-1 R1, out-of-sample replication (overlapping ids removed: %d of %d)\n"
        % (len(d["overlap"]["r1"]), len(d["overlap"]["r1"]) + len(d["samples"]["r1"])))
    for t, s in sorted(d["replication"].items()):
        out("  %-24s declared %.4f [%.4f,%.4f]  replicate %d/%d=%.4f [%.4f,%.4f]\n" % (
            t, d["per_tag"][t]["tail"]["rate"], d["per_tag"][t]["tail"]["ci"][0],
            d["per_tag"][t]["tail"]["ci"][1], s["dup"], s["n"], s["rate"],
            s["ci"][0], s["ci"][1]))
    out("\nAMENDMENT-1 R2, the site/tag confound test (overlapping ids removed: %d of %d)\n"
        % (len(d["overlap"]["r2"]), len(d["overlap"]["r2"]) + len(d["samples"]["r2"])))
    site_of = {t[2]: t[1] for t in reask.TAGS}
    for t, s in sorted(d["r2"].items()):
        out("  %-24s %-16s tail %d/%d=%.4f [%.4f,%.4f]\n" % (
            t, site_of[t], s["dup"], s["n"], s["rate"], s["ci"][0], s["ci"][1]))
    out("  D6 within-site disjoint pairs %d/%d = %.2f; cross-site %d/%d = %.2f\n" % (
        d["d6"]["within_site_disjoint"], d["d6"]["within_site_pairs"],
        d["d6"]["within_site_density"], d["d6"]["cross_site_disjoint"],
        d["d6"]["cross_site_pairs"], d["d6"]["cross_site_density"]))
    out("\nD5 the canonical edge: channels consulted and what each returned\n")
    for what, got, where in CHANNELS:
        out("  %-38s %-46s %s\n" % (what, got, where))
    out("\nclosure-reason literals seen, verbatim\n")
    for lit, c in collections.Counter(
            r["closed_reason"] for r in d["declared"]
            + [r for v in d["samples"].values() for r in v]).most_common():
        out("  %-30r %d\n" % (lit, c))

    with open(os.path.join(RAW, "tally.json"), "w") as fh:
        json.dump({"gates": [{"name": n, "rule": r, "detail": v, "outcome": o}
                             for n, r, v, o in g],
                   "pooled": d["pooled"], "matched": d["matched"],
                   "per_tag": d["per_tag"], "sensitivity": d["sensitivity"],
                   "b1": d["b1"], "replication": d["replication"], "r2": d["r2"],
                   "d6": d["d6"], "d7": d["d7"], "disjoint_pairs": d["disjoint"],
                   "overlap_rows_removed": {k: len(v) for k, v in d["overlap"].items()},
                   "channels": CHANNELS}, fh, indent=1, sort_keys=True)

    if problems:
        out("\nINTEGRITY PROBLEMS\n")
        for p in problems:
            out("  " + p + "\n")
        return 4
    if not check and not strict:
        return 0
    return rc if strict else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
