#!/usr/bin/env python3
"""E045 — the report the reader reads off the classified rows.

Split out of `read.py` at the 300-line cap. The split is by invariant: `read.py`
is the reading (corpus in, one labelled row per issue out, `raw/issues.jsonl`
written), and this is the rendering. Keeping them apart means a change to a
printed label cannot silently alter which rows are written, and a change to a
rule cannot silently alter a number that was quoted in the experiment README.

Nothing here classifies, labels, or decides. Every count printed is derived
from the rows `read.py` wrote, over denominators this file is told explicitly,
so the denominators cannot be re-derived from a different slice by accident.
"""

from rules import NEED_GAPS

AUTOMATED = ("agent", "script")


def emit(rows, ctx):
    """Print the whole report. `rows` are the classified and labelled rows."""
    n = len(rows)

    def tally(key):
        c = {}
        for r in rows:
            c[r[key]] = c.get(r[key], 0) + 1
        return c

    print("E045 read of the demand evidence behind the only candidate")
    print("=" * 72)
    print("corpus: EXPERIMENTS/038-staging-prior-art/raw/requests.jsonl")
    print("need arms: %d (%d with a 200, %d without: %s)" % (
        len(ctx["need_arms"]), len(ctx["ok"]), len(ctx["failed"]),
        ", ".join(sorted({str(r.get("status")) for r in ctx["failed"]})) or "-",
    ))
    print("harvested items: %d, unique issues: %d" % (ctx["harvested"], n))
    print("search universe (sum of total_count): %d" % ctx["universe"])
    print()
    print("requester class:")
    for k, v in sorted(tally("requester").items(), key=lambda kv: -kv[1]):
        print("  %-14s %3d  %.3f" % (k, v, v / n))
    print()
    print("interface the requester says it lacks:")
    for k, v in sorted(tally("gap").items(), key=lambda kv: -kv[1]):
        print("  %-18s %3d  %.3f" % (k, v, v / n))
    print()
    print("diff access:")
    for k, v in sorted(tally("diff_access").items(), key=lambda kv: -kv[1]):
        print("  %-14s %3d  %.3f" % (k, v, v / n))
    print()
    print("the four issues the record names:")
    for name in ctx["named"]:
        hit = [r for r in rows if r["ref"] == name]
        print("  %-26s %s" % (name, "PRESENT" if hit else "ABSENT"))
    if ctx["named_missing"]:
        print("  missing: %s" % ", ".join(ctx["named_missing"]))
    print()
    _population(rows, n)
    _instrument(rows)
    _reader(rows, n)
    print("wrote %s (%d rows)" % (ctx["out"], n))


def _population(rows, n):
    """The question item 0a turns on, over the declared denominator."""
    no_diff = [r for r in rows if r["diff_access"] == "none"]
    agent_rows = [r for r in rows if r["requester"] == "agent"]
    agent_no_diff = [r for r in agent_rows if r["diff_access"] == "none"]
    print("count over the declared denominator %d:" % n)
    print("  issues naming no diff access at all:            %d" % len(no_diff))
    print("  issues whose requester is an agent:              %d" % len(agent_rows))
    print("  ... and with no diff access:                     %d" % len(agent_no_diff))
    print("  ... and naming a line-coordinate gap:            %d" % len(
        [r for r in agent_no_diff if r["gap"] == "line-coordinate"]))
    print()


def _instrument(rows):
    """The rule classifier against the reader's labels (D069).

    Printed before the reader's own counts, because the reader's counts are the
    ones quoted and the rules are the ones whose precision is 0.372: a reader
    who reads only the totals should still have seen which instrument produced
    the labels being checked.
    """
    tp = sum(1 for r in rows if r["hand"]["need"] and r["gap"] in NEED_GAPS)
    fp = sum(1 for r in rows if not r["hand"]["need"] and r["gap"] in NEED_GAPS)
    fn = sum(1 for r in rows if r["hand"]["need"] and r["gap"] not in NEED_GAPS)
    prec = tp / float(tp + fp) if tp + fp else 0.0
    rec = tp / float(tp + fn) if tp + fn else 0.0
    print("the rule classifier's `gap` class, against the reader's labels:")
    print("  called the need: %d, of which the reader agrees: %d  precision %.3f"
          % (tp + fp, tp, prec))
    print("  the need by the reader: %d, of which the rules missed: %d  recall %.3f"
          % (tp + fn, fn, rec))
    print()


def _reader(rows, n):
    """The reader's own count, and every automated caller in it, with evidence."""
    need = [r for r in rows if r["hand"]["need"]]
    print("the reader's own count over the declared denominator %d:" % n)
    print("  issues about choosing which lines reach the index: %d  (%.3f)"
          % (len(need), len(need) / float(n)))
    for field, title, width in (
        ("requester", "by requester", 10),
        ("diff_access", "by diff access evidence", 12),
    ):
        print()
        print("  of those %d, %s:" % (len(need), title))
        group = {}
        for r in need:
            group.setdefault(r["hand"][field], []).append(r)
        for k in sorted(group, key=lambda k: -len(group[k])):
            print("    %-*s %2d" % (width, k, len(group[k])))
    print()
    # The population item 0a names: an automated caller with no diff.
    target = [r for r in need
              if r["hand"]["requester"] in AUTOMATED
              and r["hand"]["diff_access"] == "none"]
    print("  the population STATE-next-actions.md item 0a measures")
    print("  (an automated caller with no diff access at all):  %d" % len(target))
    for r in target:
        print("      %-32s %s" % (r["ref"], r["title"][:60]))
    print()
    print("  every automated caller in the reader's need rows, with the evidence:")
    for r in need:
        if r["hand"]["requester"] in AUTOMATED:
            print("      %-30s %-9s %-8s %s"
                  % (r["ref"], r["hand"]["requester"],
                     r["hand"]["diff_access"], r["hand"]["wants"][:60]))
    print()