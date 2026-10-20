#!/usr/bin/env python3
"""E181: render `ANS`'s input, one file per (row, arm), and prove the key answer is absent.

Arms, exactly as PROTOCOL.md defines them:

  A0  the question text, and nothing else. The floor.
  A1  the question text plus one line under `The reporter adds this:`
      carrying the fact `EXT` extracted. The treatment.
  B1  the question text plus the whole discussion verbatim under
      `Discussion under the question and its accepted answer:`. The strongest
      accessible alternative: paste the thread. Read as *all* comments on both
      posts, because that is what a user with the tab open actually has, and
      because AMENDMENT 1 established the round trip runs mostly on the
      question.
  C1  the question text plus one line under `The reporter adds this:` carrying
      a fact extracted from a DIFFERENT row - the next fact-bearing row in
      index order, wrapping. The negative control.

`ANS` sees one file at a time, with no arm label in the filename and nothing
about the experiment in the body. The row number and arm never appear inside
the text.

Run: python3 EXPERIMENTS/181-fact-supply-closes-gap/make_inputs.py
"""
import html
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "ans-input")
E177 = "EXPERIMENTS/177-evidence-gated-need"
E178 = "EXPERIMENTS/178-evidence-where-does-it-live"
C1_N = 10


def strip_html(raw):
    txt = re.sub(r"<code>(.*?)</code>", lambda m: " `" + m.group(1) + "` ", raw, flags=re.S)
    txt = re.sub(r"<[^>]+>", " ", txt)
    txt = html.unescape(txt).replace("\u00a0", " ")
    return re.sub(r"[ \t]+", " ", txt).strip()


def main():
    pop = json.load(open(os.path.join(HERE, "population.json")))
    man = pop["manifest"]
    facts = {}
    for line in open(os.path.join(HERE, "facts.jsonl")):
        r = json.loads(line)
        if r["fact"]:
            facts[r["qid"]] = r
    rows = {r["qid"]: r for r in
            json.load(open(os.path.join(E177, "rows.json")))["rows"]}

    # B1 needs every comment on both posts, de-duplicated, in creation order.
    prior = json.load(open(os.path.join(E178, "comments.json")))
    acom = dict((int(k), v) for k, v in prior["answer_comments"].items())
    qcom = {}
    for line in open(os.path.join(E178, "raw", "se.jsonl")):
        rec = json.loads(line)
        if "/questions/" not in rec["url"] or "/comments" not in rec["url"]:
            continue
        for c in rec["body"].get("items", []):
            qcom.setdefault(c["post_id"], []).append(c)

    def dedupe(items):
        seen, out = set(), []
        for c in sorted(items, key=lambda c: c.get("creation_date", 0)):
            if c["comment_id"] in seen:
                continue
            seen.add(c["comment_id"])
            out.append(c)
        return out

    withfacts = [m for m in man if m["qid"] in facts]
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    for f in os.listdir(OUT):
        os.remove(os.path.join(OUT, f))

    placebo = {}
    for i, m in enumerate(withfacts[:C1_N]):
        other = withfacts[(i + 1) % len(withfacts)]["qid"]
        placebo[m["qid"]] = facts[other]["fact"]

    index = []
    seq = 0
    for m in withfacts:
        qid = m["qid"]
        r = rows[qid]
        head = ("TITLE: %s\nTAGS: %s\n\nQUESTION AS POSTED:\n%s\n"
                % (r["title"], ",".join(r.get("tags") or []), strip_html(r["body"])))
        arms = {"A0": head}
        arms["A1"] = head + "\nThe reporter adds this:\n%s\n" % facts[qid]["fact"]
        if qid in placebo:
            arms["C1"] = head + "\nThe reporter adds this:\n%s\n" % placebo[qid]
        cs = dedupe(qcom.get(qid, []) + acom.get(r["key_answer_id"], []))
        disc = "\nDiscussion under the question and its accepted answer:\n"
        for c in cs:
            disc += "- %s\n" % strip_html(c["body"])
        arms["B1"] = head + disc
        for arm in ("A0", "A1", "B1", "C1"):
            if arm not in arms:
                continue
            seq += 1
            path = os.path.join(OUT, "%03d.txt" % seq)
            with open(path, "w") as fh:
                fh.write(arms[arm])
            index.append({"seq": seq, "arm": arm, "qid": qid,
                          "file": os.path.relpath(path, HERE)})

    with open(os.path.join(HERE, "ans-index.json"), "w") as fh:
        json.dump({"index": index, "n_rows": len(withfacts),
                   "fact_bearing_qids": [m["qid"] for m in withfacts],
                   "placebo_qids": sorted(placebo),
                   "b1_comments_per_row": dict(
                       (str(m["qid"]), len(dedupe(qcom.get(m["qid"], [])
                                                  + acom.get(rows[m["qid"]]["key_answer_id"], []))))
                       for m in withfacts)},
            fh, indent=1, sort_keys=True)

    # the assertion: no accepted-answer text anywhere ANS will see
    bad = []
    for e in index:
        body = open(os.path.join(HERE, e["file"])).read()
        kbody = strip_html(rows[e["qid"]]["key_body"] or "")[:120].strip()
        if len(kbody) > 40 and kbody in body:
            bad.append([e["seq"], "key-answer-prefix"])
    assert not bad, "ANS input leaked the accepted answer: %r" % (bad,)
    print("fact-bearing rows %d, ANS files %d, leak assertion passed"
          % (len(withfacts), len(index)))


if __name__ == "__main__":
    main()