#!/usr/bin/env python3
"""E143 fetch-threads: fetch answers for the 20 attempt-sample questions.

Runs AFTER attempts.jsonl is committed (attempt discipline). Raw JSON is
saved to threads-raw.json; grading reads the converged answer.
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
API = "https://api.stackexchange.com/2.3/questions"


def fetch_answers(qid):
    params = {
        "site": "stats",
        "order": "desc",
        "sort": "votes",
        "filter": "withbody",
    }
    url = f"{API}/{qid}/answers?" + urllib.parse.urlencode(params)
    for attempt in range(6):
        req = urllib.request.Request(
            url, headers={"User-Agent": "think-free-e143/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.load(resp)
            if data.get("backoff"):
                print(f"backoff {data['backoff']}s", file=sys.stderr)
                time.sleep(data["backoff"])
            return data
        except urllib.error.HTTPError as exc:
            body = exc.read().decode()[:200]
            print(f"HTTP {exc.code} on qid {qid}: {body}", file=sys.stderr)
            if exc.code in (400, 429, 502) and attempt < 5:
                wait = 20 * (attempt + 1)
                print(f"waiting {wait}s", file=sys.stderr)
                time.sleep(wait)
            else:
                raise
    raise RuntimeError("unreachable")


def main():
    attempts = [json.loads(l) for l in open(os.path.join(HERE, "attempts.jsonl"))]
    out = {}
    for a in attempts:
        qid = a["question_id"]
        data = fetch_answers(qid)
        items = data.get("items", [])
        out[str(qid)] = {
            "n_answers": len(items),
            "answers": [
                {"score": i.get("score"), "is_accepted": i.get("is_accepted"),
                 "body": i.get("body", "")}
                for i in items
            ],
        }
        print(f"qid {qid}: {len(items)} answers, quota {data.get('quota_remaining')}",
              file=sys.stderr)
        time.sleep(0.5)  # gentle on the quota
    with open(os.path.join(HERE, "threads-raw.json"), "w") as fh:
        json.dump(out, fh)
    print("wrote threads-raw.json", file=sys.stderr)


if __name__ == "__main__":
    main()
