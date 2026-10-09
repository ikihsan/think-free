#!/usr/bin/env python3
"""E071 probe: does each platform's public API expose an arrival/view field?

Declared in PROTOCOL.md before any result was read. Three arms:

  A  Hacker News  - firebase item objects  (the E063/E066 HN corpus source)
  B  GitHub       - REST issue objects   (the E063/E066 GitHub corpus source)
  C  Stack Exchange - /2.3/questions     (the E062 route; positive control)

The measurement is the presence or absence of the field on the returned object.
A field that exists but is zero is a measured zero; a field that is absent is a
missing observation and never a denominator (D082). The probe records both,
separately, so a reader can tell the two apart.

Stdlib only. One request per item, one thread pool, results appended to
raw/probe.json. Exit 0: this is a measurement, not a gate; outcome.py reads the
gate table out of the same JSON.
"""

import json
import os
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

UA = "ThinkFree-E071/1.0 (arrival-field existence probe)"

HN_ITEM = "https://hacker-news.firebaseio.com/v0/item/%d.json"
HN_TOP = "https://hacker-news.firebaseio.com/v0/topstories.json"
GH_ISSUE = "https://api.github.com/repos/%s/issues/%d"
SE_QUESTIONS = "https://api.stackexchange.com/2.3/questions"

# Public repos chosen because they have issues enabled and are not rate-limited
# for anonymous reads. The exact ids are recorded in raw/probe.json so the
# sample is reproducible.
GH_REPOS = [
    ("fivethirtyeight/data", 1), ("torvalds/linux", 2),
    ("nodejs/node", 1), ("microsoft/vscode", 1),
    ("facebook/react", 1), ("rust-lang/rust", 1),
    ("python/cpython", 1), ("golang/go", 1),
]
SE_SITES = ["cooking", "gardening", "diy", "woodworking"]

# Every key any inspected API has used for an arrival / view count, plus the
# generic ones, so the absence is an absence of the whole family and not of one
# spelling.
ARRIVAL_KEYS = (
    "view_count", "views", "viewCount", "viewed", "viewed_count",
    "impressions", "hits", "pageviews",
)


def get(url, tries=3, timeout=45):
    """GET with retries. Returns (status, parsed_json_or_None, raw_bytes)."""
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read()
                try:
                    return resp.status, json.loads(raw.decode("utf-8")), raw
                except ValueError:
                    return resp.status, None, raw
        except Exception as exc:  # noqa: BLE001 - recorded, not swallowed
            if attempt == tries - 1:
                return 0, None, str(exc).encode("utf-8")
            time.sleep(1.5 * (attempt + 1))
    return 0, None, b""


def summarise(obj):
    """Which arrival keys does this object carry, and what are their values?

    Distinguishes three states per key: absent, present-and-zero, present-and-
    positive. A platform that never returns the key at all is a missing
    observation, not a zero.
    """
    if not isinstance(obj, dict):
        return {"present": False, "state": "not_an_object", "keys": []}
    keys = sorted(k for k in obj if k in ARRIVAL_KEYS)
    out = {"present": bool(keys), "state": "absent", "keys": keys, "values": {}}
    if keys:
        positive = False
        for k in keys:
            v = obj.get(k)
            out["values"][k] = v
            try:
                if float(v) > 0:
                    positive = True
            except (TypeError, ValueError):
                pass
        out["state"] = "positive" if positive else "zero"
    return out


def arm_hn(n=60):
    status, ids, _ = get(HN_TOP)
    ids = (ids or [])[:n]
    if not isinstance(ids, list):
        return {"platform": "hackernews", "rows": [], "error": "no topstories"}

    def one(i):
        st, obj, _ = get(HN_ITEM % i)
        return {"id": i, "http": st, "type": (obj or {}).get("type"),
                "top_level_keys": sorted((obj or {}).keys())
                if isinstance(obj, dict) else [],
                "arrival": summarise(obj)}

    with ThreadPoolExecutor(max_workers=8) as pool:
        rows = list(pool.map(one, ids))
    return {"platform": "hackernews", "source": HN_TOP, "rows": rows}


def arm_github():
    def one(spec):
        repo, num = spec
        st, obj, _ = get(GH_ISSUE % (repo, num))
        return {"repo": repo, "number": num, "http": st,
                "top_level_keys": sorted(obj.keys())
                if isinstance(obj, dict) else [],
                "arrival": summarise(obj)}

    with ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(one, GH_REPOS))
    return {"platform": "github", "source": "GET /repos/{owner}/{repo}/issues/{n}",
            "rows": rows}


def arm_stackexchange(sites=None):
    """Positive control: the surface E062 actually measured."""
    sites = sites or SE_SITES
    rows = []
    for site in sites:
        url = (SE_QUESTIONS + "?site=%s&pagesize=20&order=desc&sort=votes"
               "&filter=!nNPvSNdWme" % site)
        st, obj, raw = get(url)
        items = (obj or {}).get("items") if isinstance(obj, dict) else None
        if not items:
            rows.append({"site": site, "http": st, "arrival": summarise(obj),
                         "n_rows": 0, "error": "no items"})
            continue
        present = sum(1 for it in items if "view_count" in it)
        positive = sum(1 for it in items
                       if isinstance(it.get("view_count"), (int, float))
                       and it["view_count"] > 0)
        rows.append({
            "site": site, "http": st, "n_rows": len(items),
            "with_view_count_key": present,
            "with_view_count_positive": positive,
            "arrival": {"present": present > 0,
                        "state": "positive" if positive else
                                 ("zero" if present else "absent"),
                        "keys": ["view_count"] if present else []},
            "sample_view_counts": [it.get("view_count") for it in items[:8]],
        })
    return {"platform": "stackexchange", "source": SE_QUESTIONS, "rows": rows}


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "raw", "probe.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)

    arms = {"arm_a_hackernews": arm_hn(),
            "arm_b_github": arm_github(),
            "arm_c_stackexchange_control": arm_stackexchange()}
    payload = {"experiment": "071-viewcount-denominator", "date": "2026-10-09",
               "arrival_keys_probed": list(ARRIVAL_KEYS),
               "arms": arms}
    with open(out, "w") as fh:
        json.dump(payload, fh, indent=1, sort_keys=True)

    for name, arm in sorted(arms.items()):
        ok = [r for r in arm["rows"] if r.get("arrival", {}).get("present")]
        tot = [r for r in arm["rows"] if not r.get("error")]
        print("%-32s rows=%-4d carrying_an_arrival_field=%d"
              % (name, len(tot), len(ok)))
    print("\nwrote", out)


if __name__ == "__main__":
    sys.exit(main())