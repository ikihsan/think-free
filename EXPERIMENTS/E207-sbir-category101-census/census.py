#!/usr/bin/env python3
"""E207: complete R41/R42 census of FY2023 NIH RePORTER projects.

Recomputes E204's category-101 headline from the full population the API
reports, with no row cap and no sampling. Writes raw/census.json and
summary.json. Deterministic.
"""
import json
import os
import time
import urllib.request
from collections import Counter, defaultdict

URL = "https://api.reporter.nih.gov/v2/projects/search"
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
os.makedirs(RAW, exist_ok=True)


def fetch_all(activity_codes, fiscal_year=2023):
    """Fetch every project for the given activity codes, stopped by meta.total."""
    all_results = []
    seen = set()
    offset = 0
    reported_total = None
    while True:
        payload = json.dumps({
            "criteria": {"fiscal_years": [fiscal_year],
                         "activity_codes": activity_codes},
            "offset": offset,
            "limit": 100,
        }).encode()
        req = urllib.request.Request(
            URL, data=payload,
            headers={"User-Agent": "think-free-research/0.1",
                     "Content-Type": "application/json"},
            method="POST")
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.load(r)
        results = data.get("results", [])
        if reported_total is None:
            reported_total = data.get("meta", {}).get("total", 0)
        if not results:
            break
        for row in results:
            aid = row.get("appl_id")
            if aid not in seen:
                seen.add(aid)
                all_results.append(row)
        if len(all_results) >= reported_total:
            break
        offset += 100
        time.sleep(0.05)
    return all_results, reported_total


def main():
    grants, reported_total = fetch_all(["R41", "R42"])
    print("API reported total for FY2023 R41/R42: %d" % reported_total)
    print("Fetched distinct rows: %d" % len(grants))

    with open(os.path.join(RAW, "census.json"), "w") as f:
        json.dump({"reported_total": reported_total, "rows": grants}, f, indent=1)

    # Category -> rows whose spending_categories contains that code
    cat_rows = defaultdict(list)
    for g in grants:
        for c in (g.get("spending_categories") or []):
            cat_rows[c].append(g)

    def top5_share(rows):
        org_amt = defaultdict(float)
        for r in rows:
            org = (r.get("organization") or {}).get("org_name") or "UNKNOWN"
            org_amt[org] += (r.get("award_amount") or 0)
        total = sum(org_amt.values())
        if total <= 0:
            return 0.0, 0, 0.0
        top5 = sorted(org_amt.values(), reverse=True)[:5]
        return sum(top5) / total, len(org_amt), total

    summary = {"reported_total": reported_total, "fetched": len(grants),
               "categories": {}}
    for c, rows in cat_rows.items():
        share, n_org, total_amt = top5_share(rows)
        summary["categories"][str(c)] = {
            "grants": len(rows), "distinct_orgs": n_org,
            "total_amount": total_amt, "top5_share": share}

    # Rank categories by grant count
    ranked = sorted(summary["categories"].items(),
                    key=lambda kv: kv[1]["grants"], reverse=True)
    summary["ranked_by_grants"] = [
        {"category": c, **v} for c, v in ranked[:10]]

    with open(os.path.join(HERE, "summary.json"), "w") as f:
        json.dump(summary, f, indent=1)

    # Console report
    print("\nTop 10 categories by grant count (census):")
    for c, v in ranked[:10]:
        print("  cat %-6s grants=%-4d orgs=%-4d top5_share=%.4f" %
              (c, v["grants"], v["distinct_orgs"], v["top5_share"]))
    c101 = summary["categories"].get("101")
    if c101:
        print("\nCategory 101 census: grants=%d orgs=%d top5_share=%.4f total=$%.0f" %
              (c101["grants"], c101["distinct_orgs"], c101["top5_share"],
               c101["total_amount"]))
    else:
        print("\nCategory 101 ABSENT from census categories.")


if __name__ == "__main__":
    main()
