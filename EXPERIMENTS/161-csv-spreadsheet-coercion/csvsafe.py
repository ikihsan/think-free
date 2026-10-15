#!/usr/bin/env python3
"""csvsafe - report, or repair, the cells a spreadsheet will reinterpret when
it opens a CSV.

Every rule here was measured against a real engine (LibreOffice Calc, headless,
CSV import with special-number detection on) on real files and on a control set
of 75 values; see ../RESULT.md.  The rules are not taken from documentation.

    csvsafe check FILE.csv [-v]        report what an engine would change
    csvsafe write IN.csv OUT.csv       write a copy with the damaging cells
                                       protected as ="value"
    csvsafe write --all IN.csv OUT     protect every cell an engine would
                                       change, not only the damaging ones

The repair is deliberately narrow: a protected cell is only one whose value the
engine would lose or alter irreversibly.  Note that ="" is read literally by
non-spreadsheet consumers (pandas, R, jq), so a repaired file is safe to open
in a spreadsheet and unsafe to read with a script unless the reader strips the
wrapper.  Exit codes: 0 nothing found, 3 damaging cells found, 1 usage error.
"""
import argparse
import csv
import re
import sys

LEADING_ZERO = re.compile(r"^[-+]?0\d+$")
DIGITS = re.compile(r"^[-+]?\d*$")
DATE = re.compile(r"^(\d{4}-\d{1,2}-\d{1,2}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4}"
                  r"|\d{1,2}\.\d{1,2}\.\d{2,4}|\d{1,2}-[A-Za-z]{3,9}-\d{2,4}"
                  r"|[A-Za-z]{3,9} \d{1,2}, ?\d{4})$")
DATETIME = re.compile(r"^(\d{4}-\d{2}-\d{2}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4})"
                      r"[T ]\d{1,2}:\d{2}(:\d{2})?(\.\d+)?( ?[AaPp][Mm])?"
                      r"(Z|[+-]\d{2}:?\d{2})?$")
TIME = re.compile(r"^\d{1,2}:\d{2}(:\d{2})?$")
AMPM = re.compile(r"^\d{1,2}:\d{2}(:\d{2})? ?[AaPp][Mm]$")
NUMBER = re.compile(r"^[-+]?(\d{1,3}(,\d{3})+|\d+)(\.\d*)?([eE][-+]?\d+)?$")
PLAIN_NUM = re.compile(r"^[-+]?(\d+)(\.\d*)?([eE][-+]?\d+)?$")
ANY_NUM = re.compile(r"^[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?$")
CURRENCY = re.compile(r"^\$[\d,]+(\.\d+)?$")
EXEC = re.compile(r"^[=+@\t]")
BOOLS = ("TRUE", "FALSE", "True", "False", "true", "false")

# rule -> (damaging, one-line statement of what the engine does)
RULES = [
    ("leading_zero", True, "engine reads it as a number and drops the leading zeros"),
    ("precision_loss", True, "engine reads it as a double and changes the digits"),
    ("formula_executed", True, "engine evaluates the leading = as a formula"),
    ("formula_coercion", False, "engine evaluates the leading + - @ or tab"),
    ("datetime", False, "engine reads it as a date-time"),
    ("date", False, "engine reads it as a date"),
    ("time", False, "engine reads it as a time"),
    ("thousands_separator", False, "engine reads it as a number and drops the separators"),
    ("percent", False, "engine reads it as a number and drops the %"),
    ("currency", False, "engine reads it as a number and drops the symbol"),
    ("bool", False, "engine reads it as a boolean"),
    ("number_spelling", False, "engine rewrites the number in its own spelling"),
]


def canonical(s):
    """The spelling an engine writes back for this number, when it differs."""
    n = s.lstrip("+")
    if n.endswith("."):
        n = n[:-1]
    if n.startswith("."):
        n = "0" + n
    if n.startswith("-."):
        n = "-0" + n[1:]
    if "." in n and "e" not in n.lower():
        head, _, frac = n.partition(".")
        frac = frac.rstrip("0")
        n = head + ("." + frac if frac else "")
    return n


def classify(cell):
    """-> (rule, damaging) for a cell an engine would alter, or (None, False)."""
    s = cell
    if s == "":
        return None, False
    if s != s.strip():
        return "whitespace", False
    if s.startswith("+") and ANY_NUM.match(s[1:]):
        return classify(s[1:])          # the + is dropped; the rest decides
    if EXEC.match(s) or (s.startswith("-") and len(s) > 1 and not s[1].isdigit()):
        return ("formula_executed", True) if s.startswith("=") else ("formula_coercion", False)
    if LEADING_ZERO.match(s):
        return "leading_zero", True
    if DATETIME.match(s):
        return "datetime", False
    if DATE.match(s):
        return "date", False
    if AMPM.match(s) or TIME.match(s):
        return "time", False
    plain = PLAIN_NUM.match(s) or ANY_NUM.match(s)
    if plain:
        if any(c in s for c in "eE"):
            return "number_spelling", False
        body = plain.group(1) + (plain.group(2) or "") + (plain.group(3) or "")
        if len(body.replace(".", "").replace("-", "").replace("+", "")) > 15:
            try:
                if float(s) != float("%.15g" % float(s)):
                    return "precision_loss", True
            except ValueError:
                pass
        if canonical(s) != s:
            return "number_spelling", False
        return None, False
    if NUMBER.match(s):
        return "thousands_separator", False
    if s.endswith("%") and PLAIN_NUM.match(s[:-1]):
        return "percent", False
    if s.startswith("$") and (PLAIN_NUM.match(s[1:]) or CURRENCY.match(s)):
        return "currency", False
    if s in BOOLS:
        return "bool", False
    return None, False


DAMAGING = {r for r, d, _ in RULES if d}


def protect(cell):
    return '="%s"' % cell.replace('"', '""')


def scan(path, limit=None):
    counts, examples, total, damaging = {}, {}, 0, 0
    with open(path, "r", encoding="utf-8", errors="replace", newline="") as f:
        for ri, row in enumerate(csv.reader(f)):
            for ci, cell in enumerate(row):
                rule, harm = classify(cell)
                if rule is None:
                    continue
                total += 1
                if harm:
                    damaging += 1
                counts[rule] = counts.get(rule, 0) + 1
                if rule not in examples or len(examples[rule]) < 3:
                    examples.setdefault(rule, [])
                    if len(examples[rule]) < 3:
                        examples[rule].append((ri + 1, ci + 1, cell))
            if limit and ri + 1 >= limit:
                break
    return counts, examples, total, damaging


def repair(src, dst, all_rules):
    counts = {}
    with open(src, "r", encoding="utf-8", errors="replace", newline="") as fin, \
            open(dst, "w", encoding="utf-8", newline="") as fout:
        writer = csv.writer(fout, lineterminator="\n")
        for row in csv.reader(fin):
            out = []
            for cell in row:
                rule, harm = classify(cell)
                if rule and (harm or all_rules):
                    counts[rule] = counts.get(rule, 0) + 1
                    out.append(protect(cell))
                else:
                    out.append(cell)
            writer.writerow(out)
    return counts


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd")
    c = sub.add_parser("check")
    c.add_argument("file")
    c.add_argument("-v", "--verbose", action="store_true")
    c.add_argument("--limit", type=int, default=None)
    w = sub.add_parser("write")
    w.add_argument("src")
    w.add_argument("dst")
    w.add_argument("--all", dest="all_rules", action="store_true",
                   help="protect every altered cell, not only the damaging ones")
    args = ap.parse_args(argv)
    if args.cmd == "check":
        counts, examples, total, damaging = scan(args.file, args.limit)
        print("%s: %d cells an engine would change, %d of them damaging"
              % (args.file, total, damaging))
        for rule in sorted(counts, key=lambda r: -counts[r]):
            kind = "DAMAGING" if rule in DAMAGING else "altered "
            print("  %-20s %-9s %7d  %s"
                  % (rule, kind, counts[rule],
                     dict((r, w) for r, _d, w in RULES).get(rule, "")))
            if args.verbose:
                for ri, ci, cell in examples.get(rule, []):
                    print("      row %d col %d: %r" % (ri, ci, cell))
        return 3 if damaging else 0
    if args.cmd == "write":
        counts = repair(args.src, args.dst, args.all_rules)
        print("%s -> %s: protected %d cells (%s)"
              % (args.src, args.dst, sum(counts.values()),
                 ", ".join("%s=%d" % kv for kv in sorted(counts.items()))))
        return 0
    ap.print_usage()
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))