"""Reachability of the accepted answer's fix by the post's own error literal.

The instrument is deliberately one-sided.  A query that returns the fix is
evidence the developer's workflow finds it; a query that does not return it is
evidence about *this index and this query*, not about search in general, and is
recorded as such.
"""
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request

SEARCH = "https://api.github.com/search/issues"
UA = "think-free-e169/1.0"
TOPK = 10
_SLEEP = 6.5                      # unauthenticated search: 10 requests/minute
_TRACK = re.compile(r"github\.com/([^/\"']+)/([^/\"'#?]+)/(issues|pull)/(\d+)")


def github_target(answer_html):
    """(owner, repo, number) of the first tracker link in the accepted answer.

    `issues` and `pull` share one index in the search API, so a pull request is
    a legitimate return for an issue query.
    """
    for m in _TRACK.finditer(answer_html or ""):
        return {"owner": m.group(1), "repo": m.group(2), "number": int(m.group(4))}
    return None


def _norm(o, r, n):
    # Python 3.8 is one of the interpreters this repository's CI runs on, so no
    # str.removesuffix here.
    if r.lower().endswith(".git"):
        r = r[:-4]
    return "%s/%s#%d" % (o.lower(), r.lower(), n)


def _results(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "application/vnd.github+json"})
    try:
        with urllib.request.urlopen(req, timeout=45) as fh:
            return json.loads(fh.read().decode("utf-8")), None
    except urllib.error.HTTPError as exc:
        body = ""
        try:
            body = exc.read().decode("utf-8", "replace")[:120]
        except Exception:                                        # noqa: BLE001
            pass
        return None, "http_%d %s" % (exc.code, body)
    except Exception as exc:                                      # noqa: BLE001
        return None, "err %s" % type(exc).__name__


def query(literal, page=1):
    """One exact-phrase query.  Returns (items, total, error)."""
    q = '"%s"' % literal.replace('"', " ")
    url = "%s?%s" % (SEARCH, urllib.parse.urlencode(
        {"q": q, "per_page": TOPK, "page": page, "sort": "best-match"}))
    data, err = _results(url)
    time.sleep(_SLEEP)
    if err:
        return [], None, err
    return (data.get("items", []), data.get("total_count"), None)


def rank_of(items, target):
    """1-based position of the target among the returned items, else None."""
    want = _norm(target["owner"], target["repo"], target["number"])
    for i, it in enumerate(items[:TOPK], start=1):
        html_url = it.get("html_url", "")
        m = re.search(r"github\.com/([^/]+)/([^/]+)/(?:issues|pull)/(\d+)", html_url)
        if not m:
            continue
        if _norm(m.group(1), m.group(2), int(m.group(3))) == want:
            return i
    return None


def search_once(literal, target):
    items, total, err = query(literal)
    if err:
        # One retry at double the delay, declared in the protocol.
        time.sleep(_SLEEP)
        items, total, err = query(literal)
    if err:
        return {"rank": None, "unreadable": err, "total": None, "n_items": 0}
    return {"rank": rank_of(items, target), "unreadable": None,
            "total": total, "n_items": len(items)}


def variants(literal, tag):
    """G4 secondary arm: a human iterates, so two looser queries follow."""
    out = [literal]
    if tag:
        out.append("%s %s" % (literal, tag))
    words = literal.split()
    if len(words) > 6:
        out.append(" ".join(words[-6:]))
    seen, uniq = set(), []
    for v in out:
        v = " ".join(v.split())
        if v and v.lower() not in seen:
            seen.add(v.lower())
            uniq.append(v)
    return uniq[1:]


def search_variants(lits, target):
    """Try each declared variant in order; report the first hit's rank."""
    best = {"rank": None, "which": None, "tried": [], "unreadable": None}
    for v in lits:
        r = search_once(v, target)
        best["tried"].append(v)
        if r["unreadable"]:
            best["unreadable"] = r["unreadable"]
            continue
        if r["rank"]:
            best["rank"], best["which"] = r["rank"], v
            return best
    return best