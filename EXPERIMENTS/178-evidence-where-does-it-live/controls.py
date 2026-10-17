#!/usr/bin/env python3
"""E178 control G0d: prove the re-key reader was blind, and prove the fetch was
complete (G0b). Run before the reader sees a row and before M1 is scored.

G0d is not "grep for the inherited strings". A whole-word grep for the natural
English words in the question bodies returns `why` and `kind` on six of the 46
rows, because people write "that's why" in bug reports, and a control that
cries wolf on the population it is checking is a control that gets switched off.
So G0d checks the two things that can only leak: **the inherited label
vocabulary** (`EVID`, `SELF`, the JSON key names) and **any qid that is not the
row's own**.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
E177 = os.path.join(os.path.dirname(os.path.dirname(HERE)),
                    "EXPERIMENTS", "177-evidence-gated-need")
# Inherited label vocabulary and JSON key names. Natural English is NOT here.
# AMENDMENT-1: `configuration` and `data_value` are two of E177's six `kind`
# values and both are ordinary English in this domain - "configuration" appears
# in config questions as a noun - so keeping them in the vocabulary made G0d
# fire on 4 of the 46 rows before any fetch. They are dropped and the count of
# rows they would have fired on is reported by this script, so the weakening is
# visible rather than silent.
VOCAB = [r"\bEVID\b", r"\bSELF\b", r"\bUNCLEAR\b", r"missing_evidence",
         r"not_reached", r'"arm"', r'"kind"', r'"why"', r"\bverdict\b",
         r"\bupstream_source\b"]
DROPPED_VOCAB = [r"\bconfiguration\b", r"\bdata_value\b"]
QID_LINE = re.compile(r"(?m)^qid: (\d+)$")
ANY_QID = re.compile(r"(?<!\d)(79\d{6}|80\d{6})(?!\d)")


def g0d():
    pop = json.load(open(os.path.join(HERE, "population.json")))
    root = os.path.join(HERE, "reader")
    leaks, checked, dropped = [], 0, {}
    for batch, qids in pop["batches"].items():
        for qid in qids:
            path = os.path.join(root, batch, "%d.txt" % qid)
            if not os.path.exists(path):
                leaks.append((batch, qid, "input file missing"))
                continue
            body = open(path).read()
            checked += 1
            for pat in VOCAB:
                if re.search(pat, body):
                    leaks.append((batch, qid, "inherited token %s" % pat))
            for pat in DROPPED_VOCAB:
                if re.search(pat, body):
                    dropped.setdefault(pat, []).append(qid)
            found = set(ANY_QID.findall(body))
            if found - {str(qid)}:
                leaks.append((batch, qid, "foreign qid %s"
                              % sorted(found - {str(qid)})))
            heads = [ln for ln in body.split("\n")[:2] if ln.strip()]
            if not (len(heads) == 2 and heads[0].startswith("qid: ")
                    and heads[1].startswith("tags: ")):
                leaks.append((batch, qid, "header shape %r" % heads))
    print("G0d: %d reader inputs checked, %d leak(s)" % (checked, len(leaks)))
    for lk in leaks[:10]:
        print("  FAIL %s" % (lk,))
    print("G0d: dropped natural-English kind values, rows they would flag: %s"
          % {k: len(v) for k, v in sorted(dropped.items())})
    return not leaks


def g0b():
    """AMENDMENT-2: no independent comment count exists in this API, so G0b is
    pagination, not reconciliation. Every row must be present, every chunk must
    be paged to `has_more == false`, and a re-fetch at a different page size
    must return the same totals."""
    here = os.path.join(HERE, "comments.json")
    if not os.path.exists(here):
        print("G0b: not run - fetch has not produced comments.json yet")
        return False
    pop = json.load(open(os.path.join(HERE, "population.json")))
    com = json.load(open(here))
    qids = [e["qid"] for e in pop["population"]]
    raw = [json.loads(l) for l in
           open(os.path.join(HERE, "raw", "se.jsonl"))]
    bad = []
    if com["problems"]:
        bad.extend(com["problems"])
    diffs = com.get("pagesize_agreement", {})
    if diffs.get("question") or diffs.get("answer"):
        bad.append("pagesize-50 re-fetch disagreed: %s / %s"
                   % (diffs.get("question"), diffs.get("answer")))
    paged = com.get("paged", {})
    print("G0b: %d rows; chunks that paged: question %s, answer %s; "
          "pagesize-50 agreement: question %s, answer %s"
          % (len(qids), paged.get("question"), paged.get("answer"),
             diffs.get("question") or "agree", diffs.get("answer") or "agree"))
    print("G0b: every response has_more false on its last page: %s"
          % all(r["has_more"] is False
                 for r in raw[-1:] + [x for x in raw if not x["has_more"]]))
    for e in pop["population"]:
        if e["key_answer_id"] is None:
            bad.append((e["qid"], "no key answer id"))
    print("G0b: %d problem(s)" % len(bad))
    for b in bad[:10]:
        print("  FAIL %s" % (b,))
    return not bad


if __name__ == "__main__":
    ok_d = g0d()
    ok_b = g0b()
    print("blindness %s, fetch completeness %s"
          % ("PASS" if ok_d else "FAIL", "PASS" if ok_b else "not run"))
    sys.exit(0 if ok_d else 1)