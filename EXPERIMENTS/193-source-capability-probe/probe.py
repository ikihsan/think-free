#!/usr/bin/env python3
"""E193 — source capability probe. One request per source, declared in PROTOCOL.md.

Records status, content-type, byte count, sha256, and a 200-character raw
excerpt for each source. A 200 whose body strips to <200 non-whitespace
characters is recorded as `refusal`, not `capture` (the E028 lesson).

No retries, no proxies, no rotating identity. One request each.
"""
import hashlib
import json
import os
import ssl
import sys
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
os.makedirs(RAW, exist_ok=True)

UA = "think-free-research/0.1 (+repository evidence probe; contact: none)"

SOURCES = [
    ("stackexchange", "control", "https://api.stackexchange.com/2.3/questions?site=stackoverflow&pagesize=1"),
    ("github", "control", "https://api.github.com/search/repositories?q=knitting+repair&per_page=1"),
    ("openalex", "control", "https://api.openalex.org/works?search=knit%20graph&per-page=1"),
    ("duckduckgo", "control", "https://html.duckduckgo.com/html/?q=knitting+repair"),
    ("reddit", "demand", "https://www.reddit.com/r/knitting/search.json?q=mending&restrict_sr=1&limit=5"),
    ("etsy", "demand", "https://www.etsy.com/search?q=knitting%20repair%20service"),
    ("ebay", "demand", "https://www.ebay.com/sch/i.html?_nkw=knitting+mending+service&_sacat=0"),
    ("opencollective", "demand", "https://api.opencollective.com/graphql"),
    ("census_cbp", "demand", "https://api.census.gov/data/2022/cbp?get=NAME&for=us:*"),
    ("datagov", "demand",
     "https://catalog.data.gov/api/3/action/package_search?q=repair&rows=1"),
]

POST_BODY = {"opencollective": json.dumps({"query": "{ allCategories { total } }"})}


def fetch(url, name):
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "application/json, text/html;q=0.9, */*;q=0.8",
    })
    if name in POST_BODY:
        req.data = POST_BODY[name].encode()
        req.add_header("Content-Type", "application/json")
    row = {"source": name, "url": url, "method": "POST" if name in POST_BODY else "GET"}
    try:
        with urllib.request.urlopen(req, timeout=25, context=ctx) as r:
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
    except Exception as e:  # DNS, TLS, timeout, connection reset
        row["status"] = None
        row["error"] = "%s: %s" % (type(e).__name__, e)
        row["bytes"] = 0
        row["sha256"] = None
        row["nonws_chars"] = 0
        row["verdict"] = "unreachable"
        row["excerpt"] = ""
        return row
    row["bytes"] = len(body)
    row["sha256"] = hashlib.sha256(body).hexdigest() if body else None
    text = body.decode("utf-8", "replace")
    row["nonws_chars"] = len("".join(text.split()))
    row["excerpt"] = text[:200].replace("\n", " ")
    if row["status"] == 200 and row["nonws_chars"] >= 200:
        row["verdict"] = "capture"
    elif row["status"] == 200:
        row["verdict"] = "refusal"
    else:
        row["verdict"] = "error"
    return row


def main():
    rows = [fetch(url, name) for name, role, url in SOURCES]
    for r, (_n, role, _u) in zip(rows, SOURCES):
        r["role"] = role
    out = {
        "experiment": "E193",
        "host_python": sys.version.split()[0],
        "user_agent": UA,
        "rows": rows,
    }
    path = os.path.join(RAW, "probe.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2, sort_keys=True)
    for r in rows:
        print("%-15s %-8s %-5s %-9s bytes=%-8s nonws=%-8s %s" % (
            r["source"], r["role"], r["status"], r["verdict"], r["bytes"],
            r["nonws_chars"], r.get("error", "")[:60]))
    controls = [r for r in rows if r["role"] == "control"]
    demand = [r for r in rows if r["role"] == "demand"]
    g1 = sum(1 for r in controls if r["verdict"] == "capture") >= 3
    g2 = sum(1 for r in demand if r["verdict"] == "capture") >= 2
    print("G1 control integrity (>=3 of 4 captures): %s" % ("PASS" if g1 else "FAIL"))
    print("G2 usable demand sources (>=2 of 6 captures): %s" % ("PASS" if g2 else "FAIL"))
    print("wrote %s" % path)


if __name__ == "__main__":
    main()