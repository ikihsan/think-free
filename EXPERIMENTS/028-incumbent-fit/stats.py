#!/usr/bin/env python3
"""E028: reader agreement, controls, the declared gates, and the verdict.

Every gate in PROTOCOL.md is computed here and printed, including the ones that
fire. Nothing is omitted because it was inconvenient. The arithmetic lives in
`fitstats.py`.
"""
import json
import os

import fitstats
from fitstats import agreement_note, cohen_kappa, lexical_summary, wilson

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
LABELS = ("serves", "partial", "does_not_serve", "unreadable",
          "no_distinguishing_attribute")
READERS = ("r1", "r2")


def load():
    facts = {r["row"]: r for r in fitstats.read_jsonl(
        os.path.join(RAW, "record_facts.json"))}
    step_a = {r["row"]: r for r in fitstats.read_jsonl(
        os.path.join(RAW, "step_a_r1.jsonl"))}
    readers = {}
    for r in READERS:
        rows = {}
        for b in (1, 2):
            for rec in fitstats.read_jsonl(os.path.join(
                    RAW, "step_b_%s_batch%d.jsonl" % (r, b))):
                rows[(rec["row"], rec["pairing"])] = rec
        readers[r] = rows
    view = {}
    for r in READERS:
        with open(os.path.join(RAW, "view_b_%s.json" % r)) as fh:
            for e in json.load(fh)["view"]:
                view.setdefault(r, {})[(e["row"], e["pairing"])] = e
    return facts, step_a, readers, view


def step_a_agreement():
    sa1 = {r["row"]: r for r in fitstats.read_jsonl(
        os.path.join(RAW, "step_a_r1.jsonl"))}
    sa2 = {r["row"]: r for r in fitstats.read_jsonl(
        os.path.join(RAW, "step_a_r2.jsonl"))}
    cats = ("yes", "inferred", "none")
    a = [sa1[r]["attribute_stated"] for r in sorted(sa1)]
    b = [sa2[r]["attribute_stated"] for r in sorted(sa1)]
    return {
        "scheme": "attribute_stated in {yes, inferred, none}",
        "n": len(sa1),
        "agree": sum(1 for x, y in zip(a, b) if x == y),
        "kappa": cohen_kappa(a, b, cats),
        "conflicts": [{"row": r, "r1": sa1[r]["attribute"],
                       "r2": sa2[r]["attribute"]}
                      for r in sorted(sa1)
                      if sa1[r]["attribute_stated"]
                      != sa2[r]["attribute_stated"]],
        "attribute_stated_counts_r1": {c: sum(1 for x in a if x == c)
                                       for c in cats},
        "attribute_stated_counts_r2": {c: sum(1 for x in b if x == c)
                                       for c in cats},
    }


def controls(readers, mismatch_rows):
    c1 = {}
    for r in READERS:
        labs = [readers[r][(row, "mismatched_with")]["label"]
                for row in mismatch_rows]
        bad = [l for l in labs if l in ("serves", "partial")]
        c1[r] = {
            "n": len(labs),
            "not_serving": sum(1 for l in labs if l == "does_not_serve"),
            "refused_as_no_attribute": sum(1 for l in labs if l
                                           == "no_distinguishing_attribute"),
            "unreadable": sum(1 for l in labs if l == "unreadable"),
            "called_serving": len(bad),
            "rate_called_serving": (round(len(bad) / len(labs), 4)
                                    if labs else None),
            "detail": {row: readers[r][(row, "mismatched_with")]["label"]
                       for row in mismatch_rows},
        }
    return c1, {r: readers[r][("H03", "own")]["label"] for r in READERS}


def fit_population(readers, fit_rows):
    table = []
    for row in fit_rows:
        entry = {"row": row}
        for r in READERS:
            rec = readers[r][(row, "own")]
            entry["label_" + r] = rec["label"]
            entry["note_" + r] = rec["note"]
            entry["evidence_" + r] = rec.get("evidence")
        entry["agree"] = entry["label_r1"] == entry["label_r2"]
        table.append(entry)
    no_attr = sorted({row for row in fit_rows
                      if any(readers[r][(row, "own")]["label"]
                             == "no_distinguishing_attribute"
                             for r in READERS)})
    unread = sorted({row for row in fit_rows
                     if any(readers[r][(row, "own")]["label"] == "unreadable"
                            for r in READERS)})
    pop = [row for row in fit_rows if row not in no_attr and row not in unread]
    return table, pop, no_attr, unread


def counts_for(readers, pop):
    """Two aggregations, declared here because the protocol named neither.

    strict  a row is serving only if BOTH readers said serves
    either  a row is serving if EITHER reader said serves
    """
    def serves(row):
        return any(readers[r][(row, "own")]["label"] == "serves"
                   for r in READERS)

    def dsn(row):
        return all(readers[r][(row, "own")]["label"]
                   in ("does_not_serve", "no_distinguishing_attribute",
                       "unreadable") for r in READERS)

    sv = [row for row in pop if serves(row)]
    no = [row for row in pop if dsn(row)]
    both = [row for row in pop
            if all(readers[r][(row, "own")]["label"] == "serves"
                   for r in READERS)]
    out = {
        "fit_population": len(pop),
        "serves": len(sv), "serves_ci95": wilson(len(sv), len(pop)),
        "serves_rows": sv,
        "does_not_serve_by_both": len(no),
        "does_not_serve_by_both_ci95": wilson(len(no), len(pop)),
        "does_not_serve_rows": no,
    }
    both_n = len(both)
    return {"either": out,
            "strict": dict(out, serves=both_n, serves_rows=both,
                           serves_ci95=wilson(both_n, len(pop)))}


def decide(a1, a2, a4, b1, a3_lo, c2):
    if a4["fires"]:
        causes = []
        if a4["under_ten"]:
            causes.append("the fit population is under ten rows")
        if not a1["passes"]:
            causes.append("a declared control failed (C2, the positive "
                          "control, returned %r and %r)"
                          % (c2["r1"], c2["r2"]))
        if a4["kappa_identical_every_row"]:
            causes.append("both readers labelled every row identically")
        return "not_evaluated", "A4 fires: " + "; ".join(causes)
    if b1["fires"]:
        return ("prior_art_fits",
                "B1 fires: the incumbents the screens named do what the "
                "clauses asked for, at the recorded population")
    if a3_lo >= 0.20:
        return ("prior_art_does_not_fit",
                "A3 fires: both readers found no fit in at least a fifth of "
                "the fit population, with the Wilson lower bound at or above "
                "0.20")
    return ("inconclusive",
            "neither gate fired: the does_not_serve share's lower bound is "
            "below 0.20 and the serves share's lower bound is below 0.60")


def main():
    facts, step_a, readers, view = load()
    fit_rows = sorted({row for (row, p) in readers["r1"] if p == "own"})
    mismatch_rows = sorted({row for (row, p) in readers["r1"]
                            if p == "mismatched_with"})
    sa = step_a_agreement()
    c1, c2 = controls(readers, mismatch_rows)
    table, pop, no_attr, unread = fit_population(readers, fit_rows)
    counts = counts_for(readers, pop)

    k_both = cohen_kappa([readers["r1"][(row, "own")]["label"] for row in pop],
                         [readers["r2"][(row, "own")]["label"] for row in pop],
                         LABELS)

    c1_pass = all(c1[r]["rate_called_serving"] <= 0.10 for r in READERS)
    c2_pass = c2["r1"] == "serves" and c2["r2"] == "serves"
    a1 = {"c1_mismatched_control": c1_pass,
          "c2_positive_control_H03": c2_pass,
          "c2_labels": c2, "passes": c1_pass and c2_pass}
    a2 = {"declared_floor": 0.6, "kappa": k_both,
          "agrees_on": sum(1 for t in table if t["agree"]), "n": len(pop),
          "passes": (k_both is not None and k_both >= 0.6),
          "warning": agreement_note(k_both)}
    a3_lo = counts["strict"]["does_not_serve_by_both_ci95"][0]
    a4 = {"fit_population": len(pop), "under_ten": len(pop) < 10,
          "c1_c2_pass": a1["passes"],
          "kappa_identical_every_row": all(t["agree"] for t in table),
          "fires": (len(pop) < 10 or not a1["passes"]
                    or all(t["agree"] for t in table))}
    b1 = {"declared_floor": 0.60,
          "strict_serves": counts["strict"]["serves"],
          "strict_serves_ci95": counts["strict"]["serves_ci95"],
          "either_serves": counts["either"]["serves"],
          "either_serves_ci95": counts["either"]["serves_ci95"],
          "fires": counts["strict"]["serves_ci95"][0] >= 0.60}
    verdict, reason = decide(a1, a2, a4, b1, a3_lo, c2)

    for entry in table:
        entry["screen_verdict"] = facts[entry["row"]]["verdict"]
        entry["attribute"] = step_a[entry["row"]]["attribute"]
        entry["attribute_stated"] = step_a[entry["row"]]["attribute_stated"]

    out = {
        "schema": "origin.e028-incumbent-fit/1",
        "observed_utc": "2026-10-05",
        "population": {
            "declared": "every row whose declared kill category is prior_art "
                        "in E024 rows.json, plus every cause==prior_art row "
                        "in E012 screened.jsonl",
            "declared_total": 29,
            "arm1_harvest_rows": len(facts),
            "arm2_sealed_rows": 10,
            "arm2_executed": False,
            "arm2_reason": "declaration names the report prose each "
                           "requirement must be copied from; that extraction "
                           "is itself a labelling act and was not done in "
                           "this run rather than done after the harvest arm "
                           "reported a result",
            "fit_rows_naming_at_least_one_artifact": len(fit_rows),
            "rows_naming_no_artifact": len(facts) - len(fit_rows),
            "fit_population": len(pop),
            "excluded_no_distinguishing_attribute": no_attr,
            "excluded_unreadable": unread,
        },
        "step_a_agreement": sa,
        "controls": {"c1_mismatched": c1, "c2_positive_H03": c2},
        "fit_table": table,
        "counts": counts,
        "lexical_index": lexical_summary(view),
        "gates": {
            "a1_instrument": a1, "a2_agreement": a2,
            "a3_kill_does_not_serve_lower_bound_0_20": {
                "declared": 0.20,
                "does_not_serve_by_both":
                    counts["strict"]["does_not_serve_by_both"],
                "wilson_lower_bound": a3_lo, "fires": a3_lo >= 0.20},
            "b1_serves_lower_bound_0_60": b1, "a4_not_evaluated": a4},
        "verdict": verdict,
        "verdict_reason": reason,
        "limitations": [
            "One reader family. MISSION.md records that agents share model "
            "biases and are not independent human validation; kappa measures "
            "consistency between two passes of the same family.",
            "A row's serves label means at least one of the four artifacts "
            "the screen listed FIRST does the attribute. An artifact it listed "
            "fifth could serve and the row would still read does_not_serve. "
            "90 artifacts were named, 81 have stored documentation, and at "
            "most 4 per row were shown.",
            "Documentation was stored at 12,000 characters per artifact and "
            "shown at 1,800. A capability claim outside the head of a README "
            "is invisible here in both directions.",
            "The fit is tested against what the artifact's own documentation "
            "claims. It is not a test of whether the artifact works, and a "
            "documented silence is not a demonstrated absence of fit.",
            "19 of the 29 declared rows were measured. The ten sealed-report "
            "rows were not, and they are the rows that closed the mission's "
            "own candidates.",
            "Row H03 is both a population row and the declared positive "
            "control, so its recovery is not independent evidence about "
            "itself.",
        ],
    }
    with open(os.path.join(HERE, "results.json"), "w") as fh:
        json.dump(out, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(json.dumps({k: out[k] for k in
                      ("verdict", "verdict_reason", "gates", "counts",
                       "step_a_agreement", "lexical_index")}, indent=2))


if __name__ == "__main__":
    main()