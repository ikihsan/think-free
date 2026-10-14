#!/usr/bin/env python3
"""valueset.py — M2, the deterministic canonicalizer.

Does a submission report the same *values* as a reference answer, once
formatting is removed? Standard library only, deterministic, no network.

What it compares is a **multiset of canonical values**, so list order, thousands
separators, decimal trailing zeros, currency placement, percent spelling and
whitespace cannot change the verdict. What it does **not** compare is what each
value is said to be about: see the declared weakness in PROTOCOL.md.

M1 (E114's ground.py) binds values to their surrounding words; this module
deliberately does not, which is the trade this experiment exists to measure.
"""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "114-value-grounding"))
import ground  # noqa: E402  (E114's extractor, imported unchanged)

SCALES = {"thousand": 1e3, "million": 1e6, "billion": 1e9}


def _num(text):
    """Parse a numeric string to float, tolerating separators. None if not numeric."""
    t = text.replace(",", "").replace(" ", "").strip()
    try:
        return float(t)
    except ValueError:
        return None


def _money(raw):
    m = re.search(r"\$\s?([\d][\d,]*(?:\.\d+)?)\s*(thousand|million|billion)?",
                  raw, re.I)
    if not m:
        return None
    v = _num(m.group(1))
    if v is None:
        return None
    scale = SCALES.get((m.group(2) or "").lower())
    return v * scale if scale else v


def _date(raw):
    """Canonical (year, month, day) or None. Order of the two renderings varies."""
    v = re.sub(r"(\d)(st|nd|rd|th)\b", r"\1", raw, flags=re.I)
    m = re.match(r"([A-Za-z]+)\.?\s+(\d{1,2}),?\s+(\d{4})$", v)
    if m:
        mon = ground.ABBR.get(m.group(1)[:3].capitalize(), m.group(1))
        names = [n.lower() for n in ground.MONTHS]
        if mon.lower() in names:
            return (int(m.group(3)), names.index(mon.lower()) + 1, int(m.group(2)))
        return None
    m = re.match(r"(\d{1,2})\s+([A-Za-z]+),?\s+(\d{4})$", v)
    if m:
        mon = ground.ABBR.get(m.group(2)[:3].capitalize(), m.group(2))
        names = [n.lower() for n in ground.MONTHS]
        if mon.lower() in names:
            return (int(m.group(3)), names.index(mon.lower()) + 1, int(m.group(1)))
        return None
    m = re.match(r"(\d{1,2})/(\d{1,2})/(\d{2,4})$", v)
    if m:
        a, b, yr = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if yr < 100:
            yr += 2000 if yr < 70 else 1900
        if 1 <= a <= 12 <= 31 or 1 <= b <= 12 <= 31:
            if 1 <= a <= 12 and 1 <= b <= 12:
                return (yr, a, b) if a <= 12 and b <= 12 else None
        return None
    return None


def _code(raw):
    """A citation is compared as a collapsed string: spacing and case removed."""
    t = re.sub(r"\s+", " ", raw).strip().lower()
    t = re.sub(r"\s*\(\s*", "(", t)
    t = re.sub(r"\s*\)\s*", ")", t)
    return re.sub(r"[ .]", "", t)


def canonical(text):
    """Every value in `text` as a hashable canonical key, in document order."""
    out = []
    for kind, raw in ground.extract(text):
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


def numeric_multiset(text):
    """Canonical numeric values only, sorted. Used by the arm-integrity gate,
    because it is independent of the string canonicalization M2 compares with."""
    vals = []
    for kind, raw in ground.extract(text):
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


def compare(reference, submission):
    """Verdict and the values that differ, as sorted canonical key lists."""
    ref, sub = sorted(canonical(reference)), sorted(canonical(submission))
    missing = [k for k in ref if k not in sub]
    extra = [k for k in sub if k not in ref]
    return {"verdict": "match" if ref == sub else "mismatch",
            "n_reference": len(ref), "n_submission": len(sub),
            "missing": [list(map(str, k)) for k in missing][:20],
            "extra": [list(map(str, k)) for k in extra][:20]}


if __name__ == "__main__":
    import json
    ref, sub = sys.argv[1], sys.argv[2]
    print(json.dumps(compare(open(ref).read(), open(sub).read()), sort_keys=True))
