#!/usr/bin/env python3
"""E208: does category fragmentation predict newcomer entry in NIH SBIR?

Reads only raw/prior_years.json (the fetch fetch_prior.py committed). Writes
gates.json and per_category.csv. Gates G0-G4 are as declared in PROTOCOL.md
before the fetch; nothing here changes a threshold.

Stdlib only. The permutation test is seeded (20261021) and is the only random
component; it affects p, never a point estimate.
"""
import csv
import json
import os
import random
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw", "prior_years.json")

PRIMARY_WINDOW = list(range(2018, 2023))    # prior years, primary
SENSITIVITY_WINDOW = list(range(2014, 2023))  # prior years, sensitivity
OUTCOME_YEAR = 2023
MIN_ORGS = 10           # analysis population threshold (declared)
SEED = 20261021
PERMUTATIONS = 10000

# E207's committed census, for G0
E207 = {"rows": 368, "cat101_grants": 147, "cat101_grants_band": (132, 162),
        "cat101_orgs": 134, "cat101_orgs_band": (121, 147),
        "cat101_top5": 0.1159, "cat101_top5_band": (0.066, 0.166)}


def org_key(row):
    """Stable organization identity: external_org_id, else org_ipf_code."""
    org = row.get("organization") or {}
    return org.get("external_org_id") or org.get("org_ipf_code")


def org_name_key(row):
    org = row.get("organization") or {}
    return " ".join((org.get("org_name") or "").upper().split())


def categories_of(row):
    return [c for c in (row.get("spending_categories") or [])]


def top5_share(rows, keyfn):
    amounts = defaultdict(float)
    for r in rows:
        amounts[keyfn(r)] += r.get("award_amount") or 0
    total = sum(amounts.values())
    if total <= 0:
        return 0.0
    return sum(sorted(amounts.values(), reverse=True)[:5]) / total


def average_ranks(values):
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def pearson(xs, ys):
    n = len(xs)
    if n < 3:
        return 0.0
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = sum((x - mx) ** 2 for x in xs) ** 0.5
    dy = sum((y - my) ** 2 for y in ys) ** 0.5
    if dx == 0 or dy == 0:
        return 0.0
    return num / (dx * dy)


def spearman(xs, ys):
    return pearson(average_ranks(xs), average_ranks(ys))


def main():
    data = json.load(open(RAW))
    fy = {int(k): v for k, v in data.items()}
    rows_2023 = fy[OUTCOME_YEAR]["rows"]
    prior = [r for y in PRIMARY_WINDOW for r in fy[y]["rows"]]
    prior_all = [r for y in SENSITIVITY_WINDOW for r in fy[y]["rows"]]

    gates = {}

    # --- G0: reproduce the known census -------------------------------------
    c101 = [r for r in rows_2023 if 101 in categories_of(r)]
    c101_orgs_id = {org_key(r) for r in c101}
    c101_top5_id = top5_share(c101, org_key)
    c101_top5_name = top5_share(c101, org_name_key)
    g0 = {
        "fy2023_rows": len(rows_2023),
        "fy2023_rows_expected": E207["rows"],
        "cat101_grants": len(c101),
        "cat101_grants_band": list(E207["cat101_grants_band"]),
        "cat101_orgs": len(c101_orgs_id),
        "cat101_orgs_band": list(E207["cat101_orgs_band"]),
        "cat101_top5_by_id": round(c101_top5_id, 4),
        "cat101_top5_by_name": round(c101_top5_name, 4),
        "cat101_top5_band": list(E207["cat101_top5_band"]),
    }
    g0["pass"] = (
        len(rows_2023) == E207["rows"]
        and E207["cat101_grants_band"][0] <= len(c101) <= E207["cat101_grants_band"][1]
        and E207["cat101_orgs_band"][0] <= len(c101_orgs_id) <= E207["cat101_orgs_band"][1]
        and E207["cat101_top5_band"][0] <= c101_top5_id <= E207["cat101_top5_band"][1]
    )
    gates["G0_reproduces_census"] = g0

    # --- G1: identity coverage ---------------------------------------------
    def coverage(rows):
        have = sum(1 for r in rows if org_key(r))
        return have / len(rows) if rows else 0.0
    g1 = {"fy2023_coverage": round(coverage(rows_2023), 4),
          "prior_coverage": round(coverage(prior), 4),
          "threshold": 0.99}
    g1["pass"] = g1["fy2023_coverage"] >= 0.99 and g1["prior_coverage"] >= 0.99
    gates["G1_identity_coverage"] = g1

    # --- G2: per-year completeness -----------------------------------------
    years_checked = {}
    for y in PRIMARY_WINDOW:
        years_checked[y] = {"reported": fy[y]["reported_total"],
                            "fetched": fy[y]["fetched"],
                            "pass": fy[y]["reported_total"] == fy[y]["fetched"]}
    g2 = {"years": years_checked,
          "pass": all(v["pass"] for v in years_checked.values())}
    gates["G2_prior_window_complete"] = g2

    # --- the measurement (only meaningful if G0-G2 pass) --------------------
    def build(prior_rows, prior_years):
        prior_orgs = defaultdict(set)          # category -> orgs seen before
        prior_orgs_any = set()
        for r in prior_rows:
            for c in categories_of(r):
                prior_orgs[c].add(org_key(r))
            prior_orgs_any.add(org_key(r))
        by_cat = defaultdict(list)
        for r in rows_2023:
            for c in categories_of(r):
                by_cat[c].append(r)
        table = []
        for cat, rows in by_cat.items():
            orgs = {org_key(r) for r in rows}
            new_seg = {o for o in orgs if o not in prior_orgs.get(cat, set())}
            new_dom = {o for o in orgs if o not in prior_orgs_any}
            amounts = defaultdict(float)
            for r in rows:
                amounts[org_key(r)] += r.get("award_amount") or 0
            total = sum(amounts.values())
            top5 = (sum(sorted(amounts.values(), reverse=True)[:5]) / total
                    if total > 0 else 0.0)
            table.append({
                "category": cat,
                "grants": len(rows),
                "orgs": len(orgs),
                "top5_share": round(top5, 4),
                "fragmentation": round(1 - top5, 4),
                "segment_newcomers": len(new_seg),
                "segment_entrant_fraction": round(len(new_seg) / len(orgs), 4) if orgs else None,
                "domain_newcomers": len(new_dom),
                "domain_entrant_fraction": round(len(new_dom) / len(orgs), 4) if orgs else None,
                "window": "%d-%d" % (min(prior_years), max(prior_years)),
            })
        return sorted(table, key=lambda t: t["category"])

    table = build(prior, PRIMARY_WINDOW)
    table_sens = build(prior_all, SENSITIVITY_WINDOW)

    analysis = [t for t in table if t["orgs"] >= MIN_ORGS]
    xs = [t["fragmentation"] for t in analysis]
    ys = [t["segment_entrant_fraction"] for t in analysis]
    rho = spearman(xs, ys)

    rng = random.Random(SEED)
    extreme = 0
    for _ in range(PERMUTATIONS):
        shuffled = ys[:]
        rng.shuffle(shuffled)
        if spearman(xs, shuffled) >= rho:
            extreme += 1
    p_one_sided = (extreme + 1) / (PERMUTATIONS + 1)

    g3 = {"n_categories": len(analysis), "spearman_rho": round(rho, 4),
          "permutations": PERMUTATIONS, "seed": SEED,
          "p_one_sided": round(p_one_sided, 5),
          "thresholds": {"rho": 0.40, "p": 0.05}}
    g3["pass"] = rho >= 0.40 and p_one_sided < 0.05
    gates["G3_fragmentation_entry_association"] = g3

    c101_row = next((t for t in table if t["category"] == 101), None)
    g4 = {"category": 101,
          "segment_entrant_fraction":
              c101_row["segment_entrant_fraction"] if c101_row else None,
          "threshold": 0.30}
    g4["pass"] = bool(c101_row and
                      c101_row["segment_entrant_fraction"] is not None
                      and c101_row["segment_entrant_fraction"] >= 0.30)
    gates["G4_headline_category"] = g4

    analysis_sens = [t for t in table_sens if t["orgs"] >= MIN_ORGS]
    xs_s = [t["fragmentation"] for t in analysis_sens]
    ys_s = [t["segment_entrant_fraction"] for t in analysis_sens]
    sensitivity = {"window": "2014-2022", "n_categories": len(analysis_sens),
                   "spearman_rho": round(spearman(xs_s, ys_s), 4),
                   "completeness": {str(y): {
                       "reported": fy[y]["reported_total"],
                       "fetched": fy[y]["fetched"],
                       "pass": fy[y]["reported_total"] == fy[y]["fetched"]}
                       for y in SENSITIVITY_WINDOW if y not in PRIMARY_WINDOW},
                   "note": "declared sensitivity, not gated"}

    out = {
        "gates": gates,
        "analysis_population": {
            "threshold_min_orgs": MIN_ORGS,
            "n_categories": len(analysis),
            "categories": sorted(t["category"] for t in analysis),
        },
        "overall": {
            "fy2023_orgs_in_analysis":
                sum(t["orgs"] for t in analysis),
            "segment_newcomers_in_analysis":
                sum(t["segment_newcomers"] for t in analysis),
            "domain_newcomers_in_analysis":
                sum(t["domain_newcomers"] for t in analysis),
        },
        "per_category": table,
        "sensitivity": sensitivity,
        "all_gates_pass": all(g["pass"] for g in gates.values()),
    }
    with open(os.path.join(HERE, "gates.json"), "w") as f:
        json.dump(out, f, indent=1)
    with open(os.path.join(HERE, "per_category.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(table[0].keys()))
        w.writeheader()
        for t in table:
            w.writerow(t)

    for name, g in gates.items():
        print("%-42s %s" % (name, "PASS" if g["pass"] else "FAIL"), g)
    print("rho=%.4f p=%.5f n=%d | overall segment newcomers %d/%d | "
          "domain %d/%d" % (
              rho, p_one_sided, len(analysis),
              out["overall"]["segment_newcomers_in_analysis"],
              out["overall"]["fy2023_orgs_in_analysis"],
              out["overall"]["domain_newcomers_in_analysis"],
              out["overall"]["fy2023_orgs_in_analysis"]))
    print("sensitivity 2014-2022:", sensitivity)


if __name__ == "__main__":
    main()
