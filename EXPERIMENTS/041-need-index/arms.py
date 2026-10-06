#!/usr/bin/env python3
"""E041 arms: the positive control F064 could not build, and its three controls.

Reads raw/corpus.jsonl and writes raw/arms.jsonl plus raw/corpus_index.json.

Arms (PROTOCOL.md "Arms"):
  P   a duplicate-labelled row and the target it names, BOTH inside the corpus
  N0  one row from a different repository, per P row, fixed deterministic rule
  N1  the most similar row that is not the target, per P row  (built in tally.py,
      which is where the similarities live; here the *slot* is declared)
  NULL every (P row, corpus row) cosine, reported as a base rate

The exclusion rule, arm definition, and normalisation are all declared in
PROTOCOL.md and are not varied after the first computation.
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
CORPUS = os.path.join(RAW, "corpus.jsonl")
LOG = os.path.join(RAW, "capture_log.json")
ARMS = os.path.join(RAW, "arms.jsonl")

# --- the six declared reference patterns, in order; first match wins ---------
REF_PATTERNS = [
    re.compile(r"duplicate\s+of\s+#(\d+)", re.I),
    re.compile(r"dup(?:e|licate)?\s*(?:of|:)\s*#(\d+)", re.I),
    re.compile(r"same\s+(?:as|issue\s+as)\s+#(\d+)", re.I),
    re.compile(r"->\s*#(\d+)"),
    re.compile(r"see\s*#(\d+)"),
    re.compile(r"https?://github\.com/[^/\s]+/[^/\s]+/issues/(\d+)", re.I),
]

# --- normalisation, declared in PROTOCOL.md --------------------------------
HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)
URL = re.compile(r"https?://\S+", re.I)
REF_PHRASE = re.compile(
    r"(duplicate\s+of\s*#\d+|dup(?:e|licate)?\s*(?:of|:)\s*#\d+|"
    r"same\s+(?:as|issue\s+as)\s*#\d+|->\s*#\d+|see\s*#\d+|"
    r"issues/\d+)", re.I)
MARKDOWN = re.compile(r"[`*_>#|~\[\]()]")
WS = re.compile(r"\s+")
ENTITY = re.compile(r"&(#\d+|#x[0-9a-f]+|[a-z]+);")
ENTITIES = {"amp": "&", "lt": "<", "gt": ">", "quot": '"', "apos": "'",
            "nbsp": " ", "#39": "'", "#x27": "'", "#x2f": "/", "#47": "/"}
BODY_CHARS = 200

STOP = None  # E040's fixed stoplist is used; see the import below.
TOKEN = None


def _unused():  # pragma: no cover - kept only to make the removal explicit
    pass


# The stratification "shares >= 1 content term" must use the *instrument's*
# tokenisation, or the stratum is drawn with a different ruler than the
# measurement it stratifies. E040's is imported rather than restated.
_E040DIR = os.path.join(os.path.dirname(HERE), "040-need-clustering")
sys.path.insert(0, _E040DIR)
from gates import tokens  # noqa: E402,F811


def unescape(m):
    body = m.group(1)
    if body.startswith("#x") or body.startswith("#X"):
        try:
            return chr(int(body[2:], 16))
        except ValueError:
            return " "
    if body.startswith("#"):
        try:
            return chr(int(body[1:]))
        except ValueError:
            return " "
    return ENTITIES.get(body.lower(), " ")


def normalise(text):
    t = ENTITY.sub(unescape, text or "")
    t = HTML_COMMENT.sub(" ", t)
    t = URL.sub(" ", t)
    t = REF_PHRASE.sub(" ", t)
    t = MARKDOWN.sub(" ", t)
    return WS.sub(" ", t).strip()


def target_ref(body):
    for pat in REF_PATTERNS:
        m = pat.search(body or "")
        if m:
            return int(m.group(1))
    return None


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    with open(LOG) as fh:
        log = json.load(fh)
    excluded = sorted(r for r, v in log["repos"].items()
                      if v.get("excluded_automation"))

    corpus, seen = [], set()
    dup_order = []
    with open(CORPUS) as fh:
        for line in fh:
            row = json.loads(line)
            key = (row["repo"], row["number"])
            if key in seen:          # a split query can repeat a row at a boundary
                continue
            seen.add(key)
            if row["repo"] in excluded:
                continue
            norm_body = normalise(row["body"])
            corpus.append({
                "key": "%s#%s" % (row["repo"], row["number"]),
                "repo": row["repo"],
                "number": row["number"],
                "title": normalise(row["title"]),
                "body": norm_body[:BODY_CHARS],
                # The raw body is kept because target extraction must read the
                # reference phrase, which normalisation is required to strip.
                # Reading it from `body` would find nothing, always.
                "raw_body": row["body"],
                "state_reason": row["state_reason"],
                "author": row["author"],
            })
            if row["state_reason"] == "duplicate":
                dup_order.append((row["repo"], row["number"]))

    index = {}
    for i, r in enumerate(corpus):
        index.setdefault(r["repo"], {})[r["number"]] = i

    # --- arm P: the judged pair, both members inside the corpus --------------
    pairs, dropped = [], {"no_parseable_ref": 0, "target_not_in_corpus": 0,
                          "target_is_self": 0, "target_missing_title": 0}
    for repo, num in dup_order:
        a = index.get(repo, {}).get(num)
        if a is None:
            continue
        ref = target_ref(corpus[a]["raw_body"])
        if ref is None:
            dropped["no_parseable_ref"] += 1
            continue
        if ref == num:
            dropped["target_is_self"] += 1
            continue
        b = index.get(repo, {}).get(ref)
        if b is None:
            dropped["target_not_in_corpus"] += 1
            continue
        if not corpus[a]["title"] and not corpus[b]["title"]:
            dropped["target_missing_title"] += 1
            continue
        a_terms = set(tokens(corpus[a]["title"]))
        b_terms = set(tokens(corpus[b]["title"]))
        pairs.append({
            "repo": repo, "dup": corpus[a]["key"], "target": corpus[b]["key"],
            "dup_row": a, "target_row": b,
            "stratum": "S-easy" if (a_terms & b_terms) else "S-hard",
            "shared_title_terms": len(a_terms & b_terms),
        })

    with open(ARMS, "w") as fh:
        for p in pairs:
            out = dict(p)
            out["arm"] = "P"
            fh.write(json.dumps(out, sort_keys=True) + "\n")

    stats = {
        "corpus_rows": len(corpus),
        "corpus_rows_by_repo": {r: sum(1 for x in corpus if x["repo"] == r)
                                for r in sorted({x["repo"] for x in corpus})},
        "duplicate_labelled_in_corpus": len(dup_order),
        "pairs_P": len(pairs),
        "pairs_by_stratum": {"S-easy": sum(1 for p in pairs
                                           if p["stratum"] == "S-easy"),
                             "S-hard": sum(1 for p in pairs
                                           if p["stratum"] == "S-hard")},
        "dropped": dropped,
        "repos_excluded_automation": excluded,
        "corpus_sha256": sha256(CORPUS),
        "arms_sha256": sha256(ARMS),
    }
    with open(os.path.join(RAW, "arms_summary.json"), "w") as fh:
        json.dump(stats, fh, indent=1, sort_keys=True)
    print(json.dumps(stats, indent=1, sort_keys=True))
    if not pairs:
        print("\nNO POSITIVE PAIRS. The control cannot be built; stop and report.")
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
