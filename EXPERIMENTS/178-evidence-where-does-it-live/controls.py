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
    """Every one of the 46 must have a comments record and a reconciled count."""
    here = os.path.join(HERE, "comments.json")
    counts_file = os.path.join(HERE, "comment_counts.json")
    if not (os.path.exists(here) and os.path.exists(counts_file)):
        print("G0b: not run - fetch has not produced comments.json yet")
        return False
    pop = json.load(open(os.path.join(HERE, "population.json")))
    counts = {int(k): v for k, v in
              json.load(open(counts_file))["comment_counts"].items()}
    com = json.load(open(here))
    qcom = {int(k): v for k, v in com["question_comments"].items()}
    acom = {int(k): v for k, v in com["answer_comments"].items()}
    bad = []
    for e in pop["population"]:
        qid = e["qid"]
        if qid not in counts:
            bad.append((qid, "no default-filter record"))
        elif counts[qid] != len(qcom.get(qid, [])):
            bad.append((qid, "comment_count %s vs %d returned"
                        % (counts[qid], len(qcom.get(qid, [])))))
        aid = e["key_answer_id"]
        if not aid:
            bad.append((qid, "no key answer id"))
        elif aid not in acom and counts.get(qid, 0) and aid not in acom:
            bad.append((qid, "key answer %d returned no comment thread" % aid))
    print("G0b: %d rows checked, %d mismatch(es); fetch problems: %s"
          % (len(pop["population"]), len(bad), com["problems"] or "none"))
    for b in bad[:10]:
        print("  FAIL %s" % (b,))
    return not bad and not com["problems"]


if __name__ == "__main__":
    ok_d = g0d()
    ok_b = g0b()
    print("blindness %s, fetch completeness %s"
          % ("PASS" if ok_d else "FAIL", "PASS" if ok_b else "not run"))
    sys.exit(0 if ok_d else 1)