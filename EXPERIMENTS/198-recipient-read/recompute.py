#!/usr/bin/env python3
"""E198 recompute -- rebuild analysis from committed raw captures only.

This verifies that the analysis.json can be reproduced from the bytes on disk
without re-querying the API. A judgement over fetched data that cannot be tied
to the bytes it was read from is not a measurement (F049, D061).
"""
import json
import os
import sys

import client

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")


def load_panel1_from_raw():
    """Reconstruct panel1.json from individual capture files."""
    rows = []
    for code in client.IT_CODES:
        recipients = []
        statuses = []
        unused_filters = []
        page = 1
        while True:
            capture_name = "recip_%s_p%d" % (code, page)
            json_path = os.path.join(RAW, capture_name + ".json")
            meta_path = os.path.join(RAW, capture_name + ".meta.json")
            if not (os.path.exists(json_path) and os.path.exists(meta_path)):
                break
            with open(json_path, "rb") as fh:
                raw = fh.read()
            with open(meta_path) as fh:
                meta = json.load(fh)
            st = meta["response"]["status"]
            statuses.append({"page": page, "status": st, "reused": meta["response"].get("reused", False)})
            if st != 200:
                break
            try:
                parsed = json.loads(raw.decode("utf-8", "replace"))
            except Exception:
                break
            results = parsed.get("results") or []
            recipients.extend(results)
            unused_filters.extend(client.unused_filter_messages(parsed))
            page_meta = parsed.get("page_metadata") or {}
            if not page_meta.get("hasNext", False):
                break
            page += 1

        total_amount = sum(r.get("amount", 0) for r in recipients)
        sorted_recips = sorted(recipients, key=lambda r: r.get("amount", 0), reverse=True)
        top10_amount = sum(r.get("amount", 0) for r in sorted_recips[:10])
        top10_share = top10_amount / total_amount if total_amount > 0 else 0

        names = {r.get("name", "") for r in recipients if r.get("name")}
        rows.append({
            "code": code,
            "recipient_count": len(recipients),
            "total_amount": total_amount,
            "top10_amount": top10_amount,
            "top10_share": top10_share,
            "recipients": recipients,
            "statuses": statuses,
            "unused_filters": unused_filters,
            "distinct_names": len(names),
        })
    return {"experiment": "E198", "panel": "A", "population_source": "E197 IT_CODES", "rows": rows}


def compute_gates(panel_data):
    rows = panel_data["rows"]
    g1_pass = True
    g1_details = {}
    for row in rows:
        code = row["code"]
        ok = (row["recipient_count"] > 0 and
              all(s["status"] == 200 for s in row["statuses"]))
        g1_details[code] = {"pass": ok, "recipient_count": row["recipient_count"],
                            "pages": len(row["statuses"])}
        if not ok:
            g1_pass = False

    all_names = set()
    g2_details = {}
    g2_pass = True
    for row in rows:
        code = row["code"]
        names = {r.get("name", "") for r in row["recipients"] if r.get("name")}
        all_names.update(names)
        top10_share = row["top10_share"]
        code_pass = top10_share <= 0.80
        g2_details[code] = {"top10_share": top10_share, "pass": code_pass,
                            "recipient_count": row["recipient_count"]}
        if not code_pass:
            g2_pass = False

    total_distinct = len(all_names)
    total_distinct_pass = total_distinct >= 20
    if not total_distinct_pass:
        g2_pass = False
    g2_details["total_distinct"] = {"count": total_distinct, "pass": total_distinct_pass}

    return {"G1": {"pass": g1_pass, "details": g1_details},
            "G2": {"pass": g2_pass, "details": g2_details}}


def main():
    panel_data = load_panel1_from_raw()
    gates = compute_gates(panel_data)

    # Load the committed analysis.json for comparison
    with open(os.path.join(RAW, "analysis.json")) as fh:
        committed = json.load(fh)

    # Compare gates
    gate_match = (gates["G1"]["pass"] == committed["gates"]["G1"]["pass"] and
                  gates["G2"]["pass"] == committed["gates"]["G2"]["pass"])

    # Compare per-code details
    detail_match = True
    for g in ("G1", "G2"):
        for code, d1 in gates[g]["details"].items():
            if code not in committed["gates"][g]["details"]:
                detail_match = False
                break
            d2 = committed["gates"][g]["details"][code]
            for k in d1:
                if k in d2 and d1[k] != d2[k]:
                    detail_match = False
                    break
            if not detail_match:
                break
        if not detail_match:
            break

    print("Gate match:", gate_match)
    print("Detail match:", detail_match)

    if gate_match and detail_match:
        print("RECOMPUTE: PASS — analysis.json reproduced from raw captures")
        return 0
    else:
        print("RECOMPUTE: FAIL — analysis.json diverges from raw captures")
        return 1


if __name__ == "__main__":
    sys.exit(main())