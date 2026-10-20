#!/usr/bin/env python3
"""E198 analysis -- compute gates from panel1.json and controls."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")


def load_panel1():
    path = os.path.join(RAW, "panel1.json")
    with open(path) as fh:
        return json.load(fh)


def load_controls():
    # Controls are run inline; we re-run them here for the analysis
    # But for now, we'll compute from panel1 data
    return {}


def compute_gates(panel_data):
    rows = panel_data["rows"]

    # G1: all five codes return well-formed, non-empty list with pagination
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

    # G2: vendor concentration
    # Total distinct recipients across five codes ≥ 20
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

    return {
        "G1": {"pass": g1_pass, "details": g1_details},
        "G2": {"pass": g2_pass, "details": g2_details},
    }


def main():
    panel_data = load_panel1()
    gates = compute_gates(panel_data)

    print("=== GATES ===")
    for g, v in gates.items():
        print("%s: %s" % (g, "PASS" if v["pass"] else "FAIL"))
        for k, d in v["details"].items():
            print("  %s: %s" % (k, d))

    # Write analysis.json
    out_path = os.path.join(RAW, "analysis.json")
    with open(out_path, "w") as fh:
        json.dump({"experiment": "E198", "gates": gates,
                   "panel_data": panel_data}, fh, indent=1, sort_keys=True)
    print("wrote %s" % out_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())