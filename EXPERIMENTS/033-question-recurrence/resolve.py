"""E033 — resolve the canonical of the declared edge subset.

PROTOCOL.md section 7. For the first PER_SITE_EDGES duplicate closures per site in
file order, call /questions/{id}/related and take its top-ranked row as the API's
guess at the canonical. `related` 404s on a vectorised id list (observed), so this
costs one request per edge; the canonical's own metadata is then read in one batched
/questions/{ids} call, which is a cross-check on the id rather than the only source.
"""
import collections
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
LOG = os.path.join(RAW, "resolve_log.jsonl")
EDGES = os.path.join(RAW, "edges.jsonl")
CANON = os.path.join(RAW, "canonicals.jsonl")

BASE = "https://api.stackexchange.com/2.3"
PER_SITE_EDGES = 20          # PROTOCOL 7: "first 20 duplicate closures per site"
TAG = re.compile(r"<[^>]+>")


def record(**kw):
    with open(LOG, "a") as fh:
        fh.write(json.dumps(kw, sort_keys=True) + "\n")


def get(path, params):
    url = BASE + path + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "think-free/E033"})
    for attempt in range(1, 5):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                raw = resp.read().decode("utf-8", "replace")
                status = resp.getcode()
            if not raw.strip():
                record(url=url, status=status, bytes=0, verdict="refused_empty")
                return status, None, url
            data = json.loads(raw)
            record(url=url, status=status, bytes=len(raw),
                   sha256=hashlib.sha256(raw.encode("utf-8")).hexdigest(),
                   items=len(data.get("items", [])), quota=data.get("quota_remaining"),
                   verdict="ok", ts=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
            return status, data, url
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace") if e.fp else ""
            record(url=url, status=e.code, bytes=len(body), verdict="http_error",
                   body=body[:200], ts=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
            if e.code in (429, 500, 503):
                time.sleep(2 ** attempt)
                continue
            return e.code, None, url
        except Exception as e:                       # noqa: BLE001 - logged, not hidden
            record(url=url, status=0, verdict="exception", body=repr(e)[:200],
                   ts=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
            if attempt < 3:
                time.sleep(2 ** attempt)
                continue
            return 0, None, url
    return 0, None, url


def slim(row, site):
    owner = row.get("owner") or {}
    return {
        "question_id": row.get("question_id"),
        "site": site,
        "user_id": owner.get("user_id"),
        "display_name": owner.get("display_name"),
        "score": row.get("score"),
        "answer_count": row.get("answer_count"),
        "is_answered": row.get("is_answered"),
        "accepted_answer_id": row.get("accepted_answer_id"),
        "creation_date": row.get("creation_date"),
        "title": html.unescape(TAG.sub("", row.get("title") or "")),
    }


def main():
    rows = [json.loads(l) for l in open(os.path.join(RAW, "harvest.jsonl")) if l.strip()]
    by_site = collections.defaultdict(list)
    for r in rows:
        if r.get("closed_reason") == "Duplicate":
            by_site[r["site"]].append(r)

    picked = []
    for site in sorted(by_site):
        for r in by_site[site][:PER_SITE_EDGES]:
            picked.append(r)
    print("duplicate closures available: %s"
          % {s: len(v) for s, v in sorted(by_site.items())})
    print("edges declared for resolution: %d" % len(picked))

    edges = []
    for r in picked:
        status, data, url = get("/questions/%s/related" % r["question_id"],
                                {"site": r["site"]})
        items = (data or {}).get("items") or []
        print("dup=%-9s site=%-8s status=%s related=%d quota=%s"
              % (r["question_id"], r["site"], status, len(items),
                 (data or {}).get("quota_remaining")))
        edge = {
            "dup": {"question_id": r["question_id"], "site": r["site"],
                    "user_id": r["user_id"], "title": r["title"],
                    "score": r["score"], "answer_count": r["answer_count"],
                    "creation_date": r["creation_date"],
                    "closed_date": r.get("closed_date"), "body": r["body"]},
            "related_n": len(items),
            "related_status": status,
        }
        if items:
            edge["canonical"] = slim(items[0], r["site"])
            edge["canonical"]["related_rank"] = 1
            edge["canonical"]["related_rows"] = [
                {"question_id": i.get("question_id"), "score": i.get("score"),
                 "title": html.unescape(TAG.sub("", i.get("title") or ""))}
                for i in items]
        edges.append(edge)

    # One batched read of the canonicals' own rows: a cross-check on the id, not the
    # only source for its metadata (PROTOCOL 7).
    ids = [e["canonical"]["question_id"] for e in edges if e.get("canonical")]
    confirm = {}
    for site in sorted({e["dup"]["site"] for e in edges if e.get("canonical")}):
        mine = [i for i in ids
                if any(e["dup"]["site"] == site and e["canonical"]["question_id"] == i
                       for e in edges if e.get("canonical"))]
        for start in range(0, len(mine), 100):
            chunk = mine[start:start + 100]
            status, data, url = get("/questions/%s" % ",".join(str(i) for i in chunk),
                                    {"site": site, "filter": "default"})
            print("confirm site=%-8s ids=%d status=%s quota=%s"
                  % (site, len(chunk), status, (data or {}).get("quota_remaining")))
            for item in (data or {}).get("items", []):
                confirm[item.get("question_id")] = slim(item, site)

    with open(EDGES, "w") as fh:
        for e in edges:
            fh.write(json.dumps(e) + "\n")
    with open(CANON, "w") as fh:
        for qid in sorted(confirm):
            fh.write(json.dumps(confirm[qid]) + "\n")

    resolved = sum(1 for e in edges if e.get("canonical"))
    print("edges written: %d  with a top-ranked related row: %d  canonicals confirmed: %d"
          % (len(edges), resolved, len(confirm)))
    print("wrote %s and %s" % (os.path.relpath(EDGES), os.path.relpath(CANON)))


if __name__ == "__main__":
    main()