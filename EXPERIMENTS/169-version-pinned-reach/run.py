"""E169 step 3: extract the literal, find the accepted answer's tracker target,
query the tracker with the literal, and record the rank of the target.

`--dry-run` writes the query plan without issuing a request, so the literal
extractor can be read before the 10-requests-per-minute budget is spent.
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import literals                                                  # noqa: E402
import reach                                                     # noqa: E402

CLASSIFIED = os.path.join(os.path.dirname(HERE), "168-version-pinned-need",
                          "classified.jsonl")
THREADS = os.path.join(HERE, "threads-all.json")


def load_rows():
    pop = [json.loads(l) for l in open(CLASSIFIED) if l.strip()]
    pop = [r for r in pop if r["vp"] == 1]
    pop.sort(key=lambda r: -r["views"])
    threads = json.load(open(THREADS))
    rows = []
    for r in pop:
        qid = str(r["qid"])
        t = threads.get(qid)
        if not t:
            rows.append({"qid": qid, "idx": r["idx"], "views": r["views"],
                         "title": r["title"], "state": "not_fetchable"})
            continue
        text = literals.to_text(t.get("body"))
        ans = t.get("answers") or []
        accepted = ans[0] if ans else {}
        # AMENDMENT 1: the target is the first tracker link in the thread,
        # accepted answer first.  Accepted-answer-only yields 6 rows, below
        # the protocol's own floor of 8; the thread yields the population the
        # gate was written for.
        target = reach.github_target(accepted.get("body"))
        target_where = "accepted" if target else None
        if not target:
            for a in ans:
                target = reach.github_target(a.get("body"))
                if target:
                    target_where = "other_answer"
                    break
        lit = literals.primary(text)
        rows.append({
            "qid": qid, "idx": r["idx"], "views": r["views"],
            "title": r["title"], "state": "ok",
            "n_answers": len(ans),
            "literal": lit,
            "weak_literal": literals.weak_literal(text),
            "target": target,
            "target_where": target_where,
            "in_e168_24": qid in set(json.load(open(os.path.join(
                os.path.dirname(HERE), "168-version-pinned-need",
                "threads.json"))).keys()),
        })
    return rows


def wilson(k, n, z=1.96):
    if n == 0:
        return [None, None]
    p = k / float(n)
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / d
    return [round(max(0.0, c - h), 4), round(min(1.0, c + h), 4)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    rows = load_rows()
    plan = [r for r in rows if r["state"] == "ok"
            and r.get("target") and r.get("literal")]
    if args.dry_run:
        out = os.path.join(HERE, "raw", "query-plan.json")
        json.dump({"rows": len(rows), "queries": len(plan), "plan": plan},
                  open(out, "w"), indent=1)
        print(json.dumps({"rows_total": len(rows),
                          "not_fetchable": sum(1 for r in rows
                                               if r["state"] != "ok"),
                          "ok": sum(1 for r in rows if r["state"] == "ok"),
                          "with_literal": sum(1 for r in rows if r["state"] == "ok"
                                              and r.get("literal")),
                          "with_target": sum(1 for r in rows if r["state"] == "ok"
                                             and r.get("target")),
                          "queries_planned": len(plan)}, indent=2))
        return 0

    for i, r in enumerate(plan, 1):
        tag = r["title"].split()[0].lower() if r["title"] else ""
        r["primary"] = reach.search_once(r["literal"], r["target"])
        if not r["primary"]["rank"]:
            vs = reach.variants(r["literal"], tag)
            r["variant"] = reach.search_variants(vs, r["target"])
        # G5 null query: the same target, reached by a plausible query that
        # carries no error literal.  If this works as well, the literal is not
        # what did the reaching.
        r["null_query"] = reach.search_once(
            " ".join(r["title"].split()[:8]), r["target"])
        sys.stderr.write("[%d/%d] %s rank=%s null=%s\n" % (
            i, len(plan), r["qid"],
            (r["primary"] or {}).get("rank", "err"),
            (r["null_query"] or {}).get("rank", "err")))

    fetched = [r for r in rows if r["state"] == "ok"]
    with_target = [r for r in fetched if r.get("target")]
    searched = [r for r in with_target if r.get("literal")]
    no_literal = [r for r in with_target if not r.get("literal")]
    unreadable = [r for r in searched if (r.get("primary") or {}).get("unreadable")]
    hit = [r for r in searched
           if (r.get("primary") or {}).get("rank")
           and not (r["primary"] or {}).get("unreadable")]
    var_hit = [r for r in searched
               if not (r.get("primary") or {}).get("rank")
               and (r.get("variant") or {}).get("rank")]
    null_hit = [r for r in searched
                if (r.get("null_query") or {}).get("rank")
                and not (r["null_query"] or {}).get("unreadable")]
    lit_rows = [r for r in fetched if r.get("literal")]
    summary = {
        "population_vp1": 85,
        "rows_measured": len(fetched),
        "rows_not_fetchable": len(rows) - len(fetched),
        "g3_literal_in_post": {"k": len(lit_rows), "n": len(fetched),
                               "share": round(len(lit_rows) / float(len(fetched)), 4),
                               "wilson95": wilson(len(lit_rows), len(fetched))},
        "g3_no_literal": {"k": len(fetched) - len(lit_rows), "n": len(fetched),
                          "share": round((len(fetched) - len(lit_rows)) / float(len(fetched)), 4),
                          "wilson95": wilson(len(fetched) - len(lit_rows), len(fetched))},
        "g2_denominator": {
            "with_tracker_target": len(with_target),
            "of_which_no_literal_so_not_searched": len(no_literal),
            "searched": len(searched),
            "unreadable": len(unreadable),
        },
        "g2_single_exact_query": {"k": len(hit), "n": len(searched),
                                  "share": round(len(hit) / float(len(searched)), 4)
                                  if searched else None,
                                  "wilson95": wilson(len(hit), len(searched))},
        "g4_variant_arm": {"k": len(var_hit), "n": len(searched) - len(hit),
                           "share_of_searched": round(len(var_hit) / float(len(searched)), 4)
                           if searched else None,
                           "combined_with_primary": {
                               "k": len(hit) + len(var_hit), "n": len(searched),
                               "share": round((len(hit) + len(var_hit)) / float(len(searched)), 4)
                               if searched else None}},
        "ranks": sorted((r["primary"] or {}).get("rank")
                        for r in searched if (r["primary"] or {}).get("rank")),
        "g5_null_query": {"k": len(null_hit), "n": len(searched),
                          "share": round(len(null_hit) / float(len(searched)), 4)
                          if searched else None,
                          "wilson95": wilson(len(null_hit), len(searched))},
        "target_where": {w: sum(1 for r in with_target if r["target_where"] == w)
                         for w in ("accepted", "other_answer")},
    }
    json.dump({"summary": summary, "rows": rows},
              open(os.path.join(HERE, "raw", "results.json"), "w"), indent=1)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())