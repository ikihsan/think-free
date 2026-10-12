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
40 000-character rule, so a value counts as grounded only when the words around
it **in the answer** are also found around an occurrence **in the document**.

v1. v0 failed the verbatim control at 0.367 (see AMENDMENT-2.md). Three fixes:
context is a character window in the answer rather than a sentence split, because
splitting on `[.;]` cuts inside `49 CFR 1002.3(a)`; date matching tries every
plausible rendering instead of one string with its commas deleted; and the `code`
pattern no longer matches `Page 64617`. Values nested inside a longer match are
dropped, so `49 CFR 1002.3(a)` counts once and not four times.
"""
import html
import os
import re
import sys

STOP = set("""a an the of to in for and or by with at on from as is are be been was
were this that these those it its his her their our your my we they he she i you
not no also any all each other others such same more most less least than then
so if when while under over above below after before during between within
without into onto per may must shall can could would should will do does did
done have has had""".split())

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]
MONTH_RE = "|".join(MONTHS)
ABBR = {"Jan": "January", "Feb": "February", "Mar": "March", "Apr": "April",
        "May": "May", "Jun": "June", "Jul": "July", "Aug": "August",
        "Sep": "September", "Sept": "September", "Oct": "October",
        "Nov": "November", "Dec": "December"}
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
        r"|\b\d{2,4}-\d{3,4}\b(?=[A-Z])")),
    ("qty", re.compile(
        r"\d[\d,]*(?:\.\d+)?\s?(?:lb|lbs|pound|pounds|kg|kilogram|kilograms|"
        r"mt|metric ton|metric tons|ton|tons|nautical mile|nautical miles|"
        r"\bnm\b|foot|feet|\bm\b|degree|degrees|hour|hours|day|days|year|years)",
        re.I)),
    ("num", re.compile(r"\b\d[\d,]*(?:\.\d+)?\b")),
]


def normalize(raw):
    """Readable text: tags gone, entities decoded, hard line wraps joined."""
    txt = re.sub(r"<[^>]+>", " ", raw)
    txt = html.unescape(txt).replace(" ", " ")
    txt = re.sub(r"\s*\n\s*", " ", txt)
    return re.sub(r"[ \t]+", " ", txt).strip()


BOUND = re.compile(r"[.;](?=\s)|—")


def unit(text, start, end, cap=420):
    """The enclosing sentence-or-table-row of text[start:end].

    A fixed character window is wrong for tabular rules: in a fee table the
    description sits a hundred characters to the left of the amount, so the
    window never sees the words that identify what the amount is *for*. Split
    on `.`/`;` followed by whitespace but never inside a number or a citation.
    """
    left = 0
    for m in BOUND.finditer(text, max(0, start - cap), start):
        left = m.end()
    right = len(text)
    for m in BOUND.finditer(text, end, min(len(text), end + cap)):
        right = m.start() + 1
        break
    return text[left:right]


SUFFIX = ("ings", "ing", "edly", "ed", "es", "s", "ly", "ment", "tion", "ions")


def stem(w):
    for suf in SUFFIX:
        if len(w) > len(suf) + 3 and w.endswith(suf):
            return w[:-len(suf)]
    return w


def content_words(text):
    return set(stem(w) for w in re.findall(r"[a-z][a-z'\-]{2,}", text.lower())
               if w not in STOP)


def date_renderings(value):
    """Every rendering a document might legitimately use for this date."""
    v = re.sub(r"(\d)(st|nd|rd|th)\b", r"\1", value, flags=re.I)
    v = v.replace(".", "")
    out = {v.lower().replace(",", ""), v.lower()}
    m = re.match(r"([A-Za-z]+)\s+(\d{1,2}),?\s+(\d{4})$", v)
    if m:
        mon, day, yr = m.group(1), m.group(2), m.group(3)
        mon = ABBR.get(mon[:3].capitalize(), mon)
        out |= {"%s %s, %s" % (mon, day, yr), "%s %s %s" % (mon, day, yr),
                "%s %d, %s" % (mon, int(day), yr)}
    m = re.match(r"(\d{1,2})\s+([A-Za-z]+),?\s+(\d{4})$", v)
    if m:
        day, mon, yr = m.group(1), m.group(2), m.group(3)
        mon = ABBR.get(mon[:3].capitalize(), mon)
        out |= {"%s %s, %s" % (mon, day, yr), "%s %s %s" % (mon, day, yr)}
    m = re.match(r"(\d{1,2})/(\d{1,2})/(\d{2,4})$", v)
    if m:
        a, b, yr = m.group(1), m.group(2), m.group(3)
        out |= {"%s/%s/%s" % (a, b, yr), "%s/%s/%s" % (b, a, yr)}
    return {o for o in out if o}


def renderings(value, kind):
    """The strings under which this value may legitimately occur."""
    v = value.strip()
    if kind == "date":
        return date_renderings(v)
    v = re.sub(r"^\$\s*", "", v)
    v = re.sub(r"\s+(?:million|billion|thousand)$", "", v, flags=re.I)
    cands = {v.lower()}                       # the comma form, as the document writes it
    bare = v.replace(",", "")
    cands.add(bare.lower())
    if "." in bare:
        cands.add(bare.rstrip("0").rstrip(".").lower())
    if kind == "money" and "." not in bare:
        cands.add(bare + ".00")
    return {c for c in cands if c}


def extract(answer):
    """Every value claim in the answer, longest match wins, no nested double-count."""
    spans = []
    for kind, pat in PATTERNS:
        for m in pat.finditer(answer):
            spans.append((m.start(), m.end(), kind, m.group(0)))
    spans.sort(key=lambda s: (s[0], -(s[1] - s[0])))
    kept = []
    for s, e, kind, raw in spans:
        if any(k[0] <= s and e <= k[1] for k in kept):
            continue
        kept.append((s, e, kind, raw))
    return [(k, r) for _, _, k, r in kept]


def judge(doc, answer, threshold=0.6, window=90):
    dlow = doc.lower()
    out = []
    for kind, raw in extract(answer):
        at = answer.find(raw)
        # Two granularities, applied symmetrically to both sides, best-of wins.
        # Sentence-unit alone cannot score an enumerating answer (its unit is one
        # clause of a very long ";"-separated sentence); fixed-window alone cannot
        # score a fee table (the row label sits ~100 characters from the amount).
        ctxs = [content_words(unit(answer, at, at + len(raw))),
                content_words(answer[max(0, at - window):at + len(raw) + window])]
        ctxs = [c for c in ctxs if c]
        if not ctxs:
            continue
        best = 0.0
        found = False
        for cand in renderings(raw, kind):
            start = 0
            while True:
                i = dlow.find(cand, start)
                if i < 0:
                    break
                found = True
                wins = [content_words(unit(doc, i, i + len(cand))),
                        content_words(doc[max(0, i - window):i + len(cand) + window])]
                for ctx in ctxs:
                    for win in wins:
                        if ctx:
                            best = max(best, len(ctx & win) / float(len(ctx)))
                start = i + 1
                if best >= 0.999:
                    break
            if best >= 0.999:
                break
        if not found:
            out.append({"kind": kind, "value": raw,
                        "verdict": "ungrounded_value", "score": 0.0})
        else:
            out.append({"kind": kind, "value": raw,
                        "verdict": "grounded" if best >= threshold
                        else "ungrounded_claim", "score": round(best, 3)})
    return out


def load_doc(num, rawdir):
    with open(os.path.join(rawdir, "text", num + ".txt"), "rb") as fh:
        return normalize(fh.read().decode("utf-8", "replace"))


def main():
    import json
    rawdir, answers = sys.argv[1], sys.argv[2]
    threshold = float(sys.argv[3]) if len(sys.argv) > 3 else 0.6
    out_name = sys.argv[4] if len(sys.argv) > 4 else "checked.jsonl"
    rows = [json.loads(l) for l in open(answers) if l.strip()]
    cache, total, counts = {}, 0, {}
    for r in rows:
        num = r["document_number"]
        if num not in cache:
            cache[num] = load_doc(num, rawdir)
        r["checked"] = judge(cache[num], r["answer"], threshold)
        r["n_values"] = len(r["checked"])
        total += len(r["checked"])
        for v in r["checked"]:
            counts[v["verdict"]] = counts.get(v["verdict"], 0) + 1
    with open(os.path.join(os.path.dirname(answers), out_name), "w") as fh:
        for r in rows:
            fh.write(json.dumps(r, sort_keys=True) + "\n")
    print(json.dumps({"threshold": threshold, "rows": len(rows),
                      "values_checked": total, "counts": counts}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())