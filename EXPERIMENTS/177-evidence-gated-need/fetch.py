#!/usr/bin/env python3
"""E177 stage 1: re-fetch E175's committed draw with answer bodies on disk.

E175 logged its Stack Exchange responses as URL + item count only, so the
answer bodies were discarded after the repository extractor ran over them. E177
needs them as the key. This script fetches the same ids with the same filter
and writes **every response body** to `raw/se.jsonl`, headers included, so the
quota cost and the bytes are auditable.

Nothing here reads or judges an answer. It moves bytes.
"""
import hashlib
import json
import os
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
E175 = os.path.join(os.path.dirname(os.path.dirname(HERE)),
                    "EXPERIMENTS", "175-repo-from-report")
SE = "https://api.stackexchange.com/2.3"
UA = "think-free-e177/1.0"


def se(path, params):
    url = "%s/%s?%s" % (SE, path, urllib.parse.urlencode(params))
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "application/json"})
    os.makedirs(RAW, exist_ok=True)
    with urllib.request.urlopen(req, timeout=60) as fh:
        body = json.loads(fh.read().decode("utf-8"))
        head = {k.lower(): v for k, v in fh.headers.items()}
    rec = {"url": url,
           "quota_remaining": head.get("x-ratelimit-remaining"),
           "quota_reset_epoch": head.get("x-ratelimit-reset"),
           "body": body}
    with open(os.path.join(RAW, "se.jsonl"), "a") as out:
        out.write(json.dumps(rec, sort_keys=True) + "\n")
    time.sleep(1.2)
    return body, rec


def chunks(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


def main():
    ids = json.load(open(os.path.join(E175, "queries.json")))["drawn_ids"]
    src = {r["qid"]: r for r in json.load(open(os.path.join(E175, "sample.json")))["rows"]}
    print("reusing E175's committed draw of %d ids (seed %s)"
          % (len(ids), json.load(open(os.path.join(E175, "queries.json")))["seed"]))

    questions, answers, last = {}, {}, None
    for part in chunks(ids, 100):
        qs, last = se("questions/%s" % ";".join(str(i) for i in part),
                      {"site": "stackoverflow", "filter": "withbody",
                       "pagesize": 100})
        for it in qs["items"]:
            questions[it["question_id"]] = it
    print("question bodies: %d of %d" % (len(questions), len(ids)))

    for part in chunks(ids, 20):
        if not any((questions.get(i) or {}).get("answer_count") for i in part):
            continue
        page, more = 1, True
        while more:
            try:
                ans, last = se("questions/%s/answers"
                               % ";".join(str(i) for i in part),
                               {"site": "stackoverflow", "filter": "withbody",
                                "pagesize": 100, "sort": "votes", "page": page})
            except Exception as exc:                            # noqa: BLE001
                print("answers chunk %s page %d failed: %s"
                      % (part[:3], page, exc))
                break
            for a in ans["items"]:
                answers.setdefault(a["question_id"], []).append(a)
            more = bool(ans.get("has_more"))
            if more:
                page += 1
    print("answer bodies for %d of %d questions"
          % (len(answers), len(ids)))

    rows = []
    for qid in ids:
        q = questions.get(qid)
        if q is None:
            continue
        acc = q.get("accepted_answer_id")
        pool = answers.get(qid) or []
        # AMENDMENT 2: the key is the highest-scoring answer, ties broken by the
        # earliest creation_date then the lowest answer_id. This pool carries an
        # accepted answer on 6 rows, which cannot key the declared n of 60.
        best = None
        for a in pool:
            k = (-(a.get("score") or 0), a.get("creation_date") or 0,
                 a.get("answer_id") or 0)
            if best is None or k < best[0]:
                best = (k, a)
        # `filter=withbody` returns tags as bare strings; the default filter
        # returns objects. First run crashed here; declared and committed
        # before the re-run (AMENDMENT-1).
        tags = [t["name"] if isinstance(t, dict) else t for t in q.get("tags", [])]
        rows.append({
            "qid": qid,
            "title": q.get("title", ""),
            "body": q.get("body", ""),
            "tags": tags,
            "view_count": q.get("view_count"),
            "answer_count": q.get("answer_count"),
            "accepted_answer_id": acc,
            "key_answer_id": (best[1].get("answer_id") if best else None),
            "key_score": (best[1].get("score") if best else None),
            "key_is_accepted": bool(best and best[1].get("answer_id") == acc),
            "key_body": (best[1].get("body") if best else None),
            "answers_fetched": len(pool),
        })
    have = sum(1 for r in rows if r["key_body"])
    payload = {"rows": rows, "sha256": hashlib.sha256(
        json.dumps([r["qid"] for r in rows]).encode()).hexdigest()}
    with open(os.path.join(HERE, "rows.json"), "w") as fh:
        json.dump(payload, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("rows.json: %d rows, key answer present on %d (accepted on %d), "
          "ids digest %s"
          % (len(rows), have, sum(1 for r in rows if r["key_is_accepted"]),
             payload["sha256"][:16]))
    print("quota remaining: %s" % (last or {}).get("quota_remaining"))


if __name__ == "__main__":
    sys.exit(main())