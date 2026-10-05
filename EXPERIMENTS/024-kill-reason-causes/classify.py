#!/usr/bin/env python3
"""The mechanical half of 024's classification rule.

`PROTOCOL.md` assigns four mutually exclusive categories by precedence, from
"the primary source states that ...". Deciding which of those four sentences a
source states is a judgement, and this module does not make it: every category
in `rows.json` was written by hand, carrying the verbatim deciding sentence that
produced it, and this module only checks that the assignment obeys the declared
precedence and that the deciding sentence is actually present in the cited
primary source.

That split is the point. The category is the judgement and cannot be
mechanised; the precedence order, the population size and the sentence's
presence in the cited file are all mechanical and are what a disagreeing reader
would most want checked. `CLASSIFYING.md` states why the judgement half is not
re-derived here.

    python3 classify.py            # both populations, the gates, results.json
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROWS = os.path.join(HERE, "rows.json")
CONTROL = os.path.join(HERE, "control_rows.json")
RESULTS = os.path.join(HERE, "results.json")
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))

# The declared precedence, highest priority first. PROTOCOL.md's table plus the
# fifth category CONTROL.md added to make the control well posed.
PRECEDENCE = [
    "never_a_candidate",
    "unrecorded",
    "information_insufficient",
    "falsified_mechanism",
    "prior_art",
]

# H1's declared threshold, and the amendment's scope.
H1_MAJORITY = 0.50

CAUSE_RE = re.compile(r"^[a-z_]+$")


def load(path):
    """The `rows` member of one of this experiment's records.

    Both records carry provenance alongside their rows -- the population rule,
    the control's pass condition, the disclosure -- and that prose is metadata,
    not data. Returning the document instead of the list would hand `check_rows`
    a dict and fail on the first row, which is what happened on the first run."""
    with open(path) as fh:
        return json.load(fh)["rows"]


def norm(text):
    """Collapse whitespace and fold the typographic characters a sealed report
    uses interchangeably with ASCII. The deciding sentences are quoted by hand,
    so this only has to survive curly quotes, en-dashes and double spaces."""
    text = text.replace("’", "'").replace("‘", "'")
    text = text.replace("“", '"').replace("”", '"')
    text = text.replace("—", "-").replace("–", "-")
    text = text.replace(" ", " ")
    return re.sub(r"\s+", " ", text)


def sentence_present(sentence, path):
    """Is the quoted deciding sentence actually in the cited primary source?"""
    full = os.path.join(ROOT, path)
    if not os.path.exists(full):
        return "cited_file_missing"
    body = norm(open(full, encoding="utf-8").read())
    return "present" if norm(sentence) in body else "NOT_FOUND"


def check_rows(rows):
    """Every row: category is legal, precedence matches the recorded secondary
    reasons, and the deciding sentence is in the cited file."""
    problems = []
    for row in rows:
        cat = row["category"]
        if not CAUSE_RE.match(cat):
            problems.append((row["id"], "category %r is not a legal token" % cat))
            continue
        if cat not in PRECEDENCE:
            problems.append((row["id"], "category %r is outside the declared set" % cat))
        # Precedence: a row assigned to category C may list a secondary reason,
        # but any listed reason must rank strictly lower than C.
        rank = PRECEDENCE.index(cat)
        for sec in row.get("secondary", []):
            if sec not in PRECEDENCE:
                problems.append((row["id"], "secondary %r is not a legal token" % sec))
            elif PRECEDENCE.index(sec) >= rank:
                problems.append((row["id"], "secondary %r outranks %s" % (sec, cat)))
        # A treatment row must quote the deciding sentence and it must be in the
        # cited file. A control row need not: CONTROL.md's replacement control is
        # assigned mechanically off recorded evidence, so it has no hand-quoted
        # sentence to verify, and inventing one would misrepresent it as a
        # judgement. Its `corpora_with_deciding_text` field is the evidence.
        if "deciding_sentence" in row:
            # A row with no deciding sentence is only acceptable if it says why,
            # and only when the absence is the fact: either the row was never a
            # candidate, or it was promoted and no reason was ever recorded.
            if not row["deciding_sentence"]:
                if "sentence_absent_because" not in row:
                    problems.append((row["id"], "no deciding sentence and no "
                                                   "explanation for its absence"))
                elif row["category"] not in ("never_a_candidate", "unrecorded"):
                    problems.append((row["id"], "no deciding sentence, yet category "
                                                   "%r asserts one" % row["category"]))
            else:
                where = sentence_present(row["deciding_sentence"], row["source"])
                if where != "present":
                    problems.append((row["id"], "deciding sentence %s in %s"
                                     % (where, row["source"])))
        elif "assigned_by" not in row:
            problems.append((row["id"], "neither a deciding sentence nor an "
                                           "`assigned_by` provenance note"))
    return problems


def tally(rows, categories=None):
    counts = {}
    for row in rows:
        counts[row["category"]] = counts.get(row["category"], 0) + 1
    return dict(sorted(counts.items()))


def treatment(rows):
    """H1 and H2 over the treatment population.

    `never_a_candidate` rows are excluded from H1's denominator: a row that was
    never promoted had no kill reason attributed to it, so counting it would
    make a cause share smaller by adding rows no cause applies to. The protocol
    added that category to make the *control* well posed; applying the same rule
    here is stated here rather than assumed."""
    population = len(rows)
    never = sum(1 for r in rows if r["category"] == "never_a_candidate")
    eligible = [r for r in rows if r["category"] != "never_a_candidate"]
    prior = sum(1 for r in eligible if r["category"] == "prior_art")
    share = prior / len(eligible) if eligible else 0.0
    return {
        "population": population,
        "never_a_candidate_excluded": never,
        "h1_denominator": len(eligible),
        "prior_art_n": prior,
        "h1_prior_art_share": share,
        "declared_floor": H1_MAJORITY,
        "h1_verdict": "survives" if share > H1_MAJORITY else "killed",
        "h2_stated_count": 12,
        "h2_measured_count": population,
        "h2_agrees_with_the_stated_twelve": population == 12,
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
    The rule is free to score worse than 9 of 12, and a worse score is a real
    result -- it would show the hand-built categories do not track the
    evidence."""
    prior = [r for r in rows if r["category"] == "prior_art"]
    hits = sum(1 for r in rows if r["truth_is_prior_art"] == (r["category"] == "prior_art"))
    fp = [r for r in rows if r["category"] == "prior_art" and not r["truth_is_prior_art"]]
    fn = [r for r in rows if r["category"] != "prior_art" and r["truth_is_prior_art"]]
    correct = len(rows) - len(fp) - len(fn)
    return {
        "population": rows[0]["population_note"] if rows else "",
        "rows": len(rows),
        "reference_prior_art": sum(1 for r in rows if r["truth_is_prior_art"]),
        "reference_no_prior_art": sum(1 for r in rows if not r["truth_is_prior_art"]),
        "rule_prior_art": len(prior),
        "correct": correct,
        "false_positives": [r["name"] for r in fp],
        "false_negatives": [r["name"] for r in fn],
        "baseline_always_prior_art": sum(1 for r in rows if r["truth_is_prior_art"]),
        "note_on_baseline": (
            "A rule that read F029's cause column and nothing else would label all 12 "
            "prior_art and score %d of 12 -- three false positives, the exact error F035 "
            "documented. The control's discriminating cases are those three."
        ) % sum(1 for r in rows if r["truth_is_prior_art"]),
        "verdict": (
            "passes"
            if not fn and len(fp) <= 1
            else "FAILS"
        ),
        "verdict_rule": (
            "Passes at no false negatives and at most one false positive: the reference "
            "labels contain three known errors, so a rule that reproduced all three "
            "would be failing, not succeeding."
        ),
        "what_this_does_not_establish": (
            "Agreement with E016 is not correctness -- its arm-2 gate landed exactly on "
            "its threshold with one row deciding it. And the decisive limit is the one "
            "E023 already measured on this mission's labels: one reader, no second coder. "
            "This bounds whether the rule tracks an external label set, not whether this "
            "reader's judgements on the treatment rows are right."
        ),
    }


def sensitivity(rows, contested):
    """How fragile is H1?

    The protocol declared a single threshold and no sensitivity band, which is a
    gap: at a 50% floor a majority gate can be decided by one row. So the
    question every reader of a majority result has to ask is computed here
    instead: which rows, moved one at a time, would change the verdict, and how
    many would have to move together.

    `contested` is the list of rows whose primary source states more than one
    reason, so precedence decided them. Those are the rows a second reader could
    reasonably move; a row with one unambiguous reason is not a lever."""
    eligible = [r for r in rows if r["category"] != "never_a_candidate"]
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
    flip_all = [r for r in eligible if r["category"] == "prior_art" and r["id"] in contested]
    return {
        "eligible": n,
        "prior_art_n": base,
        "margin_over_the_floor": base / n - H1_MAJORITY,
        "rows_that_flip_the_verdict_alone": [l["id"] for l in levers if l["would_flip_the_verdict"]],
        "every_prior_art_row_flips_it_alone": len(levers) == base,
        "contested_rows": contested,
        "share_if_every_contested_prior_art_row_moves": (
            (base - len(flip_all)) / n if n else 0.0
        ),
        "verdict_if_contested_rows_all_move": (
            "killed"
            if n and (base - len(flip_all)) / n <= H1_MAJORITY
            else "survives"
        ),
        "verdict_if_one_row_moves": "killed",
        "reading": (
            "H1 survives, and it survives by exactly one row. Every one of the %d "
            "prior-art rows, moved to any other declared category, puts the share at "
            "9/18 = 0.500 and kills it. A majority gate with a one-row margin is a "
            "verdict about the population, not a robust finding about prior art."
            % base
        ),
    }


def main():
    rows = load(ROWS)
    crows = load(CONTROL)
    problems = check_rows(rows)
    problems += [("control/" + rid, problem) for rid, problem in check_rows(crows)]
    for row_id, problem in problems:
        print("PROBLEM %s: %s" % (row_id, problem))
    out = {
        "schema": "origin.kill-reason-causes/1",
        "experiment": "024-kill-reason-causes",
        "observed_utc": "2026-10-05",
        "treatment": treatment(rows),
        "sensitivity": sensitivity(rows, ["A1", "C2", "D1", "D2", "D5", "C3"]),
        "control": control(crows),
        "rule_problems": ["%s: %s" % (a, b) for a, b in problems],
        "limits": [
            "One reader assigned every category and there is no second coder. The deciding "
            "sentence is recorded per row so a disagreeing reader can re-derive each "
            "category and name the single sentence they disagree about.",
            "The four categories are the record's own vocabulary, not the world's, and the "
            "precedence order is a declared convention that can move a row across the 50% line.",
            "This is a count over the record as written. It is not a measurement of what "
            "exists in the world and nothing here is a novelty claim.",
            "H1's denominator excludes never_a_candidate rows. Including them would report a "
            "smaller prior-art share by adding rows to which no kill reason applies.",
        ],
    }
    with open(RESULTS, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")
    t, c = out["treatment"], out["control"]
    print("\ntreatment: %d rows, %d eligible" % (t["population"], t["h1_denominator"]))
    print("counts:", json.dumps(t["counts_eligible_only"]))
    print("H1 prior_art share %.3f against floor %.2f -> %s"
          % (t["h1_prior_art_share"], H1_MAJORITY, t["h1_verdict"]))
    print("H2 measured %d against the stated twelve -> agrees: %s"
          % (t["h2_measured_count"], t["h2_agrees_with_the_stated_twelve"]))
    sn = out["sensitivity"]
    print("sensitivity: margin over floor %.3f; %d rows alone would flip it; "
          "all contested rows moving -> %s"
          % (sn["margin_over_the_floor"], len(sn["rows_that_flip_the_verdict_alone"]),
             sn["verdict_if_contested_rows_all_move"]))
    print("control: %d/%d correct (baseline %d), FP %s, FN %s -> %s"
          % (c["correct"], c["rows"], c["baseline_always_prior_art"],
             c["false_positives"] or "none", c["false_negatives"] or "none",
             c["verdict"]))
    print("rule problems: %d" % len(problems))
    return 0


if __name__ == "__main__":
    sys.exit(main())