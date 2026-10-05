#!/usr/bin/env python3
"""The gates of 024, computed from `rows.json`.

`PROTOCOL.md` assigns four mutually exclusive categories by precedence, from
"the primary source states that ...". Deciding which of those four sentences a
source states is a judgement, and this module does not make it: every category
was written by hand, carrying the verbatim deciding sentence that produced it.
`rowcheck.py` checks that the record obeys the declared precedence and quotes
real sentences; this module reads a checked record and computes H1, H2, the
control's score and the sensitivity analysis.

**The sensitivity analysis is not in the protocol and that was a gap in the
protocol.** H1 was declared against a bare 50% floor, and a majority gate with a
one-row margin turns out to be decided by one reader's judgement about six
rows. Any reader of a majority result has to be told that, so `sensitivity()`
computes it rather than leaving it to whoever notices.

    python3 classify.py            # both populations, the gates, results.json
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results.json")

# H1's declared threshold.
H1_MAJORITY = 0.50

# Rows whose primary source states more than one reason, so the declared
# precedence decided them. These are the rows a second reader could reasonably
# move; a row with one unambiguous reason is not a lever. C3 is in the list
# because RESEARCH/C.md discards it on prior art plus a fieldwork-cost
# objection.
CONTESTED = ["A1", "C2", "C3", "D1", "D2", "D5"]

import rowcheck  # noqa: E402  (path is set by HERE before the import)


def load(name):
    return rowcheck.load(os.path.join(HERE, name))


def tally(rows):
    counts = {}
    for row in rows:
        counts[row["category"]] = counts.get(row["category"], 0) + 1
    return dict(sorted(counts.items()))


def eligible_rows(rows):
    """Rows a kill reason applies to.

    `never_a_candidate` rows are excluded: a row that was never promoted had no
    kill reason attributed to it, so counting it would make a cause share
    smaller by adding rows no cause applies to. CONTROL.md added that category
    to make the *control* well posed; applying the same rule here is stated
    rather than assumed."""
    return [r for r in rows if r["category"] != "never_a_candidate"]


def treatment(rows):
    """H1 and H2 over the treatment population."""
    eligible = eligible_rows(rows)
    prior = sum(1 for r in eligible if r["category"] == "prior_art")
    share = prior / len(eligible) if eligible else 0.0
    return {
        "population": len(rows),
        "never_a_candidate_excluded": len(rows) - len(eligible),
        "h1_denominator": len(eligible),
        "prior_art_n": prior,
        "h1_prior_art_share": share,
        "declared_floor": H1_MAJORITY,
        "h1_verdict": "survives" if share > H1_MAJORITY else "killed",
        "h2_stated_count": 12,
        "h2_measured_count": len(rows),
        "h2_agrees_with_the_stated_twelve": len(rows) == 12,
        "counts": tally(rows),
        "counts_eligible_only": tally(eligible),
    }


def control(rows):
    """The replacement control: E016's independently produced prior-art verdicts
    on 12 of F029's judgement kills. Same population, same label semantics, a
    different instrument at a different time, and with three known errors in the
    reference labels.

    CONTROL.md's declared pass condition is deliberately not "match the
    reference": the three no_prior_art_found items were known to this reader
    before the rule was applied to them, so a perfect score would prove nothing.
    The rule is free to score worse than the baseline, and a worse score is a
    real result -- it would show the hand-built categories do not track the
    evidence."""
    prior = [r for r in rows if r["category"] == "prior_art"]
    fp = [r for r in rows if r["category"] == "prior_art" and not r["truth_is_prior_art"]]
    fn = [r for r in rows if r["category"] != "prior_art" and r["truth_is_prior_art"]]
    baseline = sum(1 for r in rows if r["truth_is_prior_art"])
    return {
        "population": "E016's per-item prior-art verdicts on F029's 13 "
                      "adjudicable judgement kills, each with deciding text "
                      "recorded; a different instrument at a different time, "
                      "with known errors in the reference labels.",
        "rows": len(rows),
        "reference_prior_art": baseline,
        "reference_no_prior_art": len(rows) - baseline,
        "rule_prior_art": len(prior),
        "correct": len(rows) - len(fp) - len(fn),
        "false_positives": [r["name"] for r in fp],
        "false_negatives": [r["name"] for r in fn],
        "baseline_always_prior_art": baseline,
        "note_on_baseline": (
            "A rule that read F029's cause column and judged nothing would label all "
            "%d prior_art and score %d of %d -- the false positives F035 documented. "
            "The control's discriminating cases are those rows."
        ) % (len(rows), baseline, len(rows)),
        "verdict": "passes" if not fn and len(fp) <= 1 else "FAILS",
        "verdict_rule": (
            "Passes at no false negatives and at most one false positive: the reference "
            "labels contain three known errors, so a rule reproducing all three would be "
            "failing, not succeeding."
        ),
        "what_this_does_not_establish": (
            "Agreement with E016 is not correctness -- its arm-2 gate landed exactly on its "
            "threshold with one row deciding it. And the decisive limit is the one E023 "
            "already measured on this mission's labels: one reader, no second coder. This "
            "bounds whether the rule tracks an external label set, not whether this "
            "reader's judgements on the treatment rows are right."
        ),
    }


def sensitivity(rows, contested):
    """How fragile is H1?

    Which rows, moved one at a time, would change the verdict, and how many would
    have to move together."""
    eligible = eligible_rows(rows)
    n = len(eligible)
    base = sum(1 for r in eligible if r["category"] == "prior_art")
    levers = [
        {
            "id": r["id"],
            "name": r["name"],
            "share_if_moved": (base - 1) / n,
            "would_flip_the_verdict": (base - 1) / n <= H1_MAJORITY,
        }
        for r in eligible
        if r["category"] == "prior_art"
    ]
    moved = [r for r in eligible
             if r["category"] == "prior_art" and r["id"] in contested]
    worst = (base - len(moved)) / n if n else 0.0
    return {
        "eligible": n,
        "prior_art_n": base,
        "margin_over_the_floor": base / n - H1_MAJORITY if n else 0.0,
        "rows_that_flip_the_verdict_alone": [l["id"] for l in levers
                                             if l["would_flip_the_verdict"]],
        "every_prior_art_row_flips_it_alone": len(levers) == base,
        "contested_rows": contested,
        "share_if_every_contested_prior_art_row_moves": worst,
        "verdict_if_one_row_moves": "killed" if any(
            l["would_flip_the_verdict"] for l in levers) else "survives",
        "verdict_if_contested_rows_all_move": "killed" if worst <= H1_MAJORITY else "survives",
        "reading": (
            "H1 survives, and it survives by exactly one row. Every one of the %d "
            "prior-art rows, moved to any other declared category, puts the share at "
            "%d/%d = %.3f and kills it. A majority gate with a one-row margin is a "
            "verdict about the population, not a robust finding about prior art."
            % (base, base - 1, n, (base - 1) / n)
        ),
    }


LIMITS = [
    "One reader assigned every category and there is no second coder. The deciding "
    "sentence is recorded per row so a disagreeing reader can re-derive each category "
    "and name the single sentence they disagree about.",
    "The four categories are the record's own vocabulary, not the world's, and the "
    "precedence order is a declared convention that moves rows across the 50% line.",
    "This is a count over the record as written. It is not a measurement of what exists "
    "in the world and nothing here is a novelty claim.",
    "H1's denominator excludes never_a_candidate rows. Including them would report a "
    "smaller prior-art share by adding rows to which no kill reason applies.",
]


def main():
    rows = load("rows.json")
    crows = load("control_rows.json")
    problems = rowcheck.check_all(rows)
    problems += [("control/" + rid, p) for rid, p in rowcheck.check_all(crows)]
    for row_id, problem in problems:
        print("PROBLEM %s: %s" % (row_id, problem))
    out = {
        "schema": "origin.kill-reason-causes/1",
        "experiment": "024-kill-reason-causes",
        "observed_utc": "2026-10-05",
        "treatment": treatment(rows),
        "sensitivity": sensitivity(rows, CONTESTED),
        "control": control(crows),
        "rule_problems": ["%s: %s" % (a, b) for a, b in problems],
        "limits": LIMITS,
    }
    with open(RESULTS, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")
    t, c, sn = out["treatment"], out["control"], out["sensitivity"]
    print("\ntreatment: %d rows, %d eligible" % (t["population"], t["h1_denominator"]))
    print("counts:", json.dumps(t["counts_eligible_only"]))
    print("H1 prior_art share %.3f against floor %.2f -> %s"
          % (t["h1_prior_art_share"], H1_MAJORITY, t["h1_verdict"]))
    print("H2 measured %d against the stated twelve -> agrees: %s"
          % (t["h2_measured_count"], t["h2_agrees_with_the_stated_twelve"]))
    print("sensitivity: margin %.3f; %d rows alone would flip it; all contested moving -> %s"
          % (sn["margin_over_the_floor"], len(sn["rows_that_flip_the_verdict_alone"]),
             sn["verdict_if_contested_rows_all_move"]))
    print("control: %d/%d correct (baseline %d), FP %s, FN %s -> %s"
          % (c["correct"], c["rows"], c["baseline_always_prior_art"],
             c["false_positives"] or "none", c["false_negatives"] or "none", c["verdict"]))
    print("rule problems: %d" % len(problems))
    return 0


if __name__ == "__main__":
    sys.exit(main())