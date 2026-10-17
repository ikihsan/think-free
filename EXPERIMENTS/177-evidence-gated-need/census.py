#!/usr/bin/env python3
"""E177 measurement 1: the evidence-gain census, over all rows with an accepted answer.

Descriptive and automatic. **Not** the arm definition - see PROTOCOL.md. The
arms are a reader's judgement; this is a lexical overlap count, reported so the
census characterises the region whether or not the comparison fires.

Evidence gain = share of the accepted answer's content tokens that do not
already appear in the question (title + body). The stopword list is fixed here,
written before the fetch, and is not tuned to any result.
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOKEN = re.compile(r"[a-z0-9_+.\-]{3,}")

STOP = set("""
the and for that with this from you your are was were not but all any can has
had its out get use used using make makes made one two three first last same
how what why when where which who whom whose will would should could may might
must does did done doing have here they them their there then than into over
under about after before while only also just like more most some such each
other another because been being both few many much own very dont doesnt
isnt arent wasnt werent cant couldnt shouldnt wouldnt dont
""".split())


def toks(text):
    return [t for t in TOKEN.findall((text or "").lower()) if t not in STOP]


def strip_html(text):
    return re.sub(r"<[^>]+>", " ", text or "")


def wilson(k, n, z=1.959963985):
    if not n:
        return (0.0, 1.0)
    p = k / float(n)
    d = 1.0 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / d
    return (max(0.0, c - h), min(1.0, c + h))


def main():
    data = json.load(open(os.path.join(HERE, "rows.json")))
    rows = [r for r in data["rows"] if r.get("key_body")]
    out = []
    for r in rows:
        q = toks(strip_html(r["title"]) + " " + strip_html(r["body"]))
        a = toks(strip_html(r["key_body"]))
        qset = set(q)
        aset = set(a)
        gain_set = aset - qset
        gain = (len(gain_set) / float(len(aset))) if aset else 0.0
        out.append({"qid": r["qid"], "view_count": r["view_count"],
                    "q_tokens": len(qset), "a_tokens": len(aset),
                    "evidence_gain": round(gain, 4),
                    "gain_tokens": sorted(gain_set)[:40]})
    gains = sorted(o["evidence_gain"] for o in out)
    n = len(gains)
    med = gains[n // 2] if n else 0.0
    at_half = sum(1 for g in gains if g >= 0.5)
    lo, hi = wilson(at_half, n)
    result = {
        "rows_with_key_answer": n,
        "rows_drawn": len(data["rows"]),
        "evidence_gain_median": med,
        "evidence_gain_min": gains[0] if n else None,
        "evidence_gain_max": gains[-1] if n else None,
        "share_gain_ge_0.50": at_half,
        "share_gain_ge_0.50_rate": round(at_half / n, 4) if n else None,
        "share_gain_ge_0.50_ci95": [round(lo, 4), round(hi, 4)],
        "rows_sha256": data["sha256"],
        "census_sha256": hashlib.sha256(
            json.dumps(out, sort_keys=True).encode()).hexdigest(),
        "stopwords": len(STOP),
    }
    with open(os.path.join(HERE, "census.json"), "w") as fh:
        json.dump({"summary": result, "rows": out}, fh, indent=1, sort_keys=True)
        fh.write("\n")
    for k in ("rows_with_key_answer", "evidence_gain_median",
              "share_gain_ge_0.50", "share_gain_ge_0.50_rate",
              "share_gain_ge_0.50_ci95"):
        print("%-28s %s" % (k, result[k]))
    return 0


if __name__ == "__main__":
    sys.exit(main())