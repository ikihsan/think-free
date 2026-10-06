"""E034 — the network half of the reader: fetch the declared population and its two
amendment arms. Split out of `reask.py` at the 300-line cap, because the product surface
(a person running `report`) should not have to import an HTTP client to do it.

Nothing here decides anything. `reask.py` holds the declared registry and the report;
`tally.py` holds the gates. Every request is appended to raw/pages.jsonl with its response
body, so the sha256 in the log is recomputable from committed bytes rather than asserted.
"""

import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request

from reask import API, PAGE_SIZE, RAW, TAGS, DECLARED_TAGS, SAMPLES, url_for

HERE = os.path.dirname(os.path.abspath(__file__))
USER_AGENT = "think-free/E034"


def _get(url):
    """One request. Returns (status, body_bytes). A transport error is recorded as a
    status of 0 with the error text, never as an empty success."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=40) as resp:
            return resp.getcode(), resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()
    except Exception as exc:                                   # transport, DNS, timeout
        return 0, str(exc).encode()


def _row(it, stratum, site, tag, arm, sample):
    owner = it.get("owner") or {}
    return {"question_id": it.get("question_id"), "arm": arm, "sample": sample,
            "stratum": stratum, "site": site, "tag": tag,
            "score": it.get("score"), "closed_reason": it.get("closed_reason"),
            "closed_date": it.get("closed_date"), "is_answered": it.get("is_answered"),
            "accepted_answer_id": it.get("accepted_answer_id"),
            "answer_count": it.get("answer_count"), "view_count": it.get("view_count"),
            "creation_date": it.get("creation_date"), "title": it.get("title"),
            "user_id": owner.get("user_id"), "display_name": owner.get("display_name"),
            "has_closed_reason_key": "closed_reason" in it}


def _log(log, entry, body):
    entry.update(bytes=len(body), sha256=hashlib.sha256(body).hexdigest())
    try:
        doc = json.loads(body.decode("utf-8"))
    except Exception:
        entry.update(items=0, quota=None, has_more=None, verdict="unparsed")
        log.write(json.dumps(entry, sort_keys=True) + "\n")
        log.flush()
        return None, entry
    items = doc.get("items") or []
    entry.update(items=len(items), quota=doc.get("quota_remaining"),
                 has_more=doc.get("has_more"),
                 verdict="ok" if entry["status"] == 200 else "error")
    entry["body"] = body.decode("utf-8")
    log.write(json.dumps(entry, sort_keys=True) + "\n")
    log.flush()
    return doc, entry


def _fetch(pairs, sample, sleep, backoff_sleep=True):
    """Walk (stratum, site, tag, arm, page) tuples, appending every attempt to the log."""
    os.makedirs(RAW, exist_ok=True)
    rows = []
    with open(os.path.join(RAW, "pages.jsonl"), "a") as log:
        for stratum, site, tag, arm, page in pairs:
            url = url_for(site, tag, arm, page, PAGE_SIZE)
            status, body = _get(url)
            entry = {"url": url, "status": status, "stratum": stratum, "site": site,
                     "tag": tag, "arm": arm, "sample": sample, "page": page,
                     "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
            doc, entry = _log(log, entry, body)
            if doc is None:
                break
            for it in doc.get("items") or []:
                rows.append(_row(it, stratum, site, tag, arm, sample))
            if status != 200:
                break
            if backoff_sleep and doc.get("backoff"):
                time.sleep(int(doc["backoff"]) + 1)
            if not doc.get("has_more"):
                break
            time.sleep(sleep)
    return rows


def _write(path, rows):
    with open(path, "w") as fh:
        for r in rows:
            fh.write(json.dumps(r, sort_keys=True) + "\n")
    return len(rows)


def harvest(pages=4, sleep=0.4):
    """PROTOCOL.md section 3's population. Only the eight declared tags are harvested, in
    their declared order; AMENDMENT-1's two R2 tags are fetched by `replicate`, so
    re-running `harvest` reproduces the declared population and not the amended one.

    `pages` is the budget per arm per tag, never a target: a page that returns
    has_more=false ends that arm early, and `n` is always the fetched row count.
    """
    pairs = []
    for stratum, site, tag in [t for t in TAGS if t[2] in DECLARED_TAGS]:
        for arm in ("tail", "head", "default"):
            for page in range(1, pages + 1):
                pairs.append((stratum, site, tag, arm, page))
    rows = _fetch(pairs, "declared", sleep)
    n = _write(os.path.join(RAW, "harvest.jsonl"), rows)
    sys.stderr.write("harvest requests={} rows={}\n".format(
        requests=len(pairs), rows=n))
    return n


def replicate(sample="R1", tags=None, arm="tail", first=5, pages=4, sleep=0.4):
    """AMENDMENT-1. A sample disjoint from the declared population by construction: same
    route, same parameters, a page index the declared run did not read.

    `R1` reads the next pages for the two tags that decide A4, so a rate that holds there
    is a rate in a second sample. `R2` reads page 1 onwards for one further tag on each of
    the two sites whose single existing tag decided A4 — the site/tag confound test.

    R1 is *nearly* disjoint: the paginated ordering is not perfectly stable across the page
    boundary, so `tally.py` removes overlapping ids and reports the count.
    """
    if tags is None:
        _arm, _tags, _first = SAMPLES[sample]
        tags = _tags
    pairs = []
    for tag in tags:
        stratum, site = next((st, si) for st, si, tg in TAGS if tg == tag)
        for page in range(first, first + pages):
            pairs.append((stratum, site, tag, arm, page))
    rows = _fetch(pairs, sample, sleep)
    n = _write(os.path.join(RAW, "%s.jsonl" % sample.lower()), rows)
    sys.stderr.write("{sample} requests={len(pairs)} rows={n}\n".format(
        sample=sample, len=len(pairs), n=n))
    return n


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd")
    h = sub.add_parser("harvest")
    h.add_argument("--pages", type=int, default=4)
    rp = sub.add_parser("replicate")
    rp.add_argument("--sample", choices=sorted(SAMPLES), default="R1")
    rp.add_argument("--tags", nargs="+", default=None)
    rp.add_argument("--first", type=int, default=None)
    rp.add_argument("--pages", type=int, default=4)
    a = ap.parse_args()
    if a.cmd == "harvest":
        harvest(pages=a.pages)
    elif a.cmd == "replicate":
        replicate(sample=a.sample, tags=tuple(a.tags) if a.tags else None,
                  first=a.first if a.first is not None else (5 if a.sample == "R1" else 1),
                  pages=a.pages)
    else:
        ap.print_help()
    sys.exit(0)
