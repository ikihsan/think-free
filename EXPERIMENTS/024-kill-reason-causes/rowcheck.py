#!/usr/bin/env python3
"""The half of 024's rule that checks the record rather than tallying it.

`classify.py` computes the gates. This module is the check that the hand-built
`rows.json` obeys `PROTOCOL.md` — that every category is legal, that no row
carries a secondary reason the declared precedence forbids, and that every
assigned category quotes a deciding sentence **actually present in the cited
primary source**.

The split is by invariant. Every tally in `classify.py` reads `rows.json`, so a
defect in the record propagates into every figure those tallies produce; that
makes verification a property of the record and not of any one gate, which is the
same reason 015 moved `attribution.py` away from `serving.py`.

**This check is not decoration.** On its first run it reported four defects in
the author's own hand work, including two restated deciding sentences that do not
exist in their cited sources — the defect class F024 names, where a plausible
sentence is indistinguishable from a real one to a reader who has not diffed it.

    python3 rowcheck.py           # the problems, or the count of zero
"""

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))

# PROTOCOL.md's order, plus the fifth category CONTROL.md added to make the
# control well posed. Highest priority first.
PRECEDENCE = [
    "never_a_candidate",
    "unrecorded",
    "information_insufficient",
    "falsified_mechanism",
    "prior_art",
]

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
    text = text.replace("\xa0", " ")
    return re.sub(r"\s+", " ", text)


def sentence_present(sentence, path):
    """Is the quoted deciding sentence actually in the cited primary source?"""
    full = os.path.join(ROOT, path)
    if not os.path.exists(full):
        return "cited_file_missing"
    with open(full, encoding="utf-8") as fh:
        body = norm(fh.read())
    return "present" if norm(sentence) in body else "NOT_FOUND"


def check_row(row):
    problems = []
    cat = row.get("category")
    if not isinstance(cat, str) or not CAUSE_RE.match(cat):
        return [(row.get("id", "?"), "category %r is not a legal token" % cat)]
    if cat not in PRECEDENCE:
        problems.append((row["id"], "category %r is outside the declared set" % cat))

    # Precedence: a row assigned to category C may list a secondary reason, but
    # any listed reason must rank strictly lower than C. `prior_art` ranks
    # lowest, so it can never be a secondary of another category -- which is how
    # A1 and C2 were caught declaring it so.
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
        # A row with no deciding sentence is only acceptable if it says why, and
        # only when the absence is the fact: either the row was never a
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


def check_all(rows):
    problems = []
    for row in rows:
        problems.extend(check_row(row))
    return problems


def main():
    rows = load(os.path.join(HERE, "rows.json"))
    crows = load(os.path.join(HERE, "control_rows.json"))
    problems = check_all(rows)
    problems += [("control/" + rid, p) for rid, p in check_all(crows)]
    for row_id, problem in problems:
        print("PROBLEM %s: %s" % (row_id, problem))
    print("rowcheck: %d row(s) checked, %d problem(s)"
          % (len(rows) + len(crows), len(problems)))
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())