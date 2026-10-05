#!/usr/bin/env python3
"""Build the blind population for E027: the 31 clause-killed harvested needs.

Writes raw/population.jsonl, one row per clause-based kill, carrying the
*full* comment text and no original cause, no original reason, and no verdict
of any kind. A classifier reading this file cannot see what the screen said.

The population rule is fixed in PROTOCOL.md and is enforced here rather than
described: the three categories are the ones a mechanism screen decides by
reading prose, and `prior_art` is excluded because E016 already re-adjudicated
it on three corpora. `--selftest` asserts the population is exactly the rule and
that no leakage field is present, so the exclusion cannot be quietly widened and
a classifier cannot be handed the answer.

Standard library only. No network.

    python3 population.py --selftest
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(
    HERE, "..", "..", "EXPERIMENTS", "012-candidate-harvest", "raw", "screened.jsonl"
)

CLAUSE_BASED = ("vague", "not_a_software_need", "needs_hardware")

# Fields copied to the blind file. The original `cause`, `reason` and `name` are
# deliberately absent; `index` is kept only so a row can be joined back.
ALLOWED = ("index", "id", "date", "story", "trigger", "text", "clause")

FORBIDDEN = ("cause", "reason", "name")


def load_source():
    path = os.path.realpath(SOURCE)
    if not os.path.exists(path):
        raise SystemExit("source population not found: %s" % path)
    rows = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                rows.append(json.loads(line))
    return path, rows


def build(rows):
    population = []
    for row in rows:
        if row.get("cause") not in CLAUSE_BASED:
            continue
        out = {k: row[k] for k in ALLOWED if k in row}
        population.append(out)
    return population


def selftest(rows, population):
    """Assert the population rule and the absence of leakage. Exits nonzero."""
    problems = []

    expected = [r for r in rows if r.get("cause") in CLAUSE_BASED]
    if len(population) != 31:
        problems.append("population is %d rows, the protocol declares 31"
                        % len(population))
    if len(population) != len(expected):
        problems.append("population does not match the declared category rule")

    ids = [r.get("index") for r in population]
    if len(set(ids)) != len(ids):
        problems.append("duplicate index in population")
    if sorted(ids) != ids:
        problems.append("population is not in the source's recorded order")

    for row in population:
        for field in FORBIDDEN:
            if field in row:
                problems.append("row %s leaks %r" % (row.get("index"), field))
        if not (row.get("text") or "").strip():
            problems.append("row %s has no comment text" % row.get("index"))

    # Every excluded row must be a category the protocol excludes, and the
    # excluded set must be exactly the prior-art verdicts.
    excluded = [r for r in rows if r.get("cause") not in CLAUSE_BASED]
    if {r.get("cause") for r in excluded} - {"prior_art"}:
        problems.append("population rule excludes a non-prior_art category")

    if problems:
        for p in problems:
            print("SELFTEST FAIL: %s" % p, file=sys.stderr)
        return 1
    print("selftest ok: %d clause-killed rows, %d prior_art rows held out"
          % (len(population), len(excluded)))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true",
                    help="assert the population rule and print the counts")
    ap.add_argument("--out", default=os.path.join(HERE, "raw", "population.jsonl"))
    args = ap.parse_args()

    path, rows = load_source()
    population = build(rows)

    if args.selftest:
        return selftest(rows, population)

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        for row in population:
            fh.write(json.dumps(row, sort_keys=True) + "\n")
    print("source     %s" % os.path.relpath(path, os.path.join(HERE, "..")))
    print("population %d rows -> %s" % (len(population), os.path.relpath(args.out)))
    return 0


if __name__ == "__main__":
    sys.exit(main())