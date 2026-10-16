"""GitHub issue search client and arm construction for E170.

The instrument's semantics were probed before the arms were declared and are
recorded in PROTOCOL.md: term-AND within a scope, `repo:`/`in:` honoured,
quotes NOT enforced as phrases, and a bare number parsed as an issue-number
qualifier.  Nothing here assumes more than that.
"""
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request

SEARCH = "https://api.github.com/search/issues"
CORE = "https://api.github.com/repos/%s/%s/issues/%d"
UA = "think-free-e170/1.0"
TOPK = 10
SLEEP = 6.5                      # unauthenticated search: 10 requests/minute
_NUM = re.compile(r"\d")
_TRACK = re.compile(
    r"github\.com/([^/\"']+)/([^/\"'#?]+)/(?:issues|pull)/(\d+)")
# Function words carry no discriminating power, so the control phrase is the
# first three non-function tokens of the target's body.  Fixed list, no tuning.
_STOP = set("""a an the and or but if then than that this these those it its is
are was were be been being am do does did done doing have has had having i me my we
our you your he him his she her it they them their what which who whom when where
why how all any both each few more most other some such no nor not only own same so
too very can will just should now for from with without about into over under again
out up down off on at by as is are was were were be been to in on of""".split())


def norm_target(owner, repo, number):
    return "%s/%s#%d" % (owner.lower(), repo.lower(), number)


def rank_of(items, target):
    """1-based position of the target among returned items, else None."""
    want = norm_target(*target)
    for i, it in enumerate(items, start=1):
        m = _TRACK.search(it.get("html_url") or "")
        if m and norm_target(m.group(1), m.group(2), int(m.group(3))) == want:
            return i
    return None


def _get(url, sleep_after=SLEEP):
    req = urllib.request.Request(
        url, headers={"User-Agent": UA, "Accept": "application/vnd.github+json"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=45) as fh:
                body = json.loads(fh.read().decode("utf-8"))
            time.sleep(sleep_after)
            return body, None
        except urllib.error.HTTPError as exc:
            detail = ""
            try:
                detail = exc.read().decode("utf-8", "replace")[:160]
            except Exception:                                     # noqa: BLE001
                pass
            if exc.code in (403, 429) and "rate limit" in detail.lower():
                wait = 70
                time.sleep(wait)
                continue
            return None, "http_%d %s" % (exc.code, detail)
        except Exception as exc:                                   # noqa: BLE001
            if attempt == 2:
                return None, "err %s" % type(exc).__name__
            time.sleep(3)
    return None, "rate_limited"


def search(query):
    """(items, total_count, error) for one query, per_page=TOPK."""
    url = "%s?%s" % (SEARCH, urllib.parse.urlencode(
        {"q": query, "per_page": TOPK}))
    data, err = _get(url)
    if err:
        return [], None, err
    return data.get("items", []), data.get("total_count"), None


def fetch_target(owner, repo, number):
    """The tracker document.  Core API: 60 requests/hour unauthenticated."""
    data, err = _get(CORE % (owner, repo, number), sleep_after=1.2)
    if err:
        return None, err
    return {"title": data.get("title"), "body": data.get("body") or "",
            "state": data.get("state"), "comments": data.get("comments")}, None


def control_phrase(body):
    """First three non-function, length>=3 tokens of the document.

    Deterministic and offline: it never consults the index, so it cannot be
    tuned toward whatever the index happens to like.
    """
    toks = [t for t in re.split(r"\s+", body or "")
            if len(t) >= 3 and not _STOP.match(t.lower().strip(".,;:()[]<>"))
            and re.search(r"[A-Za-z0-9]", t)]
    for n in (3, 2):
        if len(toks) >= n:
            return " ".join(toks[:n])
    return " ".join(toks)


def arms(row, target):
    """The seven query forms, declared in PROTOCOL.md."""
    phrase = (row.get("phrase") or "").strip()
    keyword = (row.get("keyword") or "").strip()
    scope = "repo:%s/%s" % (target["owner"], target["repo"])
    owner_re = re.compile(r"\b(%s|%s)\b" % (re.escape(target["owner"]),
                                           re.escape(target["repo"])),
                          re.I)
    a2 = " ".join(t for t in keyword.split() if not owner_re.match(t))
    out = [
        ("A0_bare_global", phrase),
        ("A0_quoted_global", '"%s"' % phrase if phrase else ""),
        ("A0_bare_repo", "%s %s" % (scope, phrase) if phrase else ""),
        ("A0_quoted_repo", '%s "%s"' % (scope, phrase) if phrase else ""),
        ("A1_global", keyword),
        ("A1_repo", "%s %s" % (scope, keyword)),
        ("A2_global", a2),
    ]
    return [(name, q) for name, q in out if q.strip()]


def has_number(text):
    return bool(_NUM.search(text or ""))