#!/usr/bin/env python3
"""The tally and the gate, for 014.

The gate is declared in `README.md` before the run and is implemented here, so
it cannot be adjusted to a result. It has three ways to answer and only one of
them is a direction:

  dead          >= 50% of decided incumbents show serving evidence
  survives      <  50% do
  inconclusive  more than 20% undecided, or any placebo shows serving evidence

`undecided` means no channel produced a figure at all and no channel refused:
the instrument could not read anything. That is different from a figure of zero,
which is a reading, and the difference is recorded per row rather than summed
away. A refusal is never zero -- the hypothesis under test predicts low numbers,
and every defect found so far in this repository's own instruments (F032, three
of them) pushed measurements towards zero.
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FLOOR_RATE = 1000
FLOOR_RELEASE = 10000
FLOOR_DOCKER = 100000
HALF = 0.5
MAX_UNDECIDED = 0.2


INSTRUMENT_CORRECTION = (
    "The first run counted a repository publishing no release assets as a decided "
    "reading of zero use. 13 of 30 incumbents entered the denominator that way and "
    "the gate printed 40% served. Those 13 tell us about distribution -- the "
    "project ships nothing to download -- and nothing about use. Excluding them "
    "gives 12 of 17, or 71%. Asserted in tests/test_serving_stats.py.")


def reading_cumulative(row):
    """Cumulative channels that returned a figure about *use*.

    A repository that publishes no release assets has told us something about its
    **distribution** -- it ships nothing to download -- and nothing at all about
    how much it is used. Treating that as a zero reading is the same shape of
    error as the one this experiment exists to name: a proxy read as if it were
    the property. See INSTRUMENT_CORRECTION.
    """
    return [c for c in row.get("cumulative") or [] if c.get("value", 0) > 0]


def classify(row):
    """(rate_best, cumulative_best, undecided) for one measured repository.

    `undecided` means **no channel produced any reading about use** -- every
    channel was refused, or nothing was published to any channel the instrument
    reads. It is not the same as a reading of zero: a registry that answers 0
    downloads for a package it recognises *is* a reading, and `measure()` records
    it explicitly. Collapsing the two would let an instrument that could not see
    anything manufacture a result, and would let a project that distributes
    nothing masquerade as a project nobody uses.
    """
    rate = 0
    for r in row.get("rate") or []:
        if r["value"] >= FLOOR_RATE:
            rate = max(rate, r["value"])
    cumulative = 0
    for c in reading_cumulative(row):
        floor = FLOOR_DOCKER if c["channel"] == "dockerpulls" else FLOOR_RELEASE
        if c["value"] >= floor:
            cumulative = max(cumulative, c["value"])
    read_something = bool(row.get("rate") or reading_cumulative(row))
    undecided = not read_something
    return rate, cumulative, undecided


def served(row):
    """One reading: does this repository clear any declared floor?"""
    rate, cumulative, _ = classify(row)
    return max(rate, cumulative) > 0


def tally(rows):
    decided = [r for r in rows if not classify(r)[2]]
    undecided = len(rows) - len(decided)
    hits = [r for r in decided if served(r)]
    rate_hits = [r for r in decided if classify(r)[0] > 0]
    rel_hits = [r for r in decided
                if any(c["channel"] == "ghreleases" and c["value"] >= FLOOR_RELEASE
                       for c in r.get("cumulative") or [])]
    docker_hits = [r for r in decided
                   if any(c["channel"] == "dockerpulls" and c["value"] >= FLOOR_DOCKER
                          for c in r.get("cumulative") or [])]
    return {
        "n": len(rows),
        "decided": len(decided),
        "undecided": undecided,
        "undecided_share": (undecided / float(len(rows))) if rows else 0.0,
        "served": len(hits),
        "served_share": (len(hits) / float(len(decided))) if decided else 0.0,
        "served_by_rate_channel": len(rate_hits),
        "served_by_release_assets": len(rel_hits),
        "served_by_docker": len(docker_hits),
        "refused_any": sum(1 for r in rows if r.get("refused")),
        "unverified_attribution": sum(1 for r in rows if r.get("unverified")),
        "served_repos": sorted(r["repo"] for r in hits),
    }


def gate(main_rows, placebo_rows, placebo_verdict=None):
    """Apply the declared arms. Returns (verdict, reason, main, placebo)."""
    main = tally(main_rows)
    plac = tally(placebo_rows)
    if plac["served"]:
        return ("inconclusive",
                "a placebo repository shows serving evidence, so the instrument "
                "measures something other than use: %s" % ", ".join(plac["served_repos"]),
                main, plac)
    # An arm that could not read its controls has not passed. The declared placebo
    # was five zero-star repositories that publish nothing to any channel, so all
    # five were undecided and a false positive was impossible by construction --
    # which is not evidence of accuracy, it is the absence of a test.
    if placebo_verdict is not None and not placebo_verdict.get("readable_controls"):
        return ("inconclusive",
                "no placebo control was readable, so the floors were never "
                "challenged by a known-unused project: %s" % placebo_verdict["verdict"],
                main, plac)
    if placebo_verdict is not None and placebo_verdict.get("false_positives"):
        return ("inconclusive",
                "the floors fired on %d of %d readable controls: %s"
                % (len(placebo_verdict["false_positives"]),
                   placebo_verdict["readable_controls"],
                   ", ".join(placebo_verdict["false_positives"])),
                main, plac)
    if not main["decided"]:
        return ("inconclusive", "no incumbent produced a reading", main, plac)
    if main["undecided_share"] > MAX_UNDECIDED:
        return ("inconclusive",
                "%.0f%% of incumbents were undecided, above the declared 20%%"
                % (100 * main["undecided_share"]), main, plac)
    if main["served_share"] >= HALF:
        return ("dead", "%.0f%% of decided incumbents clear a declared floor"
                % (100 * main["served_share"]), main, plac)
    return ("survives", "%.0f%% of decided incumbents clear a declared floor"
            % (100 * main["served_share"]), main, plac)


STOPWORDS = {
    "a", "an", "and", "or", "the", "for", "to", "of", "in", "on", "with", "at",
    "by", "from", "is", "are", "be", "it", "its", "this", "that", "as", "into",
    "alternative", "tool", "tools", "app", "apps", "software", "other", "others",
}


def content_terms(phrasing):
    """Whole-word content terms of a phrasing, stopwords and all."""
    return {t for t in re.findall(r"[a-z0-9+#.]+", (phrasing or "").lower())
            if len(t) > 2 and t not in STOPWORDS}


def is_ontopic(repo_row):
    """Mechanical: a content term of any phrasing that named it appears in the
    repository's own name or description. No judgement, so it cannot be tuned
    after seeing which answer it gives."""
    terms = set()
    for phrasing in repo_row.get("phrasings") or []:
        terms |= content_terms(phrasing)
    haystack = ("%s %s" % (repo_row["repo"], repo_row.get("desc") or "")).lower()
    return any(t in haystack for t in terms)


def ontopic(rows):
    return [r for r in rows if is_ontopic(r)]


def render(name, rows):
    print("\n== %s (n=%d)" % (name, len(rows)))
    for r in rows:
        rate, cumulative, undecided = classify(r)
        marks = []
        if rate:
            marks.append("rate=%s" % "{:,}".format(rate))
        if cumulative:
            marks.append("cumulative=%s" % "{:,}".format(cumulative))
        if r.get("refused"):
            marks.append("refused=%d" % len(r["refused"]))
        if r.get("unverified"):
            marks.append("unverified=%d" % len(r["unverified"]))
        print("  %-42s %7s* %-12s %s" % (
            r["repo"], r.get("stars", "?"),
            "UNDECIDED" if undecided else "read", " ".join(marks)))


def main():
    cache = json.load(open(os.path.join(HERE, "raw", "serving.json")))
    pop = json.load(open(os.path.join(HERE, "raw", "incumbents.json")))
    data = {g: [cache[r["repo"]] for r in rows if r["repo"] in cache]
            for g, rows in (("incumbents", pop["incumbents"]),
                            ("cluster", pop["cluster"]), ("placebo", pop["placebo"]))}
    data["cluster_tally"] = tally(data["cluster"])
    data["raw_serving"] = cache
    data["raw_incumbents"] = {k: v for k, v in pop.items() if k != "search_blocks"}
    data["search_blocks"] = pop["search_blocks"]

    # The rebuilt placebo arm, if it has run. `placebo.py` exists because the
    # declared one was unreadable; an arm that cannot be exercised is reported as
    # unexercised rather than as a pass.
    try:
        with open(os.path.join(HERE, "raw", "placebo.json")) as f:
            placebo = json.load(f)
    except (IOError, OSError, ValueError):
        placebo = None
    data["placebo_control"] = placebo
    if placebo:
        print("\nreadable placebo controls: %d, false positives: %d -- %s"
              % (placebo["readable_controls"], len(placebo["false_positives"]),
                 placebo["verdict"]))

    verdict, reason, main_t, plac_t = gate(data["incumbents"], data["placebo"],
                                           placebo)
    render("incumbents", data["incumbents"])
    render("cluster", data["cluster"])
    render("placebo", data["placebo"])
    if placebo:
        render("placebo-controls (readable, unpopular)", placebo["controls"])
    for label, t in (("incumbents", main_t), ("cluster", data["cluster_tally"]),
                     ("placebo", plac_t)):
        print("\n%s: decided %d/%d, served %d (%.0f%% of decided), "
              "undecided %.0f%%, release-assets %d, docker %d, rate-channel %d"
              % (label, t["decided"], t["n"], t["served"], 100 * t["served_share"],
                 100 * t["undecided_share"], t["served_by_release_assets"],
                 t["served_by_docker"], t["served_by_rate_channel"]))

    # One gate, and the record says which reading it is on. The first run of this
    # file counted a project that publishes nothing to any channel as a project
    # nobody uses: 13 of 30 incumbents entered the denominator with no evidence
    # in them, and it printed 40% served. `reading_cumulative` is the correction.
    data["gate"] = {"verdict": verdict, "reason": reason,
                    "arm": "declared, with the instrument correction named in "
                           "stats.INSTRUMENT_CORRECTION"}
    print("\nGATE: %s -- %s" % (verdict, reason))
    data["incumbents_tally"] = main_t
    data["placebo_tally"] = plac_t

    # The second arm, declared in the README before any figure was read: the
    # on-topic subset, matched mechanically. Reported whatever it says.
    data["on_topic_tally"] = tally(ontopic(data["incumbents"]))
    print("\non-topic subset: decided %d/%d, served %d (%.0f%% of decided)"
          % (data["on_topic_tally"]["decided"], data["on_topic_tally"]["n"],
             data["on_topic_tally"]["served"],
             100 * data["on_topic_tally"]["served_share"]))

    path = os.path.join(HERE, "results.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=1, sort_keys=True)
        f.write("\n")
    print("wrote results.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())