"""E211 — entry-survival measurement.

Freeze the design in ../PROTOCOL.md; this file only executes it. Standard
library only. Identity matching is on UEI; normalized-name matching runs
alongside as the I2 robustness estimate.

Usage:  python3 run.py            # writes results.json and raw/*.json
"""
import json
import os
import re
import sys
import time
import urllib.request

API = "https://api.usaspending.gov/api/v2"
AWARD = API + "/search/spending_by_award/"
RECIPIENT = API + "/search/spending_by_category/recipient/"
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

A_START, A_END = "2020-10-01", "2021-09-30"   # cohort window (FY20-21)
B_START, B_END = "2022-10-01", "2025-09-30"   # return window (FY23-25)
SMALL = 100_000.0
PAGE_CEILING = 50          # pages per query series, per PROTOCOL
REQUESTS = {"n": 0}


def post(url, payload, tries=3):
    REQUESTS["n"] += 1
    body = json.dumps(payload).encode()
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, data=body,
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode())
        except Exception as e:  # noqa: BLE001 - network retries, logged
            if attempt == tries - 1:
                raise
            sys.stderr.write("retry after %s\n" % e)
            time.sleep(2 * (attempt + 1))


def award_rows(code, start, end, first_page=1, n_pages=PAGE_CEILING):
    """Small funded awards, amount ascending, from the award-level endpoint."""
    rows = []
    censored = False
    page = first_page
    last = None
    while page < first_page + n_pages:
        data = post(AWARD, {
            "filters": {"time_period": [{"start_date": start, "end_date": end}],
                        "psc_codes": [code], "award_type_codes": ["A", "B", "C", "D"]},
            "fields": ["Award ID", "Recipient Name", "Recipient UEI",
                       "Award Amount", "Awarding Agency"],
            "page": page, "limit": 100, "sort": "Award Amount", "order": "asc"})
        results = data.get("results", [])
        if not results:
            break
        for r in results:
            amt = r.get("Award Amount") or 0.0
            if amt <= 0:
                continue
            if amt > SMALL:
                return rows, False          # walked past the small band: done
            rows.append({"uei": (r.get("Recipient UEI") or "").strip(),
                         "name": r.get("Recipient Name") or "",
                         "amount": amt,
                         "agency": r.get("Awarding Agency") or "",
                         "award_id": r.get("Award ID") or ""})
        last = results[-1].get("Award Amount") or 0.0
        if not data.get("page_metadata", {}).get("hasNext"):
            break
        page += 1
    else:
        censored = True                     # ceiling hit without passing $100k
    return rows, censored


def recipient_rows(code, start, end, n_pages=PAGE_CEILING):
    """Recipient aggregates (all sizes) for the return window."""
    rows = []
    page = 1
    while page <= n_pages:
        data = post(RECIPIENT, {
            "category": "recipient",
            "filters": {"time_period": [{"start_date": start, "end_date": end}],
                        "psc_codes": [code], "award_type_codes": ["A", "B", "C", "D"]},
            "page": page, "limit": 100, "sort": "amount", "order": "desc"})
        results = data.get("results", [])
        for r in results:
            rows.append({"uei": (r.get("uei") or "").strip(),
                         "name": r.get("name") or "",
                         "amount": r.get("amount") or 0.0})
        if not data.get("page_metadata", {}).get("hasNext"):
            return rows, False
        page += 1
    return rows, True


SUFFIXES = re.compile(r"\b(INC|INCORPORATED|LLC|LLP|LTD|CORP|CORPORATION|COMPANY|CO|THE)\b")
PUNCT = re.compile(r"[^A-Z0-9 ]+")


def norm(name):
    n = PUNCT.sub(" ", name.upper())
    n = SUFFIXES.sub(" ", n)
    return " ".join(n.split())


def save(name, obj):
    with open(os.path.join(RAW, name), "w") as f:
        json.dump(obj, f, indent=1, sort_keys=True)


def main():
    os.makedirs(RAW, exist_ok=True)
    out = {"windows": {"A": [A_START, A_END], "B": [B_START, B_END]},
           "codes": {}, "negative_control_6810": None}

    def cached(fname, fetch):
        path = os.path.join(RAW, fname)
        if os.path.exists(path):
            return json.load(open(path))
        obj = fetch()
        save(fname, obj)
        return obj

    cohort_a = {}
    for code in ("7030", "DA10", "DA01"):
        got = cached("A_%s.json" % code,
                     lambda c=code: dict(zip(("censored", "rows"),
                                             award_rows(c, A_START, A_END)),
                                         code=c))
        rows, cens = got["rows"], got["censored"]
        with_uei = sum(1 for r in rows if r["uei"])
        ueis = {r["uei"] for r in rows if r["uei"]}
        cohort_a[code] = ueis
        out["codes"][code] = {
            "cohort_awards": len(rows), "cohort_censored": cens,
            "cohort_uei_coverage": (with_uei / len(rows)) if rows else 0.0,
            "cohort_distinct_uei": len(ueis),
            "max_cohort_amount": max((r["amount"] for r in rows), default=0.0)}

    b_lists = {}
    for code in ("7030", "DA10", "DA01", "6810"):
        got = cached("B_%s.json" % code,
                     lambda c=code: dict(zip(("censored", "rows"),
                                             recipient_rows(c, B_START, B_END)),
                                         code=c))
        rows, cens = got["rows"], got["censored"]
        b_lists[code] = rows
        if code in out["codes"]:
            out["codes"][code]["b_recipients"] = len(rows)
            out["codes"][code]["b_censored"] = cens
        else:
            out["negative_control_6810"] = {"b_recipients": len(rows),
                                            "b_censored": cens}

    # survivor sets by UEI and by normalized name (I2 robustness estimate)
    b_uei = {code: {r["uei"]: r for r in rows if r["uei"]}
             for code, rows in b_lists.items()}
    b_name = {code: {norm(r["name"]): r for r in rows if norm(r["name"])}
              for code, rows in b_lists.items()}

    # 7030 cohort rows kept for the I3 audit and cross-market reporting
    a_rows = {code: json.load(open(os.path.join(RAW, "A_%s.json" % code)))["rows"]
              for code in ("7030", "DA10", "DA01")}

    for code in ("7030", "DA10", "DA01"):
        c = out["codes"][code]
        cohort = cohort_a[code]
        surv = cohort & set(b_uei[code])
        c.update({"survivors": sorted(surv),
                  "survival": (len(surv) / len(cohort)) if cohort else 0.0})
        # name-based estimate over distinct cohort names
        cn = {norm(r["name"]) for r in a_rows[code] if norm(r["name"])}
        surv_n = cn & set(b_name[code])
        c["survival_name_est"] = (len(surv_n) / len(cn)) if cn else 0.0
        # graduation: B aggregate > $100k
        grads = [u for u in surv if b_uei[code][u]["amount"] > SMALL]
        c["graduates"] = len(grads)
        c["graduation"] = (len(grads) / len(cohort)) if cohort else 0.0
        # net-positive return: B aggregate > $0 (deobligation nets to 0/negative)
        pos = [u for u in surv if b_uei[code][u]["amount"] > 0]
        c["survivors_net_positive"] = len(pos)
        c["survival_net_positive"] = (len(pos) / len(cohort)) if cohort else 0.0
        c["median_survivor_b_amount"] = sorted(
            b_uei[code][u]["amount"] for u in surv)[len(surv) // 2] if surv else 0.0

    # cross-market + negative control against the 7030 cohort
    c7 = out["codes"]["7030"]["survivors"]
    cross = {}
    for other in ("DA10", "DA01", "6810"):
        cross[other] = len(set(c7) & set(b_uei[other]))
    out["cross_market_7030_cohort"] = cross

    # I3 audit material: 10 random within-7030 matched pairs, with context
    import random
    random.seed(211)
    audit = []
    by_uei_a = {}
    for r in a_rows["7030"]:
        if r["uei"]:
            by_uei_a.setdefault(r["uei"], r)
    for u in random.sample(c7, min(10, len(c7))):
        audit.append({"uei": u, "a": by_uei_a.get(u), "b": b_uei["7030"].get(u)})
    out["audit_pairs_7030"] = audit

    save("results.json", out)
    print(json.dumps({k: v for k, v in out.items() if k != "audit_pairs_7030"},
                     indent=1, sort_keys=True))
    print("requests:", REQUESTS["n"])


if __name__ == "__main__":
    main()
