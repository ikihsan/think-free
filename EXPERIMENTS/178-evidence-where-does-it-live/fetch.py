#!/usr/bin/env python3
"""E178 stage 2: fetch what the thread itself carries.

Three surfaces, all of them things Stack Overflow already publishes about a
question it hosts, and none of them an assistant's opinion:

  1. `questions/{ids}` with the DEFAULT filter -> `comment_count` per question,
     which is the completeness cross-check for control G0b and the ordering key
     for the G0a control set. The default filter carries no bodies, so this
     costs no bytes the protocol did not declare.
  2. `questions/{ids}/comments` -> what was asked in the thread.
  3. `answers/{ids}/comments` -> what was asked of the asker in the key answer.

Every response is appended to `raw/se.jsonl` with its URL, its item count and
the quota counters the body carries, so the cost is auditable afterwards.

Nothing here reads or judges a comment. It moves bytes.
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
UA = "think-free-e178/1.0"
SITE = "stackoverflow"


def se(path, params):
    url = "%s/%s?%s" % (SE, path, urllib.parse.urlencode(params))
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "application/json"})
    os.makedirs(RAW, exist_ok=True)
    with urllib.request.urlopen(req, timeout=90) as fh:
        raw = fh.read().decode("utf-8")
        body = json.loads(raw)
    rec = {"url": url, "n_items": len(body.get("items", [])),
           "has_more": body.get("has_more", False),
           "quota_remaining": body.get("quota_remaining"),
           "body": body}
    with open(os.path.join(RAW, "se.jsonl"), "a") as out:
        out.write(json.dumps(rec, sort_keys=True) + "\n")
    time.sleep(1.3)
    return rec


def chunks(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


def fetch_all(endpoint, ids, key):
    """Fetch `endpoint` for ids in chunks; return {id: [items]}, plus a log."""
    got, problems = {}, []
    for part in chunks(ids, 20):
        path = endpoint % ";".join(str(i) for i in part)
        rec = se(path, {"site": SITE, "filter": "withbody", "pagesize": 100})
        for it in rec["body"].get("items", []):
            got.setdefault(key(it), []).append(it)
        if rec["has_more"]:
            problems.append("%s: has_more true for chunk starting %d"
                            % (endpoint, part[0]))
    return got, problems


def main():
    pop = json.load(open(os.path.join(HERE, "population.json")))
    qids = [e["qid"] for e in pop["population"]]
    aids = [e["key_answer_id"] for e in pop["population"]
            if e["key_answer_id"]]
    problems, quota = [], []

    # 1. comment_count for every row in the arm population, default filter.
    counts = {}
    for part in chunks(sorted(qids + pop["self_arm_ids"]), 100):
        rec = se("questions/%s" % ";".join(str(i) for i in part),
                 {"site": SITE, "filter": "default", "pagesize": 100})
        for it in rec["body"].get("items", []):
            counts[it["question_id"]] = it.get("comment_count") or 0
        quota.append(rec["quota_remaining"])
    print("default-filter records: %d (expected %d); comment_count present on %d"
          % (len(counts), len(set(qids + pop["self_arm_ids"])),
             sum(1 for q in counts if counts[q] is not None)))
    with open(os.path.join(HERE, "comment_counts.json"), "w") as fh:
        json.dump({"comment_counts": {str(k): v for k, v in counts.items()},
                   "source": "questions/{ids}?filter=default",
                   "note": "0 and absent are distinguished in raw/se.jsonl; "
                           "an id absent here is absent from the fetch"},
                  fh, indent=1, sort_keys=True)
        fh.write("\n")

    # 2. the control set, fixed by rule: the five SELF-arm rows with the most
    #    comments. Declared in PROTOCOL.md before this fetch ran.
    control = sorted(pop["self_arm_ids"],
                     key=lambda q: (-(counts.get(q, 0) or 0), q))[:5]
    print("G0a control set (rule: 5 SELF rows, most comments first): %s -> %s"
          % (control, [counts.get(q) for q in control]))

    # 3. question comments and key-answer comments.
    qcom, p1 = fetch_all("questions/%s/comments", qids,
                         lambda it: it["post_id"])
    acom, p2 = fetch_all("answers/%s/comments", aids,
                         lambda it: it["post_id"])
    problems += p1 + p2

    payload = {
        "control_set": control,
        "control_rule": "five SELF-arm rows of E177's population with the "
                        "highest comment_count on the default filter, ties by "
                        "ascending qid",
        "question_comments": {str(k): v for k, v in qcom.items()},
        "answer_comments": {str(k): v for k, v in acom.items()},
        "fetched": {"question_comment_threads": len(qcom),
                    "answer_comment_threads": len(acom),
                    "question_ids": len(qids), "key_answer_ids": len(aids)},
        "problems": problems,
        "quota_remaining_last": quota[-1] if quota else None,
    }
    with open(os.path.join(HERE, "comments.json"), "w") as fh:
        json.dump(payload, fh, indent=1, sort_keys=True)
        fh.write("\n")

    # G0b, reported not assumed: which of the 46 came back with no thread at
    # all, and does the comment count reconcile with the default filter.
    got_q = set(qcom)
    zero = sorted(q for q in qids if q not in got_q)
    bad = []
    for q in qids:
        n = len(qcom.get(q, []))
        if q in counts and counts[q] != n:
            bad.append((q, counts[q], n))
    print("question comment threads returned for %d of %d (no thread: %s)"
          % (len(got_q), len(qids), zero or "none"))
    print("comment_count reconciliation mismatches: %s" % (bad or "none"))
    print("key-answer comment threads: %d of %d; control set fetched: %d"
          % (len(acom), len(aids),
             sum(1 for q in control if q in got_q)))
    print("problems: %s" % (problems or "none"))
    print("quota remaining at the default-filter stage: %s"
          % (quota[-1] if quota else None))
    return 0


if __name__ == "__main__":
    sys.exit(main())