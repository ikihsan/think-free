#!/usr/bin/env python3
"""E194 — price and demand scan over the iTunes Search API.

Terms, window, metrics and gates are fixed in PROTOCOL.md before this ran.
One request per term, no retries, no sorting after the fetch, no filtering.
"""
import hashlib
import json
import os
import ssl
import statistics
import sys
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
os.makedirs(RAW, exist_ok=True)
UA = "think-free-research/0.1 (+repository demand scan)"
WINDOW = 50

TERMS = [
    ("control_positive", "todo"),
    ("control_positive", "password manager"),
    ("control_negative", "zzqxqv glorb tapestry"),
    ("difficulty", "shift schedule"),
    ("difficulty", "receipt scanner"),
    ("difficulty", "warranty tracker"),
    ("difficulty", "home inventory"),
    ("difficulty", "meal plan"),
    ("difficulty", "pet medication"),
    ("difficulty", "chore chart"),
    ("difficulty", "moving checklist"),
    ("difficulty", "plant watering"),
    ("difficulty", "reading list"),
    ("difficulty", "sourdough"),
    ("difficulty", "pool care"),
]
REPEAT = ("difficulty", "pool care"), ("difficulty", "sourdough")


def fetch(term):
    url = "https://itunes.apple.com/search?" + urllib.parse.urlencode(
        {"term": term, "entity": "software", "country": "us", "limit": 200})
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    row = {"term": term, "url": url, "fetched_utc": None}
    try:
        with urllib.request.urlopen(req, timeout=30,
                                    context=ssl.create_default_context()) as r:
            body = r.read()
            row["status"] = r.status
    except urllib.error.HTTPError as e:
        row["status"] = e.code
        body = b""
    except Exception as e:
        row.update({"status": None, "error": "%s: %s" % (type(e).__name__, e),
                    "result_count": None, "apps": []})
        return row
    data = json.loads(body.decode("utf-8", "replace"))
    row["result_count"] = data.get("resultCount")
    row["body_sha256"] = hashlib.sha256(body).hexdigest()
    apps = []
    for a in data.get("results", []):
        apps.append({
            "trackId": a.get("trackId"),
            "name": a.get("trackName"),
            "seller": a.get("sellerName"),
            "price": a.get("formattedPrice") or ("%.2f" % a.get("price", 0.0)),
            "price_value": a.get("price"),
            "ratings": a.get("userRatingCount"),
            "rating": a.get("averageUserRating"),
            "genre": (a.get("primaryGenreName") or ""),
        })
    row["apps"] = apps[:WINDOW]
    row["apps_returned"] = len(apps)
    return row


def measure(row):
    apps = row.get("apps") or []
    paid = [a for a in apps if (a.get("price_value") or 0) > 0]
    free = [a for a in apps if (a.get("price_value") or 0) == 0]
    prices = [a["price_value"] for a in paid if a.get("price_value") is not None]
    ratings = [a["ratings"] for a in paid if isinstance(a.get("ratings"), int)]
    out = {
        "term": row.get("term"),
        "status": row.get("status"),
        "result_count": row.get("result_count"),
        "apps_returned": row.get("apps_returned"),
        "window": len(apps),
        "paid": len(paid),
        "free": len(free),
        "median_paid_price": statistics.median(prices) if prices else None,
        "ratings_paid": sum(ratings) if ratings else 0,
        "median_ratings_paid": statistics.median(ratings) if ratings else None,
        "ratings_top1_paid": max(ratings) if ratings else 0,
    }
    return out


def main():
    rows = []
    for role, term in TERMS:
        row = fetch(term)
        row["role"] = role
        rows.append(row)
        print("fetched %-24s role=%-17s status=%s results=%s" % (
            term, role, row.get("status"), row.get("result_count")))
    reps = []
    for _role, term in REPEAT:
        row = fetch(term)
        base = next(r for r in rows if r["term"] == term)
        first5 = [a["trackId"] for a in (base.get("apps") or [])[:5]]
        again5 = [a["trackId"] for a in (row.get("apps") or [])[:5]]
        reps.append({"term": term,
                     "result_count_first": base.get("result_count"),
                     "result_count_second": row.get("result_count"),
                     "first5_identical": first5 == again5})
        print("repeat %-24s count %s -> %s  first5_identical=%s" % (
            term, base.get("result_count"), row.get("result_count"), first5 == again5))

    measured = [measure(r) for r in rows]
    by_term = {m["term"]: m for m in measured}
    pos = [by_term[t] for _r, t in TERMS if _r == "control_positive"]
    neg = [by_term[t] for _r, t in TERMS if _r == "control_negative"]
    diffs = [m for r, m in zip(rows, measured) if r["role"] == "difficulty"]

    g1 = all((m["paid"] >= 1 and (m["median_paid_price"] or 0) >= 0.99) for m in pos) and len(pos) == 2
    g2 = all((m["result_count"] == 0) for m in neg)
    g3 = sum(1 for m in diffs if m["paid"] >= 5) >= 4
    thin = [m for m in diffs if m["ratings_paid"] >= 100000 and m["paid"] <= 10]
    g4 = len(thin) >= 1
    g5 = all(r["first5_identical"] for r in reps) and all(
        r["result_count_first"] == r["result_count_second"] for r in reps)

    gates = {"G1_positive_controls": g1, "G2_negative_control": g2,
             "G3_money_exists": g3, "G4_thin_supply_high_demand": g4,
             "G5_fetch_reproducible": g5}
    out = {"experiment": "E194", "host_python": sys.version.split()[0], "window": WINDOW,
           "terms": TERMS, "measured": measured, "gates": gates,
           "thin_supply_rows": [m["term"] for m in thin],
           "repeat_checks": reps, "fetch_detail": [
               {"term": r["term"], "status": r.get("status"), "error": r.get("error"),
                "result_count": r.get("result_count"), "apps_returned": r.get("apps_returned"),
                "body_sha256": r.get("body_sha256")} for r in rows]}
    path = os.path.join(RAW, "scan.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2, sort_keys=True)

    print("\n%-24s %6s %6s %8s %12s %12s" % ("term", "paid", "free", "med$", "ratings_pd", "top1_pd"))
    for m in measured:
        print("%-24s %6s %6s %8s %12s %12s" % (
            m["term"], m["paid"], m["free"], m["median_paid_price"],
            m["ratings_paid"], m["ratings_top1_paid"]))
    print("")
    for k, v in sorted(gates.items()):
        print("%-30s %s" % (k, "PASS" if v else "FAIL"))
    print("thin-supply rows: %s" % (out["thin_supply_rows"] or "none"))
    print("wrote %s" % path)


if __name__ == "__main__":
    main()