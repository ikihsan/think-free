#!/usr/bin/env python3
"""E067 view-count measurement framework — core engine.

Reads a need statement corpus in E062 arm1.jsonl format and computes the
full view_count measurement suite: G1 reconciliation, G4 age gradient,
state distribution, unremedied arrival, unremedied shape, and by-site
breakdown.

Writes outcome.json-compatible results.
"""

import collections
import json
import os
import sys
from datetime import datetime

from classify import classify_need

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def pct(a, b):
    """Percentage a/b, returning 0.0 when b is 0."""
    return 0.0 if not b else 100.0 * a / b


def parse_date(raw):
    """Convert a unix-timestamp field to a float years-from-now, or None."""
    if raw is None or raw == 0:
        return None
    try:
        return (datetime.now().timestamp() - float(raw)) / (365.25 * 86400)
    except (ValueError, TypeError):
        return None


def _state(r):
    """Return the platform state of a row: 'accepted', 'answered', 'closed', 'open'."""
    if r.get("accepted_answer_id"):
        return "accepted"
    if r.get("is_answered"):
        return "answered"
    if r.get("closed_reason"):
        return "closed"
    return "open"


def _top_row_unanswered_years(openr):
    """Years the top unremedied row has been open, or None."""
    dates = [parse_date(r.get("creation_date")) for r in openr if parse_date(r.get("creation_date")) is not None]
    if not dates:
        return None
    return round((max(dates) - min(dates)) / (365.25 * 86400), 1) if len(dates) > 1 else None


def process_corpus(input_path):
    """Process a corpus and return the outcome dict."""
    rows = [json.loads(l) for l in open(input_path, "r", encoding="utf-8") if l.strip()]

    # --- G1 reconciliation (partial: rows-level) ---
    sites = sorted(set(r["_site"] for r in rows))
    rows_with_body = sum(1 for r in rows if r.get("body"))
    rows_with_outcome_fields = sum(
        1 for r in rows if "is_answered" in r and "closed_reason" in r
    )

    # --- G4 age gradient ---
    cohorts = []
    for lo, hi, label in ((0, 2, "<2y"), (2, 5, "2-5y"),
                          (5, 10, "5-10y"), (10, 999, ">10y")):
        sel = [r for r in rows
               if lo <= (parse_date(r.get("creation_date")) or 0) < hi]
        if not sel:
            continue
        n = len(sel)
        open_pct = pct(
            sum(1 for r in sel if _state(r) == "open"), n
        )
        accepted_pct = pct(
            sum(1 for r in sel if _state(r) == "accepted"), n
        )
        cohorts.append({
            "cohort": label, "n": n,
            "open_pct": round(open_pct, 1),
            "accepted_pct": round(accepted_pct, 1),
        })
    opens = [c["open_pct"] for c in cohorts]
    max_gap_points = round(max(opens) - min(opens), 1) if opens else None
    meets_10_point_gate = (max_gap_points >= 10.0) if max_gap_points is not None else None
    monotone = opens == sorted(opens) if opens else None

    # --- State distribution ---
    STATES = ("accepted", "answered", "closed", "open")
    by_state = []
    for s in STATES:
        v = sorted(r.get("view_count", 0) for r in rows if _state(r) == s)
        if not v:
            continue
        by_state.append({
            "state": s, "n": len(v),
            "median_views": v[len(v) // 2],
            "p90_views": v[int(0.9 * len(v))],
            "max_views": v[-1],
            "share_pct": round(pct(len(v), len(rows)), 1),
        })

    # --- Unremedied arrival ---
    open_rows = [r for r in rows if _state(r) == "open"]
    openr = sorted(open_rows, key=lambda r: -r.get("view_count", 0))
    open_views_total = sum(r.get("view_count", 0) for r in openr)
    total_views_all = sum(r.get("view_count", 0) for r in rows)  # all rows
    conc = {}
    for frac in (0.05, 0.10, 0.25):
        k = max(1, int(round(frac * len(openr))))
        conc[f"top_{int(frac * 100)}_pct"] = {
            "rows": k,
            "share_of_unremedied_views_pct": round(pct(
                sum(r.get("view_count", 0) for r in openr[:k]), open_views_total), 1),
        }
    unremedied_arrival = {
        "n": len(openr),
        "views_total": open_views_total,  # sum of open rows' views only
        "share_of_all_views_pct": round(pct(open_views_total, total_views_all), 1) if rows else 0,
        "median_views": sorted(r.get("view_count", 0) for r in openr)[len(openr) // 2] if openr else 0,
        "top_row_views": openr[0]["view_count"] if openr else 0,
        "top_row_title": openr[0].get("title", "") if openr else "",
        "top_row_unanswered_years": _top_row_unanswered_years(openr),
        "concentration": conc,
    }

    # --- Unremedied shape ---
    cls = collections.Counter(classify_need(r.get("title", "")) for r in openr)
    unremedied_shape = {
        "n": len(openr),
        "classes": dict(cls.most_common()),
        "by_site": dict(collections.Counter(r.get("_site", "unknown") for r in openr).most_common()),
    }

    # --- Build output ---
    outcome = {
        "g1": {
            "rows": len(rows),
            "sites": sites,
            "rows_with_body": rows_with_body,
            "rows_with_outcome_fields": rows_with_outcome_fields,
        },
        "g4": {
            "cohorts": cohorts,
            "max_gap_points": max_gap_points,
            "meets_10_point_gate": meets_10_point_gate,
            "monotone": monotone,
        },
        "state_distribution": by_state,
        "unremedied_arrival": unremedied_arrival,
        "unremedied_shape": unremedied_shape,
    }

    return outcome


def main():
    """Entry point when run as: python3 -m viewcount process|classify|report."""
    if len(sys.argv) < 3:
        print("Usage: python3 -m viewcount <process|classify|report> [args]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "process":
        if len(sys.argv) < 5:
            print("Usage: python3 -m viewcount process --input <path> --output <path>")
            sys.exit(1)
        input_path = None
        output_path = None
        args = sys.argv[2:]
        i = 0
        while i < len(args):
            if args[i] == "--input" and i + 1 < len(args):
                input_path = args[i + 1]
                i += 2
            elif args[i] == "--output" and i + 1 < len(args):
                output_path = args[i + 1]
                i += 2
            else:
                i += 1
        if not input_path or not output_path:
            print("Missing --input or --output")
            sys.exit(1)
        outcome = process_corpus(input_path)
        with open(output_path, "w", encoding="utf-8") as fh:
            json.dump(outcome, fh, indent=2, sort_keys=True)
            fh.write("\n")
        print(f"Wrote {output_path}")
        print(f"  G1 rows={outcome['g1']['rows']} sites={len(outcome['g1']['sites'])}")
        print(f"  G4 cohorts={len(outcome['g4']['cohorts'])} max_gap={outcome['g4']['max_gap_points']}pt gate={outcome['g4']['meets_10_point_gate']}")
        print(f"  Unremedied n={outcome['unremedied_arrival']['n']} views_total={outcome['unremedied_arrival']['views_total']}")

    elif command == "classify":
        title = sys.argv[2] if len(sys.argv) > 2 else ""
        print(classify_need(title))

    elif command == "report":
        output_path = sys.argv[2] if len(sys.argv) > 2 else None
        if output_path:
            outcome = json.load(open(output_path, "r", encoding="utf-8"))
        else:
            # try to find outcome.json in cwd
            outcome = None
            for p in ["outcome.json", "../outcome.json", "../../outcome.json"]:
                if os.path.exists(p):
                    outcome = json.load(open(p, "r", encoding="utf-8"))
                    break
            if outcome is None:
                print("No outcome.json found")
                sys.exit(1)
        _report(outcome)

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


def _report(outcome):
    """Print a human-readable summary matching E062 outcome.py format."""
    g1 = outcome["g1"]
    g4 = outcome["g4"]
    ua = outcome["unremedied_arrival"]

    print(f"G1  rows={g1['rows']} sites={len(g1['sites'])} api_items={g1.get('items_declared_by_api', 'n/a')} all_200={g1.get('requests_all_200', 'n/a')}")
    print(f"G4  still-open share by age cohort:")
    for c in g4["cohorts"]:
        print(f"      %-6s n=%4d open %5.1f%%  accepted %5.1f%%" % (c["cohort"], c["n"], c["open_pct"], c["accepted_pct"]))
    print(f"      max gap %.1f points, gate(>=10)=%s, monotone=%s" % (g4["max_gap_points"], "PASS" if g4["meets_10_point_gate"] else "FAIL", "yes" if g4["monotone"] else "no"))
    print(f"state distribution:")
    # state_distribution is at the top level of the outcome dict
    if "state_distribution" in outcome:
        for s in outcome["state_distribution"]:
            print("      %-9s n=%4d (%4.1f%%)  views median %6d p90 %7d max %8d" % (s["state"], s["n"], s["share_pct"], s["median_views"], s["p90_views"], s["max_views"]))
    else:
        print("  (no state distribution)")
    print(f"unremedied arrival (n={ua['n']}): %.1f%% of all views, median %d views; top row %d views unanswered %.1fy" % (
        ua["share_of_all_views_pct"], ua["median_views"], ua["top_row_views"], ua["top_row_unanswered_years"]))
    for k, v in sorted(ua["concentration"].items()):
        print("      %s of unremedied rows carry %s%% of ALL views" % (k, v["share_of_unremedied_views_pct"]))
    print(f"shape of the {ua['n']} no-remedy rows (all classified, see tsv):")
    # classes are in unremedied_shape
    us = outcome["unremedied_shape"]
    classes = us.get("classes", {})
    for k, v in sorted(classes.items(), key=lambda x: -x[1]):
        print("      %-24s %3d  %5.1f%%" % (k, v, pct(v, ua["n"])))