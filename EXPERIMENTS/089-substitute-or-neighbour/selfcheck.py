#!/usr/bin/env python3
"""E089 -- self-check: every label's `evidence` field must be traceable to the
bytes it rests on. Prints, per row, whether the quoted text was found verbatim
in the package's own description, so a reader can audit the labelling without
re-running the counting.

Run:  python3 selfcheck.py     Exit 0 when every row is accounted for.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
E064 = os.path.join(HERE, "..", "064-remedy-existence", "raw")


def norm(s):
    return " ".join((s or "").split())


def load(path):
    with open(path) as fh:
        head = fh.readline().rstrip("\n").split("\t")
        out = []
        for line in fh:
            if line.strip():
                p = line.rstrip("\n").split("\t")
                p += [""] * (len(head) - len(p))
                out.append(dict(zip(head, p)))
        return out


def main():
    meta = {(m["ecosystem"], m["name"]): m.get("desc") or ""
            for m in json.load(open(os.path.join(E064,
                                                 "metadata-falseaccepts.json")))}
    ctrl = {(m["ecosystem"], m["name"]): m.get("desc") or ""
            for m in json.load(open(os.path.join(E064, "metadata-real.json")))}

    verbatim = paraphrased = absent = 0
    problems = []
    for r in load(os.path.join(HERE, "labels.tsv")):
        key = (r["ecosystem"], r["name"])
        desc, ev = norm(meta.get(key)), norm(r["evidence"])
        if ev == "(no description)":
            if desc:
                problems.append("%s: labelled as having no description, but the "
                                "file has %r" % (key, desc[:60]))
            verbatim += 1
            continue
        # the leading quoted span, up to the first " -- " note or closing quote
        span = ev.split(" -- ")[0].strip().strip('"')
        span = span.split(" = ")[0].strip().strip('"')
        if norm(span) and norm(span) in desc:
            verbatim += 1
        elif span and norm(span.split("...")[0]) in desc:
            paraphrased += 1
        else:
            absent += 1
            problems.append("%s: evidence not found verbatim: %r vs %r"
                            % (key, span[:60], desc[:60]))

    c_verbatim = c_absent = 0
    for r in load(os.path.join(HERE, "control-labels.tsv")):
        key = (r["ecosystem"], r["name"])
        desc, span = norm(ctrl.get(key)), norm(r["evidence"]).split(" -- ")[0]
        if norm(span) in desc or norm(span).strip('"') in desc:
            c_verbatim += 1
        else:
            c_absent += 1
            problems.append("control %s: %r not in %r" % (key, span[:50], desc[:50]))

    print("population rows: %d verbatim, %d ellipsised, %d not found"
          % (verbatim, paraphrased, absent))
    print("control rows:    %d verbatim, %d not found" % (c_verbatim, c_absent))
    for p in problems:
        print("  ! %s" % p)
    print("every label's evidence is traceable: %s"
          % (not problems and absent == 0 and c_absent == 0))
    return 0 if (not problems and absent == 0 and c_absent == 0) else 3


if __name__ == "__main__":
    sys.exit(main())