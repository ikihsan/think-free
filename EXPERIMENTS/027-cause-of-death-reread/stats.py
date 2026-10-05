#!/usr/bin/env python3
"""Every number E027 reports, computed from the captures only.

Reads `raw/reader_r.jsonl`, `raw/reader_s.jsonl` and the committed E012
population, and writes `results.json`. Nothing below is typed from memory.

Three figures, in the order the protocol declares them:

  A1  population integrity
  B1  six-category Cohen's kappa, declared floor 0.6
  C1  the kill gate: convergent flips, where *both* readers independently put a
      row in a survivor-relevant category

and one clearly-labelled post-hoc figure, because the declared kappa turned out
to answer a question the gate does not ask: the six categories split into a
survivor-relevant group and a not-survivor-relevant group, and the gate is
declared over the group, not over the six labels. The post-hoc binary kappa is
reported as an observation about the structure of the disagreement and is NOT
used in any verdict.

Standard library only, no network.

    python3 stats.py
"""
import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
SOURCE = os.path.join(
    HERE, "..", "..", "EXPERIMENTS", "012-candidate-harvest", "raw", "screened.jsonl"
)

CLAUSE_BASED = ("vague", "not_a_software_need", "needs_hardware")
SURVIVOR_RELEVANT = ("mechanism_stated", "self_built", "prior_art")

CATEGORIES = (
    "mechanism_stated",
    "prior_art",
    "self_built",
    "not_a_software_need",
    "needs_hardware",
    "still_vague",
)

KAPPA_FLOOR = 0.6
C1_THRESHOLD = 5
POPULATION = 31


def read_jsonl(path):
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def cohen_kappa(pairs, labels):
    """Cohen's kappa over a label->label contingency.

    `pairs` is an iterable of (label_a, label_b). Both margins are used, so a
    label neither reader ever used simply contributes zero expected agreement
    rather than shifting the base rate.
    """
    n = len(pairs)
    if n == 0:
        return None
    agree = sum(1 for a, b in pairs if a == b)
    po = agree / float(n)
    counts_a = collections.Counter(a for a, _ in pairs)
    counts_b = collections.Counter(b for _, b in pairs)
    pe = sum((counts_a[l] / float(n)) * (counts_b[l] / float(n)) for l in labels)
    if pe == 1.0:
        # Every row in one label: kappa is undefined, not 1.0. Reporting 1.0
        # here would be a gate that cannot fail, which D056 forbids.
        return {"kappa": None, "po": po, "pe": pe, "agree": agree, "n": n,
                "note": "degenerate: expected agreement is 1.0, kappa undefined"}
    return {"kappa": (po - pe) / (1.0 - pe), "po": po, "pe": pe,
            "agree": agree, "n": n}


def main():
    r_rows = read_jsonl(os.path.join(RAW, "reader_r.jsonl"))
    s_rows = read_jsonl(os.path.join(RAW, "reader_s.jsonl"))
    src = {row["index"]: row for row in read_jsonl(os.path.realpath(SOURCE))}

    problems = []

    # A1 -- population integrity
    a1_cause_rule = sum(1 for idx in src if src[idx]["cause"] in CLAUSE_BASED)
    if len(r_rows) != POPULATION or len(s_rows) != POPULATION:
        problems.append("A1: reader files hold %d and %d rows, protocol declares %d"
                        % (len(r_rows), len(s_rows), POPULATION))
    if len(r_rows) != a1_cause_rule:
        problems.append("A1: population is not the declared category rule")
    if {row["index"] for row in r_rows} != {row["index"] for row in s_rows}:
        problems.append("A1: the two readers did not cover the same rows")
    empty = [row["index"] for row in r_rows if not (src[row["index"]].get("text") or "").strip()]
    if empty:
        problems.append("A1: rows with no comment text: %s" % empty)

    r = {row["index"]: row["category"] for row in r_rows}
    s = {row["index"]: row["category"] for row in s_rows}
    indices = sorted(r)

    for idx in indices:
        for name, table in (("R", r), ("S", s)):
            if table[idx] not in CATEGORIES:
                problems.append("%s: row %s has undeclared category %r" % (name, idx, table[idx]))

    # B1 -- six-category kappa, the declared agreement gate
    b1 = cohen_kappa([(r[i], s[i]) for i in indices], CATEGORIES)
    b1_pass = b1["kappa"] is not None and b1["kappa"] >= KAPPA_FLOOR

    # C1 -- the kill gate, declared over rows where both readers agree
    convergent = [i for i in indices
                  if r[i] in SURVIVOR_RELEVANT and s[i] in SURVIVOR_RELEVANT]
    either = [i for i in indices
              if r[i] in SURVIVOR_RELEVANT or s[i] in SURVIVOR_RELEVANT]
    c1_fires = len(convergent) >= C1_THRESHOLD
    c1_verdict = ("c1_fires" if len(convergent) >= C1_THRESHOLD
                  else "c1_fires_only_in_the_refused_band"
                  if len(convergent) > 2 else "c1_does_not_fire")

    # Post-hoc, reported as structure and used in no verdict: the gate is
    # declared over the survivor/not-survivor split, not over six labels.
    binary = cohen_kappa(
        [(r[i] in SURVIVOR_RELEVANT, s[i] in SURVIVOR_RELEVANT) for i in indices],
        [True, False],
    )

    flips = []
    for idx in convergent:
        flips.append({
            "index": idx,
            "id": src[idx]["id"],
            "original_cause": src[idx]["cause"],
            "original_reason": src[idx]["reason"],
            "reader_r": r[idx],
            "reader_s": s[idx],
            "both_survivor_relevant": True,
            "clause": src[idx]["clause"],
        })

    disagreements = []
    for idx in indices:
        if r[idx] != s[idx]:
            disagreements.append({
                "index": idx, "original_cause": src[idx]["cause"],
                "reader_r": r[idx], "reader_s": s[idx],
                "both_survivor_relevant": (r[idx] in SURVIVOR_RELEVANT
                                           and s[idx] in SURVIVOR_RELEVANT),
            })

    # Is either reader's survivor-relevant set a subset of the other's?
    r_set = {i for i in indices if r[i] in SURVIVOR_RELEVANT}
    s_set = {i for i in indices if s[i] in SURVIVOR_RELEVANT}

    vague = [i for i in indices if src[i]["cause"] == "vague"]
    results = {
        "experiment": "027-cause-of-death-reread",
        "computed_by": "stats.py from raw/reader_r.jsonl and raw/reader_s.jsonl",
        "population": {
            "rule": "the clause-based causes of death in E012's 50-row screen",
            "rows": len(indices),
            "prior_art_rows_held_out": len(src) - len(indices),
            "original_causes": dict(collections.Counter(src[i]["cause"] for i in indices)),
        },
        "gates": {
            "a1_integrity": {
                "declared": "%d rows, each with non-empty text" % POPULATION,
                "rows": len(indices),
                "pass": not problems,
                "problems": problems,
            },
            "b1_agreement": {
                "declared": "Cohen's kappa >= %.1f over the six categories" % KAPPA_FLOOR,
                "kappa": b1["kappa"],
                "po": b1["po"], "pe": b1["pe"],
                "agree": b1["agree"], "n": b1["n"],
                "pass": b1_pass,
                "consequence": (
                    "the restated six-category table is inconclusive and no cause "
                    "share from this experiment is reported as a fact"
                    if not b1_pass else "the restated table may be reported"
                ),
            },
            "c1_kill_gate": {
                "declared": (
                    "fires if >= %d of the %d rows are survivor-relevant to BOTH "
                    "readers; <=2 the extraction rule is not the cause; 3-4 refuses "
                    "a verdict" % (C1_THRESHOLD, POPULATION)
                ),
                "convergent_flips": len(convergent),
                "union_of_either_reader": len(either),
                "verdict": c1_verdict,
                "fires": c1_fires,
            },
        },
        "posthoc_binary_agreement": {
            "note": ("the declared six-category kappa is low partly because the "
                     "readers disagree about which non-survivor label a row takes; "
                     "the gate is declared over the survivor/not-survivor split, so "
                     "this is reported as structure and used in no verdict"),
            "kappa": binary["kappa"],
            "po": binary["po"], "pe": binary["pe"],
            "agree": binary["agree"], "n": binary["n"],
        },
        "structure": {
            "reader_r_survivor_set": sorted(r_set),
            "reader_s_survivor_set": sorted(s_set),
            "r_is_strict_subset_of_s": r_set < s_set,
            "contested_survivor_rows": sorted(r_set - s_set),
        },
        "category_counts": {
            "R": dict(collections.Counter(r[i] for i in indices)),
            "S": dict(collections.Counter(s[i] for i in indices)),
        },
        "original_vague_rows": {
            "rows": len(vague),
            "convergent_flips": len([i for i in vague if i in set(convergent)]),
            "per_row": [
                {"index": i, "original_cause": src[i]["cause"],
                 "reader_r": r[i], "reader_s": s[i],
                 "both_survivor_relevant": i in set(convergent)}
                for i in vague
            ],
        },
        "convergent_flips": flips,
        "disagreements": disagreements,
    }

    with open(os.path.join(HERE, "results.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1, sort_keys=True)
        fh.write("\n")

    g = results["gates"]
    print("population            %d rows (%d prior_art held out)"
          % (len(indices), results["population"]["prior_art_rows_held_out"]))
    print("A1 integrity          %s" % ("pass" if g["a1_integrity"]["pass"] else "FAIL"))
    print("B1 kappa (6 cats)     %.4f  (declared floor %.1f) -> %s"
          % (g["b1_agreement"]["kappa"], KAPPA_FLOOR,
             "pass" if b1_pass else "FAIL, restated table inconclusive"))
    print("C1 convergent flips   %d of %d (declared >=%d) -> %s"
          % (g["c1_kill_gate"]["convergent_flips"], POPULATION,
             C1_THRESHOLD, c1_verdict))
    print("   union of either    %d" % g["c1_kill_gate"]["union_of_either_reader"])
    print("posthoc binary kappa  %.4f  (structure only, used in no verdict)"
          % results["posthoc_binary_agreement"]["kappa"])
    print("R's flips inside S's  %s" % results["structure"]["r_is_strict_subset_of_s"])
    for problem in problems:
        print("PROBLEM: %s" % problem, file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())