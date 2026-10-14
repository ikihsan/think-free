#!/usr/bin/env python3
"""regvalue — Verify that values in a regulatory summary are grounded in the source text.

This is a deterministic, standard-library-only tool that extracts values (money, dates,
citations, percentages, quantities, numbers) from both a reference document and a
summary/submission, then compares them canonically.

Two comparison modes:
  - canonical: compares (kind, value) pairs — distinguishes money from bare numbers
  - numeric: compares only numeric values — matches \$12,500,000 with 12500000 dollars

Usage:
    python3 regvalue.py <reference.txt> <summary.txt> [--mode canonical|numeric]
    python3 regvalue.py --fetch <FR_DOC_NUMBER>  # fetch from Federal Register API

Exit codes: 0 = all values grounded, 1 = ungrounded values found, 2 = error
"""
import html
import json
import os
import re
import sys
import urllib.request
from typing import List, Tuple, Dict, Any, Optional

# ---- Constants from ground.py ----
STOP = set("""a an the of to in for and or by with at on from as is are be been was
were this that these those it its his her their our your my we they he she i you
not no also any all each other others such same more most less least than then
so if when while under over above below after before during within without
into onto per may must shall can could would should will do does did done
have had""".split())

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]
MONTH_RE = "|".join(MONTHS)

ABBR = {"Jan": "January", "Feb": "February", "Mar": "March", "Apr": "April",
        "May": "May", "Jun": "June", "Jul": "July", "Aug": "August",
        "Sep": "September", "Nov": "September", "Oct": "October",
        "Dec": "December"}
ABBR_RE = "|".join(sorted(ABBR, key=len, reverse=True))

PATTERNS = [
    ("date", re.compile(
        r"(?:%s)\.?\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4}" % MONTH_RE +
        r"|\d{1,2}\s+(?:%s)\.?\s+\d{4}" % MONTH_RE +
        r"|(?:%s)\.?\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4}" % ABBR_RE +
        r"|\d{1,2}/\d{1,2}/\d{2,4}")),
    ("money", re.compile(r"\$\s?\d[\d,]*(?:\.\d+)?(?:\s?(?:million|billion|thousand))?",
                         re.I)),
    ("pct", re.compile(r"\d[\d,]*(?:\.\d+)?\s?(?:percent|%)", re.I)),
    ("code", re.compile(
        r"\d+\s+CFR\s+(?:part\s+)?[\d.]+(?:\s*(?:through|-|to)\s*[\d.]+)?"
        r"(?:\([A-Za-z0-9()]*\))*"
        r"|\d+\s+U\.?S\.?C\.?\s*(?:et seq\.|\s*\d+[A-Za-z0-9()]*|§\s*\d+)"
        r"|\d+\s*FR\s+\d+"
        r"|Docket\s+No\.?\s*[\w.()\-]+"
        r"|RIN\s+\d{4}-[A-Z]{2}\d{2}"
        r"|\b\d{2,4}-\d{3,4}\b(?=[A-Z][a-z]|\s)")),
    ("qty", re.compile(
        r"\d[\d,]*(?:\.\d+)?\s?(?:lb|lbs|pound|pounds|kg|kilogram|kilograms|"
        r"mt|metric ton|metric tons|ton|tons|nautical mile|nautical miles|"
        r"\bnm\b|foot|feet|\bm\b|degree|degrees|hour|hours|day|days|year|years)",
        re.I)),
    ("num", re.compile(r"\b\d[\d,]*(?:\.\d+)?\b")),
]

SCALES = {"thousand": 1e3, "million": 1e6, "billion": 1e9}

# ---- Core functions ----

def normalize(raw: str) -> str:
    """Readable text: tags gone, entities decoded, hard line wraps joined."""
    txt = re.sub(r"<[^>]+>", " ", raw)
    txt = html.unescape(txt).replace(" ", " ")
    txt = re.sub(r"\s*\n\s*", " ", txt)
    return re.sub(r"[ \t]+", " ", txt).strip()


def _num(text: str) -> Optional[float]:
    t = text.replace(",", "").replace(" ", "").strip()
    try:
        return float(t)
    except ValueError:
        return None


def _money(raw: str) -> Optional[float]:
    m = re.search(r"\$\s?([\d][\d,]*(?:\.\d+)?)\s*(thousand|million|billion)?",
                  raw, re.I)
    if not m:
        return None
    v = _num(m.group(1))
    if v is None:
        return None
    scale = SCALES.get((m.group(2) or "").lower())
    return v * scale if scale else v


def _date(raw: str) -> Optional[Tuple[int, int, int]]:
    v = re.sub(r"(\d)(st|nd|rd|th)\b", r"\1", raw, flags=re.I)
    m = re.match(r"([A-Za-z]+)\.?\s+(\d{1,2}),?\s+(\d{4})$", v)
    if m:
        mon = ABBR.get(m.group(1)[:3].capitalize(), m.group(1))
        names = [n.lower() for n in MONTHS]
        if mon.lower() in names:
            return (int(m.group(3)), names.index(mon.lower()) + 1, int(m.group(2)))
        return None
    m = re.match(r"(\d{1,2})\s+([A-Za-z]+),?\s+(\d{4})$", v)
    if m:
        mon = ABBR.get(m.group(2)[:3].capitalize(), m.group(2))
        names = [n.lower() for n in MONTHS]
        if mon.lower() in names:
            return (int(m.group(3)), names.index(mon.lower()) + 1, int(m.group(1)))
        return None
    m = re.match(r"(\d{1,2})/(\d{1,2})/(\d{2,4})$", v)
    if m:
        # Assume US format MM/DD/YYYY for Federal Register documents
        month, day, yr = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if yr < 100:
            yr += 2000 if yr < 70 else 1900
        if 1 <= month <= 12 and 1 <= day <= 31:
            return (yr, month, day)
        return None
    return None


def _code(raw: str) -> str:
    t = re.sub(r"\s+", " ", raw).strip().lower()
    t = re.sub(r"\s*\(\s*", "(", t)
    t = re.sub(r"\s*\)\s*", ")", t)
    return re.sub(r"[ .]", "", t)


def extract(text: str) -> List[Tuple[str, str]]:
    """Every value claim in the text, longest match wins, no nested double-count."""
    spans = []
    for kind, pat in PATTERNS:
        for m in pat.finditer(text):
            spans.append((m.start(), m.end(), kind, m.group(0)))
    spans.sort(key=lambda s: (s[0], -(s[1] - s[0])))
    kept = []
    for s, e, kind, raw in spans:
        if any(k[0] <= s and e <= k[1] for k in kept):
            continue
        kept.append((s, e, kind, raw))
    return [(k, r) for _, _, k, r in kept]


def canonical(text: str) -> List[Tuple[str, Any]]:
    """Every value in `text` as a hashable canonical key, in document order."""
    out = []
    for kind, raw in extract(text):
        if kind == "money":
            key = _money(raw)
            out.append(("money", key if key is not None else raw.lower()))
        elif kind == "date":
            key = _date(raw)
            out.append(("date", key if key is not None else raw.lower()))
        elif kind == "code":
            out.append(("code", _code(raw)))
        elif kind == "pct":
            m = re.search(r"([\d][\d,]*(?:\.\d+)?)", raw)
            v = _num(m.group(1)) if m else None
            out.append(("pct", v if v is not None else raw.lower()))
        elif kind == "qty":
            m = re.search(r"([\d][\d,]*(?:\.\d+)?)", raw)
            v = _num(m.group(1)) if m else None
            out.append(("qty", v if v is not None else raw.lower()))
        else:  # num
            v = _num(raw)
            out.append(("num", v if v is not None else raw.lower()))
    return out


def numeric_multiset(text: str) -> List[float]:
    """Canonical numeric values only, sorted. Ignores kind."""
    vals = []
    for kind, raw in extract(text):
        v = None
        if kind == "money":
            v = _money(raw)
        elif kind == "pct":
            m = re.search(r"([\d][\d,]*(?:\.\d+)?)", raw)
            v = _num(m.group(1)) if m else None
        elif kind == "qty":
            m = re.search(r"([\d][\d,]*(?:\.\d+)?)", raw)
            v = _num(m.group(1)) if m else None
        elif kind == "num":
            v = _num(raw)
        if v is not None:
            vals.append(round(float(v), 6))
    return sorted(vals)


def compare_canonical(reference: str, submission: str) -> Dict[str, Any]:
    """Compare using canonical (kind, value) pairs."""
    ref, sub = canonical(reference), canonical(submission)
    # Sort by kind then by string representation of value for deterministic ordering
    ref_sorted = sorted(ref, key=lambda x: (x[0], str(x[1])))
    sub_sorted = sorted(sub, key=lambda x: (x[0], str(x[1])))
    missing = [k for k in ref_sorted if k not in sub_sorted]
    extra = [k for k in sub_sorted if k not in ref_sorted]
    return {"verdict": "match" if ref_sorted == sub_sorted else "mismatch",
            "n_reference": len(ref_sorted), "n_submission": len(sub_sorted),
            "missing": [list(map(str, k)) for k in missing],
            "extra": [list(map(str, k)) for k in extra]}


def compare_numeric(reference: str, submission: str) -> Dict[str, Any]:
    """Compare using numeric multiset only."""
    ref, sub = numeric_multiset(reference), numeric_multiset(submission)
    missing = [k for k in ref if k not in sub]
    extra = [k for k in sub if k not in ref]
    return {"verdict": "match" if ref == sub else "mismatch",
            "n_reference": len(ref), "n_submission": len(sub),
            "missing": missing, "extra": extra}


def fetch_federal_register(doc_number: str) -> Dict[str, str]:
    """Fetch a Federal Register document and split into SUMMARY and reference."""
    url = f"https://www.federalregister.gov/api/v1/documents/{doc_number}.json"
    with urllib.request.urlopen(url, timeout=30) as resp:
        data = json.load(resp)
    
    # Get full text
    full_text = data.get("body_html", "")
    if not full_text:
        # Try to get from PDF or other fields
        full_text = data.get("html_url", "")
    
    normalized = normalize(full_text)
    
    # Split on SUMMARY section
    summary_match = re.search(r"<summary>(.*?)</summary>", full_text, re.I | re.DOTALL)
    if summary_match:
        summary = normalize(summary_match.group(1))
        # Reference is everything except SUMMARY
        reference = re.sub(r"<summary>.*?</summary>", "", full_text, flags=re.I | re.DOTALL)
        reference = normalize(reference)
    else:
        # Fallback: try to find SUMMARY in normalized text
        parts = re.split(r"\bSUMMARY\b", normalized, maxsplit=1, flags=re.I)
        if len(parts) == 2:
            reference, summary = parts[0], parts[1]
        else:
            reference, summary = normalized, ""
    
    return {"reference": reference, "summary": summary, "title": data.get("title", ""),
            "document_number": doc_number}


def main() -> int:
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Verify values in a regulatory summary against source text",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 regvalue.py regulation.txt summary.txt
  python3 regvalue.py regulation.txt summary.txt --mode numeric
  python3 regvalue.py --fetch 2024-12345
  python3 regvalue.py --fetch 2024-12345 --mode numeric --json
        """
    )
    parser.add_argument("reference", nargs="?", help="Reference document (source text)")
    parser.add_argument("submission", nargs="?", help="Summary/submission to verify")
    parser.add_argument("--fetch", metavar="FR_DOC_NUMBER",
                        help="Fetch document from Federal Register API")
    parser.add_argument("--mode", choices=["canonical", "numeric"], default="canonical",
                        help="Comparison mode (default: canonical)")
    parser.add_argument("--json", action="store_true", help="Output JSON result")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if args.fetch:
        if args.reference or args.submission:
            parser.error("--fetch cannot be used with reference/submission arguments")
        try:
            data = fetch_federal_register(args.fetch)
            reference, submission = data["reference"], data["summary"]
            if not submission:
                print(f"Warning: No SUMMARY section found for {args.fetch}", file=sys.stderr)
                return 2
            if args.verbose:
                print(f"Fetched: {data['title']}", file=sys.stderr)
                print(f"Reference length: {len(reference)}, Summary length: {len(submission)}",
                      file=sys.stderr)
        except Exception as e:
            print(f"Error fetching {args.fetch}: {e}", file=sys.stderr)
            return 2
    elif args.reference and args.submission:
        try:
            with open(args.reference, "r") as f:
                reference = normalize(f.read())
            with open(args.submission, "r") as f:
                submission = normalize(f.read())
        except Exception as e:
            print(f"Error reading files: {e}", file=sys.stderr)
            return 2
    else:
        parser.error("Provide either --fetch or both reference and submission files")
    
    # Run comparison
    if args.mode == "canonical":
        result = compare_canonical(reference, submission)
    else:
        result = compare_numeric(reference, submission)
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Verdict: {result['verdict']}")
        print(f"Reference values: {result['n_reference']}")
        print(f"Submission values: {result['n_submission']}")
        if result["missing"]:
            print(f"Missing from submission ({len(result['missing'])}):")
            for m in result["missing"][:10]:
                print(f"  - {m}")
            if len(result["missing"]) > 10:
                print(f"  ... and {len(result['missing']) - 10} more")
        if result["extra"]:
            print(f"Extra in submission ({len(result['extra'])}):")
            for e in result["extra"][:10]:
                print(f"  - {e}")
            if len(result["extra"]) > 10:
                print(f"  ... and {len(result['extra']) - 10} more")
    
    return 0 if result["verdict"] == "match" else 1


if __name__ == "__main__":
    sys.exit(main())