#!/usr/bin/env python3
"""E206 API client module: HTTP calls, caching, and utilities."""

import hashlib
import json
import os
import time
import urllib.error
import urllib.request
import ssl

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
UA = "think-free-research/0.1 (+repository think-free E206)"
BASE = "https://api.usaspending.gov/api/v2/search/"

AWARD_TYPES = ["A", "B", "C", "D"]
FULL_WINDOW = [{"start_date": "2020-01-01", "end_date": "2025-12-31"}]
RECENT_WINDOW = [{"start_date": "2024-10-01", "end_date": "2025-09-30"}]


def base_filters(**extra):
    f = {"award_type_codes": AWARD_TYPES}
    f.update(extra)
    return f


def call(endpoint, payload, capture_name, retries=3, pause=0.5):
    """POST to an endpoint, capture the body, return (status, parsed_or_text, meta)."""
    os.makedirs(RAW, exist_ok=True)
    url = BASE + endpoint
    body = json.dumps(payload).encode()
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
    msgs = (parsed or {}).get("messages") or []
    return [m for m in msgs if isinstance(m, str) and "were not used" in m]