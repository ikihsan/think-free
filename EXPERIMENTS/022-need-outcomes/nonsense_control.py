#!/usr/bin/env python3
"""E022: the nonsense control C3.

F036 recorded a web instrument that answered HTTP 200 with ten well-formed,
wholly unrelated results for each of 38 queries, and nothing inside such a
capture distinguishes it from a real one. This asks the reader for the reply tree
of comment ids that do not exist.

  * a `200` with a parsed object carrying a reply count  -> the reader invents
    facts and the capture cannot be trusted; that is a REFUSAL of the arm
  * a 404/400                                         -> the reader tells lies

Either way the arm is refused and no rate is reported from it. Recorded before
the rates are computed.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from run import fetch_item  # noqa: E402

OUT = os.path.join(HERE, "raw", "nonsense_control.json")
FABRICATED = ["99999999999999", "88888888888888", "77777777777777"]


def main():
    import urllib.request
    results = []
    for fake in FABRICATED:
        status, item = fetch_item(fake)
        with urllib.request.urlopen(
                "https://hacker-news.firebaseio.com/v0/item/%s.json" % fake,
                timeout=20) as r:
            body = r.read().decode()
        results.append({
            "id": fake,
            "status": status,
            "body": body.strip()[:80],
            "http": r.status,
            "carries_reply_count": bool(item.get("kids")) if isinstance(item, dict) else False,
        })
        print("%s -> status=%s http=%s body=%r" % (fake, status, r.status, body.strip()[:40]))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump({
            "control": "C3_nonsense_ids",
            "ids": results,
            "verdict": ("reader_invents_facts"
                        if any(r["carries_reply_count"] for r in results)
                        else "reader_reports_absence"),
        }, f, indent=1, sort_keys=True)

    verdict = json.load(open(OUT))["verdict"]
    print("verdict: %s" % verdict)
    if verdict == "reader_invents_facts":
        print("CONTROL FAILED: the reader returns content for a nonexistent id.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
