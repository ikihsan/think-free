#!/usr/bin/env python3
"""build_arms.py — split each Federal Register rule into SUMMARY (submission)
and the rest (reference), and emit arms.jsonl.

Standard library only, deterministic. The SUMMARY section is delimited by
'SUMMARY:' at the start of a line and the next ALL-CAPS section header.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

# Section headers in a Federal Register document, in order of appearance.
# SUMMARY is always first; the next header ends it.
SECTION_RE = re.compile(r"\n([A-Z][A-Za-z\s/]{2,}[A-Za-z])\s*:\s*")


PAGE_MARKER_RE = re.compile(r"\[\[Page\s+\d+\]\]")


def split_summary(text):
    """Return (summary, reference) where reference is the full text minus the
    SUMMARY section. If no SUMMARY is found, summary is empty and reference
    is the full text. Page markers [[Page XXXXX]] are stripped from both."""
    m = re.search(r"\nSUMMARY\s*:\s*", text)
    if not m:
        return "", PAGE_MARKER_RE.sub("", text)
    rest = text[m.end():]
    # Find the next section header after the SUMMARY content.
    # Search in rest directly; SECTION_RE requires a leading \n, so prepend
    # one and offset the slice positions accordingly.
    next_m = SECTION_RE.search("\n" + rest)
    if next_m:
        # next_m.start() is the index of the \n in "\n" + rest; subtract 1
        # to get the index in rest where the next header begins.
        cut = next_m.start() - 1
        if cut < 0:
            cut = 0
        summary = rest[:cut]
        # Reconstruct reference: everything before SUMMARY + everything
        # from the next header onward (skip the \n that precedes it).
        reference = text[: m.start()] + text[m.end() + cut:]
    else:
        summary = rest
        reference = text[: m.start()]
    summary = PAGE_MARKER_RE.sub("", summary).strip()
    reference = PAGE_MARKER_RE.sub("", reference).strip()
    return summary, reference


def main():
    docs_path = os.path.join(RAW, "documents.json")
    if not os.path.exists(docs_path):
        print("ERROR: raw/documents.json not found. Run fetch.py first.")
        return 1

    docs = json.load(open(docs_path))
    arms = []
    n_with_summary = 0
    n_with_values = 0

    for doc in docs:
        doc_num = doc["document_number"]
        txt_path = os.path.join(RAW, f"{doc_num}.txt")
        if not os.path.exists(txt_path):
            continue
        text = open(txt_path).read()
        summary, reference = split_summary(text)
        if not summary:
            continue
        n_with_summary += 1
        # Check if summary contains any digit (value-bearing)
        has_digit = bool(re.search(r"\d", summary))
        if has_digit:
            n_with_values += 1
        arms.append({
            "document_number": doc_num,
            "title": doc.get("title", ""),
            "publication_date": doc.get("publication_date", ""),
            "summary": summary,
            "reference": reference,
            "has_digit": has_digit,
        })

    out_path = os.path.join(HERE, "arms.jsonl")
    with open(out_path, "w") as f:
        for arm in arms:
            f.write(json.dumps(arm, sort_keys=True) + "\n")

    print(f"Documents with SUMMARY: {n_with_summary}")
    print(f"Documents with digit in SUMMARY: {n_with_values}")
    print(f"Wrote {len(arms)} arms to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
