"""Complete 7030's window-A small-award band (the PROTOCOL's page-50 censor).

Extends raw/A_7030.json by paging the same ascending query until the amount
passes $100k or the series ends, deduplicating against rows already saved.
Also estimates incumbent contamination: how many cohort names appear in
E198's published top-10 vendor lists, and how many survivors hold >$1M
FY23-25 aggregates (a large-operator proxy).
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import run as e211  # noqa: E402 - reuse the frozen query helper

RAW = os.path.join(HERE, "raw")
MAX_PAGES = 120


def key(r):
    return (r["award_id"], r["uei"], r["amount"])


def complete_7030():
    path = os.path.join(RAW, "A_7030.json")
    got = json.load(open(path))
    have = {key(r) for r in got["rows"]}
    page = 1
    added = 0
    while page <= MAX_PAGES:
        data = e211.post(e211.AWARD, {
            "filters": {"time_period": [{"start_date": e211.A_START,
                                         "end_date": e211.A_END}],
                        "psc_codes": ["7030"],
                        "award_type_codes": ["A", "B", "C", "D"]},
            "fields": ["Award ID", "Recipient Name", "Recipient UEI",
                       "Award Amount", "Awarding Agency"],
            "page": page, "limit": 100, "sort": "Award Amount", "order": "asc"})
        results = data.get("results", [])
        if not results:
            break
        done = False
        for r in results:
            amt = r.get("Award Amount") or 0.0
            if amt <= 0:
                continue
            if amt > e211.SMALL:
                done = True
                break
            row = {"uei": (r.get("Recipient UEI") or "").strip(),
                   "name": r.get("Recipient Name") or "",
                   "amount": amt,
                   "agency": r.get("Awarding Agency") or "",
                   "award_id": r.get("Award ID") or ""}
            if key(row) not in have:
                have.add(key(row))
                got["rows"].append(row)
                added += 1
        if done:
            got["censored"] = False
            break
        if not data.get("page_metadata", {}).get("hasNext"):
            got["censored"] = False
            break
        page += 1
    json.dump(got, open(path, "w"), indent=1, sort_keys=True)
    print("pages walked: %d, rows added: %d, total rows: %d, censored: %s"
          % (page, added, len(got["rows"]), got["censored"]))


def contamination():
    top = set()
    # E198 raw recipient lists carry the published top-10 names
    for cand in ("EXPERIMENTS/198-recipient-read/raw",
                 "../../198-recipient-read/raw"):
        p = os.path.join(HERE, cand)
        if os.path.isdir(p):
            for fn in os.listdir(p):
                if not fn.endswith(".json"):
                    continue
                try:
                    doc = json.load(open(os.path.join(p, fn)))
                except Exception:  # noqa: BLE001
                    continue
                rows = doc if isinstance(doc, list) else doc.get("results", [])
                for r in rows[:10]:
                    n = r.get("name") or r.get("Recipient Name") or ""
                    if n:
                        top.add(e211.norm(n))
    print("top-vendor names loaded: %d" % len(top))
    for code in ("7030", "DA10", "DA01"):
        rows = json.load(open(os.path.join(RAW, "A_%s.json" % code)))["rows"]
        names = {e211.norm(r["name"]) for r in rows}
        hits = sorted(names & top)
        b = {r["uei"]: r for r in
             json.load(open(os.path.join(RAW, "B_%s.json" % code)))["rows"]
             if r["uei"]}
        cohort_ueis = {r["uei"] for r in rows if r["uei"]}
        big = [u for u in cohort_ueis
               if u in b and b[u]["amount"] > 1_000_000]
        print("%s: distinct cohort names=%d, matching E198 top-10 lists=%d %s| "
              "survivors with FY23-25 aggregate > $1M: %d (%.1f%% of cohort)"
              % (code, len(names), len(hits), hits, len(big),
                 100.0 * len(big) / max(1, len(cohort_ueis))))


if __name__ == "__main__":
    complete_7030()
    contamination()
