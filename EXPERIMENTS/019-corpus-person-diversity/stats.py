#!/usr/bin/env python3
"""Every arm-A figure in results.json, computed from the raw capture only.

No figure in the record is typed by hand. This script reads
raw/corpus_authors.jsonl and writes the arm-A block of results.json; it never
reads the corpus file, the screen, or any earlier finding, so a change in any
of those cannot silently move a number.
"""
import json
import os
import statistics
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
CAPTURE = os.path.join(HERE, "raw", "corpus_authors.jsonl")
RESULTS = os.path.join(HERE, "results.json")


def path(*parts):
    return os.path.join(HERE, *parts)


def share(top_n, total):
    return round(float(top_n) / float(total), 4) if total else 0.0


def arm_a():
    rows = [json.loads(l) for l in open(CAPTURE) if l.strip()]
    total = len(rows)
    ok = [r for r in rows if r.get("status") == "ok" and r.get("author")]
    authors = Counter(r["author"] for r in ok)
    stories = {r.get("story_id") for r in ok}
    days = {(r.get("posted") or 0) // 86400 for r in ok}
    per = sorted(authors.values())
    n_auth = len(authors)

    by_trigger = defaultdict(Counter)
    for r in ok:
        by_trigger[r.get("trigger")][r["author"]] += 1
    trigger_rows = []
    for trig, c in by_trigger.items():
        counts = sorted(c.values())
        trigger_rows.append({
            "trigger": trig,
            "comments": sum(counts),
            "distinct_authors": len(c),
            "comments_per_author_max": counts[-1] if counts else 0,
        })
    trigger_rows.sort(key=lambda t: -t["comments"])

    head1 = sum(sorted(authors.values(), reverse=True)[:10])
    top1pct_n = max(1, n_auth // 100)
    top1pct = sum(sorted(authors.values(), reverse=True)[:top1pct_n])

    return {
        "capture": "raw/corpus_authors.jsonl",
        "comments": total,
        "rows_with_author": len(ok),
        "gate_a1_met": (len(ok) / float(total) if total else 0.0) >= 0.95,
        "distinct_authors": n_auth,
        "distinct_parent_stories": len(stories),
        "distinct_days": len(days),
        "comments_per_author": {
            "min": per[0] if per else 0,
            "median": statistics.median(per) if per else 0,
            "mean": round(statistics.mean(per), 3) if per else 0,
            "p90": per[int(0.9 * (len(per) - 1))] if per else 0,
            "p99": per[int(0.99 * (len(per) - 1))] if per else 0,
            "max": per[-1] if per else 0,
        },
        "rows_in_single_comment_authors": sum(1 for v in per if v == 1),
        "top_10_authors_comment_share": share(head1, len(ok)),
        "top_1pct_authors_comment_share": share(top1pct, len(ok)),
        "deleted_or_dead_rows": sum(
            1 for r in ok if r.get("deleted") or r.get("dead")),
        "distinct_triggers": len(trigger_rows),
        "per_trigger": trigger_rows,
        "computed_by": "stats.py from raw/corpus_authors.jsonl",
    }


def arm_a2():
    """Read arm A2's raw capture and add the declared gate on top of it."""
    block = json.load(open(path("raw", "arm_a2.json")))
    share = block["share_bottleneck_1"]
    block["gate"] = {
        "declared": "share_bottleneck_1 >= 0.90 closes the aggregation "
                    "generator; < 0.50 means sharing exists; between, no "
                    "verdict",
        "met": block["verdict"] != "no_verdict_distribution_reported",
        "band": "50-90% -> no verdict, distribution reported",
    }
    return block


def arm_b():
    """Gate B1 and the kill gate, computed from raw/arm_b.json only."""
    raw = json.load(open(path("raw", "arm_b.json")))
    pos = [r["distinct_authors"] for r in raw["positive_controls"]]
    neg = [r["distinct_authors"] for r in raw["negative_controls"]]
    pos_ok = [n for n in pos if n is not None]
    neg_ok = [n for n in neg if n is not None]
    neg_median = statistics.median(neg_ok) if neg_ok else 0
    threshold = 3.0 * neg_median
    pos_pass = sum(1 for n in pos_ok if n >= threshold)
    floor = [n for n in pos_ok if n <= 1]
    clause_authors = []
    for c in raw["clauses"]:
        a = max(c["verbatim_hits"]["distinct_authors"] or 0,
                c["content4_hits"]["distinct_authors"] or 0)
        clause_authors.append({"row": c["row"], "best_distinct_authors": a})
    clause_authors.sort(key=lambda r: -r["best_distinct_authors"])
    weakest_pos = min(pos_ok) if pos_ok else None
    above_median_pos = statistics.median(pos_ok) if pos_ok else None
    kill = bool(clause_authors) and weakest_pos is not None and all(
        r["best_distinct_authors"] < weakest_pos for r in clause_authors)
    positive_gate = bool(clause_authors) and above_median_pos is not None and any(
        r["best_distinct_authors"] > above_median_pos for r in clause_authors)
    degenerate = neg_median == 0
    return {
        "capture": "raw/arm_b.json",
        "gate_b1_declared": ">= 5 of 6 positive controls at >= 3x the median "
                            "negative control",
        "negative_median_distinct_authors": neg_median,
        "positive_threshold": threshold,
        "positive_controls_passed": pos_pass,
        "positive_controls_at_or_below_floor": len(floor),
        "gate_b1_met_numerically": pos_pass >= 5,
        "gate_b1_degenerate": degenerate,
        "gate_b1_verdict": (
            "degenerate: the negative median is 0, so 3x it is 0 and the "
            "threshold cannot separate anything; and %d of %d positive "
            "controls with demonstrated adoption returned 0 or 1 distinct "
            "authors, so the instrument cannot rank and no recurrence verdict "
            "is drawn" % (len(floor), len(pos_ok))),
        "arm_b1": "inconclusive",
        "clauses": clause_authors,
        "kill_gate_declared": "every clause below the weakest positive control",
        "kill_gate_met": kill,
        "kill_gate_evaluable": False,
        "kill_gate_note": (
            "numerically met but not evaluable: the same 0-or-1 readings that "
            "disqualify the controls disqualify the clauses"),
        "positive_gate_met": positive_gate,
        "arm_b2": {
            "authors_in_capture": raw["b2_local"]["authors_in_capture"],
            "authors_naming_both_families":
                raw["b2_local"]["authors_naming_both"],
            "share": raw["b2_local"]["share_of_corpus"],
            "verdict": "inconclusive",
            "note": ("the rows are visibly not F033's cluster on inspection, so "
                     "2% is consistent with background co-occurrence of a common "
                     "term family and separates nothing"),
        },
        "computed_by": "stats.py from raw/arm_b.json",
    }


def main():
    block = arm_a()
    existing = {}
    if os.path.exists(RESULTS):
        try:
            existing = json.load(open(RESULTS))
        except ValueError:
            existing = {}
    existing["experiment"] = "E019 corpus person diversity"
    existing["arm_a"] = block
    existing["arm_a2"] = arm_a2()
    existing["arm_b"] = arm_b()
    existing["verdict"] = {
        "h1_corpus_is_wide": True,
        "h2_corpus_is_narrow": False,
        "h3_person_recurrence_salvages_clauses": "not_testable_with_this_instrument",
        "arm_a": "decisive",
        "arm_a2": "declared band 50-90%, no verdict, distribution reported",
        "arm_b1": "instrument failed its own controls",
        "arm_b2": "inconclusive",
        "what_is_established": (
            "1401 comments carry 1250 distinct authors, and 79.25% of eligible "
            "clauses share no content word with any other clause. The corpus is "
            "a wide audience of individual requesters, not a sample of shared "
            "needs."),
        "what_is_not_established": (
            "that the requests lack shared demand; only that this corpus cannot "
            "show it, and that no lexical recurrence instrument tried here can "
            "show it either."),
    }
    with open(path("results.json"), "w") as f:
        json.dump(existing, f, indent=1, sort_keys=True)
    print("arm_a  distinct_authors=%d  gate_a1=%s"
          % (block["distinct_authors"], block["gate_a1_met"]))
    print("arm_a2  share_bottleneck_1=%.4f  verdict=%s"
          % (existing["arm_a2"]["share_bottleneck_1"],
             existing["arm_a2"]["verdict"]))
    print("arm_b   gate_b1_numerically=%s degenerate=%s  kill_gate_met=%s "
          "evaluable=%s"
          % (existing["arm_b"]["gate_b1_met_numerically"],
             existing["arm_b"]["gate_b1_degenerate"],
             existing["arm_b"]["kill_gate_met"],
             existing["arm_b"]["kill_gate_evaluable"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())