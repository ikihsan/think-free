#!/usr/bin/env python3
"""E181 stage 1: fix the population and move the bytes EXT is allowed to see.

Mechanical only. This script selects rows, fetches the comments Stack Overflow
publishes on each row's accepted answer, and writes one EXT input file per row.
It does not read a comment, judge a comment, extract a fact, or write an answer.

Three properties are load-bearing and are asserted here rather than assumed:

  1. The 20 rows are the first 20 of E177's scored EVID rows in E177's own
     `score/index.json` order. That order is CLF's emission order, which is the
     seeded draw order, which is descending view_count. The selection therefore
     depends on arrival and on nothing anybody saw while reading the rows.
  2. An EXT input file contains the question and the comments and **not** the
     accepted answer. The assertion below re-reads every file after it is
     written and fails the run if a key-answer id or a key-answer fragment is
     present.
  3. Every fetched response is appended to `raw/se.jsonl` with its URL, item
     count, paging flag and quota counter, so the quota cost is auditable.

Run:  python3 EXPERIMENTS/181-fact-supply-closes-gap/prep.py
"""
import hashlib
import html
import json
import os
import re
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
EXTIN = os.path.join(HERE, "ext")
SE = "https://api.stackexchange.com/2.3"
UA = "think-free-e181/1.0"
SITE = "stackoverflow"
N = 20

E177 = "EXPERIMENTS/177-evidence-gated-need"
E178 = "EXPERIMENTS/178-evidence-where-does-it-live"


def se(path, params):
    url = "%s/%s?%s" % (SE, path, urllib.parse.urlencode(params))
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "application/json"})
    os.makedirs(RAW, exist_ok=True)
    with urllib.request.urlopen(req, timeout=90) as fh:
        body = json.loads(fh.read().decode("utf-8"))
    rec = {"url": url, "n_items": len(body.get("items", [])),
           "has_more": body.get("has_more", False),
           "quota_remaining": body.get("quota_remaining"),
           "body": body}
    with open(os.path.join(RAW, "se.jsonl"), "a") as out:
        out.write(json.dumps(rec, sort_keys=True) + "\n")
    time.sleep(1.2)
    return rec


def chunks(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


def strip_html(raw):
    """Comment and question bodies as SE serves them, minus the markup.

    Deliberately naive and declared: SE comment bodies are short and this only
    has to be readable to one reader. It is not an instrument -- no number is
    computed from it.
    """
    txt = re.sub(r"<code>(.*?)</code>", lambda m: " `" + m.group(1) + "` ", raw,
                 flags=re.S)
    txt = re.sub(r"<[^>]+>", " ", txt)
    txt = html.unescape(txt)
    txt = txt.replace("\u00a0", " ")
    return re.sub(r"[ \t]+", " ", txt).strip()


def main():
    labels = {l["qid"]: l for l in
              json.load(open(os.path.join(E177, "labels.json")))["labels"]}
    pids = json.load(open(os.path.join(E177, "score", "index.json")))["pids"]
    rows = {r["qid"]: r for r in
            json.load(open(os.path.join(E177, "rows.json")))["rows"]}

    # (1) population selection, in E177's own order
    evid = [int(p.split("-")[1]) for p in pids
            if p.startswith("g-") and labels[int(p.split("-")[1])]["arm"] == "EVID"]
    pop = evid[:N]
    assert len(pop) == N, "population shorter than declared: %d" % len(pop)

    # answers E178 already fetched and committed: reuse the bytes, do not re-fetch
    prior = json.load(open(os.path.join(E178, "comments.json")))
    comments = {int(k): v for k, v in prior["answer_comments"].items()}

    need = [rows[q]["key_answer_id"] for q in evid
            if rows[q]["key_answer_id"] not in comments]
    for batch in chunks(need, 20):
        rec = se("answers/%s/comments" % ";".join(str(i) for i in batch),
                 {"site": SITE, "filter": "withbody", "pagesize": 100})
        for c in rec["body"].get("items", []):
            comments.setdefault(c["post_id"], []).append(c)

    # question comments: E178 fetched and committed these too (its fetch.py
    # stage 2), but comments.json only carries the answer-side ones, so they are
    # recovered from E178's raw capture rather than re-fetched.
    raw_q = {}
    for line in open(os.path.join(E178, "raw", "se.jsonl")):
        r = json.loads(line)
        if "/questions/" not in r["url"] or "/comments" not in r["url"]:
            continue
        for c in r["body"].get("items", []):
            raw_q.setdefault(c["post_id"], []).append(c)
    have_q = set(raw_q)

    # (2) EXT inputs: question + both comment sets, never the accepted answer
    os.makedirs(EXTIN, exist_ok=True)
    for old in os.listdir(EXTIN):
        os.remove(os.path.join(EXTIN, old))

    # (1b) eligibility, then n: a row is eligible when the thread's round trip
    # is actually on disk somewhere (question comments or answer comments).
    eligible = [q for q in evid
                if q in have_q or rows[q]["key_answer_id"] in comments]
    ineligible = [q for q in evid if q not in eligible]
    pop = eligible[:N]
    assert len(pop) == N, "eligible population shorter than declared: %d" % len(pop)

    manifest = []
    for i, qid in enumerate(pop, 1):
        r = rows[qid]
        aid = r["key_answer_id"]
        qc = sorted(raw_q.get(qid, []), key=lambda c: c.get("creation_date", 0))
        ac = sorted(comments.get(aid, []),
                    key=lambda c: c.get("creation_date", 0))
        lines = []
        lines.append("TITLE: %s" % r["title"])
        lines.append("TAGS: %s" % ",".join(r.get("tags") or []))
        lines.append("QUESTION AS POSTED:")
        lines.append(strip_html(r["body"]))
        lines.append("")
        lines.append("COMMENTS ON THE QUESTION, in order:")
        if qc:
            for c in qc:
                lines.append("- [%s] %s" % (
                    (c.get("owner") or {}).get("display_name", "?"),
                    strip_html(c["body"])))
        else:
            lines.append("(none)")
        lines.append("")
        lines.append("COMMENTS ON THE ANSWER THAT WAS ACCEPTED, in order "
                     "(the accepted answer itself is NOT shown to you):")
        if ac:
            for c in ac:
                lines.append("- [%s] %s" % (
                    (c.get("owner") or {}).get("display_name", "?"),
                    strip_html(c["body"])))
        else:
            lines.append("(none)")
        path = os.path.join(EXTIN, "%02d-%d.txt" % (i, qid))
        text = "\n".join(lines) + "\n"
        with open(path, "w") as fh:
            fh.write(text)
        manifest.append({"n": i, "qid": qid, "key_answer_id": aid,
                         "n_question_comments": len(qc),
                         "n_answer_comments": len(ac),
                         "n_comments": len(qc) + len(ac),
                         "view_count": r.get("view_count"),
                         "file": os.path.relpath(path, HERE)})

    # (2b) the assertion: no key-answer text in any EXT input
    leaks = []
    for m in manifest:
        body = open(os.path.join(HERE, m["file"])).read()
        kbody = strip_html(rows[m["qid"]]["key_body"] or "")
        probe = kbody[:120].strip()
        if len(probe) > 40 and probe in body:
            leaks.append([m["n"], "key-answer-prefix"])
        if str(m["key_answer_id"]) in body:
            leaks.append([m["n"], "key-answer-id"])
    assert not leaks, "EXT input leaked the accepted answer: %r" % (leaks,)

    digest = hashlib.sha256("".join(str(m["qid"]) for m in manifest)
                            .encode()).hexdigest()
    out = {"n_requested": N,
           "population_all_scored_evid": evid,
           "selection_rule": ("first 20 ELIGIBLE rows of E177's 30 scored EVID "
                              "rows in score/index.json order; that order is "
                              "the seeded shuffle of seed 17720261018 over the "
                              "30, i.e. a random permutation of them, so the "
                              "selection is by a coin and by no property of "
                              "the rows"),
           "eligibility_rule": ("at least one comment on the question or on "
                                "its accepted answer is on disk; eligibility "
                                "is decided before any reader sees a row"),
           "n_eligible": len(eligible),
           "ineligible": ineligible,
           "population": pop,
           "manifest": manifest,
           "n_with_any_comment": sum(1 for m in manifest if m["n_comments"] > 0),
           "refetched_answer_comment_sets": need,
           "question_comments_source": "E178 raw/se.jsonl, questions/*/comments",
           "leak_assertion": "passed: no key-answer id or 120-char prefix in any "
                             "EXT input",
           "population_sha256": digest}
    with open(os.path.join(HERE, "population.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print("population %s" % digest)
    print("rows with at least one comment: %d/20" % out["n_with_any_comment"])
    print("refetched answer comment sets: %d" % len(need))


if __name__ == "__main__":
    main()