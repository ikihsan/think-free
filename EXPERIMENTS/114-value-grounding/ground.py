#!/usr/bin/env python3
"""ground.py — is every claim in an answer supported by the document it is about?

Mechanical, standard library only, deterministic. It does not know which arm a
row came from and never sees the answer's correctness.

Two verdicts, because they are different failures and a tool that conflates them
is not useful:

  ungrounded_value  the value itself does not occur anywhere in the document
  ungrounded_claim  the value occurs, but nowhere near the words the answer uses
                    to describe it

A bare membership test is close to vacuous for a three-digit number in a
40 000-character rule, so a value is only counted as grounded when the sentence
around it in the answer is also found around an occurrence in the document.
"""
import html
import os
import re
import sys

STOP = set("""a an the of to in for and or by with at on from as is are be been was were
this that these those it its his her their our your my we they he she i you not no
also any all each other others such same more most less least than then so if when
while under over above below after before during between within without into onto
per each may must shall can could would should will do does did done have has had
be ing ed ly s""".split())

MONTHS = ("January February March April May June July August September October "
          "November December").split()
MONTH_RE = "|".join(MONTHS)
AMBIG = "January February March April May June July August September October " \
        "November December Jan Feb Mar Apr Jun Jul Aug Sep Sept Oct Nov Dec".split()

VALUE_PATTERNS = [
    ("money", re.compile(r"\$\s?\d[\d,]*(?:\.\d+)?(?:\s?(?:million|billion|thousand))?", re.I)),
    ("pct", re.compile(r"\d+(?:\.\d+)?\s?(?:percent|%)", re.I)),
    ("date", re.compile(
        r"(?:%s)\.?\s+\d{1,2},?\s+\d{4}" % MONTH_RE +
        r"|\d{1,2}\s+(?:%s)\.?\s+\d{4}" % MONTH_RE +
        r"|\d{1,2}/\d{1,2}/\d{2,4}", re.I)),
    ("code", re.compile(
        r"\d+\s+CFR\s+(?:part\s+)?[\d.]+(?:\s*(?:through|-|to)\s*[\d.]+)?(?:\([a-z0-9()]*\))*"
        r"|\d+\s+U\.?S\.?C\.?\s*(?:et seq\.)?\s*[\d.]*[a-z0-9()]*"
        r"|\d+\s+FR\s+\d+"
        r"|Docket\s+No\.?\s*[\w.()\-]+"
        r"|RIN\s+\d{4}-[A-Z]{2}\d{2}"
        r"|\b\d+\s*-\s*\d+\b(?=\s|$)[A-Z]?"
        r"|\b[A-Z]{2,5}\s+\d+\b"
        r"|\b\d{3}-\d{2}\b")),
    ("qty", re.compile(
        r"\d[\d,]*\s?(?:lb|lbs|pound|pounds|kg|kilograms?|mt|metric tons?|tons?|"
        r"nm|nautical miles?|feet|foot|deg|degrees?|miles?|hours?|days?|years?)", re.I)),
    ("num", re.compile(r"\b\d[\d,]*(?:\.\d+)?\b")),
]

SENT_SPLIT = re.compile(r"(?<=[.;:])\s+")


def strip_html(raw):
    txt = re.sub(r"<[^>]+>", " ", raw)
    txt = html.unescape(txt)
    txt = txt.replace(" ", " ")
    return txt


def normalize(raw):
    """Readable text: tags gone, entities decoded, hard line wraps joined."""
    txt = strip_html(raw)
    # GPO text is hard-wrapped mid-sentence; rejoin without inserting a break
    txt = re.sub(r"\s*\n\s*", " ", txt)
    txt = re.sub(r"[ \t]+", " ", txt)
    return txt.strip()


def content_words(text):
    words = re.findall(r"[A-Za-z][A-Za-z'\-]{2,}", text.lower())
    return set(w for w in words if w not in STOP)


def canonical(value, kind):
    """A shape-comparable rendering, so $56.00 and 56 match and 5,794,826 matches."""
    v = value.strip()
    v = re.sub(r"^\$\s?", "", v)
    v = re.sub(r"[\s,](?=(?:\d{3})+(?:\D|$))", "", v)
    v = v.replace(",", "")
    v = re.sub(r"^(0+)", "", v) if v.isdigit() else v
    v = re.sub(r"\.0+$", "", v)
    return v.lower()


def find_value(doc, value, kind):
    """Every offset in doc where `value` occurs under a permissive normalization."""
    cv = canonical(value, kind)
    if not cv:
        return []
    if kind == "money":
        bare = cv
        cands = {bare, bare.rstrip("0").rstrip(".") if "." in bare else bare}
        cands = {c for c in cands if c}
    else:
        cands = {cv}
    hits = []
    dlow = doc.lower()
    for c in cands:
        start = 0
        while True:
            i = dlow.find(c, start)
            if i < 0:
                break
            hits.append((i, i + len(c)))
            start = i + 1
    return hits


def occurrences(doc, value, kind):
    """Offsets where the value occurs, with a permissive word-order normalisation."""
    hits = find_value(doc, value, kind)
    if not hits:
        return []
    # tolerate the document splitting a cite across a line: retry on a de-spaced doc
    de = re.sub(r"\s+", "", doc)
    cv = canonical(value, kind)
    if cv and cv in de.lower():
        for m in re.finditer(re.escape(cv), de.lower()):
            hits.append(("despaced", m.start(), m.end()))
    return hits


def judge(doc, answer, threshold=0.6, window=90):
    """Return a list of {kind, value, verdict, score} for every value in `answer`."""
    out = []
    for sentence in SENT_SPLIT.split(answer):
        if not sentence.strip():
            continue
        seen = set()
        for kind, pat in VALUE_PATTERNS:
            for m in pat.finditer(sentence):
                raw = m.group(0)
                key = (kind, canonical(raw, kind))
                if key in seen:
                    continue
                seen.add(key)
                ctxt = content_words(sentence)
                ctxt.discard(canonical(raw, kind).replace(".", "").replace("-", ""))
                ctx = {w for w in ctxt
                       if w not in canonical(raw, kind).lower()}
                if not ctx:
                    continue
                hits = occurrences(doc, raw, kind)
                if not hits:
                    out.append({"kind": kind, "value": raw,
                                "verdict": "ungrounded_value", "score": 0.0})
                    continue
                best = 0.0
                for h in hits:
                    if h[0] == "despaced":
                        continue
                    s, e = h[0], h[1]
                    win = content_words(doc[max(0, s - window):e + window])
                    score = (len(ctx & win) / float(len(ctx))) if ctx else 0.0
                    best = max(best, score)
                out.append({"kind": kind, "value": raw,
                            "verdict": "grounded" if best >= threshold
                            else "ungrounded_claim",
                            "score": round(best, 3)})
    return out


def load_doc(num, rawdir):
    path = os.path.join(rawdir, "text", num + ".txt")
    with open(path, "rb") as fh:
        return normalize(fh.read().decode("utf-8", "replace"))


def main():
    import json
    rawdir = sys.argv[1]
    answers = sys.argv[2]
    threshold = float(sys.argv[3]) if len(sys.argv) > 3 else 0.6
    rows = [json.loads(l) for l in open(answers) if l.strip()]
    cache = {}
    total = 0
    counts = {}
    for r in rows:
        num = r["document_number"]
        if num not in cache:
            cache[num] = load_doc(num, rawdir)
        doc = cache[num]
        verdicts = judge(doc, r["answer"], threshold)
        r["checked"] = verdicts
        r["n_values"] = len(verdicts)
        total += len(verdicts)
        for v in verdicts:
            counts[v["verdict"]] = counts.get(v["verdict"], 0) + 1
    with open(os.path.join(os.path.dirname(answers), "checked.jsonl"), "w") as fh:
        for r in rows:
            fh.write(json.dumps(r, sort_keys=True) + "\n")
    print(json.dumps({"threshold": threshold, "rows": len(rows),
                      "values_checked": total, "counts": counts}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())