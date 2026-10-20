#!/usr/bin/env python3
"""E178 stage 1: fix the population and write the re-key reader's inputs.

Reads only what E177 committed (`labels.json`, `rows.json`, `arms.json`,
`score/verdicts.jsonl`) and writes:

  population.json      the 46 EVID qids in E177's own emission order, their key
                       answer ids, and the SELF-arm ids the G0a control set is
                       drawn from by rule
  reader/<n>/*.txt     one file per row: question + key answer, no arm, no kind,
                       no label, no verdict, no view count
  reader/BATCHES.json  the qid list per batch, and the inherited strings G0d
                       greps for

Nothing here judges anything and nothing here fetches anything.
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
E177 = os.path.join(os.path.dirname(os.path.dirname(HERE)),
                    "EXPERIMENTS", "177-evidence-gated-need")
BATCH = 8
TAG = re.compile(r"<[^>]+>")
CODE = re.compile(r"(?s)<code>.*?</code>")


def text(html):
    """HTML to plain text, keeping code blocks - they carry the evidence.

    Copied verbatim from E177's roles.py so both experiments tokenise the same
    bytes the same way. A copy rather than an import, because E177's file is an
    input to this one and imports between committed experiment directories are
    how a later reader ends up unable to tell which version ran.
    """
    kept = []

    def grab(m):
        kept.append(m.group(0))
        return " "

    CODE.sub(grab, html or "")
    out = TAG.sub(" ", html or "")
    for k in kept:
        out += "\n" + TAG.sub(" ", k)
    for a, b in (("&lt;", "<"), ("&gt;", ">"), ("&amp;", "&"), ("&quot;", '"')):
        out = out.replace(a, b)
    out = re.sub(r"&#\d+;", " ", out)
    return re.sub(r"[ \t]+", " ", out).strip()


def wrap(s, width=90):
    out = []
    for ln in (s or "").split("\n"):
        if not ln:
            out.append("")
        for i in range(0, len(ln), width):
            out.append(ln[i:i + width])
    return out or [""]


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()


def main():
    labels = json.load(open(os.path.join(E177, "labels.json")))
    rows = {r["qid"]: r for r in
            json.load(open(os.path.join(E177, "rows.json")))["rows"]}

    lab = {r["qid"]: r for r in labels["labels"]}
    evid = [q for q in lab if lab[q]["arm"] == "EVID"]
    # All 52 SELF rows of the population, not the 30 E177 sampled: the control
    # set is drawn from the arm, and taking the sampled 30 would make the
    # control set a subset of the arm's own measured rows.
    self_ids = sorted(q for q in lab if lab[q]["arm"] == "SELF")
    missing = [q for q in evid if q not in rows or not rows[q].get("key_body")]
    if missing:
        print("FATAL: %d of the %d EVID rows have no key body in rows.json: %s"
              % (len(missing), len(evid), missing[:5]))
        return 1

    # Order: E177's own emission order (which is the draw order, by arrival), so
    # the batches are a partition of a sequence that exists in the record and not
    # an order this session chose after reading anything.
    pop = []
    for qid in evid:
        r = rows[qid]
        pop.append({"qid": qid, "key_answer_id": r["key_answer_id"],
                    "key_score": r["key_score"], "tags": r["tags"],
                    "view_count": r["view_count"]})

    batches = {}
    for i in range(0, len(pop), BATCH):
        batches["b%d" % (i // BATCH)] = pop[i:i + BATCH]

    for name, part in batches.items():
        d = os.path.join(HERE, "reader", name)
        os.makedirs(d, exist_ok=True)
        for entry in part:
            r = rows[entry["qid"]]
            path = os.path.join(d, "%d.txt" % entry["qid"])
            with open(path, "w") as fh:
                fh.write("qid: %d\ntags: %s\n\n"
                         % (entry["qid"], ", ".join(r["tags"])))
                for label, body in (("TITLE", r["title"]),
                                    ("QUESTION", text(r["body"])),
                                    ("KEY ANSWER (highest scored)",
                                     text(r["key_body"]))):
                    fh.write("=== %s ===\n" % label)
                    for ln in wrap(body):
                        fh.write(ln + "\n")
                    fh.write("\n")

    # The strings control G0d greps for: if any of them appears in a reader
    # input file, the reader was not blind and the re-key is not a second coder.
    inherited = sorted({"arm", "kind", "why", "EVID", "SELF", "missing_evidence",
                        "reached", "not_reached"})

    with open(os.path.join(HERE, "population.json"), "w") as fh:
        json.dump({"population": pop,
                   "batches": {k: [e["qid"] for e in v]
                               for k, v in batches.items()},
                   "self_arm_ids": self_ids,
                   "inherited_strings": inherited,
                   "sha256": digest([e["qid"] for e in pop]),
                   "digest_question_key": digest(
                       {str(e["qid"]): [text(rows[e["qid"]]["body"]),
                                        text(rows[e["qid"]]["key_body"])]
                        for e in pop}),
                   "note": "46 rows, E177's emission order; the control set is "
                           "the five SELF-arm rows with the highest "
                           "comment_count, fixed by rule in PROTOCOL.md G0a"},
                  fh, indent=1, sort_keys=True)
        fh.write("\n")

    total = sum(os.path.getsize(os.path.join(HERE, "reader", b, f))
                for b in os.listdir(os.path.join(HERE, "reader"))
                if os.path.isdir(os.path.join(HERE, "reader", b))
                for f in os.listdir(os.path.join(HERE, "reader", b)))
    print("population %d rows in %d batches of <=%d; reader bytes %d"
          % (len(pop), len(batches), BATCH, total))
    print("population sha256 %s" % digest([e["qid"] for e in pop])[:16])
    print("SELF-arm ids available for the G0a control set: %d" % len(self_ids))
    return 0


if __name__ == "__main__":
    sys.exit(main())