#!/usr/bin/env python3
"""E182 stage 1: fetch every answer score for E177's 60 scored rows.

Moves bytes only. Reads no answer body, judges nothing, and never sees an
assistant answer or an arm label: the population arrives as a flat list of
question ids and the arm labels are joined only in stage 2.

Every response body is written to raw/se.jsonl with its URL and the remaining
quota, so the quota cost and the bytes are auditable (D061). The default
answer filter is used -- it carries answer_id, question_id, score and
is_accepted, and no body, so the response is small and nothing that could be
read as an answer reaches disk.

Usage: python3 fetch.py [--limit N]   (N caps rows, for a smoke run)
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
E177 = os.path.join(os.path.dirname(os.path.dirname(HERE)),
                    "EXPERIMENTS", "177-evidence-gated-need")
SE = "https://api.stackexchange.com/2.3"
UA = "think-free-e182/1.0"

# Split by question, not by chunk index: a failure loses 20 rows, not one.
CHUNK = 20


def se(path, params, note=None):
    url = "%s/%s?%s" % (SE, path, urllib.parse.urlencode(params))
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "application/json"})
    os.makedirs(RAW, exist_ok=True)
    with urllib.request.urlopen(req, timeout=60) as fh:
        body = json.loads(fh.read().decode("utf-8"))
        # The whole header set, verbatim. A 20-row smoke run on 2026-10-18 read
        # x-ratelimit-remaining back as None on every response: the Cloudflare
        # edge in front of this endpoint returns CF-Cache-Status and does not
        # forward the ratelimit headers. Parsing two named fields would have
        # recorded "quota unknown" as if it were a measurement; storing the set
        # records the absence, which is the finding.
        head = {k: v for k, v in fh.headers.items()}
    rec = {"url": url,
           "headers": head,
           "quota_remaining": head.get("x-ratelimit-remaining"),
           "quota_reset_epoch": head.get("x-ratelimit-reset"),
           "note": note,
           "body": body}
    with open(os.path.join(RAW, "se.jsonl"), "a") as out:
        out.write(json.dumps(rec, sort_keys=True) + "\n")
    time.sleep(1.2)
    return body, rec


def quota():
    """The quota baseline and end line, from /info.

    The endpoint that does carry the budget is /info, so the cost of this
    experiment is audited through it rather than through the answers endpoint's
    stripped headers.
    """
    body, _ = se("info", {"site": "stackoverflow"}, note="quota probe")
    return {"quota_remaining": body.get("quota_remaining"),
            "backoff": body.get("backoff")}


def scored_qids():
    """The 60 rows E177 scored, from E177's own committed files.

    verdicts.jsonl keys every scored row `g-<qid>`; the `g0b-` control rows are
    excluded here so no control can leak into the population.
    """
    qids = []
    with open(os.path.join(E177, "score", "verdicts.jsonl")) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            pid = json.loads(line)["pid"]
            if pid.startswith("g0"):
                continue
            if not pid.startswith("g-"):
                raise SystemExit("unexpected pid shape: %r" % pid)
            qids.append(int(pid[2:]))
    seen, uniq = set(), []
    for q in qids:
        if q not in seen:
            seen.add(q)
            uniq.append(q)
    return uniq


def main():
    limit = None
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])

    qids = scored_qids()
    print("population: %d scored qids from E177's verdicts" % len(qids))
    if limit:
        qids = qids[:limit]
        print("  capped to %d for this run" % limit)

    scores, last = {}, None
    q_before = quota()
    print("quota before: %s (backoff %s)" % (q_before["quota_remaining"],
                                              q_before["backoff"]))
    done = 0
    for i in range(0, len(qids), CHUNK):
        part = qids[i:i + CHUNK]
        page, more = 1, True
        got = 0
        while more:
            ans, last = se("questions/%s/answers"
                           % ";".join(str(q) for q in part),
                           {"site": "stackoverflow", "pagesize": 100,
                            "sort": "votes", "page": page})
            items = ans.get("items", [])
            for a in items:
                scores.setdefault(a["question_id"], []).append(
                    {"answer_id": a.get("answer_id"),
                     "score": a.get("score"),
                     "is_accepted": a.get("is_accepted")})
                got += 1
            more = bool(ans.get("has_more"))
            if more:
                page += 1
        done += 1
        print("  chunk %d: qids %d..%d -> %d answers"
              % (done, part[0], part[-1], got))
    q_after = quota()
    print("quota after: %s" % q_after["quota_remaining"])

    out = {"rows": {str(q): scores.get(q, []) for q in qids},
           "population_sha256": hashlib.sha256(
               json.dumps(qids).encode()).hexdigest(),
           "quota_before": q_before,
           "quota_after": q_after,
           "note": "scores only, default filter, no answer body on disk"}
    with open(os.path.join(HERE, "scores.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")

    complete = sum(1 for v in out["rows"].values() if v)
    print("scores.json: %d of %d rows carry an answer score vector"
          % (complete, len(qids)))
    print("population digest %s" % out["population_sha256"][:16])
    return 0


if __name__ == "__main__":
    sys.exit(main())