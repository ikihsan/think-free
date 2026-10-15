#!/usr/bin/env python3
"""build_arms.py — split each Federal Register rule into SUPPLEMENTARY INFORMATION (submission)
and the rest (reference), and emit arms.jsonl.

Standard library only, deterministic. The SUPPLEMENTARY INFORMATION section is delimited by
'SUPPLEMENTARY INFORMATION:' at the start of a line and the end of the document.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

# Section headers in a Federal Register document, in order of appearance.
# SUPPLEMENTARY INFORMATION is typically the last major section.
SECTION_RE = re.compile(r"\n([A-Z][A-Za-z\s/]{2,}[A-Za-z])\s*:\s*")

PAGE_MARKER_RE = re.compile(r"\[\[Page\s+\d+\]\]")


def split_supplementary(text):
    """Return (supplementary, reference) where reference is the full text minus the
    SUPPLEMENTARY INFORMATION section. If no SUPPLEMENTARY INFORMATION is found,
    supplementary is empty and reference is the full text. Page markers [[Page XXXXX]]
    are stripped from both."""
    # Find SUPPLEMENTARY INFORMATION section
    m = re.search(r"\nSUPPLEMENTARY INFORMATION\s*:\s*", text)
    if not m:
        return "", PAGE_MARKER_RE.sub("", text)
    rest = text[m.end():]
    # SUPPLEMENTARY INFORMATION goes to the end of the document
    supplementary = rest
    # Reference is everything before SUPPLEMENTARY INFORMATION
    reference = text[: m.start()]
    supplementary = PAGE_MARKER_RE.sub("", supplementary).strip()
    reference = PAGE_MARKER_RE.sub("", reference).strip()
    return supplementary, reference


def main():
    docs_path = os.path.join(RAW, "documents.json")
    if not os.path.exists(docs_path):
        print("ERROR: raw/documents.json not found. Run fetch.py first.")
        return 1

    docs = json.load(open(docs_path))
    arms = []
    n_with_supp = 0
    n_with_values = 0

    for doc in docs:
        doc_num = doc["document_number"]
        txt_path = os.path.join(RAW, f"{doc_num}.txt")
        if not os.path.exists(txt_path):
            continue
        text = open(txt_path).read()
        supplementary, reference = split_supplementary(text)
        if not supplementary:
            continue
        n_with_supp += 1
        # Check if supplementary contains any digit (value-bearing)
        has_digit = bool(re.search(r"\d", supplementary))
        if has_digit:
            n_with_values += 1
        arms.append({
            "document_number": doc_num,
            "title": doc.get("title", ""),
            "publication_date": doc.get("publication_date", ""),
            "supplementary": supplementary,
            "reference": reference,
            "has_digit": has_digit,
        })

    out_path = os.path.join(HERE, "arms.jsonl")
    with open(out_path, "w") as f:
        for arm in arms:
            f.write(json.dumps(arm, sort_keys=True) + "\n")

    print(f"Documents with SUPPLEMENTARY INFORMATION: {n_with_supp}")
    print(f"Documents with digit in SUPPLEMENTARY INFORMATION: {n_with_values}")
    print(f"Wrote {len(arms)} arms to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())