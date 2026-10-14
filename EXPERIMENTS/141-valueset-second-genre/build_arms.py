#!/usr/bin/env python3
"""build_arms.py — SQuAD v2.0 dev into arms.jsonl, once, deterministically.

One row per question. Nothing here decides a gate; it only records the
population and the arm membership, so that the exclusions K1's denominator
depends on are readable from the file before any instrument runs (D110).

Run:  python3 build_arms.py
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw", "dev-v2.0.json")
ARMS = os.path.join(HERE, "arms.jsonl")

# The corpus this protocol was written against. A different file is a
# different population and the run stops rather than scoring it silently.
EXPECTED_SHA256 = "80a5225e94905956a6446d296ca1093975c4d3b3260f1d6c8f68bc2ab77182d8"
EXPECTED_BYTES = 4370528

DIGIT = re.compile(r"\d")
# AMENDMENT-1 arms N and C. Both are ordinary regexes over corpus fields, so
# both exclusions stay checkable from arms.jsonl alone (D110).
VALUE_SPAN = re.compile(r"^[\s$€£]*\d|^(January|February|March|April|May|June|July|"
                         r"August|September|October|November|December)\b", re.I)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main():
    if not os.path.exists(RAW):
        sys.exit("raw/dev-v2.0.json is missing and raw/ is gitignored; fetch the "
                 "url in SOURCES.md and check the digest before scoring anything")
    size = os.path.getsize(RAW)
    digest = sha256(RAW)
    if size != EXPECTED_BYTES or digest != EXPECTED_SHA256:
        sys.exit("corpus is not the one this protocol names: %d bytes %s" % (size, digest))

    corpus = json.load(open(RAW, encoding="utf-8"))
    rows = []
    for article in corpus["data"]:
        title = article["title"]
        for para in article["paragraphs"]:
            context = para["context"]
            ctx_key = hashlib.sha256(context.encode("utf-8")).hexdigest()
            for qa in para["qas"]:
                answers = qa.get("answers") or []
                # The answer span a crowdworker selected. For an impossible
                # question the list is empty by construction, which is why the
                # submission is question-plus-span and the question carries
                # the value claims on the B arm.
                answer = answers[0]["text"] if answers else ""
                question = qa["question"]
                # AMENDMENT-1 arm C: a human-written plausible answer to a
                # question the passage cannot answer, taken from a different
                # passage. Arm N: the gold span is itself a value.
                plausible_rows = qa.get("plausible_answers") or []
                plausible = plausible_rows[0]["text"] if plausible_rows else ""
                rows.append({
                    "id": qa["id"],
                    "arm": "B" if qa.get("is_impossible") else "A",
                    "has_digit": bool(DIGIT.search(question)),
                    "answer_is_value": bool(VALUE_SPAN.match(answer)),
                    "plausible": plausible,
                    "title": title,
                    "context_sha256": ctx_key,
                    "context": context,
                    "question": question,
                    "answer": answer,
                    "submission": (question + " " + answer).strip(),
                })

    rows.sort(key=lambda r: r["id"])
    with open(ARMS, "w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, sort_keys=True) + "\n")

    counts = {
        "rows": len(rows),
        "A": sum(1 for r in rows if r["arm"] == "A"),
        "B": sum(1 for r in rows if r["arm"] == "B"),
        "A_digit": sum(1 for r in rows if r["arm"] == "A" and r["has_digit"]),
        "B_digit": sum(1 for r in rows if r["arm"] == "B" and r["has_digit"]),
        "A_value_answer": sum(1 for r in rows if r["arm"] == "A" and r["answer_is_value"]),
        "B_with_plausible": sum(1 for r in rows if r["arm"] == "B" and r["plausible"]),
        "paragraphs": len({r["context_sha256"] for r in rows}),
        "articles": len({r["title"] for r in rows}),
    }
    counts["corpus_sha256"] = digest
    counts["corpus_bytes"] = size
    with open(os.path.join(HERE, "population.json"), "w", encoding="utf-8") as fh:
        json.dump(counts, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(json.dumps(counts, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
