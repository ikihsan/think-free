#!/usr/bin/env python3
"""E177 role inputs: write the three blinded passes' input files.

Nothing here judges anything. It strips HTML, fixes the populations, and writes
one file per role so a reader's context cannot contain a field it must not see:

  clf/a.jsonl, clf/b.jsonl   question + key answer          (no labels)
  clf_population.json        the 100 qids, in draw order
  score/pairs.jsonl          key answer alone, plus the control pairings
  control_pairs.json         G0b / G0c pairings, fixed by rule

`ANS` is given its questions at run time, after the arms exist, by `arms.py`.
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TAG = re.compile(r"<[^>]+>")
CODE = re.compile(r"(?s)<code>.*?</code>")


def text(html):
    """HTML to plain text, keeping code blocks - they carry the evidence."""
    kept = []

    def grab(m):
        kept.append(m.group(0))
        return " "

    CODE.sub(grab, html or "")
    out = TAG.sub(" ", html or "")
    for k in kept:
        out += "\n" + TAG.sub(" ", k)
    out = re.sub(r"&lt;", "<", out)
    out = re.sub(r"&gt;", ">", out)
    out = re.sub(r"&amp;", "&", out)
    out = re.sub(r"&quot;", '"', out)
    out = re.sub(r"&#\d+;", " ", out)
    return re.sub(r"[ \t]+", " ", out).strip()


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()


def main():
    rows = [r for r in json.load(open(os.path.join(HERE, "rows.json")))["rows"]
            if r.get("key_body")]
    for r in rows:
        r["question_text"] = text(r["body"])
        r["key_text"] = text(r["key_body"])
    keyed = sorted(rows, key=lambda r: (-(r["view_count"] or 0), r["qid"]))
    pop = keyed[:100]
    half = len(pop) // 2
    for name, part in (("a", pop[:half]), ("b", pop[half:])):
        os.makedirs(os.path.join(HERE, "clf"), exist_ok=True)
        with open(os.path.join(HERE, "clf", "%s.jsonl" % name), "w") as fh:
            for r in part:
                fh.write(json.dumps({
                    "qid": r["qid"], "title": r["title"],
                    "view_count": r["view_count"], "tags": r["tags"],
                    "question": r["question_text"],
                    "key_answer": r["key_text"],
                    "key_score": r["key_score"],
                }, sort_keys=True) + "\n")
        # AMENDMENT 4: one file per row, hard-wrapped. A single-line JSON row
        # loses its question to a 2000-character line cap whenever the key
        # answer carries a code block; that cost CLF batch a 18 of 50 rows.
        os.makedirs(os.path.join(HERE, "clf", name), exist_ok=True)
        for r in part:
            path = os.path.join(HERE, "clf", name, "%d.txt" % r["qid"])
            with open(path, "w") as fh:
                fh.write("qid: %d\nview_count: %s\ntags: %s\nkey_score: %s\n\n"
                         % (r["qid"], r["view_count"], ", ".join(r["tags"]),
                            r["key_score"]))
                for label, key in (("TITLE", "title"),
                                   ("QUESTION", "question_text"),
                                   ("KEY ANSWER", "key_text")):
                    fh.write("=== %s ===\n" % label)
                    for ln in (r[key] or "").split("\n") or [""]:
                        for i in range(0, max(len(ln), 1), 90):
                            fh.write(ln[i:i + 90] + "\n")
                    fh.write("\n")
    with open(os.path.join(HERE, "clf_population.json"), "w") as fh:
        json.dump({"qids": [r["qid"] for r in pop],
                   "view_counts": [r["view_count"] for r in pop],
                   "batches": {"a": [r["qid"] for r in pop[:half]],
                               "b": [r["qid"] for r in pop[half:]]},
                   "sha256": digest([r["qid"] for r in pop]),
                   "digest_population": digest(
                       {str(r["qid"]): [r["question_text"], r["key_text"]]
                        for r in pop})},
                  fh, indent=1, sort_keys=True)
        fh.write("\n")

    # G0b / G0c controls, fixed by rule over the 45 rows OUTSIDE the population.
    rest = keyed[100:]
    g0b = rest[:5]                      # same answer vs itself: equivalent
    g0c = rest[5:15]                    # answer i vs answer j: not equivalent
    ctl = {
        "g0b_identical_pairs": [{"id": "g0b-%d" % r["qid"], "a_qid": r["qid"],
                                 "b_qid": r["qid"]} for r in g0b],
        "g0c_distinct_pairs": [{"id": "g0c-%d-%d" % (a["qid"], b["qid"]),
                                "a_qid": a["qid"], "b_qid": b["qid"]}
                               for a, b in zip(g0c[::2], g0c[1::2])],
        "note": "g0b is one row's key answer against the same row's key answer; "
                "g0c is one row's key answer against another row's, from outside "
                "the 100-row population. Fixed before any reader ran.",
    }
    with open(os.path.join(HERE, "control_pairs.json"), "w") as fh:
        json.dump(ctl, fh, indent=1, sort_keys=True)
        fh.write("\n")

    os.makedirs(os.path.join(HERE, "score"), exist_ok=True)
    need = sorted({p["a_qid"] for p in ctl["g0b_identical_pairs"]}
                  | {p["a_qid"] for p in ctl["g0c_distinct_pairs"]}
                  | {p["b_qid"] for p in ctl["g0c_distinct_pairs"]})
    with open(os.path.join(HERE, "score", "control_key_texts.json"), "w") as fh:
        json.dump({str(r["qid"]): r["key_text"] for r in rows
                   if r["qid"] in need}, fh, indent=1, sort_keys=True)
        fh.write("\n")

    print("keyed rows %d; CLF population %d (batches %d/%d); control pool %d"
          % (len(rows), len(pop), half, len(pop) - half, len(rest)))
    print("clf_population sha256 %s" % digest([r["qid"] for r in pop])[:16])
    print("bytes of question+answer text in the two batches: %d"
          % sum(len(r["question_text"]) + len(r["key_text"])
                for r in pop))


if __name__ == "__main__":
    sys.exit(main())