"""E035 -- AMENDMENT-2. Re-read the Unanswered surface's ids through the route that carries
the closure label.

`/questions/unanswered` refuses every custom filter (PROTOCOL.md section 4b), so its own
bytes cannot say whether a question was already answered elsewhere. `/questions/{ids}`
accepts the same ids, 100 per request, and its default filter includes `closed_reason`.

This adds a label and removes nothing: the ids, scores, sites and tags stay as fetched in
attempt set 1, and the merge is keyed on `question_id`. A row the re-read cannot find is
recorded as `unread` rather than dropped, because "the API did not return it" and "it has
no closure label" are different facts.
"""

import collections
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
API = "https://api.stackexchange.com/2.3/questions"
CHUNK = 100
USER_AGENT = "think-free/E035"


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.getcode(), resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()
    except Exception as exc:
        return 0, str(exc).encode()


def load_u(path=None):
    path = path or os.path.join(RAW, "u1.jsonl")
    with open(path) as fh:
        return [json.loads(l) for l in fh if l.strip()]


def chunks(seq, n=CHUNK):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


def relabel(sleep=0.4, page_size=CHUNK):
    rows = load_u()
    ids = sorted({r["question_id"] for r in rows})
    # The {ids} route requires `site` as well; the first attempt omitted it and got
    # 400 `site is required` on its only request. That attempt stays in raw/relabel.jsonl.
    by_site = collections.defaultdict(list)
    for r in rows:
        by_site[r["site"]].append(r["question_id"])
    found = {}
    attempts = []
    log_path = os.path.join(RAW, "relabel.jsonl")
    with open(log_path, "a") as log:
        for site in sorted(by_site):
            for group in chunks(sorted(set(by_site[site])), page_size):
                url = "{api}/{ids}?site={site}&pagesize={n}".format(
                    api=API, ids=";".join(map(str, group)), site=site, n=page_size)
                status, body = _get(url)
                entry = {"url_prefix": "{api}/<{n} ids>?site={site}".format(
                             api=API, n=len(group), site=site),
                         "site": site, "ids": [str(i) for i in group], "status": status,
                         "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest(),
                         "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
                try:
                    doc = json.loads(body.decode("utf-8"))
                except Exception:
                    entry.update(items=0, quota=None, verdict="unparsed")
                    log.write(json.dumps(entry, sort_keys=True) + "\n")
                    log.flush()
                    attempts.append(entry)
                    continue
                items = doc.get("items") or []
                entry.update(items=len(items), quota=doc.get("quota_remaining"),
                             verdict="ok" if status == 200 else "error")
                entry["body"] = body.decode("utf-8")
                log.write(json.dumps(entry, sort_keys=True) + "\n")
                log.flush()
                attempts.append(entry)
                for it in items:
                    found[it["question_id"]] = {"closed_reason": it.get("closed_reason"),
                                                "closed_date": it.get("closed_date"),
                                                "has_closed_reason_key": "closed_reason" in it}
                if status != 200:
                    break
                if doc.get("backoff"):
                    time.sleep(int(doc["backoff"]) + 1)
                time.sleep(sleep)

    merged, unread = [], []
    for r in rows:
        got = found.get(r["question_id"])
        if got is None:
            unread.append(r["question_id"])
            r["closed_reason"] = None
            r["has_closed_reason_key"] = False
            r["label_state"] = "unread"
        else:
            r.update(got)
            r["label_state"] = "read"
        merged.append(r)
    out = os.path.join(RAW, "u_labelled.jsonl")
    with open(out, "w") as fh:
        for r in merged:
            fh.write(json.dumps(r, sort_keys=True) + "\n")
    with open(os.path.join(RAW, "relabel_attempts.json"), "w") as fh:
        json.dump(attempts, fh, indent=2, sort_keys=True)
    keyed = sum(1 for r in merged if r["label_state"] == "read"
                and r["has_closed_reason_key"])
    sys.stderr.write("relabel requests={} rows={} labelled={} unread={} quota_left={}\n".format(
        len(attempts), len(merged), keyed, len(unread),
        attempts[-1]["quota"] if attempts else None))
    return len(merged)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--page-size", type=int, default=CHUNK)
    relabel(page_size=ap.parse_args().page_size)
    sys.exit(0)
