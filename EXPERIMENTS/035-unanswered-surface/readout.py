#!/usr/bin/env python3
"""E035 -- the reader. PROTOCOL.md section 7.

    python3 readout.py --tag travel/customs
    python3 readout.py --tag stackoverflow/regex --limit 40
    python3 readout.py --survey

Prints, for one tag, the questions that Stack Overflow's own surfaces do not list, and
marks the ones its moderators have already recorded as answered elsewhere.

It needs no clustering, no embeddings and no canonical: the canonical edge is unreachable
from any client (E034 section 2, nine channels), so a tool that grouped similar questions
would be guessing. `closed_reason == "Duplicate"` is a field the platform already holds,
and this reader's whole claim is that nobody surfaces it for this population.

Default mode reads the committed E034 bytes and makes no network request, so the output
is reproducible offline and a reviewer can diff it against a sha256.
"""

import argparse
import collections
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
E034_RAW = os.path.normpath(os.path.join(HERE, "..", "034-reask-tail", "raw"))
U_RAW = os.path.join(HERE, "raw")
SOURCES = ("harvest.jsonl", "r1.jsonl", "r2.jsonl")

# D063: `closed_reason` is ten literals and two of them spell the same thing.
DUPLICATE_LITERALS = ("duplicate", "exact duplicate")


def is_duplicate(row):
    return (row.get("closed_reason") or "").strip().lower() in DUPLICATE_LITERALS


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 1.0)
    p, d = k / float(n), 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5)
    return (max(0.0, (c - h) / d), min(1.0, (c + h) / d))


def load_backlog():
    """E034's tail population: the bottom of each tag's score distribution, which is the
    ordering no Stack Overflow page offers (PROTOCOL.md section 2, P1b)."""
    rows = []
    for name in SOURCES:
        path = os.path.join(E034_RAW, name)
        if not os.path.exists(path):
            continue
        with open(path) as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                r = json.loads(line)
                if r.get("arm") == "tail":
                    r["link"] = "https://{}/q/{}".format(
                        "stackoverflow.com" if r["site"] == "stackoverflow"
                        else r["site"] + ".stackexchange.com", r["question_id"])
                    rows.append(r)
    return rows


def load_unanswered_ids():
    """The id set of `/questions/unanswered`, the surface `tab=Unanswered` is built on.
    Loaded only so the readout can tell a reader which rows that surface already lists."""
    path = os.path.join(U_RAW, "u1.jsonl")
    if not os.path.exists(path):
        return set()
    with open(path) as fh:
        return {json.loads(l)["question_id"] for l in fh if l.strip()}


def newest_creation(rows):
    return max((r.get("creation_date") or 0) for r in rows) if rows else 0


def parse_tag(text):
    if "/" not in text:
        raise argparse.ArgumentTypeError("tag must be site/tag, e.g. travel/customs")
    site, tag = text.split("/", 1)
    return site, tag


def rate_line(k, n):
    lo, hi = wilson(k, n)
    return "{:.4f}  CI95 [{:.4f}, {:.4f}]".format(k / float(n), lo, hi)


def survey(rows):
    cells = collections.defaultdict(list)
    for r in rows:
        cells[(r["site"], r["tag"])].append(r)
    print("score-tail backlog by tag -- the ordering no Stack Overflow page offers\n")
    print("  {:34s} {:>5s} {:>5s} {:>8s}  {}".format("tag", "n", "dup", "rate", "CI95"))
    for key in sorted(cells):
        sub = cells[key]
        k = sum(1 for r in sub if is_duplicate(r))
        print("  {:34s} {:5d} {:5d}  {}".format(
            key[0] + "/" + key[1], len(sub), k, rate_line(k, len(sub))))
    print("\nRead as: of the {} lowest-scored questions in these tags, {} ({:.1f}%) are "
          "closed as\nduplicates of a question that already has an answer.".format(
              len(rows), sum(1 for r in rows if is_duplicate(r)),
              100.0 * sum(1 for r in rows if is_duplicate(r)) / max(1, len(rows))))


def report(rows, uids, site, tag, limit, newest):
    sub = [r for r in rows if r["site"] == site and r["tag"] == tag]
    if not sub:
        sys.stderr.write("no committed tail rows for {}/{}\n".format(site, tag))
        return 1
    dup = [r for r in sub if is_duplicate(r)]
    shown = sorted(sub, key=lambda r: (0 if is_duplicate(r) else 1,
                                       -r["score"], -(r.get("view_count") or 0)))
    shown = shown[:limit] if limit else shown
    unans_here = sum(1 for r in sub if r["question_id"] in uids)

    print("{}/{}".format(site, tag))
    print("  backlog          {} lowest-scored questions".format(len(sub)))
    print("  closed duplicate {}  {}".format(len(dup), rate_line(len(dup), len(sub))))
    print("  listed by tab=Unanswered   {} of {} ({:.1f}%)".format(
        unans_here, len(sub), 100.0 * unans_here / len(sub)))
    print()
    print("  {:>4s} {:>7s} {:>9s} {:>5s} {:>9s}  {}".format(
        "score", "views", "age", "ans", "closure", "title"))
    for r in shown:
        age = (newest - r["creation_date"]) / 86400.0 / 365.25 if r.get("creation_date") else 0
        reason = (r.get("closed_reason") or "-")[:9]
        title = (r.get("title") or "(no title in committed bytes)")[:58]
        print("  {:>4d} {:>7d} {:>8.1f}y {:>5d} {:>9s}  {}".format(
            r["score"], r.get("view_count") or 0, age, r.get("answer_count") or 0,
            reason, title))
        print("  {:>4s} {:>7s} {:>9s} {:>5s} {:>9s}  {}".format(
            "", "", "", "", "", r["link"]))
    print("\n  'closure: Duplicate' is the platform's own label. This reader does not")
    print("  compute similarity and cannot name the canonical question: no client can")
    print("  (E034 section 2, nine channels tried). Click the row to see the banner.")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--tag", type=parse_tag, default=None,
                    help="site/tag, e.g. travel/customs")
    ap.add_argument("--limit", type=int, default=20)
    ap.add_argument("--survey", action="store_true",
                    help="one line per tag instead of one worklist")
    a = ap.parse_args(argv)
    rows = load_backlog()
    if not rows:
        sys.stderr.write("no committed backlog bytes\n")
        return 1
    newest = newest_creation(rows)
    if a.survey or a.tag is None:
        survey(rows)
        return 0
    return report(rows, load_unanswered_ids(), a.tag[0], a.tag[1], a.limit, newest)


if __name__ == "__main__":
    sys.exit(main())
