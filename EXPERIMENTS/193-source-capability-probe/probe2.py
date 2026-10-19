#!/usr/bin/env python3
"""E193 panel 2 — money-bearing sources that are not marketplaces.

Same recording rule as panel 1, with the two instrument defects AMENDMENT-1
declares fixed: a 2xx body that carries a refusal marker is a `refusal`, and a
JSON endpoint whose body does not parse is a `refusal`, whatever its length.

One request per source. No retries, no key acquisition, no identity rotation.
"""
import hashlib
import json
import os
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
os.makedirs(RAW, exist_ok=True)

UA = "think-free-research/0.1 (+repository evidence probe)"

# A 2xx body carrying one of these is a refusal, whatever its length.
REFUSAL_MARKERS = (
    "missing key", "captcha", "challenge", "are you a robot", "access denied",
    "unusual traffic", "enable javascript",
)

SOURCES = [
    ("itunes", "demand",
     "https://itunes.apple.com/search?" + urllib.parse.urlencode(
         {"term": "knitting repair", "entity": "software", "limit": 5, "country": "us"}),
     "json"),
    ("gbooks", "demand",
     "https://www.googleapis.com/books/v1/volumes?" + urllib.parse.urlencode({"q": "knitting repair", "maxResults": 5}),
     "json"),
    ("comtrade", "demand",
     "https://comtradeapi.un.org/public/v1/preview/C/A/HS?" + urllib.parse.urlencode(
         {"period": "2023", "reporterCode": "842", "cmdCode": "590110", "flowCode": "M", "partnerCode": "0"}),
     "json"),
    ("opencollective", "demand", "https://api.opencollective.com/graphql", "json"),
]

POST_BODY = {"opencollective": json.dumps({
    "query": "{ collective(slug: \"webpack\") { name stats { totalTransactions startDate } } }"})}

HTML_MARKERS = {"itunes": "resultCount", "gbooks": "totalItems", "comtrade": "data"}


def classify(name, status, ctype, body):
    text = body.decode("utf-8", "replace")
    low = text[:4000].lower()
    if status is None or not (200 <= status < 300):
        return "error"
    for m in REFUSAL_MARKERS:
        if m in low:
            return "refusal"
    if ctype and "json" in ctype:
        try:
            json.loads(text)
        except Exception:
            return "refusal"
        return "capture" if text.strip() else "refusal"
    marker = HTML_MARKERS.get(name)
    if marker and marker in text[:20000]:
        return "capture"
    return "refusal"


def fetch(name, role, url, kind):
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "application/json, text/html;q=0.9, */*;q=0.8"})
    if name in POST_BODY:
        req.data = POST_BODY[name].encode()
        req.add_header("Content-Type", "application/json")
    row = {"source": name, "role": role, "url": url,
           "method": "POST" if name in POST_BODY else "GET"}
    try:
        with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
            body = r.read()
            row["status"] = r.status
            row["content_type"] = r.headers.get("Content-Type", "")
    except urllib.error.HTTPError as e:
        body = b""
        try:
            body = e.read()
        except Exception:
            pass
        row["status"] = e.code
        row["content_type"] = e.headers.get("Content-Type", "") if e.headers else ""
    except Exception as e:
        row.update({"status": None, "error": "%s: %s" % (type(e).__name__, e), "bytes": 0,
                    "sha256": None, "verdict": "unreachable", "excerpt": ""})
        return row
    row["bytes"] = len(body)
    row["sha256"] = hashlib.sha256(body).hexdigest() if body else None
    row["excerpt"] = body[:200].decode("utf-8", "replace").replace("\n", " ")
    row["verdict"] = classify(name, row["status"], row["content_type"], body)
    return row


def main():
    rows = [fetch(n, r, u, k) for n, r, u, k in SOURCES]
    out = {"experiment": "E193", "panel": 2, "host_python": sys.version.split()[0],
           "user_agent": UA, "rows": rows}
    path = os.path.join(RAW, "probe2.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2, sort_keys=True)
    for r in rows:
        print("%-15s %-4s %-9s bytes=%-8s %s" % (r["source"], r["status"], r["verdict"],
                                                 r["bytes"], (r.get("error") or "")[:50]))
    caps = sum(1 for r in rows if r["verdict"] == "capture")
    g2b = caps >= 2
    print("G2-panel2 (>=2 of 4 captures): %s  [%d captured]" % ("PASS" if g2b else "FAIL", caps))
    print("panel 1's failure stands; this panel is additive")
    print("wrote %s" % path)


if __name__ == "__main__":
    main()