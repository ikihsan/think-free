"""Build the E032 reader sheets from raw/harvest.jsonl.

Emits, each with its sha256 recorded beside it (D061, from F049):

  sheets/q1_reader1.tsv   60 rows, keys q-001..q-060, in harvest order
  sheets/q1_reader2.tsv   the same 60 rows, different keys, different order
  sheets/q1_nonsense.tsv  24 token-shuffled bodies, keys n-01..n-24  (A4)
  sheets/pairs.tsv        written later by link.py, not here

A reader is never shown the site, the author, the question id or the key's
meaning, and the two readers are given disjoint key spaces so a returned row
cannot be matched by key alone.
"""
import hashlib
import json
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
SHEETS = os.path.join(HERE, "sheets")

STOP = set("""a an the and or but if of to in on at for with from by as is are was were be been am
i you he she it we they me my your our their his her its this that these those do does did done
not no nor so than then there here what which who whom when where why how all any both each few
more most other some such only own same too very can will just should now would could my about
into out up down over under again further once because while during before after above below
""".split())
TOKEN = re.compile(r"[A-Za-z][A-Za-z'-]+")


def tokens(text):
    return [t for t in TOKEN.findall(text) if t.lower() not in STOP and len(t) > 2]


def digest(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def write(path, header, rows):
    with open(path, "w") as fh:
        fh.write("\t".join(header) + "\n")
        for row in rows:
            fh.write("\t".join(str(c).replace("\t", " ").replace("\n", " ") for c in row) + "\n")
    return digest(path)


def main():
    os.makedirs(SHEETS, exist_ok=True)
    src = os.path.join(RAW, "harvest.jsonl")
    rows = [json.loads(line) for line in open(src) if line.strip()]
    if len(rows) != 60:
        sys.exit("PROTOCOL declares 60 rows; raw holds %d" % len(rows))

    r1 = [("q-%03d" % (i + 1), rows[i]["body"]) for i in range(60)]
    d1 = write(os.path.join(SHEETS, "q1_reader1.tsv"), ["key", "body"], r1)

    shuffled = list(rows)
    rng = random.Random(20261006)
    rng.shuffle(shuffled)
    order = [rows.index(row) for row in shuffled]
    r2 = [("z-%03d" % (i + 1), shuffled[i]["body"]) for i in range(60)]
    d2 = write(os.path.join(SHEETS, "q1_reader2.tsv"), ["key", "body"], r2)

    # A4 nonsense: content tokens shuffled within the row, order destroyed. The
    # vocabulary, the length and the author-voice survive; the propositional
    # content does not. A reader that returns a clause here is answering from
    # fluency rather than from what the text says.
    nrows = []
    for i, row in enumerate(rows[:24]):
        toks = tokens(row["body"])
        random.Random(90000 + i).shuffle(toks)
        body = " ".join(toks)
        nrows.append(("n-%02d" % (i + 1), body))
    d4 = write(os.path.join(SHEETS, "q1_nonsense.tsv"), ["key", "body"], nrows)

    manifest = {
        "schema": "origin.e032.sheets/1",
        "source": "raw/harvest.jsonl",
        "source_sha256": digest(src),
        "q1_reader1": {"path": "sheets/q1_reader1.tsv", "rows": 60, "sha256": d1},
        "q1_reader2": {"path": "sheets/q1_reader2.tsv", "rows": 60, "sha256": d2},
        "q1_nonsense": {"path": "sheets/q1_nonsense.tsv", "rows": 24, "sha256": d4},
        # Reader keys -> 0-based row index into raw/harvest.jsonl, so link.py
        # never re-derives the shuffle. D061's rule is to check row identity by
        # order, not by key set; this map is what that check reads.
        "keymap": {
            "q1_reader1": {"q-%03d" % (i + 1): i for i in range(60)},
            "q1_reader2": {"z-%03d" % (i + 1): j for i, j in enumerate(order)},
        },
    }
    with open(os.path.join(SHEETS, "MANIFEST.json"), "w") as fh:
        json.dump(manifest, fh, indent=2, sort_keys=True)
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()