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


def fetch_all(endpoint, ids, key, pagesize=100):
    """Fetch `endpoint` for ids in chunks, paging to exhaustion.

    AMENDMENT-2: the first run read one page per chunk and printed no warning
    when `has_more` was true, truncating sixteen of the 46 rows. Pages are now
    followed and every page's `has_more` and item count is in raw/se.jsonl.
    """
    got, problems, paged = {}, [], []
    for part in chunks(ids, 20):
        page = 1
        while True:
            rec = se(endpoint % ";".join(str(i) for i in part),
                     {"site": SITE, "filter": "withbody",
                      "pagesize": pagesize, "page": page})
            for it in rec["body"].get("items", []):
                got.setdefault(key(it), []).append(it)
            if not rec["has_more"]:
                break
            paged.append((part[0], page))
            page += 1
            if page > 20:
                problems.append("%s: gave up after 20 pages for chunk %d"
                                % (endpoint, part[0]))
                break
    return got, problems, paged


def refetch_agreement(endpoint, ids, key, got):
    """Re-fetch with a different page size; the totals must agree.

    The pagination loop above writes `has_more` to disk and trusts it. This is
    the check that does not trust it: same ids, `pagesize=50`, compare totals.
    """
    again, _, _ = fetch_all(endpoint, ids, key, pagesize=50)
    diffs = []
    for qid, items in again.items():
        if len(items) != len(got.get(qid, [])):
            diffs.append((qid, len(got.get(qid, [])), len(items)))
    for qid, items in got.items():
        if qid not in again:
            diffs.append((qid, len(items), 0))
    return again, diffs


def main():
    pop = json.load(open(os.path.join(HERE, "population.json")))
    qids = [e["qid"] for e in pop["population"]]
    aids = [e["key_answer_id"] for e in pop["population"]
            if e["key_answer_id"]]
    problems, quota = [], []

    # AMENDMENT-2: stage 1 (the default-filter question fetch for a comment
    # count) is withdrawn. Neither `default` nor `withbody` carries
    # `comment_count`, so the "0 on 98 rows" it produced was an absent field
    # read as zero, and the G0a control set was ordered on that fiction. The
    # control set is now ordered on the comments this script fetches, which is
    # the rule PROTOCOL.md already declared with a different instrument.

    # 1. question comments and key-answer comments for the 46.
    qcom, p1, pg1 = fetch_all("questions/%s/comments", qids,
                              lambda it: it["post_id"])
    acom, p2, pg2 = fetch_all("answers/%s/comments", aids,
                              lambda it: it["post_id"])
    problems += p1 + p2

    # 2. the G0a control set, fixed by rule: the five SELF-arm rows with the
    #    most comments. Needs the whole SELF arm's comments (AMENDMENT-2).
    scom, p3, pg3 = fetch_all("questions/%s/comments", pop["self_arm_ids"],
                              lambda it: it["post_id"])
    problems += p3
    counts = {q: len(v) for q, v in qcom.items()}
    scounts = {q: len(v) for q, v in scom.items()}
    control = sorted(pop["self_arm_ids"],
                     key=lambda q: (-scounts.get(q, 0), q))[:5]
    print("G0a control set (rule: 5 SELF rows, most comments first): %s -> %s"
          % (control, [scounts.get(q, 0) for q in control]))
    print("SELF arm comment counts, top 10 by count: %s"
          % sorted(scounts.items(), key=lambda kv: (-kv[1], kv[0]))[:10])

    # 3. G0b part 3, the check that does not trust the paging loop: the
    #    paged endpoints are re-fetched at pagesize 50 and the totals must
    #    agree. Both endpoints are re-fetched whole, so the check also covers
    #    the chunks that did not page.
    q2, diffq = refetch_agreement("questions/%s/comments", qids,
                                  lambda it: it["post_id"], qcom)
    a2, diffa = refetch_agreement("answers/%s/comments", aids,
                                  lambda it: it["post_id"], acom)

    payload = {
        "control_set": control,
        "control_rule": "five SELF-arm rows of E177's population with the most "
                        "question comments in the fetched thread, ties by "
                        "ascending qid (AMENDMENT-2: the ordering instrument "
                        "changed, the rule did not)",
        "control_comments": {str(k): scom.get(k, []) for k in control},
        "self_arm_comment_counts": {str(k): v for k, v in scounts.items()},
        "question_comments": {str(k): v for k, v in qcom.items()},
        "answer_comments": {str(k): v for k, v in acom.items()},
        "fetched": {"question_comment_threads": len(qcom),
                    "answer_comment_threads": len(acom),
                    "self_arm_comment_threads": len(scom),
                    "question_ids": len(qids), "key_answer_ids": len(aids)},
        "paged": {"question": pg1, "answer": pg2, "self_arm": pg3},
        "pagesize_agreement": {"question": diffq, "answer": diffa},
        "problems": problems,
    }
    with open(os.path.join(HERE, "comments.json"), "w") as fh:
        json.dump(payload, fh, indent=1, sort_keys=True)
        fh.write("\n")

    # G0b, reported not assumed: which of the 46 came back with no thread at
    # all, which chunks paged, and whether a different page size agrees.
    zero = sorted(q for q in qids if q not in qcom)
    print("question comment threads returned for %d of %d; %d with no "
          "comments: %s" % (len(qcom), len(qids), len(zero), zero))
    print("chunks that paged: question %s, answer %s, self_arm %s"
          % (pg1, pg2, pg3))
    print("pagesize-50 re-fetch disagreements: question %s, answer %s"
          % (diffq or "none", diffa or "none"))
    print("key-answer comment threads: %d of %d; total question comments %d"
          % (len(acom), len(aids), sum(counts.values())))
    print("problems: %s" % (problems or "none"))
    if os.path.exists(os.path.join(RAW, "se.jsonl")):
        recs = [json.loads(l) for l in open(os.path.join(RAW, "se.jsonl"))]
        print("requests on disk: %d; quota_remaining on the last: %s"
              % (len(recs), recs[-1]["body"].get("quota_remaining")))
    return 0


if __name__ == "__main__":
    sys.exit(main())