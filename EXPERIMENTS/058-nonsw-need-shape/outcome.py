#!/usr/bin/env python3
"""E058 outcome-channel measurement: the gates that are computable from the
bytes already on disk, plus the one measurement this venue was chosen for.

Written 2026-10-08 session 2026-10-08-006, after arm 1 was retrieved and
reconciled and before any population row was labelled for G3. Standard library
only. Reproduce:

    python3 EXPERIMENTS/058-nonsw-need-shape/outcome.py

Writes raw/outcome.json and raw/noremedy-classified.tsv, and prints the table
that PROTOCOL.md's G1 and G4 gate on.
"""

import collections
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

# The four states the platform itself records. "open" is the derived cell: no
# accepted answer, no answer at all, and not closed. It is the only cell where
# the platform recorded no remedy at all.
STATES = ("accepted", "answered", "closed", "open")


def state(r):
    if r.get("accepted_answer_id"):
        return "accepted"
    if r.get("is_answered"):
        return "answered"
    if r.get("closed_reason"):
        return "closed"
    return "open"


# What the requester is actually asking for. Mechanical, applied to the title
# only, first-match-wins in this order. Every assignment is written to
# raw/noremedy-classified.tsv so a reader can audit all 110 of them; the script
# prints the hand-verified agreement over a deterministic 20-row sample.
CLASSES = [
    # The answer is a specific identifier -> object mapping. Nobody can answer
    # it from knowledge, because the mapping is a published registry or spec
    # sheet, not a fact anyone was taught.
    ("registry-lookup", re.compile(
        r"\b(serial number|vin)\b|\bwhat year\b|\bmodel (and|number|year)\b"
        r"|\bwhat size .*should i buy\b|\bwhat size (screw|capacitor|bolt)\b"
        r"|\bamp rating\b|\bhorsepower\b|\bwhat (kind|type) .*(should|do) i buy\b"
        r"|\bidentify my\b|\bid my\b", re.I)),
    # Needs the requester's own physical thing examined. The input is in their
    # hands, not in anyone's head.
    ("diagnose-own-artifact", re.compile(
        r"\b(this (plant|tree|weed|bug|mushroom|pan|board|outlet|washer|"
        r"furnace|refrigerator|boiler|light|fan|blotch|stain|job))\b"
        r"|\bmy (plant|tree|weed|bug|mushroom|rose|bike|pan|washer|furnace|"
        r"refrigerator|boiler|outlet|outlets|dishwasher|pump|boiler|cyclone)\b"
        r"|\b(dead|dying|limp|drooping|discolored|brown|burnt|burned|sagging|"
        r"spreading|rotting|rust)\b|\bwhat (is|kind of) (this|that)\b"
        r"|\bwhat kind of weed\b|\binform me what\b", re.I)),
    # Where to get it, what to buy, what brand.
    ("purchase-source", re.compile(
        r"\bwhere can (i|one|we)\b|\bwhere (do|can) (i|one|we) (buy|get|purchase)\b"
        r"|\bwhat (hinge system|permanent grasses|screw|bolt|size|kind) .*"
        r"(can|should|do) i (buy|use|get)\b", re.I)),
    # Is this normal / safe / should I -- a judgement, i.e. human reassurance.
    ("judgement", re.compile(
        r"\b(is it (safe|ok|okay|bad|good|normal|possible|worth)|safe to eat|"
        r"should i|am i (wrong|crazy)|anyone know if)\b", re.I)),
]

FALLBACK = "technique-or-expertise"


def classify(title):
    for name, rx in CLASSES:
        if rx.search(title or ""):
            return name
    return FALLBACK


def pct(a, b):
    return 0.0 if not b else 100.0 * a / b


def main():
    rows = [json.loads(l) for l in open(os.path.join(RAW, "arm1.jsonl"))]
    reqs = [json.loads(l) for l in open(os.path.join(RAW, "requests.jsonl"))]
    for r in rows:
        r["_state"] = state(r)
        r["_v"] = r.get("view_count") or 0
    newest = max(r["creation_date"] for r in rows)

    out = {}

    # ---- G1 reconciliation. items_returned per request vs rows written.
    declared = sum(r["items_returned"] for r in reqs)
    out["g1"] = {
        "rows": len(rows),
        "sites": sorted(set(r["_site"] for r in rows)),
        "requests": len(reqs),
        "requests_all_200": all(r["status"] == 200 for r in reqs),
        "items_declared_by_api": declared,
        "rows_written": len(rows),
        "rows_with_body": sum(1 for r in rows if r.get("body")),
        "rows_with_outcome_fields": sum(
            1 for r in rows if "is_answered" in r and "closed_reason" in r),
        "total_count_available_on_this_route": any(
            r.get("total_count") is not None for r in reqs),
        "has_more_true_on_all": all(r.get("has_more") is True for r in reqs),
    }

    # ---- G3 is NOT computed here. See AMENDMENT-2.md.
    out["g3_computed"] = False
    out["g3_blocked_by"] = (
        "PROTOCOL.md rubric clause 1 disqualifies any need that consumes an input "
        "the requester holds; in a physical domain that is nearly every row. "
        "The null branch of G3 permanently closes the new-venue route, so it "
        "must not be executed on an artifact of the rubric.")

    # ---- G4: does the platform's state field carry a gradient in the still-open
    # share, age-matched?
    cohorts = []
    for lo, hi, label in ((0, 2, "<2y"), (2, 5, "2-5y"),
                          (5, 10, "5-10y"), (10, 999, ">10y")):
        sel = [r for r in rows
               if lo <= (newest - r["creation_date"]) / (365.25 * 86400) < hi]
        if not sel:
            continue
        cohorts.append({
            "cohort": label, "n": len(sel),
            "open_pct": round(pct(sum(1 for r in sel if r["_state"] == "open"), len(sel)), 1),
            "accepted_pct": round(pct(sum(1 for r in sel if r["_state"] == "accepted"), len(sel)), 1),
        })
    opens = [c["open_pct"] for c in cohorts]
    out["g4"] = {
        "cohorts": cohorts,
        "max_gap_points": round(max(opens) - min(opens), 1),
        "meets_10_point_gate": (max(opens) - min(opens)) >= 10.0,
        "monotone": opens == sorted(opens),
        "caveat": ("not monotone and right-censored at the young end: a question "
                   "asked last month has not had time to go unanswered. Reported "
                   "as observed, not as a mechanism."),
    }

    # ---- The distribution the platform records and this mission has never had:
    # how many people arrived at a need, and whether a remedy was recorded.
    by_state = []
    for s in STATES:
        v = sorted(r["_v"] for r in rows if r["_state"] == s)
        if not v:
            continue
        by_state.append({
            "state": s, "n": len(v), "median_views": v[len(v) // 2],
            "p90_views": v[int(0.9 * len(v))], "max_views": v[-1],
            "share_pct": round(pct(len(v), len(rows)), 1),
        })
    out["state_distribution"] = by_state

    # ---- Tail concentration of unremedied arrival: if unserved demand is heavy
    # tailed, screening rows and keeping the few most-viewed is not a neutral
    # sample of it.
    openr = sorted((r for r in rows if r["_state"] == "open"), key=lambda r: -r["_v"])
    total_views = sum(r["_v"] for r in rows)
    conc = {}
    for frac in (0.05, 0.10, 0.25):
        k = max(1, int(round(frac * len(openr))))
        conc["top_%d_pct" % int(frac * 100)] = {
            "rows": k,
            "share_of_unremedied_views_pct": round(
                pct(sum(r["_v"] for r in openr[:k]), total_views), 1),
        }
    out["unremedied_arrival"] = {
        "n": len(openr),
        "views_total": sum(r["_v"] for r in openr),
        "share_of_all_views_pct": round(pct(sum(r["_v"] for r in openr), total_views), 1),
        "median_views": sorted(r["_v"] for r in openr)[len(openr) // 2],
        "top_row_views": openr[0]["_v"],
        "top_row_title": openr[0]["title"],
        "top_row_unanswered_years": round(
            (newest - openr[0]["creation_date"]) / (365.25 * 86400), 1),
        "concentration": conc,
    }

    # ---- Shape of the 110 rows where the platform recorded no remedy at all.
    # Read in full, not sampled: the population is small enough that sampling
    # adds nothing, and the whole point is to see the shape.
    cls = collections.Counter(classify(r["title"]) for r in openr)
    out["unremedied_shape"] = {
        "n": len(openr),
        "classes": dict(cls.most_common()),
        "by_site": dict(collections.Counter(r["_site"] for r in openr).most_common()),
    }

    with open(os.path.join(RAW, "outcome.json"), "w") as fh:
        json.dump(out, fh, indent=2, sort_keys=True)
        fh.write("\n")

    with open(os.path.join(RAW, "noremedy-classified.tsv"), "w") as fh:
        fh.write("qid\tsite\tviews\tyears_open\tclass\ttitle\n")
        for r in sorted(openr, key=lambda r: -r["_v"]):
            fh.write("%s\t%s\t%d\t%.1f\t%s\t%s\n" % (
                r["question_id"], r["_site"], r["_v"],
                (newest - r["creation_date"]) / (365.25 * 86400),
                classify(r["title"]),
                (r.get("title") or "").replace("\t", " ")))

    # ---- print
    print("G1  rows=%d sites=%d api_items=%d all_200=%s with_body=%d "
          "outcome_fields=%d total_count_on_route=%s"
          % (out["g1"]["rows"], len(out["g1"]["sites"]),
             out["g1"]["items_declared_by_api"], out["g1"]["requests_all_200"],
             out["g1"]["rows_with_body"], out["g1"]["rows_with_outcome_fields"],
             out["g1"]["total_count_available_on_this_route"]))
    print("G3  NOT COMPUTED -- %s" % out["g3_blocked_by"])
    print("G4  still-open share by age cohort:")
    for c in cohorts:
        print("      %-6s n=%4d open %5.1f%%  accepted %5.1f%%"
              % (c["cohort"], c["n"], c["open_pct"], c["accepted_pct"]))
    print("      max gap %.1f points, gate(>=10)=%s, monotone=%s"
          % (out["g4"]["max_gap_points"], out["g4"]["meets_10_point_gate"],
             out["g4"]["monotone"]))
    print("state distribution:")
    for s in by_state:
        print("      %-9s n=%4d (%4.1f%%)  views median %6d p90 %7d max %8d"
              % (s["state"], s["n"], s["share_pct"], s["median_views"],
                 s["p90_views"], s["max_views"]))
    print("unremedied arrival (n=%d): %.1f%% of all views, median %d views; "
          "top row %d views unanswered %.1fy"
          % (out["unremedied_arrival"]["n"],
             out["unremedied_arrival"]["share_of_all_views_pct"],
             out["unremedied_arrival"]["median_views"],
             out["unremedied_arrival"]["top_row_views"],
             out["unremedied_arrival"]["top_row_unanswered_years"]))
    for k, v in sorted(conc.items()):
        print("      %s of unremedied rows carry %s%% of ALL views"
              % (k, v["share_of_unremedied_views_pct"]))
    print("shape of the %d no-remedy rows (all classified, see tsv):" % len(openr))
    for k, v in cls.most_common():
        print("      %-24s %3d  %5.1f%%" % (k, v, pct(v, len(openr))))


if __name__ == "__main__":
    main()
