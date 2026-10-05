#!/usr/bin/env python3
"""E016's third corpus: the open web, through DuckDuckGo's HTML endpoint.

The declared corpus is "the open web". The harness's own web search tool was
tried three times on 2026-10-04 and answered `Web search cancelled` each time,
so the corpus is read over HTTP instead. That is a substitution of instrument and
it is recorded in raw/probe_run.json and in the README rather than passed over
silently; the queries are exactly the ones declared in phrasings.json.

This is the corpus no prior-art probe in this repository has read. It is also the
corpus a practitioner would use: the question is what happens when you type the
need into a search engine.

Standard library only. Appends to raw/web_search.jsonl and never decides
anything: attribution is recorded separately.
"""
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
ENDPOINT = "https://html.duckduckgo.com/html/?q={q}"
UA = "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) think-free-e015/1"
PACE = 4.0


def clean(text):
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text or ""))).strip()


def fetch(query):
    url = ENDPOINT.format(q=urllib.parse.quote_plus(query))
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html"})
    try:
        with urllib.request.urlopen(req, timeout=40) as fh:
            return fh.getcode(), fh.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, ""
    except Exception as exc:
        return "error:%s" % type(exc).__name__, ""


def parse(body):
    """Titles and destinations out of the HTML endpoint's result markup."""
    out = []
    for block in re.findall(r'<div class="result results_links.*?</div>\s*</div>', body, re.S):
        link = re.search(r'class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', block, re.S)
        if not link:
            continue
        href = html.unescape(link.group(1))
        dest = ""
        m = re.search(r"uddg=([^&]+)", href)
        if m:
            dest = urllib.parse.unquote(m.group(1))
        snippet = re.search(r'class="result__snippet"[^>]*>(.*?)</a>', block, re.S)
        out.append({"title": clean(link.group(2)), "url": dest,
                    "snippet": clean(snippet.group(1))[:300] if snippet else ""})
    return out


def main():
    os.makedirs(RAW, exist_ok=True)
    which = sys.argv[1] if len(sys.argv) > 1 else "first"
    with open(os.path.join(HERE, "phrasings.json"), encoding="utf-8") as fh:
        items = json.load(fh)["items"]
    items.sort(key=lambda it: (not it.get("control", False), it["index"]))
    for item in items:
        phrasings = item["web"]
        queries = phrasings[:1] if which == "first" else phrasings[1:]
        for query in queries:
            time.sleep(PACE)
            code, body = fetch(query)
            rec = {"corpus": "openweb", "engine": "duckduckgo-html",
                   "index": item["index"], "name": item["name"], "query": query,
                   "http_status": code, "url": ENDPOINT.format(q=urllib.parse.quote_plus(query))}
            rec["results"] = parse(body) if code == 200 else []
            with open(os.path.join(RAW, "web_search.jsonl"), "a", encoding="utf-8") as fh:
                fh.write(json.dumps(rec, sort_keys=True) + "\n")
            print("web %2d %-18s %-52s n=%d %s" % (
                item["index"], item["name"], query[:52], len(rec["results"]), code), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
