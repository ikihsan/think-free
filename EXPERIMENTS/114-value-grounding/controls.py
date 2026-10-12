#!/usr/bin/env python3
"""controls.py — build the two control arms for E114.

Arm B (positive control): answers of the same shape with exactly one value
replaced by a confusable one. Two flavours, because they test different halves
of the checker and v0 showed that a membership-only checker passes the first:

  B1 from_document  the replacement really occurs elsewhere in the same
                    document, so only the context window can catch it
  B2 absent         the replacement has the same shape and occurs nowhere in
                    the document, so only membership can catch it

Arm C (negative control): a **contiguous** span of the document, lifted
verbatim. Contiguous matters: v0's arm C concatenated six sentences, so the
answer window at a junction held words from the next sentence and the checker
flagged them, which is an artifact of the control rather than of the checker.

The corrupter never reads the checker's output and is seeded, so the arms are
reproducible from the committed documents.
"""
import json
import os
import random
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ground import extract, normalize  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 114
CORRUPTIBLE = ("money", "qty", "date", "code", "num")


def load(rawdir, num):
    with open(os.path.join(rawdir, "text", num + ".txt"), "rb") as fh:
        return normalize(fh.read().decode("utf-8", "replace"))


def digits_of(s):
    return re.sub(r"\D", "", s)


def same_shape(a, b):
    return len(digits_of(a)) == len(digits_of(b)) and a[-1:] == b[-1:]


def perturb(value, kind, rng, pool, in_doc):
    """A replacement of the same shape, drawn from `pool` (real numbers in doc)."""
    n = digits_of(value)
    if not n:
        return None
    d = len(n)
    if kind == "money":
        for _ in range(60):
            cand = rng.choice(pool)
            if len(cand) != d:
                continue
            return "$" + cand
        return None
    if kind == "qty":
        unit = re.sub(r"^[\d,\.]+\s*", "", value)
        for _ in range(60):
            cand = rng.choice(pool)
            if len(cand) == d:
                return cand + " " + unit
        return None
    if kind == "num":
        for _ in range(60):
            cand = rng.choice(pool)
            if len(cand) == d:
                return cand
        return None
    if kind == "date":
        m = re.match(r"([A-Za-z]+)\.?\s+(\d{1,2}),?\s+(\d{4})", value)
        if m:
            mon, day, yr = m.group(1), int(m.group(2)), int(m.group(3))
            newday = rng.randint(1, 28)
            while newday == day:
                newday = rng.randint(1, 28)
            return "%s %d, %d" % (mon, newday, yr)
        return None
    if kind == "code":
        m = re.match(r"(\d+\s+CFR\s+[\d.]+)", value)
        if m:
            tail = m.group(1).rsplit(".", 1)[-1]
            t = digits_of(tail)
            if not t:
                return None
            alt = "".join(str((int(ch) + rng.randint(1, 5)) % 10) for ch in t)
            head = m.group(1).rsplit(".", 1)[0]
            return head + "." + alt
        return None
    return None


def number_pool(doc):
    seen = []
    for num in re.findall(r"\b\d[\d,]{2,}\b", doc):
        c = num.replace(",", "")
        if 3 <= len(c) <= 9 and c not in seen:
            seen.append(c)
    return seen


def corrupt(answer, doc, rng, mode):
    """One corruption, either drawn from the document (B1) or absent from it (B2)."""
    vals = [(k, v) for k, v in extract(answer) if k in CORRUPTIBLE and digits_of(v)]
    rng.shuffle(vals)
    pool = number_pool(doc)
    absent = []
    for _ in range(400):
        d = rng.randint(2, 6)
        cand = str(rng.randint(10 ** (d - 1), 10 ** d - 1))
        if cand not in pool and cand not in doc.replace(",", ""):
            absent.append(cand)
    for kind, value in vals:
        if mode == "B1_from_document":
            repl = perturb(value, kind, rng, pool, set())
            if repl and repl != value and re.search(re.escape(digits_of(repl)[-3:]), doc):
                return kind, value, repl, mode
        else:
            for cand in absent:
                repl = perturb(value, kind, rng, [cand], set())
                if repl and repl != value and cand not in doc.replace(",", ""):
                    return kind, value, repl, mode
    return None


def main():
    rawdir = os.path.join(HERE, "raw")
    rows = [json.loads(l) for l in open(os.path.join(HERE, "answers.jsonl")) if l.strip()]
    rng = random.Random(SEED)
    docs, out, stats = {}, [], {"B1_from_document": 0, "B2_absent": 0,
                                "C_verbatim": 0, "skipped": 0}
    for r in rows:
        num = r["document_number"]
        if num not in docs:
            docs[num] = load(rawdir, num)
        doc = docs[num]
        for mode in ("B1_from_document", "B2_absent"):
            rec = corrupt(r["answer"], doc, rng, mode)
            if rec is None:
                stats["skipped"] += 1
                continue
            kind, original, repl, mode = rec
            i = r["answer"].find(original)
            out.append({
                "document_number": num, "arm": "B", "corruption": mode,
                "question": r["question"],
                "answer": r["answer"][:i] + repl + r["answer"][i + len(original):],
                "original_value": original, "corrupted_value": repl,
                "corrupted_kind": kind,
            })
            stats[mode] += 1
        # C: one contiguous span, verbatim, 600 characters
        body = re.sub(r"\[\[Page[^\]]*\]\]", "  ", doc)
        for _ in range(20):
            start = rng.randrange(0, max(1, len(body) - 900))
            span = body[start:start + 600]
            if extract(span):
                out.append({"document_number": num, "arm": "C",
                            "corruption": "C_verbatim", "question": r["question"],
                            "answer": span, "span_start": start})
                stats["C_verbatim"] += 1
                break
        else:
            stats["skipped"] += 1
    path = os.path.join(HERE, "controls.jsonl")
    with open(path, "w") as fh:
        for r in out:
            fh.write(json.dumps(r, sort_keys=True) + "\n")
    print(json.dumps(stats, sort_keys=True), "rows:", len(out))


if __name__ == "__main__":
    main()