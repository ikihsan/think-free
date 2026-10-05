#!/usr/bin/env python3
"""E029 -- build one reader view per reader: 74 matched + 74 mismatched, shuffled.

Protocol: EXPERIMENTS/029-need-build-match/PROTOCOL.md and
PROTOCOL-AMENDMENT-1.md (both declared before any reader ran).

A reader sees exactly two things -- the need statement verbatim, and the titles and
urls the same person shipped after it. It never sees the author's name, the story
title, the thread, the author's item count, or which of the two arms a row is in.
The arm label is not written into the view at all; the key that recovers it is
written to a separate file the reader is never given.

The story-title arm is built here too, because that is the arm that can kill H1, and
it is scored by the same reader with the same rubric and the same blindness.
"""
import json
import os
import random
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(ROOT, "raw")
POPULATION = os.path.join(RAW, "population.jsonl")
BUILDS = os.path.join(RAW, "builds.jsonl")
STORIES = os.path.join(RAW, "stories.jsonl")

SEED = 2901


def read_jsonl(path):
    with open(path) as f:
        return [json.loads(l) for l in f if l.strip()]


def load():
    pop = {d["author"]: d for d in read_jsonl(POPULATION)}
    builds = {d["author"]: d for d in read_jsonl(BUILDS)}
    stories = {d["story_id"]: d for d in read_jsonl(STORIES)}
    return pop, builds, stories


def later_items(author, need, builds):
    """Every tag-verified show_hn item that postdates the need statement."""
    ni = int(need["comment_id"])
    out = []
    for it in builds.get(author, {}).get("items") or []:
        if int(it["id"]) > ni:
            out.append(it)
    return out


def render(need_text, items):
    lines = ["NEED", need_text, "", "SHIPPED"]
    if not items:
        lines.append("(this person has not posted a Show HN item since)")
    for it in items:
        lines.append("title: %s" % (it.get("title") or "(no title)"))
        lines.append("url: %s" % (it.get("url") or "(no url)"))
    return "\n".join(lines)


def main():
    pop, builds, stories = load()

    eligible = []
    for a, r in pop.items():
        items = later_items(a, r["need"], builds)
        if items:
            eligible.append({"author": a, "need": r["need"], "items": items})
    eligible.sort(key=lambda e: e["author"])

    no_later = sorted(set(pop) - set(e["author"] for e in eligible))
    sys.stderr.write("eligible with a later build: %d ; without: %d\n"
                     % (len(eligible), len(no_later)))

    # The mismatched arm's partner pool is restricted to authors who also have a build
    # postdating their own need. Drawn from all 241, 45 of the 74 mismatched rows
    # rendered an empty SHIPPED section and could only be labelled `unrelated`, which
    # depresses the control by construction and would hand C1 an artifact (amendment 2).
    pool = sorted(e["author"] for e in eligible)
    rng = random.Random(SEED)
    shuffled_pool = pool[:]
    rng.shuffle(shuffled_pool)
    if len(shuffled_pool) != len(pool) or len(set(shuffled_pool)) != len(pool):
        sys.stderr.write("FAIL: the partner pool is not a permutation of the population\n")
        return 1
    # Sattolo's algorithm on the index list: for i from n-1 down to 1, swap index i
    # with a uniformly chosen index in [0, i). This produces a single cycle over all n
    # elements, so sigma(i) != i for every i when n >= 2 -- exactly the derangement the
    # mismatched arm needs.
    #
    # The first version of this file shifted a shuffled *name* list by one index and
    # asserted the result had no fixed point. It did not: shifting asks whether a name
    # sits in its own slot, not whether a name lands on its own author's row, so it
    # self-paired one author at random and the assertion caught it. Deranging the
    # indices removes the distinction between the two questions.
    sigma = list(range(len(pool)))
    for i in range(len(sigma) - 1, 0, -1):
        j = rng.randrange(i)
        sigma[i], sigma[j] = sigma[j], sigma[i]
    if any(sigma[i] == i for i in range(len(sigma))):
        sys.stderr.write("FAIL: Sattolo index derangement has a fixed point\n")
        return 1
    partner = {pool[i]: pool[sigma[i]] for i in range(len(pool))}
    fixed = [a for a in partner if partner[a] == a]
    if fixed:
        sys.stderr.write("FAIL: derangement has %d fixed point(s), e.g. %s\n"
                         % (len(fixed), fixed[:3]))
        return 1

    rows, key = [], []
    for i, e in enumerate(eligible):
        rows.append({"row_id": "M%02d" % i, "body": render(e["need"]["text"], e["items"])})
        key.append({"row_id": "M%02d" % i, "arm": "matched", "author": e["author"],
                    "story_id": e["need"]["story_id"]})
    n = len(eligible)
    for i, e in enumerate(eligible):
        # A MISMATCHED pair is the matched author's own need beside a DIFFERENT author's
        # shipped items. The first version of this file rendered the PARTNER's own need
        # beside the PARTNER's own items -- which is a matched pair for the partner, so
        # the control was a relabelled replicate of the treatment arm. That is why the
        # two arms returned byte-identical lexical statistics (amendment 3).
        other = partner[e["author"]]
        rows.append({"row_id": "X%02d" % i,
                     "body": render(e["need"]["text"],
                                    later_items(other, pop[other]["need"], builds))})
        key.append({"row_id": "X%02d" % i, "arm": "mismatched", "author": e["author"],
                    "partner": other, "story_id": e["need"]["story_id"]})

    # The story-title arm: same shipped items, paired with the title of the thread the
    # author's own need was posted in. This is the control that can kill H1.
    for i, e in enumerate(eligible):
        sid = e["need"]["story_id"]
        st = stories.get(sid) or {}
        title = st.get("title") or "(story title unavailable)"
        rows.append({"row_id": "T%02d" % i, "body": render(title, e["items"])})
        key.append({"row_id": "T%02d" % i, "arm": "story_title", "author": e["author"],
                    "story_id": sid})

    order = list(range(len(rows)))
    rng.shuffle(order)
    shuffled = [rows[j] for j in order]

    for reader in ("r1", "r2"):
        with open(os.path.join(RAW, "view_%s.txt" % reader), "w") as f:
            f.write("# E029 reader view -- see RUBRIC.md. One label per row.\n")
            f.write("# Output: row_id<TAB>label<TAB>capability<TAB>what_it_is\n")
            for j, r in enumerate(shuffled):
                f.write("\n===== ROW %d | id %s =====\n%s\n" % (j + 1, r["row_id"], r["body"]))
        sys.stderr.write("wrote raw/view_%s.txt with %d rows\n" % (reader, len(shuffled)))

    with open(os.path.join(RAW, "view_key.json"), "w") as f:
        json.dump(key, f, indent=1, sort_keys=True)
    sys.stderr.write("wrote raw/view_key.json (%d rows)\n" % len(key))
    return 0


if __name__ == "__main__":
    sys.exit(main())
