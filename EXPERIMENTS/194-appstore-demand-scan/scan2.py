#!/usr/bin/env python3
"""E194 panel 2 — relevance-controlled demand scan over the iTunes Search API.

Same terms and same bars as panel 1 (AMENDMENT-2). Three instrument changes:
whole returned set at limit=25, a negative control with no dictionary word, and
a per-row relevance check (G6).

One request per term. G5 re-fetches two terms.
"""
import hashlib
import json
import os
import re
import ssl
import statistics
import sys
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
os.makedirs(RAW, exist_ok=True)
UA = "think-free-research/0.1 (+repository demand scan, panel 2)"
LIMIT = 25

TERMS = [
    ("control_positive", "todo"),
    ("control_positive", "password manager"),
    ("control_negative", "zzqxqv glorbwump"),
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
REPEAT = ("pool care", "sourdough")
STOP = {"a", "an", "the", "for", "and", "to", "my", "in", "of", "with"}


def toks(s):
    return [t for t in re.split(r"[^a-z0-9]+", (s or "").lower()) if t and t not in STOP]


def fetch(term, limit=LIMIT):
    url = "https://itunes.apple.com/search?" + urllib.parse.urlencode(
        {"term": term, "entity": "software", "country": "us", "limit": limit})
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    row = {"term": term, "limit": limit, "url": url}
    try:
        with urllib.request.urlopen(req, timeout=30,
                                    context=ssl.create_default_context()) as r:
            body = r.read()
            row["status"] = r.status
    except urllib.error.HTTPError as e:
        row.update({"status": e.code, "result_count": None, "apps": []})
        return row
    except Exception as e:
        row.update({"status": None, "error": "%s: %s" % (type(e).__name__, e),
                    "result_count": None, "apps": []})
        return row
    data = json.loads(body.decode("utf-8", "replace"))
    row["result_count"] = data.get("resultCount")
    row["body_sha256"] = hashlib.sha256(body).hexdigest()
    row["apps"] = [{
        "trackId": a.get("trackId"), "name": a.get("trackName"),
        "seller": a.get("sellerName"), "price": a.get("price"),
        "formattedPrice": a.get("formattedPrice"), "ratings": a.get("userRatingCount"),
        "genre": a.get("primaryGenreName"),
    } for a in data.get("results", [])]
    return row


def measure(row):
    apps = row.get("apps") or []
    tt = set(toks(row.get("term")))
    rel = sum(1 for a in apps if tt & set(toks((a.get("name") or "") + " " + (a.get("seller") or ""))))
    paid = [a for a in apps if (a.get("price") or 0) > 0]
    prices = [a["price"] for a in paid if a.get("price") is not None]
    ratings = [a["ratings"] for a in paid if isinstance(a.get("ratings"), int)]
    top3 = sorted(paid, key=lambda a: -(a.get("ratings") or 0))[:3]
    return {
        "term": row.get("term"), "status": row.get("status"),
        "result_count": row.get("result_count"), "returned": len(apps),
        "relevance_rate": round(rel / len(apps), 4) if apps else None,
        "paid": len(paid), "free": len(apps) - len(paid),
        "median_paid_price": round(statistics.median(prices), 2) if prices else None,
        "ratings_paid": sum(ratings),
        "ratings_paid_excl_top1": sum(ratings) - (top3[0].get("ratings") or 0) if top3 else 0,
        "median_ratings_paid": statistics.median(ratings) if ratings else None,
        "top3_paid_by_ratings": [{"name": a["name"], "price": a["formattedPrice"],
                                  "ratings": a["ratings"]} for a in top3],
    }


def main():
    rows = []
    for role, term in TERMS:
        row = fetch(term)
        row["role"] = role
        rows.append(row)
        print("fetched %-24s %-6s status=%s resultCount=%s returned=%d" % (
            term, role, row.get("status"), row.get("result_count"), len(row.get("apps") or [])))
    reps = []
    for term in REPEAT:
        again = fetch(term)
        base = next(r for r in rows if r["term"] == term)
        reps.append({
            "term": term,
            "result_count_identical": base.get("result_count") == again.get("result_count"),
            "first5_identical": [a["trackId"] for a in base["apps"][:5]] ==
                                [a["trackId"] for a in again["apps"][:5]],
        })
        print("repeat %-24s resultCount %s -> %s identical5=%s" % (
            term, base.get("result_count"), again.get("result_count"),
            reps[-1]["first5_identical"]))

    measured = [measure(r) for r in rows]
    by = {m["term"]: m for m in measured}
    pos = [by[t] for r, t in TERMS if r == "control_positive"]
    neg = [by[t] for r, t in TERMS if r == "control_negative"]
    diffs = [m for r, m in zip(rows, measured) if r["role"] == "difficulty"]

    g1 = len(pos) == 2 and all(m["paid"] >= 1 and (m["median_paid_price"] or 0) >= 0.99 for m in pos)
    g2 = len(neg) == 1 and neg[0]["result_count"] == 0
    g3 = sum(1 for m in diffs if m["paid"] >= 5) >= 4
    thin = [m["term"] for m in diffs if m["ratings_paid"] >= 100000 and m["paid"] <= 10]
    g4 = len(thin) >= 1
    g5 = all(r["result_count_identical"] and r["first5_identical"] for r in reps)
    unrel = [m["term"] for m in diffs if (m["relevance_rate"] or 0) < 0.60]
    g6 = len(unrel) == 0

    gates = {"G1_positive_controls": g1, "G2_negative_control": g2, "G3_money_exists": g3,
             "G4_thin_supply_high_demand": g4, "G5_fetch_reproducible": g5,
             "G6_relevance_in_every_row": g6}
    out = {"experiment": "E194", "panel": 2, "limit": LIMIT, "gates": gates,
           "measured": measured, "thin_supply_rows": thin, "unreliable_rows": unrel,
           "repeat_checks": reps,
           "fetch_detail": [{"term": r["term"], "status": r.get("status"),
                             "result_count": r.get("result_count"), "error": r.get("error"),
                             "body_sha256": r.get("body_sha256")} for r in rows],
           "apps": [{"term": r["term"], "apps": r.get("apps") or []} for r in rows]}
    path = os.path.join(RAW, "scan2.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2, sort_keys=True)

    print("\n%-24s %5s %5s %5s %6s %8s %12s %12s" % (
        "term", "ret", "rel%", "paid", "med$", "medrat", "ratings_pd", "pd_ex_top1"))
    for m in measured:
        print("%-24s %5s %5s %5s %6s %8s %12s %12s" % (
            m["term"], m["returned"], m["relevance_rate"], m["paid"],
            m["median_paid_price"], m["median_ratings_paid"], m["ratings_paid"],
            m["ratings_paid_excl_top1"]))
    print("")
    for k, v in sorted(gates.items()):
        print("%-30s %s" % (k, "PASS" if v else "FAIL"))
    print("thin-supply rows: %s ; rows failing G6: %s" % (thin or "none", unrel or "none"))
    print("wrote %s" % path)


if __name__ == "__main__":
    main()