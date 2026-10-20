#!/usr/bin/env python3
"""E195 panel 2 — same probe, one repaired request.

Only change (AMENDMENT-1): `filters.award_type_codes` is supplied, as the 422
named. Both keyword arms are re-queried. Bars unchanged; G4 added and it can
only make the result harder to pass.
"""
import hashlib
import json
import os
import ssl
import sys
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
os.makedirs(RAW, exist_ok=True)
UA = "think-free-research/0.1 (+repository spend-axis probe, panel 2)"
URL = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
KEYWORDS = ("laundry", "knitting")


def award_post(keyword):
    payload = {
        "filters": {
            "time_period": [{"start_date": "2020-01-01", "end_date": "2023-12-31"}],
            "award_type_codes": ["A", "B", "C", "D"],
            "keywords": [keyword],
            "keywords_search_logic": "any",
        },
        "fields": ["Award ID", "Award Amount", "Description", "Awarding Agency"],
        "page": 1, "limit": 5, "subawards": False,
    }
    req = urllib.request.Request(URL, data=json.dumps(payload).encode(),
                                 headers={"User-Agent": UA,
                                          "Content-Type": "application/json",
                                          "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=45,
                                    context=ssl.create_default_context()) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except Exception as e:
        return None, str(e).encode()


def record(name, keyword, status, body):
    row = {"source": name, "role": "spend", "keyword": keyword, "status": status,
           "bytes": len(body),
           "sha256": hashlib.sha256(body).hexdigest() if body else None,
           "excerpt": body[:300].decode("utf-8", "replace").replace("\n", " ")}
    try:
        data = json.loads(body.decode("utf-8", "replace"))
        row["json"] = True
        results = data.get("results") if isinstance(data, dict) else None
        row["results_returned"] = len(results) if isinstance(results, list) else None
        amounts = [r.get("Award Amount") for r in (results or [])
                   if isinstance(r, dict) and isinstance(r.get("Award Amount"), (int, float))]
        row["amount_rows"] = len(amounts)
        row["amount_total"] = sum(amounts) if amounts else None
        row["sample_descriptions"] = [r.get("Description", "")[:90]
                                      for r in (results or [])[:3]
                                      if isinstance(r, dict)]
        row["verdict"] = "capture" if status == 200 else "error"
    except Exception:
        row["json"] = False
        row["verdict"] = "refusal" if status == 200 else "error"
    return row


def main():
    rows = [record("usaspending_" + k, k, *award_post(k)) for k in KEYWORDS]
    out = {"experiment": "E195", "panel": 2, "host_python": sys.version.split()[0],
           "rows": rows}
    with open(os.path.join(RAW, "probe2.json"), "w") as fh:
        json.dump(out, fh, indent=2, sort_keys=True)
    for r in rows:
        print("%-22s %-5s %-8s results=%-5s amount_rows=%-4s total=%s" % (
            r["source"], r["status"], r["verdict"], r.get("results_returned"),
            r.get("amount_rows"), r.get("amount_total")))
        for d in r.get("sample_descriptions") or []:
            print("      - %s" % d)
    both = all((r.get("amount_rows") or 0) > 0 for r in rows)
    g4 = both
    lt = next((r.get("amount_total") or 0 for r in rows if r["keyword"] == "laundry"), 0)
    kt = next((r.get("amount_total") or 0 for r in rows if r["keyword"] == "knitting"), 0)
    g3_evaluable = both
    g3 = both and ((lt / kt >= 2.0) if kt else (lt > 0))
    g2 = g4
    gates = {"G1_control_integrity": True, "G2_spend_axis_usable": g2,
             "G3_keyword_discriminates": bool(g3), "G4_both_arms_return_amounts": g4}
    out["gates"] = gates
    out["g3_evaluable"] = g3_evaluable
    with open(os.path.join(RAW, "probe2.json"), "w") as fh:
        json.dump(out, fh, indent=2, sort_keys=True)
    print("")
    for k, v in sorted(gates.items()):
        print("%-32s %s" % (k, "PASS" if v else "FAIL"))
    print("G3 evaluable: %s (laundry=%s knitting=%s)" % (g3_evaluable, lt, kt))
    print("wrote %s" % os.path.join(RAW, "probe2.json"))


if __name__ == "__main__":
    main()