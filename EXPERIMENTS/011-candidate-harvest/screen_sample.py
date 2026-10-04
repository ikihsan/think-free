#!/usr/bin/env python3
"""Attach a cause of death to each item in the mechanically-drawn sample.

The verdicts below are judgements, not measurements, and are labelled as such
wherever they are used. Two things make them more than opinion:

  * the sample itself is drawn by `sample_needs.py` under a stated rule, so no
    item was picked for looking promising;
  * the `prior_art` verdicts that could carry weight are re-checked against a
    countable source by `prior_art_probe.py` and `prior_art_probe2.py`.

Causes are the categories the record already uses for the sixteen candidates the
six sealed reports produced, so the two generators can be compared directly.
The one category with no counterpart in that record is `single_reporter` /
`vague`, and it is where most of the difference between the two generators shows
up -- which is the finding, and the reason these counts matter.

CAUSES
  prior_art           a tool already serves it
  vague               the clause does not state a mechanism, so nothing can be tested
  not_a_software_need it asks for a regulation, a price, a community, or a document
  needs_hardware      the mechanism needs a device, a room, or a person
  survives_screen_1_3 passed both screens; see README.md

Run from this directory:

    python3 screen_sample.py
"""
import json
import sys
import os


HERE = os.path.dirname(os.path.abspath(__file__))


def path(*parts):
    """Resolve a data path next to this script.

    The evidence is only reproducible if it can be re-run from anywhere, so the
    raw files are addressed relative to the script rather than to the caller's
    working directory.
    """
    return os.path.join(HERE, *parts)


# index -> (short name, cause, one-line reason)
VERDICTS = {
    0: ("hn-client", "prior_art", "HN clients already exist; the ask needs HN's own cooperation"),
    1: ("atomic-distro", "prior_art", "Silverblue, Bazzite, Talos and similar exist"),
    2: ("unclear-2", "vague", "no mechanism stated anywhere in the comment"),
    3: ("webp-encode", "prior_art", "libwebp and libvips are fast; the complaint is about one implementation"),
    4: ("low-fee-card", "not_a_software_need", "asks for a payment network's interchange economics"),
    5: ("agent-memory", "prior_art", "mem0, Letta, Agno and per-vendor resume files all serve this"),
    6: ("architecture-photos", "vague", "an aesthetic disagreement, no mechanism"),
    7: ("runtime-instrumentation", "prior_art", "eBPF plus OpenTelemetry sample decisions at runtime"),
    8: ("flashcards", "prior_art", "Anki plus an LLM is widely available"),
    9: ("political-framing", "not_a_software_need", "an argument about a person"),
    10: ("joke-10", "vague", "a joke; no need is stated"),
    11: ("age-proof", "needs_hardware", "anonymous age credentials need real issuers, regulators and users"),
    12: ("hn-tagging", "prior_art", "flags and lists already carry this in HN clients"),
    13: ("community-emphasis", "not_a_software_need", "asks HN to change what it posts"),
    14: ("atproto-pds", "prior_art", "ATProto directory and handle resolution exist"),
    15: ("device-id", "vague", "asks to change one vendor's identifier settings"),
    16: ("word-game", "prior_art", "many open clones"),
    17: ("social-space", "not_a_software_need", "asks for a different social norm"),
    18: ("natural-language-solvers", "vague", "no mechanism; a complaint about default behaviour"),
    19: ("stunts", "vague", "no mechanism"),
    20: ("game-browser", "vague", "no mechanism; specific to one game"),
    21: ("soldering-tips", "needs_hardware", "needs a soldering iron and a tip"),
    22: ("support-tickets", "not_a_software_need", "describes a behaviour, asks for a culture change"),
    23: ("context-free-23", "vague", "the clause has no subject"),
    24: ("manifesto", "not_a_software_need", "asks for a document to read"),
    25: ("sf-internet", "vague", "the clause has no subject"),
    26: ("scraper-trap", "prior_art", "the commenter shipped one and others exist"),
    27: ("agent-inline-27", "vague", "no mechanism stated"),
    28: ("philosophy-doc", "not_a_software_need", "asks for a rationale document"),
    29: ("webmcp-a11y", "not_a_software_need", "asks a standards body a question"),
    30: ("bulk-seed-books", "prior_art", "calibre, OPDS and Kavita serve this"),
    31: ("security-practices", "not_a_software_need", "asks for guidance to be trustworthy"),
    32: ("youth-vote", "not_a_software_need", "an observation about an election"),
    33: ("ad-backgrounds", "not_a_software_need", "asks for regulation"),
    34: ("url-popularity", "prior_art", "PRISTI, Common Crawl link data and commercial backlink indexes all exist"),
    35: ("cpp-subset-linter", "prior_art", "clang-tidy, IWYU and -Werror cover the enforceable part"),
    36: ("s3-alternative", "prior_art", "Garage, MinIO, SeaweedFS and others"),
    37: ("toggle-per-site", "vague", "no mechanism stated"),
    38: ("cheap-monitoring", "prior_art", "uptime-kuma is 92k stars; free tiers exist"),
    39: ("source-link", "vague", "no mechanism"),
    40: ("interest-field", "prior_art", "ATProto interests, Mastodon tags and schema.org all model this"),
    41: ("public-infrastructure", "not_a_software_need", "a political request"),
    42: ("selective-stage", "prior_art", "git add -p and jj's split already do this"),
    43: ("ev-ramp", "needs_hardware", "a vehicle setting"),
    44: ("agpl-ecosystem", "vague", "a licensing opinion, no mechanism"),
    45: ("model-changelog", "prior_art", "OpenRouter changelogs, Artificial Analysis and newsletters"),
    46: ("context-free-46", "vague", "the clause has no subject"),
    47: ("stdlib-easy", "vague", "the clause names no subject; needs the parent comment"),
    48: ("flip-clock", "needs_hardware", "a physical design object"),
    49: ("gdrive-disk-usage", "prior_art", "ggdu exists; TreeSize is a commercial service doing this"),
}


def main():
    rows = [json.loads(l) for l in open(path("raw", "sample.jsonl"))]
    if len(rows) != len(VERDICTS):
        print("verdicts cover %d items, sample has %d -- they must match"
              % (len(VERDICTS), len(rows)), file=sys.stderr)
        return 1
    out = []
    for i, r in enumerate(rows):
        name, cause, why = VERDICTS[i]
        r2 = dict(r)
        r2.update({"index": i, "name": name, "cause": cause, "reason": why})
        out.append(r2)
    tally = {}
    for r in out:
        tally[r["cause"]] = tally.get(r["cause"], 0) + 1
    with open(path("raw", "screened.jsonl"), "w") as f:
        for r in out:
            f.write(json.dumps(r, sort_keys=True) + "\n")
    print("screened %d items" % len(out))
    for c, n in sorted(tally.items(), key=lambda kv: -kv[1]):
        print("  %-22s %2d  (%.0f%%)" % (c, n, 100.0 * n / len(out)))
    return 0


if __name__ == "__main__":
    sys.exit(main())