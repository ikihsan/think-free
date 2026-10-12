#!/usr/bin/env python3
"""controls.py — build the two control arms for E114.

Arm B (positive control) answers of the same shape with exactly one value
replaced by a confusable one. Two flavours, because they test different halves
of the checker:

  B1 from_document  the replacement is a value that really occurs elsewhere in
                    the same document, so a membership-only checker passes it.
                    Only the context window can catch it.
  B2 absent         the replacement has the same shape and occurs nowhere in
                    the document. Only membership can catch it.

Arm C (negative control) answers built from verbatim sentences of the document.
A checker that fires here is measuring normalization noise.

The corrupter never looks at the checker's output and is seeded, so the arms are
reproducible.
"""
import json
import os
import random
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ground import VALUE_PATTERNS, canonical, normalize  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 114


def sentences(doc):
    body = re.sub(r"\[\[Page[^\]]*\]\]", " ", doc)
    parts = re.split(r"(?<=[.;:])\s+", body)
    return [p.strip() for p in parts if len(p.strip()) > 60]


def values_in(text):
    out = []
    for kind, pat in VALUE_PATTERNS:
        for m in pat.finditer(text):
            out.append((kind, m.group(0)))
    return out


def all_numbers(doc):
    seen = []
    for num in re.findall(r"\b\d[\d,]*(?:\.\d+)?\b", doc):
        c = canonical(num, "num")
        if len(c) >= 3 and c not in seen:
            seen.append(c)
    return seen


def corrupt_money(v, other):
    return "$" + other


def build_b1(answer, doc, rng):
    """Replace one money/qty value with a different real value from the doc."""
    cands = [m for m in re.finditer(r"\$\s?\d[\d,]*(?:\.\d+)?", answer)]
    if not cands:
        return None
    pool = all_numbers(doc)
    if len(pool) < 20:
        return None
    m = rng.choice(cands)
    for _ in range(40):
        repl = rng.choice(pool)
        if canonical(repl, "num") != canonical(m.group(0), "money"):
            break
    else:
        return None
    return {"original": m.group(0), "replacement": "$" + repl,
            "kind": "B1_from_document",
            "answer": answer[:m.start()] + "$" + repl + answer[m.end():]}


def build_b2(answer, doc, rng):
    """Replace one money value with a same-shape value that occurs nowhere."""
    cands = [m for m in re.finditer(r"\$\s?\d[\d,]*(?:\.\d+)?", answer)]
    if not cands:
        return None
    in_doc = set(all_numbers(doc))
    m = rng.choice(cands)
    digits = len(re.sub(r"\D", "", m.group(0)))
    for _ in range(200):
        n = rng.randint(10 ** (digits - 1), 10 ** digits - 1)
        if str(n) not in in_doc and len(str(n)) == digits:
            break
    else:
        return None
    repl = "$" + format(n, ",d") if n > 999 else "$" + str(n)
    if canonical(repl, "money") in in_doc:
        return None
    return {"original": m.group(0), "replacement": repl, "kind": "B2_absent",
            "answer": answer[:m.start()] + repl + answer[m.end():]}


def main():
    rawdir = os.path.join(HERE, "raw")
    rows = [json.loads(l) for l in open(os.path.join(HERE, "answers.jsonl")) if l.strip()]
    rng = random.Random(SEED)
    docs = {}
    out = []
    stats = {"B1_from_document": 0, "B2_absent": 0, "C_verbatim": 0, "skipped": 0}
    for r in rows:
        num = r["document_number"]
        if num not in docs:
            with open(os.path.join(rawdir, "text", num + ".txt"), "rb") as fh:
                docs[num] = normalize(fh.read().decode("utf-8", "replace"))
        doc = docs[num]
        for builder in (build_b1, build_b2):
            rec = builder(r["answer"], doc, rng)
            if rec is None:
                stats["skipped"] += 1
                continue
            out.append({
                "document_number": num,
                "arm": "B",
                "corruption": rec["kind"],
                "question": r["question"],
                "answer": rec["answer"],
                "corrupted_value": rec["replacement"],
                "original_value": rec["original"],
            })
            stats[rec["kind"]] += 1
        sents = sentences(doc)
        if len(sents) >= 6:
            start = rng.randrange(0, max(1, len(sents) - 6))
            out.append({
                "document_number": num,
                "arm": "C",
                "corruption": "C_verbatim",
                "question": r["question"],
                "answer": " ".join(sents[start:start + 6]),
            })
            stats["C_verbatim"] += 1
        else:
            stats["skipped"] += 1
    path = os.path.join(HERE, "controls.jsonl")
    with open(path, "w") as fh:
        for r in out:
            fh.write(json.dumps(r, sort_keys=True) + "\n")
    print(json.dumps(stats, sort_keys=True), "rows:", len(out))


if __name__ == "__main__":
    main()