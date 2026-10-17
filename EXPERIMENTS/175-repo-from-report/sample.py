#!/usr/bin/env python3
"""E175 stage 1: draw the sample, fetch the threads, name the gold repository.

Committed before any request. Writes `sample.json` (the drawn rows, the thread
fetch, the gold repository per row) and `raw/se.jsonl` (every Stack Exchange
response, headers included, so the quota cost and the question ids are auditable).

The draw is a seeded shuffle over the pool's unexposed rows. No row is chosen by
reading it.
"""
import hashlib
import json
import os
import random
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
REPO = os.path.join(os.path.dirname(os.path.dirname(HERE)))
POOL = os.path.join(REPO, "EXPERIMENTS", "126-stackoverflow-service-test",
                    "screening.jsonl")
GRADED = os.path.join(REPO, "EXPERIMENTS", "126-stackoverflow-service-test",
                      "grading-results.jsonl")
READ13 = os.path.join(REPO, "EXPERIMENTS", "169-version-pinned-reach",
                      "raw", "containment.json")
SE = "https://api.stackexchange.com/2.3"
UA = "think-free-e175/1.0"
DRAW = 40
SEED = 17520261017


def se(path, params=None):
    url = "%s/%s?%s" % (SE, path, urllib.parse.urlencode(params or {}))
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "application/json"})
    os.makedirs(RAW, exist_ok=True)
    with urllib.request.urlopen(req, timeout=40) as fh:
        body = json.loads(fh.read().decode("utf-8"))
        head = {k.lower(): v for k, v in fh.headers.items()}
    rec = {"url": url, "items": len(body.get("items") or []),
           "has_more": body.get("has_more"),
           "quota_remaining": head.get("x-ratelimit-remaining"),
           "quota_reset_epoch": head.get("x-ratelimit-reset")}
    with open(os.path.join(RAW, "se.jsonl"), "a") as fh2:
        fh2.write(json.dumps(rec, sort_keys=True) + "\n")
    time.sleep(1.1)
    return body, rec


def main():
    pool = [json.loads(l) for l in open(POOL) if l.strip()]
    graded = set()
    if os.path.exists(GRADED):
        for line in open(GRADED):
            if line.strip():
                graded.add(json.loads(line)["question_id"])
    read = set()
    if os.path.exists(READ13):
        for r in json.load(open(READ13))["rows"]:
            read.add(int(r["qid"]))
    exposed = {int(r["question_id"]) for r in pool} & (graded | read)
    free = [r for r in pool if int(r["question_id"]) not in graded | read]
    rng = random.Random(SEED)
    rng.shuffle(free)
    drawn = free[:DRAW]
    for r in drawn:
        r["question_id"] = int(r["question_id"])
    ids = [r["question_id"] for r in drawn]
    manifest = {
        "seed": SEED, "draw": DRAW, "pool_rows": len(pool),
        "excluded_e126_graded": len(graded), "excluded_e169_read": len(read),
        "candidate_rows": len(free), "drawn_ids": ids,
        "drawn_sha256": hashlib.sha256(
            json.dumps(ids, sort_keys=True).encode()).hexdigest(),
        "note": "committed before any request; the draw cannot have been tuned",
    }
    with open(os.path.join(HERE, "queries.json"), "w") as fh:
        json.dump(manifest, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("excluded %d graded, %d read in full; free=%d; drew %d rows"
          % (len(graded), len(read), len(free), len(ids)))

    # --- threads: questions (bodies + accepted_answer_id) then answers -------
    qs, rec1 = se("questions/%s" % ";".join(str(i) for i in ids),
                  {"site": "stackoverflow", "filter": "withbody",
                   "pagesize": 100})
    print("questions: %d items, quota left %s" % (len(qs["items"]), rec1["quota_remaining"]))
    accepted = {i["question_id"]: i.get("accepted_answer_id") for i in qs["items"]}

    answers, rec2 = {}, None
    try:
        ans, rec2 = se("questions/%s/answers" % ";".join(str(i) for i in ids),
                       {"site": "stackoverflow", "filter": "withbody",
                        "pagesize": 100, "sort": "votes"})
        for a in ans["items"]:
            answers.setdefault(a["question_id"], []).append(a)
    except Exception as exc:                                   # noqa: BLE001
        print("batched answers failed (%s); falling back per question" % exc)
    if not answers:
        for qid in ids:
            try:
                ans, rec = se("questions/%d/answers" % qid,
                              {"site": "stackoverflow", "filter": "withbody",
                               "pagesize": 100, "sort": "votes"})
                for a in ans["items"]:
                    answers.setdefault(qid, []).append(a)
            except Exception as exc:                           # noqa: BLE001
                print("  %d answers failed: %s" % (qid, exc))
    print("answers for %d of %d questions; quota left %s"
          % (len(answers), len(ids), (rec2 or {}).get("quota_remaining")))

    sys.path.insert(0, HERE)
    from derive import gh_repo                                     # noqa: E402

    rows = []
    for r in drawn:
        qid = r["question_id"]
        ans = answers.get(qid) or []
        acc = accepted.get(qid)
        order = ([a for a in ans if a.get("answer_id") == acc]
                 + [a for a in ans if a.get("answer_id") != acc])
        gold, gold_from = None, None
        for a in order:
            gold = gh_repo(a.get("body") or "")
            if gold:
                gold_from = "accepted" if a.get("answer_id") == acc else "top_voted"
                break
        rows.append({"qid": qid, "title": r["title"], "body": r["body"],
                     "tags": r["tags"], "view_count": r["view_count"],
                     "answer_count": r["answer_count"],
                     "gold_repo": gold, "gold_from": gold_from,
                     "answers_fetched": len(ans)})
    have = sum(1 for r in rows if r["gold_repo"])
    with open(os.path.join(HERE, "sample.json"), "w") as fh:
        json.dump({"manifest": manifest, "quota": [rec1, rec2], "rows": rows},
                  fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("gold repository named for %d of %d drawn rows" % (have, len(rows)))
    for r in rows:
        print("  %d %-28s %s" % (r["qid"], (r["gold_repo"] or "-"),
                                  (r["gold_from"] or "-")))


if __name__ == "__main__":
    main()