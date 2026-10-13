#!/usr/bin/env python3
"""E126: validate the attempt sample against the declared rule,
then fetch the threads (answers + comments) for grading.

The rule (PROTOCOL.md + AMENDMENT-1): the attempt sample is the
20 highest-view_count answerable-class rows within Arm A.
attempts.jsonl must cover exactly that set, and every attempt must
carry attempt_first=true (written before any thread was read).

Thread fetch happens only after the attempts file exists, so the
attempt discipline is preserved by construction.
"""
import json
import os
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
API = "https://api.stackexchange.com/2.3"


def get(path, **params):
    params["site"] = "stackoverflow"
    params["filter"] = "withbody"
    url = API + path + "?" + urllib.parse.urlencode(params)
    for attempt in range(6):
        req = urllib.request.Request(
            url, headers={"User-Agent": "think-free-e126/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.load(resp)
            if data.get("backoff"):
                time.sleep(data["backoff"])
            return data
        except urllib.error.HTTPError as exc:
            if exc.code in (400, 429, 502) and attempt < 5:
                time.sleep(20 * (attempt + 1))
            else:
                raise
    raise RuntimeError("unreachable")


def main():
    screening = [json.loads(line)
                 for line in open(os.path.join(HERE, "screening.jsonl"))]
    # the declared sample: Arm A, question/answerable, top 20 by view_count
    pool = [r for r in screening
            if r["arm"] == "A_votes" and not r["dropped"]
            and r["shape"] == "question" and r["sub"] == "answerable"]
    pool.sort(key=lambda r: -r["view_count"])
    declared = pool[:20]
    declared_ids = {r["question_id"] for r in declared}

    attempts = [json.loads(line)
                for line in open(os.path.join(HERE, "attempts.jsonl"))
                if line.strip()]
    attempt_ids = {a["question_id"] for a in attempts}

    assert attempt_ids == declared_ids, (
        "sample mismatch: missing %s, extra %s"
        % (declared_ids - attempt_ids, attempt_ids - declared_ids))
    assert all(a.get("attempt_first") for a in attempts), (
        "an attempt lacks attempt_first=true")
    print("sample validated: 20 answerable rows, "
          "view_count %d..%d" % (
              min(r["view_count"] for r in declared),
              max(r["view_count"] for r in declared)))

    # fetch threads: answers (all, vote-sorted) and comments, batched
    ids = sorted(declared_ids)
    threads = {}
    for i in range(0, len(ids), 20):
        chunk = ";".join(str(q) for q in ids[i:i + 20])
        answers = get("/questions/" + chunk + "/answers",
                      sort="votes", order="desc", pagesize=100)
        for a in answers.get("items", []):
            threads.setdefault(a["question_id"], {})["answers"] = (
                threads.get(a["question_id"], {}).get("answers", [])
                + [a])
        comments = get("/questions/" + chunk + "/comments",
                       sort="votes", order="desc", pagesize=100)
        for c in comments.get("items", []):
            threads.setdefault(c["post_id"], {})["question_comments"] = (
                threads.get(c["post_id"], {}).get("question_comments", [])
                + [c])
    # also the questions themselves (accepted_answer_id, answer_count)
    qs = get("/questions/" + ";".join(str(q) for q in ids))
    for q in qs.get("items", []):
        threads.setdefault(q["question_id"], {})["question"] = q

    with open(os.path.join(HERE, "threads.json"), "w") as fh:
        json.dump(threads, fh)
    n_answered = sum(1 for t in threads.values() if t.get("question", {}).get("accepted_answer_id"))
    print("fetched threads for %d questions; %d carry an accepted answer"
          % (len(threads), n_answered))


if __name__ == "__main__":
    main()
