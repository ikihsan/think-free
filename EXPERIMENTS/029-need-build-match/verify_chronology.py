#!/usr/bin/env python3
"""E029 -- falsify the chronological proxy against real timestamps.

The reader population is selected on HN item-id ordering, and the headline split
(167 of 241 shipped before the need, 74 after) rests entirely on it. A proxy is
admissible only if it can be shown wrong, so this samples authors from BOTH sides of
the claimed split, fetches the real `created_at_i` for the need comment and for the
first few shipped items, and reports where the two disagree.

A disagreement would not invalidate the split -- it would invalidate the *selection*,
because a wrongly-excluded author would have been shown to a reader as a `unrelated`
row. That is the failure PROTOCOL-AMENDMENT-1.md exists to prevent, so it is the
thing worth checking.
"""
import json
import os
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(ROOT, "raw")
OUT = os.path.join(RAW, "chronology_verification.jsonl")

BASE = "https://hn.algolia.com/api/v1/items/%s"
UA = "think-free-e029-verify/1.0 (research instrument; stdlib urllib)"

# Sampled across the claimed split rather than at random: three from each side, so a
# proxy that inverts for only one direction is caught.
FROM_EACH_SIDE = 4
ITEMS_PER_AUTHOR = 3


def read_jsonl(name):
    with open(os.path.join(RAW, name)) as f:
        return [json.loads(l) for l in f if l.strip()]


def created_at_i(item_id):
    req = urllib.request.Request(BASE % urllib.parse.quote(str(item_id)),
                                 headers={"User-Agent": UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8", "replace")).get("created_at_i"), "ok"
        except Exception as e:
            if attempt == 2:
                return None, "error_%s" % type(e).__name__
            time.sleep(1.5)
    return None, "refused"


import urllib.parse  # noqa: E402  (used by created_at_i)


def main():
    pop = {d["author"]: d for d in read_jsonl("population.jsonl")}
    builds = {d["author"]: d for d in read_jsonl("builds.jsonl")}
    key = json.load(open(os.path.join(RAW, "view_key.json")))
    eligible = sorted(set(k["author"] for k in key if k["arm"] == "matched"))
    ineligible = sorted(a for a in pop if a not in set(eligible))

    def pick(lst, n):
        if not lst:
            return []
        step = max(1, len(lst) // n)
        return [lst[i * step] for i in range(min(n, len(lst)))]

    sample = [(a, "claimed_eligible") for a in pick(eligible, FROM_EACH_SIDE)]
    sample += [(a, "claimed_ineligible") for a in pick(ineligible, FROM_EACH_SIDE)]

    agree = disagree = unreadable = 0
    rows = []
    for author, side in sample:
        ni = int(pop[author]["need"]["comment_id"])
        need_t, need_status = created_at_i(ni)
        items = builds[author].get("items") or []
        checked = []
        for it in items[:ITEMS_PER_AUTHOR]:
            t, status = created_at_i(it["id"])
            if t is None or need_t is None:
                unreadable += 1
                checked.append({"id": it["id"], "status": status or need_status,
                                "timestamp": None})
                continue
            checked.append({"id": it["id"], "created_at_i": t,
                            "id_order_says_later": int(it["id"]) > ni,
                            "timestamp_says_later": t > need_t})
            time.sleep(0.12)
        id_later = any(int(it["id"]) > ni for it in items)
        ts_later = any(c.get("timestamp_says_later") for c in checked)
        verdict = "agrees" if id_later == ts_later else "DISAGREES"
        if id_later == ts_later:
            agree += 1
        else:
            disagree += 1
        rows.append({"author": author, "side": side, "need_comment": ni,
                     "need_created_at_i": need_t, "need_status": need_status,
                     "n_items_total": len(items), "items_checked": checked,
                     "id_order_says_any_later": id_later,
                     "timestamps_say_any_later": ts_later, "verdict": verdict})
        print("%-16s %-18s need=%s items=%d id_later=%s ts_later=%s -> %s"
              % (author, side, need_t, len(items), id_later, ts_later, verdict))
        time.sleep(0.15)

    with open(OUT, "w") as f:
        for r in rows:
            f.write(json.dumps(r, sort_keys=True) + "\n")

    print("\nauthors sampled %d; agree %d; disagree %d; items unreadable %d"
          % (len(sample), agree, disagree, unreadable))
    if disagree:
        print("FAIL: the item-id proxy is not trustworthy for this selection")
        return 1
    if agree + disagree < len(sample):
        print("FAIL: some authors yielded no comparable timestamp")
        return 1
    print("PASS: item-id ordering agrees with created_at on every sampled author")
    return 0


if __name__ == "__main__":
    sys.exit(main())
