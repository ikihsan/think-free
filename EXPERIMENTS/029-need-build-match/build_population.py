#!/usr/bin/env python3
"""E029 -- build the eligible population from three existing captures.

Protocol: EXPERIMENTS/029-need-build-match/PROTOCOL.md (declared before the first
fetch). Three captures are joined and no network is touched:

  025-need-staters-builderhood/raw/need_arm.jsonl   author -> nb_show_hn
  022-need-outcomes/raw/outcomes.jsonl              author -> need statements
  026-unserved-need-structure/raw/texts.jsonl       comment_id -> the words

A refusal is never an absence, so a capture line that cannot be parsed is counted
and reported rather than skipped: a malformed line must not silently shrink a
denominator (F042's build-arm defect).
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.dirname(ROOT)

NEED_ARM = os.path.join(EXP, "025-need-staters-builderhood", "raw", "need_arm.jsonl")
OUTCOMES = os.path.join(EXP, "022-need-outcomes", "raw", "outcomes.jsonl")
TEXTS = os.path.join(EXP, "026-unserved-need-structure", "raw", "texts.jsonl")

OUT = os.path.join(ROOT, "raw", "population.jsonl")

MIN_WORDS = 15  # declared in PROTOCOL.md, section "Population"


def read_jsonl(path):
    rows, malformed = [], 0
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except ValueError:
                malformed += 1
    return rows, malformed


def strip_html(text):
    t = re.sub(r"<p>", "\n\n", text or "")
    t = re.sub(r"<[^>]+>", " ", t)
    for a, b in (("&#x27;", "'"), ("&quot;", '"'), ("&amp;", "&"),
                 ("&lt;", "<"), ("&gt;", ">"), ("&#x2F;", "/"), ("&nbsp;", " ")):
        t = t.replace(a, b)
    return re.sub(r"[ \t]+", " ", t).strip()


def n_words(text):
    return len([w for w in strip_html(text).split() if w.strip()])


def main():
    if not os.path.isdir(os.path.join(ROOT, "raw")):
        os.makedirs(os.path.join(ROOT, "raw"))

    arm, arm_bad = read_jsonl(NEED_ARM)
    outcomes, out_bad = read_jsonl(OUTCOMES)
    texts, txt_bad = read_jsonl(TEXTS)
    sys.stderr.write(
        "capture lines: need_arm=%d(%d malformed) outcomes=%d(%d) texts=%d(%d)\n"
        % (len(arm), arm_bad, len(outcomes), out_bad, len(texts), txt_bad))

    text_by_comment = {}
    for d in texts:
        cid = d.get("comment_id")
        if cid is not None:
            text_by_comment[str(cid)] = d

    # author -> [need statement rows], keeping only rows whose text is readable
    by_author = {}
    no_text = 0
    for d in outcomes:
        a, cid = d.get("author"), d.get("comment_id")
        if not a or cid is None:
            no_text += 1
            continue
        rec = text_by_comment.get(str(cid))
        if not rec or not (rec.get("text") or "").strip():
            no_text += 1
            continue
        by_author.setdefault(a, []).append({
            "comment_id": str(cid),
            "story_id": str(d.get("story_id")),
            "trigger": d.get("trigger"),
            "answered": d.get("answered"),
            "n_words": n_words(rec["text"]),
            "text": strip_html(rec["text"]),
        })
    sys.stderr.write("authors with >=1 readable need statement: %d (rows unreadable: %d)\n"
                     % (len(by_author), no_text))

    # The population is fixed by the protocol at "nb_show_hn >= 1" over the need arm.
    builders = []
    refused = 0
    for d in arm:
        if d.get("status") != "ok":
            refused += 1
            continue
        nb = d.get("nb_show_hn")
        if isinstance(nb, int) and nb >= 1:
            builders.append(d["author"])
    builders.sort()
    sys.stderr.write("declared population (nb_show_hn >= 1): %d  (arm refusals: %d)\n"
                     % (len(builders), refused))

    rows, excl_multi, excl_short, excl_unjoined = [], 0, 0, 0
    for a in builders:
        needs = by_author.get(a)
        if not needs:
            excl_unjoined += 1
            continue
        if len(needs) > 1:
            excl_multi += 1          # which need the build answers is not decidable
            continue
        n = needs[0]
        if n["n_words"] < MIN_WORDS:
            excl_short += 1          # nothing for a reader to judge against
            continue
        rows.append({"author": a, "nb_show_hn": None, "need": n})

    sys.stderr.write(
        "eligible after exclusions: %d  (multi-need %d, short %d, unjoined %d)\n"
        % (len(rows), excl_multi, excl_short, excl_unjoined))
    if len(rows) < 40:
        sys.stderr.write("FAIL: fewer than 40 eligible rows; the reader arm cannot run\n")
        return 1

    with open(OUT, "w") as f:
        for r in rows:
            f.write(json.dumps(r, sort_keys=True) + "\n")
    print("wrote %d rows to %s" % (len(rows), OUT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
