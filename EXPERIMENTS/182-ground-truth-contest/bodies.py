#!/usr/bin/env python3
"""E182 stage 3: fetch answer bodies for all 60 scored rows, for the
prescriptive-overlap instrument declared in AMENDMENT 1.

Reads no assistant answer and no arm label: the qid list comes from scores.json
and nothing else is joined until stage 4. Bodies go to raw/se-bodies.jsonl
with their URL, quota probe beside them, so the bytes are auditable (D061).

Usage: python3 bodies.py [--limit N]
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
SE = "https://api.stackexchange.com/2.3"
UA = "think-free-e182/1.0"
CHUNK = 20

# One Stack Overflow answer in this corpus assigns an environment-variable
# *name* to a config key in a public code sample -- it carries no value. The
# scanner's generic `assigned-credential` rule matches the value position and
# cannot tell the two apart, and `tools/originlib/secrets.py` records the same
# class of false refusal on this venue for the `sk-` rule. The suppression is
# declared on the file and recorded in the session log, so it is visible rather
# than silent. (The literal snippet is not reproduced here: writing it would
# make this file match the rule it documents.)
ALLOW = "# origin-allow-secret-patterns: assigned-credential\n"


def se(path, params, note=None):
    url = "%s/%s?%s" % (SE, path, urllib.parse.urlencode(params))
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "application/json"})
    os.makedirs(RAW, exist_ok=True)
    with urllib.request.urlopen(req, timeout=60) as fh:
        body = json.loads(fh.read().decode("utf-8"))
        head = {k: v for k, v in fh.headers.items()}
    rec = {"url": url, "note": note, "headers": head, "body": body}
    target = os.path.join(RAW, "se-bodies.jsonl")
    if not os.path.exists(target):
        with open(target, "w") as out:
            out.write(ALLOW)
    with open(target, "a") as out:
        out.write(json.dumps(rec, sort_keys=True) + "\n")
    time.sleep(1.2)
    return body, rec


def main():
    limit = None
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])
    if "--rebuild-from-raw" in sys.argv:
        return rebuild_from_raw()

    qids = sorted(int(k) for k in json.load(
        open(os.path.join(HERE, "scores.json")))["rows"])
    if limit:
        qids = qids[:limit]
    print("population: %d qids" % len(qids))

    out = {}
    for i in range(0, len(qids), CHUNK):
        part = qids[i:i + CHUNK]
        page, more, got = 1, True, 0
        while more:
            body, _ = se("questions/%s/answers" % ";".join(str(q) for q in part),
                         {"site": "stackoverflow", "filter": "withbody",
                          "pagesize": 100, "sort": "votes", "page": page},
                         note="overlap instrument body fetch")
            items = body.get("items", [])
            for a in items:
                out.setdefault(str(a["question_id"]), []).append(
                    {"answer_id": a.get("answer_id"),
                     "score": a.get("score"),
                     "creation_date": a.get("creation_date"),
                     "is_accepted": a.get("is_accepted"),
                     "body": a.get("body", "")})
                got += 1
            more = bool(body.get("has_more"))
            if more:
                page += 1
        print("  chunk %d: qids %d..%d -> %d answers" % (i // CHUNK + 1,
                                                          part[0], part[-1], got))

    # One ordered list per question: top-voted first, then earliest, then
    # lowest id -- E177's own tie-break, so answer[0] is the key answer whose
    # score scores.json already reproduced.
    for q, answers in out.items():
        answers.sort(key=lambda a: (-(a["score"] or 0), a["creation_date"] or 0,
                                    a["answer_id"] or 0))

    with open(os.path.join(HERE, "bodies.json"), "w") as fh:
        # The derived dump carries the same declared suppression as the raw
        # capture it comes from, because it contains the same public answer
        # body. A `#` first line is not valid JSON, so every reader of this
        # file goes through load_bodies() below rather than json.load.
        fh.write(ALLOW)
        json.dump({"rows": out, "qids": qids}, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("bodies.json: %d rows, %d answers total"
          % (len(out), sum(len(v) for v in out.values())))
    return 0


def rebuild_from_raw():
    """Rebuild bodies.json from the committed raw capture, with no new fetch.

    The raw capture is the evidence of record; the derived dump is written
    from it so the two cannot drift apart. Costs zero quota.
    """
    out = {}
    seen = set()
    with open(os.path.join(RAW, "se-bodies.jsonl")) as fh:
        for line in fh:
            if line.startswith("#") or not line.strip():
                continue
            rec = json.loads(line)
            for a in rec["body"].get("items", []):
                # The raw capture holds two independent fetches: the 60-row
                # body fetch and G5's 10-row fetch, which overlaps it. An
                # answer is one answer, so the set is keyed by
                # (question, answer) and a repeated answer is not counted twice.
                key = (a.get("question_id"), a.get("answer_id"))
                if key in seen:
                    continue
                seen.add(key)
                out.setdefault(str(a["question_id"]), []).append(
                    {"answer_id": a.get("answer_id"),
                     "score": a.get("score"),
                     "creation_date": a.get("creation_date"),
                     "is_accepted": a.get("is_accepted"),
                     "body": a.get("body", "")})
    qids = sorted(int(k) for k in json.load(
        open(os.path.join(HERE, "scores.json")))["rows"])
    for q in qids:
        out.setdefault(str(q), [])
    for q, answers in out.items():
        answers.sort(key=lambda a: (-(a["score"] or 0), a["creation_date"] or 0,
                                    a["answer_id"] or 0))
    with open(os.path.join(HERE, "bodies.json"), "w") as fh:
        fh.write(ALLOW)
        json.dump({"rows": out, "qids": qids}, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("rebuilt bodies.json from raw: %d rows, %d answers, 0 requests"
          % (len(out), sum(len(v) for v in out.values())))
    return 0


def load_bodies(path):
    """Read a dump written with the ALLOW directive as its first line."""
    with open(path) as fh:
        text = "".join(line for line in fh if not line.startswith("#"))
    return json.loads(text)


if __name__ == "__main__":
    sys.exit(main())