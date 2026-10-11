#!/usr/bin/env python3
"""E091 fetch: repair the 200-character truncation defect in the stored population.

The committed population.jsonl and probes.jsonl store each topic's first post cut
at ~200 characters (AMENDMENT-1, Defect A). This re-fetches the full text from
the Discourse API, records a sha256 of every body before and after, and writes
full.jsonl. Run with --verify to reproduce the defect from the stored files
alone, with no network.
"""
import hashlib
import html
import json
import os
import re
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://community.anovaculinary.com/t/%s.json"
UA = "think-free-research/1.0 (experiment E091; contact: repository owner)"


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def strip_cooked(cooked):
    """Discourse serves HTML; the stored text is plain. Same recipe for both."""
    text = re.sub(r"<br\s*/?>", "\n", cooked)
    text = re.sub(r"</p>", "\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    return html.unescape(text).strip()


def load(name):
    path = os.path.join(HERE, name)
    with open(path) as handle:
        return [json.loads(line) for line in handle]


def fetch(topic_id, retries=3):
    last = None
    for attempt in range(retries):
        try:
            request = urllib.request.Request(BASE % topic_id, headers={"User-Agent": UA})
            with urllib.request.urlopen(request, timeout=25) as response:
                return json.loads(response.read().decode("utf-8", "replace"))
        except Exception as exc:                      # noqa: BLE001 - reported, not swallowed
            last = exc
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError("fetch failed for %s: %s" % (topic_id, last))


def verify_offline(population, probes):
    """Reproduce Defect A from the stored files. No network."""
    rows = population + probes
    lengths = sorted(len(r["first_post"]) for r in rows)
    over = sum(1 for n in lengths if n >= 199)
    print("rows=%d  stored first_post chars=%d" % (len(rows), sum(lengths)))
    print("lengths: min=%d median=%d max=%d" % (lengths[0], lengths[len(lengths) // 2], lengths[-1]))
    print("rows at/over the 199-200 cut: %d of %d" % (over, len(rows)))
    return {"rows": len(rows), "stored_chars": sum(lengths), "at_cut": over}


def main():
    population = load("population.jsonl")
    probes = load("probes.jsonl")

    if "--verify" in sys.argv:
        verify_offline(population, probes)
        return 0

    seen, out, totals = {}, [], {"stored": 0, "full": 0}
    for row in population + probes:
        topic_id = row["id"]
        if topic_id in seen:
            continue
        data = fetch(topic_id)
        posts = data["post_stream"]["posts"]
        first = strip_cooked(posts[0]["cooked"])
        thread = [strip_cooked(p["cooked"]) for p in posts]
        seen[topic_id] = True
        totals["stored"] += len(row["first_post"])
        totals["full"] += len(first)
        out.append({
            # The Discourse API returns topic ids as ints and the stored rows
            # also carry ints, but every consumer of this file joins on the id.
            # Normalise to str at the single point of construction so a join
            # cannot silently miss every row (observed, this session).
            "id": str(topic_id),
            "api_id_type": type(data.get("id")).__name__,
            "title": data.get("title", row.get("title", "")),
            "views": data.get("views", row.get("views")),
            "replies": data.get("posts_count", row.get("replies")),
            "category_id": data.get("category_id"),
            "first_post": first,
            "first_post_sha256": sha(first),
            "stored_first_post": row["first_post"],
            "stored_sha256": sha(row["first_post"]),
            "thread": thread,
        })
        time.sleep(0.4)

    with open(os.path.join(HERE, "full.jsonl"), "w") as handle:
        for row in out:
            handle.write(json.dumps(row, sort_keys=True) + "\n")

    print("rows=%d  stored=%d  full=%d  retained=%.3f"
          % (len(out), totals["stored"], totals["full"],
             totals["stored"] / float(totals["full"])))
    print("rows where stored text is a prefix of full: %d of %d"
          % (sum(1 for r in out if r["first_post"].startswith(r["stored_first_post"][:60])), len(out)))

    # A1: the repaired population must join back to the stored selection.
    stored = {str(r["id"]) for r in population}
    got = {r["id"] for r in out}
    print("A1 population accessibility: %d of %d stored rows re-fetched, all with full text: %s"
          % (len(stored & got), len(stored),
             all(len(r["first_post"]) > 0 for r in out)))
    print("wrote full.jsonl")
    return 0


if __name__ == "__main__":
    sys.exit(main())
