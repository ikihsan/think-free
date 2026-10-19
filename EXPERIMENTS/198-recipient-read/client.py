#!/usr/bin/env python3
"""Shared USAspending client for E198.

Every panel writes each response body to `raw/` with its sha256 before parsing
it, so the parse is reproducible from bytes that are on disk and a later reader
can tell a parse defect from a source defect.
"""
import hashlib
import json
import os
import ssl
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
UA = "think-free-research/0.1 (+repository federal-spend recipient experiment)"
BASE = "https://api.usaspending.gov/api/v2/search/"

# The declared window and award types. One place, so a panel cannot drift.
WINDOW = [{"start_date": "2020-01-01", "end_date": "2025-12-31"}]
AWARD_TYPES = ["A", "B", "C", "D"]

IT_CODES = ["DA01", "DA10", "7A21", "7030", "D304"]

# E196's head100 cell totals for C3 control
CELL_TOTALS = {
    "DA01": 94_910_000_000,
    "DA10": 33_010_000_000,
    "7A21": 29_210_000_000,
    "7030": 25_830_000_000,
    "D304": 20_370_000_000,
}


def base_filters(**extra):
    f = {"time_period": WINDOW, "award_type_codes": AWARD_TYPES}
    f.update(extra)
    return f


def call(endpoint, payload, capture_name, retries=2, pause=0.5):
    """POST to an endpoint, capture the body, return (status, parsed_or_text)."""
    os.makedirs(RAW, exist_ok=True)
    url = BASE + endpoint
    body = json.dumps(payload).encode()
    # Reuse a capture only when its stored *request key* matches, so a changed
    # parameter can never read a stale body back as if it were fresh.
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
            last = (status, raw)
            if e.code == 422 and attempt == retries:
                break
            if e.code not in (429, 500, 502, 503, 504) and attempt == retries:
                break
        except Exception as e:
            last = (None, ("%s: %s" % (type(e).__name__, e)).encode())
            raw = b""
            if attempt == retries:
                break
        time.sleep(pause * (attempt + 1))
    else:
        status, raw = last

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
    """USAspending's silent way of ignoring a filter: a 'not used' message."""
    msgs = (parsed or {}).get("messages") or []
    return [m for m in msgs if isinstance(m, str) and "were not used" in m]


def recipient_page(psc_code, page, limit=100, capture_prefix="recip"):
    """Fetch one page of recipients for a PSC code."""
    payload = {
        "filters": base_filters(psc_codes=[psc_code]),
        "limit": limit,
        "page": page,
        "spending_level": "awards"
    }
    capture_name = "%s_%s_p%d" % (capture_prefix, psc_code, page)
    return call("spending_by_category/recipient/", payload, capture_name)


def recipient_all(psc_code, capture_prefix="recip"):
    """Fetch all pages of recipients for a PSC code."""
    all_results = []
    page = 1
    has_next = True
    statuses = []
    unused_filters = []
    while has_next:
        st, parsed, meta = recipient_page(psc_code, page, capture_prefix=capture_prefix)
        statuses.append({"page": page, "status": st, "reused": meta.get("reused", False)})
        if st != 200 or not isinstance(parsed, dict):
            break
        results = parsed.get("results") or []
        all_results.extend(results)
        unused_filters.extend(unused_filter_messages(parsed))
        page_meta = parsed.get("page_metadata") or {}
        has_next = page_meta.get("hasNext", False)
        page += 1
    return all_results, statuses, unused_filters


def control_zzzz(capture_prefix="ctl"):
    """C1: PSC ZZZZ returns empty 200."""
    payload = {
        "filters": base_filters(psc_codes=["ZZZZ"]),
        "limit": 100, "page": 1, "spending_level": "awards"
    }
    return call("spending_by_category/recipient/", payload, "%s_zzzz" % capture_prefix)


def control_not_a_code(capture_prefix="ctl"):
    """C2: PSC not-a-code returns 422 or empty."""
    payload = {
        "filters": base_filters(psc_codes=["not-a-code"]),
        "limit": 100, "page": 1, "spending_level": "awards"
    }
    return call("spending_by_category/recipient/", payload, "%s_notacode" % capture_prefix)