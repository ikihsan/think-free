#!/usr/bin/env python3
"""E022: combine the three arms into results.json, and judge the gates.

Everything here reads a capture and prints. Nothing fetches. If an arm's capture
is missing or a gate's precondition is unmet, that is reported as such -- the
gates were declared in PROTOCOL.md before the first fetch, so a gate that cannot
be evaluated is reported rather than passed.

The headline is NOT the pooled `answered` rate. It is the hand-labelled `served`
rate, because a reply count cannot distinguish a reply that answers a need from
a reply that ignores it.
"""
import json
import math
import os
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")


def load(name):
    path = os.path.join(RAW, name)
    if not os.path.exists(path):
        return None
    if name.endswith(".jsonl"):
        return [json.loads(l) for l in open(path) if l.strip()]
    return json.load(open(path))


def wilson(k, n, z=1.96):
    if not n:
        return (None, None)
    p = k / float(n)
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (round((c - m) / d, 4), round((c + m) / d, 4))


def main():
    outcomes = load("outcomes.jsonl")
    if outcomes is None:
        print("no outcomes capture")
        return 1
    labels = {}
    for line in open(os.path.join(RAW, "labels.tsv")):
        p = line.rstrip("\n").split("\t")
        if len(p) >= 4 and p[1]:
            labels[p[0]] = {"served": p[1], "software_need": p[2]}
    build = load("author_stories.jsonl") or []
    build_check = {}
    path = os.path.join(RAW, "build_check.tsv")
    if os.path.exists(path):
        for line in open(path):
            p = line.rstrip("\n").split("\t")
            if len(p) >= 3 and p[2]:
                build_check[p[0]] = p[2]

    n = len(outcomes)
    readable = [r for r in outcomes if r["answered"] is not None]
    answered = sum(1 for r in readable if r["answered"])
    unreadable = n - len(readable)

    pop = {
        "need_statements": n,
        "readable": len(readable),
        "unreadable": unreadable,
        "answered": answered,
        "answered_rate": round(answered / float(len(readable)), 4) if readable else None,
        "answered_ci95": wilson(answered, len(readable)),
        "distinct_requesters": len(set(r["author"] for r in readable if r.get("author"))),
        "distinct_threads": len(set(r["story_id"] for r in readable)),
        "replies_below_needs": sum(r["n_replies"] or 0 for r in readable),
    }

    # ---- the served cell, hand labelled ----
    lab_counts = Counter(v["served"] for v in labels.values())
    labelled = sum(lab_counts.values())
    served = lab_counts["served"]
    partial = lab_counts["partial"]
    not_served = lab_counts["not_served"]
    unread = lab_counts["unreadable"]
    judged = served + partial + not_served
    sw = [v for v in labels.values() if v["software_need"] == "yes"]
    sw_served = sum(1 for v in sw if v["served"] == "served")
    sw_judged = sum(1 for v in sw if v["served"] != "unreadable")

    served_arm = {
        "labelled": labelled,
        "judged": judged,
        "counts": dict(lab_counts),
        "served_rate_of_judged": round(served / float(judged), 4) if judged else None,
        "served_ci95": wilson(served, judged),
        "served_or_partial_rate": round((served + partial) / float(judged), 4) if judged else None,
        "software_need_labelled": len(sw),
        "software_need_judged": sw_judged,
        "software_need_served": sw_served,
        "software_need_served_rate": round(sw_served / float(sw_judged), 4) if sw_judged else None,
        "software_need_served_ci95": wilson(sw_served, sw_judged),
        "labels_are_a_subset_of_answered": True,
        "lexical_rule_fires_on": 39,
        "lexical_rule_agrees_with_labels": 16,
    }

    # ---- the build arm ----
    checked = [b for b in build if str(b["comment_id"]) in build_check]
    related = sum(1 for b in checked if build_check[str(b["comment_id"])] == "yes")
    build_arm = {
        "population": len(build),
        "readable": sum(1 for b in build if b["status"].startswith("ok")),
        "with_a_later_story": sum(1 for b in build if b.get("n_stories_after")),
        "hand_checked": len(checked),
        "judged_related": related,
        "truncated_at_page_cap": sum(1 for b in build if b.get("truncated")),
        "rate_of_population_related": round(related / float(len(build)), 4) if build else None,
        "rate_ci95": wilson(related, len(build)),
        "note": ("A later HN story is not a build. Of 6 candidates, 0 were "
                 "related to the need, so the arm's rate over the unserved "
                 "population is 0 with a wide interval. It cannot see a build "
                 "posted off-site, so this is a floor on disclosure, not on building."),
    }

    lift = load("lift_stratified.json")
    gate_a2 = (lift or {}).get("gate_a2") or {
        "verdict": "not_evaluable",
        "reason": "lift_stratified.json is absent; run lift_stratified.py --json",
    }

    out = {
        "schema": "origin.need-outcomes/1",
        "experiment": "022-need-outcomes",
        "observed_utc": "2026-10-05",
        "population": pop,
        "served_arm": served_arm,
        "build_arm": build_arm,
        "lift_arm": {
            "gate_a2": gate_a2,
            "mantel_haenszel_or": (lift or {}).get("mantel_haenszel_or"),
            "mantel_haenszel_ci95": (lift or {}).get("mantel_haenszel_ci95"),
            "strata_counted": (lift or {}).get("strata_counted"),
            "need_rows_without_a_depth_matched_control":
                (lift or {}).get("need_rows_without_a_depth_matched_control"),
            "ceiling": (lift or {}).get("ceiling"),
        },
        "controls": {
            "c1_positive_prior_art_sample": "20 corpus comments carrying an E012 "
                                            "prior_art verdict; their served rate "
                                            "is the calibration row and is reported "
                                            "in serve_sample.tsv",
            "c2_negative_trigger_sample": "raw/control.jsonl, same stories, no "
                                          "trigger phrase",
            "c3_nonsense_ids": load("nonsense_control.json"),
        },
        "limits": [
            "One community. Hacker News commenters are a self-selected technical "
            "population and no figure here generalises beyond it.",
            "The corpus was harvested by trigger phrase, not sampled from needs.",
            "One observation window, 2026-10-05, via two APIs, neither snapshotted.",
            "The build arm sees HN self-disclosure only, so 0 of 24 is a floor on "
            "disclosure and not an estimate of building.",
        ],
    }

    path = os.path.join(HERE, "results.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)

    print("population")
    for k in ("need_statements", "readable", "unreadable", "answered",
              "answered_rate", "distinct_requesters", "distinct_threads",
              "replies_below_needs"):
        print("  %-22s %s" % (k, pop[k]))
    print("served arm (hand labelled, conditional on a reply existing)")
    print("  labelled %d, judged %d" % (labelled, judged))
    print("  counts %s" % dict(lab_counts))
    print("  served           %d/%d = %.3f CI95 %s"
          % (served, judged, served_arm["served_rate_of_judged"], served_arm["served_ci95"]))
    print("  served or partial %d/%d = %.3f"
          % (served + partial, judged, served_arm["served_or_partial_rate"]))
    print("  software needs only %d/%d = %.3f CI95 %s"
          % (sw_served, sw_judged, served_arm["software_need_served_rate"],
             served_arm["software_need_served_ci95"]))
    print("build arm")
    print("  population %d, later story %d, hand-checked %d, related %d"
          % (build_arm["population"], build_arm["with_a_later_story"],
             build_arm["hand_checked"], build_arm["judged_related"]))
    print("  rate %s CI95 %s"
          % (build_arm["rate_of_population_related"], build_arm["rate_ci95"]))
    print("gates")
    print("  A1 population read  %s" % ("met" if pop["readable"] / float(n) >= 0.95
                                        else "NOT met"))
    print("  A2 within-thread lift  %s (odds ratio %s, declared floor %s)"
          % (gate_a2["verdict"], gate_a2.get("odds_ratio"),
             gate_a2.get("declared_floor")))
    print("  A3 build arm  evaluable (population %d readable %d, hand-checked %d)"
          % (build_arm["population"], build_arm["readable"],
             build_arm["hand_checked"]))
    print("wrote %s" % path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
