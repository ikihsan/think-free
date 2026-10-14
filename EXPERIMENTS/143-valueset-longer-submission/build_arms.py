#!/usr/bin/env python3
"""build_arms.py — split each Federal Register rule into preamble (submission)
and CFR amendments (reference), and emit arms.jsonl.

Standard library only, deterministic. The preamble ends at "List of Subjects"
or the first "PART XX--" header. The CFR amendments are everything from
that point onward.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

# Pattern to find the boundary between preamble and CFR amendments
# "List of Subjects in 10 CFR Part XX" or "PART XX--" (CFR part header)
PREAMBLE_END_RE = re.compile(r"\n(List of Subjects in 10 CFR Part [^\n]+)\n")
PART_HEADER_RE = re.compile(r"\n(PART \d+--[^\n]+)\n")

PAGE_MARKER_RE = re.compile(r"\[\[Page\s+\d+\]\]")


def split_preamble(text):
    """Return (preamble, cfr_amendments) where cfr_amendments is the
    regulatory text starting from 'List of Subjects' or 'PART XX--'.
    If neither is found, preamble is empty and cfr_amendments is full text.
    Page markers [[Page XXXXX]] are stripped from both.
    """
    # Try "List of Subjects" first
    m = PREAMBLE_END_RE.search(text)
    if m:
        cut = m.start()
        preamble = text[:cut]
        cfr_amendments = text[cut:]
        return PAGE_MARKER_RE.sub("", preamble).strip(), PAGE_MARKER_RE.sub("", cfr_amendments).strip()

    # Fall back to "PART XX--"
    m = PART_HEADER_RE.search(text)
    if m:
        cut = m.start()
        preamble = text[:cut]
        cfr_amendments = text[cut:]
        return PAGE_MARKER_RE.sub("", preamble).strip(), PAGE_MARKER_RE.sub("", cfr_amendments).strip()

    # No boundary found
    return "", PAGE_MARKER_RE.sub("", text).strip()


def main():
    docs_path = os.path.join(RAW, "documents.json")
    if not os.path.exists(docs_path):
        print("ERROR: raw/documents.json not found. Run fetch.py first.")
        return 1

    docs = json.load(open(docs_path))
    arms = []
    n_with_preamble = 0
    n_with_values = 0
    n_no_boundary = 0

    for doc in docs:
        doc_num = doc["document_number"]
        txt_path = os.path.join(RAW, f"{doc_num}.txt")
        if not os.path.exists(txt_path):
            continue
        text = open(txt_path).read()
        preamble, cfr_amendments = split_preamble(text)
        if not preamble:
            n_no_boundary += 1
            continue
        if not cfr_amendments:
            print(f"WARNING: {doc_num} has preamble but no CFR amendments")
            continue
        n_with_preamble += 1
        # Check if preamble contains any digit (value-bearing)
        has_digit = bool(re.search(r"\d", preamble))
        if has_digit:
            n_with_values += 1
        arms.append({
            "document_number": doc_num,
            "title": doc.get("title", ""),
            "publication_date": doc.get("publication_date", ""),
            "preamble": preamble,
            "cfr_amendments": cfr_amendments,
            "has_digit": has_digit,
        })

    out_path = os.path.join(HERE, "arms.jsonl")
    with open(out_path, "w") as f:
        for arm in arms:
            f.write(json.dumps(arm, sort_keys=True) + "\n")

    print(f"Documents with preamble: {n_with_preamble}")
    print(f"Documents with digit in preamble: {n_with_values}")
    print(f"Documents with no boundary found: {n_no_boundary}")
    print(f"Wrote {len(arms)} arms to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())