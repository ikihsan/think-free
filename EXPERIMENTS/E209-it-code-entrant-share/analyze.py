#!/usr/bin/env python3
"""
E209: Analyze entrant share for 5 IT PSC codes.

Reads raw/ files written by fetch.py. Computes per-code metrics and gates.
"""

import json
import os
import math
import random

EXP_RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

CODES = ["DA01", "DA10", "7A21", "7030", "D304"]
WINDOWS = ["current", "prior"]

# E198 reference values for G0
E198_REF = {
    "DA01": {"recipients": 3610, "top5_share": 0.345},
    "DA10": {"recipients": 3651, "top5_share": 0.358},
    "7A21": {"recipients": 3977, "top5_share": 0.489},
    "7030": {"recipients": 3917, "top5_share": 0.384},
    "D304": {"recipients": 1155, "top5_share": 0.576},
}

def load_window(code, window):
    """Load all pages for a code+window, return list of rows."""
    rows = []
    page = 1
    while True:
        fpath = os.path.join(EXP_RAW, f"{window}_{code}_p{page}.json")
        if not os.path.exists(fpath):
            break
        with open(fpath) as f:
            data = json.load(f)
        rows.extend(data.get("results", []))
        page += 1
    return rows

def obligation_by_id(rows):
    """Sum obligation per recipient_id; return (dict, missing_count)."""
    by_id = {}
    missing = 0
    for r in rows:
        rid = r.get("recipient_id")
        if not rid:
            missing += 1
            continue
        amt = r.get("amount") or 0.0
        by_id[rid] = by_id.get(rid, 0.0) + amt
    return by_id, missing

def top_k_share(by_id, k=5):
    """Top-k obligation share."""
    vals = sorted(by_id.values(), reverse=True)
    total = sum(vals)
    if total <= 0:
        return 0.0
    return sum(vals[:k]) / total

def spearman(xs, ys):
    """Spearman rho with average ranks; n>=3."""
    n = len(xs)
    if n < 3:
        return None

    def ranks(v):
        order = sorted(range(n), key=lambda i: v[i])
        r = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j + 1 < n and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1.0
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r

    rx, ry = ranks(xs), ranks(ys)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((rx[i] - mx) * (ry[i] - my) for i in range(n))
    dx = math.sqrt(sum((rx[i] - mx) ** 2 for i in range(n)))
    dy = math.sqrt(sum((ry[i] - my) ** 2 for i in range(n)))
    if dx == 0 or dy == 0:
        return None
    return num / (dx * dy)

def permutation_test(xs, ys, n_perm=10000, seed=20261021):
    """One-sided permutation test for Spearman rho >= observed."""
    rho_obs = spearman(xs, ys)
    if rho_obs is None:
        return None, None
    random.seed(seed)
    n = len(xs)
    count = 0
    for _ in range(n_perm):
        ys_perm = ys[:]
        random.shuffle(ys_perm)
        rho_perm = spearman(xs, ys_perm)
        if rho_perm is not None and rho_perm >= rho_obs:
            count += 1
    p = (count + 1) / (n_perm + 1)
    return rho_obs, p

def analyze_code(code):
    """Compute all metrics for one code."""
    cur_rows = load_window(code, "current")
    pri_rows = load_window(code, "prior")
    
    cur_by_id, cur_missing = obligation_by_id(cur_rows)
    pri_by_id, pri_missing = obligation_by_id(pri_rows)
    
    cur_ids = set(cur_by_id.keys())
    pri_ids = set(pri_by_id.keys())
    
    seg_new = cur_ids - pri_ids
    seg_frac = len(seg_new) / len(cur_ids) if cur_ids else 0.0
    
    # Domain newcomer: absent from ALL 5 codes' prior windows
    all_pri_ids = set()
    for c in CODES:
        p_rows = load_window(c, "prior")
        p_by_id, _ = obligation_by_id(p_rows)
        all_pri_ids.update(p_by_id.keys())
    
    dom_new = cur_ids - all_pri_ids
    dom_frac = len(dom_new) / len(cur_ids) if cur_ids else 0.0
    
    frag = 1.0 - top_k_share(cur_by_id, 5)
    top5_share = top_k_share(cur_by_id, 5)
    obligation = round(sum(cur_by_id.values()), 2)
    
    # G0: compare to E198
    e198 = E198_REF[code]
    recip_match = abs(len(cur_ids) - e198["recipients"]) / e198["recipients"] <= 0.05
    top5_match = abs(top5_share - e198["top5_share"]) <= 0.05
    
    # G1: identity coverage
    total_rows = len(cur_rows)
    id_coverage = 1.0 - (cur_missing / total_rows) if total_rows > 0 else 0.0
    
    return {
        "code": code,
        "current_rows": total_rows,
        "current_recipients": len(cur_ids),
        "prior_recipients": len(pri_ids),
        "segment_newcomers": len(seg_new),
        "segment_newcomer_fraction": round(seg_frac, 4),
        "domain_newcomer_fraction": round(dom_frac, 4),
        "fragmentation": round(frag, 4),
        "top5_share": round(top5_share, 4),
        "current_obligation": obligation,
        "current_missing_recids": cur_missing,
        "prior_missing_recids": pri_missing,
        "id_coverage": round(id_coverage, 4),
        "g0_recip_match": recip_match,
        "g0_top5_match": top5_match,
    }

def main():
    print("=" * 72)
    print("E209 ANALYSIS — IT PSC Code Entrant Share")
    print("=" * 72)
    
    all_results = []
    for code in CODES:
        print(f"Analyzing {code}...", flush=True)
        result = analyze_code(code)
        all_results.append(result)
    
    # Print per-code results
    print("\n" + "=" * 72)
    print("PER-CODE METRICS")
    print("=" * 72)
    print(f"{'code':<8} {'cur_rows':>8} {'cur_rec':>7} {'pri_rec':>7} {'seg_new':>7} {'seg_frac':>8} {'dom_frac':>8} {'frag':>6} {'top5':>6} {'id_cov':>6}")
    print("-" * 72)
    for r in all_results:
        print(f"{r['code']:<8} {r['current_rows']:>8} {r['current_recipients']:>7} {r['prior_recipients']:>7} {r['segment_newcomers']:>7} {r['segment_newcomer_fraction']:>8.4f} {r['domain_newcomer_fraction']:>8.4f} {r['fragmentation']:>6.4f} {r['top5_share']:>6.4f} {r['id_coverage']:>6.4f}")
    
    # Gates
    print("\n" + "=" * 72)
    print("GATE VERDICTS")
    print("=" * 72)
    
    # G0: Reproduce E198
    g0_pass = all(r["g0_recip_match"] and r["g0_top5_match"] for r in all_results)
    print(f"G0 reproduce E198: {'PASS' if g0_pass else 'FAIL'}")
    for r in all_results:
        status = "✓" if r["g0_recip_match"] and r["g0_top5_match"] else "✗"
        print(f"  {status} {r['code']}: recipients {r['current_recipients']} vs {E198_REF[r['code']]['recipients']}, top-5 {r['top5_share']:.4f} vs {E198_REF[r['code']]['top5_share']:.4f}")
    
    # G1: Identity coverage
    g1_pass = all(r["id_coverage"] >= 0.99 for r in all_results)
    print(f"\nG1 identity coverage (≥0.99): {'PASS' if g1_pass else 'FAIL'}")
    for r in all_results:
        status = "✓" if r["id_coverage"] >= 0.99 else "✗"
        print(f"  {status} {r['code']}: {r['id_coverage']:.4f} ({r['current_missing_recids']} missing of {r['current_rows']})")
    
    # G2: Prior window fetched (check all 5 prior years per code)
    # The prior window is FY2018-2022 as a single query, not per-year.
    # We verify all 5 codes returned data in prior window.
    g2_pass = all(r["prior_recipients"] > 0 for r in all_results)
    print(f"\nG2 prior window fetched (all 5 codes have prior recipients): {'PASS' if g2_pass else 'FAIL'}")
    for r in all_results:
        status = "✓" if r["prior_recipients"] > 0 else "✗"
        print(f"  {status} {r['code']}: {r['prior_recipients']} prior recipients")
    
    # G3: Fragmentation → Entry (kill gate)
    frags = [r["fragmentation"] for r in all_results]
    seg_fracs = [r["segment_newcomer_fraction"] for r in all_results]
    rho, p = permutation_test(frags, seg_fracs)
    g3_pass = (rho is not None) and (rho >= 0.40) and (p < 0.05)
    print(f"\nG3 fragmentation → entry (kill gate): {'PASS' if g3_pass else 'FAIL'}")
    print(f"  Spearman ρ = {rho:.4f}" if rho is not None else "  Spearman ρ = None")
    print(f"  One-sided permutation p = {p:.4f}" if p is not None else "  p = None")
    print(f"  Thresholds: ρ ≥ 0.40, p < 0.05")
    
    # G4: Code-level entry (≥ 0.30 for at least 1 code)
    g4_pass = any(r["segment_newcomer_fraction"] >= 0.30 for r in all_results)
    print(f"\nG4 code-level entry (≥0.30 for ≥1 code): {'PASS' if g4_pass else 'FAIL'}")
    for r in all_results:
        status = "✓" if r["segment_newcomer_fraction"] >= 0.30 else "✗"
        print(f"  {status} {r['code']}: {r['segment_newcomer_fraction']:.4f}")
    
    # Overall
    print("\n" + "=" * 72)
    print("OVERALL")
    print("=" * 72)
    all_gates = {"G0": g0_pass, "G1": g1_pass, "G2": g2_pass, "G3": g3_pass, "G4": g4_pass}
    for g, v in all_gates.items():
        print(f"  {g}: {'PASS' if v else 'FAIL'}")
    overall = all(all_gates.values())
    print(f"\nAll gates: {'PASS' if overall else 'FAIL'}")
    if not g3_pass:
        print("KILL GATE (G3) FIRED — fragmentation does not predict entry.")
    
    # Write outputs
    with open(os.path.join(OUT_DIR, "gates.json"), "w") as f:
        json.dump({
            "gates": all_gates,
            "rho": rho,
            "p": p,
            "n_codes": len(CODES),
        }, f, indent=2)
    
    with open(os.path.join(OUT_DIR, "per_category.csv"), "w") as f:
        f.write("code,current_recipients,prior_recipients,segment_newcomers,segment_newcomer_fraction,domain_newcomer_fraction,fragmentation,top5_share,current_obligation,id_coverage\n")
        for r in sorted(all_results, key=lambda x: x["code"]):
            f.write(f"{r['code']},{r['current_recipients']},{r['prior_recipients']},{r['segment_newcomers']},{r['segment_newcomer_fraction']},{r['domain_newcomer_fraction']},{r['fragmentation']},{r['top5_share']},{r['current_obligation']},{r['id_coverage']}\n")
    
    # Sensitivity: nine-year prior window (FY2014-2022) - not gated, post-hoc
    print("\n" + "=" * 72)
    print("SENSITIVITY (post-hoc, not gated): nine-year prior window not tested")
    print("=" * 72)
    print("  USAspending API time_period supports single range; FY2014-2022 would be")
    print("  a separate query. Not implemented in this analysis.")
    
    return 0 if overall else 1

if __name__ == "__main__":
    exit(main())