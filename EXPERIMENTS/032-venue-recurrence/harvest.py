"""Harvest the E032 population: 60 long-form questions from non-programming
Stack Exchange sites, selected by a structural rule carrying no requirement
vocabulary.

PROTOCOL.md section "Population, declared before the fetch".
"""
import html
import json
import os
import re
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
LOG = os.path.join(RAW, "fetch_log.jsonl")
OUT = os.path.join(RAW, "harvest.jsonl")

API = "https://api.stackexchange.com/2.3/questions"
# Declared order; the first three that yield >= PER_SITE usable bodies are used.
SITES = ["woodworking", "outdoors", "cooking", "boardgames", "gardening"]
PER_SITE = 20
SITES_USED = 3
FROM = 1735689600          # 2025-01-01T00:00:00Z
TO = 1782000000            # 2026-06-16T00:00:00Z, the PROTOCOL window's end
MIN_WORDS, MAX_WORDS = 40, 600

TAG = re.compile(r"<[^>]+>")
WS = re.compile(r"\s+")


def plain(body_html):
    """Question bodies arrive as HTML; words are counted on the text."""
    text = re.sub(r"(?is)<(script|style).*?</\1>", " ", body_html)
    return WS.sub(" ", html.unescape(TAG.sub(" ", text))).strip()


def fetch(site, page, pagesize=100):
    params = {
        "site": site,
        "pagesize": pagesize,
        "order": "desc",
        "sort": "votes",
        "filter": "withbody",
        "fromdate": FROM,
        "todate": TO,
        "page": page,
    }
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "think-free/E032"})
    attempt = 0
    while True:
        attempt += 1
        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                raw = resp.read().decode("utf-8", "replace")
            return 200, json.loads(raw), raw
        except urllib.error.HTTPError as e:
            raw = e.read().decode("utf-8", "replace") if e.fp else ""
            if e.code in (400, 429, 500, 503) and attempt < 6:
                wait = 2 ** attempt
                record(site, page, e.code, len(raw), wait)
                time.sleep(wait)
                continue
            return e.code, None, raw
        except Exception as e:                      # noqa: BLE001 - logged, not hidden
            if attempt < 4:
                time.sleep(2 ** attempt)
                continue
            return 0, None, repr(e)


def record(site, page, status, nbytes, wait=None):
    with open(LOG, "a") as fh:
        fh.write(json.dumps({
            "site": site, "page": page, "status": status, "bytes": nbytes,
            "backoff_s": wait, "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }) + "\n")


def usable(item, site):
    """Exactly PROTOCOL step 2: 40..600 words of body, and a named author."""
    owner = (item.get("owner") or {}).get("display_name")
    if not owner:
        return None
    text = plain(item.get("body", ""))
    n = len(text.split())
    if n < MIN_WORDS or n > MAX_WORDS:
        return None
    return {
        "question_id": item.get("question_id"),
        # The withbody filter omits `site`, so it is stamped from the request.
        "site": site,
        "author": owner,
        "creation_date": item.get("creation_date"),
        "score": item.get("score"),
        "title": html.unescape(TAG.sub("", item.get("title", ""))),
        "words": n,
        "body": text,
    }


def main():
    os.makedirs(RAW, exist_ok=True)
    rows, used = [], []
    for site in SITES:
        if len(used) >= SITES_USED:
            break
        kept, page = [], 1
        while page <= 4 and len(kept) < PER_SITE:
            status, data, raw = fetch(site, page)
            record(site, page, status, len(raw))
            print("site=%s page=%s status=%s items=%s quota=%s"
                  % (site, page, status,
                     len(data.get("items", [])) if data else "-",
                     data.get("quota_remaining") if data else "-"))
            if status != 200 or not data:
                break
            for item in data.get("items", []):
                row = usable(item, site)
                if row:
                    kept.append(row)
                if len(kept) >= PER_SITE:
                    break
            if not data.get("has_more"):
                break
            page += 1
        if len(kept) >= PER_SITE:
            used.append(site)
            rows.extend(kept)
            print("  -> kept %d from %s" % (len(kept), site))

    with open(OUT, "w") as fh:
        for row in rows:
            fh.write(json.dumps(row) + "\n")
    print("sites used: %s" % used)
    print("rows: %d  distinct authors: %d" % (len(rows), len({r["author"] for r in rows})))
    print("wrote %s" % os.path.relpath(OUT))


if __name__ == "__main__":
    main()