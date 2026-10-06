"""E035 -- fetch the Unanswered surface. PROTOCOL.md section 4's single arm.

Nothing here decides anything. Every request is appended to raw/pages.jsonl with its
response body, so the sha256 in the log is recomputable from committed bytes rather than
asserted (D061). `pages` is a budget per tag, never a target: a page that returns
has_more=false ends that tag's arm, and n is always the fetched row count.
"""

import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request

from analyse import TAGS

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

# PROTOCOL.md section 4. The Unanswered surface, ordered ascending by score, so that U1 is
# an identity test between two id sets rather than a comparison of two rates. E034's tail
# arm used pagesize=25; the /docs cap is 100 and section 8 declares the consequence.
API = "https://api.stackexchange.com/2.3/questions/unanswered"
PAGE_SIZE = 100
PAGES = 3
USER_AGENT = "think-free/E035"

# AMENDMENT-1. Attempt set 1 showed the two routes carry different default filters: this
# one omits closed_reason, closed_date and accepted_answer_id from the key set entirely,
# so the label was unreadable rather than absent. The filter is named explicitly here and
# the attempt set is recorded on every row, so a reader can tell which fetch produced it.
FILTER = "closed_reason;closed_date;accepted_answer_id"


def url_for(site, tag, page, pagesize=PAGE_SIZE):
    return ("{api}?site={site}&tagged={tag}&sort=votes&order=asc"
            "&filter={f}&pagesize={n}&page={p}").format(api=API, site=site, tag=tag,
                                                        f=FILTER, n=pagesize, p=page)


def _get(url):
    """One request. A transport error is recorded as status 0 with the error text, never
    as an empty success -- a status-0 row and a 200-with-no-items row are different facts."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.getcode(), resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()
    except Exception as exc:                                   # transport, DNS, timeout
        return 0, str(exc).encode()


def _row(it, site, tag, attempt):
    owner = it.get("owner") or {}
    return {"question_id": it.get("question_id"), "arm": "U", "attempt": attempt,
            "site": site, "tag": tag,
            "score": it.get("score"), "closed_reason": it.get("closed_reason"),
            "closed_date": it.get("closed_date"), "is_answered": it.get("is_answered"),
            "accepted_answer_id": it.get("accepted_answer_id"),
            "answer_count": it.get("answer_count"), "view_count": it.get("view_count"),
            "creation_date": it.get("creation_date"), "title": it.get("title"),
            "user_id": owner.get("user_id"), "display_name": owner.get("display_name"),
            "link": it.get("link"), "has_closed_reason_key": "closed_reason" in it}


def harvest(attempt=2, pages=PAGES, sleep=0.4):
    os.makedirs(RAW, exist_ok=True)
    rows = []
    attempts = []
    seen = set()
    suffix = "" if attempt == 1 else str(attempt)
    log_path = os.path.join(RAW, "pages%s.jsonl" % suffix)
    with open(log_path, "a") as log:
        for site, tag in TAGS:
            for page in range(1, pages + 1):
                url = url_for(site, tag, page)
                status, body = _get(url)
                entry = {"url": url, "status": status, "site": site, "tag": tag,
                         "arm": "U", "attempt": attempt, "page": page,
                         "bytes": len(body),
                         "sha256": hashlib.sha256(body).hexdigest(),
                         "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
                try:
                    doc = json.loads(body.decode("utf-8"))
                except Exception:
                    entry.update(items=0, quota=None, has_more=None, verdict="unparsed")
                    log.write(json.dumps(entry, sort_keys=True) + "\n")
                    log.flush()
                    attempts.append(entry)
                    break
                items = doc.get("items") or []
                entry.update(items=len(items), quota=doc.get("quota_remaining"),
                             has_more=doc.get("has_more"),
                             verdict="ok" if status == 200 else "error")
                entry["body"] = body.decode("utf-8")
                log.write(json.dumps(entry, sort_keys=True) + "\n")
                log.flush()
                attempts.append(entry)
                for it in items:
                    qid = it.get("question_id")
                    if qid in seen:
                        continue
                    seen.add(qid)
                    rows.append(_row(it, site, tag, attempt))
                if status != 200:
                    break
                if doc.get("backoff"):
                    time.sleep(int(doc["backoff"]) + 1)
                if not doc.get("has_more"):
                    break
                time.sleep(sleep)
    out = os.path.join(RAW, "u%s.jsonl" % suffix)
    with open(out, "w") as fh:
        for r in rows:
            fh.write(json.dumps(r, sort_keys=True) + "\n")
    with open(os.path.join(RAW, "attempts%s.json" % suffix), "w") as fh:
        json.dump(attempts, fh, indent=2, sort_keys=True)
    sys.stderr.write("U attempt{attempt} requests={n} rows={rows} quota_left={q}\n".format(
        attempt=attempt, n=len(attempts), rows=len(rows),
        q=attempts[-1]["quota"] if attempts else None))
    return len(rows)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--pages", type=int, default=PAGES)
    ap.add_argument("--attempt", type=int, default=2)
    harvest(attempt=ap.parse_args().attempt, pages=ap.parse_args().pages)
    sys.exit(0)
