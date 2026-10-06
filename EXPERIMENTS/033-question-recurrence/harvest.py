"""Harvest the E033 population: 500 questions per site, two non-programming
Stack Exchange sites, chosen by a structural rule carrying no requirement
vocabulary.

PROTOCOL.md section 3. Every fetch records its request URL, status, byte count and
the sha256 of the response body, so the population can be re-derived or refuted
from committed bytes alone.
"""
import hashlib
import html
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
LOG = os.path.join(RAW, "fetch_log.jsonl")
OUT = os.path.join(RAW, "harvest.jsonl")

API = "https://api.stackexchange.com/2.3/questions"
# Declared order; the first two that yield PER_SITE questions inside the window.
# AMENDMENT-1: order and floors declared before this attempt's fetch. The first
# run's site list is in raw/fetch_log.jsonl and none of its counts were used.
SITES = ["travel", "math", "cooking", "outdoors"]
PER_SITE = 500
MIN_SITE = 400
SITES_USED = 3
FROM = 1704067200          # 2024-01-01T00:00:00Z
TO = 1719792000            # 2024-07-01T00:00:00Z
PAGESIZE = 100
MAX_PAGES = 5

TAG = re.compile(r"<[^>]+>")
WS = re.compile(r"\s+")


def plain(body_html):
    """Question bodies arrive as HTML; word counts are taken on the text."""
    text = re.sub(r"(?is)<(script|style).*?</\1>", " ", body_html or "")
    return WS.sub(" ", html.unescape(TAG.sub(" ", text))).strip()


def record(**kw):
    with open(LOG, "a") as fh:
        fh.write(json.dumps(kw, sort_keys=True) + "\n")


def fetch(site, page, sort="creation", order="desc", pagesize=PAGESIZE, extra=None):
    params = {
        "site": site,
        "pagesize": pagesize,
        "sort": sort,
        "order": order,
        "filter": "withbody",
        "fromdate": FROM,
        "todate": TO,
        "page": page,
    }
    if extra:
        params.update(extra)
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "think-free/E033"})
    attempt = 0
    while True:
        attempt += 1
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                raw = resp.read().decode("utf-8", "replace")
                status = resp.getcode()
            if not raw.strip():
                # F036/E028's shape: 200 whose body strips to nothing is a refusal.
                record(url=url, site=site, page=page, status=status, bytes=0,
                       sha256=hashlib.sha256(b"").hexdigest(), verdict="refused_empty")
                return status, None, url
            data = json.loads(raw)
            record(url=url, site=site, page=page, status=status, bytes=len(raw),
                   sha256=hashlib.sha256(raw.encode("utf-8")).hexdigest(),
                   items=len(data.get("items", [])), quota=data.get("quota_remaining"),
                   verdict="ok", ts=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
            return status, data, url
        except urllib.error.HTTPError as e:
            raw = e.read().decode("utf-8", "replace") if e.fp else ""
            record(url=url, site=site, page=page, status=e.code, bytes=len(raw),
                   sha256=hashlib.sha256(raw.encode("utf-8")).hexdigest(),
                   verdict="http_error", body=raw[:200],
                   ts=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
            if e.code in (429, 500, 503) and attempt < 5:
                time.sleep(2 ** attempt)
                continue
            return e.code, None, url
        except Exception as e:                       # noqa: BLE001 - logged, not hidden
            record(url=url, site=site, page=page, status=0, bytes=0,
                   verdict="exception", body=repr(e)[:200],
                   ts=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
            if attempt < 4:
                time.sleep(2 ** attempt)
                continue
            return 0, None, url


def usable(item, site):
    """PROTOCOL 3.3: every question in the sample is in the population. The only
    requirement is a question id, so no filter can quietly raise the rate."""
    qid = item.get("question_id")
    if qid is None:
        return None
    owner = item.get("owner") or {}
    text = plain(item.get("body", ""))
    return {
        "question_id": qid,
        "site": site,                        # the withbody filter omits `site`
        "user_id": owner.get("user_id"),
        "display_name": owner.get("display_name"),
        "creation_date": item.get("creation_date"),
        "score": item.get("score"),
        "answer_count": item.get("answer_count"),
        "is_answered": item.get("is_answered"),
        "closed_reason": item.get("closed_reason"),      # absent => not closed
        "closed_date": item.get("closed_date"),
        "title": html.unescape(TAG.sub("", item.get("title", ""))),
        "words": len(text.split()),
        "body": text,
    }


def main():
    os.makedirs(RAW, exist_ok=True)
    rows, used, seen = [], [], set()
    for site in SITES:
        if len(used) >= SITES_USED:
            break
        kept, page, dup_ids = [], 1, 0
        while page <= MAX_PAGES and len(kept) < PER_SITE:
            status, data, url = fetch(site, page)
            print("site=%-8s page=%s status=%s items=%s quota=%s"
                  % (site, page, status,
                     len(data.get("items", [])) if data else "-",
                     data.get("quota_remaining") if data else "-"))
            if status != 200 or not data:
                break
            for item in data.get("items", []):
                row = usable(item, site)
                if not row:
                    continue
                if row["question_id"] in seen:
                    dup_ids += 1
                    continue
                seen.add(row["question_id"])
                kept.append(row)
            if not data.get("has_more"):
                break
            page += 1
        print("  -> %s kept %d (pages=%d, repeat ids skipped=%d)"
              % (site, len(kept), page - 1, dup_ids))
        if len(kept) >= MIN_SITE:
            used.append(site)
            rows.extend(kept[:PER_SITE])
        else:
            print("  -> %s below the declared floor of %d; trying the next site in order"
                  % (site, MIN_SITE))

    with open(OUT, "w") as fh:
        for row in rows:
            fh.write(json.dumps(row) + "\n")
    print("sites used: %s" % used)
    print("rows: %d  distinct users: %d"
          % (len(rows), len({r["user_id"] for r in rows if r["user_id"] is not None})))
    print("wrote %s" % os.path.relpath(OUT))


if __name__ == "__main__":
    main()