#!/usr/bin/env python3
"""E016's third corpus via Bing, because DuckDuckGo refused all 19 first-pass
queries with HTTP 202 on 2026-10-04 (recorded in raw/web_search.jsonl).

Same declared queries as phrasings.json, same append-only convention. The
substitution of instrument is recorded in raw/probe_run.json, the README and
the session record, never passed over silently.

Picking a search engine's organic HTML is a different instrument than
DuckDuckGo's: what both can see is "anything a search engine indexes", what
differs is ranking and coverage. This bounds, but does not remove, the
corpora's stated blindness.
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
ENDPOINT = "https://www.bing.com/search?q={q}"
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
    out = []
    for block in re.findall(r'<li class="b_algo".*?</li>', body, re.S):
        link = re.search(r'<h2[^>]*><a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', block, re.S)
        if not link:
            continue
        snippet = re.search(r'<p[^>]*>(.*?)</p>', block, re.S)
        out.append({"title": clean(link.group(2)), "url": link.group(1),
                    "snippet": clean(snippet.group(1))[:300] if snippet else ""})
    return out


def main():
    os.makedirs(RAW, exist_ok=True)
    with open(os.path.join(HERE, "phrasings.json"), encoding="utf-8") as fh:
        items = json.load(fh)["items"]
    items.sort(key=lambda it: (not it.get("control", False), it["index"]))
    for item in items:
        for query in item["web"]:
            time.sleep(PACE)
            code, body = fetch(query)
            rec = {"corpus": "openweb", "engine": "bing-html",
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
