#!/usr/bin/env python3
"""Shared USAspending client for E196.

Every panel writes each response body to `raw/` with its sha256 before parsing
it, so the parse is reproducible from bytes that are on disk and a later reader
can tell a parse defect from a source defect.
"""
import hashlib
import math
import json
import os
import ssl
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
UA = "think-free-research/0.1 (+repository federal-spend metering experiment)"
BASE = "https://api.usaspending.gov/api/v2/search/"

# The declared window and award types. One place, so a panel cannot drift.
WINDOW = [{"start_date": "2020-01-01", "end_date": "2025-12-31"}]
AWARD_TYPES = ["A", "B", "C", "D"]


def base_filters(**extra):
    f = {"time_period": WINDOW, "award_type_codes": AWARD_TYPES}
    f.update(extra)
    return f


def call(endpoint, payload, capture_name, retries=2, pause=0.6):
    """POST to an endpoint, capture the body, return (status, parsed_or_text)."""
    os.makedirs(RAW, exist_ok=True)
    url = BASE + endpoint
    body = json.dumps(payload).encode()
    # Reuse a capture only when its stored *request key* matches, so a changed
    # parameter can never read a stale body back as if it were fresh. This is
    # what makes AMENDMENT-3's re-run free for the 1,300 captures already on
    # disk, and it is why the reuse is checked against the stored request
    # rather than against the file's existence.
    meta_path = os.path.join(RAW, capture_name + ".meta.json")
    for suffix in (".json", ".body"):
        body_path = os.path.join(RAW, capture_name + suffix)
        if os.path.exists(body_path) and os.path.exists(meta_path):
            try:
                prior = json.load(open(meta_path))
                if (prior.get("request") == payload
                        and prior.get("response", {}).get("endpoint") == url):
                    with open(body_path, "rb") as fh:
                        cached = fh.read()
                    meta = dict(prior["response"], reused=True)
                    try:
                        return (meta.get("status"),
                                json.loads(cached.decode("utf-8", "replace")), meta)
                    except Exception:
                        break
            except Exception:
                break
    last = (None, "")
    for attempt in range(retries + 1):
        req = urllib.request.Request(
            url, data=body,
            headers={"User-Agent": UA, "Content-Type": "application/json",
                     "Accept": "application/json"})
        try:
            with urllib.request.urlopen(
                    req, timeout=180,
                    context=ssl.create_default_context()) as r:
                status, raw = r.status, r.read()
            break
        except urllib.error.HTTPError as e:
            status, raw = e.code, e.read()
            last = (status, raw.decode("utf-8", "replace")[:400])
            if e.code == 422 and attempt == retries:
                break
        except Exception as e:  # network, TLS, timeout
            last = (None, "%s: %s" % (type(e).__name__, e))
            raw = b""
            if attempt == retries:
                break
        time.sleep(pause * (attempt + 1))
    else:  # pragma: no cover - loop always breaks or returns
        status, raw = last

    # The body is written as `.json` so the repository's `raw/*.json` negation in
    # .gitignore tracks it. Raw response bytes are the evidence; a capture the
    # record cannot commit is a capture nobody can recompute from.
    with open(os.path.join(RAW, capture_name + ".json"), "wb") as fh:
        fh.write(raw or b"")
    meta = {"endpoint": url, "status": status,
            "bytes": len(raw or b""),
            "sha256": hashlib.sha256(raw or b"").hexdigest()}
    with open(os.path.join(RAW, capture_name + ".meta.json"), "w") as fh:
        json.dump({"request": payload, "response": meta}, fh, indent=1,
                  sort_keys=True)
    try:
        parsed = json.loads((raw or b"").decode("utf-8", "replace"))
    except Exception:
        parsed = None
    return status, parsed, meta


def unused_filter_messages(parsed):
    """USAspending's silent way of ignoring a filter: a 'not used' message.

    E196's G2 turns on this. A request whose filter was ignored returns a
    confident, well-formed answer about the *wrong* population.
    """
    msgs = (parsed or {}).get("messages") or []
    return [m for m in msgs if isinstance(m, str) and "were not used" in m]


def by_award(payload, capture_name, **kw):
    p = {"fields": ["Award ID", "Award Amount", "Description",
                    "generated_unique_award_id", "Awarding Agency"],
         "subawards": False, "sort": "Award Amount", "page": 1, "limit": 100}
    p.update(payload)
    return call("spending_by_award/", p, capture_name, **kw)


def award_count(psc_code, capture_name, **kw):
    p = {"filters": base_filters(psc_codes=[psc_code]),
         "subawards": False, "page": 1, "limit": 1}
    return call("spending_by_award_count/", p, capture_name, **kw)


def category_psc(payload, capture_name, **kw):
    p = {"limit": 100, "page": 1, "spending_level": "awards"}
    p.update(payload)
    return call("spending_by_category/psc/", p, capture_name, **kw)


def rank_profile(psc_code, ranks, capture_prefix):
    """AMENDMENT-3: the amount block at each declared ascending rank.

    Returns {rank: {"page", "min", "max", "rows", "status"}} where `max` is
    the exact maximum of the 100-row block containing that rank, so "at least
    k awards are at or below `max`" is a one-sided exact statement rather than
    an interpolation.
    """
    out = {}
    for rank in ranks:
        page = max(1, int(math.ceil(rank / 100.0)))
        st, parsed, _ = by_award(
            {"filters": base_filters(psc_codes=[psc_code]), "order": "asc",
             "page": page}, "%s_rank%d_p%d" % (capture_prefix, rank, page))
        results = (parsed or {}).get("results") if isinstance(parsed, dict) else None
        amts = [r["Award Amount"] for r in (results or [])
                if isinstance(r.get("Award Amount"), (int, float))]
        out[rank] = {"page": page, "status": st, "rows": len(amts),
                     "min": min(amts) if amts else None,
                     "max": max(amts) if amts else None}
    return out


def low_tail_awards(psc_code, cutoff, capture_prefix, max_pages=6):
    """Every award of a code with `Award Amount` <= cutoff (AMENDMENT-1).

    Ascending order makes the walk exhaustive rather than a sample: it stops the
    moment an amount exceeds the cutoff, so the rows collected are the whole
    low tail of the code's award-amount distribution, not the first k of them.

    Returns (rows, walked_pages, stopped_cleanly, statuses). Rows are the raw
    award dicts; zero and negative amounts are left in place for the caller to
    tally separately, because folding a deobligation into a small-purchase total
    would let a cell shrink itself below the bar.
    """
    rows, statuses = [], []
    walked, stopped = 0, False
    for page in range(1, max_pages + 1):
        st, parsed, _ = by_award(
            {"filters": base_filters(psc_codes=[psc_code]), "order": "asc",
             "page": page},
            "%s_p%d" % (capture_prefix, page))
        statuses.append(st)
        walked = page
        if st != 200:
            break
        results = parsed.get("results") if isinstance(parsed, dict) else None
        if not isinstance(results, list) or not results:
            stopped = True
            break
        over = False
        for r in results:
            amt = r.get("Award Amount")
            if not isinstance(amt, (int, float)):
                continue
            if amt > cutoff:
                over = True
                break
            rows.append(r)
        if over:
            stopped = True
            break
    return rows, walked, stopped, statuses