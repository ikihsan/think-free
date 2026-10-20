#!/usr/bin/env python3
"""E195 — is the spend axis reachable from this host, and does a keyword select?

Terms, rows and gates are fixed in PROTOCOL.md. One request per row, no
retries, no key acquisition.
"""
import hashlib
import json
import os
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
os.makedirs(RAW, exist_ok=True)
UA = "think-free-research/0.1 (+repository spend-axis probe)"

GETS = [
    ("control", "stackexchange",
     "https://api.stackexchange.com/2.3/questions?site=stackoverflow&pagesize=1"),
    ("control", "openalex", "https://api.openalex.org/works?search=repair&per-page=1"),
    ("control", "github", "https://api.github.com/rate_limit"),
    ("spend", "usaspending_agencies",
     "https://api.usaspending.gov/api/v2/references/toptier_agencies/"),
    ("spend", "comtrade", "https://comtradeapi.un.org/public/v1/preview/C/A/HS"
     "?period=2023&reporterCode=842&cmdCode=590110&flowCode=M&partnerCode=0"),
]
POSTS = [
    ("spend", "usaspending_laundry"),
    ("spend", "usaspending_knitting"),
]


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30, context=ssl.create_default_context()) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception as e:
        return None, str(e).encode()


def award_post(keyword):
    """USAspending award search: a plain-language keyword, asking for the amount."""
    payload = {
        "filters": {
            "time_period": [{"start_date": "2020-01-01", "end_date": "2023-12-31"}],
            "keywords": [keyword],
        },
        "fields": ["Award ID", "Award Amount", "Description", "Awarding Agency"],
        "page": 1, "limit": 5, "subawards": False,
    }
    req = urllib.request.Request(
        "https://api.usaspending.gov/api/v2/search/spending_by_award/",
        data=json.dumps(payload).encode(),
        headers={"User-Agent": UA, "Content-Type": "application/json",
                 "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=40, context=ssl.create_default_context()) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except Exception as e:
        return None, str(e).encode()


def record(role, name, status, body, note=None):
    row = {"role": role, "source": name, "status": status, "bytes": len(body),
           "sha256": hashlib.sha256(body).hexdigest() if body else None,
           "excerpt": body[:200].decode("utf-8", "replace").replace("\n", " ")}
    try:
        data = json.loads(body.decode("utf-8", "replace"))
        row["json"] = True
        if isinstance(data, dict) and "results" in data:
            row["results_returned"] = len(data["results"])
        if isinstance(data, dict) and isinstance(data.get("results"), list):
            amounts = [r.get("Award Amount") for r in data["results"]
                       if isinstance(r, dict) and isinstance(r.get("Award Amount"), (int, float))]
            row["amount_rows"] = len(amounts)
            row["amount_total"] = sum(amounts) if amounts else None
        row["top_keys"] = sorted(data.keys())[:8] if isinstance(data, dict) else None
    except Exception:
        row["json"] = False
    if status == 200 and row.get("json"):
        row["verdict"] = "capture"
    elif status == 200:
        row["verdict"] = "refusal"
    else:
        row["verdict"] = "error"
    if note:
        row["note"] = note
    return row


def main():
    rows = [record(r, n, *get(u)) for r, n, u in GETS]
    for r, n in POSTS:
        st, body = award_post(n.replace("usaspending_", ""))
        rows.append(record(r, n, st, body, note="keyword=%s" % n.replace("usaspending_", "")))
    out = {"experiment": "E195", "host_python": sys.version.split()[0], "user_agent": UA,
           "rows": rows}
    with open(os.path.join(RAW, "probe.json"), "w") as fh:
        json.dump(out, fh, indent=2, sort_keys=True)
    for r in rows:
        print("%-24s %-9s %-5s %-9s bytes=%-7s %s" % (
            r["source"], r["role"], r["status"], r["verdict"], r["bytes"], r["excerpt"][:60]))
    by = {r["source"]: r for r in rows}
    controls = [r for r in rows if r["role"] == "control"]
    spends = [r for r in rows if r["role"] == "spend"]
    g1 = sum(1 for r in controls if r["verdict"] == "capture") >= 2
    with_amount = any(r.get("amount_rows") for r in spends)
    g2 = sum(1 for r in spends if r["verdict"] == "capture") >= 2 and with_amount
    l, k = by.get("usaspending_laundry"), by.get("usaspending_knitting")
    lt = (l or {}).get("amount_total") or 0
    kt = (k or {}).get("amount_total") or 0
    ratio = (lt / kt) if kt else float("inf")
    g3 = (ratio >= 2.0) or (lt > 0) != (kt > 0)
    gates = {"G1_control_integrity": g1, "G2_spend_axis_usable": g2,
             "G3_keyword_discriminates": bool(g3)}
    out["gates"] = gates
    out["amount_ratio_laundry_over_knitting"] = ratio
    with open(os.path.join(RAW, "probe.json"), "w") as fh:
        json.dump(out, fh, indent=2, sort_keys=True)
    print("")
    for kk, v in sorted(gates.items()):
        print("%-28s %s" % (kk, "PASS" if v else "FAIL"))
    print("rows carrying a numeric award amount: %s" % with_amount)
    print("laundry/knitting amount ratio: %s" % ratio)
    print("wrote %s" % os.path.join(RAW, "probe.json"))


if __name__ == "__main__":
    main()