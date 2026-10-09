#!/usr/bin/env python3
"""E070 arm W - fetch confusion reports from two read-only APIs.

Stack Exchange (stackoverflow, unauthenticated) and the GitHub issue
search (unauthenticated). Queries are the pre-declared set from
PROTOCOL.md; nothing is added after the first fetch. Every response
body is written to raw/api/ verbatim before anything is read, so a
later re-read classifies the same bytes the classifier saw.

Rate limits: Stack Exchange answers backoff in the envelope and this
script honours it; GitHub allows 10 unauthenticated requests per
minute, so the script paces itself. Stdlib only.
"""
import json
import os
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw", "api")

# site, query, class  -- fixed before the first fetch
SE_QUERIES = [
    ("stackoverflow", "sklearn scikit-learn", "PC"),
    ("stackoverflow", "telegram python-telegram-bot", "PC"),
    ("stackoverflow", "beautifulsoup beautifulsoup4", "PC"),
    ("stackoverflow", "pip install color vs colour", "PC"),
    # Amendment 3: typed-name control queries - a B report
    # names the name the user typed, not the one they meant.
    ("stackoverflow", "pip install telegram", "PC"),
    ("stackoverflow", "pip install sklearn", "PC"),
    ("stackoverflow", "pip install beautifulsoup", "PC"),
    ("stackoverflow", "pip install color", "PC"),
    ("stackoverflow", "pip install succeeded but import failed", "G"),
    ("stackoverflow", "installed wrong package", "G"),
    ("stackoverflow", "pip install wrong package", "G"),
    ("stackoverflow", "pip install typo", "G"),
    ("stackoverflow", "different pypi package than intended", "G"),
    ("stackoverflow", "pip install similar name", "G"),
    ("stackoverflow", "how to install numpy python", "PL"),
    ("stackoverflow", "pip cache clear", "PL"),
]

GH_QUERIES = [
    ("pip install succeeded but import failed", "G"),
    ("installed wrong pypi package", "G"),
    ("pip install typo wrong package", "G"),
    ("installed the wrong package github issue", "G"),
    ("sklearn scikit-learn", "PC"),
    ("beautifulsoup beautifulsoup4", "PC"),
    ("pip install telegram", "PC"),
]


def get(url, pause):
    time.sleep(pause)
    req = urllib.request.Request(url,
                                 headers={"User-Agent": "E070-observation/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def stackexchange(site, query, pages=1):
    """All items for one query, honouring the API's own backoff."""
    items = []
    for page in range(1, pages + 1):
        params = urllib.parse.urlencode({
            "q": query, "site": site, "pagesize": 25,
            "page": page, "filter": "withbody"})
        url = "https://api.stackexchange.com/2.3/search/advanced?" + params
        d = get(url, 7.0)
        items.extend(d.get("items", []))
        if d.get("backoff"):
            time.sleep(int(d["backoff"]) + 1)
        if not d.get("has_more"):
            break
    return items


def github(query):
    params = urllib.parse.urlencode({"q": query + " type:issue",
                                     "per_page": 25})
    url = "https://api.github.com/search/issues?" + params
    d = get(url, 7.0)
    return d.get("items", [])


def main():
    os.makedirs(RAW, exist_ok=True)
    manifest = []
    for site, query, klass in SE_QUERIES:
        items = stackexchange(site, query)
        slug = "%s-%s" % (site, "".join(c if c.isalnum() else "-"
                                        for c in query).strip("-"))
        path = os.path.join(RAW, "se-%s.json" % slug)
        with open(path, "w") as f:
            json.dump({"site": site, "query": query, "class": klass,
                       "items": items}, f, indent=1)
        manifest.append({"venue": "stackexchange", "site": site,
                         "query": query, "class": klass,
                         "n": len(items), "file": os.path.basename(path)})
        print("se", site, repr(query), len(items), flush=True)
    for query, klass in GH_QUERIES:
        items = github(query)
        slug = "".join(c if c.isalnum() else "-" for c in query).strip("-")
        path = os.path.join(RAW, "gh-%s.json" % slug)
        with open(path, "w") as f:
            json.dump({"query": query, "class": klass,
                       "items": items}, f, indent=1)
        manifest.append({"venue": "github", "query": query,
                         "class": klass, "n": len(items),
                         "file": os.path.basename(path)})
        print("gh", repr(query), len(items), flush=True)
    with open(os.path.join(RAW, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=1)
    print("wrote", os.path.join(RAW, "manifest.json"))


if __name__ == "__main__":
    main()
