#!/usr/bin/env python3
"""E025 -- stats. Every figure written to results.json comes from the raw
captures and from this file, never from memory.

Protocol: EXPERIMENTS/025-need-staters-builderhood/PROTOCOL.md
"""
import json
import math
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(ROOT, "raw")


def load(name):
    path = os.path.join(RAW, name)
    rows = {}
    if not os.path.exists(path):
        return rows
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except ValueError:
                continue
            # Later rows for an author are fresher (e.g. footprint filled in).
            rows[d["author"]] = d
    return rows


def wilson(k, n, z=1.96):
    """Wilson score interval. Used because every arm is small enough that the
    normal approximation misbehaves near 0."""
    if n == 0:
        return (None, None, None)
    p = float(k) / n
    denom = 1.0 + z * z / n
    centre = (p + z * z / (2.0 * n)) / denom
    half = (z * math.sqrt(p * (1 - p) / n + z * z / (4.0 * n * n))) / denom
    return (p, max(0.0, centre - half), min(1.0, centre + half))


def arm_stats(rows, label):
    """A row counts only when the fetch succeeded. A refusal is never a zero."""
    ok = {a: r for a, r in rows.items() if r.get("status") == "ok"
          and r.get("nb_show_hn") is not None}
    refused = [a for a, r in rows.items() if r.get("status") != "ok"]
    builders = [a for a, r in ok.items() if r["nb_show_hn"] > 0]
    n = len(ok)
    k = len(builders)
    p, lo, hi = wilson(k, n)
    return {
        "arm": label,
        "authors_fetched_ok": n,
        "authors_refused": len(refused),
        "refused_authors": sorted(refused)[:20],
        "authors_with_at_least_one_show_hn": k,
        "raw_rate": round(p, 6) if p is not None else None,
        "ci95_low": round(lo, 6) if lo is not None else None,
        "ci95_high": round(hi, 6) if hi is not None else None,
    }


def overlap(a, b):
    if a["ci95_low"] is None or b["ci95_low"] is None:
        return None
    return not (a["ci95_high"] < b["ci95_low"] or b["ci95_high"] < a["ci95_low"])


def main():
    controls = load("gate_a1_controls.jsonl")
    verified = ["olalonde", "keepamovin", "byran", "jart", "mikemcquaid", "erohead"]
    original = ["pg", "patio11", "chromium", "antirez"]

    gate_a1 = {
        "question": "is the show_hn tag recoverable: 6 of 6 verified positives, and 0 for a nonsense account",
        "threshold": ">= 6 of 6 verified positives, and nonsense == 0",
        "verified_positive_control_members": verified,
        "original_believed_positive_controls": original,
        "detail": [
            {"author": a, "nb_show_hn": controls.get(a, {}).get("nb_show_hn"),
             "group": "verified_positive"}
            for a in verified
        ] + [
            {"author": a, "nb_show_hn": controls.get(a, {}).get("nb_show_hn"),
             "group": "original_believed_positive",
             "note": "kept with its 0; see the Gate A1 correction in PROTOCOL.md"}
            for a in original
        ] + [
            {"author": "zzqqxxnonsensecontrol",
             "nb_show_hn": controls.get("zzqqxxnonsensecontrol", {}).get("nb_show_hn"),
             "group": "nonsense"}
        ],
    }
    recovered = sum(1 for a in verified
                    if (controls.get(a, {}).get("nb_show_hn") or 0) > 0)
    nonsense = controls.get("zzqqxxnonsensecontrol", {}).get("nb_show_hn")
    gate_a1["recovered"] = recovered
    gate_a1["nonsense_value"] = nonsense
    gate_a1["met"] = bool(recovered == 6 and nonsense == 0)

    need = arm_stats(load("need_arm.jsonl"), "need")
    ctrl = arm_stats(load("control_arm.jsonl"), "control")

    ratio = None
    if need["raw_rate"] is not None and ctrl["raw_rate"]:
        ratio = need["raw_rate"] / ctrl["raw_rate"]

    overlapping = overlap(need, ctrl)

    gate_a2 = {
        "question": "is the need arm's show_hn rate at least 2x the control arm's, with non-overlapping Wilson intervals",
        "threshold": ">= 2x ratio AND intervals do not overlap",
        "ratio": round(ratio, 4) if ratio is not None else None,
        "intervals_overlap": overlapping,
        "met": bool(ratio is not None and ratio >= 2.0 and overlapping is False),
        "reading": "H1 survives: need-staters announce at an ordinary-or-higher rate, so the corpus is not closed by the disclosure floor E022 declared.",
    }
    gate_b1 = {
        "question": "do the two arms' intervals overlap",
        "threshold": "overlapping intervals kill H1 and confirm W1",
        "met": bool(overlapping is True),
        "reading": "H1 fails: the need arm is not distinguishable from ordinary commenters in the same stories.",
    }
    gate_c1 = {
        "question": "is the need arm's raw rate below 5%, which makes 'who builds' not evaluable and leaves only the null",
        "threshold": "< 0.05 -> not_evaluated for who builds",
        "need_arm_raw_rate": need["raw_rate"],
        "met": bool(need["raw_rate"] is not None and need["raw_rate"] < 0.05),
    }

    if not gate_a1["met"]:
        verdict = "instrument_invalid"
    elif gate_c1["met"]:
        verdict = "not_evaluated"
    elif gate_a2["met"]:
        verdict = "h1_survives"
    else:
        verdict = "h1_fails"

    # The confounder, reported rather than corrected: HN selects heavy posters
    # into show_hn because they post at all. Both arms carry it.
    footprint = {}
    for label, name in (("need", "need_arm.jsonl"), ("control", "control_arm.jsonl")):
        rows = load(name)
        pairs = [(r.get("total_items_by_author"), r.get("nb_show_hn"))
                 for r in rows.values()
                 if r.get("total_items_by_author") is not None
                 and r.get("nb_show_hn") is not None]
        if pairs:
            builders = [t for t, s in pairs if s > 0]
            others = [t for t, s in pairs if s == 0]
            footprint[label] = {
                "authors_with_a_footprint_sample": len(pairs),
                "median_total_items_builders": sorted(builders)[len(builders) // 2] if builders else None,
                "median_total_items_non_builders": sorted(others)[len(others) // 2] if others else None,
            }

    results = {
        "schema": "origin.need-staters-builderhood/1",
        "experiment": "025-need-staters-builderhood",
        "observed_utc": "2026-10-05",
        "computed_by": "stats.py from raw/*.jsonl",
        "instrument": {
            "source": "Hacker News Algolia index, https://hn.algolia.com/api/v1/search",
            "query": "tags=author_<name>,show_hn&hitsPerPage=1",
            "count_read": "nbHits",
            "what_it_is": "a floor on public disclosure of having shipped something on HN",
            "what_it_is_not": "a rate of building. It cannot see a build that was never announced, and it says nothing about whether what was built was good, used, or related to the stated need.",
        },
        "arms": {"need": need, "control": ctrl},
        "gates": {"gate_a1": gate_a1, "gate_a2": gate_a2, "gate_b1": gate_b1, "gate_c1": gate_c1},
        "confounder_not_corrected": {
            "description": "HN assigns show_hn to people who post; heavy posters are selected into it. Both arms are exposed identically, which is why the control arm is drawn from the same stories rather than from HN at large.",
            "footprint_sample": footprint,
        },
        "verdict": verdict,
        "limits": [
            "The show_hn tag is set by HN, not by the author. Any positive reading is a lower bound on disclosure, and E022's arm had the same floor, so this does not measure what E022 could not.",
            "One platform and one announcement channel. A builder who ships without announcing on HN is invisible here, in both arms.",
            "The arms differ in when their members were active: the need corpus spans 2024-01-01 onward, the control comments are drawn from the same stories in the same window, so the window is shared but the population is not matched on tenure.",
            "This measures whether need-staters and ordinary commenters differ in announcing. It does not measure whether any candidate exists, and it reopens no prior-art death.",
            "Gate A1's original control set was wrong (two of four were not positive controls at all). The correction is recorded in PROTOCOL.md and README.md; the instrument recovered the tag correctly throughout.",
        ],
    }

    with open(os.path.join(ROOT, "results.json"), "w") as f:
        json.dump(results, f, indent=1, sort_keys=True)
        f.write("\n")
    print(json.dumps(results, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
